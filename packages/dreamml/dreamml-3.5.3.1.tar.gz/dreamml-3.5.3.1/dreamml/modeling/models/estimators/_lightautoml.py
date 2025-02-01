"""
Обертка для LightAutoML
"""

import logging
import time
from typing import Dict, Any, List, Optional

import numpy as np
import pandas as pd


from lightautoml.tasks import Task
from lightautoml.automl.presets.tabular_presets import TabularAutoML

from sklearn.metrics import roc_auc_score

from dreamml.logging import get_logger
from dreamml.modeling.models.estimators import BaseModel


_logger = get_logger(__name__)


def gini(y_true, y_pred):
    return 2 * roc_auc_score(y_true, y_pred) - 1


class LAMA(BaseModel):
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

    # lambda y_true, y_pred: 2 * roc_auc_score(y_true, y_pred) -1)

    def __init__(
        self,
        estimator_params: Dict[str, Any],
        task: str,
        used_features: List[str],
        categorical_features: List[str] = None,
        metric_name=None,
        metric_params=None,
        weights=None,
        lama_time=None,
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
            train_logger=train_logger,
            **params,
        )
        self.model_name = "LAMA"
        self.timeout = lama_time
        self.estimator_class = self.get_estimator()
        self.fitted = False

    def get_estimator(self) -> TabularAutoML:
        if self.task == "binary":
            estimator = TabularAutoML(
                Task(
                    name="binary",
                    metric=self.eval_metric,
                ),
                timeout=self.timeout,
            )
        elif self.task == "regression":
            estimator = TabularAutoML(
                Task(
                    name="reg",
                    loss=self.params["loss_function"],
                    metric=self.eval_metric,
                ),
                timeout=self.timeout,
            )
        elif self.task == "multiclass":
            estimator = TabularAutoML(
                Task(
                    name="multiclass",
                    loss="crossentropy",
                    metric="crossentropy",
                ),
                timeout=self.timeout,
            )
        else:
            raise NotImplementedError(f"{self.task} is not supported for LAMA.")

        return estimator

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
        _logger.info(
            f"{time.ctime()}, start fitting LightAutoML, "
            f"train.shape: {data.shape[0]} rows, {data.shape[1]} cols.",
        )
        dtrain = pd.concat([data, target], axis=1)
        self.estimator = self.estimator_class
        self.estimator.fit_predict(dtrain, roles={"target": target.name}, verbose=1)

        used_features = self.estimator.get_feature_scores("fast")
        if used_features is None:
            self.used_features = data.columns.tolist()
        else:
            self.used_features = list(used_features.iloc[:, 0])

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

        prediction = self.estimator.predict(data)

        if self.task in ["binary", "regression"]:
            return prediction.data[:, 0]
        elif self.task == "multiclass":
            prediction = self.estimator.predict(data)
            return prediction.data
        else:
            raise ValueError(f"Задача {self.task} не поддерживается.")