import numpy as np
import pandas as pd
import os

from sklearn.metrics import (
    precision_score,
    recall_score,
    precision_recall_curve,
    auc,
    roc_auc_score,
    roc_curve,
)
from sklearn.metrics._regression import _check_reg_targets, mean_absolute_error
from sklearn.utils import check_consistent_length

try:
    import cupy as cp
except ImportError:
    cp = None

from py_boost.gpu.losses import BCELoss, BCEMetric, Loss, Metric
from py_boost.gpu.losses import auc as pyboost_auc


class PyBoostBCEWithNanLoss(BCELoss):
    """
    LogLoss Objective с Nan для PyBoost
    """

    alias = "BCE"
    clip_value = 1e-7

    def __init__(self, *args, **kwargs):
        if cp is None:
            raise ImportError("cupy is required to use py_boost")

        super().__init__(*args, **kwargs)

    def base_score(self, y_true):
        means = cp.clip(
            cp.nanmean(y_true, axis=0), self.clip_value, 1 - self.clip_value
        )
        return cp.log(means / (1 - means))

    def __get_grad_hess(self, y_true: np.ndarray, y_pred: np.ndarray):
        # first, get nan mask for y_true
        mask = cp.isnan(y_true)
        # then, compute loss with any values at nan places just to prevent the exception
        grad, hess = super().get_grad_hess(cp.where(mask, 0, y_true), y_pred)
        # invert mask
        mask = (~mask).astype(cp.float32)
        # multiply grad and hess on inverted mask
        # now grad and hess eq. 0 on NaN points
        # that actually means that prediction on that place sould not be updated
        grad = grad * mask
        hess = hess * mask

        return grad, hess

    def get_grad_hess(
        self, y_true: np.ndarray, y_pred: np.ndarray
    ):  # pyboost Metric class abstractmehod definition
        return self.__get_grad_hess(y_true, y_pred)


class PyBoostBCEWithNanMetric(BCEMetric):
    alias = "BCE"

    def __init__(self, *args, **kwargs):
        if cp is None:
            raise ImportError("cupy is required to use py_boost")

        super(BCEMetric, self).__init__(*args, **kwargs)

    def __call__(self, y_true, y_pred, sample_weight=None):

        bces = []
        mask = ~cp.isnan(y_true)

        for i in range(y_true.shape[1]):
            m = mask[:, i]
            w = None if sample_weight is None else sample_weight[:, 0][m]
            bces.append(cp.mean(self.error(y_true[:, i][m], y_pred[:, i][m])).get())

        return np.mean(bces)


class PyBoostNanAuc(Metric):
    alias = "nan_auc"

    def __init__(self, *args, **kwargs):
        if cp is None:
            raise ImportError("cupy is required to use py_boost")

        super().__init__(*args, **kwargs)

    def __call__(self, y_true, y_pred, sample_weight=None):

        aucs = []
        mask = ~cp.isnan(y_true)

        for i in range(y_true.shape[1]):
            m = mask[:, i]
            w = None if sample_weight is None else sample_weight[:, 0][m]
            aucs.append(pyboost_auc(y_true[:, i][m], y_pred[:, i][m], w))

        return np.mean(aucs)

    def compare(self, v0, v1):
        return v0 > v1


class PyBoostMAPELoss(Loss):

    alias = "mape"

    multiplier: int = 10

    def __init__(self, *args, **kwargs):
        if cp is None:
            raise ImportError("cupy is required to use py_boost")

        super(Loss).__init__(*args, **kwargs)

    def base_score(self, y_true):
        return y_true.mean(axis=0)

    def __get_grad_hess(self, y_true: np.ndarray, y_pred: np.ndarray):
        n = len(y_true)
        less = (y_pred < y_true).reshape(-1, 1)
        more = (y_pred > y_true).reshape(-1, 1)

        grad = cp.zeros(len(y_true), dtype=y_true.dtype).reshape(-1, 1)
        grad[less] = -1 * self.multiplier
        grad[more] = 1 * self.multiplier

        grad = cp.array(grad, dtype=cp.float32)
        hess = cp.ones(len(y_true), dtype=y_true.dtype).reshape(-1, 1)

        return grad, hess

    def postprocess_output(self, y_pred):
        return y_pred.reshape(-1, 1)

    def get_grad_hess(
        self, y_true: np.ndarray, y_pred: np.ndarray
    ):  # pyboost Metric class abstractmehod definition
        return self.__get_grad_hess(y_true, y_pred)


