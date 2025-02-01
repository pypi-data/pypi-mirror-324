import numpy as np
from typing import Optional, Dict
from scipy.stats import pearsonr, spearmanr

from dreamml.logging import get_logger
from dreamml.modeling.metrics.metrics_mapping import metrics_mapping
from dreamml.modeling.models.estimators import BoostingBaseModel
from dreamml.modeling.models.estimators import BaseModel
from dreamml.reports.metrics_calculation import BaseMetricsCalculator

_logger = get_logger(__name__)


class CalculateAMTSMetrics(BaseMetricsCalculator):

    def __init__(
        self,
        models: Dict[str, BaseModel],
        group_column,
        split_by_group,
        predictions: Optional[Dict] = None,
        vectorizers: Optional[Dict] = None,
    ) -> None:
        super().__init__(models, predictions=predictions, vectorizers=vectorizers)
        self.models = models
        self.predictions_ = {}
        self.metrics = self._get_metrics_to_calculate()
        self.group_column = group_column
        self.split_by_group = split_by_group

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

        for name in ["mae", "rmse", "mape", "r2"]:
            if name not in metrics:
                metrics[name] = metrics_mapping[name]()

        metrics["pearsonr"] = pearsonr
        metrics["spearmanr"] = spearmanr

        return metrics

    def create_all_predictions(self, **eval_set):
        """
        Применение всех моделей из self.models к наборам данных
        из eval_set
        """
        for model in self.models:

            if model == "LinearReg":
                sample_pred = {}
                for sample in eval_set:
                    data, _ = eval_set[sample]
                    data = data.sort_index()
                    pred = self.create_prediction(self.models[model], data)
                    sample_pred[sample] = pred
                self.predictions_[f"{model}_model_0"] = sample_pred

            else:
                for model_group in self.models[model].models_by_groups:

                    sample_pred = {}

                    for sample in eval_set:
                        data, _ = eval_set[sample]
                        data = data.sort_index()
                        pred = self.create_prediction(self.models[model], data)

                        if self.split_by_group:
                            sample_pred[sample] = pred[model_group]
                        else:
                            sample_pred[sample] = pred

                    self.predictions_[f"{model}_{model_group}"] = sample_pred

    def calculate_metrics(self, model_name, model_group, **kwargs):
        """
        Вычисление метрик.

        Parameters
        ----------
        model_name: string
            Название модели из self.models.

        eval_sets: dict
            Словарь, ключ - название выборки, значение - кортеж
            с матрицой признаков для применения модели и вектором
            истинных ответов.

        Returns
        -------
        metrics_score: list
            Список со значением метрик.

        """
        try:
            metrics_score = [model_name]
        except TypeError:
            metrics_score = [model_name]

        for metric_name, metric in self.metrics.items():
            for sample in kwargs:
                df, target = kwargs[sample]

                if self.split_by_group:
                    df["y"] = target
                    for group_name, df_group in df.groupby(self.group_column):
                        if f"model_{group_name}" == model_group:
                            target = np.array(df_group["y"])
                        pred = self.predictions_[f"{model_name}_{model_group}"][sample]
                else:
                    pred = self.predictions_[f"{model_name}_{model_group}"][sample]

                try:
                    score = metric(target, pred)
                except (ValueError, TypeError, KeyError) as e:
                    print(f"{e}")
                    score = np.nan

                if isinstance(score, tuple):
                    metrics_score.append(round(100 * score[0], 2))
                elif isinstance(score, (int, float, np.float32, np.float64)):
                    if metric_name in [
                        "r2",
                    ]:
                        metrics_score.append(round(100 * score, 2))
                    else:
                        metrics_score.append(round(score, 2))
                else:
                    metrics_score.append(0)

        return metrics_score

    def transform(self, **eval_sets):
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
        self.create_all_predictions(**eval_sets)
        for model in self.models:
            if model == "LinearReg":
                scores[f"{model}_model_0"] = self.calculate_metrics(
                    model, "model_0", **eval_sets
                )
            else:
                for model_group in self.models[model].models_by_groups:
                    scores[f"{model}_{model_group}"] = self.calculate_metrics(
                        model, model_group, **eval_sets
                    )
        return self._to_frame(scores, **eval_sets)