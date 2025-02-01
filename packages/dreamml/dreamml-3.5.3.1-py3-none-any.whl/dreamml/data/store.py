"""
Модуль с реализацией сущностей для взаимодействия с хранилищем данных.

Доступные сущности:
- get_input: функция для загрузки данных.
- save_data: функция для сохранения данных на диск.

=============================================================================

"""

import os
import pickle
import time
from typing import Union, Tuple, Optional

import pandas as pd
import pyspark
from pandas import DataFrame
from pyspark.sql import SparkSession

from dreamml.configs.config_storage import ConfigStorage
from dreamml.data._hadoop import (
    get_hadoop_input,
    get_hadoop_sql_input,
    get_hadoop_parquet_input,
)
from dreamml.logging import get_logger
from dreamml.logging.monitoring import DataLoadedLogData

_logger = get_logger(__name__)


def _compress_datatypes(X: pd.DataFrame) -> pd.DataFrame:
    """
    Сжатие типов данных во входных данных.
    Типы int64 сжимаются в int32, типы float64 сжимаются во float32.

    Parameters
    ----------
    X: pandas.core.frame.DataFrame
        Матрица входных данных.

    Returns
    -------
    X_compressed: pandas.core.frame.DataFrame
        Матрица входных данных с сжатыми типами данных.

    """
    usage_before = X.memory_usage(deep=True).sum()
    usage_before = round(usage_before / 1024 / 1024, 2)
    int64 = X.dtypes[X.dtypes == "int64"].index  # int32: (-2147483648; 2147483647)
    int64 = X[int64].max()[X[int64].max() <= 2147483647].index
    int64 = X[int64].min()[X[int64].min() >= -2147483648].index
    float64 = X.dtypes[X.dtypes == "float64"].index  # float32: (-3,4e+38; 3.4e+38)

    X[int64] = X[int64].astype("int32")
    X[float64] = X[float64].astype("float32")
    usage_after = X.memory_usage(deep=True).sum()
    usage_after = round(usage_after / 1024 / 1024, 2)

    _logger.info("Data is compressed to 32bit types.")
    _logger.debug(
        f"Memory usage before compression = {usage_before} Mb, after compression = {usage_after} Mb."
    )
    return X


def create_old_dict_compat(config: ConfigStorage) -> dict:
    """
    Функция для сохранения обратной совместимости с другими модулями DreamML, которые не перешли на использование
    ConfigStorage
    Parameters
    ----------
    config: ConfigStorage
        Конфигурации эксперимента
    Returns
    -------
    conf: dict
        Словарь с конфигурациями эксперимента
    """
    compat_config = {
        "dev_data_path": config.dev_data_path,
        "oot_data_path": config.oot_data_path,
        "train_data_path": config.train_data_path,
        "valid_data_path": config.valid_data_path,
        "test_data_path": config.test_data_path,
        "multitarget": config.multitarget,
        "target_name": config.target_name,
        "drop_features": config.drop_features,
        "never_used_features": config.never_used_features,
        "time_column": config.time_column,
        "task": config.task,
        "path_to_exog_data": config.path_to_exog_data,
    }

    if config.data_path is not None:
        compat_config["data_path"] = config.data_path

    return compat_config


