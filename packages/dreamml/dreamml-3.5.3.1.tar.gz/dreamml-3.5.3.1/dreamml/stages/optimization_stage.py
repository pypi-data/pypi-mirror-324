import logging
from copy import deepcopy
from operator import gt, lt
from typing import Any, Dict

import numpy as np
from typing import List

from dreamml.data._hadoop import create_spark_session, stop_spark_session
import optuna
import pandas as pd
from py4j.protocol import Py4JJavaError
from sklearn.exceptions import NotFittedError

from dreamml.modeling.models.estimators import BoostingBaseModel, BaseModel
from dreamml.pipeline.fitter import FitterBase
from dreamml.stages.stage import BaseStage

optuna.logging.set_verbosity(optuna.logging.WARNING)

from dreamml.configs.config_storage import ConfigStorage
from dreamml.data._dataset import DataSet
from dreamml.utils import ValidationType
from dreamml.utils.spark_init import init_spark_env
from dreamml.utils.spark_session_configuration import spark_conf
from dreamml.stages.model_based_stage import ModelBasedStage
from dreamml.stages.algo_info import AlgoInfo
from dreamml.utils.get_n_iterartions import get_n_iterations

from dreamml.modeling.models.optimizer import (
    BayesianOptimizationModel,
    CVBayesianOptimizationModel,
    OptunaOptimizationModel,
    CVOptunaOptimizationModel,
    DistributedOptimizationModel,
    DistributedOptimizationCVModel,
)
from dreamml.logging import get_logger


_logger = get_logger(__name__)


