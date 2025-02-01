from typing import Optional, List, Union, Tuple

import numpy as np
import pandas as pd

from sklearn.metrics import (
    roc_auc_score,
    fbeta_score,
    auc,
    roc_curve,
    precision_recall_curve,
    precision_score,
    recall_score,
    accuracy_score,
    log_loss,
    f1_score,
)
from sklearn.preprocessing import LabelBinarizer

from dreamml.modeling.metrics._base_metric import BaseMetric, OptimizableMetricMixin
from dreamml.modeling.metrics.metric_functions import (
    precision_at_k_score_,
    recall_at_k_score_,
    gini_at_k_score_,
    roc_auc_at_k_score_,
    precision_recall_auc_at_k_score_,
    sensitivity_specificity_auc_at_k_score_,
    PyBoostBCEWithNanLoss,
    PyBoostNanAuc,
    PyBoostBCEWithNanMetric,
    PyBoostGini,
)


def _prepare_dtypes(
    y_true: Union[pd.DataFrame, np.ndarray], y_pred: [pd.DataFrame, np.ndarray]
) -> Tuple[np.ndarray, np.ndarray]:
    y_true = y_true.values if isinstance(y_true, (pd.DataFrame, pd.Series)) else y_true
    y_pred = y_pred.values if isinstance(y_pred, (pd.DataFrame, pd.Series)) else y_pred
    return y_true, y_pred


def _set_average(task: str):
    default_average = {
        "binary": "binary",
        "multilabel": "binary",
        "multiclass": "macro",
    }
    return default_average[task]


def _reshape_estimator_preds(task, y_true: np.ndarray, y_pred: np.array):
    if task in ["multiclass", "multilabel"] and len(y_pred.shape) == 1:
        return y_pred.reshape(y_true.shape[0], -1)
    return y_pred


class ClassificationMetric(BaseMetric):
    _task_type: str = "classification"

    def __init__(
        self,
        model_name: Optional[str] = None,
        task: Optional[str] = None,
        target_with_nan_values: bool = False,
        labels: Optional[List[Union[int, str, float]]] = None,
        average: Optional[str] = "binary",
        **params,
    ):
        super().__init__(
            model_name=model_name,
            task=task,
            target_with_nan_values=target_with_nan_values,
            **params,
        )
        self.average = _set_average(self._task) if average == "binary" else average
        self.multi_class = "ovr"
        # т.к. для задачи multiclass применяем label_encoder к y_true, классы принимают значения от 0 до n_classes
        self.arange_labels = (
            np.arange(len(labels)) if self._task == "multiclass" else None
        )

    def __call__(self, y_true, y_pred):
        y_true, y_pred = _prepare_dtypes(y_true, y_pred)

        # FIXME: _detailed_model_statisitics.py multilabel_detailed_model_stats
        if self._task == "multilabel":
            if self.average is not None:
                self.average = "binary"
            return self._calculate_macro_score_with_nan_values(y_true, y_pred)
        else:
            return self._score_function(y_true, y_pred)

    def _calculate_macro_score_with_nan_values(
        self, y_true: np.ndarray, y_pred: np.ndarray
    ):
        """
        Расчет macro метрики с/без NaN значениями для задачи MultiLabel Classification.

        Parameters
        ----------
        y_true: np.ndarray - матрица таргетов (n_samples, n_classes)
        y_pred: np.ndarray - матрица предсказанных вероятностей (n_samples, n_classes)

        Returns
        -------
        if multilabel_average_none_flag = True:
            Список метрики по каждому классу
        else:
            Macro метрика по всем классам
        """
        y_true_flatten, y_pred_flatten = [], []
        metric_list = []
        num_classes = y_true.shape[1]
        mask = ~np.isnan(y_true)  # Маска для исключения NaN значений

        for class_idx in range(num_classes):
            mask_by_class_idx = mask[:, class_idx]
            y_true_idx_class = y_true[mask_by_class_idx, class_idx]
            y_pred_idx_class = y_pred[mask_by_class_idx, class_idx]

            # ["logloss", "accuracy"] для этих метрик нет понятия average, поэтому считаем micro
            if self.name in ["logloss", "accuracy"]:
                # y_true_flatten.append(y_true_idx_class)
                # y_pred_flatten.append(y_pred_idx_class)

                # для новой версии numpy:
                y_true_flatten = np.append(y_true_flatten, np.array(y_true_idx_class))
                y_pred_flatten = np.append(y_pred_flatten, np.array(y_pred_idx_class))
            else:
                # Рассчитываем метрику для текущего класса
                metric = self._score_function(y_true_idx_class, y_pred_idx_class)

                # ["roc_auc", "gini"] при average=None возвращают метрику сразу для 1 класса
                if self.average is None and self.name not in ["roc_auc", "gini"]:
                    metric_list.append(metric[1])
                else:
                    metric_list.append(metric)

        if self.name in ["logloss", "accuracy"]:
            return self._score_function(
                np.array(y_true_flatten).T, np.array(y_pred_flatten).T
            )

        # Если флаг average is None - считаем бинарную метрику для каждого класса с average None
        # Возвращаем метрику для 1 класса по каждому классу
        if self.average is None and self.name not in ["logloss", "accuracy"]:
            return metric_list

        # Возвращаем среднюю метрику (macro)
        return np.mean(metric_list) if metric_list else 0.0

    def _calculate_multiclass_macro_metric(
        self, y_true, y_pred_proba, metric="roc_auc"
    ):
        """
        Функция для расчета roc_auc_score в случае неравного количества
        классов в train и oot выборках. Решает ошибку:
        ValueError: Only one class present in y_true. ROC AUC score is not defined in that case.
        """

        result = []
        labels_in_y_true = np.unique(y_true)
        lb = LabelBinarizer(sparse_output=False).fit(self.arange_labels)
        y_true_binarizerd = lb.transform(y_true)

        for class_idx in self.arange_labels:
            if class_idx in labels_in_y_true:
                if metric == "roc_auc":
                    score = roc_auc_score(
                        y_true_binarizerd[:, class_idx],
                        y_pred_proba[:, class_idx],
                        average=self.average,
                    )
                    score = np.array(score)
                elif metric == "precision_recall_auc":
                    precision, recall, _ = precision_recall_curve(
                        y_true_binarizerd[:, class_idx],
                        y_pred_proba[:, class_idx],
                    )
                    score = auc(recall, precision)
                else:
                    score = np.nan
                result = np.append(result, score)
            else:
                result = np.append(result, np.nan)

        if self.average is None:
            return result
        return np.nanmean(result)


