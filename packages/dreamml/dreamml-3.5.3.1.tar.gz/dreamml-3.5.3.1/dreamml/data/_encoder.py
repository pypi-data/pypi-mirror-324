import pandas as pd


class BaseEncoder:
    """
    Базовый класс-заглушка энкодера.
    Используется, если пользователь не подал путь до энкодера, в таком случае метод transform тожедественный.

    """

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        return data