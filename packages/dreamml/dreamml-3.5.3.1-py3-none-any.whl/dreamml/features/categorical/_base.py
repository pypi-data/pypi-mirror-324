import numpy as np
import pandas as pd


def find_categorical_features(data: pd.DataFrame, config: dict) -> np.array:
    """
    Функция поиска категориальных переменных в датасете.
    Поиск осуществляется по типам: к категориальным признакам
    относятся колонки типа object / category, кроме колонок,
    которые указанные как drop_features.

    Parameters
    ----------
    data: pandas.DataFrame
        Матрица признаков.

    config: dict, optional, default = config_file
        Словарь с конфигурацией запуска кернела.

    Returns
    -------
    cat_features: numpy.array
        Список категориальных признаков.

    """
    task = config["task"]
    target_name = config["target_name"]

    categorical_features = config.get("categorical_features", [])
    text_cols = config.get("text_features", [])

    object_cols = data.dtypes[data.dtypes == "object"].index.tolist()
    category_cols = data.dtypes[data.dtypes == "category"].index.tolist()

    for feature in object_cols + category_cols:
        if feature not in categorical_features + text_cols:
            categorical_features.append(feature)

    if task == "multiclass" and target_name not in categorical_features:
        categorical_features.append(target_name)

    elif task != "multiclass" and target_name in categorical_features:
        msg = f"For a {task} task, the target must be in int or float format, but got: {data[target_name].dtype}."
        raise ValueError(msg)

    return np.unique(categorical_features).tolist()