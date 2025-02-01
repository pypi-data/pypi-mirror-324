from typing import Dict, Optional

import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr
from sklearn.metrics import mean_absolute_error, r2_score

from dreamml.logging import get_logger
from dreamml.modeling.metrics.metrics_mapping import metrics_mapping
from dreamml.modeling.metrics.utils import calculate_quantile_bins
from dreamml.modeling.models.estimators import BoostingBaseModel, BaseModel
from dreamml.reports.metrics_calculation import BaseMetricsCalculator


_logger = get_logger(__name__)


class CalculateDataStatistics:
    """
    Расчет статистик по данным. Содержит:

        - статистику по каждой выборке train / valid / ... :
          количество наблюдений в каждой выборке, количество
          целевыйх событий, доля целевого события.

        - статиску по переменным: название целевой переменной,
          количество категориальных признаков, количество непрерывных
          признаков.

        - статистику по переменным: название переменной, количество
          заполненных значений, минимальное значение, среднее значение,
          максимальное значение, перцентили 25, 50, 75.

    Parameters:
    -----------
    encoder: dspl.feature_extraction.transformers
        Трансформер для преобразования категориальных признаков.

    log_transformer: dspl.feature_extraction.transformers
        Трансформер для преобразования целевой переменной.

    corr_importance: pd.DataFrame
        Датафрейм с однофакторным анализом переменных.

    config: Dict[string, Any]
         Словарь с конфигурацией эксперимента.

    Attributes:
    -----------
    transformer: CategoricalFeaturesTransformer
        Трансформер категориальных признаков.

    gini: pandas.DataFrame
        Датафрейм с анализом переменных по метрике Джини.

    """

    def __init__(self, encoder, log_transformer, corr_importance, config: dict) -> None:
        self.gini = corr_importance
        self.transformer = encoder
        self.log_transformer = log_transformer
        self.categorical = self.transformer.cat_features
        self.config = config

    def _preprocessing_data(self, **eval_sets):
        """
        Данные об удалении выбросов по целевой переменной
        """

        msg = "Удалены выбросы по целевой переменной" "({} и {} перцентили).".format(
            self.config["min_percentile"], self.config["max_percentile"]
        )
        values = [
            msg if sample in ["train", "valid", "test2"] else "-"
            for sample in eval_sets
        ]
        return values

    def _calculate_samples_stats(self, log_scale: bool, prefix: str = "", **eval_sets):
        """
        Расчет статистики по выборке data и вектора target.
        Расчитывается количество наблюдений, количество целевых событий
        и доля целевого события.

        Parameters:
        -----------
        eval_sets: Dict[string, Tuple[pandas.DataFrame, pandas.Series]]
            Словарь с выборками, для которых требуется рассчитать статистику.
            Ключ словаря - название выборки (train / valid / ...), значение -
            кортеж с матрицей признаков (data) и вектором ответов (target).

        log_scale: bool
            target в логарифмированном виде или нет. Флаг, принимающий
            значения True, False. Если log_scale = True, то таргет в
            логарифмированно виде и требуется применить inverse_transform.

        prefix: str, optional, default = ""
            Префикс для Data-Statistics.

        Returns:
        --------
        result: pandas.DataFrame
            Датафрейм с рассчитанной статистикой.

        """
        result = {}
        for data_name in eval_sets:
            data, target = eval_sets[data_name]

            if log_scale:
                target = self.log_transformer.inverse_transform(target)

            result[data_name] = [
                len(data),
                np.mean(target),
                np.std(target),
                np.min(target),
                np.percentile(target, 25),
                np.percentile(target, 50),
                np.percentile(target, 75),
                np.max(target),
                "-",
            ]
        result = pd.DataFrame(result).T.reset_index()
        result.columns = [
            "Выборка",
            "# наблюдений",
            f"{prefix}target AVG-value",
            f"{prefix}target STD-value",
            f"{prefix}target MIN-value",
            f"{prefix}target 25% percentile",
            f"{prefix}target 50% percentile",
            f"{prefix}target 75% percentile",
            f"{prefix}target MAX-value",
            "Предобработка",
        ]
        result["Предобработка"] = self._preprocessing_data(**eval_sets)
        return result.fillna(0)

    def _calculate_variables_stats(self, **eval_sets) -> pd.DataFrame:
        """
        Расчет статистик по переменным. Рассчитывается количество
        заполненных значений признака, среднее значение признака,
        стандартное отклонение признака, минимальное значение
        признака, 25-ый перцентиль признака, медиана признака,
        75-ый перцентиль признака, максимальное значение признака.

        Parameters:
        -----------
        eval_sets: Dict[string, Tuple[pandas.DataFrame, pandas.Series]]
            Словарь с выборками, для которых требуется рассчитать статистику.
            Ключ словаря - название выборки (train / valid / ...), значение -
            кортеж с матрицей признаков (data) и вектором ответов (target).

        Returns:
        --------
        result: pandas.DataFrame
            Датафрейм с рассчитанной статистикой.


        """
        sample_name = next(iter(eval_sets))
        data, _ = eval_sets[sample_name]

        result = data.describe().T.reset_index()
        result.columns = [
            "Variable name",
            "Number of filled value",
            "AVG-value",
            "STD-value",
            "MIN-value",
            "25% percentile-value",
            "50% percentile-value",
            "75% percentile-value",
            "MAX-value",
        ]
        if self.categorical:
            mask = result["Variable name"].isin(self.categorical)
            features = [
                "AVG-value",
                "STD-value",
                "MIN-value",
                "25% percentile-value",
                "50% percentile-value",
                "75% percentile-value",
                "MAX-value",
            ]
            result.loc[mask, features] = "."

        return result.fillna(0)

    def _calculate_variables_types_stats(self) -> pd.DataFrame:
        """
        Расчет статистик по типам переменным. Рассчитывается количество
        категориальных переменных, количество непрерывных переменных
        и название целевой переменной.

        """
        target_name = self.config["target_name"]
        log_target = self.config.get("log_target", False)
        target_name = f"log({target_name})" if log_target else target_name

        stats = pd.DataFrame(
            {
                "Целевая переменная": [self.config["target_name"]],
                "loss_function": self.config["loss_function"],
                "eval_metric": self.config["eval_metric"],
                "# категорий": [len(self.transformer.cat_features)],
            }
        )
        if self.gini is not None:
            stats["# непрерывных"] = [self.gini.shape[0]]

        return stats.fillna(0)

    def transform(self, **eval_sets) -> None:
        """
        Построение отчета с статистиками о данных.

        Parameters:
        -----------
        eval_sets: Dict[string, Tuple[pandas.DataFrame, pandas.Series]]
            Словарь с выборками, для которых требуется рассчитать статистику.
            Ключ словаря - название выборки (train / valid / ...), значение -
            кортеж с матрицей признаков (data) и вектором ответов (target).

        """
        if self.log_transformer.fitted:
            res = (
                self._calculate_samples_stats(log_scale=True, prefix="", **eval_sets),
                self._calculate_samples_stats(
                    log_scale=False, prefix="log-", **eval_sets
                ),
            )
            result = (
                *res,
                self._calculate_variables_types_stats(),
                self._calculate_variables_stats(**eval_sets),
            )
        else:
            result = (
                self._calculate_samples_stats(log_scale=False, **eval_sets),
                self._calculate_variables_types_stats(),
                self._calculate_variables_stats(**eval_sets),
            )
        return result


