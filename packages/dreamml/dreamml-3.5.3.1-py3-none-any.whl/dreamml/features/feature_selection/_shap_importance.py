from copy import deepcopy
from typing import Union
import shap
import numpy as np
import pandas as pd
import xgboost as xgb
from tqdm.auto import tqdm
from sklearn.base import BaseEstimator, TransformerMixin

from dreamml.modeling.metrics import BaseMetric
from dreamml.modeling.metrics.metrics_mapping import metrics_mapping

from dreamml.modeling.models.estimators import PyBoostModel


class ShapFeatureSelection(BaseEstimator, TransformerMixin):
    """
    Отбор признаков на основе Shap-Values и Uplift-теста.
    Для модели рассчитывается Shap-Values, после чего обучается
    модель на подмножестве признаков, размером от 1 до n: от
    самого важного до наименее важного. После обучения всех
    моделей - отбирается модель, которая укладывается в заданный
    диапазон изменения качества.

    Parameters
    ----------
    estimator: callable
        Обученный экземпляр модели.

    max_delta: int or float, optional, default = 1
        Максимально абсолютная допустимая разница между
        значением метрики качества для модели estimator и
        полученной в ходе uplift-тестирования модели.

    used_features: List[str]
        Список используемых признаков.

    metric: str
        Название используемой метрики.

    maximize: bool, optional, default = None
        Флаг максимизации метрики качества.
        Если значение True, то метрику требуется
        максимизировать, иначе - минимизировать.

    relative: bool, optional, default = None
        Флаг относительной разницы между значением метрики расчитанным напрямую
        и значением метрики в uplift-test
    """

    def __init__(
        self,
        estimator,
        metric_name,
        max_delta: Union[int, float] = 0.01,
        maximize: bool = True,
        relative: bool = False,
        metric_params: dict = None,
        task: str = "binary",
    ):
        self.estimator = estimator
        if self.estimator.categorical_features is None:
            self.estimator.categorical_features = []
        self.max_delta = max_delta
        self.used_features = estimator.used_features
        self.metric: BaseMetric = metrics_mapping.get(metric_name)(
            task=task, **metric_params
        )
        self.task = task
        self.metric_params = metric_params
        self.maximize = maximize
        self.relative = relative

    def _calculate_shap_values(self, X: pd.DataFrame) -> list:
        """
        Вычисление Shap-values для объекта экземпляра модели.
        Parameters
        ----------
        X: pandas.core.frame.DataFrame
            Матрица признаков для вычисления Shap-values.

        Returns
        -------
        shap_values: numpy.array
            Матрица Shap-values.

        """
        if isinstance(self.estimator, PyBoostModel):
            explainer = shap.PermutationExplainer(
                estimator, masker=shap.maskers._tabular.Tabular(data)
            )
        else:
            explainer = shap.TreeExplainer(self.estimator.estimator)

        try:
            if isinstance(explainer, shap.PermutationExplainer):
                shap_values = explainer.shap_values(
                    X=X[self.used_features], npermutations=5
                )
            else:
                shap_values = explainer.shap_values(X=X[self.used_features])
        except ValueError:
            X = xgb.DMatrix(X[self.used_features])
            shap_values = explainer.shap_values(X=X)

        if isinstance(shap_values, list):
            return shap_values[0]
        return shap_values

    def _calculate_feature_importance(self, X: pd.DataFrame):
        """
        Вычисление и сортировка важности признаков на
        основе Shap-values.
        Parameters
        ----------
        X: pandas.core.frame.DataFrame
            Матрица признаков для вычисления Shap-values.
        Returns
        -------
        importance: pandas.core.frame.DataFrame
            Матрица с отсортированными по важности признаками.
        """
        shap_values = self._calculate_shap_values(X=X)
        importance = pd.DataFrame(
            {
                "feature-name": self.estimator.used_features,
                "importance": np.abs(shap_values.mean(axis=0)),
            }
        )
        importance = importance.sort_values(by="importance", ascending=False)
        importance = importance.reset_index(drop=True)

        return importance

    def _calculate_uplift_iteration(self, X, y, features, *eval_set):
        """
        Вычисление одной итерации Uplift-теста.

        Parameters
        ----------
        X: pandas.core.frame.DataFrame
            Матрица признаков для обучения модели.

        y: pandas.core.frame.Series
            Вектор целевой переменной для обучения модели.

        features: List[str]
            Список признаков для обучения модели.

        eval_set: Tuple[pd.DataFrame, pd.Series]
            Кортеж с валидационными данными. Первый элемент
            кортежа - матрица признаков, второй элемент
            кортежа - вектор целевой переменной.

        Returns
        -------
        score: float
            Значение метрики качества на eval_set.

        """
        estimator = deepcopy(self.estimator)
        estimator.used_features = features
        estimator.categorical_features = list(
            set(estimator.categorical_features) & set(features)
        )
        estimator.fit(X, y, *eval_set)

        y_pred = estimator.transform(eval_set[0])

        score = self.metric(eval_set[1], y_pred)

        return score

    def transform(self, X, y, *eval_set):
        self.scores = {}
        importance = self._calculate_feature_importance(X)
        base_pred = self.estimator.transform(eval_set[0])
        base_score = self.metric(eval_set[1], base_pred)

        for num in tqdm(range(len(importance))):
            used_features = importance.loc[:num, "feature-name"]
            used_features = used_features.values.tolist()
            score = self._calculate_uplift_iteration(X, y, used_features, *eval_set)
            self.scores[num + 1] = [used_features, score]
            # TODO проблема: относительная шкала для метрик регрессии. Дельта в 0.001, а не в 1.0

            if self.relative and self.maximize:
                # Регрессия, относительная разница
                # Максимизация метрики
                if (base_score - score) / base_score <= self.max_delta:
                    return used_features
            elif self.relative:
                # Регрессия, относительная разница
                # Минимизация метрики
                if (score - base_score) / base_score <= self.max_delta:
                    return used_features
            else:
                if base_score - score <= self.max_delta:
                    return used_features


def finetune_features(shap_transformer: callable, threshold: float) -> list:
    """
    Финальный отбор признаков на основе относительного
    прироста качества при Uplift-тесте.

    Parameters
    ----------
    shap_transformer: dreamml.features.ShapFeatureSelection
        Обученный трансформер для отбора признаков на основе SHAP.

    threshold: float
        Значение для отбора признаков.
        По умолчанию, считается, что порог равен shap_threshold / 2.

    Returns
    -------
    selected_features: List[str]
        Список отобранных признаков.

    """
    num_features = len(shap_transformer.scores)
    total_features = shap_transformer.scores[num_features]
    total_features = total_features[0]

    scores = pd.DataFrame(shap_transformer.scores).T
    scores["delta"] = scores[1].diff().fillna(1)
    scores["features"] = total_features

    selected_features = scores[scores["delta"] > threshold]
    selected_features = selected_features["features"].values.tolist()

    return selected_features