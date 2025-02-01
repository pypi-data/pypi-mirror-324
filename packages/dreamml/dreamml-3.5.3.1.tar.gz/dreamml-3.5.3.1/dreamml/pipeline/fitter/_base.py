from abc import ABC
import abc
from typing import List, Optional

import pandas as pd

from dreamml.data._dataset import DataSet


class FitterBase(ABC):
    validation_type = None

    """
    Базовый класс Fitter
    """

    @staticmethod
    @abc.abstractmethod
    def get_validation_target(
        data_storage: DataSet, vectorization_name: Optional[str] = None
    ):
        """
        Возвращает истинные значения для расчета метрики (т.к. все данные по валидации у данного класса).

        Parameters
        ----------
        data_storage: DataSet
            Экземпляр класса-хранилища данных.

        Returns
        -------
        y_true: pd.Series
            Истинные значения для расчета метрики.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def train(
        self,
        estimator,
        data_storage: DataSet,
        metric: callable,
        used_features: List = None,
        sampling_flag: bool = None,
        vectorization_name: Optional[str] = None,
    ):
        """
        Основная функция для запуска модуля.

        Parameters
        ----------
        estimator: dreamml.modeling.models.estimators.boosting_base.BoostingBaseModel
            Экземпляр модели для обучения.

        data_storage: DataSet
            Экземпляр класса-хранилища данных.

        used_features: List
            Список используемых признаков.

        metric: callable
            Метрика для оценки качества модели.

        sampling_flag: bool
            Нужно ли использование сэмплинга(нужно для permutation stage, если датасет большой)

        Returns
        -------
        final_estimator: dreamml.modeling.models.estimators
            Финалиная модель обученная на среднем количестве итераций по всем фолдам умноженному на коэфициент.

        cv_estimators: None
            Для совместимости с FitterCV.

        used_features: List
            Список используемых признаков.

        vectorization_name: Optional[str]
            Алгоритм векторизации

        predictions: pd.Series
            Предсказания модели на валидационной выборке.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def calculate_importance(
        self,
        estimators,
        data_storage: DataSet,
        used_features: List = None,
        splitter_df: pd.DataFrame = None,
        fraction_sample: float = 1,
        vectorization_name: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        Функция для отбора признаков на основе кросс-валидации.

        Parameters
        ----------
        estimators: List[estimators] or dreamml.modeling.models.estimators.boosting_base.BoostingBaseModel
            Список экземпляров модели для обучения или 1 экземпляр, который будет растиражирован на все фолды.

        data_storage: DataSet
            Экземпляр класса-хранилища данных.

        used_features: List
            Список используемых признаков.

        splitter_df: pd.DataFrame
            Таблица, по которой будет проходить разбиение данных.

        fraction_sample: float, optional, default = 1.0,
            Доля наблюдений от data для оценки важности признаков.

        vectorization_name: Optional[str]
            Алгоритм векторизации

        Returns
        -------
        importance: pd.DataFrame
            Таблица с оценкой важности признаков.

        """
        raise NotImplementedError