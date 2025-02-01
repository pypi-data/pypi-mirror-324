import logging
from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np

from dreamml.features.feature_extraction._transformers import LogTargetTransformer
from dreamml.modeling.models.estimators import BoostingBaseModel
from dreamml.modeling.models.callbacks.callbacks import PyBoostLoggingCallback

try:
    import cupy as cp
    from py_boost import GradientBoosting, SketchBoost
except ImportError:
    cp = None
    GradientBoosting = None
    SketchBoost = None


class PyBoostModel(BoostingBaseModel):
    model_name = "PyBoost"

    """
    Модель PyBoost со стандартизованным API для DreamML

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
        train_logger: Optional[logging.Logger] = None,
        log_target_transformer: LogTargetTransformer = None,
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
            log_target_transformer=log_target_transformer,
            train_logger=train_logger,
        )

        self.estimator_class = self._estimators.get(self.task, GradientBoosting)
        self.verbose = self.params.pop("verbose", 100)
        self.callback = PyBoostLoggingCallback(train_logger)

    @property
    def _estimators(self):
        """
        Словарь с Sklearn обёртками над PyBoost

        Returns
        -------
        estimators : dict
            Key - решаемая задача
            Value - класс, отвечающий за обучение модели под конкретную задачу
        """

        estimators = {
            "binary": GradientBoosting,
            "multiclass": GradientBoosting,
            "multilabel": SketchBoost,
            "regression": GradientBoosting,
            # "timeseries": CatBoostRegressor,
        }
        return estimators

    def _create_eval_set(
        self, data: pd.DataFrame, target: pd.Series, *eval_set, asnumpy: bool = False
    ):
        """
        Создание eval_set в sklearn-формате.
        """
        data = self.validate_input_data(data)

        if asnumpy:  # convert pd.DataFrame to numpy array for pyboost input if needed
            data, target = np.array(data.values, dtype=np.float32), np.array(
                target.values, dtype=np.float32
            )

        if eval_set:
            valid_data = self.validate_input_data(eval_set[0])
            if self.task == "regression" and isinstance(
                self.log_target_transformer, LogTargetTransformer
            ):
                eval_set = (
                    valid_data,
                    self.log_target_transformer.transform(eval_set[1]),
                )
            else:
                eval_set = (valid_data, eval_set[1])

            if asnumpy:
                return [
                    (data, target),
                    (
                        (np.array(valid_data.values, dtype=np.float32)),
                        np.array(eval_set[1].values, dtype=np.float32),
                    ),
                ]
            return [(data, target), (valid_data, eval_set[1])]

        return [(data, target)]

    def _create_fit_params(
        self,
        data: pd.DataFrame,
        target: pd.Series,
        weights: pd.Series,
        *eval_set,
        asnumpy: bool = False,
    ):
        """
        Создание параметров обучения в pyboost-формате.
        [{'X': X_test, 'y': y_test, 'sample_weight', w}, ...]"

        """

        _eval_sets = []
        for i, _set in enumerate(
            self._create_eval_set(data, target, *eval_set, asnumpy=True)
        ):
            _eval_set = {"X": _set[0], "y": _set[1], "sample_weight": None}
            _eval_sets.append(_eval_set)

        return {
            "eval_sets": _eval_sets,
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

        data, eval_set = self._pre_fit(data, *eval_set)

        if self.weights is not None:
            weights = self.weights.copy()
            weights = weights.loc[data.index]
        else:
            weights = None

        params = {
            key: value
            for key, value in self.params.items()
            if key not in ["objective", "eval_metric", "loss_function"]
        }
        params["callbacks"] = [self.callback]
        params["verbose"] = -1 if not self.verbose else 10

        objective = self.objective.get_model_objective()
        eval_metric = self.eval_metric.get_model_metric()

        self.estimator = self.estimator_class(
            loss=objective, metric=eval_metric, **params
        )

        if self.task == "regression" and isinstance(
            self.log_target_transformer, LogTargetTransformer
        ):
            target = self.log_target_transformer.fit_transform(target)

        fit_params = self._create_fit_params(
            data, target, weights, *eval_set, asnumpy=True
        )

        self.estimator.fit(
            X=np.array(data, dtype=np.float32),
            y=np.array(target, dtype=np.float32),
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

        self.check_is_fitted
        data = self.validate_input_data(data)
        prediction = self.estimator.predict(
            data
        )  # pyboost returns only proba values, does not have predict method
        if self.task in ["multilabel", "multiclass"]:
            return prediction
        elif self.task in ["regression", "binary", "timeseries"]:
            if self.task == "regression" and isinstance(
                self.log_target_transformer, LogTargetTransformer
            ):
                prediction = self.log_target_transformer.inverse_transform(prediction)
            return prediction.reshape(
                -1,
            )
        else:
            raise ValueError(f"Задача {self.task} не поддерживается.")

    def __call__(self, data):
        return self.transform(data)

    @staticmethod
    def _get_best_iteration(estimator) -> int:
        return estimator.best_round