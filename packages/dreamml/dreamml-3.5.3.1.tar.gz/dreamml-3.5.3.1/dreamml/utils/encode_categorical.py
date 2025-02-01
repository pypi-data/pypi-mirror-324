from copy import deepcopy
import pandas as pd

from dreamml.features.categorical.categorical_encoder import (
    CategoricalFeaturesTransformer,
)
from dreamml.configs.config_storage import ConfigStorage


def encode_categorical(
    config: ConfigStorage,
    dev_data: pd.DataFrame,
    oot_data: pd.DataFrame,
    indexes: tuple,
):
    """
    Применение CategoricalEncoder для каждого набора данных в eval_sets.

    Parameters
    ----------
    config
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
    train_idx, valid_idx = indexes[0], indexes[1]
    train_valid = dev_data.loc[train_idx]
    train_valid = train_valid.append(dev_data.loc[valid_idx])

    encoder_conf = {
        "categorical_features": deepcopy(config.categorical_features),
        "text_features": deepcopy(config.text_features),
        "target_name": config.target_name,
        "time_column": config.time_column,
        "task": config.task,
    }

    transformer = CategoricalFeaturesTransformer(encoder_conf)
    _ = transformer.fit(dev_data)

    dev_data = transformer.transform(dev_data)
    if oot_data is not None:
        oot_data = transformer.transform(oot_data)

    return dev_data, oot_data, transformer