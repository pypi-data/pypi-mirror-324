import warnings
import logging

# Сохранение формата warnings, потому что некоторые библиотеки имеют свойство их менять
# shap>0.44.1 должен исправить эту проблему
from tqdm import TqdmExperimentalWarning

default_formatwarning = warnings.formatwarning

warnings.filterwarnings(
    "ignore",
    message="etna.*is not available.*",
)
warnings.filterwarnings(
    "ignore",
    message="wandb.*is not available.*",
)
warnings.filterwarnings(
    "ignore",
    message=".*package isn't installed.*",
)
warnings.filterwarnings(
    "ignore",
    message=".*package isn't installed.*",
)
warnings.filterwarnings(
    "ignore",
    message=".*tqdm.autonotebook.tqdm.*",
)
warnings.filterwarnings(
    "ignore",
    message='"is" with a literal.*',
)
warnings.filterwarnings(
    "ignore",
    message="No Nvidia GPU detected!.*",
)
warnings.filterwarnings(
    "ignore",
    message="LightGBM binary classifier with TreeExplainer shap values output.*",
)
warnings.filterwarnings(
    "ignore",
    message="The frame.append method is deprecated and will be removed.*",
)
warnings.filterwarnings(
    "ignore",
    message="Attempting to set identical low and high xlims makes.*",
)

import shap  # Заранее импортим shap, чтобы исправить форматирование

warnings.formatwarning = default_formatwarning

import lightautoml.utils.installation

logging.getLogger("lightautoml.utils.installation").setLevel(logging.ERROR)


class DMLWarning(Warning):
    """
    Base class for all warnings related to DreamML functionality.
    """

    pass