def get_input(
    spark: Optional[SparkSession], data_path: str, config: Union[ConfigStorage, dict]
) -> Tuple[DataFrame, None]:
    """
    Загрузка входных данных из файла data_path.
    Загрузка возможных с диска (.csv / .pkl), из TeraData, из Hadoop.

    Parameters
    ----------
    spark: SparkSession
        Объект текущей Spark сессии

    data_path: string
        Ключ в config, по которому расположен путь до выборки с данными.

    config: ConfigStorage
        Главный конфигурационный объект DreamML.
        Обратная совместимость - Либо словарь dict для модулей, не обновлённых под релиз 2.0

    Returns
    -------
    data_x_y: Tuple[x: pd.DataFrame, y: Union[pd.Series, pd.DataFrame]]
        x: Датафрейм с данными для тренировки
        y:
        - Значения одной целевой переменной в виде pd.Series
        - Значения нескольких целевых переменных в виде pd.DataFrame,
        если задан параметр multitarget в config
    """
    start_time = time.time()

    use_compression = config.get("use_compression", False)
    if isinstance(config, ConfigStorage):
        config = create_old_dict_compat(config)

    drop_features = config.get("drop_features", []) + config.get(
        "never_used_features", []
    )

    file_name = config.get(data_path)

    if file_name is None:
        raise ValueError(f"Incorrect path to {data_path} data.")
    elif file_name.rsplit(".", 1)[-1] == "csv":
        data = pd.read_csv(file_name)
    elif file_name.rsplit(".", 1)[-1] == "pkl":
        data = pd.read_pickle(file_name)
    elif file_name.rsplit(".", 1)[-1] == "pickle":
        data = pd.read_pickle(file_name)
    elif file_name.rsplit(".", 1)[-1] == "parquet":
        data = pd.read_parquet(file_name)
    elif file_name.rsplit(".", 1)[-1] == "xlsx":
        data = pd.read_excel(file_name)
    elif "select " in file_name.lower():
        data = get_hadoop_sql_input(
            spark=spark, path=file_name, drop_features=drop_features
        )
    elif file_name.rsplit(":", 1)[0] == "hdfs":
        data = get_hadoop_parquet_input(
            spark=spark, path=file_name, drop_features=drop_features
        )
    else:
        try:
            data = get_hadoop_input(
                spark=spark, path=file_name, drop_features=drop_features
            )
        except (NameError, FileNotFoundError) as e:
            raise NameError(
                f"DreamML supports only formats: .csv, .pkl, .pickle, .parquet, database.table or sql ("
                f"HiveQl)\n"
            ) from e

    if use_compression:
        data = _compress_datatypes(data)

    if config.get("path_to_exog_data") is not None:
        return data, None

    target_name = config.get("target_name")

    # train_data_path -> train_data
    data_type_name = data_path
    if data_type_name.endswith("_path"):
        data_type_name = data_type_name[: -len("_path")]

    elapsed_time = time.time() - start_time
    _logger.monitor(
        f"Loaded {data_type_name} with shape {data.shape}.",
        extra={
            "log_data": DataLoadedLogData(
                name=data_type_name,
                length=len(data),
                features_num=data.shape[1],
                nan_count=data.isna().sum().sum(),
                elapsed_time=elapsed_time,
            )
        },
    )

    if "data_path" in config:
        save_data(
            data,
            data_type_name=data_type_name,
            target_name=target_name,
            save_path=config["data_path"],
            task=config["task"],
            target_label_encoder=config.get("target_label_encoder", True),
        )

    # У валидаторов есть тест на наличие столбца index
    # этот столбец нужен, так как при загрузке-выгрузке с hadoop бывало, что терялись некоторые строчки
    if "index" in data.columns:
        data = data.reset_index(drop=True)
    else:
        data = data.reset_index()

    multitarget = config.get("multitarget")
    if multitarget:
        target_name = [target_name] + multitarget
    #     В таком случае будет возвращён DataFrame

    if target_name is None:
        return data, None

    return data, data[target_name]


def save_data(
    data,
    data_type_name: str,
    target_name: None,
    save_path: str,
    task: str,
    target_label_encoder: bool,
):
    """
    Сохранение данные и метаинформации данных в папку data.

    Механизм сохранения: осуществляется попытка создания папки
    data, если папка создана - то сохранить data, meta_data.
    Если папка создана не была, то считывать все meta_data и
    сравнивать с текущим набором данных, если data.shape
    совпал хотя бы с одним meta_data, то сохранение данных
    не производить. Если data.shape не совпал ни с одним
    meta_data, то сохранить данные.

    Parameters
    ----------
    data: pandas.DataFrame
        Набор данных для сохранения.

    data_type_name: string
        Название набора данных.

    target_name: str
        Название колонки с таргетом.

    save_path: str
        Путь до сохранения данных

    task: str
        Название задачи

    target_label_encoder: bool
        Флаг label encoding таргета

    """

    if task in ("binary", "multiclass", "multilabel"):
        target_mean = 0
    else:
        if target_name is None or data[target_name].dtype not in [int, float]:
            target_mean = 0
        else:
            target_mean = round(data[target_name].values.mean(), 4)

    raw_data_path = os.path.join(save_path, "raw")
    os.makedirs(raw_data_path, exist_ok=True)

    metadata_postfix = "_metadata"

    metadata = {
        "shape": data.shape,
        "target_mean": target_mean,
    }

    is_already_saved_data = False
    saved_metadata_names = [
        filename
        for filename in os.listdir(raw_data_path)
        if data_type_name in filename and metadata_postfix in data_type_name
    ]
    for filename in saved_metadata_names:
        saved_metadata_path = os.path.join(raw_data_path, filename)

        try:
            with open(saved_metadata_path, "rb") as f:
                meta_data = pickle.load(f)

            if meta_data == metadata:
                is_already_saved_data = True
                break
        except (ValueError, pickle.UnpicklingError):
            pass
        except Exception as e:
            _logger.exception(
                f"Unexpected error occured while processing {saved_metadata_path}: {e}"
            )

    if not is_already_saved_data:
        numeration_postfix = f"_{len(saved_metadata_names) + 1}"

        data_save_path = os.path.join(
            raw_data_path, data_type_name + numeration_postfix + ".pkl"
        )
        data.to_pickle(data_save_path)

        metadata_path = os.path.join(
            raw_data_path,
            data_type_name + metadata_postfix + numeration_postfix + ".pkl",
        )
        with open(metadata_path, "wb") as f:
            pickle.dump(metadata, f)