from dreamml.utils.spark_utils import spark_conf
import pprint
import pandas as pd


class ZeroDataFrameException(Exception):
    """
    Ошибка возникающая при возращении из spark датасета с нулевым количеством наблюдений
    """

    def __init__(self):
        self.spark_conf = list(spark_conf.getAll())
        self.message = f"""Был возращён датасет с 0 наблюдений
        Попробуйте использовать свои более мощные конфигурации spark сессии (SparkConf),
        а за основу можете взять нашу сессию
        {pprint.pformat(self.spark_conf)}"""
        super(ZeroDataFrameException, self).__init__(self.message)


class ColumnDoesntExist(Exception):
    """
    Ошибка возникающая при отсутствии колонки в датафрейме
    """

    def __init__(self, column_name: str, data: pd.DataFrame, msg: str = None):
        self.column_name = column_name
        self.data = data
        if msg:
            self.msg = msg
        else:
            self.msg = f"Указанная колонка {column_name} в данной таблице не существует"

    def __str__(self):
        return self.msg


class MissingRequiredConfig(Exception):
    """
    Ошибка возникающая при отсутствии обязательного конфига
    """

    def __init__(self, config_name: str = None):
        self.msg = f"Обязательный конфиг {config_name} пустой"

    def __str__(self):
        return self.msg