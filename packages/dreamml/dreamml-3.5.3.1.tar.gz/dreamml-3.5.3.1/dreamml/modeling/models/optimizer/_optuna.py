from abc import ABC
from copy import deepcopy
from typing import Tuple

import optuna
import pandas as pd
from optuna import Trial

from dreamml.logging import get_logger
from dreamml.modeling.cv import make_cv
from dreamml.modeling.metrics import BaseMetric

_logger = get_logger(__name__)


class OptunaOptimizator(ABC):
    def __init__(self, params_bounds, model):
        self.model = model
        self.params_bounds = params_bounds
        self._logger = model._logger or _logger

    @staticmethod
    def _check_param_value(param_name):
        """ """
        # FIXME: Нужно задавать распределение параметра в одном месте в конфиге,
        #  параметры брать тоже из одного места (не из ..)
        integer_params = [
            "max_depth",
            "num_leaves",
            "subsample_for_bin",
            "min_child_weight",
            "scale_pos_weight",
            "max_bin",
            "min_data_in_bin",
            "epochs",
            "batch_size",
            "max_iter",
            "num_topics",
            "num_models",
            "iterations",
        ]
        loginteger_params = [
            "min_child_samples",
            "min_data_in_leaf",
        ]
        discrete_params = [
            "subsample",
            "colsample_bytree",
            "colsample_bylevel",
            "colsample",
        ]
        loguniform_params = [
            "learning_rate",
            "lr",
            "gamma",
            "alpha",
            "reg_alpha",
            "reg_lambda",
            "l2_leaf_reg",
            "min_split_gain",
            "lambda_l2",
            "C",
            "eta",
            "weight_decay",
            "tol",
            "l1_ratio",
        ]
        category_params = [
            "optimizer_type",
            "scheduler_type",
            "sampler_type",
            "penalty",
            "solver",
        ]

        if param_name in integer_params:
            return "integer"
        elif param_name in loginteger_params:
            return "loginteger"
        elif param_name in discrete_params:
            return "discrete"
        elif param_name in loguniform_params:
            return "loguniform"
        elif param_name in category_params:
            return "category"
        else:
            raise ValueError(
                f"Для параметра {param_name} не задано распределение для сэмплирования при оптимизации."
            )

    def prepare_params(self, trial: Trial):
        params = deepcopy(self.model.params)
        for param_name in self.params_bounds:
            param_type = self._check_param_value(param_name)

            if param_type == "integer":
                param_value_min, param_value_max = self.params_bounds[param_name]
                params[param_name] = trial.suggest_int(
                    param_name, param_value_min, param_value_max
                )
            elif param_type == "loginteger":
                param_value_min, param_value_max = self.params_bounds[param_name]
                params[param_name] = trial.suggest_int(
                    param_name, param_value_min, param_value_max, log=True
                )
            elif param_type == "discrete":
                param_value_min, param_value_max = self.params_bounds[param_name]
                params[param_name] = trial.suggest_discrete_uniform(
                    param_name, param_value_min, param_value_max, 0.1
                )
            elif param_type == "loguniform":
                param_value_min, param_value_max = self.params_bounds[param_name]
                params[param_name] = trial.suggest_loguniform(
                    param_name, param_value_min, param_value_max
                )
            elif param_type == "category":
                params[param_name] = trial.suggest_categorical(
                    param_name, self.params_bounds[param_name]
                )
            else:
                _logger.warning(
                    f"Заданный параметр '{param_name}' не включён в список параметров Optuna"
                )
        return params


class CVOptunaOptimizationModel(OptunaOptimizator):
    """
    Optuna-оптимизация ML-моделей для DreamML.

    Parameters
    ----------
    model: DSPL.models
        Экземпляр модели со стандартизованным API для DreamML.

    metric: BaseMetric
        Метрика для оценки качества модели.

    eval_set: Tuple[pd.DataFrame, pd.Series]
        Набор данных для валидации и подбора гиперпараметров.

    params_bounds: dict
        Словарь c границами оптимизируемых параметров,
        ключ словаря - название гиперпараметра, значение - кортеж
        с минимальным и максимальным значением.

    maximize: bool, optional, default = True
        Флаг максимизации метрики. Опциональный параметр,
        по умолчанию True. Если равен True, то цель оптимизации -
        максимизация metric, если равен False, то цель
        оптимизации - минимизация metric.

    n_iter: int, optional, default = 30
        Количество итераций работы оптимизатора.

    seed: int, optional, default = 27
        it's random_state position.

    Attributes
    ----------

    optimizer: optuna.study.Study
        Экземпляр оптимизатора Optuna.

    """

    def __init__(
        self,
        model,
        cv,
        metric: BaseMetric,
        params_bounds: dict,
        splitter_df: pd.DataFrame,
        n_iter: int = 64,
        timeout: int = 7200,
        seed: int = 27,
    ) -> None:

        super().__init__(params_bounds, model)
        self.cv = cv
        self.splitter_df = splitter_df
        self.metric = metric
        self.optimizer = None
        self.train_set = None
        self.maximize = metric.maximize
        self.n_iter = n_iter
        self.timeout = timeout
        self.seed = seed
        self.direction = "minimize"

    def objective(self, trial: Trial) -> float:
        """
        Функция оптимизации.
        """

        prepared_model_params = self.prepare_params(trial)

        if self.model.model_name == "log_reg":
            if (
                "penalty" in prepared_model_params
                and prepared_model_params["penalty"] == "elasticnet"
            ):
                prepared_model_params["l1_ratio"] = trial.suggest_uniform(
                    "l1_ratio", 0.0, 1.0
                )
            else:
                prepared_model_params["l1_ratio"] = None

        self.model.params = prepared_model_params
        _, cv_score, _, _, _, _ = make_cv(
            estimator=self.model,
            x_train_cv=self.train_set[0],
            y_train_cv=self.train_set[1],
            cv=self.cv,
            splitter_df=self.splitter_df,
            metric=self.metric,
        )

        if self.maximize:
            metric = -cv_score
        else:
            metric = cv_score

        self._logger.debug(f"Trial({trial.number}) params: {trial.params}")
        self._logger.info(f"Trial({trial.number}) score: {cv_score}")

        return metric

    def fit(self, data, target) -> None:
        """
        Обучение оптимизатора.

        Parameters
        ----------
        data: pandas.DataFrame, shape = [n_samples, n_features]
            матрица признаков для обучения.

        target: pandas.Series, shape = [n_samples, ]
            вектор истинных ответов.

        """
        self.train_set = (data, target)
        self.optimizer = optuna.create_study(
            sampler=optuna.samplers.TPESampler(seed=self.seed),
            direction=self.direction,
        )
        self.optimizer.optimize(
            self.objective,
            n_trials=self.n_iter,
            timeout=self.timeout,
            show_progress_bar=True,
        )
        max_params = self.optimizer.best_params

        return max_params


