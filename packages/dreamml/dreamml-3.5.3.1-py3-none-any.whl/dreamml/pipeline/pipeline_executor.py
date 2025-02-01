import pandas as pd


def choose_pipeline(data: dict) -> str:
    """
    Функция возвращающая метод валидации в зависимости от размера обучающей выборки
    Parameters
    ----------
    data: dict
        Словарь с данными. Ключ название выборки, значение кортеж с матрицей признаков (pd.DataFrame)
        и вектором целевой переменной (pd.Series)
    Returns
    -------
    validation: str
        Способ валидации
        validation == "cv" - будет выбрана папйплайн основанный на кросс-валидации
        validation == "hold-out" - будет выбран пайплайн основанный на разбиение обучающей выборки на train/valid/test

    """
    train_len = data.get("train", pd.DataFrame())[0].shape[0]
    valid_len = data.get("valid", pd.DataFrame())[0].shape[0]

    total_len = train_len + valid_len
    if total_len < 250000:
        return "cv"
    else:
        return "hold-out"