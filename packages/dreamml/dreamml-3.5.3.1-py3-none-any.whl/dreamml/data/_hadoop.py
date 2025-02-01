"""
Модуль с реализацией сущностей для взаимодействия с Hadoop.

Доступные сущности:
- create_spark_session: функция для создания Hive-сессии.
- get_hadoop_input: функция для получения данных из Hadoop в pandas.DataFrame
- prepare_dtypes: функция для приведения типов данных из pyspark.DataFrame в pandas.DataFrame.

=============================================================================

"""

import pandas as pd
import sys
from pyspark import SparkConf
from pyspark.sql import SparkSession

from dreamml.logging import get_logger
from ..utils.spark_session_configuration import spark_conf
from ..utils.spark_init import init_spark_env
from ..utils.temporary_directory import TempDirectory

_logger = get_logger(__name__)


def create_spark_session(
    spark_config: SparkConf = None, temp_dir: TempDirectory = None
) -> SparkSession:
    """
    Создание SparkSession.
    Если не заданы параметры спарковской сессии, то
    поднимается дефолтная спарковская сессия с предопределнными
    параметрами.

    Parameters
    ----------
    spark_config: pyspark.SparkConf
        Объект SparkConf для установки свойств spark.
    temp_dir: TempDirectory
        Название временной папки для сохранения промежуточных расходов

    Returns
    -------
    spark: pyspark.sql.SparkSession
        Сессия для выгрузки данных из Hive и HDFS.

    """
    _logger.info("Starting Spark session...")

    init_spark_env()

    if "user-venvs" in sys.executable:  # DataLab
        spark = (
            SparkSession.builder.config("spark.ui.enabled", "true")
            .config("spark.driver.memory", "2g")
            .config("spark.executor.instances", "2")
            .config("spark.executor.cores", "2")
            .config("spark.kubernetes.executor.limit.cores", "2")
            .config("spark.kubernetes.executor.request.cores", "1800m")
            .config("spark.executor.memory", "2g")
            .config("spark.executor.memoryOverhead", "100m")
            .config("spark.sql.parquet.compression.codec", "snappy")
            .config("spark.sql.execution.arrow.pyspark.enabled", "true")
            .getOrCreate()
        )
    else:
        if spark_config is None:
            spark_config = spark_conf

        if temp_dir is not None:
            tmp_dir_path = temp_dir.name
        else:
            tmp_dir_path = "dml_spark_temp_dir"

        spark_config.set("spark.local.dir", tmp_dir_path)
        spark = (
            SparkSession.builder.enableHiveSupport()
            .config(conf=spark_config)
            .getOrCreate()
        )

    _logger.info("Spark session is started!")

    return spark


def stop_spark_session(spark: SparkSession, temp_dir: TempDirectory = None):
    """
    Останавливает Spark-сессию,
    очищает временную папку

    Parameters
    ----------
    spark: pyspark.sql.session.SparkSession
        Объект текущей Spark сессии
    temp_dir: TempDirectory
        Объект для очищения временной папки
    """
    spark.stop()

    if temp_dir is not None:
        temp_dir.clear()

    _logger.info("Spark session is stopped.")


def get_hadoop_input(spark, path: str, drop_features=None) -> pd.DataFrame:
    """
    Выгрузить данные из Hadoop.

    Parameters
    ----------
    spark: pyspark.sql.session.SparkSession
        Сессия для выгрузки данных из Hive и HDFS.
    path: string
        Путь до данных / SQL-запрос для выгрузки данных.
    Returns
    -------
    data: pandas.DataFrame
        Набор данных.

    """
    data = spark.table(path)
    data = data.toPandas()
    data = prepare_dtypes(data, drop_features)

    return data


def get_hadoop_sql_input(spark, path: str, drop_features=None) -> pd.DataFrame:
    """
    Выгрузить данные из Hadoop с помощью SQL-запроса.

    Parameters
    ----------
    spark: pyspark.sql.session.SparkSession
        Сессия для выгрузки данных из Hive и HDFS.
    path: string
        SQL-запрос для выгрузки данных.
    Returns
    -------
    data: pandas.DataFrame
        Набор данных.

    """
    path = path.replace(";", "")
    data = spark.sql(path)
    data = data.toPandas()
    data = prepare_dtypes(data, drop_features)

    return data


def get_hadoop_parquet_input(spark, path: str, drop_features=None) -> pd.DataFrame:
    """
    Выгрузить данные из Hadoop из папки с parquet.

    Parameters
    ----------
    spark: pyspark.sql.session.SparkSession
        Сессия для выгрузки данных из Hive и HDFS.
    path: string
        Путь до папки с parquet
    Returns
    -------
    data: pandas.DataFrame
        Набор данных.

    """
    data = spark.read.format("parquet").load(path)
    data = data.toPandas()
    data = prepare_dtypes(data, drop_features)

    return data


def prepare_dtypes(df: pd.DataFrame, drop_features=None):
    """
    Приведение типов данных.

    Parameters
    ----------
    df: pyspark.DataFrame
        Набор данных в pyspark.

    Returns
    -------
    df_transformed: pd.DataFrame
        Набор данных в pandas.

    """
    if drop_features is None:
        drop_features = []
    obj_features = df.dtypes[df.dtypes == "object"].index

    cannot_cast_features = []
    for feature in obj_features:
        if feature in drop_features:
            continue

        try:
            df[feature] = df[feature].astype(float)
        except (ValueError, TypeError) as e:
            cannot_cast_features.append(feature)

    _logger.warning(
        f"Can't cast to float the following 'object' features: {cannot_cast_features}"
    )

    return df