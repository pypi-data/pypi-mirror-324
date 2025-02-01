from copy import deepcopy
from pathlib import Path
from typing import Tuple, Dict, Optional

import pandas as pd

from dreamml.logging import get_logger
from dreamml.utils.spark_init import init_spark_env
from dreamml.utils.temporary_directory import TempDirectory
from dreamml.data.exceptions import ColumnDoesntExist


DISTRIBUTED = "distributed"
DREAMML_PATH = Path(__file__).parent.parent
NEVER_USED_FEATURES_PATH = DREAMML_PATH / "references" / "never_used_features.txt"

_logger = get_logger(__name__)


def get_base_config() -> dict:
    try:
        with open(NEVER_USED_FEATURES_PATH, "r") as file:
            never_used_features = file.readlines()
    except FileNotFoundError as e:
        _logger.warning(
            f"{e} - Файл с названиями неиспользуемых признаков ({NEVER_USED_FEATURES_PATH}) не найден."
        )
        never_used_features = []

    base_config = {
        "data_path": "../data",
        "runs_path": "../results/",
        "never_used_features": never_used_features,
        "categorical_features": None,
        # параметры разбиения данных на train / valid / test
        "split_params": [0.6, 0.2, 0.2],
        "group_column": "",
        "sort": None,
        # максимально допустимые отклонения в метрике качества и выборка для расчета
        "absolute_diff": 15,
        "relative_diff": 25,
        "valid_sample": "valid",
        # порог для отбора признаков по PSI и выборка для расчета PSI
        "psi_threshold": 0.1,
        "psi_sample": "valid",
        # порог для отбора признаков по метрике Джини
        "gini_threshold": 2,
        "gini_absolute_diff": 10,
        "gini_relative_diff": 30,
        # порог для отбора признаков на основе перестановок (см. документацию подробнее)
        "permutation_threshold": 0.01,
        # количество итераций оптимизатора гиперпараметров моделей
        "n_iterations": 20,
        # Флаг использования WhiteBox AutoML
        "use_whitebox_automl": True,
        # Объект создания временной папки
        "temp_dir": TempDirectory(),
    }
    return base_config


def _check_config(config: dict) -> dict:
    """
    Проверка значений конфигурационного файла.

    Parameters
    ----------
    config: dict
        Конфигурационный файл из Jupyter Notebook DreamML.
        Заполняется пользователем.

    Returns
    -------
    config: dict
        Полный конфигурационный файл DreamML.

    """
    base_config = get_base_config()
    _missed_params = list(set(base_config.keys()) - set(config.keys()))
    update_config = {key: base_config[key] for key in _missed_params}
    config_ = deepcopy(config)
    config_.update(update_config)
    if config_.get("optimizer") == DISTRIBUTED:
        init_spark_env()
    return config_


def prediction_out(model, eval_sets: Dict[str, Tuple[pd.DataFrame, pd.Series]]):
    """
    Возращает значения для переменных prediction_dict

    Parameters
    ----------
    model: экземпляр класса
    eval_sets: Dict[string, Tuple[pd.DataFrame, pd.Series]]
        Словарь, где ключ - название выборки, значение - кортеж с
        матрицей признаков и вектором истинных ответов.
    """

    prediction_dict = {}

    for sample in eval_sets:
        data, target = eval_sets[sample]
        prediction = model.transform(data)
        prediction_dict[sample] = prediction
    return prediction_dict


def get_sample_frac(shape: int) -> int:
    """
    Возвращает размер сэмлированной выборки в зависимости от размера тренировачного сета.

    Parameters
    ----------
    param shape: Размер тренировочной выборкию
    return: Размер новой сэмплированной выборки.
    """
    dict_of_shapes_and_fractions = {
        200000: 0.7,
        400000: 0.6,
        600000: 0.5,
    }

    sample_frac = 1

    for key, value in dict_of_shapes_and_fractions.items():
        if shape > key:
            sample_frac = value

    return int(sample_frac * shape)


def check_column_in_data(
    column_name: str, data: pd.DataFrame, msg: str = None
) -> Optional[Exception]:
    """
    Проверяет наличие колонки в датафрейме

    Parameters
    ----------
    column_name: Название колонки
    data: Датафрейм pd.DataFrame
    msg: Опциональное сообщение, которое можно выводить вместо дефолтного на экран
    """
    if column_name not in data.columns:
        raise ColumnDoesntExist(column_name, data, msg)