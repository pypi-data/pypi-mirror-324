from typing import Optional, Tuple, Dict
import numpy as np
import pandas as pd
import math

from sklearn.metrics import confusion_matrix
from dreamml.reports.kds import report
from sklearn.preprocessing import LabelBinarizer

from dreamml.modeling.metrics.metrics_mapping import metrics_mapping
from dreamml.logging import get_logger
from dreamml.reports.metrics_calculation import BaseMetricsCalculator
from dreamml.modeling.models.estimators import BaseModel
from dreamml.utils.confidence_interval import (
    create_bootstrap_scores,
    calculate_conf_interval,
)

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
    models: Dict[string, estiamtor]
        Словарь с моделями: ключ словаря - название модели,
        значение словаря - экземпляр с моделью.

    config: Dict[string, Any]
         Словарь с конфигурацией эксперимента.

    Attributes:
    -----------
    transformer: CategoricalFeaturesTransformer
        Трансформер категориальных признаков.

    features: pd.Series
        Список всех признаков.

    """

    def __init__(
        self,
        transformer: Optional,
        features: pd.Series,
        config: dict,
        task: str,
        business: bool = False,
    ) -> None:
        self.features = features
        self.transformer = transformer
        self.config = config
        self.task = task
        self.business = business

    def _calculate_samples_stats(self, **eval_sets) -> pd.DataFrame:
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

        Returns:
        --------
        result: pandas.DataFrame
            Датафрейм с рассчитанной статистикой.

        """
        if self.task == "binary":
            result = {}
            for data_name in eval_sets:
                data, target = eval_sets[data_name]

                if self.business:
                    time_column = self.config.get("time_column")
                    if time_column is not None:
                        start_date = data[time_column].min()
                        end_date = data[time_column].max()
                    else:
                        start_date = "NA"
                        end_date = "NA"

                    stats = [
                        start_date,
                        end_date,
                        len(data),
                        len(data) - np.sum(target),
                        np.sum(target),
                        np.mean(target),
                    ]

                    if "All_sample" not in result:
                        result["All_sample"] = ["NA", "NA", 0, 0, 0, 0]
                        if time_column is not None:
                            result["All_sample"][0] = start_date
                            result["All_sample"][1] = end_date

                    if time_column is not None:
                        result["All_sample"][0] = min(
                            start_date, result["All_sample"][0]
                        )
                        result["All_sample"][1] = max(end_date, result["All_sample"][1])
                    result["All_sample"][2] += stats[2]
                    result["All_sample"][3] += stats[3]
                    result["All_sample"][4] += stats[4]
                    result["All_sample"][5] = (
                        result["All_sample"][4] / result["All_sample"][2]
                    )
                else:
                    stats = [len(data), np.sum(target), np.mean(target)]

                result[data_name] = stats

            result = pd.DataFrame(result).T.reset_index()

            if self.business:
                columns = [
                    "Выборка",
                    "Start_date",
                    "End_date",
                    "Наблюдений",
                    '"0"',
                    '"1"',
                    "Event-Rate",
                ]
            else:
                columns = ["Выборка", "# наблюдений", "# events", "# eventrate"]

            result.columns = columns

            if self.business and self.config.get("time_column") is not None:
                result["Start_date"] = result["Start_date"].dt.strftime("%d.%m.%y")
                result["End_date"] = result["End_date"].dt.strftime("%d.%m.%y")

            return result.fillna(0)

        elif self.task in ("multiclass", "multilabel"):
            if self.task == "multiclass":
                labels = self.config["metric_params"]["labels"]
                arange_labels = np.arange(len(labels))
                labels_dict = dict(zip(arange_labels, labels))
                label_binarizer = LabelBinarizer().fit(arange_labels)
                eval_set_cols = labels
            else:
                eval_set_cols = eval_sets["train"][1].columns.tolist()

            columns = ["Выборка", "# наблюдений"]
            columns.extend([f"# events {class_name}" for class_name in eval_set_cols])
            columns.extend(
                [f"# eventrate {class_name}" for class_name in eval_set_cols]
            )

            result = {}
            for data_name in eval_sets:
                data, target = eval_sets[data_name]
                if self.config["task"] == "multiclass":
                    labels_in_sample = arange_labels

                    target = pd.DataFrame(
                        data=label_binarizer.transform(target), columns=labels_in_sample
                    )

                events = np.sum(target).tolist()
                event_rate = np.mean(target).tolist()
                result[data_name] = [len(data)] + events + event_rate

            result = pd.DataFrame(result).T.reset_index()
            assert len(columns) == result.shape[1]
            result.columns = columns
            return result.fillna(0)

        else:
            raise ValueError(
                f'Task must be in ["binary", "multiclass" or "multilabel"] but got {self.task}'
            )

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

        if len(result.columns) == 5:  # В датасете только текстовые фичи
            result.columns = ["index", "count", "unique", "top", "freq"]
        else:
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

        return result.fillna(0)

    def _calculate_variables_types_stats(self) -> pd.DataFrame:
        """
        Расчет статистик по типам переменным. Рассчитывается количество
        категориальных переменных, количество непрерывных переменных
        и название целевой переменной.

        """
        if self.task in ["multiclass", "multilabel"]:
            target_names = (
                [self.config["target_name"]]
                if not isinstance(self.config["target_name"], list)
                else self.config["target_name"]
            )
            stats = pd.DataFrame(
                {"Целевая переменная": [target_name for target_name in target_names]}
            )
            stats["# категорий"] = len(self.transformer.cat_features)
            stats["# непрерывных"] = (
                self.features.shape[0]
                - len(self.transformer.cat_features)
                - len(self.config["drop_features"])
            )
            return stats.fillna(0)

        elif self.config["task"] in ["binary"]:
            stats = pd.DataFrame(
                {
                    "Целевая переменная": [self.config["target_name"]],
                    "# категорий": [len(self.transformer.cat_features)],
                    "# непрерывных": [
                        self.features.shape[0]
                        - len(self.transformer.cat_features)
                        - len(self.config["drop_features"])
                    ],
                }
            )
            return stats.fillna(0)

        else:
            raise ValueError('Task must be in ["binary", "multiclass" or "multilabel"]')

    def transform(
        self, **eval_sets
    ) -> Tuple[Optional[pd.DataFrame], pd.DataFrame, pd.DataFrame]:
        """
        Построение отчета с статистиками о данных.

        Parameters:
        -----------
        eval_sets: Dict[string, Tuple[pandas.DataFrame, pandas.Series]]
            Словарь с выборками, для которых требуется рассчитать статистику.
            Ключ словаря - название выборки (train / valid / ...), значение -
            кортеж с матрицей признаков (data) и вектором ответов (target).

        """
        result = (
            self._calculate_samples_stats(**eval_sets),
            self._calculate_variables_types_stats(),
            self._calculate_variables_stats(**eval_sets),
        )
        return result


