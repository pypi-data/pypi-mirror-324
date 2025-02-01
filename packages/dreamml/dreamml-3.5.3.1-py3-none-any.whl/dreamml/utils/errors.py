class MissedColumnError(IndexError):
    """
    Класс для идентификации ошибки несоответствия
    ожидаемых и полученных столбцов в pandas.DataFrame
    """

    pass


class MissedTargetError(Exception):
    pass


class ConfigurationError(Exception):
    pass