class PyBoostMAPEMetric(Metric):
    alias = "mape"

    def __init__(self, *args, **kwargs):
        if cp is None:
            raise ImportError("cupy is required to use py_boost")

        super(Metric, self).__init__(*args, **kwargs)

    def error(self, y_true, y_pred):
        epsilon = cp.finfo(cp.float64).eps
        mape = cp.abs(y_pred - y_true) / cp.maximum(cp.abs(y_true), epsilon)
        output = cp.average(mape, axis=0)
        return output

    def __call__(self, y_true, y_pred, sample_weight=None):
        err = self.error(y_true, y_pred)
        return cp.average(err)

    def compare(self, v0, v1):
        return v0 < v1


class PyBoostQuantileLoss(Loss):

    alias = "quantile"

    alpha: float = 0.5

    def __init__(self, alpha, *args, **kwargs):
        if cp is None:
            raise ImportError("cupy is required to use py_boost")

        super(Loss).__init__(*args, **kwargs)

        self.alpha = alpha

    def base_score(self, y_true):
        return y_true.mean(axis=0)

    def __get_grad_hess(self, y_true: np.ndarray, y_pred: np.ndarray):
        grad = cp.zeros_like(y_pred)
        hess = cp.zeros_like(y_pred)

        ix = y_true < y_pred
        ix_x = y_true[ix] - y_pred[ix]
        not_ix_x = y_true[~ix] - y_pred[~ix]

        grad[ix] = (1 - self.alpha) * ((ix_x >= 0) * ix_x + (ix_x < 0) * ix_x * -1)
        grad[~ix] = (self.alpha) * (
            (not_ix_x >= 0) * not_ix_x + (not_ix_x < 0) * not_ix_x * -1
        )

        hess[ix] = (1 - self.alpha) * ((ix_x >= 0) + (ix_x < 0) * -1)
        hess[~ix] = (self.alpha) * ((not_ix_x >= 0) + (not_ix_x < 0) * -1)

        grad = -1 * cp.array(grad, dtype=cp.float32).reshape(-1, 1)
        hess = cp.array(hess, dtype=cp.float32).reshape(-1, 1)
        return grad, hess

    def postprocess_output(self, y_pred):
        return y_pred.reshape(-1, 1)

    def get_grad_hess(
        self, y_true: np.ndarray, y_pred: np.ndarray
    ):  # pyboost Metric class abstractmehod definition
        return self.__get_grad_hess(y_true, y_pred)


class PyBoostQuantileMetric(Metric):

    alias = "quantile"

    alpha: float = 0.5

    def __init__(self, alpha, *args, **kwargs):
        if cp is None:
            raise ImportError("cupy is required to use py_boost")

        super(Metric, self).__init__(*args, **kwargs)

        self.alpha = alpha

    def error(self, y_true, y_pred):
        y_pred = y_pred.reshape(-1, 1)
        ix = y_true < y_pred
        loss = cp.zeros_like(y_pred)
        loss[ix] = (1 - self.alpha) * cp.abs(y_true[ix] - y_pred[ix])
        loss[~ix] = self.alpha * cp.abs(y_true[~ix] - y_pred[~ix])
        output = cp.average(loss, axis=0)
        return output

    def postprocess_output(self, y_pred):
        return y_pred.reshape(-1, 1)

    def __call__(self, y_true, y_pred, sample_weight=None):
        err = self.error(y_true, y_pred)
        return cp.average(err)

    def compare(self, v0, v1):
        return v0 < v1


