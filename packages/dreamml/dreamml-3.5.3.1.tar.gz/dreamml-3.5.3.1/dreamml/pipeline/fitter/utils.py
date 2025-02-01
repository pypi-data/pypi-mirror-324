from typing import Optional, Type

from dreamml.configs.config_storage import ConfigStorage
from dreamml.logging import get_logger
from dreamml.modeling.cv import BaseCrossValidator
from dreamml.pipeline.fitter._cv import _get_cv
from dreamml.pipeline.fitter import (
    FitterBase,
    FitterCV,
    FitterHO,
    FitterAMTS,
    FitterClustering,
)
from dreamml.utils import ValidationType


_logger = get_logger(__name__)


def choose_validation_type_by_data_size(size: int) -> ValidationType:
    """
    Функция возвращающая метод валидации в зависимости от размера обучающей выборки
    Parameters
    ----------
    size: int
        Размер обучающей выборки
    Returns
    -------
    validation: ValidationType
        Способ валидации
        validation == "cv" - будет выбрана папйплайн основанный на кросс-валидации
        validation == "hold-out" - будет выбран пайплайн основанный на разбиение обучающей выборки на train/valid/test

    """
    return ValidationType.CV if size < 250000 else ValidationType.HOLDOUT


def get_fitter(
    config: ConfigStorage,
    data_size: Optional[int] = None,
    custom_cv: Optional[Type[BaseCrossValidator]] = None,
    vectorization_name: Optional[str] = None,
) -> FitterBase:
    """
    Метод выбирает тип валидации, после возвращает нужный fitter (FitterCV или FitterHO)
    """
    if vectorization_name == "bert":
        return FitterHO()

    if config.validation == "auto":
        if data_size is None:
            raise ValueError("Can't get fitter automatically without data_size")

        validation = choose_validation_type_by_data_size(data_size)
    else:
        validation = config.validation

    validation = ValidationType(validation)

    if config.task == "amts":
        if custom_cv is not None:
            _logger.warning(
                "Передан класс `custom_cv` для кастомной кросс-валидации, который не поддерживается для amts задаче."
            )
        return FitterAMTS()

    if config.task == "topic_modeling":
        if custom_cv is not None:
            _logger.warning(
                "Передан класс `custom_cv` для кастомной кросс-валидации, который не поддерживается для topic_modeling задаче."
            )
        return FitterClustering()

    if validation == ValidationType.CV:
        cv = _get_cv(config, custom_cv=custom_cv)

        return FitterCV(cv)
    elif validation == ValidationType.HOLDOUT:
        if custom_cv is not None:
            _logger.warning(
                "Передан класс `custom_cv` для кастомной кросс-валидации, но тип валидации `validation` выбран не cv."
            )

        return FitterHO()
    else:
        raise ValueError(f"Can't get fitter for validation type = {validation.value}.")