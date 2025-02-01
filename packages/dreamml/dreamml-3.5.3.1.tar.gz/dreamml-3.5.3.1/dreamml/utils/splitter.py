# coding=utf-8
"""
Модуль с реализацией трансформера для разбиения выборки на train / valid / test.

Доступные сущности:
- DataSplitter: сплиттер на train / valid / test.
"""

from typing import List, Dict, Tuple, Sequence, Optional
import warnings

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import train_test_split
from skmultilearn.model_selection import IterativeStratification

from dreamml.utils.warnings import DMLWarning


def check_input_lengths(split_fractions):
    assert len(split_fractions) in (2, 3), (
        f"Указанное правило разбиения должно содержать 2 или 3 класса. "
        f"Подано {len(split_fractions)}."
    )
    if len(split_fractions) == 2:
        assert (
            sum(split_fractions) < 1 - 1e-5
        ), "Введённые доли в сумме должны быть меньше 1 и доля теста != 0"
        split_fractions.append(1 - sum(split_fractions))

    assert (
        abs(1 - sum(split_fractions)) <= 1e-5
    ), "Указанные доли в сумме должный давать 1"


class DataSplitter(BaseEstimator, TransformerMixin):
    """
    Разбиение выборки на train / valid / test.

    Parameters
    ----------
    split_fractions: List[float]
        Список с параметрами разбиения выборки на train / valid / test.
        Может быть указано в виде долей разбиения: [0.6, 0.3, 0.1]. Доля теста > 0.
        Доля теста может быть определена автоматически.

    group_column: string, optional, default = None
        Название поля, по которому произвести разбиение.
        Опциональный параметр, по умолчанию не используется.

    target_name: string, optional, default = None
        Название поля, по которому произвести stratified разбиение, если не указан параметр `group_column`.
        Опциональный параметр, по умолчанию не используется.
    """

    def __init__(
        self,
        split_fractions: List[float],
        shuffle: bool = True,
        group_column: Optional[str] = None,
        target_name: Optional[str] = None,
        stratify: bool = False,
        task: Optional[str] = None,
        time_column: Optional[str] = None,
        split_by_group: bool = False,
    ):

        check_input_lengths(split_fractions)

        self.split_fractions = split_fractions
        self.n_samples = len(split_fractions)
        self.group_column = group_column
        self.split_by_group = split_by_group
        self.target_name = target_name
        self.shuffle = shuffle
        self.stratify = stratify
        self.task = task
        self.time_column = time_column

    def transform(
        self, data: pd.DataFrame, target: Optional[Sequence] = None
    ) -> Tuple[Sequence, Sequence, Sequence]:
        """
        Разбиение исходной выборки на train / valid / test.

        Parameters
        ----------
        data: pd.DataFrame
            Датасет для разбиения.

        target: Sequence, optional, default = None
            Используется в случае, если необходимо провести stratified разбиение
            датасета `data` по произвольному таргету.
            Опциональный параметр, по умолчанию не используется.

        Returns
        -------
        indexes: Tuple[Sequence, Sequence, Sequence]
            Индексы тренировочной, валидационной и тестовой выборки.

        """
        splitter = self.get_splitter()

        if target is None:
            indexes = splitter(data)
        else:
            # for backward compatibility
            original_target_name = self.target_name
            self.target_name = "__tmp__"

            data["__tmp__"] = target
            indexes = splitter(data)
            data.pop("__tmp__")

            self.target_name = original_target_name

        return indexes

    def get_splitter(self) -> callable:
        """
        Выбор метода разбиения исходной выборки на train / valid / test.

        Returns
        -------
        splitter: callable
            Метод разбиения данных.

        """
        if self.group_column and self.split_by_group:
            return self._column_split
        elif self.target_name:
            return self._random_stratify_split
        else:
            return self._random_split

    def _random_stratify_split(
        self, data: pd.DataFrame
    ) -> Tuple[Sequence, Sequence, Sequence]:
        """
        Случайное, стратифицированное по целевой переменной,
        разбиение данных на train / valid / test. Применяется в случае,
        если target - бинарный вектор.

        Parameters
        ----------
        data: pandas.DataFrame, shape = [n_samples, n_features]
            Обучающая выборка.

        Returns
        -------
        indexes: Tuple[Sequence, Sequence, Sequence]
            Индексы тренировочной, валидационной и тестовой выборки.

        """
        target = data.get(self.target_name)

        if self.stratify:
            if target is None:
                warnings.warn(
                    f"Cannot perform stratified split with {self.target_name}. Performing random split",
                    DMLWarning,
                    stacklevel=3,
                )
            elif isinstance(target, pd.DataFrame):
                return self._calculate_multilabel_stratify_split_idx(
                    data=data,
                    target=target,
                )
            else:
                return self._calculate_split_idx(data.index, target, self.shuffle)

        return self._random_split(data)

    def _random_split(self, data: pd.DataFrame) -> Tuple[Sequence, Sequence, Sequence]:
        """
        Случайное разбиение данных на train / valid / test.
        Применяется в случае, если target - вектор непрерывной целевой
        переменной.

        Parameters
        ----------
        data: pandas.DataFrame, shape = [n_samples, n_features]
            Обучающая выборка.

        Returns
        -------
        indexes: Tuple[Sequence, Sequence, Sequence]
            Индексы тренировочной, валидационной и тестовой выборки.

        """
        return self._calculate_split_idx(data.index, shuffle=self.shuffle)

    def _column_split(self, data: pd.DataFrame) -> Tuple[Sequence, Sequence, Sequence]:
        """
        Разбиение данных на train / valid / test по заданному полю.
        Применяется в случае, когда задано self.group_column и требуется
        разбить данные по полю (например: по клиенту).

        Parameters
        ----------
        data: pandas.DataFrame, shape = [n_samples, n_features]
            Обучающая выборка.

        Returns
        -------
        indexes: Tuple[Sequence, Sequence, Sequence]
            Индексы тренировочной, валидационной и тестовой выборки.

        """

        values = data[self.group_column].unique()
        if self.task is not None and self.task == "timeseries":
            train_idx, valid_idx, test_idx = self._timeseries_segment_split(data)
            return train_idx, valid_idx, test_idx

        train_idx, valid_idx, test_idx = self._calculate_split_idx(
            values, shuffle=self.shuffle
        )

        train_mask = data[self.group_column].isin(train_idx)
        train_idx = data.loc[train_mask].index

        valid_mask = data[self.group_column].isin(valid_idx)
        valid_idx = data.loc[valid_mask].index

        test_mask = data[self.group_column].isin(test_idx)
        test_idx = data.loc[test_mask].index

        return train_idx, valid_idx, test_idx

    def _timeseries_segment_split(self, data: pd.DataFrame):
        """
        Разбиение данных на train / valid / [test] по заданному полю.
        Применяется в случае, когда задано group_column и требуется
        разбить данные по полю (например: по клиенту) для задачи timeseries.

        Parameters
        ----------
        data: pandas.DataFrame, shape = [n_samples, n_features]
            Обучающая выборка.

        target: pandas.Series, shape = [n_samples, ]
            Вектор целевой переменной.

        Returns
        -------
        eval_set: Dict[string, Tuple[pd.DataFrame, pd.Series]]
            Словарь, где ключ - название выборки, значение - кортеж
            с матрицей признаков и вектором целевой переменной.

        """
        train_segmented, test_segmented, val_segmented = [], [], []

        for segment in data[self.group_column].unique():
            segment_data = data[data[self.group_column] == segment]
            if self.time_column is not None and self.time_column in data.columns:
                segment_data = segment_data.sort_values(by=[self.time_column])
            else:
                segment_data = segment_data.sort_index()

            train_size = int(len(segment_data) * self.split_fractions[0])
            test_size = int(len(segment_data) * self.split_fractions[2])

            train = segment_data.iloc[:train_size].index.to_list()
            test = segment_data.iloc[
                train_size : train_size + test_size
            ].index.to_list()
            valid = segment_data.iloc[train_size + test_size :].index.to_list()

            train_segmented.extend(train)
            test_segmented.extend(test)
            val_segmented.extend(valid)

        return (
            pd.Index(train_segmented),
            pd.Index(test_segmented),
            pd.Index(val_segmented),
        )

    def _calculate_split_idx(
        self,
        idx_array: Sequence,
        target: Optional[Sequence] = None,
        shuffle: bool = False,
    ) -> Tuple[Sequence, Sequence, Sequence]:
        """
        Вычисление индексов для train / valid / test частей.

        Parameters
        ----------
        idx_array: Sequence
            Индексы для разбиения.

        target: Sequence, optional, default = None
            Вектор целевой переменной, опциональный параметр,
            по умолчанию не используется.

        Returns
        -------
        indexes: Tuple[Sequence, Sequence, Sequence]
            Индексы тренировочной, валидационной и тестовой выборки.

        """
        train_idx, valid_idx = train_test_split(
            idx_array,
            train_size=self.split_fractions[0],
            stratify=target,
            shuffle=shuffle,
        )

        if (
            isinstance(self.split_fractions[0], float)
            and sum(self.split_fractions) <= 1
        ):
            size = self.split_fractions[1] / (
                self.split_fractions[1] + self.split_fractions[2]
            )
        else:
            size = self.split_fractions[1]

        if isinstance(target, pd.Series):
            target = target.loc[valid_idx]

        valid_idx, test_idx = train_test_split(
            valid_idx,
            train_size=size,
            stratify=target,
            random_state=10,
            shuffle=shuffle,
        )

        return train_idx, valid_idx, test_idx

    def _calculate_multilabel_stratify_split_idx(
        self,
        data: pd.DataFrame,
        target: pd.DataFrame,
    ) -> Tuple[Sequence, Sequence, Sequence]:
        """
        Вычисление индексов для multilabel train / valid / test частей.

        Parameters
        ----------
        idx_array: Sequence
            Индексы для разбиения.

        target: Sequence, optional, default = None
            Вектор целевой переменной, опциональный параметр,
            по умолчанию не используется.

        Returns
        -------
        indexes: Tuple[Sequence, Sequence, Sequence]
            Индексы тренировочной, валидационной и тестовой выборки.

        """
        if target.isna().sum().sum():
            target = target.fillna(value=-1)

        train_indexes, test_indexes = iterative_train_test_split(
            data.values,
            target.values,
            test_size=self.split_fractions[2],
        )
        if (
            isinstance(self.split_fractions[0], float)
            and sum(self.split_fractions) <= 1
        ):
            size = self.split_fractions[1] / (
                self.split_fractions[1] + self.split_fractions[2]
            )
        else:
            size = self.split_fractions[1]

        test_indexes, valid_indexes = iterative_train_test_split(
            data.values[test_indexes],
            target.values[test_indexes],
            test_size=size,
        )
        return train_indexes, valid_indexes, test_indexes


def iterative_train_test_split(X, y, test_size):
    """Iteratively stratified train/test split

    Parameters
    ----------
    test_size : float, [0,1]
        the proportion of the dataset to include in the test split, the rest will be put in the train set

    Returns
    -------
    train_indexes, test_indexes
        stratified indexes into train/test split
    """

    stratifier = IterativeStratification(
        n_splits=2, order=2, sample_distribution_per_fold=[test_size, 1.0 - test_size]
    )
    train_indexes, test_indexes = next(stratifier.split(X, y))
    return train_indexes, test_indexes