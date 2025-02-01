from pyspark import SparkConf
from pyspark.sql import SparkSession

from dreamml.utils.spark_session_configuration import spark_conf


def create_spark_session(conf: SparkConf = None) -> SparkSession:
    if conf is None:
        conf = spark_conf

    spark = SparkSession.builder.enableHiveSupport().config(conf=conf).getOrCreate()

    return spark


# def get_hyperopt_spark_conf(local_dir: str) -> SparkConf:
#     """
#     Функция создания конгфигурация спарка для распределённого оптимизатора hyperopt
#
#     Parameters
#     ----------
#     local_dir: str
#         Путь до временной папки
#
#     Returns
#     -------
#     hyperopt_spark_conf: SparkConf
#         Конифгурации для запуска спарк сессии для распределённого оптимизатора
#     """
#     hyperopt_spark_conf = spark_conf
#     hyperopt_spark_conf.set("spark.local.dir", local_dir)
#
#     return hyperopt_spark_conf