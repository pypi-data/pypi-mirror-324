import pandas as pd
from typing import List, Dict, Optional

from dreamml.features.feature_selection.shap_importance import (
    calculate_shap_feature_importance,
)
from dreamml.data._dataset import DataSet
from dreamml.modeling.metrics import BaseMetric
from dreamml.pipeline.fitter import FitterBase
from dreamml.utils import ValidationType
from dreamml.modeling.models.estimators import BaseModel


class FitterHO(FitterBase):
    validation_type = ValidationType.HOLDOUT

    @staticmethod
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
        data = data_storage.get_eval_set(vectorization_name=vectorization_name)
        _, y_true = data["valid"]

        return y_true

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
        Функция для отбора признаков на hold-out разбиении (train/valid/test).

        Parameters
        ----------
        estimators: dreamml.modeling.models.boosting_base.BaseModel
            Экземпляр модели для обучения.

        data_storage: DataSet
            Экземпляр класса-хранилища данных

        used_features: List
            Список используемых признаков.

        splitter_df: pd.DataFrame
            (для одинакового интерфейса с кросс-валидацией).

        fraction_sample: float, optional, default = 1.0,
            Доля наблюдений от data для оценки важности признаков.

        Returns
        -------
        importance: pd.DataFrame
            Таблица с оценкой важности признаков.

        """
        data = data_storage.get_eval_set(
            used_features, vectorization_name=vectorization_name
        )
        x_train, y_train = data["train"]

        importance = calculate_shap_feature_importance(
            estimator=estimators, data=x_train, fraction_sample=fraction_sample
        )

        column_name = [x for x in importance.columns.tolist() if "importance" in x][0]
        importance = importance.sort_values(by=column_name, ascending=False)

        return importance.reset_index(drop=True)

    def train(
        self,
        estimator: BaseModel,
        data_storage: DataSet,
        metric: BaseMetric,
        used_features: List = None,
        sampling_flag: bool = False,
        vectorization_name: Optional[str] = None,
    ):
        """
        Основная функция для запуска модуля.

        Parameters
        ----------
        estimator: dreamml.modeling.models.estimators._base.BaseModel
            Экземпляр модели для обучения.

        data_storage: DataSet
            Экземпляр класса-хранилища данных.

        used_features: List
            Список используемых признаков.

        metric: BaseMetric
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

        predictions: pd.Series
            Предсказания модели на валидационной выборке.
        """

        eval_set = data_storage.get_eval_set(
            used_features, vectorization_name=vectorization_name
        )
        if sampling_flag and data_storage.get_dev_n_samples() >= 250000:
            eval_set["train"] = data_storage.sample(
                used_features, vectorization_name=vectorization_name
            )

        estimator.fit(*eval_set["train"], *eval_set["valid"])
        predictions = estimator.transform(eval_set["valid"][0])

        estimator.evaluate_and_print(**eval_set)

        return estimator, None, predictions