class CalculateRegressionMetrics(BaseMetricsCalculator):
    """
    Расчет метрик для задачи регрессии:
    MAE, RMSE, R2

    Parameters
    ----------
    log_transformer: dspl.feature_extraction.transformers
        Трансформер для преобразования целевой переменной.

    models: Dict[str, BaseModel])
        Словарь, ключ - название модели, значение - экземпляр
        ML-модели для DS-Template, из (src.models).

    """

    def __init__(
        self,
        models: Dict[str, BaseModel],
        log_transformer: Optional = None,
        predictions: Optional[Dict] = None,
        vectorizers: Optional[Dict] = None,
    ) -> None:
        self.log_transformer = log_transformer

        def transform_target(target):
            if self.log_transformer is not None and self.log_transformer.fitted:
                target = self.log_transformer.inverse_transform(target)

            return target

        super().__init__(
            models,
            predictions,
            vectorizers,
            calculate_metrics_ratio=False,
            transform_target=transform_target,
        )

    def _get_metrics_to_calculate(self):
        first_model = None
        for first_model in self.models.values():
            if isinstance(first_model, BoostingBaseModel):
                break
        if first_model is None:
            raise RuntimeError(
                "No instances of `BoostingBaseModel` found in `prepared_model_dict`"
            )

        metrics = {
            first_model.objective.name: first_model.objective,
            first_model.eval_metric.name: first_model.eval_metric,
        }

        # additional metrics
        for name in ["mae", "rmse", "mape", "r2"]:
            if name not in metrics:
                metrics[name] = metrics_mapping[name]()

        metrics["pearsonr"] = lambda x, y: pearsonr(x, y)[0]
        metrics["spearmanr"] = lambda x, y: spearmanr(x, y)[0]

        return metrics

    def create_prediction(self, model: BaseModel, data: pd.DataFrame) -> np.array:
        pred = super().create_prediction(model, data)

        if self.log_transformer.fitted:
            pred = self.log_transformer.inverse_transform(pred)

        return pred