class LogLoss(ClassificationMetric, OptimizableMetricMixin):
    name = "logloss"
    maximize = False

    def _score_function(self, y_true, y_pred):
        y_pred = _reshape_estimator_preds(self._task, y_true, y_pred)

        if self._task == "multiclass":
            return log_loss(y_true, y_pred, labels=self.arange_labels)
        return log_loss(y_true, y_pred)

    def _get_pyboost_custom_objective(
        self,
    ):
        _objective = PyBoostBCEWithNanLoss()
        return _objective

    def _get_pyboost_custom_metric(
        self,
    ):
        _metric = PyBoostBCEWithNanMetric()
        return _metric


class Gini(ClassificationMetric):
    name = "gini"
    maximize = True

    def _score_function(self, y_true, y_pred):
        y_pred = _reshape_estimator_preds(self._task, y_true, y_pred)

        if self._task == "multiclass":
            if len(np.unique(y_true)) != len(np.unique(y_pred)):
                return (
                    2
                    * self._calculate_multiclass_macro_metric(
                        y_true, y_pred, metric="roc_auc"
                    )
                    - 1
                )
            return (
                2
                * roc_auc_score(
                    y_true,
                    y_pred,
                    average=self.average,
                    multi_class=self.multi_class,
                    labels=self.arange_labels,
                )
                - 1
            )
        return 2 * roc_auc_score(y_true, y_pred, average="macro") - 1

    def _get_pyboost_custom_metric(
        self,
    ):
        _metric = PyBoostGini()
        return _metric


class ROCAUC(ClassificationMetric):
    name = "roc_auc"
    maximize = True

    def _score_function(self, y_true, y_pred):
        y_pred = _reshape_estimator_preds(self._task, y_true, y_pred)

        if self._task == "multiclass":
            if len(np.unique(y_true)) != len(np.unique(y_pred)):
                return self._calculate_multiclass_macro_metric(
                    y_true, y_pred, metric="roc_auc"
                )
            return roc_auc_score(
                y_true,
                y_pred,
                average=self.average,
                multi_class=self.multi_class,
                labels=self.arange_labels,
            )
        return roc_auc_score(y_true, y_pred, average="macro")

    def _get_pyboost_custom_metric(
        self,
    ):  # Так можно определять кастомные objectives и metrics, отнаследовавшись от ClassificationMetric
        _metric = PyBoostNanAuc()
        return _metric


class SSAUC(ClassificationMetric):
    name = "sensitivity_specificity_auc"
    maximize = True

    def _score_function(self, y_true, y_pred):
        y_pred = _reshape_estimator_preds(self._task, y_true, y_pred)

        fpr, tpr, _ = roc_curve(y_true, y_pred)
        return auc(1 - fpr, tpr)


class PRAUC(ClassificationMetric):
    name = "precision_recall_auc"
    maximize = True

    def _score_function(self, y_true, y_pred):
        y_pred = _reshape_estimator_preds(self._task, y_true, y_pred)

        if self._task == "multiclass":
            return self._calculate_multiclass_macro_metric(
                y_true, y_pred, metric="precision_recall_auc"
            )
        precision, recall, _ = precision_recall_curve(y_true, y_pred)
        return auc(recall, precision)