class PyBoostMSELoss(Loss):
    alias = "mse"

    def __init__(self, *args, **kwargs):
        if cp is None:
            raise ImportError("cupy is required to use py_boost")

        super(Loss).__init__(*args, **kwargs)

    def base_score(self, y_true):
        return y_true.mean(axis=0)

    def __get_grad_hess(self, y_true: np.ndarray, y_pred: np.ndarray):
        grad = y_pred - y_true
        hess = cp.ones(len(y_true), dtype=y_true.dtype).reshape(-1, 1)

        return grad, hess

    def postprocess_output(self, y_pred):
        return y_pred.reshape(
            -1,
        )

    def get_grad_hess(
        self, y_true: np.ndarray, y_pred: np.ndarray
    ):  # pyboost Metric class abstractmehod definition
        return self.__get_grad_hess(y_true, y_pred)


class PyBoostMSEMetric(Metric):
    alias = "mse"

    def __init__(self, *args, **kwargs):
        if cp is None:
            raise ImportError("cupy is required to use py_boost")

        super(Metric, self).__init__(*args, **kwargs)

    def error(self, y_true, y_pred):
        mse = (y_true - y_pred) ** 2
        output = cp.average(mse, axis=0)
        return output

    def __call__(self, y_true, y_pred, sample_weight=None):
        err = self.error(y_true, y_pred)
        return cp.average(err)

    def compare(self, v0, v1):
        return v0 < v1


class PyBoostGini(Metric):
    alias = "gini"

    def __init__(self, *args, **kwargs):
        if cp is None:
            raise ImportError("cupy is required to use py_boost")

        super().__init__(*args, **kwargs)

    def __call__(self, y_true, y_pred, sample_weight=None):

        aucs = []
        mask = ~cp.isnan(y_true)

        for i in range(y_true.shape[1]):
            m = mask[:, i]
            w = None if sample_weight is None else sample_weight[:, 0][m]
            aucs.append(self.error(y_true[:, i][m], y_pred[:, i][m], w))

        return np.mean(aucs)

    def error(self, y_true, y_pred, sample_weight=None):
        auc = pyboost_auc(y_true, y_pred, sample_weight)
        return 2 * auc - 1

    def compare(self, v0, v1):
        return v0 > v1


def mean_log_error(
    y_true, y_pred, *, sample_weight=None, multioutput="uniform_average", squared=True
):
    y_type, y_true, y_pred, multioutput = _check_reg_targets(
        y_true, y_pred, multioutput
    )
    check_consistent_length(y_true, y_pred, sample_weight)

    if (y_true < 0).any() or (y_pred < 0).any():
        raise ValueError(
            "Mean Squared Logarithmic Error cannot be used when "
            "targets contain negative values."
        )

    return mean_absolute_error(
        np.log1p(y_true),
        np.log1p(y_pred),
        sample_weight=sample_weight,
        multioutput=multioutput,
    )


def symmetric_mean_absolute_percentage_error(
    y_true, y_pred, *, sample_weight=None, multioutput="uniform_average"
):
    y_type, y_true, y_pred, multioutput = _check_reg_targets(
        y_true, y_pred, multioutput
    )
    check_consistent_length(y_true, y_pred, sample_weight)
    epsilon = np.finfo(np.float64).eps
    mape = np.abs(y_pred - y_true) / np.maximum(np.abs(y_true + y_pred) / 2, epsilon)
    output_errors = np.average(mape, weights=sample_weight, axis=0)
    if isinstance(multioutput, str):
        if multioutput == "raw_values":
            return output_errors
        elif multioutput == "uniform_average":
            # pass None as weights to np.average: uniform mean
            multioutput = None

    return np.average(output_errors, weights=multioutput)


