"""
# dreamml.features.categorical.categorical_encoder.py

# Team: Dream-Desk
# Author: Nikita Varganov
# e-mail: Varganov.N.V@sberbank.ru

=============================================================================

Модуль с реализацией доработанной версии LabelEncoder.

Доступные сущности:
- LabelEncoder: трансформер для обработки категориальных признаков

=============================================================================

"""

from copy import deepcopy
from typing import Union, Dict, List
import numpy as np
import pandas as pd
from sklearn.exceptions import NotFittedError
from sklearn.base import BaseEstimator, TransformerMixin

from dreamml.features.categorical._base import find_categorical_features
from dreamml.features.categorical._ordinal_encoder import DmlOrdinalEncoder
from dreamml.features.categorical._label_encoder import DmlLabelEncoder
from dreamml.features.categorical._one_hot_encoder import DmlOneHotEncoder
from dreamml.logging import get_logger

_logger = get_logger(__name__)


class CategoricalFeaturesTransformer(BaseEstimator, TransformerMixin):
    """
    Подготовка категориальных признаков: поиск и замена
    пропусков на фиксированное значение, применение
    LabelEncoder'a для перевода категорий в целочисленные
    векторы.

    Parameters:
    -----------
    config: dict
        Словарь с параметрами:
            * "categorical_features": config.categorical_features,
            * "task": config.task,
            * "target_name": config.target_name,

    fill_value: string, optional, default = "NA"
        Значение для заполнения пропущенных элементов.

    copy: bool, optional, default = True
        Если True, то создается копия data. Если False,
        то все преобразования data производится inplace.

    Attributes:
    -----------
    _unique_values: Dict[string: list]
        Словарь уникальных значений признака, для которых
        был применен метод fit. Ключ словаря - название
        категориального признака, значение - список уникальных
        значений данного признака.

    encoders: Dict[string: LabelEncoder()]
        Словарь encoder'ов для каждого категориального признака.
        Ключ словаря - название категориального признака,
        значение - экземпляр LabelEncoder(), для которого
        был применен метод fit.

    cat_features: List[str]
        Словарь строк с названием категориальных переменных.

    fitted: bool
        Флаг, обученного трансформера.
        По умолчанию, равен False, т.е. обучение проведено не было.

    """

    def __init__(
        self,
        config: dict,
        fill_value: str = "NA",
        copy: bool = True,
        max_unique_values: int = 5,
    ) -> None:
        self.fill_value = fill_value
        self.config = config
        self.copy = copy
        self.task = config.get("task", "binary")
        self.target_name = self.config.get("target_name")
        self.max_unique_values: int = max_unique_values
        self.encoders = {}
        self._unique_values = {}
        self.cat_features = None
        self.fitted = False
        self.target_name = self.config["target_name"]

    def _copy(self, data: pd.DataFrame) -> pd.DataFrame:
        return deepcopy(data) if self.copy else data

    @property
    def check_is_fitted(self):
        """
        Свойство для проверки использования метода 'fit'.
        Требуется для корректного применения трансформера на
        тестовую / валидационную выборку. Если метод 'fit' не был
        предварительно применен, то возбуждается исключение NotFittedError.

        """
        if not self.fitted:
            msg = (
                "This estimator is not fitted yet. Call 'fit' with "
                "appropriate arguments before using this estimator."
            )
            raise NotFittedError(msg)
        return True

    def _add_pandas_category_for_fillna(self, data, is_fitting=False):
        # pandas не может использовать .fillna на колонке с типом 'category'
        # нужно сначала добавить self.fill_value в набор категорий в этой колонке

        pandas_categorical_columns = data.dtypes[
            data.dtypes == "category"
        ].index.tolist()

        for column in pandas_categorical_columns:
            if self.fill_value in data.loc[:, column].cat.categories:
                if is_fitting:
                    raise ValueError(
                        f"Значение fill_value={self.fill_value} для заполнения пропусков "
                        f"совпадает с категорией в колонке {column=}."
                    )
                else:
                    continue

            data.loc[:, column] = data.loc[:, column].cat.add_categories(
                self.fill_value
            )

        return data

    def _prepare_data_dtypes(self, series: pd.Series) -> pd.Series:
        """
        Подготовка данных для передачи данных на вход encoder'a:
            - замена пропусков на fill_value;
            - преобразованеи столбца значений в object-столбец.

        Parameters:
        -----------
        series: pandas.Series
            Вектор наблюдений.

        Returns:
        --------
        series_prepared: pandas.Series
            Преобразованный вектор наблюдений.
        """
        series_prepared = series.fillna(self.fill_value)
        series_prepared = series_prepared.astype("str")
        return series_prepared

    def _find_new_values(self, series: pd.Series) -> pd.Series:
        """
        Поиск новых значений категориального признака, которые
        не были обработаны методом fit. Новые значения категории
        заменяются на fill_value, если fill_value был обработан
        методом fit, иначе - заменяются на первую обработанную
        категорию.

        Parameters:
        -----------
        series: pandas.Series
            Вектор наблюдений.

        Returns:
        --------
        series: pandas.Series
            Преобразованный вектор наблюдений.
        """
        observed_values = np.unique(series)
        expected_values = self._unique_values[series.name]
        new_values = list(set(observed_values) - set(expected_values))

        if new_values:
            bad_values_mask = series.isin(new_values)
            series[bad_values_mask] = (
                self.fill_value
                if self.fill_value in expected_values
                else expected_values[0]
            )

        return series

    def fit(self, data: pd.DataFrame):
        """
        Обучение Encoders

        Parameters:
        -----------
        data: pandas.DataFrame
            Матрица признаков.

        Returns:
        --------
        self: CategoricalFeaturesTransformer
        """
        _data = data.copy()
        _data = self._add_pandas_category_for_fillna(_data, is_fitting=True)

        self.cat_features = find_categorical_features(_data, config=self.config)

        for feature in self.cat_features:
            _data[feature] = self._prepare_data_dtypes(_data[feature])
            self._unique_values[feature] = np.unique(_data[feature]).tolist()

            self.encoders[feature] = DmlLabelEncoder().fit(data=_data, feature=feature)
            if feature == self.target_name:
                _logger.info(
                    f"Для целевой переменной ({self.config['target_name']}) применен LabelEncoder."
                )

            # Увеличивают количество признаков, что увеличивает время работы пайплайна
            # Теряется качество
            # Закомментировал до лучших времен

            # elif data[feature].nunique() >= self.max_unique_values:
            #     self.encoders[feature] = DmlOrdinalEncoder().fit(
            #         data=_data, feature=feature
            #     )
            #
            # else:
            #     self.encoders[feature] = DmlOneHotEncoder().fit(
            #         data=_data, feature=feature
            #     )

        self.fitted = True
        return self

    def transform(self, data):
        """
        Преобразование data, используя LabelEncoder.

        Parameters:
        -----------
        data: pandas.DataFrame
            Матрица признаков.

        Returns:
        --------
        data_transformed: pandas.DataFrame
            Преобразованная матрица признаков.
        """
        self.check_is_fitted
        data = self._add_pandas_category_for_fillna(data)

        x_transformed = self._copy(data)
        encoded_features = list(set(self.cat_features) & set(data.columns))

        for feature in encoded_features:
            x_transformed[feature] = self._prepare_data_dtypes(x_transformed[feature])
            x_transformed[feature] = self._find_new_values(x_transformed[feature])

            encoder = self.encoders[feature]
            x_transformed = encoder.transform(data=x_transformed, feature=feature)

        return x_transformed

    def inverse_transform(self, data: pd.DataFrame):
        self.check_is_fitted
        x_transformed = self._copy(data)

        for feature, encoder in sorted(self.encoders.items(), reverse=True):
            x_transformed = encoder.inverse_transform(x_transformed, feature)
        return x_transformed