class CalculateDetailedMetrics:
    """
    Расчет детальных метрик для задачи регрессии.

    Рассчитываются метрики по бинам прогнозных значений модели.
    Для каждого бина рассчитывется:
        - минимальная прогноз в бине;
        - средний прогноз в бине;
        - максимальный прогноз в бине;
        - минимальное значение таргета в бине;
        - среднее значение таргета в бине;
        - максимальное значение таргета в бине;
        - количество наблюдений в бине;
        - R2 в бине;
        - MAE в бине;
        - RMSE в бине;

    Parameters
    ----------
    log_transformer: dspl.feature_extraction.transformers
        Трансформер для преобразования целевой переменной.

    n_bins: integer, optional, default = 20
        Количество бинов.

    """

    def __init__(self, log_transformer, n_bins: int = 20):
        self.log_transformer = log_transformer
        self.n_bins = n_bins

    @staticmethod
    def calculate_total_metrics(
        data: pd.DataFrame, scores: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Расчет метрик по всему набору данных: MAE, MAPE, RMSE, R2,
        корреляция Пирсона, корреляция Спирмена.

        Parameters
        ----------
        data: pandas.DataFrame, shape = [n_samples, 3]
            Датафрейм с прогнозами модели (y_pred),
            истинными значениями целевой переменной (y_true)
            и рассчитанным бином (bin).

        scores: pandas.DataFrame, shape = [self.n_bins, ]
            Датафрейм с расчетом базовым метрик по бинам.

        Returns
        -------
        scores: pandas.DataFrame

        """
        num_row = scores.shape[0]

        scores.loc[num_row, "MAE"] = mean_absolute_error(data["y_true"], data["y_pred"])
        scores.loc[num_row, "MAPE"] = metrics_mapping["mape"]()(
            data["y_true"], data["y_pred"]
        )
        scores.loc[num_row, "RMSE"] = metrics_mapping["rmse"]()(
            data["y_true"], data["y_pred"]
        )
        scores.loc[num_row, "R2"] = 100 * r2_score(data["y_true"], data["y_pred"])
        scores.loc[num_row, "pearson-correlation"] = (
            100 * pearsonr(data["y_true"], data["y_pred"])[0]
        )
        scores.loc[num_row, "spearman-correlation"] = (
            100 * spearmanr(data["y_true"], data["y_pred"])[0]
        )
        scores.loc[num_row, "real 25p"] = np.percentile(data["y_true"], 25)
        scores.loc[num_row, "real 50p"] = np.percentile(data["y_true"], 50)
        scores.loc[num_row, "real 75p"] = np.percentile(data["y_true"], 75)

        return np.round(scores, 4)

    @staticmethod
    def bin_generator(data: pd.DataFrame) -> pd.Series:
        """
        Генератор, который возвращает маску объектов,
        относящихся к данному бину.

        Parameters
        ----------
        data: pandas.DataFrame, shape = [n_samples, 3]
            Датафрейм с прогнозами модели (y_pred),
            истинными значениями целевой переменной (y_true)
            и рассчитанным бином (bin).

        Returns
        -------
        mask: pandas.Series
            Маска объектов, относящихся к данному бину.

        """
        unique_bins = data["bin"].value_counts(ascending=True)
        sorted_bins = unique_bins.sort_index().index

        for bin_ in sorted_bins:
            mask = data["bin"] == bin_
            yield mask

    @staticmethod
    def calculate_total_stats(scores: pd.DataFrame) -> pd.DataFrame:
        """
        Расчет базовых метрик по всему набору данных.
        Базовые метрики: общее число наблюдений в выборке, количество
        целевых событий, количество нецелевых событий, доля целевого
        события в выборке.

        Parameters
        ----------
        scores: pandas.DataFrame
            Датафрейм с расчитанными базовыми метрик по бинам.

        Returns
        -------
        scores: pandas.DataFrame
            Датафрейс с расчитанными базовыми метриками по бинам
            и базовыми метрики по всему набору данных.

        """
        num_row = scores.shape[0] - 1
        scores = scores.reset_index(drop=True)

        scores.loc[num_row, "bin"] = "Total"
        scores.loc[num_row, "#obs"] = scores["#obs"].sum()
        scores.loc[num_row, "pred_mean"] = (scores["pred_mean"] * scores["#obs"]).sum()
        scores.loc[num_row, "pred_mean"] /= scores.loc[num_row, "#obs"]

        scores.loc[num_row, "real_mean"] = (scores["real_mean"] * scores["#obs"]).sum()
        scores.loc[num_row, "real_mean"] /= scores.loc[num_row, "#obs"]

        return scores

    def calculate_base_bins_metrics(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Расчет метрик по бинам.

        Parameters
        ----------
        data: pandas.DataFrame, shape = [n_samples, 3]
            Датафрейм с прогнозами модели (y_pred),
            истинными значениями целевой переменной (y_true)
            и рассчитанным бином (bin).

        Returns
        -------
        scores: pandas.DataFrame, shape = [self.n_bins, ]
            Датафрейм с метриками по бинам.

        """
        # ToDo
        # Коэффициент корреляции (Пирсона и Спирмена) в бинах
        # MAE, RMSE, R2 в бинах
        # доля истинных ответов, которая попала в бин прогнозов

        data_gp = data.groupby(["bin"])
        scores = data_gp.agg(
            {
                "y_pred": ["min", "mean", "max"],
                "y_true": ["min", "mean", "max", "count"],
            }
        )
        scores["real 25p"] = data_gp["y_true"].apply(lambda x: np.percentile(a=x, q=25))
        scores["real 50p"] = data_gp["y_true"].apply(lambda x: np.percentile(a=x, q=50))
        scores["real 75p"] = data_gp["y_true"].apply(lambda x: np.percentile(a=x, q=75))

        scores.columns = [
            "pred_min",
            "pred_mean",
            "pred_max",
            "real_min",
            "real_mean",
            "real_max",
            "#obs",
            "real 25p",
            "real 50p",
            "real 75p",
        ]

        scores = scores.reset_index()
        scores["bin"] = np.arange(1, scores.shape[0] + 1)
        scores = scores.sort_values(by="bin", ascending=True)
        rounded = np.where(scores <= 100, np.round(scores, 2), np.round(scores, 0))
        scores = pd.DataFrame(rounded, columns=scores.columns)

        return scores

    def calculate_regression_metrics_in_bins(
        self, data: pd.DataFrame, scores: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Расчет метрик MAE, R2, RMSE, корреляции Пирсона,
        корреляции Спирмена, 95% доверительный интервал для
        истинного значения целевой переменной, по бинам.

        Parameters
        ----------
        data: pandas.DataFrame, shape = [n_samples, 3]
            Датафрейм с прогнозами модели (y_pred),
            истинными значениями целевой переменной (y_true)
            и рассчитанным бином (bin).

        scores: pandas.DataFrame
            Датафрейм с расчитанными базовыми метрик по бинам.

        Returns
        -------
        sensitivity_score, specificity_score: numpy.array
            Метрики FPR, TPR по бинам.

        """
        gen = self.bin_generator(data)
        for num, mask in enumerate(gen):
            y_true = data.loc[mask, "y_true"]
            y_pred = data.loc[mask, "y_pred"]

            scores.loc[num, "MAE"] = mean_absolute_error(y_true, y_pred)
            scores.loc[num, "MAPE"] = metrics_mapping["mape"]()(y_true, y_pred)

            scores.loc[num, "RMSE"] = metrics_mapping["rmse"]()(y_true, y_pred)
            scores.loc[num, "R2"] = 100 * r2_score(y_true, y_pred)
            try:
                scores.loc[num, "pearson-correlation"] = (
                    100 * pearsonr(y_true, y_pred)[0]
                )
                scores.loc[num, "spearman-correlation"] = (
                    100 * spearmanr(y_true, y_pred)[0]
                )
            except ValueError:
                scores.loc[num, "pearson-correlation"] = 100
                scores.loc[num, "spearman-correlation"] = 100

        return scores

    def transform(self, y_true, y_pred):
        """
        Расчет метрик для каждого бина.

        Parameters
        ----------
        y_true: array-like, shape = [n_samples, ]
            Вектор истинных ответов.

        y_pred: array-like, shape = [n_samples, ]
            Вектор прогнозов.

        Returns
        -------
        scores: pandas.DataFrame, shape = [self.n_bins, 17]
            Датафрейм с рассчитаными по бинам метриками.

        """

        data = pd.DataFrame({"y_pred": y_pred, "y_true": y_true})
        data["bin"] = calculate_quantile_bins(
            data["y_pred"], self.n_bins, ascending=True
        )
        data["bin"] = data["bin"].fillna(-1)

        scores = self.calculate_base_bins_metrics(data)
        scores = self.calculate_regression_metrics_in_bins(data, scores)
        scores = self.calculate_total_metrics(data, scores)
        scores = self.calculate_total_stats(scores)
        return scores.fillna(".")