class Precision(ClassificationMetric):
    name = "precision"
    maximize = True

    def _score_function(self, y_true, y_pred):
        y_pred = _reshape_estimator_preds(self._task, y_true, y_pred)

        if self._task == "multiclass":
            y_pred_round = (
                np.argmax(y_pred, axis=1) if len(y_pred.shape) != 1 else y_pred
            )
            return precision_score(
                y_true, y_pred_round, average=self.average, labels=self.arange_labels
            )
        else:
            threshold = self.params.get("threshold", 0.5)
            y_pred_round = np.where(y_pred > threshold, 1, 0)
            return precision_score(y_true, y_pred_round, average=self.average)


class Recall(ClassificationMetric):
    name = "recall"
    maximize = True

    def _score_function(self, y_true, y_pred):
        y_pred = _reshape_estimator_preds(self._task, y_true, y_pred)

        if self._task == "multiclass":
            y_pred_round = (
                np.argmax(y_pred, axis=1) if len(y_pred.shape) != 1 else y_pred
            )
            return recall_score(
                y_true, y_pred_round, average=self.average, labels=self.arange_labels
            )
        else:
            threshold = self.params.get("threshold", 0.5)
            y_pred_round = np.where(y_pred > threshold, 1, 0)
            return recall_score(y_true, y_pred_round, average=self.average)


class Accuracy(ClassificationMetric):
    name = "accuracy"
    maximize = True

    def _score_function(self, y_true, y_pred):
        y_pred = _reshape_estimator_preds(self._task, y_true, y_pred)

        if self._task == "multiclass":
            y_pred_round = (
                np.argmax(y_pred, axis=1) if len(y_pred.shape) != 1 else y_pred
            )
        else:
            threshold = self.params.get("threshold", 0.5)
            y_pred_round = np.where(y_pred > threshold, 1, 0)

        return accuracy_score(y_true, y_pred_round)


class FBeta(ClassificationMetric):
    name = "fbeta"
    maximize = True

    def _score_function(self, y_true, y_pred):
        y_pred = _reshape_estimator_preds(self._task, y_true, y_pred)
        beta = self.params.get("beta", 1)

        if self._task == "multiclass":
            y_pred_round = (
                np.argmax(y_pred, axis=1) if len(y_pred.shape) != 1 else y_pred
            )
            return fbeta_score(
                y_true,
                y_pred_round,
                average=self.average,
                beta=beta,
                labels=self.arange_labels,
            )
        else:
            threshold = self.params.get("threshold", 0.5)
            y_pred_round = np.where(y_pred > threshold, 1, 0)
            return fbeta_score(
                y_true=y_true, y_pred=y_pred_round, average=self.average, beta=beta
            )

    def _get_catboost_metric_name(self):
        name = super()._get_catboost_metric_name()
        params = f"beta={self.params['beta']}"

        return f"{name}:{params}"


class F1Score(ClassificationMetric):
    name = "f1_score"
    maximize = True

    def _score_function(self, y_true, y_pred):
        y_pred = _reshape_estimator_preds(self._task, y_true, y_pred)

        if self._task == "multiclass":
            y_pred_round = (
                np.argmax(y_pred, axis=1) if len(y_pred.shape) != 1 else y_pred
            )
            return f1_score(
                y_true, y_pred_round, average=self.average, labels=self.arange_labels
            )
        else:
            threshold = self.params.get("threshold", 0.5)
            y_pred_round = np.where(y_pred > threshold, 1, 0)
            return f1_score(y_true, y_pred_round, average=self.average)


class PrecisionAtK(ClassificationMetric):
    name = "precision_at_k"
    maximize = True

    def _score_function(self, y_true, y_pred):
        at_k = self.params.get("at_k", 5)

        return precision_at_k_score_(y_true, y_pred, {"at_k": at_k})


class RecallAtK(ClassificationMetric):
    name = "recall_at_k"
    maximize = True

    def _score_function(self, y_true, y_pred):
        at_k = self.params.get("at_k", 5)

        return recall_at_k_score_(y_true, y_pred, {"at_k": at_k})


class GiniAtK(ClassificationMetric):
    name = "gini_at_k"
    maximize = True

    def _score_function(self, y_true, y_pred):
        at_k = self.params.get("at_k", 5)

        return gini_at_k_score_(y_true, y_pred, {"at_k": at_k})


class ROCAUCAtK(ClassificationMetric):
    name = "roc_auc_at_k"
    maximize = True

    def _score_function(self, y_true, y_pred):
        at_k = self.params.get("at_k", 5)

        return roc_auc_at_k_score_(y_true, y_pred, {"at_k": at_k})


class PRAUCAtK(ClassificationMetric):
    name = "precision_recall_auc_at_k"
    maximize = True

    def _score_function(self, y_true, y_pred):
        at_k = self.params.get("at_k", 5)

        return precision_recall_auc_at_k_score_(y_true, y_pred, {"at_k": at_k})


class SSAUCAtK(ClassificationMetric):
    name = "sensitivity_specificity_auc_at_k"
    maximize = True

    def _score_function(self, y_true, y_pred):
        at_k = self.params.get("at_k", 5)

        return sensitivity_specificity_auc_at_k_score_(y_true, y_pred, {"at_k": at_k})