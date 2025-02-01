import numpy as np
import pandas as pd
from tqdm.auto import tqdm
from sklearn.model_selection import train_test_split
from typing import Union, Optional, List

from dreamml.modeling.metrics import BaseMetric
from dreamml.modeling.models.estimators import BoostingBaseModel


def select_subset_features(
    features_imp: pd.DataFrame,
    remaining_features: List[str] = [],
    threshold_value: Union[float, int] = None,
    top_k: Optional[int] = None,
) -> list:
    """
    Функция для отбора признаков.
    Отбор признаков осуществляется на основе меры важностей признаков.
    Если задан threshold_value - то отбор производится по порогу меры
    важности (остаются признаки, мера важности которых выше заданного
    порога), если задан top_k - то отбираются top-k признаков по
    заданной мере важности.

    Parameters:
    -----------
    features_imp: pandas.DataFrame, shape = [n_features, 2]
        Матрица с оценкой важности признаков.

    remaining_features: List[str], default=[]
        Признаки, которые в любом случае должны остаться в датасете после отбора

    threshold_value: float / int, optional, default = None.
        Пороговое значение меры важности признаков.

    top_k: int, optional, default = None.
        Максимальное количество признаков.

    Returns:
    --------
    used_features: list
        Список используемых признаков.

    """
    col_name = [col for col in features_imp.columns if "importance" in col][0]
    if top_k:
        valid_features = features_imp.head(n=top_k)
    elif threshold_value:
        valid_features = features_imp[features_imp[col_name] > threshold_value]
    else:
        message = (
            "Incorrect params. Set the params: threshold_value / top_k."
            f"Current params: threshold_value = {threshold_value}, "
            f"top_k = {top_k}."
        )
        raise ValueError(message)

    needed_columns = [
        col for col in remaining_features if col not in valid_features.columns
    ]
    valid_features = pd.concat(
        [valid_features, features_imp[features_imp["feature"].isin(needed_columns)]],
        axis=0,
    )
    valid_features = valid_features[~valid_features["feature"].duplicated(keep="first")]
    return valid_features["feature"].tolist()


def calculate_permutation_feature_importance(
    estimator: BoostingBaseModel,
    metric: BaseMetric,
    data: pd.DataFrame,
    target: pd.Series,
    fraction_sample: float = 0.8,
    maximize: bool = True,
) -> pd.DataFrame:
    """
    Функция для расчета важности переменных на основе перестановок.
    Подход к оценке важности признаков основан на изменении метрики
    при перемешивании значений данного признака. Если значение метрики
    уменьшается, значит признак важен для модели, если значение метрики
    увеличивается, то признак для модели не важен и его стоит исключить.

    Parameters
    ----------
    estimator: BoostingBaseModel
        Экземпляр модели, которая поддерживает API sklearn.
        Ожидается, что модель обучена, т.е. был вызван метод fit ранее.

    metric: BaseMetric
        Функция для оценки качества модели.

    data: pandas.DataFrame
        Матрица признаков.

    target: pandas.Series
        Вектор целевой переменной.

    fraction_sample: float, optional, default = 0.15
        Доля наблюдений от data для оценки важности признаков.

    maximize: boolean, optional, default = True
        Флаг максимизации метрики. Означает, что чем выше значение метрики,
        тем качественее модель. Опциональный параметр, по умолчанию, равен True.

    Returns
    --------
    df: pd.DataFrame
        Преобразованная матрица признаков.

    """
    if not isinstance(data, pd.DataFrame):
        raise TypeError(
            f"data must be pandas.core.DataFrame, " f"but data is {type(data)}"
        )

    if fraction_sample < 0 or fraction_sample > 1:
        raise ValueError(
            f"fraction_sample must be in range [0, 1], "
            f"but fraction_sample is {fraction_sample}"
        )
    elif 0 < fraction_sample < 1:
        # FIXME: some classes in multiclass may be missing after split
        x, _, y, _ = train_test_split(
            data, target, train_size=fraction_sample, random_state=1
        )
        if isinstance(y, pd.DataFrame):
            for column_name in y:
                if y[column_name].nunique() != 2:
                    raise ValueError(
                        f"stage permutation, in the sample not all classes are in target"
                    )

    else:  # fraction_sample = 0 or fraction_sample = 1
        x = data
        y = target

    baseline_prediction = estimator.transform(x)

    baseline_score = metric(y, baseline_prediction)

    x_copy = x.copy(deep=True)

    feature_importance = np.zeros(x.shape[1])
    pbar = tqdm(x.columns)
    for num, feature in enumerate(pbar):
        pbar.set_postfix(feature=feature)

        x[feature] = np.random.permutation(x[feature])
        score = metric(y, estimator.transform(x))

        feature_importance[num] = score
        x[feature] = x_copy[feature]

    if maximize:
        feature_importance = 1 - feature_importance / baseline_score
    else:
        feature_importance = feature_importance / baseline_score - 1

    df = pd.DataFrame(
        {"feature": x.columns, f"permutation_importance": feature_importance}
    )
    df = df.sort_values(by=f"permutation_importance", ascending=False)
    df = df.reset_index(drop=True)

    return df