def cut_at_k(y_true, y_pred, at_k):
    """
    Выделение из поданых векторов top_k значений по отклику модели, присвоение top_k откликам 1
    Parameters
    ----------
    y_true: array-like, shape = [n_samples, ]
        Вектор значений целевой переменной.

    y_pred: array-like, shape = [n_samples, ]
        Вектор значений прогнозов.

    at_k: int/float
        top-k значений
    Returns
    -------
    y_true_new: array-like, shape = [at_k, ]
        Новый вектор меток

    y_pred _new: array-like, shape = [at_k, ]
        Новый вектор откликов модели (все 1)
    """
    if at_k < 1:
        at_k = round(at_k * y_pred.shape[0])
    zipped = np.dstack((y_true, y_pred))[0]
    zipped = zipped[np.argsort(zipped[:, 1])][-at_k:, :]
    zipped[:, 1] = 1
    y_true_new = zipped[:, 0]
    y_pred_new = zipped[:, 1]
    return y_true_new, y_pred_new


def recall_at_k_score_(y_true, y_pred, metric_params):
    """
    Вычисление метрики RECALL@K
    Parameters
    ----------
    y_true: array-like, shape = [n_samples, ]
    Вектор значений целевой переменной.

    y_pred: array-like, shape = [n_samples, ]
        Вектор значений прогнозов.

    at_k: float,
        Порог, используется из self.metric_params
    Returns
    -------
    score: float
        Значение метрики RECALL@K.
    """
    at_k = metric_params["at_k"]
    if at_k < 1:
        at_k = round(at_k * y_pred.shape[0])
    zipped = np.dstack((y_true, y_pred))[0]
    zipped = zipped[np.argsort(zipped[:, 1])]
    zipped[-at_k:, 1] = 1
    zipped[:-at_k, 1] = 0
    return recall_score(zipped[:, 0], zipped[:, 1])


def precision_at_k_score_(y_true, y_pred, metric_params):
    """
    Вычисление метрики PRECISION@K
    Parameters
    ----------
    y_true: array-like, shape = [n_samples, ]
    Вектор значений целевой переменной.

    y_pred: array-like, shape = [n_samples, ]
        Вектор значений прогнозов.

    at_k: float,
        Порог, используется из self.metric_params
    Returns
    -------
    score: float
        Значение метрики PRECISION@K.
    """
    y_true_new, y_pred_new = cut_at_k(y_true, y_pred, metric_params["at_k"])
    return precision_score(y_true_new, y_pred_new)


def gini_at_k_score_(y_true, y_pred, metric_params):
    """
    Вычисление метрики GINI@K
    Parameters
    ----------
    y_true: array-like, shape = [n_samples, ]
    Вектор значений целевой переменной.

    y_pred: array-like, shape = [n_samples, ]
        Вектор значений прогнозов.

    at_k: float,
        Порог, используется из self.metric_params
    Returns
    -------
    score: float
        Значение метрики GINI@K.
    """
    at_k = metric_params["at_k"]
    if at_k < 1:
        at_k = round(at_k * y_pred.shape[0])
    zipped = np.dstack((y_true, y_pred))[0]
    zipped = zipped[np.argsort(zipped[:, 1])]
    y_true_new = zipped[-at_k:, 0]
    y_pred_new = zipped[-at_k:, 1]
    if y_true_new.sum() == 0:
        result = 0
    else:
        try:
            result = 2 * roc_auc_score(y_true_new, y_pred_new) - 1
        except ValueError:
            result = 1
    return result