class OptimizationStage(ModelBasedStage):
    """
    Этап поиска оптимальных гиперпараметров модели.
    """

    name = "optimization"

    def __init__(
        self,
        algo_info: AlgoInfo,
        config: ConfigStorage,
        fitter: FitterBase,
        vectorization_name: str = None,
    ):
        super().__init__(
            algo_info=algo_info,
            config=config,
            fitter=fitter,
            vectorization_name=vectorization_name,
        )
        # TODO Лучше не хранить объект конфига в стейдже, а взять все нужные параметры из него
        self.config_storage = config
        self.predictions = None
        self.tempdir = None

    @property
    def check_is_fitted(self):
        if not self.is_fitted:
            msg = (
                "This estimator is not fitted yet. Call 'fit' with "
                "appropriate arguments before using this estimator."
            )
            raise NotFittedError(msg)
        return True

    def _set_used_features(self, data_storage: DataSet, used_features: List = None):
        if not used_features:
            data = data_storage.get_eval_set(
                used_features, vectorization_name=self.vectorization_name
            )
            used_features = data["train"][0].columns.tolist()

        used_features = self._drop_text_features(data_storage, used_features)
        return used_features

    def _get_cv_optimizer(
        self,
        optimizer_type,
        splitter_df,
        model,
        optimization_grid_params,
        distributed_grid_params,
        optimization_iters,
        optimizer_timeout,
        random_seed,
    ):
        if optimizer_type == "local":
            return CVOptunaOptimizationModel(
                model=model,
                cv=self.fitter.cv,
                metric=self.eval_metric,
                params_bounds=optimization_grid_params,
                n_iter=optimization_iters,
                timeout=optimizer_timeout,
                seed=random_seed,
                splitter_df=splitter_df,
            )
        elif optimizer_type == "optuna":
            return CVOptunaOptimizationModel(
                model=model,
                cv=self.fitter.cv,
                metric=self.eval_metric,
                params_bounds=optimization_grid_params,
                n_iter=optimization_iters,
                timeout=optimizer_timeout,
                seed=random_seed,
                splitter_df=splitter_df,
            )
        elif optimizer_type == "bayesian":
            return CVBayesianOptimizationModel(
                model=model,
                cv=self.fitter.cv,
                metric=self.eval_metric,
                maximize=self.eval_metric.maximize,
                params_bounds=optimization_grid_params,
                n_iter=optimization_iters,
                timeout=optimizer_timeout,
                seed=random_seed,
                splitter_df=splitter_df,
            )
        elif optimizer_type == "distributed":
            return DistributedOptimizationCVModel(
                model=model,
                metric=self.eval_metric,
                cv=self.fitter.cv,
                params_bounds=distributed_grid_params,
                n_iter=optimization_iters,
                timeout=optimizer_timeout,
                seed=random_seed,
                splitter_df=splitter_df,
            )
        else:
            raise ValueError(f"Wrong optimizer type: {optimizer_type}")

    def _get_ho_optimizer(
        self,
        optimizer_type,
        model,
        data,
        optimization_grid_params,
        distributed_grid_params,
        optimization_iters,
        optimizer_timeout,
        random_seed,
    ):
        if optimizer_type == "local":
            return OptunaOptimizationModel(
                model=model,
                metric=self.eval_metric,
                eval_set=data["valid"],
                params_bounds=optimization_grid_params,
                n_iter=optimization_iters,
                timeout=optimizer_timeout,
                seed=random_seed,
            )
        elif optimizer_type == "optuna":
            return OptunaOptimizationModel(
                model=model,
                metric=self.eval_metric,
                eval_set=data["valid"],
                params_bounds=optimization_grid_params,
                n_iter=optimization_iters,
                timeout=optimizer_timeout,
                seed=random_seed,
            )
        elif optimizer_type == "bayesian":
            return BayesianOptimizationModel(
                model=model,
                metric=self.eval_metric,
                maximize=self.eval_metric.maximize,
                eval_set=data["valid"],
                params_bounds=optimization_grid_params,
                n_iter=optimization_iters,
                timeout=optimizer_timeout,
                seed=random_seed,
            )
        elif optimizer_type == "distributed":
            return DistributedOptimizationModel(
                model=model,
                metric=self.eval_metric,
                params_bounds=distributed_grid_params,
                n_iter=optimization_iters,
                timeout=optimizer_timeout,
                seed=random_seed,
            )
        else:
            raise ValueError(f"Wrong optimizer type: {optimizer_type}")

    def _set_optimizer(
        self,
        model,
        opt_type,
        data_storage: DataSet,
        used_features: List = None,
        splitter_df: pd.DataFrame = None,
    ):
        """
        Функция выбора оптимизатора.

        Parameters
        ----------
        model: dreamml.modeling.models.estimators._base.BaseModel
            Экземпляр модели для обучения.

        opt_type: str
            Тип оптимизации ("auto", "local", "optuna", "bayesian", "distributed")

        data_storage: DataSet
            Экземпляр класса-хранилища данных

        used_features: List
            Список используемых признаков.

        Returns
        -------
        best_estimator: Union[OptunaOptimizationModel, DistributedOptimizationModel, BayesianOptimizationModel,
         CVOptunaOptimizationModel, CVBayesianOptimizationModel, DistributedOptimizationCVModel]
            Экземпляр оптимизированной модели.
        """
        optimization_iters = self.config_storage.n_iterations
        optimizer_timeout = self.config_storage.optimizer_timeout

        if optimizer_timeout == "auto":
            optimization_iters = None

        if optimization_iters == "auto":
            optimization_iters = get_n_iterations(data_storage.get_dev_n_samples())
            self.config_storage.n_iterations_used = optimization_iters
        model_name = model.model_name  # XGBoost, LightGBM, CatBoost, etc
        _, _, optimization_grid_params = self.config_storage.get_model_by_str(
            model_name=model_name
        )
        distributed_grid_params = self.config_storage.get_hyperopt_grid(
            bound_params=optimization_grid_params
        )
        if self.vectorization_name == "bert":
            optimization_grid_params = self.config_storage.get_bert_grid_params(
                bound_params=optimization_grid_params
            )

        if model_name == "log_reg":
            if optimization_iters > 50:
                optimization_iters = 50
                self.config_storage.n_iterations_used_log_reg = optimization_iters
                _logger.info(
                    f"log_reg optimization is set to {optimization_iters} iterations."
                )
            optimization_grid_params = self.config_storage.get_logistic_grid_params(
                bound_params=optimization_grid_params
            )

        data = data_storage.get_eval_set(
            used_features, vectorization_name=self.vectorization_name
        )
        random_seed = self.config_storage.random_seed
        parallelism = self.config_storage.parallelism
        # TODO: в следующих релизах mpack добавть подачу parallelism в гиперопт (сейчас в dreamml.modeling по дефолту 5)

        train_size = data["train"][0].shape[0]
        self._check_optimization_params(optimization_grid_params, train_size)

        validation_type = self.fitter.validation_type
        if validation_type == ValidationType.CV:
            if splitter_df is None:
                raise ValueError(f"splitter_df is required for cross-validation.")

            return self._get_cv_optimizer(
                opt_type,
                splitter_df,
                model,
                optimization_grid_params,
                distributed_grid_params,
                optimization_iters,
                optimizer_timeout,
                random_seed,
            )
        else:
            assert validation_type == ValidationType.HOLDOUT

            return self._get_ho_optimizer(
                opt_type,
                model,
                data,
                optimization_grid_params,
                distributed_grid_params,
                optimization_iters,
                optimizer_timeout,
                random_seed,
            )

    @staticmethod
    def _check_optimization_params(optimization_grid_params: dict, train_size: int):
        if "min_child_samples" in optimization_grid_params:
            min_child_samples = optimization_grid_params["min_child_samples"]
            right_border = max(train_size // 4, 5)
            optimization_grid_params["min_child_samples"] = (
                min_child_samples[0],
                right_border,
            )
        return optimization_grid_params

    def _get_optimized_model(
        self,
        init_hyperparams: Dict[str, Any],
        data_storage: DataSet,
        used_features: List = None,
    ):
        """
        Функция оптимизации гиперпараметров модели.

        Parameters
        ----------
        init_hyperparams: Dict[str, Any]
            Изначальные параметры модели

        data_storage: DataSet
            Экземпляр класса-хранилища данных

        used_features: List
            Список используемых признаков.

        Returns
        -------
        best_estimator: dreamml.models.estimators
            Экземпляр оптимизированной модели.
        """
        if self.config_storage.n_iterations == 0:
            return self
        opt_model = self._init_model(
            used_features=used_features, hyperparams=init_hyperparams
        )
        opt_model.verbose = 0
        opt_type = self.config_storage.optimizer
        if opt_type == "auto":
            opt_type = "local"
        data = data_storage.get_eval_set(
            used_features, vectorization_name=self.vectorization_name
        )
        if self.fitter.validation_type == ValidationType.CV:
            x, y = data_storage.get_cv_data_set(
                used_features, vectorization_name=self.vectorization_name
            )
        else:
            x, y = data["train"]
            if (
                self.config_storage.use_sampling
                and data_storage.get_dev_n_samples() >= 250000
            ):
                x, y = data_storage.sample(
                    used_features, vectorization_name=self.vectorization_name
                )

        random_seed = self.config_storage.random_seed
        np.random.seed(random_seed)

        if self.fitter.validation_type == ValidationType.CV:
            splitter_df = data_storage.get_cv_splitter_df(
                self.fitter.cv.get_required_columns()
            )
        else:
            splitter_df = None

        optimizer = self._set_optimizer(
            opt_model, opt_type, data_storage, used_features, splitter_df
        )
        if opt_type == "distributed":
            try:
                init_spark_env(libraries_required=True)

                # Временный (вечный) конфиг на время тестирования гиперопта
                spark_config = deepcopy(spark_conf)
                spark_config.set("spark.dynamicAllocation.maxExecutors", "5").set(
                    "spark.executor.cores", "1"
                )

                spark = create_spark_session(
                    spark_config=spark_config, temp_dir=self.tempdir
                )
                max_params = optimizer.fit(x, y, data)  # CV - max params, HO - None

                stop_spark_session(spark=spark, temp_dir=self.tempdir)
            except (Py4JJavaError, ImportError) as e:
                logging.exception(
                    f"{'*' * 127}\nBayesianOptimizationModel is used instead DistributedOptimizationModel "
                    f"because: {str(e)}\n{'*' * 127}\n"
                )
                optimizer = self._set_optimizer(
                    opt_model, "optuna", data_storage, used_features, splitter_df
                )
                max_params = optimizer.fit(x, y)
        else:
            max_params = optimizer.fit(x, y)

        if self.fitter.validation_type != ValidationType.CV:
            max_params = optimizer.model.params

        best_params = deepcopy(init_hyperparams)
        best_params.update(max_params)
        best_estimator = self._init_model(
            used_features=used_features, hyperparams=best_params
        )

        return best_estimator

    def _fit(
        self,
        model: BaseModel,
        used_features: List[str],
        data_storage: DataSet,
        models: List[BoostingBaseModel] = None,
    ) -> BaseStage:
        """
        Основная функция для запуска этапа.

        Parameters
        ----------
        model: dreamml.modeling.models.estimators.boosting_base.BoostingBaseModel
            Экземпляр модели для обучения.

        models: List[estimator]
            Список с моделями полученными на CV (здесь для совместимости)

        data_storage: DataSet
            Экземпляр класса-хранилища данных

        used_features: List
            Список используемых признаков.

        Returns
        -------
        self
        """
        np.random.seed(self.config_storage.random_seed)
        self.tempdir = self.config_storage.get_temp_dir()
        self.used_features = used_features
        if not self.used_features:
            self.used_features = model.used_features
        model_ = self._init_model(
            used_features=self.used_features, hyperparams=model.params
        )
        model_.verbose = 0
        model_, models_, self.predictions = self.fitter.train(
            estimator=model_,
            data_storage=data_storage,
            metric=self.eval_metric,
            used_features=self.used_features,
            vectorization_name=self.vectorization_name,
        )

        opt_estimator = self._get_optimized_model(
            init_hyperparams=model_.params,
            data_storage=data_storage,
            used_features=self.used_features,
        )

        np.random.seed(self.config_storage.random_seed)
        opt_model, opt_models, opt_predictions = self.fitter.train(
            estimator=opt_estimator,
            data_storage=data_storage,
            metric=self.eval_metric,
            used_features=self.used_features,
            vectorization_name=self.vectorization_name,
        )

        if self.task == "topic_modeling":
            current_score = self.eval_metric(model_.topic_modeling_data)
            opt_score = self.eval_metric(opt_model.topic_modeling_data)
        else:
            y_true = self.fitter.get_validation_target(
                data_storage, vectorization_name=self.vectorization_name
            )
            current_score = self.eval_metric(y_true, self.predictions)
            opt_score = self.eval_metric(y_true, opt_predictions)

        self.choose_best_model(
            current_score, model_, models_, opt_model, opt_models, opt_score
        )

        self.prediction = self.prediction_out(data_storage)
        self.is_fitted = True
        return self

    def choose_best_model(
        self, current_score, model_, models_, opt_model, opt_models, opt_score
    ):
        comp = gt if self.eval_metric.maximize else lt
        if comp(opt_score, current_score):
            self.final_model = opt_model
            self.models = opt_models
            selected_model = "Optimized model"
        else:
            # TODO может быть менять имя стейджа, если возвращается модель с предыдущего стейджа
            self.final_model = model_
            self.models = models_
            selected_model = "Base model"

        msg = f"\nMetric name: {self.eval_metric.name} (Maximize: {self.eval_metric.maximize})"
        msg += f"\nBase model score: {current_score}"
        msg += f"\nOptimized model score: {opt_score}"
        msg += f"\nВыбранная модель: {selected_model}"
        params = "\n"
        for k, v in self.final_model.params.items():
            params += f"{k}: {v}\n"
        msg += f"\nГиперпараметры финальной модели: {params}"

        _logger.debug(msg)

    def transform(self):
        self.check_is_fitted
        # estimator, used_features, feature_importance, predictions, cv_estimators
        return (
            self.final_model,
            self.used_features,
            self.feature_importance,
            self.predictions,
            self.models,
        )

    def _set_params(self, params: dict):
        raise NotImplementedError