import numpy as np
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_percentage_error,
    mean_absolute_error,
    median_absolute_error,
    r2_score,
    mean_squared_log_error,
)

from dreamml.modeling.metrics._base_metric import BaseMetric, OptimizableMetricMixin
from dreamml.modeling.metrics.metric_functions import (
    symmetric_mean_absolute_percentage_error,
    mean_log_error,
    PyBoostQuantileLoss,
    PyBoostQuantileMetric,
    PyBoostMAPELoss,
    PyBoostMAPEMetric,
    PyBoostMSELoss,
    PyBoostMSEMetric,
)


class RegressionMetric(BaseMetric):
    _task_type: str = "regression"


class RMSE(RegressionMetric, OptimizableMetricMixin):
    name = "rmse"
    maximize = False

    def _score_function(self, y_true, y_pred):
        return mean_squared_error(y_true, y_pred, squared=False)


class MSE(RegressionMetric, OptimizableMetricMixin):
    name = "mse"
    maximize = False

    def _score_function(self, y_true, y_pred):
        return mean_squared_error(y_true, y_pred, squared=True)

    def _get_pyboost_custom_objective(
        self,
    ):
        _objective = PyBoostMSELoss()
        return _objective

    def _get_pyboost_custom_metric(
        self,
    ):
        _metric = PyBoostMSEMetric()
        return _metric


class RMSLE(RegressionMetric, OptimizableMetricMixin):
    maximize = False
    name = "rmsle"

    def _score_function(self, y_true, y_pred):
        return mean_squared_log_error(y_true, y_pred, squared=False)


class MSLE(RegressionMetric):
    maximize = False
    name = "rmsle"

    def _score_function(self, y_true, y_pred):
        return mean_squared_log_error(y_true, y_pred, squared=True)


class MAE(RegressionMetric, OptimizableMetricMixin):
    name = "mae"
    maximize = False

    def _score_function(self, y_true, y_pred):
        return mean_absolute_error(y_true, y_pred)

    def _get_pyboost_custom_objective(
        self,
    ):
        _objective = PyBoostQuantileLoss(alpha=0.5)  # Quantile(alpha=0.5) == MAE
        return _objective

    def _get_pyboost_custom_metric(
        self,
    ):
        _metric = PyBoostQuantileMetric(alpha=0.5)  # Quantile(alpha=0.5) == MAE
        return _metric


class MALE(RegressionMetric):
    name = "male"
    maximize = False

    def _score_function(self, y_true, y_pred):
        return mean_log_error(y_true, y_pred)


class MAPE(RegressionMetric, OptimizableMetricMixin):
    name = "mape"
    maximize = False

    multiplier = 10

    def _score_function(self, y_true, y_pred):
        return mean_absolute_percentage_error(y_true, y_pred)

    def _get_gradient(self, y_true: np.ndarray, y_pred: np.ndarray):
        n = len(y_true)
        less = y_pred < y_true
        more = y_pred > y_true

        grad = np.zeros(len(y_true), dtype=y_true.dtype)
        grad[less] = -1.0 * self.multiplier
        grad[more] = 1.0 * self.multiplier

        grad = np.array(grad, dtype=np.float32)
        return grad

    def _get_hessian(self, y_true: np.ndarray, y_pred: np.ndarray):
        return np.ones(len(y_true), dtype=y_true.dtype)

    def _get_pyboost_custom_objective(
        self,
    ):
        _objective = PyBoostMAPELoss()
        return _objective

    def _get_pyboost_custom_metric(
        self,
    ):
        _metric = PyBoostMAPEMetric()
        return _metric


class SMAPE(RegressionMetric):
    name = "smape"
    maximize = False

    def _score_function(self, y_true, y_pred):
        return symmetric_mean_absolute_percentage_error(y_true, y_pred)


class HuberLoss(RegressionMetric, OptimizableMetricMixin):
    name = "huber_loss"
    maximize = False

    def _score_function(self, y_true, y_pred):
        return mean_absolute_percentage_error(y_true, y_pred)


class MdAE(RegressionMetric):
    name = "mdae"
    maximize = False

    def _score_function(self, y_true, y_pred):
        return median_absolute_error(y_true, y_pred)


class MdAPE(RegressionMetric):
    name = "mdape"
    maximize = False

    def _score_function(self, y_true, y_pred):
        return median_absolute_error(np.ones_like(y_true), y_pred / y_true)


class R2(RegressionMetric):
    name = "r2"
    maximize = True

    def _score_function(self, y_true, y_pred):
        return r2_score(y_true, y_pred)


class Quantile(RegressionMetric, OptimizableMetricMixin):
    name: str = "quantile"  # должно совпадать с "loss_function" в конфиге
    maximize: bool = False

    # name и maximize - обязательны
    # --------------

    alpha = 0.5  # пример определения параметра в функции потерь, если требуется для кастомных метрик и лоссов

    def _score_function(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        ix = y_true < y_pred
        loss = np.zeros_like(y_pred)
        loss[ix] = (1 - self.alpha) * np.abs(y_true[ix] - y_pred[ix])
        loss[~ix] = self.alpha * np.abs(y_true[~ix] - y_pred[~ix])
        return np.average(loss)

    def _get_gradient(
        self, y_true: np.ndarray, y_pred: np.ndarray
    ) -> np.ndarray:  # Нужно переопределить _get_gradient метод
        ix = y_true < y_pred
        grad = np.zeros_like(y_pred)
        ix_x = y_true[ix] - y_pred[ix]
        not_ix_x = y_true[~ix] - y_pred[~ix]
        grad[ix] = (1 - self.alpha) * ((ix_x >= 0) * ix_x + (ix_x < 0) * ix_x * -1)
        grad[~ix] = (self.alpha) * (
            (not_ix_x >= 0) * not_ix_x + (not_ix_x < 0) * not_ix_x * -1
        )
        return -grad

    def _get_hessian(
        self, y_true: np.ndarray, y_pred: np.ndarray
    ) -> np.ndarray:  # Нужно переопределить _get_hessian метод
        ix = y_true < y_pred
        hess = np.zeros_like(y_pred)
        ix_x = y_true[ix] - y_pred[ix]
        not_ix_x = y_true[~ix] - y_pred[~ix]
        hess[ix] = (1 - self.alpha) * ((ix_x >= 0) + (ix_x < 0) * -1)
        hess[~ix] = (self.alpha) * ((not_ix_x >= 0) + (not_ix_x < 0) * -1)
        return hess

    def _get_pyboost_custom_objective(
        self,
    ):
        _objective = PyBoostQuantileLoss(alpha=0.5)
        return _objective

    def _get_pyboost_custom_metric(
        self,
    ):
        _metric = PyBoostQuantileMetric(alpha=0.5)
        return _metric