def roc_auc_at_k_score_(y_true, y_pred, metric_params):
    """
    Вычисление метрики ROC_AUC@K
    Parameters
    ----------
    y_true: array-like, shape = [n_samples, ]
    Вектор значений целевой переменной.

    y_pred: array-like, shape = [n_samples, ]
        Вектор значений прогнозов.

    at_k: float,
        Порог, используется из self.metric_params
    Returns
    -------
    score: float
        Значение метрики ROC_AUC@K.
    """
    at_k = metric_params["at_k"]
    if at_k < 1:
        at_k = round(at_k * y_pred.shape[0])
    zipped = np.dstack((y_true, y_pred))[0]
    zipped = zipped[np.argsort(zipped[:, 1])]
    y_true_new = zipped[-at_k:, 0]
    y_pred_new = zipped[-at_k:, 1]
    if y_true_new.sum() == 0:
        result = 0
    else:
        try:
            result = roc_auc_score(y_true_new, y_pred_new)
        except ValueError:
            result = 1
    return result


def precision_recall_auc_at_k_score_(y_true, y_pred, metric_params):
    """
    Вычисление метрики PRECISION_RECALL_AUC@K
    Parameters
    ----------
    y_true: array-like, shape = [n_samples, ]
    Вектор значений целевой переменной.

    y_pred: array-like, shape = [n_samples, ]
        Вектор значений прогнозов.

    at_k: float,
        Порог, используется из self.metric_params
    Returns
    -------
    score: float
        Значение метрики PRECISION_RECALL_AUC@K.
    """
    y_true_new, y_pred_new = cut_at_k(y_true, y_pred, metric_params["at_k"])
    precision, recall, _ = precision_recall_curve(y_true_new, y_pred_new)
    return auc(recall, precision)


def sensitivity_specificity_auc_at_k_score_(y_true, y_pred, metric_params):
    """
    Вычисление метрики SENSITIVITY_SPECIFICITY@K
    Parameters
    ----------
    y_true: array-like, shape = [n_samples, ]
    Вектор значений целевой переменной.

    y_pred: array-like, shape = [n_samples, ]
        Вектор значений прогнозов.

    at_k: float,
        Порог, используется из self.metric_params
    Returns
    -------
    score: float
        Значение метрики SENSITIVITY_SPECIFICITY@K.
    """
    y_true_new, y_pred_new = cut_at_k(y_true, y_pred, metric_params["at_k"])
    try:
        fpr, tpr, _ = roc_curve(y_true_new, y_pred_new)
        result = auc(1 - fpr, tpr)
    except ValueError:
        result = 1
    return result


def precision_at_k_group_avg_score_(y_true, y_pred, metric_params):
    """
    Вычисление метрики PRECISION@k в группировке по group_col, расчет среднего по группам
    Parameters
    ----------
    y_true: array-like, shape = [n_samples, ]
    Вектор значений целевой переменной.

    y_pred: array-like, shape = [n_samples, ]
        Вектор значений прогнозов.

    group_col: pd.Series,
        Колонка с группировкой

    index: pd.Series
        Индексы
    Returns
    -------
    score: float
        Значение метрики PRECISION@K  группировке по group_col.
    """
    group_col = metric_params["group_col_dev"]
    index = metric_params["index"]
    group_col = group_col.loc[index]
    zipped = np.dstack((y_true, y_pred, group_col))[0]
    zipped = zipped[np.argsort(zipped[:, 2])]
    groups = np.array(
        np.split(zipped[:, :2], np.unique(zipped[:, 2], return_index=True)[1][1:])
    )
    precs = []
    for group in groups:
        precs.append(precision_at_k_score_(group[:, 0], group[:, 1], metric_params))
    return np.mean(precs)


