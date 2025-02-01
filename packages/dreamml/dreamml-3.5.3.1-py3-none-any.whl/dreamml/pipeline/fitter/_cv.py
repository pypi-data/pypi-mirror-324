import numpy as np
import pandas as pd
from typing import List, Union, Optional, Type
from copy import deepcopy

from dreamml.configs.config_storage import ConfigStorage
from dreamml.features.feature_selection.shap_importance import (
    calculate_shap_feature_importance,
)
from dreamml.data._dataset import DataSet
from dreamml.modeling.metrics import BaseMetric
from dreamml.modeling.models import PyBoostModel
from dreamml.modeling.cv import (
    make_cv,
    BaseCrossValidator,
    KFoldCrossValidator,
    GroupCrossValidator,
    GroupTimePeriodCrossValidator,
    TimeSeriesCrossValidator,
    TimeSeriesGroupTimePeriodCrossValidator,
)
from dreamml.pipeline.fitter import FitterBase
from dreamml.utils import ValidationType
from dreamml.utils.errors import ConfigurationError


class FitterCV(FitterBase):
    validation_type = ValidationType.CV

    def __init__(self, cv: BaseCrossValidator):
        """
        Parameters
        ----------
        cv: BaseCrossValidator
            Генератор для осуществления кросс-валидации.

        """
        self.cv_mean_score = None
        self.cv = cv

    @staticmethod
    def _fit_final_model(
        estimator,
        x: pd.DataFrame,
        y: pd.Series,
        n_trees_: Union[int, List[int]],
        coef_: float = 1.2,
        **eval_set,
    ):
        """
        Дообучение финальной модели на всех наблюдениях.

        Parameters
        ----------
        estimator: dreamml.modeling.models.estimators._base.BaseModel
            Экземпляр модели для обучения.

        x: pandas.core.frame.DataFrame
            Матрица признаков для обучения модели.

        y: pandas.core.frame.Series
            Вектор целевой переменной для обучения модели.

        n_trees_: int
            Среднее значение количества итераций обучения на кросс-валидации.

        coef_: float
            Коэфициент на который мы умножаем n_trees_.

        Returns
        -------
        final_estimator: dreamml.modeling.models.estimators.boosting_base.BoostingBaseModel
            Финалиная модель обученная на среднем количестве итераций по всем фолдам умноженному на коэфициент.

        """
        final_estimator = deepcopy(estimator)

        if isinstance(n_trees_, int):
            final_estimator_n_trees = max([int(coef_ * n_trees_), 1])
        else:
            final_estimator_n_trees = (coef_ * np.array(n_trees_)).astype(int)
            final_estimator_n_trees = np.where(
                final_estimator_n_trees < 1,
                np.ones_like(final_estimator_n_trees),
                final_estimator_n_trees,
            )
            final_estimator_n_trees = final_estimator_n_trees.tolist()

        if isinstance(final_estimator, PyBoostModel):
            final_estimator.params["ntrees"] = final_estimator_n_trees
        else:
            final_estimator.params["n_estimators"] = final_estimator_n_trees

        final_estimator.fit(x, y, x, y)
        final_estimator.evaluate_and_print(**eval_set)

        return final_estimator

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
        _, y_true = data_storage.get_cv_data_set(vectorization_name=vectorization_name)

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

        Returns
        -------
        importance: pd.DataFrame
            Таблица с оценкой важности признаков.

        """
        if splitter_df is None:
            raise ValueError("Cannot make cv without splitter_df")

        importance = pd.DataFrame()
        x, y = data_storage.get_cv_data_set(
            used_features, vectorization_name=vectorization_name
        )
        x = x.reset_index(drop=True)
        y = y.reset_index(drop=True)
        if not isinstance(estimators, list or np.array or pd.Series):
            # TODO для чего нужна эта конструкция?
            estimators = [estimators for _ in range(self.cv.n_splits)]
        for fold_number, (train_index, valid_index) in enumerate(
            self.cv.split(splitter_df)
        ):
            x_train, x_valid = x.loc[train_index], x.loc[valid_index]
            fold_importance = calculate_shap_feature_importance(
                estimator=estimators[fold_number],
                data=x_train,
                fraction_sample=fraction_sample,
            )

            importance = pd.concat([importance, fold_importance], axis=0)

        column_name = [x for x in importance.columns.tolist() if "importance" in x][0]
        importance = importance.groupby(["feature"])[column_name].mean().reset_index()
        importance = importance.sort_values(by=column_name, ascending=False)

        return importance.reset_index(drop=True)

    def train(
        self,
        estimator,
        data_storage: DataSet,
        metric: BaseMetric,
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

        metric: BaseMetric
            Метрика для оценки качества модели.

        sampling_flag: bool
            Нужен для совместимости

        Returns
        -------
        final_estimator: dreamml.modeling.models.estimators
            Финалиная модель обученная на среднем количестве итераций по всем фолдам умноженному на коэфициент.

        cv_estimators: List
            Список моделей обученных на фолдах.

        used_features: List
            Список используемых признаков.

        predictions: pd.Series
            Предсказания модели на out of fold.
        """
        if data_storage.task == "topic_modeling":
            x = data_storage.get_cv_data_set(
                used_features, vectorization_name=vectorization_name
            )
        else:
            x, y = data_storage.get_cv_data_set(
                used_features, vectorization_name=vectorization_name
            )
        eval_set = data_storage.get_eval_set(
            used_features, vectorization_name=vectorization_name
        )
        splitter_df = data_storage.get_cv_splitter_df(self.cv.get_required_columns())

        estimators, mean_folds_score, _, mean_folds_trees, _, oof_predictions = make_cv(
            estimator,
            x,
            y,
            self.cv,
            splitter_df,
            metric,
        )

        if estimator.task not in ["regression", "timeseries"]:
            mean_folds_score = mean_folds_score * 100
        self.cv_mean_score = mean_folds_score
        if ("valid" in eval_set) and (len(eval_set["valid"][0]) == 0):
            del eval_set["valid"]
        final_estimator = self._fit_final_model(
            estimator, x, y, n_trees_=mean_folds_trees, coef_=1.2, **eval_set
        )

        return final_estimator, estimators, oof_predictions


