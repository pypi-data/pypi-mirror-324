import warnings
from abc import ABC, abstractmethod
from collections.abc import Sequence
from functools import partial
from typing import Dict, Any, List, Optional

import numpy as np

from dreamml.logging import get_logger
from dreamml.modeling.metrics._custom_factory import (
    _xgboost_custom_objective_factory,
    _xgboost_custom_metric_factory,
    _CatBoostCustomMetricFactory,
    _CatboostCustomObjective,
    _CatboostCustomMultiObjective,
    _pyboost_custom_objective_factory,
    _pyboost_custom_metric_factory,
    _lightgbm_custom_metric_factory,
    _lightgbm_custom_objective_factory,
)
from dreamml.modeling.metrics.names_mapping import (
    metric_name_mapping,
    objective_name_mapping,
)
from dreamml.utils.warnings import DMLWarning

_logger = get_logger(__name__)


class BaseMetric(ABC):
    name: str
    maximize: bool
    params: Dict[str, Any]
    _is_resetting_indexes_required: bool
    _is_optimizable: bool
    _data_indexes: Dict[str, Sequence]
    _required_columns: List[str]
    _task_type: str

    def __init__(
        self,
        model_name: Optional[str] = None,
        task: Optional[str] = None,
        target_with_nan_values: bool = False,
        **params,
    ):

        self.params: Dict[str, Any] = params
        self._model_name = model_name.lower() if model_name is not None else None
        self._task = task
        self._target_with_nan_values = target_with_nan_values

    def get_model_metric(self):
        if self._model_name is None:
            raise ValueError(
                f"Metic has to be initialized with `model_name` parameter."
            )

        if self._model_name in ["amts", "prophet", "linear_reg", "log_reg"]:
            return self

        implemented_name = metric_name_mapping.get(self.name, {}).get(
            self._model_name, None
        )
        if isinstance(implemented_name, Dict):
            implemented_name = implemented_name.get(self._task, None)

        if implemented_name is not None:
            return implemented_name

        if self._model_name == "catboost":
            implemented_func = self._get_catboost_custom_metric()
        elif self._model_name == "lightgbm":
            implemented_func = self._get_lightgbm_custom_metric()
        elif self._model_name == "xgboost":
            implemented_func = self._get_xgboost_custom_metric()
        elif self._model_name == "pyboost":
            implemented_func = self._get_pyboost_custom_metric()
        else:
            implemented_func = None

        if implemented_func is not None:
            _logger.warning(
                f"Внимание! Выбрана метрика {self.name}, которая не реализована в {self._model_name}. "
                f"Для кастомных метрик возможны просадки по скорости из-за отсутствия оптимизации."
            )
            return implemented_func
        else:
            raise NotImplementedError(
                f"Metric {self.name} is not implemented for {self._model_name} model."
            )

    def get_model_objective(self):
        if not self.is_optimizable:
            raise TypeError(
                f"Metic {self.__class__.__name__} is not optimizable and can't be used as an objective."
            )

        if self._model_name in ["amts", "prophet", "linear_reg", "log_reg"]:
            return self

        if self._model_name is None:
            raise TypeError(
                f"Metic can't be optimized without specifying `model_name`."
            )

        if self.name == "logloss" and self._task is None:
            raise TypeError(f"`task` needs to be specified for logloss.")

        if self._model_name == "catboost":
            implemented_name = self._get_catboost_objective_name()
        elif self._model_name == "lightgbm":
            implemented_name = self._get_lightgbm_objective_name()
        elif self._model_name == "xgboost":
            implemented_name = self._get_xgboost_objective_name()
        elif self._model_name == "pyboost":
            implemented_name = self._get_pyboost_objective_name()
        elif self._model_name in ("lda", "ensembelda", "bertopic"):
            implemented_name = self._get_topic_modeling_objective_name()
        else:
            implemented_name = None

        if implemented_name is not None:
            return implemented_name

        if self._model_name == "catboost":
            implemented_func = self._get_catboost_custom_objective()
        elif self._model_name == "lightgbm":
            implemented_func = self._get_lightgbm_custom_objective()
        elif self._model_name == "xgboost":
            implemented_func = self._get_xgboost_custom_objective()
        elif self._model_name == "pyboost":
            implemented_func = self._get_pyboost_custom_objective()
        else:
            implemented_func = None

        if implemented_func is not None:
            _logger.warning(
                f"Внимание! Выбрана лосс-функция {self.name}, которая не реализована в {self._model_name}. "
                f"Для кастомных лосс-функций возможны просадки по скорости из-за отсутствия оптимизации."
            )
            return implemented_func
        else:
            raise NotImplementedError(
                f"Objective {self.name} is not implemented for {self._model_name} model."
            )

    @property
    def is_resetting_indexes_required(self):
        return getattr(self, "_is_resetting_indexes_required", False)

    @property
    def is_optimizable(self):
        return getattr(self, "_is_optimizable", False)

    @property
    @abstractmethod
    def name(self):
        raise NotImplementedError

    @property
    def task_type(self):
        return self._task_type

    @property
    @abstractmethod
    def maximize(self):
        raise NotImplementedError

    def __call__(self, y_true, y_pred):
        return self._score_function(y_true, y_pred)

    @abstractmethod
    def _score_function(self, y_true, y_pred):
        raise NotImplementedError

    def _get_pyboost_custom_metric(self):
        raise NotImplementedError(
            f"Метрика {self.name} для PyBoost не реализована, выберите другую"
        )

    def _get_catboost_custom_metric(self):
        return _CatBoostCustomMetricFactory(_custom_metric_parent=self)

    def _get_xgboost_custom_metric(self):
        if self.maximize:
            warnings.warn(
                f"Внимание! Выбрана метрика {self.name}, которая не реализована в xgboost. "
                f"Для метрик с maximize=True xgboost на данный момент плохо работает из-за особенностей xgboost.\n"
                "Unlike the scoring parameter commonly used in scikit-learn, "
                "when a callable object is provided, it’s assumed to be a cost function "
                "and by default XGBoost will minimize the result during early stopping.",
                DMLWarning,
                stacklevel=2,
            )

        func = partial(_xgboost_custom_metric_factory, self)

        # AttributeError: 'functools.partial' object has no attribute '__name__'
        func.__name__ = self.name
        return func

    def _get_lightgbm_custom_metric(self):
        func = partial(_lightgbm_custom_metric_factory, self)
        return func


