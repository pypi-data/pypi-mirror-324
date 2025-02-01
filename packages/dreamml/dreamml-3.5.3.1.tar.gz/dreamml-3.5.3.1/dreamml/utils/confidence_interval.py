from collections.abc import Callable

import numpy as np
import pandas as pd
from scipy import stats
from typing import Union, Optional

from dreamml.modeling.metrics import BaseMetric


def create_bootstrap_index(
    df: pd.DataFrame,
    bootstrap_samples: int = 200,
    random_seed: Optional[int] = None,
    task: str = "binary",
    target: Optional[Union[pd.Series, np.array]] = None,
) -> np.array:
    """
    Создание матрицы индексов объектов, попавших в бутстреп-выборку.

    Parameters
    ----------
    df: pandas.core.frame.DataFrame
        Матрица признаков для создания бутстреп-объектов.

    bootstrap_samples: int
        Количество бутстреп-объектов.

    random_seed: int
        Seed для генератора случайных чисел.

    task: str
        Тип задачи

    target: Optional[Union[pd.Series, np.array]]


    Returns
    -------
    bootstrap_index: np.array
        Матрица индексов бутстреп объектов.

    """
    if random_seed is not None:
        np.random.seed(random_seed)

    if task == "multilabel":
        if target is None:
            raise ValueError(
                "Target is required for bootstrap sampling as all classes have to be presented in samples."
            )
        bootstrap_index = np.empty((bootstrap_samples, 0), dtype=int)
        target = target.reset_index(drop=True)

        # В выборке должны быть наблюдения каждого класса
        for target_class, cnt in target.value_counts().to_frame().iterrows():
            cnt = int(cnt)
            bootstrap_index = np.append(
                bootstrap_index,
                np.random.choice(
                    target[target == target_class].index, size=(bootstrap_samples, cnt)
                ),
                axis=-1,
            )
        return bootstrap_index
    else:
        bootstrap_index = np.random.randint(
            0, df.shape[0], size=(bootstrap_samples, df.shape[0])
        )
        return bootstrap_index


def create_bootstrap_scores(
    x: pd.DataFrame,
    y: pd.Series,
    y_pred: pd.Series,
    metric: Callable,
    bootstrap_samples: int = 200,
    random_seed: int = 27,
    task: Optional[str] = None,
) -> np.array:
    """
    Вычисление метрики качества на каждой бутстреп выборке.

    Parameters
    ----------
    x: pandas.core.frame.DataFrame
        Матрица признаков для создания бутстреп-объектов.

    y: pandas.core.frame.Series
        Вектор целевой переменной.

    y_pred: pandas.core.frame.Series
        Вектор предсказаний модели.

    metric: BaseMetric
        Функция для расчета метрики.

    bootstrap_samples: int
        Количество бутстреп-объектов.

    random_seed: int
        Seed для генератора случайных чисел.

    task: str
        Тип решаемой задачи

    Returns
    -------
    bootstrap_scores: np.array
        Вектор с бутстрап оценками.

    """
    x = x.reset_index(drop=True)
    y = y.reset_index(drop=True) if isinstance(y, pd.DataFrame) else y

    if task not in (
        "multiclass",
        "multilabel",
    ):  # в этом случае предсказания - np.array([n_samples, n_classes])
        y_pred = pd.Series(y_pred)

    y_pred = (
        y_pred.reset_index(drop=True) if isinstance(y_pred, pd.DataFrame) else y_pred
    )

    bootstrap_scores = []
    bootstrap_index = create_bootstrap_index(
        x, bootstrap_samples, random_seed, task=task, target=y
    )

    y_pred = y_pred.values if isinstance(y_pred, (pd.Series, pd.DataFrame)) else y_pred
    y = y.values if isinstance(y, (pd.Series, pd.DataFrame)) else y

    for sample_idx in bootstrap_index:
        y_true_bootstrap, y_pred_bootstrap = y[sample_idx], y_pred[sample_idx]
        try:
            bootstrap_scores.append(metric(y_true_bootstrap, y_pred_bootstrap))
        except Exception as e:
            continue

    return np.array(bootstrap_scores)


def calculate_conf_interval(x: np.array, alpha: float = 0.05):
    """
    Вычисление доверительного интервала для среднего.

    Parameters
    ----------
    x: array-like, shape = [n_samples, ]
        Выборка для построения доверительного интервала.

    alpha: float, optional, default = 0.05
        Уровень доверия.

    Returns
    -------
    conf_interval: Tuple[float, float]
        Границы доверительного интервала.

    """
    # coorrect way?
    # x_mean = np.mean(x)
    # x_std = np.std(x, ddof=1)
    # n = len(x)
    # t_value = stats.t.ppf(1 - alpha / 2, n - 1)
    # std_error = x_std / np.sqrt(n)
    #
    # lower_bound = x_mean - t_value * std_error
    # upper_bound = x_mean + t_value * std_error

    # return lower_bound, upper_bound

    x_mean = np.mean(x)
    q_value = stats.t.ppf(1 - alpha / 2, x.shape[0])

    std_error = q_value * np.sqrt(x_mean) / np.sqrt(x.shape[0])

    return x_mean - std_error, x_mean + std_error