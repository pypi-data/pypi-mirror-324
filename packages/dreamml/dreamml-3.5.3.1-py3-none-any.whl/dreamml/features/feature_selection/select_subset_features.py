import pandas as pd
from typing import Union, Optional, List


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

    needed_columns = [col for col in remaining_features if col not in valid_features]
    valid_features = pd.concat(
        [valid_features, features_imp[features_imp["feature"].isin(needed_columns)]],
        axis=0,
    )
    valid_features = valid_features[~valid_features["feature"].duplicated(keep="first")]
    return valid_features["feature"].tolist()


def select_subset_features_reverse(
    features_imp: pd.DataFrame,
    remaining_features: List[str] = [],
    bot_k: Optional[int] = None,
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

    bot_k: int, optional, default = None.
        Количество отбираемых признаков.

    Returns:
    --------
    used_features: list
        Список используемых признаков.

    """
    if bot_k:
        valid_features = features_imp.iloc[:-bot_k]
    else:
        message = "Incorrect params. Set the params: bot_k." f"top_k = {bot_k}."
        raise ValueError(message)

    needed_columns = [
        col for col in remaining_features if col not in valid_features.columns
    ]
    valid_features = pd.concat(
        [
            valid_features,
            features_imp[features_imp["feature-name"].isin(needed_columns)],
        ],
        axis=0,
    )
    valid_features = valid_features[
        ~valid_features["feature-name"].duplicated(keep="first")
    ]
    return valid_features["feature-name"].tolist()