class OptunaOptimizationModel(OptunaOptimizator):
    """
    Optuna-оптимизация ML-моделей для DreamML на Hold-OUT.

    Parameters
    ----------
    model: DSPL.models
        Экземпляр модели со стандартизованным API для DreamML.

    metric: BaseMetric
        Метрика для оценки качества модели.

    eval_set: Tuple[pd.DataFrame, pd.Series]
        Набор данных для валидации и подбора гиперпараметров.

    params_bounds: dict
        Словарь c границами оптимизируемых параметров,
        ключ словаря - название гиперпараметра, значение - кортеж
        с минимальным и максимальным значением.

    maximize: bool, optional, default = True
        Флаг максимизации метрики. Опциональный параметр,
        по умолчанию True. Если равен True, то цель оптимизации -
        максимизация metric, если равен False, то цель
        оптимизации - минимизация metric.

    n_iter: int, optional, default = 30
        Количество итераций работы оптимизатора.

    seed: int, optional, default = 27
        it's random_state position.

    Attributes
    ----------
    optimizer: optuna.study.Study
        Экземпляр оптимизатора Optuna.

    """

    def __init__(
        self,
        model,
        metric: BaseMetric,
        eval_set: Tuple[pd.DataFrame, pd.Series],
        params_bounds: dict,
        n_iter: int = 30,
        timeout: int = 7200,
        seed: int = 27,
    ) -> None:

        super().__init__(params_bounds, model)
        self.metric = metric
        self.optimizer = None
        self.eval_set = eval_set
        self.maximize = metric.maximize
        self.n_iter = n_iter
        self.timeout = timeout
        self.seed = seed
        self.direction = "minimize"

    def fit(self, data, target) -> None:
        """
        Обучение оптимизатора.

        Parameters
        ----------
        data: pandas.DataFrame, shape = [n_samples, n_features]
            матрица признаков для обучения.

        target: pandas.Series, shape = [n_samples, ]
            вектор истинных ответов.

        """
        self.train_set = (data, target)
        self.optimizer = optuna.create_study(
            sampler=optuna.samplers.TPESampler(seed=self.seed),
            direction=self.direction,
        )
        self.optimizer.optimize(
            self.objective,
            n_trials=self.n_iter,
            timeout=self.timeout,
            show_progress_bar=True,
        )
        max_params = self.optimizer.best_params
        self.model.params.update(max_params)

        if self.model.task == "topic_modeling":
            self.model.fit(self.train_set)
        else:
            self.model.fit(*self.train_set, *self.eval_set)

    def objective(self, trial: Trial) -> float:
        """
        Функция оптимизации.
        """
        prepared_model_params = self.prepare_params(trial)

        if self.model.model_name == "log_reg":
            if (
                "penalty" in prepared_model_params
                and prepared_model_params["penalty"] == "elasticnet"
            ):
                prepared_model_params["l1_ratio"] = trial.suggest_uniform(
                    "l1_ratio", 0.0, 1.0
                )
            else:
                prepared_model_params["l1_ratio"] = None

        self.model.params = prepared_model_params

        if self.model.task == "topic_modeling":
            self.model.fit(self.train_set)

            if self.maximize:
                metric = -self.metric(self.model.topic_modeling_data)
            else:
                metric = self.metric(self.model.topic_modeling_data)

        else:
            self.model.fit(*self.train_set, *self.eval_set)
            y_pred = self.model.transform(self.eval_set[0])

            if self.maximize:
                metric = -self.metric(self.eval_set[1], y_pred)
            else:
                metric = self.metric(self.eval_set[1], y_pred)

        params = ""
        for k, v in trial.params.items():
            params += f"{k}: {v}\n"

        self._logger.debug(f"Trial({trial.number}) params: \n{params}")
        self._logger.info(f"Trial({trial.number}) score: {metric}\n")

        return metric