from copy import deepcopy
from typing import List, Union

import numpy as np
import pandas as pd

from dreamml.logging import get_logger
from dreamml.modeling.metrics import BaseMetric
from dreamml.modeling.models.estimators import BaseModel

_logger = get_logger(__name__)


def make_cv(
    estimator: BaseModel,
    x_train_cv,
    y_train_cv,
    cv,
    splitter_df: pd.DataFrame,
    metric: BaseMetric,
):
    """
    Функция для осуществления кросс-валидации, оценки метрики
    качества на кросс-валидации и подбор оптимального количества
    итераций обучения.

    Parameters
    ----------
    estimator: BaseModel
        Экземпляр модели для обучения.

    x_train_cv: pandas.core.frame.DataFrame
        Матрица признаков для обучения модели.

    y_train_cv: pandas.core.frame.Series
        Вектор целевой переменной для обучения модели.

    cv: dreamml.modeling.cv._cross_validators.BaseCrossValidator
        Генератор для осуществления кросс-валидации.

    splitter_df: pd.DataFrame
        Таблица, по которой будет проходить разбиение данных.

    metric: BaseMetric
        Метрика для оценки качества модели.

    Returns
    -------
    estimators: List[estimator]
        Список с обученными моделями.

    cv_score: float
        Среднее значение метрики качества на кросс-валидации.

    folds_score: List[float]
        Значение метрики качества на каждом фолде кросс-валидации.

    n_trees_: int
        Среднее значение количества итераций обучения на кросс-валидации.

    folds_trees_: List[int]
        Значение количества итераций обучения на каждом фолде кросс-валидации.

    """
    logger = estimator._logger or _logger
    task = estimator.task

    x_train_cv = x_train_cv.reset_index(drop=True)

    initial_y_indexes = y_train_cv.index
    y_train_cv = y_train_cv.reset_index(drop=True)

    if task == "multilabel":
        oof_predictions = pd.DataFrame(np.zeros_like(y_train_cv))
    elif task == "multiclass":
        oof_predictions = pd.DataFrame(
            np.empty((y_train_cv.shape[0], y_train_cv.nunique()))
        )
    else:
        oof_predictions = pd.Series(np.zeros_like(y_train_cv))

    estimators = []
    folds_score = []
    folds_trees_: Union[int, List[int]] = []

    for fold_number, (train_index, valid_index) in enumerate(cv.split(splitter_df)):
        logger.info(f"Cross-Validation, Fold {fold_number + 1}")
        y_pred, score, fold_estimator = fold_calculate(
            x_train_cv,
            estimator,
            metric,
            train_index,
            valid_index,
            y_train_cv,
        )

        folds_trees_.append(fold_estimator.best_iteration)
        estimators.append(fold_estimator)
        folds_score.append(score)

        oof_predictions.loc[valid_index] = y_pred

        logger.info(f"\nCV oof score: {round(score, 2)}")
        logger.info("*" * 111)

    oof_predictions.index = initial_y_indexes

    cv_score, cv_std = round(np.mean(folds_score), 5), round(np.std(folds_score), 5)
    logger.info(f"Total CV-score = {cv_score} +/- {cv_std}")
    logger.info("-" * 111)

    if isinstance(folds_trees_[0], int):
        mean_fold_trees = int(np.mean(folds_trees_))
    else:
        mean_fold_trees = [
            int(classifier_trees) for classifier_trees in np.mean(folds_trees_, axis=0)
        ]

    return (
        estimators,
        np.mean(folds_score),
        folds_score,
        mean_fold_trees,
        folds_trees_,
        oof_predictions,
    )


def fold_calculate(
    x_train_cv,
    estimator,
    metric: BaseMetric,
    train_index,
    valid_index,
    y_train_cv,
):
    x_train, x_valid = x_train_cv.loc[train_index], x_train_cv.loc[valid_index]
    y_train, y_valid = y_train_cv.loc[train_index], y_train_cv.loc[valid_index]
    fold_estimator = deepcopy(estimator)

    fold_estimator.fit(x_train, y_train, x_valid, y_valid)
    y_pred = fold_estimator.transform(x_valid)

    score = metric(y_pred=y_pred, y_true=y_valid)

    return y_pred, score, fold_estimator