def _get_cv(
    config: ConfigStorage,
    custom_cv: Optional[Type[BaseCrossValidator]] = None,
) -> BaseCrossValidator:
    if custom_cv is not None:
        cv = custom_cv(**config.validation_params["cv_params"])

        return cv

    if config.task in ["binary", "multiclass", "multilabel"] and config.stratify:
        stratify_column = config.target_name
    else:
        stratify_column = None

    random_state = config.random_seed if config.shuffle else None
    nlp_augs = config.text_augmentations

    if isinstance(config.group_column, str):
        group_columns = [config.group_column]
    else:
        group_columns = config.group_column

    if nlp_augs is not None and len(nlp_augs) > 0:
        cv = GroupCrossValidator(
            group_columns=[
                col for col in config._service_fields if col.find("nlp_aug") != -1
            ],
            stratify_column=stratify_column,
            n_splits=config.cv_n_folds,
            shuffle=config.shuffle,
            random_state=random_state,
        )
        return cv

    if config.time_series_split or config.time_series_window_split:
        sliding_window = True if config.time_series_window_split else False

        if config.split_by_time_period:
            cv = TimeSeriesGroupTimePeriodCrossValidator(
                time_column=config.time_column,
                time_period=config.time_column_period,
                group_columns=group_columns,
                n_splits=config.cv_n_folds,
                sliding_window=sliding_window,
                test_size=config.time_series_split_test_size,
                gap=config.time_series_split_gap,
            )
        elif config.split_by_group:
            raise ConfigurationError(
                "Can't split by group without time period in time series."
            )
        else:
            cv = TimeSeriesCrossValidator(
                time_column=config.time_column,
                n_splits=config.cv_n_folds,
                sliding_window=sliding_window,
                test_size=config.time_series_split_test_size,
                gap=config.time_series_split_gap,
            )

        return cv

    elif config.split_by_time_period:
        cv = GroupTimePeriodCrossValidator(
            time_column=config.time_column,
            time_period=config.time_column_period,
            group_columns=group_columns,
            stratify_column=stratify_column,
            n_splits=config.cv_n_folds,
            shuffle=config.shuffle,
            random_state=random_state,
        )
    elif config.split_by_group:
        cv = GroupCrossValidator(
            group_columns=group_columns,
            stratify_column=stratify_column,
            n_splits=config.cv_n_folds,
            shuffle=config.shuffle,
            random_state=random_state,
        )
    else:
        cv = KFoldCrossValidator(
            stratify_column=stratify_column,
            n_splits=config.cv_n_folds,
            shuffle=config.shuffle,
            random_state=random_state,
        )

    return cv