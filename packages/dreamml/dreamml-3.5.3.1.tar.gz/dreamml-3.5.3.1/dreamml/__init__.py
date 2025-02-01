__version__ = "3.5.3.1"

import os
from pathlib import Path

# Подтягиваем действия с warnings перед импортом любых других библиотек
import dreamml.utils.warnings
from dreamml.logging.logger import init_logging, capture_warnings

init_logging("dreamml")

# после добавления handlers к логгеру "dreamml" они не добавятся автоматически к логгеру py.warnings,
# в текущей реализации это и не нужно, так как warnings модуль нужен для разработки и добавление warnings
# в систему логирования не существенно
capture_warnings(True)

os.environ["TOKENIZERS_PARALLELISM"] = "false"


# before LAMA потому что так надо
import torch

from lightautoml.tasks import Task
from lightautoml.automl.presets.tabular_presets import TabularAutoML


__doc__ = """
DreamML - core library for working with models.
===============================================

All you need is make config for your task.

Provides:
- Data transforming: reading, splitting, encoding dataset.
- Developing ML model: for tasks such as regression, binary classification.
- Artifact saver: storing all information about given model.
- Reports: informative excel report file with model and metrics.
- Validation: validation tests and reports.
- Visualization: creating plots for comparing y_true vs y_pred. 

"""