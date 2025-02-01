from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Any, Tuple, List, Dict, Optional, Union
import warnings
import logging
import time

import numpy as np
import pandas as pd

from dreamml.features.feature_extraction._transformers import LogTargetTransformer
from dreamml.logging.logger import CombinedLogger
from dreamml.logging import get_logger
from dreamml.modeling.metrics import BaseMetric
from dreamml.modeling.metrics.metrics_mapping import metrics_mapping
from dreamml.utils.errors import MissedColumnError
from dreamml.utils.warnings import DMLWarning

_logger = get_logger(__name__)


class BaseModel(ABC):
    model_name: str = None
    """
    Класс базовой обёртки над алгоритмами машинного обучения

    Parameters
    ----------
    params : dict
        Словарь с конфигурациями для обёртки модели

    Attributes
    ----------
    params : dict
        Словарь с гиперпараметрами
    task : str
        Название задачи (regression, binary, multi, ...)
    model_name : str
        Название алгоритма (xgboost, lightgbm ...)
    used_features : list
        Список фич отобранных исходя из значений конкретной метрики
    estimator_class: dspl.models.new_wrappers.BaseModel
        Класс модели (LightGBMModel, XGBoostModel, ..)
    estimator : callable
        Экземпляр обученной модели.
    categorical_features : list
        Список категориальных фич
    """

    def __init__(
        self,
        estimator_params: Dict[str, Any],
        task: str,
        used_features: List[str] = None,
        categorical_features: List[str] = None,
        metric_name=None,
        metric_params: Dict = None,
        weights=None,
        target_with_nan_values: bool = False,
        log_target_transformer: LogTargetTransformer = None,
        parallelism: int = -1,
        train_logger: Optional[logging.Logger] = None,
        text_features: List[str] = None,
        **params,
    ):
        self.params = deepcopy(estimator_params)

        self.task = task
        self.used_features = used_features

        if categorical_features is not None and self.used_features is not None:
            categorical_features = list(
                set(categorical_features) & set(self.used_features)
            )
        self.categorical_features = categorical_features
        self.text_features = text_features

        self.weights = weights
        self.target_with_nan_values = target_with_nan_values
        self.log_target_transformer = log_target_transformer
        self.parallelism = parallelism

        self.metric_name = metric_name
        self.metric_params = metric_params.copy()

        self.eval_metric: BaseMetric = metrics_mapping[self.params["eval_metric"]](
            self.model_name,
            task=self.task,
            target_with_nan_values=self.target_with_nan_values,
            **self.metric_params,
        )
        self.objective: BaseMetric = metrics_mapping[self.params["objective"]](
            self.model_name,
            task=self.task,
            target_with_nan_values=self.target_with_nan_values,
            **self.metric_params,
        )

        self.estimator_class = None
        self.estimator = None

        self.vectorization_name = params.pop("vectorization_name", None)
        self.text_augmentations, self.aug_p = params.pop(
            "augmentation_params", (None, None)
        )

        if len(params) > 0:
            warnings.warn(
                f"{params=} are passed to model but not used.",
                DMLWarning,
                stacklevel=2,
            )
        self.fillna_value: int = 0
        self.fitted = False

        self._logger = train_logger

    def _pre_fit(self, data, *eval_set):
        if self.eval_metric.is_resetting_indexes_required:
            self.eval_metric.set_indexes(train=data.index, valid=eval_set[0].index)

        data = self.validate_input_data(data)

        new_eval_set = []
        for i in range(len(eval_set)):
            if i % 2 == 0:
                new_eval_set.append(self.validate_input_data(eval_set[i]))
            else:
                new_eval_set.append(eval_set[i])

        logger = self._logger or _logger
        logger.info(
            f"{time.ctime()}, start fitting {self.model_name}-Model, "
            f"train.shape: {data.shape[0]} rows, {data.shape[1]} cols.\n"
        )
        return data, tuple(new_eval_set)

    @abstractmethod
    def fit(self, data, target, *eval_set):
        """
        Абстрактный метод - обучение модели на данных (data, target).
        """
        pass

    @abstractmethod
    def transform(self, data):
        """
        Абстрактный метод - применение модели к данным data.
        """
        pass

    def validate_input_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Проверка входных данных data на наличие требуемых признаков.
        Если ожидаемые признаки отсутствуют в наборе данных, то
        возбуждается MissedColumnError.

        Parameters
        ----------
        data: pandas.DataFrame, shape = [n_samples, n_features]
            Матрица признаков для проверки.

        Returns
        -------
        data_validated: pandas.DataFrame
            Матрица признаков, содержащая требуемые признаки.

        """
        if self.used_features:
            missed_features = list(set(self.used_features) - set(data.columns))
            if missed_features:
                raise MissedColumnError(f"Missed " f"{list(missed_features)} columns.")
            return data[self.used_features]

        return data

    def evaluate_and_print(self, **eval_sets):
        """
        Печать в стандартный поток вывода оценки качества модели на eval_sets
        Для задач классификации используется метрика GINI
        Для задачи регрессии метрики MAE, R2, RMSE
        В словаре metrics под ключом названия метрики
        содержится функция её расчёта

        Parameters
        ----------
        eval_sets: Dict[string, Tuple[pandas.DataFrame, pandas.Series]]
            Словарь, где ключ - название выборки, значение - кортеж с
            матрицей признаков и вектором истинных ответов.
        """
        metrics_to_eval = {}

        if self.task in ["binary", "multiclass", "multilabel"]:
            metrics_to_eval["GINI"] = metrics_mapping["gini"](
                task=self.task,
                target_with_nan_values=self.target_with_nan_values,
                **self.metric_params,
            )

        elif self.task in ["regression", "timeseries"]:
            metrics_to_eval = {
                "MAE": metrics_mapping["mae"](task=self.task),
                "R2": metrics_mapping["r2"](task=self.task),
                "RMSE": metrics_mapping["rmse"](task=self.task),
            }

        if self.eval_metric.name.upper() not in metrics_to_eval:
            metrics_to_eval[self.eval_metric.name.upper()] = self.eval_metric
        if self.objective.name.upper() not in metrics_to_eval:
            metrics_to_eval[self.objective.name.upper()] = self.objective

        for sample in eval_sets:
            data, y_true = eval_sets[sample]
            y_pred = self.transform(data)

            scores = {}
            for name, metric in metrics_to_eval.items():
                try:
                    scores[name] = metric(y_true, y_pred)
                except (ValueError, KeyError, IndexError):
                    scores[name] = np.nan

            metrics_output = ", ".join(
                [f"{name} = {value:.2f}" for name, value in scores.items()]
            )
            output_per_sample = f"{sample}-score: \t {metrics_output}"

            logger = CombinedLogger([self._logger, _logger])
            logger.info(output_per_sample)

    @property
    def check_is_fitted(self):
        """
        Проверка была ли обучена модель.
        Если проверка не пройдена - возбуждается исключение NotFittedError.
        """
        if not bool(self.estimator):
            msg = (
                "This estimator is not fitted yet. Call 'fit' with"
                "appropriate arguments before using this estimator."
            )
            raise NotFittedError(msg)
        return True

    def _fill_nan_values(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Метод для заполнения NaN значений.
        Используем для log_reg, linear_reg, поскольку данные модели
        не имеют автоматической предобработки NaN значений, в отличие
        от catboost, xgboost, lightgbm
        """
        data = data.fillna(value=self.fillna_value)
        return data