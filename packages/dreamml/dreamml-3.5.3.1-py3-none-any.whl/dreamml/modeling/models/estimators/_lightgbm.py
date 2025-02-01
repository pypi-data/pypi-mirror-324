from typing import Tuple, Dict, Any, List, Optional
import logging

import pandas as pd
from lightgbm import LGBMRegressor, LGBMClassifier

from dreamml.modeling.models.callbacks.callbacks import LightGBMLoggingCallback
from dreamml.modeling.models.estimators import BoostingBaseModel
from dreamml.modeling.models.estimators._multioutput_wrappers import (
    OneVsRestClassifierWrapper,
)
from dreamml.features.feature_extraction._transformers import LogTargetTransformer


class LightGBMModel(BoostingBaseModel):
    model_name = "LightGBM"

    """
    Модель LightGBM со стандартизованным API для DreamML

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
    early_stopping_rounds : int
        Количество итераций обучения, в течении которых может наблюдаться деградация модели
        Если количество итераций больше заданного числа, то обучение останавливаться.
    fitted : bool
        Бала ли обучена модель, то есть вызван метод fit.
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
        self.estimator_class = self._estimators.get(self.task)
        self.early_stopping_rounds = self.params.pop("early_stopping_rounds", 100)
        self.verbose = self.params.pop("verbose", False)
        self.callback = LightGBMLoggingCallback(train_logger)

    @property
    def _estimators(self):
        """
        Словарь с Sklearn обёртками над LightGBM

        Returns
        -------
        estimators : dict
            Key - решаемая задача
            Value - класс, отвечающий за обучение модели под конкретную задачу

        """
        estimators = {
            "binary": LGBMClassifier,
            "multiclass": LGBMClassifier,
            "multilabel": LGBMClassifier,
            "regression": LGBMRegressor,
            "timeseries": LGBMRegressor,
        }
        return estimators

    def _create_fit_params(
        self, data: pd.DataFrame, target: pd.Series, weights: pd.Series, *eval_set
    ):
        """
        Создание параметров обучения в lgb-формате.
        """
        return {
            "early_stopping_rounds": self.early_stopping_rounds,
            "eval_set": self._create_eval_set(data, target, *eval_set),
            "sample_weight": weights,
            "verbose": self.verbose,
            "callbacks": [self.callback],
        }

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
        categorical_features = (
            self.categorical_features
            if self.categorical_features is not None
            else "auto"
        )

        data, eval_set = self._pre_fit(data, *eval_set)

        if self.weights is not None:
            weights = self.weights.copy()
            weights = weights.loc[data.index]
        else:
            weights = None

        params = {
            key: value
            for key, value in self.params.items()
            if key not in ["objective", "eval_metric", "n_estimators"]
        }
        n_estimators = self.params.get("n_estimators")

        eval_metric = self.eval_metric.get_model_metric()
        objective = self.objective.get_model_objective()
        self.estimator = self.estimator_class(
            objective=objective, n_estimators=n_estimators, **params
        )

        if self.task == "multilabel":
            self.estimator = OneVsRestClassifierWrapper(
                estimator=self.estimator,
                n_jobs=self.parallelism,
                get_best_iteration_func=self._get_best_iteration,
                n_estimators=n_estimators,
            )

        if self.task == "regression" and isinstance(
            self.log_target_transformer, LogTargetTransformer
        ):
            target = self.log_target_transformer.fit_transform(target)

        fit_params = self._create_fit_params(data, target, weights, *eval_set)
        fit_params = {
            key: value
            for key, value in fit_params.items()
            if key not in ["objective", "eval_metric"]
        }
        self._logger.debug(f"categorical_features={categorical_features,}")
        self.estimator.fit(
            X=data,
            y=target,
            categorical_feature=categorical_features,
            eval_metric=eval_metric,
            **fit_params,
        )
        self.fitted = True

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
        data = self.validate_input_data(data)
        if self.task == "binary":
            prediction = self.estimator.predict_proba(data)
            return prediction[:, 1]
        elif self.task in ("multiclass", "multilabel"):
            prediction = self.estimator.predict_proba(data)
            return prediction
        elif self.task in ("regression", "timeseries"):
            prediction = self.estimator.predict(data)
            if self.task == "regression" and isinstance(
                self.log_target_transformer, LogTargetTransformer
            ):
                prediction = self.log_target_transformer.inverse_transform(prediction)
            return prediction

    @staticmethod
    def _get_best_iteration(estimator) -> int:
        return estimator.best_iteration_