def gini_at_k_group_avg_score_(y_true, y_pred, metric_params):
    """
    Вычисление метрики GINI@k в группировке по group_col, расчет среднего по группам
    Parameters
    ----------
    y_true: array-like, shape = [n_samples, ]
    Вектор значений целевой переменной.

    y_pred: array-like, shape = [n_samples, ]
        Вектор значений прогнозов.

    group_col: pd.Series,
        Колонка с группировкой

    index: pd.Series
        Индексы
    Returns
    -------
    score: float
        Значение метрики GINI@K  группировке по group_col.
    """
    group_col = metric_params["group_col_dev"]
    index = metric_params["index"]
    group_col = group_col.loc[index]
    zipped = np.dstack((y_true, y_pred, group_col))[0]
    zipped = zipped[np.argsort(zipped[:, 2])]
    groups = np.array(
        np.split(zipped[:, :2], np.unique(zipped[:, 2], return_index=True)[1][1:])
    )
    precs = []
    for group in groups:
        precs.append(gini_at_k_score_(group[:, 0], group[:, 1], metric_params))
    return np.mean(precs)


def precision_at_k_group_max_score_(y_true, y_pred, metric_params):
    """
    Вычисление метрики PRESICION@k в группировке по group_col: отбор at_k значений из каждой группы,
    вычисление общей метрики по сформированному вектору
    Parameters
    ----------
    y_true: array-like, shape = [n_samples, ]
    Вектор значений целевой переменной.

    y_pred: array-like, shape = [n_samples, ]
        Вектор значений прогнозов.

    group_col: pd.Series,
        Колонка с группировкой

    index: pd.Series
        Индексы
    Returns
    -------
    score: float
        Значение метрики PRECISION@K  группировке по group_col.
    """
    at_k = metric_params["at_k"]
    group_col = metric_params["group_col_dev"]
    index = metric_params["index"]
    group_col = group_col.loc[index]
    zipped = np.dstack((y_true, y_pred, group_col))[0]
    zipped = zipped[np.argsort(zipped[:, 2])]
    groups = np.array(
        np.split(zipped[:, :2], np.unique(zipped[:, 2], return_index=True)[1][1:])
    )
    if at_k < 1:
        at_k = round(at_k * y_pred.shape[0])
    trues = []
    for group in groups:
        trues.append(group[np.argsort(group[:, -1])][-at_k:, :][:, 0])
    trues = np.array(
        [el for sublist in trues for el in sublist]
    )  # только реальные метки, так как мы автоматически присваиваем 1 отобранным
    return precision_score(trues, [1] * len(trues))


def gini_at_k_group_max_score_(y_true, y_pred, metric_params):
    """
    Вычисление метрики GINI@k в группировке по group_col: отбор at_k значений из каждой группы,
    вычисление общей метрики по сформированному вектору
    Parameters
    ----------
    y_true: array-like, shape = [n_samples, ]
    Вектор значений целевой переменной.

    y_pred: array-like, shape = [n_samples, ]
        Вектор значений прогнозов.

    group_col: pd.Series,
        Колонка с группировкой

    index: pd.Series
        Индексы
    Returns
    -------
    score: float
        Значение метрики GINI@K  группировке по group_col.
    """
    at_k = metric_params["at_k"]
    group_col = metric_params["group_col_dev"]
    index = metric_params["index"]
    group_col = group_col.loc[index]
    zipped = np.dstack((y_true, y_pred, group_col))[0]
    zipped = zipped[np.argsort(zipped[:, 2])]
    groups = np.array(
        np.split(zipped[:, :2], np.unique(zipped[:, 2], return_index=True)[1][1:])
    )
    if at_k < 1:
        at_k = round(at_k * y_pred.shape[0])
    trues = []
    scores = []
    for group in groups:
        trues.append(group[np.argsort(group[:, -1])][-at_k:, :][:, 0])
        scores.append(group[np.argsort(group[:, -1])][-at_k:, :][:, 1])
    trues = np.array([el for sublist in trues for el in sublist])
    scores = np.array([el for sublist in scores for el in sublist])
    if trues.sum() == 0:
        result = 0
    else:
        try:
            result = 2 * roc_auc_score(trues, scores) - 1
        except ValueError:
            result = 1
    return result


def custom_metric_score_(y_true, y_pred, metric_params):
    metric = metric_params["custom_metric"]
    return metric(y_true, y_pred)