class CalculateClassificationMetrics(BaseMetricsCalculator):
    """
    Расчет метрик для задачи бинарной классификации:
    GINI и относительной разницы в метрике качества.

    Parameters
    ----------
    models: dict
        Словарь, ключ - название модели, значение - экземпляр
        ML-модели для DS-Template, из (src.models).

    predictions_: dict
        Словарь с прогнозами модели на выборках из eval_set.

    bootstrap_samples: int
        Количество бутстрап выборок для построения доверительных интервалов.

    p_value: float
        Размер критической зоны для доверительных интервалов (по p_value / 2 с каждой стороны).

    """

    def __init__(
        self,
        models: Dict[str, BaseModel],
        bootstrap_samples: int = 200,
        p_value: float = 0.05,
        config: dict = None,
        metric_name: str = "gini",
        task: str = "binary",
        predictions: Optional[Dict] = None,
        vectorizers: Optional[Dict] = None,
    ) -> None:
        self.metric_name = metric_name
        self.bootstrap_samples = bootstrap_samples
        self.p_value = p_value
        self.metric_params = config.get("metric_params")
        self.task = task
        self.target_with_nan_values = config.get("target_with_nan_values", False)
        self.vectorizers = vectorizers

        super().__init__(models, predictions, vectorizers, calculate_metrics_ratio=True)

    def _get_metrics_to_calculate(self):
        if self.task == "multiclass":
            metric_class = metrics_mapping[self.metric_name](
                task=self.task, labels=self.metric_params["labels"]
            )
        elif self.task == "multilabel":
            metric_class = metrics_mapping[self.metric_name](
                task=self.task, target_with_nan_values=self.target_with_nan_values
            )
        else:
            metric_class = metrics_mapping[self.metric_name](
                task=self.task,
            )
        return {self.metric_name: metric_class}

    def get_best_models(self, stats_df: pd.DataFrame, **eval_sets) -> dict:
        """
        Определение лучших моделей по метрикe Gini на выборках test и OOT.

        Parameters
        ----------
        stats_df: pd.DataFrame
            Таблица с названиями моделей, метриками и количеством признаков.

        Returns
        -------
        best_results: dict
            Словарь с названием и индексом лучшей модели для test и OOT.

        """
        stats_df = stats_df.reset_index(drop=True)

        metric_name = self.metric_name
        metric = metrics_mapping[self.metric_name](task=self.task, **self.metric_params)

        metric_column = metric_name + " test"

        best_score = (
            stats_df[metric_column].max()
            if metric.maximize
            else stats_df[metric_column].min()
        )

        test_best_score_model_name = stats_df[stats_df[metric_column] == best_score][
            "Название модели"
        ].to_list()[0]

        test_scores = create_bootstrap_scores(
            x=eval_sets["test"][0],
            y=eval_sets["test"][1],
            y_pred=self.predictions_[test_best_score_model_name]["test"],
            metric=metric,
            bootstrap_samples=self.bootstrap_samples,
            task=self.task,
            random_seed=27,
        )
        test_conf_interval = calculate_conf_interval(test_scores, alpha=self.p_value)

        min_num_of_features_test = stats_df[
            (stats_df[metric_name + " test"] >= test_conf_interval[0])
            & (stats_df[metric_name + " test"] <= test_conf_interval[1])
        ]["# признаков"].min()
        if not (
            min_num_of_features_test > 0
        ):  # для метрик с группировкой: берем лучшую модель
            min_num_of_features_test = stats_df[
                stats_df["Название модели"] == test_best_score_model_name
            ]["# признаков"].max()
            _logger.info(
                "Лучшая модель на test ("
                + metric_name
                + ") выбрана не по доверительному интервалу (см. отчет), а как модель с лучшей метрикой на test"
            )

        # В случае если, небольшой датасет, то доверительный интервал строится не очень хорошо -->> уменьшаем p_value до 0.01
        if math.isnan(min_num_of_features_test):
            while self.p_value > 0.01 and math.isnan(min_num_of_features_test):
                self.p_value = np.round(self.p_value / 2, 2)
                test_conf_interval = calculate_conf_interval(
                    test_scores, alpha=self.p_value
                )

                min_num_of_features_test = stats_df[
                    (stats_df[metric_name + " test"] >= test_conf_interval[0])
                    & (stats_df[metric_name + " test"] <= test_conf_interval[1])
                ]["# признаков"].min()

        min_df_test = stats_df[stats_df["# признаков"] == min_num_of_features_test]
        if metric_name == "logloss":
            best_model_name_test = min_df_test[
                min_df_test[metric_name + " test"]
                == min_df_test[metric_name + " test"].min()
            ]["Название модели"].to_list()[0]
        else:
            best_model_name_test = min_df_test[
                min_df_test[metric_name + " test"]
                == min_df_test[metric_name + " test"].max()
            ]["Название модели"].to_list()[0]

        best_idx_test = stats_df[
            stats_df["Название модели"] == best_model_name_test
        ].index[0]

        best_results = {
            "test": {
                "name": best_model_name_test,
                "index": best_idx_test,
                "ci": test_conf_interval,
            }
        }
        if "OOT" in eval_sets.keys():
            if metric_name == "logloss":
                oot_best_score_model_name = stats_df[
                    stats_df[metric_name + " OOT"]
                    == stats_df[metric_name + " OOT"].min()
                ]["Название модели"].to_list()[0]
            else:
                oot_best_score_model_name = stats_df[
                    stats_df[metric_name + " OOT"]
                    == stats_df[metric_name + " OOT"].max()
                ]["Название модели"].to_list()[0]

            oot_scores = create_bootstrap_scores(
                x=eval_sets["OOT"][0],
                y=eval_sets["OOT"][1],
                y_pred=self.predictions_[test_best_score_model_name]["OOT"],
                metric=metric,
                bootstrap_samples=self.bootstrap_samples,
                task=self.task,
                random_seed=27,
            )
            oot_conf_interval = calculate_conf_interval(oot_scores, alpha=self.p_value)

            min_num_of_features_oot = stats_df[
                (stats_df[metric_name + " OOT"] >= oot_conf_interval[0])
                & (stats_df[metric_name + " OOT"] <= oot_conf_interval[0])
            ]["# признаков"].min()
            if not (
                min_num_of_features_oot > 0
            ):  # для метрик с группировкой: берем лучшую модель
                min_num_of_features_oot = stats_df[
                    stats_df["Название модели"] == oot_best_score_model_name
                ]["# признаков"].max()
                _logger.info(
                    "Лучшая модель на OOT ("
                    + metric_name
                    + ") выбрана не по доверительному интервалу (см. отчет), а как модель с лучшей метрикой на OOT"
                )
            min_df_oot = stats_df[stats_df["# признаков"] == min_num_of_features_oot]
            if metric_name == "logloss":
                best_model_name_oot = min_df_oot[
                    min_df_oot[metric_name + " OOT"]
                    == min_df_oot[metric_name + " OOT"].min()
                ]["Название модели"].to_list()[0]
            else:
                best_model_name_oot = min_df_oot[
                    min_df_oot[metric_name + " OOT"]
                    == min_df_oot[metric_name + " OOT"].max()
                ]["Название модели"].to_list()[0]

            best_idx_oot = stats_df[
                stats_df["Название модели"] == best_model_name_oot
            ].index[0]
            best_results["oot"] = {
                "name": best_model_name_oot,
                "index": best_idx_oot,
                "ci": oot_conf_interval,
            }
        return best_results


