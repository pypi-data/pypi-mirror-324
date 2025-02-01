"""
Модуль с реализацией функций для работы с категориальными признаками.

Доступные сущности:
- find_categorical_features: функция для поиска категориальных признаков в
    заданном наборе данных.
- encode_categorical: применение CategoricalEncoder для каждой выборки.

=============================================================================

"""

from .categorical_encoder import CategoricalFeaturesTransformer


def encode_categorical(config, **eval_sets):
    """
    Применение CategoricalEncoder для каждого набора данных в eval_sets.

    Parameters
    ----------
    config: dict
        Конфигурационный файл.

    eval_sets: Dict[string, Tuple[pandas.DataFrame, pandas.Series]]
        Словарь с выборками, для которых требуется рассчитать статистику.
        Ключ словаря - название выборки (train / valid / ...), значение -
        кортеж с матрицей признаков (data) и вектором ответов (target).

    Returns
    -------
    eval_sets: Dict[string, Tuple[pandas.DataFrame, pandas.Series]]
        Преобразованный eval_sets.

    """
    transformer = CategoricalFeaturesTransformer(config)
    train = transformer.fit_transform(eval_sets["train"][0])
    eval_sets["train"] = (train, eval_sets["train"][1])

    transformed_samples = [name for name in eval_sets if name != "train"]
    for sample in transformed_samples:
        df = transformer.transform(eval_sets[sample][0])
        eval_sets[sample] = (df, eval_sets[sample][1])

    return eval_sets, transformer