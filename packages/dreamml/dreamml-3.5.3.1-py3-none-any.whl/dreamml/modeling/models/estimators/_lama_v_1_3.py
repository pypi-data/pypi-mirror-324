"""
Обертка для новой версии WhiteBox AutoML (22.03.22)
"""

import time
import logging
from typing import Dict, Any, List, Optional

import numpy as np
import pandas as pd

from autowoe import AutoWoE

from dreamml.logging import get_logger
from dreamml.modeling.models.estimators import BaseModel

_logger = get_logger(__name__)


class WBAutoML(BaseModel):
    model_name = "WBAutoML"

    """
    Модель WhiteBox AutoML со стандартизованным API для DreamML.

    Parameters
    ----------
    estimator_params : dict
        Словарь с гиперпараметрами
    used_features : list
        Список фич отобранных исходя из значений конкретной метрики
    params : dict
        Словарь с дополнительными параметрами (optional_params, ...)

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
    fitted : bool
        Бала ли обучена модель, то есть вызван метод fit.
        True - да, False - нет

    """

    def __init__(
        self,
        estimator_params: Dict[str, Any],
        task: str,
        used_features: List[str],
        categorical_features: List[str] = None,
        metric_name=None,
        metric_params=None,
        weights=None,
        train_logger: Optional[logging.Logger] = None,
        **params,
    ):
        super().__init__(
            estimator_params,
            task,
            used_features,
            categorical_features,
            metric_name,
            metric_params,
            weights=weights,
            **params,
            train_logger=train_logger,
        )
        self.estimator_class = self._estimators.get(self.task)

    @property
    def _estimators(self):
        estimators = {
            "binary": AutoWoE(task="BIN", **self.params),
            "regression": AutoWoE(task="REG", **self.params),
        }
        return estimators

    def prepare_dtypes(self, data: pd.DataFrame, target_name: str) -> dict:
        """
        Подготовка типов данных для передачи в модель.

        Parameters
        ----------
        data: pd.DataFrame, shape = [n_samples, n_features]
            Набор данных для обучения модели.

        target_name: str
            Название целевой переменной.

        Returns
        -------
        features_types: Dict[str: str]
            Словарь, ключ - название признака,
            значение - тип признака.

        """
        if not self.categorical_features:
            self.categorical_features = {}

        num_features = set(data.columns) - set(self.categorical_features)
        num_features = num_features - set([target_name])

        cat_features = {x: "cat" for x in self.categorical_features}
        num_features = {x: "real" for x in num_features}

        return dict(**num_features, **cat_features)

    def _create_fit_params(self, data: pd.DataFrame, target: pd.Series):
        """
        Создание параметров обучения в autowoe-формате.

        """
        data = self.validate_input_data(data)
        features_type = self.prepare_dtypes(data, target.name)

        params = {
            "features_type": features_type,
            "target_name": target.name,
        }

        return params

    def fit(self, data: pd.DataFrame, target: pd.Series, *eval_set) -> None:
        """
        Обучение модели на данных data, target.

        Parameters
        ----------
        data: pandas.DataFrame, shape = [n_samples, n_features]
            Матрица признаков (обучающая выборка).

        target: pandas.Series, shape = [n_samples, ]
            Вектор целевой переменной.

        """
        data = self.validate_input_data(data)
        fit_params = self._create_fit_params(data, target)
        _logger.info(
            f"{time.ctime()}, start fitting WhiteBox AutoML, "
            f"train.shape: {data.shape[0]} rows, {data.shape[1]} cols."
        )
        dtrain = pd.concat([data, target], axis=1)
        self.estimator = self.estimator_class
        self.estimator.fit(train=dtrain, **fit_params)
        self.used_features = self.estimator.features_fit.index.tolist()
        self.fitted = True

    def transform(self, data: pd.DataFrame) -> np.array:
        """
        Применение обученной модели к данным data.
        Для применения модели должен быть ранее вызван метод fit
        и создан self.estimator. Если метод fit не был вызван, то
        будет возбуждено исключение .

        Parameters
        ----------
        data: pandas.DataFrame, shape = [n_samples, n_features]
            Матрица признаков (выборка для применения модели).

        Returns
        -------
        prediction: numpy.array, shape = [n_samples, ]
            Вектор с прогнозами модели на данных data.

        """
        if self.task == "binary":
            prediction = self.estimator.predict_proba(data)
        elif self.task == "regression":
            prediction = self.estimator.predict(data)
        else:
            raise ValueError(f"{self.task} task is not supported.")

        return prediction