import logging
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple

from sklearn.linear_model import LogisticRegression

from dreamml.modeling.models.estimators import BaseModel
from dreamml.features.feature_extraction._transformers import LogTargetTransformer
from dreamml.utils.errors import MissedColumnError


class LogRegModel(BaseModel):
    model_name = "log_reg"

    """
    Модель LogReg со стандартизованным API для DreamML

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
        Была ли обучена модель, то есть был вызван метод fit.
        True - да, False - нет

    """

    def __init__(
        self,
        estimator_params: Dict[str, Any],
        task: str,
        used_features: List[str],
        categorical_features: List[str],
        metric_name,
        metric_params,
        weights=None,
        target_with_nan_values: bool = False,
        log_target_transformer: LogTargetTransformer = None,
        parallelism: int = -1,
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
            target_with_nan_values=target_with_nan_values,
            log_target_transformer=log_target_transformer,
            parallelism=parallelism,
            train_logger=train_logger,
            **params,
        )
        self.estimator_class = self._estimators.get(self.task, LogisticRegression)

    @property
    def _estimators(self):
        """
        Словарь с Sklearn обёртками над LogReg

        Returns
        -------
        estimators : dict
            Key - решаемая задача
            Value - класс, отвечающий за обучение модели под конкретную задачу
        """
        estimators = {
            "classification": LogisticRegression,
        }
        return estimators

    def _create_eval_set(
        self, data: pd.DataFrame, target: pd.Series, *eval_set, asnumpy: bool = False
    ) -> List[Tuple[pd.DataFrame]]:
        """
        Создание eval_set в sklearn-формате.
        """
        data = self.validate_input_data(data)
        if eval_set:
            valid_data = self.validate_input_data(eval_set[0])
            return [(valid_data, eval_set[1])]

        return [(data, target)]

    def fit(self, data, target, *eval_set):
        """
        Обучение модели на данных data, target.

        Parameters
        ----------
        data: pandas.DataFrame, shape = [n_samples, n_features]
            Матрица признаков (обучающая выборка).

        target: pandas.Series, shape = [n_samples, ]
            Вектор целевой переменной.

        eval_set: Tuple[pd.DataFrame, pd.Series]
            Кортеж с валидационными данными. Первый элемент
            кортежа - матрица признаков, второй элемент
            кортежа - вектор целевой переменной.

        """
        self.estimator = self.estimator_class()
        data = self._fill_nan_values(data)
        self.estimator.fit(X=data, y=target)
        self.fitted = True

        return self

    def transform(self, data):
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
        prediction: array-like, shape = [n_samples, ]
            Вектор с прогнозами модели на данных data.
        """

        self.check_is_fitted
        data = self.validate_input_data(data)
        data = self._fill_nan_values(data)
        prediction = self.estimator.predict_proba(data)
        if self.task == "binary":
            return prediction[:, 1]
        elif self.task == "multiclass":
            return prediction

    @staticmethod
    def _get_best_iteration(estimator) -> int:
        return 1

    @property
    def best_iteration(self):
        return 1