import abc
from typing import Tuple, Callable
from copy import deepcopy
from abc import ABC
import numpy as np
import pandas as pd
from hyperopt import SparkTrials, STATUS_OK
from hyperopt import fmin, tpe

from dreamml.logging import get_logger
from dreamml.modeling.cv import make_cv
from dreamml.modeling.metrics import BaseMetric
from dreamml.modeling.models.estimators import BaseModel

_logger = get_logger(__name__)


class DistributedOptimizer(ABC):
    def __init__(
        self,
        model: BaseModel,
        params_bounds: dict,
        metric: BaseMetric,
        n_iter: int = 30,
        timeout: int = 7200,
        seed: int = 27,
        parallelism: int = 5,
    ) -> None:
        self.model = model
        self.optimizer = None
        self.metric = metric
        self.maximize = self.metric.maximize
        self.params_bounds = params_bounds
        self.init_points = int(n_iter * 0.2)
        self.n_iter = n_iter
        self.timeout = timeout
        self.seed = seed
        self.X = None
        self.y = None
        self.parallelism = parallelism
        self._logger = model._logger or _logger

    def check_param_value(self, params: dict) -> dict:
        """
        Проверка значений гиперпараметров на валидность.
        Некоторые гиперпараметры могут принимать только целые
        значений, для таких гиперпараметров - проверяется их
        значение и, при необходимости, происходит преобразованье
        в int-тип.

        Parameters
        ----------
        params: dict
            Словарь гиперпараметров, ключ словаря - название
            гиперпараметра, значение - значение гиперпараметра.

        Returns
        -------
        valid_params: dict
            Провалидированный словарь гиперпараметров.

        """
        check_params = [
            "max_depth",
            "num_leaves",
            "min_data_in_leaf",
            "min_child_samples",
            "subsample_for_bin",
            "n_estimators",
        ]
        for name in check_params:
            if params.get(name, None):
                params[name] = int(params[name])

        eps = 1e-5
        for lr_param in ["learning_rate", "lr"]:
            if lr_param in params and params[lr_param] == 0:
                params[lr_param] = params[lr_param] + eps
                self._logger.debug(
                    f"Hyperopt {lr_param} | {params[lr_param] - eps} -> {params[lr_param]}"
                )
        return params

    @abc.abstractmethod
    def fit(self, data: pd.DataFrame, target: pd.Series, eval_sets: dict = None):
        pass


class DistributedOptimizationModel(DistributedOptimizer):
    """
    Hyperopt оптимизация ML-моделей для DreamML.

    Parameters
    ----------
    model: DSPL.models
        Экземпляр модели со стандартизованным API для DS-Template.

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
    init_points: int
        Количество итераций для инициализации оптимизатора.
        Принимается равным 30% от общего числа итераций.

    optimizer: bayes_opt.bayesian_optimization.BayesianOptimization
        Экземпляр оптимизатора bayes_opt.

    """

    def _objective(self, eval_sets: dict) -> Callable[[dict], dict]:
        """
        Функция замыкания для функции оптимизации HyperOpt

        Parameters
        ----------
        eval_sets: dict
            Словарь с ключем название выборки и
            значением кортеж с датасетом признаков и
            вектором целевой переменной

        Returns
        -------
        objective: func

        """

        def objective_split(params: dict) -> dict:
            """
            Функция оптимизации для train/valid/test валидации

            Parameters
            ----------
            params: dict
                Словарь гиперпараметров оптимизируемой модели

            Returns
            -------
            status: dict
                Словарь спицифический для функций оптимизации HyperOpt
            """
            valid_params = self.check_param_value(params)

            estimator = deepcopy(self.model)
            estimator.params.update(valid_params)
            estimator.fit(self.X, self.y, *eval_sets["valid"])
            y_pred = estimator.transform(eval_sets["valid"][0])

            score = self.metric(eval_sets["valid"][1], y_pred)
            self._logger.info("=" * 120)
            return {"loss": -score if self.maximize else score, "status": STATUS_OK}

        return objective_split

    def fit(
        self, data: pd.DataFrame, target: pd.Series, eval_sets: dict = None
    ) -> None:
        """
        Обучение оптимизатора.

        Parameters
        ----------
        eval_sets: dict
        data: pandas.DataFrame, shape = [n_samples, n_features]
            матрица признаков для обучения.

        target: pandas.Series, shape = [n_samples, ]
            вектор истинных ответов.

        """
        self._logger.info("*" * 127)
        self._logger.info("Start fiting optimizer")
        self._logger.info("*" * 127)
        self.X, self.y = data, target
        algo, spark_trials = tpe.suggest, SparkTrials(parallelism=self.parallelism)
        objective = self._objective(eval_sets=eval_sets)

        best_hyperparams = fmin(
            fn=objective,
            space=self.params_bounds,
            trials=spark_trials,
            algo=algo,
            max_evals=self.n_iter,
            rstate=np.random.default_rng(self.seed),
        )
        best_hyperparams = self.check_param_value(best_hyperparams)
        self.model.params.update(best_hyperparams)
        self.model.fit(self.X, self.y, *eval_sets["valid"])
        self.model.evaluate_and_print(**eval_sets)
        self._logger.info("*" * 127)


