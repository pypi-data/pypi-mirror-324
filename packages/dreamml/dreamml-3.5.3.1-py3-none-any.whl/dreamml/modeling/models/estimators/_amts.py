import numpy as np
import pandas as pd
from scipy.optimize import minimize
import optuna
import random
import logging
from prophet import Prophet
from prophet.diagnostics import cross_validation, performance_metrics
from typing import Dict, Any
import multiprocessing as mp

from dreamml.logging.logger import CombinedLogger
from dreamml.logging import get_logger
from dreamml.modeling.models.estimators import BaseModel

_logger = get_logger(__name__)

import gc


class AMTSModel(BaseModel):
    model_name = "AMTS"
    """
    Класс Alt-mode timeseries

    Parameters
    ----------
    estimator_params : dict
        Словарь с гиперпараметрами
    task : str
        Название задачи (regression, binary, multi, ...)
    metric_name : str
        Название метрики
    metric_params: dict
        Параметры метрики

    Attributes
    ----------
    estimator_class
        Экземпляр базовой модели
    n_iterations: int
        Кол-во итераций для оптимизации
    split_by_group: bool
    group_column: str
        Название столбца с группами
    horizon: int
        Горизонт прогнозирования
    models_by_groups: dict
        Словарь key - сегмент, value - базовая модель
    hyper_params_by_group: dict
        Словарь key - сегмент, value - гиперпараметры для калибровки
    """

    def __init__(
        self,
        estimator_params: Dict[str, Any],
        task: str,
        metric_name=None,
        metric_params: Dict = None,
        **params,
    ):
        super().__init__(
            estimator_params=estimator_params,
            task=task,
            metric_name=metric_name,
            metric_params=metric_params,
            **params,
        )
        self.estimator_class = self._estimators.get(self.task)
        self.n_iterations = self.params["n_iterations"]
        self.split_by_group = self.params["split_by_group"]
        self.group_column = self.params["group_column"]
        self.horizon = self.params["horizon"]
        self.time_column_frequency = self.params["time_column_frequency"]
        self.final_fit = False

        self.models_by_groups = dict()
        self.hyper_params_by_group = dict()
        self.hyper_params_calib_by_groups = dict()

        self.forecast = None
        self.df_prophet_dev = None
        self.cross_val_initial = 0
        self.cross_val_period = 0
        self.cross_val_horizon = 0

        self.mem_info = 0

    @property
    def _estimators(self):
        estimators = {"amts": Prophet}
        return estimators

    def process_group(self, group_data):
        group_name, df_group = group_data

        self.df_prophet_dev = df_group[: -self.horizon]
        if self.final_fit:
            self.df_prophet_dev = df_group

        self.calculate_cross_val_params()

        study = optuna.create_study(direction="minimize")
        study.optimize(
            func=self.optuna_obj, n_trials=self.n_iterations, show_progress_bar=True
        )

        logging.getLogger("cmdstanpy").disabled = True
        self.estimator = self.estimator_class(**study.best_params)
        self.estimator.fit(self.df_prophet_dev[["ds", "y"]])

        self.forecast = np.array(
            self.estimator.predict(self.df_prophet_dev["ds"].to_frame())["yhat"]
        )
        logging.getLogger("cmdstanpy").disabled = False

        hyper_params_calib_by_groups = dict()

        if self.time_column_frequency.value == "D":
            self.optimize_hyper_params(model_name=f"model_{group_name}")
            hyper_params_calib_by_groups.update(
                self.hyper_params_calib_by_groups[f"model_{group_name}"]
            )
        gc.collect()

        return (
            f"model_{group_name}",
            self.estimator,
            study.best_params,
            hyper_params_calib_by_groups,
        )

    def parallel_optimization(self, df, group_column):
        groups = [
            (group_name, df_group) for group_name, df_group in df.groupby(group_column)
        ]
        with mp.Pool(mp.cpu_count() - 2) as pool:
            results = []
            for result in pool.imap(self.process_group, groups):
                results.append(result)
                gc.collect()

        models_by_groups = {
            model_name: estimator for model_name, estimator, _, _ in results
        }
        hyper_params_by_group = {
            model_name: best_params for model_name, _, best_params, _ in results
        }
        hyper_params_calib_by_groups = {
            model_name: calib_params for model_name, _, _, calib_params in results
        }

        return models_by_groups, hyper_params_by_group, hyper_params_calib_by_groups

    def fit_group(self, amts_data: Dict):
        """
        Обучение и оптимизация модели на данных amts_data по группам.

        Parameters
        ----------
        amts_data: Dict,  {sample_name, Tuple(X, y)}
        """
        df = amts_data["train"][0]
        df["y"] = amts_data["train"][1]

        (
            self.models_by_groups,
            self.hyper_params_by_group,
            self.hyper_params_calib_by_groups,
        ) = self.parallel_optimization(
            df=df,
            group_column=self.group_column,
        )

        self.fitted = True

    def fit(self, amts_data: Dict, final=False):
        """
        Обучение и оптимизация модели на данных amts_data.

        Parameters
        ----------
        amts_data: Dict,  {sample_name, Tuple(X, y)}
        """
        self.final_fit = final

        if self.split_by_group:
            self.fit_group(amts_data)
            return

        self.df_prophet_dev = amts_data["train"][0]
        self.df_prophet_dev["y"] = amts_data["train"][1]

        self.calculate_cross_val_params()

        study = optuna.create_study(direction="minimize")
        study.optimize(
            func=self.optuna_obj, n_trials=self.n_iterations, show_progress_bar=True
        )

        logging.getLogger("cmdstanpy").disabled = True
        self.estimator = self.estimator_class(**study.best_params)
        self.estimator.fit(self.df_prophet_dev[["ds", "y"]])
        self.forecast = np.array(
            self.estimator.predict(self.df_prophet_dev["ds"].to_frame())["yhat"]
        )
        logging.getLogger("cmdstanpy").disabled = False

        # оптимизация параметров: "is_weekend", "is_holiday", "is_pre_holiday" , "is_pre_pre_holiday"
        if self.time_column_frequency.value == "D":
            self.optimize_hyper_params(model_name="model_0")

        self.models_by_groups["model_0"] = self.estimator
        self.hyper_params_by_group["model_0"] = study.best_params

        self.fitted = True

    def prophet_crossval(self, params):
        logging.getLogger("cmdstanpy").disabled = True
        model = Prophet(**params)
        model.fit(self.df_prophet_dev)
        df_cv = cross_validation(
            model,
            initial=f"{self.cross_val_initial} days",
            period=f"{self.cross_val_period} days",
            horizon=f"{self.cross_val_horizon} days",
            parallel=None if self.split_by_group else "processes",
        )
        df_p = performance_metrics(df_cv)
        logging.getLogger("cmdstanpy").disabled = False
        loss = 0
        try:
            loss = df_p["mape"].mean()
        except Exception as e:
            pass
        return loss

    def optuna_obj(self, trial):
        """
        Оптимизация параметров для модели Prophet. Loss-Function для optuna
        """
        params = {
            "changepoint_prior_scale": trial.suggest_loguniform(
                name="changepoint_prior_scale", low=0.01, high=10
            ),
            "seasonality_prior_scale": trial.suggest_loguniform(
                name="seasonality_prior_scale", low=0.1, high=10
            ),
            "weekly_seasonality": trial.suggest_int(
                name="weekly_seasonality", low=0, high=10
            ),
            "yearly_seasonality": trial.suggest_int(
                name="yearly_seasonality", low=0, high=20
            ),
        }

        return self.prophet_crossval(params)

    def optimize_hyper_params(self, model_name: str):
        """
        Оптимизация параметров для признаков ["is_weekend", "is_holiday", "is_pre_holiday", "is_pre_pre_holiday"].
        """
        self.hyper_params_calib_by_groups[model_name] = {
            "is_weekend": random.normalvariate(0, 1),
            "is_holiday": random.normalvariate(0, 1),
            "is_pre_holiday": random.normalvariate(0, 1),
            "is_pre_pre_holiday": random.normalvariate(0, 1),
        }

        target = np.array(self.df_prophet_dev["y"])
        forecast = self.forecast
        for name_param, w_init in self.hyper_params_calib_by_groups[model_name].items():
            b = np.array(self.df_prophet_dev[name_param])
            results = minimize(
                self.calibration_obj,
                w_init,
                args=(target, forecast, b),
                method="Nelder-Mead",
            )
            loss, opt_w = results.fun, results.x
            self.hyper_params_calib_by_groups[model_name][name_param] = opt_w

    def calibration_obj(self, w, target, forecast, b):
        """
        Loss-Function для оптимизация параметров под признаки ["is_weekend", "is_holiday", "is_pre_holiday", "is_pre_pre_holiday"].
        """
        return self.objective(target, (forecast + (w * b)))

    def calculate_cross_val_params(self):
        if self.time_column_frequency.value == "H":
            self.cross_val_initial = int(int(len(self.df_prophet_dev) * 0.2) / 24)
            self.cross_val_period = int(int(len(self.df_prophet_dev) * 0.1) / 24)
            self.cross_val_horizon = int(self.horizon / 24)

        if self.time_column_frequency.value == "D":
            self.cross_val_initial = int(len(self.df_prophet_dev) * 0.2)
            self.cross_val_period = int(len(self.df_prophet_dev) * 0.1)
            self.cross_val_horizon = self.horizon

        if self.time_column_frequency.value == "W":
            self.cross_val_initial = int(len(self.df_prophet_dev) * 0.2) * 7
            self.cross_val_period = int(len(self.df_prophet_dev) * 0.1) * 7
            self.cross_val_horizon = self.horizon * 7

        if self.time_column_frequency.value == "M":
            self.cross_val_initial = int(len(self.df_prophet_dev) * 0.2) * 30
            self.cross_val_period = int(len(self.df_prophet_dev) * 0.1) * 30
            self.cross_val_horizon = self.horizon * 30

        if self.time_column_frequency.value == "Y":
            self.cross_val_initial = int(len(self.df_prophet_dev) * 0.2) * 365
            self.cross_val_period = int(len(self.df_prophet_dev) * 0.1) * 365
            self.cross_val_horizon = self.horizon * 365

    def transform(self, df_prophet: pd.DataFrame) -> np.array:
        """
        Применение обученной модели к данным df_prophet.
        Для применения модели должен быть ранее вызван метод fit
        и создан self.estimator. Если метод fit не был вызван, то
        будет вызвано исключение.

        Parameters
        ----------
        df_prophet: pandas.DataFrame, shape = [n_samples, n_features]
            Матрица признаков (выборка для применения модели).

        Returns
        -------
        prediction: array-like, shape = [n_samples, ]
            Вектор с прогнозами модели на данных data.
        """
        if self.split_by_group:
            forecast_dict = dict()
            for group_name, df_group in df_prophet.groupby(self.group_column):
                forecast = np.array(
                    self.models_by_groups[f"model_{group_name}"].predict(df_group)[
                        "yhat"
                    ]
                )
                if self.time_column_frequency.value == "D":
                    forecast = forecast
                    +(
                        self.hyper_params_calib_by_groups[f"model_{group_name}"][
                            "is_weekend"
                        ]
                        * df_prophet["is_weekend"]
                    )
                    +(
                        self.hyper_params_calib_by_groups[f"model_{group_name}"][
                            "is_holiday"
                        ]
                        * df_prophet["is_holiday"]
                    )
                    +(
                        self.hyper_params_calib_by_groups[f"model_{group_name}"][
                            "is_pre_holiday"
                        ]
                        * df_prophet["is_pre_holiday"]
                    )
                    +(
                        self.hyper_params_calib_by_groups[f"model_{group_name}"][
                            "is_pre_pre_holiday"
                        ]
                        * df_prophet["is_pre_pre_holiday"]
                    )

                forecast_dict[f"model_{group_name}"] = forecast
            return forecast_dict

        else:
            forecast = np.array(
                self.models_by_groups["model_0"].predict(df_prophet)["yhat"]
            )
            if self.time_column_frequency.value == "D":
                forecast = forecast
                +(
                    self.hyper_params_calib_by_groups["model_0"]["is_weekend"]
                    * df_prophet["is_weekend"]
                )
                +(
                    self.hyper_params_calib_by_groups["model_0"]["is_holiday"]
                    * df_prophet["is_holiday"]
                )
                +(
                    self.hyper_params_calib_by_groups["model_0"]["is_pre_holiday"]
                    * df_prophet["is_pre_holiday"]
                )
                +(
                    self.hyper_params_calib_by_groups["model_0"]["is_pre_pre_holiday"]
                    * df_prophet["is_pre_pre_holiday"]
                )
            return forecast

    def evaluate_and_print(self, **eval_sets):
        """
        Печать в стандартный поток вывода оценки качества модели на eval_sets
        Для задач классификации используется метрика GINI
        Для задачи регрессии метрики MAE, R2, RMSE
        В словаре metrics под ключом названия метрики
        содержится функция её расчёта

        Parameters
        ----------
        eval_sets: Dict[string, Tuple[pandas.DataFrame, pandas.Series]]
            Словарь, где ключ - название выборки, значение - кортеж с
            матрицей признаков и вектором истинных ответов.
        """
        if not self.split_by_group:
            super().evaluate_and_print(**eval_sets)
        else:
            metrics_to_eval = {}
            if self.eval_metric.name.upper() not in metrics_to_eval:
                metrics_to_eval[self.eval_metric.name.upper()] = self.eval_metric
            if self.objective.name.upper() not in metrics_to_eval:
                metrics_to_eval[self.objective.name.upper()] = self.objective

            df = eval_sets["train"][0]
            df["y"] = eval_sets["train"][1]
            eval_sets_tmp = {"train": None, "valid": None}
            for group_name, df_group in df.groupby(self.group_column):
                eval_sets_tmp["train"] = pd.concat(
                    [eval_sets_tmp["train"], df_group[: -self.horizon]], axis=0
                )
                eval_sets_tmp["valid"] = pd.concat(
                    [eval_sets_tmp["valid"], df_group[-self.horizon :]], axis=0
                )

            for sample in eval_sets_tmp:
                data = eval_sets_tmp[sample]
                forecast_dict = self.transform(data)

                scores = {}
                for group_name, df_group in data.groupby(self.group_column):
                    y_true = df_group["y"]
                    y_pred = forecast_dict[f"model_{group_name}"]

                    for name, metric in metrics_to_eval.items():
                        try:
                            scores[name] = metric(y_true, y_pred)
                        except (ValueError, KeyError, IndexError):
                            scores[name] = np.nan

                    metrics_output = ", ".join(
                        [f"{name} = {value:.2f}" for name, value in scores.items()]
                    )
                    output_per_sample = (
                        f"{sample}-score: {group_name}--group: \t {metrics_output}"
                    )

                    logger = CombinedLogger([self._logger, _logger])
                    logger.info(output_per_sample)