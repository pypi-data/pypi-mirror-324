metric_name_mapping = {
    "rmse": {
        "catboost": "RMSE",
        "lightgbm": "rmse",
        "xgboost": "rmse",
        "pyboost": "rmse",
    },
    "rmsle": {"xgboost": "rmsle", "pyboost": "rmsle"},
    "msle": {
        "catboost": "MSLE",
    },
    "mse": {
        "lightgbm": "mse",
    },
    "r2": {"catboost": "R2", "pyboost": "r2"},
    "fbeta": {
        "catboost": "F",
    },
    "mape": {
        "catboost": "MAPE",
        "lightgbm": "mape",
        "xgboost": "mape",
    },
    "smape": {
        "catboost": "SMAPE",
    },
    "mdae": {
        "catboost": "MedianAbsoluteError",
    },
    "mae": {
        "lightgbm": "mae",
        "xgboost": "mae",
        "catboost": "MAE",
    },
    "huber_loss": {
        "lightgbm": "huber",
        "xgboost": "mphe",
        "catboost": "Huber:delta=1",
    },
    "fair_loss": {
        "lightgbm": "fair",
        "catboost": "FairLoss",
    },
    "poisson": {
        "lightgbm": "poisson",
        "catboost": "Poisson",
    },
    "gamma": {
        "lightgbm": "poisson",
    },
    "gamma_deviance": {
        "lightgbm": "gamma_deviance",
    },
    "tweedie": {
        "lightgbm": "tweedie",
        "catboost": "Tweedie",
    },
    "ndcg": {
        "lightgbm": "ndcg",
    },
    "mean_average_precision": {
        "lightgbm": "map",
        "xgboost": "map",
        "catboost": "MAP",
    },
    "average_precision": {
        "lightgbm": "average_precision",
    },
    "roc_auc": {
        "lightgbm": "auc",
        "xgboost": "auc",
        "catboost": "AUC",
        "pyboost": "auc",
    },
    "accuracy": {
        "catboost": "Accuracy",
        "pyboost": "accuracy",
    },
    "precision": {
        "catboost": "Precision",
        "pyboost": "precision",
    },
    "recall": {
        "catboost": "Recall",
        "pyboost": "recall",
    },
    "precision_recall_auc": {
        "xgboost": "aucpr",
        "catboost": "PRAUC",
    },
    "cross-entropy": {
        "lightgbm": "cross-entropy",
        "catboost": "CrossEntropy",
        "pyboost": "crossentropy",
    },
    "kullback_leibler": {
        "lightgbm": "kullback_leibler",
    },
    "quantile": {
        "lightgbm": "quantile",
        "catboost": "Quantile",
    },
    "f1_score": {
        "catboost": {
            "binary": "F1",
            "multiclass": "TotalF1",
            "multilabel": "F1",
        },
        "lightgbm": {
            "binary": "f1",
        },
        "pyboost": {
            "binary": "f1",
            "multiclass": "f1",
            "multilabel": "f1",
        },
    },
    "logloss": {
        "catboost": {
            "binary": "Logloss",
            "multiclass": "MultiClass",
            "multilabel": "MultiLogloss",
        },
        "xgboost": {
            "binary": "logloss",
            "multiclass": "mlogloss",
            "multilabel": "logloss",
        },
        "lightgbm": {
            "binary": "binary",
            "multiclass": "multiclass",
            "multilabel": "binary",
        },
        "pyboost": {
            "binary": "logloss",
            "multiclass": "crossentropy",
        },
    },
    "log_perplexity": {
        "lda": "log_perplexity",
        "ensembelda": "log_perplexity",
    },
    "coherence": {
        "lda": "coherence",
        "ensembelda": "coherence",
        "bertopic": "coherence",
    },
    "average_distance": {
        "lda": "average_distance",
        "ensembelda": "average_distance",
        "bertopic": "average_distance",
    },
    "silhouette_score": {"bertopic": "silhouette_score"},
}

objective_name_mapping = {
    "mse": {
        "catboost": "RMSE",
        "lightgbm": "mse",
        "xgboost": "reg:squarederror",
        "pyboost": "mse",
    },
    "rmse": {
        "catboost": "RMSE",
        "lightgbm": "rmse",
        "xgboost": "reg:squarederror",
    },
    "rmsle": {
        "xgboost": "reg:squaredlogerror",
    },
    "mape": {
        "catboost": "MAPE",
        "lightgbm": "mape",
    },
    "mae": {
        "lightgbm": "mae",
        "catboost": "MAE",
        "xgboost": "reg:absoluteerror",
    },
    "huber_loss": {
        "lightgbm": "huber",
        "xgboost": "reg:pseudohubererror",
        "catboost": "Huber:delta=1",
    },
    "fair_loss": {
        "lightgbm": "fair",
    },
    "poisson": {
        "lightgbm": "poisson",
        "catboost": "Poisson",
    },
    "quantile": {
        "lightgbm": "quantile",
        "catboost": "Quantile",
        "xgboost": "reg:quantileerror",
    },
    "gamma": {
        "lightgbm": "gamma",
    },
    "tweedie": {
        "lightgbm": "tweedie",
        "catboost": "Tweedie",
    },
    "binary_logloss": {
        "lightgbm": "binary",
        "catboost": "Logloss",
        "xgboost": "binary:logistic",
        "pyboost": "binary",
    },
    "cross-entropy": {
        "lightgbm": "cross-entropy",
        "catboost": "CrossEntropy",
        "pyboost": "crossentropy",
    },
    "multiclass_logloss": {
        "lightgbm": "multiclass",
        "catboost": "MultiClass",
        "xgboost": "multi:softprob",
        "pyboost": "multiclass",
    },
    "multiclassova": {
        "lightgbm": "multiclassova",
        "catboost": "MultiClassOneVsAll",
    },
    "multilabel_logloss": {
        "catboost": "MultiLogloss",
        "xgboost": "binary:logistic",
        "lightgbm": "binary",
    },
    "multi-cross-entropy": {
        "catboost": "MultiCrossEntropy",
    },
    "log_perplexity": {
        "lda": "log_perplexity",
        "ensembelda": "log_perplexity",
    },
    "coherence": {
        "lda": "coherence",
        "ensembelda": "coherence",
        "bertopic": "coherence",
    },
    "average_distance": {
        "lda": "average_distance",
        "ensembelda": "average_distance",
        "bertopic": "average_distance",
    },
    "silhouette_score": {"bertopic": "silhouette_score"},
}