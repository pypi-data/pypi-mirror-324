class BaseModelParams:
    def __init__(self, config_storage):
        self.config_storage = config_storage
        self.task = self.config_storage.task

    def get_common_params(self):
        return {}

    def get_hyper_params(self):
        common_params = self.get_common_params()
        specific_params = self.get_specific_params()
        common_params.update(specific_params)
        return common_params

    def get_specific_params(self):
        raise NotImplementedError("This method should be overridden by subclasses")

    def get_bounds(self):
        raise NotImplementedError("This method should be overridden by subclasses")

    def get_fixed_params(self):
        hyper_params = self.get_hyper_params()
        fixed_params = {}
        for k, v in hyper_params.items():
            fixed_params[k] = v
        fixed_params.pop("n_estimators", None)
        return fixed_params

    def merge_with_user_params(self, default_params, user_params):
        merged_params = default_params.copy()
        merged_params.update(user_params)
        return merged_params


class XGBoostParams(BaseModelParams):
    def get_specific_params(self):
        return {
            "objective": self.config_storage.loss_function,
            "eval_metric": self.config_storage.eval_metric,
            "seed": self.config_storage.random_seed,
            "verbose": self.config_storage.verbose,
            "n_estimators": self.config_storage.n_estimators,
            "enable_categorical": (
                False if self.config_storage.categorical_features is not None else True
            ),
            "booster": "gbtree",
            "early_stopping_rounds": max(self.config_storage.n_estimators // 10, 1),
            "device": "gpu" if self.config_storage.device == "cuda" else "cpu",
            "tree_method": "hist",
        }

    def get_bounds(self):
        xgboost_bounds_params = {
            "max_depth": (2, 11),
            "min_child_weight": (1, 100),
            "scale_pos_weight": (1, 100),
            "subsample": (0.5, 0.9),
            "colsample_bytree": (0.5, 0.9),
            "gamma": (1e-8, 5),
            "reg_alpha": (1e-8, 10),
            "reg_lambda": (1e-8, 10),
            "learning_rate": (1e-6, 0.3),
        }
        return xgboost_bounds_params


class LightGBMParams(BaseModelParams):
    def get_specific_params(self):
        specific_params = {
            "objective": self.config_storage.loss_function,
            "eval_metric": self.config_storage.eval_metric,
            "seed": self.config_storage.random_seed,
            "verbose": self.config_storage.verbose,
            "n_estimators": self.config_storage.n_estimators,
            "n_jobs": 6,
            # "device": "gpu" if self.config_storage.device == "cuda" else "cpu",
            "device": "cpu",
        }
        if self.task in ("regression", "timeseries"):
            specific_params["boosting_type"] = "goss"

        return specific_params

    def get_bounds(self):
        lightgbm_bounds_params = {
            "max_depth": (2, 11),
            "num_leaves": (16, 128),
            "min_child_samples": (
                5,
                5000,
            ),  # Изменяется в зависимости от размера датасета в optimization_stage.py
            "reg_lambda": (0.1, 20),
            "reg_alpha": (0.1, 20),
            "learning_rate": (1e-6, 0.3),
        }
        return lightgbm_bounds_params


class CatBoostParams(BaseModelParams):
    def get_specific_params(self):
        params = {
            "objective": self.config_storage.loss_function,
            "eval_metric": self.config_storage.eval_metric,
            "verbose": self.config_storage.verbose,
            "n_estimators": self.config_storage.n_estimators,
            "random_seed": self.config_storage.random_seed,
            "early_stopping_rounds": max(self.config_storage.n_estimators // 10, 1),
            "task_type": "GPU" if self.config_storage.device == "cuda" else "CPU",
        }
        params["task_type"] = (
            "CPU" if self.config_storage.task == "multilabel" else params["task_type"]
        )
        return params

    def get_bounds(self):
        catboost_bounds_params = {
            "max_depth": (2, 11),
            "l2_leaf_reg": (1, 100),
            "learning_rate": (1e-6, 0.3),
        }
        if self.config_storage.device not in ["gpu", "cuda"]:
            catboost_bounds_params["colsample_bylevel"] = (
                0.6,
                0.9,
            )  # colsample не работает на gpu для catboost
        return catboost_bounds_params


class PyBoostParams(BaseModelParams):
    def get_specific_params(self):
        return {
            "objective": self.config_storage.loss_function,
            "eval_metric": self.config_storage.eval_metric,
            "seed": self.config_storage.random_seed,
            "verbose": self.config_storage.verbose,
            "ntrees": self.config_storage.n_estimators,
            "es": max(self.config_storage.n_estimators // 10, 1),
        }

    def get_bounds(self):
        pyboost_bounds_params = {
            "max_depth": (2, 11),
            "lr": (1e-6, 0.3),
            "lambda_l2": (1e-5, 100),
            "min_data_in_leaf": (5, 5000),
            "colsample": (0.5, 1.0),
            "subsample": (0.5, 1.0),
            "max_bin": (2, 255),
            "min_data_in_bin": (1, 10),
        }
        if self.task in ("regression", "timeseries"):
            pyboost_bounds_params["lr"] = ((1e-6, 0.3),)
        return pyboost_bounds_params


class WhiteBoxAutoMLParams(BaseModelParams):
    def get_specific_params(self):
        return {}

    def get_bounds(self):
        return {}


class BoostarootaParams(BaseModelParams):
    def get_specific_params(self):
        specific_params = {
            "metric": "auc",
            "clf": None,  # SKlearn learner, default: XGBoost
            "cutoff": 4,  # Adjustment to removal cutoff from the feature importance
            "iters": 30,  # The number of learner (XGBoost) iterations per BR iteration
            "max_rounds": 100,  # The number of BostARoota iterations (maximum)
            # Minimum share of features for removing to start next iter
            # (0.1 = if >=10% features were dropped start next round)
            "delta": 0.1,
            "silent": False,
            "shap_flag": False,
        }
        if self.task in ("regression", "timeseries"):
            specific_params = {}
        return specific_params

    def get_bounds(self):
        return {}


class ProphetParams(BaseModelParams):
    def get_specific_params(self):
        specific_params = {}
        if self.task == "amts":
            specific_params = {
                "objective": self.config_storage.loss_function,
                "eval_metric": self.config_storage.eval_metric,
                "n_iterations": self.config_storage.n_iterations,
                "time_column_frequency": self.config_storage.time_column_frequency,
                "split_by_group": self.config_storage.split_by_group,
                "group_column": self.config_storage.group_column,
                "horizon": self.config_storage.horizon,
            }
        return specific_params

    def get_bounds(self):
        return {}


class LinearRegParams(BaseModelParams):
    def get_specific_params(self):
        return {
            "objective": self.config_storage.loss_function,
            "eval_metric": self.config_storage.eval_metric,
        }

    def get_bounds(self):
        return {
            "objective": self.config_storage.loss_function,
            "eval_metric": self.config_storage.eval_metric,
        }


class LogRegParams(BaseModelParams):
    def get_specific_params(self):
        return {
            "objective": self.config_storage.loss_function,
            "eval_metric": self.config_storage.eval_metric,
            "random_state": self.config_storage.random_seed,
        }

    def get_bounds(self):
        return {}


class LDAParams(BaseModelParams):
    def get_specific_params(self):
        return {
            "objective": self.config_storage.loss_function,
            "eval_metric": self.config_storage.eval_metric,
            "num_topics": self.config_storage.num_topics,
            "passes": self.config_storage.lda_passes,
            "alpha": self.config_storage.alpha,
            "eta": self.config_storage.eta,
            "random_state": self.config_storage.random_seed,
        }

    def get_bounds(self):
        return {"num_topics": (2, 15), "alpha": (1e-2, 1), "eta": (1e-2, 1)}


class EnsembeldaParams(BaseModelParams):
    def get_specific_params(self):
        return {
            "objective": self.config_storage.loss_function,
            "eval_metric": self.config_storage.eval_metric,
            "num_topics": self.config_storage.num_topics,
            "passes": self.config_storage.lda_passes,
            "num_models": self.config_storage.num_models,
            "iterations": self.config_storage.iterations,
            "random_state": self.config_storage.random_seed,
        }

    def get_bounds(self):
        return {"num_topics": (2, 20), "num_models": (2, 20), "iterations": (1, 50)}


class BERTopicParams(BaseModelParams):
    def get_specific_params(self):
        return {
            "objective": self.config_storage.loss_function,
            "eval_metric": self.config_storage.eval_metric,
            "random_state": self.config_storage.random_seed,
            "n_neighbors": self.config_storage.n_neighbors,
            "n_components": self.config_storage.n_components,
            "min_dist": self.config_storage.min_dist,
            "metric_umap": self.config_storage.metric_umap,
            "umap_epochs": self.config_storage.umap_epochs,
            "min_cluster_size": self.config_storage.min_cluster_size,
            "max_cluster_size": self.config_storage.max_cluster_size,
            "min_samples": self.config_storage.min_samples,
            "metric_hdbscan": self.config_storage.metric_hdbscan,
            "cluster_selection_method": self.config_storage.cluster_selection_method,
            "prediction_data": self.config_storage.prediction_data,
        }

    def get_bounds(self):
        return {}


class BertParams(BaseModelParams):
    def get_specific_params(self):
        bert_specific_params = {
            "eval_metric": self.config_storage.eval_metric,
            "max_length": self.config_storage.max_length,
            "model_path": self.config_storage.bert_model_path,
            "unfreeze_layers": self.config_storage.unfreeze_layers,
            "learning_rate": self.config_storage.learning_rate,
            "epochs": self.config_storage.epochs,
            "batch_size": self.config_storage.batch_size,
            "sampler_type": self.config_storage.sampler_type,
            "optimizer_type": self.config_storage.optimizer_type,
            "scheduler_type": self.config_storage.scheduler_type,
            "weight_decay": self.config_storage.weight_decay,
            "device": "cuda" if self.config_storage.device == "cuda" else "cpu",
        }
        if self.task == "multiclass":
            bert_specific_params["objective"] = "logloss"

        elif self.task == "binary":
            bert_specific_params["objective"] = "logloss"

        return bert_specific_params

    def get_bounds(self):
        return {}