from collections import namedtuple

from typing import Dict

from sklearn.metrics import (
    mean_squared_error,
    mean_squared_log_error,
)

from dreamml.modeling.metrics import BaseMetric
from dreamml.modeling.metrics.classification import (
    FBeta,
    Gini,
    ROCAUC,
    SSAUC,
    PRAUC,
    Precision,
    Recall,
    Accuracy,
    PrecisionAtK,
    RecallAtK,
    GiniAtK,
    ROCAUCAtK,
    PRAUCAtK,
    SSAUCAtK,
    LogLoss,
    F1Score,
)
from dreamml.modeling.metrics.regression import (
    RMSE,
    MSE,
    MAPE,
    MAE,
    MdAE,
    MdAPE,
    R2,
    RMSLE,
    HuberLoss,
    SMAPE,
    MSLE,
    MALE,
)
from dreamml.modeling.metrics.topic_modeling import (
    LogPerplexity,
    Coherence,
    AverageDistance,
    SilhouetteScore,
)
from dreamml.modeling.metrics.metric_functions import (
    precision_at_k_group_max_score_,
    gini_at_k_group_max_score_,
    precision_at_k_group_avg_score_,
    gini_at_k_group_avg_score_,
    custom_metric_score_,
)


def _rmse(*args, **kwargs):
    return mean_squared_error(*args, squared=False, **kwargs)


def _rmsle(*args, **kwargs):
    return mean_squared_log_error(*args, squared=False, **kwargs)


class MetricsMapping(dict):
    custom_metrics = []

    def register(self, object_name: str, base_metric: BaseMetric):
        self.update({object_name.lower(): base_metric})
        self.custom_metrics.append(object_name.lower())


EvalMetric = namedtuple("EvalMetric", ["function", "maximize"])

old_metrics_mapping = MetricsMapping(
    {
        "precision_at_k_group_max": EvalMetric(
            precision_at_k_group_max_score_, maximize=True
        ),
        "gini_at_k_group_max": EvalMetric(gini_at_k_group_max_score_, maximize=True),
        "precision_at_k_group_avg": EvalMetric(
            precision_at_k_group_avg_score_, maximize=True
        ),
        "gini_at_k_group_avg": EvalMetric(gini_at_k_group_avg_score_, maximize=True),
        "custom_metric": EvalMetric(custom_metric_score_, maximize=True),
    }
)

metrics_mapping = MetricsMapping(
    {
        "mse": MSE,
        "rmse": RMSE,
        "msle": MSLE,
        "rmsle": RMSLE,
        "mae": MAE,
        "male": MALE,
        "mape": MAPE,
        "smape": SMAPE,
        "huber_loss": HuberLoss,
        "mdae": MdAE,
        "mdape": MdAPE,
        "r2": R2,
        "gini": Gini,
        "roc_auc": ROCAUC,
        "sensitivity_specificity_auc": SSAUC,
        "precision_recall_auc": PRAUC,
        "precision": Precision,
        "recall": Recall,
        "accuracy": Accuracy,
        "f1_score": F1Score,
        "fbeta": FBeta,
        "precision_at_k": PrecisionAtK,
        "recall_at_k": RecallAtK,
        "gini_at_k": GiniAtK,
        "roc_auc_at_k": ROCAUCAtK,
        "precision_recall_auc_at_k": PRAUCAtK,
        "sensitivity_specificity_auc_at_k": SSAUCAtK,
        "logloss": LogLoss,
        "log_perplexity": LogPerplexity,
        "coherence": Coherence,
        "average_distance": AverageDistance,
        "silhouette_score": SilhouetteScore,
    }
)