class CalculateDetailedMetrics:
    """
    Расчет детальных метрик для задачи бинарной классификации.

    Рассчитываются метрики по бинам прогнозных значений модели.
    Для каждого бина рассчитывется:
        - минимальная вероятность в бине;
        - средняя вероятность в бине;
        - максимальная вероятность в бине;
        - доля целевого события в бине (evenrate);
        - количество наблюдений в бине;
        - количество целевых событий в бине;
        - количество нецелевых событий в бине;
        - кумулятивное количество целевых событий в бине;
        - кумулятивное количество нецелевых событий в бине;
        - FPR в бине;
        - TPR в бине;
        - GINI на данном выборке;
        - ROC-AUC на данной выборке;
        - стандартная ошибка ROC-AUC;
        - 95% доверительный интервал метрики ROC-AUC.

    Parameters
    ----------
    n_bins: integer, optional, default = 20
        Количество бинов.

    """

    def __init__(
        self,
        n_bins: int = 20,
        metric_name: str = "gini",
        metric_params: dict = None,
        task: str = "binary",
    ):
        self.n_bins = n_bins
        self.metric_name = metric_name
        self.metric_params = metric_params
        self.task = task

    @staticmethod
    def calculate_conf_interval(
        y_true, y_pred, scores: pd.DataFrame, metric_name, metric_params, task: str
    ) -> pd.DataFrame:
        """
        Расчет доверительного интервала и стандартной ошибки ROC AUC.

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
            Датафрейм с рассчитаными метриками по бинам,
            доверительным интервалом ROC AUC и стандартной
            ошибкой ROC AUC.

        """
        num_row = scores.shape[0]
        task_ = "binary" if task == "multilabel" else task

        if task in ["multilabel", "binary"]:
            data = pd.DataFrame({"y_pred": y_pred, "y_true": y_true})
            data = (
                data.dropna(subset=["y_true"])
                if data["y_true"].isna().sum() > 0
                else data
            )
            y_true, y_pred = data["y_true"], data["y_pred"]

        auc = 100 * metrics_mapping.get("roc_auc")(task=task_, **metric_params)(
            y_true, y_pred
        )
        gini = 2 * auc - 100
        metric = 100 * metrics_mapping.get(metric_name)(task=task_, **metric_params)(
            y_true, y_pred
        )

        std_error = 1.96 * np.sqrt(auc * (100 - auc) / y_true.shape[0])
        std_metric = 1.96 * np.sqrt(auc * np.abs(100 - metric) / y_true.shape[0])

        scores.loc[num_row, metric_name] = metric
        scores.loc[num_row, metric_name + " Std Err"] = std_metric
        scores.loc[num_row, metric_name + " 95% LCL"] = metric - std_metric
        scores.loc[num_row, metric_name + " 95% UCL"] = metric + std_metric
        scores.loc[num_row, "GINI"] = gini
        scores.loc[num_row, "AUC"] = auc
        scores.loc[num_row, "AUC Std Err"] = std_error
        scores.loc[num_row, "AUC 95% LCL"] = auc - std_error
        scores.loc[num_row, "AUC 95% UCL"] = auc + std_error

        return np.round(scores, 4)

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
        scores.loc[num_row, "decile"] = "Total"
        scores.loc[num_row, "#obs"] = scores["#obs"].sum()
        scores.loc[num_row, "#event"] = scores["#event"].sum()
        scores.loc[num_row, "#nonevent"] = scores["#nonevent"].sum()
        scores.loc[num_row, "eventrate"] = scores["#event"].sum() / scores["#obs"].sum()
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
        data_gp = data.groupby(["bin"])
        scores = data_gp.agg(
            {"y_pred": ["min", "mean", "max"], "y_true": ["mean", "count", "sum"]}
        )
        scores.columns = [
            "prob_min",
            "prob_mean",
            "prob_max",
            "eventrate",
            "#obs",
            "#event",
        ]
        scores = scores.reset_index()
        scores["bin"] = np.arange(1, scores.shape[0] + 1)
        scores = scores.sort_values(by="bin", ascending=False)

        scores["#nonevent"] = scores["#obs"] - scores["#event"]
        scores["cum # ev"] = scores["#event"].cumsum()
        scores["cum # nonev"] = scores["#nonevent"].cumsum()
        scores = scores.reset_index(drop=True)

        try:
            fpr, tpr = self.roc_auc_metrics(data)
            tpr = np.round(100 * tpr, 4)
            fpr = np.round(100 * fpr, 4)
            scores["1 - Specificty"] = fpr[: len(scores)][::-1]
            scores["Sensitivity"] = tpr[: len(scores)][::-1]
            return scores
        except ValueError:
            return scores

    def roc_auc_metrics(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Расчет метрик FPR, TPR по бинам.

        Parameters
        ----------
        data: pandas.DataFrame, shape = [n_samples, 3]
            Датафрейм с прогнозами модели (y_pred),
            истинными значениями целевой переменной (y_true)
            и рассчитанным бином (bin).

        Returns
        -------
        sensitivity_score, specificity_score: numpy.array
            Метрики FPR, TPR по бинам.

        """
        sensitivity_score = np.zeros(self.n_bins)
        specificity_score = np.zeros(self.n_bins)
        unique_bins = data["bin"].value_counts()
        sorted_bins = unique_bins.sort_index().index

        for num, bin_ in enumerate(sorted_bins):
            mask = data["bin"] == bin_
            threshold = data.loc[mask, "y_pred"].min()
            y_pred_labels = np.where(data["y_pred"] >= threshold, 1, 0)
            tn, fp, fn, tp = confusion_matrix(data.y_true, y_pred_labels).ravel()
            sensitivity_score[num] = tp / (tp + fn)
            specificity_score[num] = fp / (fp + tn)

        return sensitivity_score, specificity_score

    def _transform(self, y_true, y_pred):
        scores = (
            report(y_true, y_pred, n_bins=self.n_bins)
            if self.task != "multiclass"
            else pd.DataFrame()
        )
        scores = self.calculate_conf_interval(
            y_true, y_pred, scores, self.metric_name, self.metric_params, task=self.task
        )
        scores = (
            self.calculate_total_stats(scores) if self.task != "multiclass" else scores
        )
        return scores.fillna(".")

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
        if self.task in ["binary", "multiclass"]:
            return self._transform(y_true, y_pred)

        elif self.task == "multilabel":
            classes = y_true.columns.tolist()
            prediction_columns = [f"{i}_pred" for i in classes]
            y_pred = pd.DataFrame(y_pred, columns=prediction_columns)
            y_true.reset_index(drop=True, inplace=True)
            y_pred.reset_index(drop=True, inplace=True)
            dataset = pd.concat([y_true, y_pred], axis=1, ignore_index=False)
            scores = []
            for idx in range(len(classes)):
                _y_true = dataset[classes[idx]].values
                _y_pred = dataset[prediction_columns[idx]].values
                scores.append((classes[idx], self._transform(_y_true, _y_pred)))
            return scores

        else:
            raise ValueError(
                'Supports only "multilabel", "multiclass" and "binary" tasks.'
            )