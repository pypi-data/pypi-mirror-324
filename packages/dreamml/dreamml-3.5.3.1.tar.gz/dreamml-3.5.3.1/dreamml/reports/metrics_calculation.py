from copy import deepcopy
from typing import Dict, Optional, Callable

import numpy as np
import pandas as pd

from dreamml.logging import get_logger
from dreamml.modeling.models.estimators import BaseModel
from dreamml.utils.vectorization_eval_set import get_eval_set_with_embeddings

_logger = get_logger(__name__)


class BaseMetricsCalculator:
    def __init__(
        self,
        models: Dict[str, BaseModel],
        predictions: Optional[Dict] = None,
        vectorizers: Optional[Dict] = None,
        calculate_metrics_ratio: bool = False,
        transform_target: Optional[Callable] = None,
    ) -> None:
        self.models = models
        self.predictions_ = predictions or {}
        self.vectorizers = vectorizers
        self.metrics = self._get_metrics_to_calculate()
        self.calculate_metrics_ratio = calculate_metrics_ratio
        self.transform_target = transform_target

    def transform(self, **eval_sets):
        """
        Расчет метрик для каждой модели из `self.models` и каждой выборки из `eval_sets`
        и получение pd.DataFrame с результатами на выходе.

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
        if not self.predictions_:
            self.create_all_predictions(**eval_sets)
        else:
            _logger.info("Used Pre-calculated predictions")

        scores = {}
        for model in self.models:
            scores[model] = self.calculate_metrics(model, **eval_sets)

        return self._to_frame(scores, **eval_sets)

    def _to_frame(self, scores: dict, **eval_sets) -> pd.DataFrame:
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

        scores_name = ["Название модели", "# признаков"]
        for metric in self.metrics:
            for sample in eval_sets:
                scores_name.append(f"{metric} {sample}")

            if self.calculate_metrics_ratio:
                scores_name.append(f"{metric} delta train vs test")
                scores_name.append(f"{metric} delta train vs test, %")

                if "OOT" in eval_sets:
                    scores_name.append(f"{metric} delta train vs OOT")
                    scores_name.append(f"{metric} delta train vs OOT, %")

        scores.columns = scores_name
        scores = scores.fillna(0)

        scores["детали о модели"] = [
            f"Ссылка на лист train {model}" for model in scores["Название модели"]
        ]
        return scores

    @staticmethod
    def create_prediction(model: BaseModel, data: pd.DataFrame) -> np.array:
        """
        Применение модели model к набору данных data.

        Parameters
        ----------
        model: BaseModel
            Экземпляр ML-модели

        data: pandas.DataFrame, shape = [n_samples, n_features]
            Набор данных для применения модели.

        Returns
        -------
        pred: np.array
            Вектор прогнозов.

        """
        try:
            pred = model.transform(data)
        except TypeError:
            pred = np.zeros(data.shape[0])

        return pred

    def calculate_metrics(self, model_name, **eval_sets):
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
            model = self.models[model_name]
            metrics_score = [len(model.used_features)]
        except TypeError:
            sample_name = next(iter(eval_sets))
            metrics_score = [len(eval_sets[sample_name][0])]

        for metric_name, metric in self.metrics.items():
            eval_sets_score = {}
            for sample in eval_sets:
                _, target = eval_sets[sample]

                if self.transform_target is not None:
                    target = self.transform_target(target)

                pred = self.predictions_[model_name]
                try:
                    score = metric(target, pred[sample])
                except (ValueError, TypeError, KeyError) as e:
                    _logger.exception(f"{e}")
                    score = np.nan

                eval_sets_score[sample] = score

            for sample, score in eval_sets_score.items():
                metrics_score.append(score)

            if self.calculate_metrics_ratio:
                diff = np.abs(eval_sets_score["train"] - eval_sets_score["test"])
                relative_diff = 100 * diff / eval_sets_score["train"]

                metrics_score += [diff, relative_diff]

                if "OOT" in eval_sets:
                    diff = np.abs(eval_sets_score["train"] - eval_sets_score["OOT"])
                    relative_diff = 100 * diff / eval_sets_score["train"]
                    metrics_score += [diff, relative_diff]

        return metrics_score

    def create_all_predictions(self, **eval_sets):
        """
        Применение всех моделей из self.models к наборам данных
        из eval_set
        """

        for model_name, model in self.models.items():
            eval_sets_ = deepcopy(eval_sets)
            self.predictions_[model_name] = {}
            samples_preds = {}

            if self.vectorizers is not None:

                if hasattr(model, "vectorization_name"):
                    if (
                        model.vectorization_name != "bert"
                        and self.vectorizers is not None
                    ):
                        vectorizer_name = f"{model.vectorization_name}_vectorizer"

                        if vectorizer_name not in self.vectorizers:
                            raise ValueError(
                                f"{vectorizer_name} not found in vectorizers."
                            )

                        vectorizer = self.vectorizers[vectorizer_name]

                        eval_sets_ = get_eval_set_with_embeddings(
                            vectorizer, eval_sets_
                        )

            for sample_name, (data, _) in eval_sets_.items():
                pred = self.create_prediction(model, data)

                samples_preds[sample_name] = pred

            self.predictions_[model_name] = samples_preds

    def _get_metrics_to_calculate(self):
        raise NotImplementedError