class CustomMetricMixin:
    _is_resetting_indexes_required: bool = True
    _data_indexes: Dict[str, Sequence]
    _required_columns: List[str]

    def set_indexes(self, **new_indexes):
        self._data_indexes = new_indexes

    @property
    def required_columns(self):
        if hasattr(self, "_required_columns"):
            return self._required_columns
        else:
            return None


class OptimizableMetricMixin:
    _is_optimizable: bool = True
    _task: str
    name: str

    def _get_gradient(self, y_true, y_pred):
        raise NotImplementedError(
            f"Gradient function for {self.name} metric is not implemented"
        )

    def _get_hessian(self, y_true, y_pred):
        raise NotImplementedError(
            f"Hessian function for {self.name} metric is not implemented"
        )

    def _get_catboost_objective_name(self):
        key = self.name if self.name != "logloss" else f"{self._task}_logloss"
        name = objective_name_mapping.get(key, {}).get("catboost")
        return name

    def _get_catboost_custom_objective(self):
        # https://github.com/catboost/catboost/blob/master/catboost/tutorials/custom_loss/custom_loss_and_metric_tutorial.ipynb
        if self._task in ["regression", "timeseries"]:
            return _CatboostCustomObjective(self)

        elif self._task in ["binary", "multiclass", "multilabel"]:
            return _CatboostCustomMultiObjective(self)

        else:
            raise NotImplementedError(
                f"CatBoost custom objectives are not done yet for {self._task}, remove catboost from fitted_model list"
            )

    def _get_xgboost_objective_name(self):
        # https://xgboost.readthedocs.io/en/stable/parameter.html#:~:text=options%20are%20below%3A-,objective,-%5Bdefault%3Dreg%3Asquarederror
        key = self.name if self.name != "logloss" else f"{self._task}_logloss"
        name = objective_name_mapping.get(key, {}).get("xgboost")
        return name

    def _get_xgboost_custom_objective(self):
        func = partial(_xgboost_custom_objective_factory, self)

        # AttributeError: 'functools.partial' object has no attribute '__name__'
        func.__name__ = self.name
        return func

    def _get_pyboost_objective_name(self):
        if self._task == "multilabel":
            return None
        key = self.name if self.name != "logloss" else f"{self._task}_logloss"
        name = objective_name_mapping.get(key, {}).get("pyboost")
        return name

    def _get_pyboost_custom_objective(self):
        raise NotImplementedError(
            f"Loss {self.name} для PyBoost не реализована, выберите другую"
        )

    def _get_lightgbm_objective_name(self):
        # https://lightgbm.readthedocs.io/en/latest/Parameters.html#objective-parameters:~:text=the%20correspondent%20functions-,objective,-%F0%9F%94%97%EF%B8%8E%2C%20default%20%3D
        key = self.name if self.name != "logloss" else f"{self._task}_logloss"
        name = objective_name_mapping.get(key, {}).get("lightgbm")
        return name

    def _get_lightgbm_custom_objective(self):
        func = partial(_lightgbm_custom_objective_factory, self)
        return func

    def _get_topic_modeling_objective_name(self):
        key = self.name
        name = objective_name_mapping.get(key, {}).get("lda")
        return name