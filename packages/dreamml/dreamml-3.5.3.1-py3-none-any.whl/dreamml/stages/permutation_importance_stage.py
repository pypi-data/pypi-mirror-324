from __future__ import annotations

from typing import List

import pandas as pd
from tqdm.auto import tqdm

from dreamml.logging.logger import CombinedLogger
from dreamml.logging import get_logger
from dreamml.modeling.cv import BaseCrossValidator
from dreamml.modeling.metrics import BaseMetric

from dreamml.features.feature_selection._permutation_importance import (
    select_subset_features,
    calculate_permutation_feature_importance,
)

from dreamml.data._dataset import DataSet

from dreamml.modeling.models.estimators import BoostingBaseModel
from dreamml.stages.algo_info import AlgoInfo
from dreamml.stages.model_based_stage import ModelBasedStage
from dreamml.stages.stage import BaseStage
from dreamml.pipeline.fitter import FitterBase
from dreamml.utils import ValidationType
from dreamml.configs.config_storage import ConfigStorage

_logger = get_logger(__name__)


class PermutationImportanceStage(ModelBasedStage):
    name = "permutation"

    def __init__(
        self,
        algo_info: AlgoInfo,
        config: ConfigStorage,
        fitter: FitterBase,
        vectorization_name: str = None,
    ):
        super().__init__(
            algo_info=algo_info,
            config=config,
            fitter=fitter,
            vectorization_name=vectorization_name,
        )
        self.threshold = config.permutation_threshold
        self.top_n = config.permutation_top_n
        self.sampling_flag = config.use_sampling
        self.remaining_features = config.remaining_features

    def _set_params(self, params: dict):
        raise NotImplementedError

    def _fit(
        self,
        model: BoostingBaseModel,
        used_features: List[str],
        data_storage: DataSet,
        models: List[BoostingBaseModel] = None,
    ) -> BaseStage:
        """
        Функция для обучения моделей на основе динамического отбора признаков по перестановкам
        Parameters
        ----------
        models:list
        data_storage: DataSet
        model: Type[BoostingBaseModel]
        used_features: list

        Returns
        -------
        self

        """
        if self.fitter.validation_type == ValidationType.CV:
            x, y = data_storage.get_cv_data_set(
                used_features, vectorization_name=self.vectorization_name
            )
        else:
            eval_set = data_storage.get_eval_set(
                used_features, vectorization_name=self.vectorization_name
            )
            x, y = eval_set["valid"][0], eval_set["valid"][1]

        if self.fitter.validation_type == ValidationType.CV:
            importance = make_cv_importance(
                models,
                x,
                y,
                self.fitter.cv,
                splitter_df=data_storage.get_cv_splitter_df(
                    self.fitter.cv.get_required_columns()
                ),
                metric=self.eval_metric,
            )
        elif self.fitter.validation_type == ValidationType.HOLDOUT:
            importance = make_ho_importance(
                x,
                y,
                estimator=model,
                metric=self.eval_metric,
            )
        else:
            raise ValueError(
                f"Can't get importance function for validaton type = {self.fitter.validation_type.value}."
            )

        best_model_info = [model, 0, models, used_features, 0]
        thresholds = self.threshold
        thresholds = (
            thresholds if isinstance(thresholds, (tuple, list)) else [thresholds]
        )
        retrained = False
        for threshold in tqdm(thresholds):
            perm_features = select_subset_features(
                importance, self.remaining_features, threshold, self.top_n
            )
            if (len(perm_features) > 0) and (len(perm_features) < len(used_features)):
                estimator = self._init_model(perm_features, model.params)
                perm_model, estimators, predictions = self.fitter.train(
                    estimator=estimator,
                    data_storage=data_storage,
                    metric=self.eval_metric,
                    used_features=perm_features,
                    sampling_flag=self.sampling_flag,
                    vectorization_name=self.vectorization_name,
                )

                perm_score = self.eval_metric(y, predictions)

                model_info = (
                    perm_model,
                    perm_score,
                    estimators,
                    perm_features,
                    threshold,
                )
                if best_model_info[1] < model_info[1]:
                    best_model_info = model_info

                retrained = True

        logger = CombinedLogger([self._logger, _logger])

        if retrained:
            old_num_features = len(used_features)
            new_num_features = len(best_model_info[3])
            logger.info(
                f"\033[7mС помощью перестановок с порогом {self.threshold} отброшено "
                f"{old_num_features-new_num_features} фичей\n"
                f"Количество отобранных фичей: {new_num_features}\033[0m"
            )
        else:
            logger.info(
                f"\033[7mС помощью перестановок с порогом {self.threshold} ни одной фичи отброшено не было\033[0m"
            )
        self.used_features = best_model_info[3]
        self.final_model = best_model_info[0]
        self.feature_importance = importance
        self.prediction = self.prediction_out(data_storage)
        self.models = best_model_info[2]

        return self


def make_cv_importance(
    estimators: list,
    x,
    y,
    cv: BaseCrossValidator,
    splitter_df: pd.DataFrame,
    metric: BaseMetric,
):
    """
    Отбор признаков на permutation-importance с кросс-валидацией.

    Parameters
    ----------
    estimators: List[dreamml_modelling.models]
        Список с экземплярами обученных моделей.

    cv: sklearn.model_selection.generator
        Генератор для разбиения данных в рамках кросс-валидации.

    x: pandas.DataFrame
        Матрица признаков.

    y: pandas.Series
        Вектор целевой переменной.

    metric: BaseMetric

    Returns
    -------
    importance: pd.DataFrame
        Датафрейм со значением Permutation Importance.

    """
    importance = pd.DataFrame()

    x = x.reset_index(drop=True)
    y = y.reset_index(drop=True)

    for fold_number, (train_index, valid_index) in enumerate(cv.split(splitter_df)):
        x_train, x_valid = x.loc[train_index], x.loc[valid_index]
        y_train, y_valid = y.loc[train_index], y.loc[valid_index]
        fold_importance = calculate_permutation_feature_importance(
            estimator=estimators[fold_number],
            metric=metric,
            maximize=metric.maximize,
            data=x_valid,
            target=y_valid,
            fraction_sample=0.8,
        )
        importance = pd.concat([importance, fold_importance], axis=0)

    importance = (
        importance.groupby(["feature"])["permutation_importance"].mean().reset_index()
    )
    importance = importance.sort_values(by="permutation_importance", ascending=False)

    return importance


def make_ho_importance(
    data,
    target,
    estimator: BoostingBaseModel,
    metric: BaseMetric,
):
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
    importance = calculate_permutation_feature_importance(
        estimator=estimator,
        metric=metric,
        maximize=metric.maximize,
        data=data,
        target=target,
        fraction_sample=0.8,
    )

    return importance