from pyspark import SparkConf
from ..utils.spark_session_configuration import spark_conf


def get_hyperopt_spark_conf(local_dir: str) -> SparkConf:
    """
    Функция создания конгфигурация спарка для распределённого оптимизатора hyperopt

    Parameters
    ----------
    local_dir: str
        Путь до временной папки

    Returns
    -------
    hyperopt_spark_conf: SparkConf
        Конифгурации для запуска спарк сессии для распределённого оптимизатора
    """

    hyperopt_spark_conf = spark_conf
    hyperopt_spark_conf.set("spark.local.dir", local_dir)
    return hyperopt_spark_conf