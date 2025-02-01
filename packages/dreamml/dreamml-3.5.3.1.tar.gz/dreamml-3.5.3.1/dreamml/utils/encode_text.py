from copy import deepcopy
from typing import List

from dreamml.configs.config_storage import ConfigStorage
from dreamml.logging import get_logger
from dreamml.features.text._base import TextFeaturesTransformer

_logger = get_logger(__name__)


def encode_text(config: ConfigStorage, dev_data, oot_data, indexes, augs, aug_p):
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
    text_preprocessing_stages: List[str] = config.text_preprocessing_stages
    vectorization_algos = config.vectorization_algos
    bert_anonimization = False

    if len(vectorization_algos) == 1 and vectorization_algos[0] in ["bert", "bertopic"]:
        if "anonimization" in text_preprocessing_stages:
            text_preprocessing_stages = ["anonimization", "lemmatization"]
            bert_anonimization = True
        else:
            text_preprocessing_stages = []
        msg = f"text_preprocessing_stages set to {text_preprocessing_stages} for bert / bertopic."
        _logger.info(msg)

    augs_flag = False
    dev_data_shape_before = dev_data.shape
    if "augmentation" in text_preprocessing_stages and augs:
        augs_flag = True

    encoder_conf = {
        "text_preprocessing_stages": text_preprocessing_stages,
        "text_features": deepcopy(config.text_features),
        "drop_features": deepcopy(config.drop_features),
        "indexes": deepcopy(indexes),
        "augs": augs,
        "aug_p": aug_p,
        "bert_anonimization": bert_anonimization,
    }

    transformer = TextFeaturesTransformer(encoder_conf)
    transformer.fit(dev_data)
    dev_data, indexes = transformer.transform(dev_data, apply_augs_flag=augs_flag)

    if oot_data is not None:
        oot_data, _ = transformer.transform(oot_data)
        if augs_flag and "_group_nlp_aug_field" not in oot_data.columns:
            oot_data["_group_nlp_aug_field"] = oot_data.index.tolist()

    # -- logs --
    if augs_flag:
        dev_data_shape_after = dev_data.shape
        diff = dev_data_shape_after[0] - dev_data_shape_before[0]
        ratio = dev_data_shape_after[0] / dev_data_shape_before[0]
        _logger.debug(f"dev_data shape before augs: {dev_data_shape_before}")
        _logger.debug(f"dev_data shape after augs: {dev_data_shape_after}")
        _logger.debug(f"diff: {diff} | ratio: {round(ratio * 100, 2)}%")

    return dev_data, oot_data, transformer, indexes