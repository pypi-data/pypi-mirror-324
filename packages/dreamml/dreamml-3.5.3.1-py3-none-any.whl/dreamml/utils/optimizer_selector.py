import pandas as pd
from typing import List, Optional
from dreamml.data._dataset import DataSet


def optimizer_selector(
    data_storage: DataSet,
    used_features: List = None,
    vectorization_name: Optional[str] = None,
) -> str:
    """
    Функция возвращающая метод оптимизации в зависимости от размера обучающей и валидационной выборок

    Parameters
    ----------
    data_storage: DataSet
        Экземпляр класса-хранилища данных

    used_features: List
        Список используемых признаков.

    vectorization_name: Optional[str]
        Алгоритм векторизации

    Returns
    -------
    optimizer: str
        Способ оптимизации
        optimizer == "distributed" - будет выбрана папйплайн основанный на кросс-валидации
        optimizer == "local" - будет выбран пайплайн основанный на разбиение обучающей выборки на train/valid/test

    """
    data = data_storage.get_eval_set(
        used_features, vectorization_name=vectorization_name
    )
    train_size = data.get("train", pd.DataFrame())[0].memory_usage(deep=True).sum()
    train_size = round(train_size / 1024 / 1024, 2)
    valid_size = data.get("valid", pd.DataFrame())[0].memory_usage(deep=True).sum()
    valid_size = round(valid_size / 1024 / 1024, 2)

    total_size = train_size + valid_size
    if total_size > 1024:
        return "local"
    else:
        return "distributed"