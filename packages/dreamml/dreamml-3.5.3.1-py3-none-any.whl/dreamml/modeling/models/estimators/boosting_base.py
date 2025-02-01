import warnings
from abc import abstractmethod
import time
from typing import Any, Tuple, List, Dict, Union

import pandas as pd
from sklearn.exceptions import NotFittedError

from dreamml.logging import get_logger
from dreamml.modeling.models.estimators import BaseModel
from dreamml.modeling.models.estimators._multioutput_wrappers import (
    OneVsRestClassifierWrapper,
)
from dreamml.features.feature_extraction._transformers import LogTargetTransformer

_logger = get_logger(__name__)


class BoostingBaseModel(BaseModel):
    model_name: str = None

    """
    Класс базовой обёртки над алгоритмами boosting

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
    estimator_class: dspl.models.new_wrappers.BoostingBaseModel
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
        **params,
    ):
        super().__init__(
            estimator_params=estimator_params,
            task=task,
            used_features=used_features,
            categorical_features=categorical_features,
            metric_name=metric_name,
            metric_params=metric_params,
            weights=weights,
            target_with_nan_values=target_with_nan_values,
            log_target_transformer=log_target_transformer,
            parallelism=parallelism,
            **params,
        )

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

    def _create_eval_set(
        self, data: pd.DataFrame, target: pd.Series, *eval_set, asnumpy: bool = False
    ) -> List[Tuple[pd.DataFrame]]:
        """
        Создание eval_set в sklearn-формате.
        """
        data = self.validate_input_data(data)
        if eval_set:
            valid_data = self.validate_input_data(eval_set[0])
            if self.task == "regression" and isinstance(
                self.log_target_transformer, LogTargetTransformer
            ):
                return [
                    (data, target),
                    (valid_data, self.log_target_transformer.transform(eval_set[1])),
                ]
            return [(data, target), (valid_data, eval_set[1])]

        return [(data, target)]

    @staticmethod
    @abstractmethod
    def _get_best_iteration(estimator) -> int:
        raise NotImplementedError

    @property
    def best_iteration(self) -> Union[int, List[int]]:
        if isinstance(self.estimator, OneVsRestClassifierWrapper):
            best_iter: List[int] = self.estimator.best_iteration
        else:
            best_iter: int = self._get_best_iteration(self.estimator)

        if best_iter is None:
            best_iter = 0

        return best_iter


class MissedColumnError(IndexError):
    """
    Класс для идентификации ошибки несоответствия
    ожидаемых и полученных столбцов в pandas.DataFrame
    """

    pass