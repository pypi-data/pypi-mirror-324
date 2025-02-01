"""
Модуль с реализацией интерфейса моделей машинного обучения.

Доступные сущности:
- BoostingBaseModel: API ML-модели.
- BaseClassifier: реализовация базового классификатора.
- BaseRegressor: реализация базового регрессора.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from copy import deepcopy

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.exceptions import NotFittedError
from sklearn.metrics import roc_auc_score

from dreamml.logging import get_logger
from dreamml.utils.errors import MissedColumnError
from dreamml.features.feature_selection._permutation_importance import (
    calculate_permutation_feature_importance,
)

_logger = get_logger(__name__)


class BoostingBaseModel(ABC, BaseEstimator, TransformerMixin):
    """
    API ML-модели для использования в DS-Template.

    Используется как базовый класс для реализации конкретной модели.
    Содержит общие методы, которые используются для любого типа модели.

    Parameters
    ----------
    params: dict
        Словарь гиперпараметров модели.

    used_features: List[string]
        Список используемых для обучения признаков.

    categorical_features: List[string], optional, default = None
        Список категориальных признаков.
        Опциональный параметр, по умолчанию не используется.

    lr_reduce: int, default = None
        Количество возможных понижений learning rate.

    Attributes
    ----------
    estimator: callable
        Экземпляр обученной модели.

    """

    def __init__(
        self,
        params: dict,
        used_features: List[str],
        categorical_features: Optional[List[str]] = None,
        lr_reduce: Optional[int] = 0,
    ):

        self.params = deepcopy(params)
        self.used_features = used_features
        if categorical_features:
            self.categorical_features = list(
                set(categorical_features) & set(used_features)
            )
        else:
            self.categorical_features = None
        self.estimator = None
        self.lr_reduce = lr_reduce

    def validate_input_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Проверка входных данных data на наличие требуемых признаков.
        Если ожидаемые признаки отсутствуют в наборе данных, то
        возбуждается MissedColumnError.

        Parameters
        ----------
        data: pandas.DataFrame, shape = [n_samples, n_features]
            Матрица признаков для проверки.

        Returns
        -------
        data_validated: pandas.DataFrame
            Матрица признаков, содержащая требуемые признаки.

        """
        if self.used_features:
            missed_features = list(set(self.used_features) - set(data.columns))
            if missed_features:
                raise MissedColumnError(f"Missed {list(missed_features)} columns.")
            return data[self.used_features]

        return data

    @property
    def check_is_fitted(self):
        """
        Проверка была ли обучена модель.
        Если проверка не пройдена - возбуждается исключение NotFittedError.
        """
        if not bool(self.estimator):
            msg = (
                "This estimator is not fitted yet. Call 'fit' with"
                "appropriate arguments before using this estimator."
            )
            raise NotFittedError(msg)
        return True

    @abstractmethod
    def fit(self, data: pd.DataFrame, target: pd.Series, *eval_set) -> None:
        """
        Абстрактный метод - обучение модели на данных (data, target).
        """
        pass

    @abstractmethod
    def transform(self, data: pd.DataFrame) -> None:
        """
        Абстрактный метод - применение модели к данным data.
        """
        pass


class BaseClassifier(BoostingBaseModel):
    """
    Базовый классификатор в DS-Template.

    Используется как базовый класс для реализации конкретного
    классификатора. Содежрит общие методы, которые используется
    для любой реализации классификатора и не зависят от деталей
    реализации.

    Parameters
    ----------
    params: dict
        Словарь гиперпараметров модели.

    used_features: List[string]
        Список используемых для обучения признаков.

    categorical_features: List[string], optional, default = None
        Список категориальных признаков.
        Опциональный параметр, по умолчанию не используется.

    Attributes
    ----------
    estimator: callable
        Экземпляр обученной модели.

    """

    def evaluate_model(self, **eval_sets) -> None:
        """
        Оценка качества модели метрикой GINI на eval_sets.

        Parameters
        ----------
        eval_sets: Dict[string, Tuple[pandas.DataFrame, pandas.Series]]
            Словарь, где ключ - название выборки, значение - кортеж с
            матрицей признаков и вектором истинных ответов.

        """
        for sample in eval_sets:
            data, target = eval_sets[sample]
            prediction = self.transform(data)

            try:
                score = roc_auc_score(target, prediction)
                score = 2 * score - 1
                score = 100 * score
            except ValueError:
                score = 0

            _logger.info(f"{sample}-score:\t GINI = {round(score, 2)}")

    def feature_importance(self, data, target):
        """
        Расчет важности признаков на основе перестановок.
        Важность рассчитывается, если задан self.eval_set,
        и применен метод `fit` для модели. Если self.eval_set
        не задан, то возбуждается ValueError.

        Parameters
        ----------
        data: pandas.DataFrame, shape = [n_samples, n_features]
            Матрица признаков (обучающая выборка).

        target: pandas.Series, shape = [n_samples, ]
            Вектор целевой переменной.

        Returns
        -------
        feature_importance: pandas.DataFrame
            Оценка важности признаков.

        """
        return calculate_permutation_feature_importance(
            self, roc_auc_score, data[self.used_features], target
        )

    def refit(self, data: pd.DataFrame, target: pd.Series, *eval_set):
        """
        Понижение learning rate и повторное применение метода
        'fit' для модели.

        Parameters
        ----------
        data: pandas.DataFrame, shape = [n_samples, n_features]
            Матрица признаков (обучающая выборка).

        target: pandas.Series, shape = [n_samples, ]
            Вектор целевой переменной.

        """
        self.lr_reduce -= 1
        _logger.info(25 * "-" + "ovefitting" + 25 * "-")
        _logger.info(
            "learning_rate_before = ",
            self.params["learning_rate"],
            " learning_rate_after = ",
            self.params["learning_rate"] / 2,
        )
        self.params["learning_rate"] /= 2
        self.fit(data, target, *eval_set)