class DistributedOptimizationCVModel(DistributedOptimizer):
    """
    Hyperopt оптимизация ML-моделей для DreamML на основе кросс-валидации.

    Parameters
    ----------
    model: DSPL.models
        Экземпляр модели со стандартизованным API для DS-Template.

    eval_set: Tuple[pd.DataFrame, pd.Series]
        Набор данных для валидации и подбора гиперпараметров.

    params_bounds: dict
        Словарь c границами оптимизируемых параметров,
        ключ словаря - название гиперпараметра, значение - кортеж
        с минимальным и максимальным значением.

    metric: BaseMetric

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
    init_points: int
        Количество итераций для инициализации оптимизатора.
        Принимается равным 30% от общего числа итераций.

    optimizer: bayes_opt.bayesian_optimization.BayesianOptimization
        Экземпляр оптимизатора bayes_opt.

    """

    def __init__(
        self,
        model,
        params_bounds: dict,
        metric: BaseMetric,
        cv,
        splitter_df: pd.DataFrame,
        n_iter: int = 30,
        timeout: int = 7200,
        seed: int = 27,
        parallelism: int = 5,
    ) -> None:
        super(DistributedOptimizationCVModel, self).__init__(
            model,
            params_bounds,
            metric=metric,
            n_iter=n_iter,
            timeout=timeout,
            seed=seed,
            parallelism=parallelism,
        )
        self.cv = cv
        self.splitter_df = splitter_df
        self.mean_score = None

    def _objective(self) -> Callable[[dict], dict]:
        """
        Функция замыкания для функции оптимизации HyperOpt

        Returns
        -------
        objective: func

        """

        def objective_cv(params) -> dict:
            """
            Функция оптимизации.
            """
            valid_params = self.check_param_value(params)

            estimator = deepcopy(self.model)
            estimator.params.update(valid_params)

            _, score, _, _, _, _ = make_cv(
                estimator=estimator,
                x_train_cv=self.X,
                y_train_cv=self.y,
                cv=self.cv,
                splitter_df=self.splitter_df,
                metric=self.metric,
            )
            return {"loss": -score if self.maximize else score, "status": STATUS_OK}

        return objective_cv

    def fit(
        self, data: pd.DataFrame, target: pd.Series, eval_sets: dict = None
    ) -> dict:
        """
        Обучение оптимизатора.

        Parameters
        ----------
        eval_sets: dict
        data: pandas.DataFrame, shape = [n_samples, n_features]
            матрица признаков для обучения.

        target: pandas.Series, shape = [n_samples, ]
            вектор истинных ответов.

        """
        self._logger.info("*" * 127 + "\nStart fiting optimizer\n" + "*" * 127)
        self.X, self.y = data, target
        algo, spark_trials = tpe.suggest, SparkTrials(parallelism=self.parallelism)
        objective = self._objective()

        best_hyperparams = fmin(
            fn=objective,
            space=self.params_bounds,
            trials=spark_trials,
            algo=algo,
            max_evals=self.n_iter,
            timeout=self.timeout,
            rstate=np.random.default_rng(self.seed),
        )
        best_hyperparams = self.check_param_value(best_hyperparams)
        self.model.params.update(best_hyperparams)

        estimators, score, _, _, _, _ = make_cv(
            estimator=self.model,
            x_train_cv=self.X,
            y_train_cv=self.y,
            cv=self.cv,
            splitter_df=self.splitter_df,
            metric=self.metric,
        )
        self.mean_score = score
        self._logger.info("*" * 127)
        return best_hyperparams