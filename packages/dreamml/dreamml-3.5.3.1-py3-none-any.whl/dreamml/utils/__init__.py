from enum import Enum


class ValidationType(Enum):
    """
    `Enum`, который хранит типы возможные типы валидации: кросс-валидация и hold-out
    """

    CV = "cv"
    HOLDOUT = "hold-out"