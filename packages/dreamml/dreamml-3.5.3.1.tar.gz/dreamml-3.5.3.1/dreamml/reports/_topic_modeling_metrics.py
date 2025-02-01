from typing import Optional, Tuple
import numpy as np
import pandas as pd
import math

from sklearn.metrics import average_precision_score
from scipy import stats

from dreamml.modeling.metrics.metrics_mapping import metrics_mapping
from dreamml.logging import get_logger
from dreamml.utils.vectorization_eval_set import get_eval_set_with_embeddings

_logger = get_logger(__name__)


class CalculateTopicModelingMetrics:

    def __init__(
        self,
        models: dict,
        bootstrap_samples: int = 200,
        p_value: float = 0.05,
        config: dict = None,
        metric_name: str = "gini",
        metric_col_name: str = "gini",
        task: str = "binary",
        vectorizers: Optional[dict] = None,
    ) -> None:
        self.models = models
        self.predictions_ = {}
        self.bootstrap_samples = bootstrap_samples
        self.p_value = p_value
        self.metric_name = metric_name
        self.metric_col_name = metric_col_name
        self.metric_params = config.get("metric_params")
        self.task = task
        self.vectorizers = vectorizers

    @staticmethod
    def create_prediction(model, data) -> np.array:
        try:
            pred = model.transform(data)
        except TypeError:
            pred = np.zeros(data.shape[0])

        return pred

    def gini_to_frame(self, scores: dict, **eval_sets) -> pd.DataFrame:
        scores = pd.DataFrame(scores)
        scores = scores.T.reset_index()

        metrics = [self.metric_name]
        scores_name = ["Название модели", "# признаков"]
        scores_name += [
            f"{metric} {sample}" for metric in metrics for sample in eval_sets
        ]
        scores.columns = scores_name
        scores = self.calculate_metrics_ratio_gini(
            self.metric_name, self.metric_col_name, scores
        )
        scores["детали о модели"] = [
            f"Ссылка на лист train {model}" for model in scores["Название модели"]
        ]
        return scores

    def pr_auc_to_frame(self, scores: dict, **eval_sets) -> pd.DataFrame:
        """
        Преобразование словаря scores в pandas.DataFrame и
        применение название столбцов (имя метрики + имя выборки).

        Parameters
        ----------
        scores: Dict[string, List[float]]
            Словарь, ключ - название модели, значение - список
            со значениями метрик бинарной классификации.

        eval_sets: Dict[string, Tuple[pd.DataFrame, pd.Series]]
            Словарь, ключ - название выборки, значение - кортеж
            с матрией признаков и вектором истинных ответов.

        Returns
        -------
        scores: pandas.DataFrame
            Значения метрик.

        """
        scores = pd.DataFrame(scores)
        scores = scores.T.reset_index()

        metrics = ["pr_auc"]
        scores_name = ["Название модели", "# признаков"]
        scores_name += [
            f"{metric} {sample}" for metric in metrics for sample in eval_sets
        ]

        scores.columns = scores_name
        scores = self.calculate_metrics_ratio_pr_auc(scores)
        scores["детали о модели"] = [
            f"Ссылка на лист train {model}" for model in scores["Название модели"]
        ]
        return scores

    @staticmethod
    def calculate_metrics_ratio_gini(
        metric_name: str, metric_col_name: str, data: pd.DataFrame
    ):
        """
        Вычисление абсолютной и относительной разницы в значении
        метрики GINI между выборками train versus test и
        train versus OOT.

        Parameters
        ----------
        data: pandas.core.frame.DataFrame
            Датафрейм с рассчитанными метриками для всех
            построенных моделей на всех выборках.

        Returns
        -------
        data: pandas.core.frame.DataFrame
            Датафрейм с рассчитанной относительной и
            абсолютной разницей в метрике качества.

        """
        columns = data.columns
        if (
            metric_col_name + " train" in columns
            and metric_col_name + " test" in columns
        ):
            data[metric_col_name + " delta train vs test"] = np.abs(
                data[metric_col_name + " train"] - data[metric_col_name + " test"]
            )
            data[metric_col_name + " delta train vs test, %"] = (
                100
                * data[metric_col_name + " delta train vs test"]
                / data[metric_col_name + " train"]
            )

        if (
            metric_col_name + " train" in columns
            and metric_col_name + " OOT" in columns
        ):
            data[metric_col_name + " delta train vs OOT"] = np.abs(
                data[metric_col_name + " train"] - data[metric_col_name + " OOT"]
            )
            data[metric_col_name + " delta train vs OOT, %"] = (
                100
                * data[metric_col_name + " delta train vs OOT"]
                / data[metric_col_name + " train"]
            )

        data = data.fillna(0)
        data = data.replace(np.nan, 0)
        return data

    @staticmethod
    def calculate_metrics_ratio_pr_auc(data: pd.DataFrame):
        """
        Вычисление абсолютной и относительной разницы в значении
        метрики PR-AUC между выборками train versus test и
        train versus OOT.

        Parameters
        ----------
        data: pandas.core.frame.DataFrame
            Датафрейм с рассчитанными метриками для всех
            построенных моделей на всех выборках.

        Returns
        -------
        data: pandas.core.frame.DataFrame
            Датафрейм с рассчитанной относительной и
            абсолютной разницей в метрике качества.

        """
        columns = data.columns
        if "pr_auc train" in columns and "pr_auc test" in columns:
            data["pr_auc delta train vs test"] = np.abs(
                data["pr_auc train"] - data["pr_auc test"]
            )
            data["pr_auc delta train vs test, %"] = (
                100 * data["pr_auc delta train vs test"] / data["pr_auc train"]
            )

        if "pr_auc train" in columns and "pr_auc OOT" in columns:
            data["pr_auc delta train vs OOT"] = np.abs(
                data["pr_auc train"] - data["pr_auc OOT"]
            )
            data["pr_auc delta train vs OOT, %"] = (
                100 * data["pr_auc delta train vs OOT"] / data["pr_auc train"]
            )

        data = data.fillna(0)
        data = data.replace(np.nan, 0)
        return data

    def create_all_predictions(self, **eval_sets):
        for model_name, model in self.models.items():
            eval_set = eval_sets.copy()

            # FIXME add for bartopic

            if "bertopic" not in model_name:
                vectorizer_name = f"{model.vectorization_name}_vectorizer"
                vectorizer = self.vectorizers[vectorizer_name]
                eval_set = get_eval_set_with_embeddings(vectorizer, eval_set)

            self.predictions_[model_name] = {}
            sample_pred = {}

            for sample_name, (X_sample, _) in eval_set.items():
                pred = self.create_prediction(model, X_sample)
                sample_pred[sample_name] = pred

            self.predictions_[model_name] = sample_pred

    def calculate_gini(self, model_name, **kwargs):
        try:
            model = self.models[model_name]
            metrics_score = [len(model.used_features)]
        except TypeError:
            sample_name = next(iter(kwargs))
            metrics_score = [len(kwargs[sample_name][0])]

        for sample in kwargs:
            _, target = kwargs[sample]
            pred = self.predictions_[model_name]
            try:
                metrics_score.append(
                    round(
                        metrics_mapping[self.metric_name](
                            task=self.task, **self.metric_params
                        )(model.topic_modeling_data),
                        4,
                    )
                )
            except ValueError:
                metrics_score.append(0.00001)

        return metrics_score

    def calculate_pr_auc(self, model_name, **kwargs):
        """
        Вычисление метрики PR-AUC.

        Parameters
        ----------
        model_name: string
            Название модели из self.models.

        kwargs: dict
            Словарь, ключ - название выборки, значение - кортеж
            с матрицой признаков для применения модели и вектором
            истинных ответов.

        Returns
        -------
        metrics_score: list
            Список со значением метрик.

        """
        try:
            model = self.models[model_name]
            metrics_score = [len(model.used_features)]
        except TypeError:
            sample_name = next(iter(kwargs))
            metrics_score = [len(kwargs[sample_name][0])]

        for sample in kwargs:
            _, target = kwargs[sample]
            pred = self.predictions_[model_name]
            y_pred = pred[sample]

            try:
                if self.task in ["multilabel", "multiclass"]:
                    zeros_classes = [
                        col for col in target.columns if target[col].sum() == 0
                    ]
                    y_pred = np.delete(
                        pred[sample],
                        [target.columns.get_loc(col) for col in zeros_classes],
                        axis=1,
                    )
                    target = target.drop(columns=zeros_classes)
                metrics_score.append(
                    round(100 * average_precision_score(target, y_pred), 4)
                )
            except ValueError:
                metrics_score.append(0.00001)

        return metrics_score

    def _create_bootstrap_index(self, X: pd.DataFrame) -> np.array:
        """
        Создание матрицы индексов объектов, попавших в
        бутстреп-выборку.

        Parameters
        ----------
        X: pandas.core.frame.DataFrame
            Матрица признаков для создания бутстреп-объектов.

        Returns
        -------
        bootstrap_index: np.array
            Матрица индексов бутстреп объектов.

        """
        np.random.seed(27)
        bootstrap_index = np.random.randint(
            0, X.shape[0], size=(self.bootstrap_samples, X.shape[0])
        )
        return bootstrap_index

    def _create_bootstrap_scores(
        self, X: pd.DataFrame, y: pd.Series, y_pred: pd.Series
    ) -> np.array:
        """
        Вычисление метрики качества на каждой бутстреп выборке.

        Parameters
        ----------
        X: pandas.core.frame.DataFrame
            Матрица признаков для создания бутстреп-объектов.

        y: pandas.core.frame.Series
            Вектор целевой переменной.

        y_pred: pandas.core.frame.Series
            Вектор предсказаний модели.

        Returns
        -------
        bootstrap_scores: np.array
            Вектор с бутстрап оценками.

        """
        counter = 0
        while True:
            try:
                bootstrap_scores = []
                bootstrap_index = self._create_bootstrap_index(X)
                if isinstance(y, pd.Series):
                    y = y.reset_index(drop=True)
                for sample_idx in bootstrap_index:
                    y_true_bootstrap, y_pred_bootstrap = (
                        y.iloc[sample_idx],
                        y_pred[sample_idx],
                    )
                    bootstrap_scores.append(
                        metrics_mapping.get(self.metric_name)(
                            task=self.task, **self.metric_params
                        )(y_true_bootstrap, y_pred_bootstrap)
                        * 100
                    )
            except Exception as e:
                counter += 1
                continue

            finally:
                break

        return np.array(bootstrap_scores)

    @staticmethod
    def _calculate_conf_interval(x: np.array, alpha: float = 0.05):
        """
        Вычисление доверительного интервала для среднего.

        Parameters
        ----------
        x: array-like, shape = [n_samples, ]
            Выборка для построения доверительного интервала.

        alpha: float, optional, default = 0.05
            Уровень доверия.

        Returns
        -------
        conf_interval: Tuple[float, float]
            Границы доверительного интервала.

        """
        x_mean = np.mean(x)
        q_value = stats.t.ppf(1 - alpha / 2, x.shape[0])

        std_error = q_value * np.sqrt(x_mean) / np.sqrt(x.shape[0])
        return x_mean - std_error, x_mean + std_error

    def get_best_models(self, stats_df: pd.DataFrame, **eval_sets) -> dict:
        metric_name = self.metric_name
        metric_col_name = self.metric_col_name
        stats_df = stats_df.reset_index(drop=True)
        if metric_name == "logloss":
            best_gini_model_name_test = stats_df[
                stats_df[metric_name + " test"] == stats_df[metric_name + " test"].min()
            ]["Название модели"].to_list()[0]

        else:
            best_gini_model_name_test = stats_df[
                stats_df[metric_name + " test"] == stats_df[metric_name + " test"].max()
            ]["Название модели"].to_list()[0]

        test_scores = self._create_bootstrap_scores(
            X=eval_sets["test"][0],
            y=eval_sets["test"][1],
            y_pred=self.predictions_[best_gini_model_name_test]["test"],
        )
        test_conf_interval = self._calculate_conf_interval(
            test_scores, alpha=self.p_value
        )
        min_num_of_features_test = stats_df[
            (stats_df[metric_name + " test"] >= test_conf_interval[0])
            & (stats_df[metric_name + " test"] <= test_conf_interval[1])
        ]["# признаков"].min()
        if not (
            min_num_of_features_test > 0
        ):  # для метрик с группировкой: берем лучшую модель
            min_num_of_features_test = stats_df[
                stats_df["Название модели"] == best_gini_model_name_test
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
                test_conf_interval = self._calculate_conf_interval(
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
                best_gini_model_name_oot = stats_df[
                    stats_df[metric_name + " OOT"]
                    == stats_df[metric_name + " OOT"].min()
                ]["Название модели"].to_list()[0]
            else:
                best_gini_model_name_oot = stats_df[
                    stats_df[metric_name + " OOT"]
                    == stats_df[metric_name + " OOT"].max()
                ]["Название модели"].to_list()[0]

            oot_scores = self._create_bootstrap_scores(
                X=eval_sets["OOT"][0],
                y=eval_sets["OOT"][1],
                y_pred=self.predictions_[best_gini_model_name_oot]["OOT"],
            )

            oot_conf_interval = self._calculate_conf_interval(
                oot_scores, alpha=self.p_value
            )
            min_num_of_features_oot = stats_df[
                (stats_df[metric_name + " OOT"] >= oot_conf_interval[0])
                & (stats_df[metric_name + " OOT"] <= oot_conf_interval[0])
            ]["# признаков"].min()
            if not (
                min_num_of_features_oot > 0
            ):  # для метрик с группировкой: берем лучшую модель
                min_num_of_features_oot = stats_df[
                    stats_df["Название модели"] == best_gini_model_name_oot
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

    def transform(self, **eval_sets):
        scores = {}
        if not self.predictions_:
            self.create_all_predictions(**eval_sets)
        else:
            _logger.info("Used Pre-calculated predictions")

        for model in self.models:
            scores[model] = self.calculate_gini(model, **eval_sets)

        return self.gini_to_frame(scores, **eval_sets)

    def transform_pr(self, **eval_sets):
        """
        Расчет метрик бинарной классификации для
        каждой модели из self.models и каждой выборки из
        eval_sets.

        Parameters
        ----------
        eval_sets: Dict[string, Tuple[pd.DataFrame, pd.Series]]
            Словарь, ключ - название выборки, значение - кортеж
            с матрией признаков и вектором истинных ответов.

        Returns
        -------
        scores: pandas.DataFrame
            Значения метрик.

        """
        scores = {}
        if not self.predictions_:
            self.create_all_predictions(**eval_sets)
        else:
            _logger.info("Used Pre-calculated predictions")

        for model in self.models:
            scores[model] = self.calculate_pr_auc(model, **eval_sets)

        return self.pr_auc_to_frame(scores, **eval_sets)