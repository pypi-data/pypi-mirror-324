import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class CorrelationFeatureSelection(BaseEstimator, TransformerMixin):
    """
    Отбор признаков на основе корреляции.
    Удаляем сильно скоррелированные между собой признаки.
    Остается один из признаков с наибольшей корреляцией с целевой переменной.

        Parameters
    ----------
    threshold: float, optional, default = 0.9
        Порог для отбора признаков. Опциональный параметр.
        По умолчанию, используется значение threshold = 0.9.

    used_features: list
        Список используемых признаков

    remaining_features: List[str], default=[]
        Признаки, которые в любом случае должны остаться в датасете после отбора

    """

    def __init__(
        self,
        threshold: float = 0.9,
        used_features: list = None,
        remaining_features: list = [],
    ):

        self.threshold = threshold
        self.used_features = used_features
        self.remaining_features = remaining_features

    def _calculate_correlations(self, X: pd.DataFrame, y: pd.Series) -> list:
        """
        Рассчет корреляций между признаками и составление списка используемых признаков.

            Parameters
        ----------
        X: pd.DataFrame
            Матрица признаков.

        y: pd.Series
            Вектор целевой переменной.

            Returns
        -------
        used_features: List
            Список отобранных признаков.
        """
        corr_matrix = X.corr().abs()
        upper_tri = corr_matrix.where(
            np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool_)
        )

        # pd.Series: index - кортеж из пары признаков, value - коэф. корреляции.
        corr_series = upper_tri.abs().unstack().dropna().sort_values()
        corr_series = corr_series[corr_series > self.threshold]

        # Корреляция с целевой переменной.
        corr_with_target = self._calculate_correlation_with_target(X, y)

        # Выбираем признак с самой высокой корреляцией с целевой переменной, а остальных исключаем.
        cols_to_drop = set()
        for col_1, col_2 in corr_series.index:
            if corr_with_target[col_1] < corr_with_target[col_2]:
                if col_1 not in self.remaining_features:
                    cols_to_drop.add(col_1)
            else:
                if col_2 not in self.remaining_features:
                    cols_to_drop.add(col_2)

        used_features = set(self.used_features) - cols_to_drop

        return list(used_features)

    @staticmethod
    def _calculate_correlation_with_target(X: pd.DataFrame, y: pd.Series) -> pd.Series:
        """
        Рассчет корреляций признаков с целевой переменной

            Parameters
        ----------
        X: pd.DataFrame
            Матрица признаков.

        y: pd.Series
            Вектор целевой переменной.

            Returns
        -------
        corr_with_target: pandas.Series
            Тaблица корреляций признаков с целевой переменной
        """
        result = X.corrwith(y).abs()

        return result

    def fit(self, X: pd.DataFrame, y: pd.Series):
        """
            Parameters
        ----------
        X: pd.DataFrame
            Матрица признаков.

        y: pd.Series
            Вектор целевой переменной.

            Returns
        -------
        self.
        """
        self.used_features = self.used_features if self.used_features else X.columns
        self.used_features = self._calculate_correlations(X, y)

        return self

    def transform(self, X: pd.DataFrame):
        """
            Parameters
        ----------
        X: pd.DataFrame
            Матрица признаков.

        y: pd.Series
            Вектор целевой переменной.

            Returns
        -------
        used_features: List
            Список отобранных признаков.
        """

        return self.used_features