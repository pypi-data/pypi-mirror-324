import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from ._base import BaseTest


class TaskDescriptionTest(BaseEstimator, TransformerMixin, BaseTest):
    """
    Описание решаемой бизнес-задачи и полное описание используемого пайплайна.

    Parameters
    ----------
    artifacts_config: dict
        Словарь с артефактами, необходимых для построения валидационного отчета.

    validation_test_config: dict
        Словарь с параметрами валидационных тестов.

    Attributes
    ----------
    used_features: List[str]
        Список используемых признаков.

    categorical_features: List[str]
        Список категориальных признаков.

    """

    def __init__(self, artifacts_config: dict, validation_test_config: dict):
        self.used_features = artifacts_config["used_features"]
        self.categorical_features = artifacts_config.get("categorical_features", list())
        self.validation_test_config = validation_test_config

    def _create_description(self, **data):
        _stagies = [
            "Cбор данных",
            "Разбиение выборки на обучение / валидацию / тест",
            "Способ обработки пропусков",
            "Способ обработки категориальных признаков",
            "Способ отбора признаков",
            "Построенные модели",
            "Оптимизация гиперпараметров модели",
        ]
        _descriptions = [
            "< Прикрепите скрипт для сбора обучающей выборки >",
            (
                "< В DreamML, по умолчанию, разбиение производится на 3 части: "
                "train, valid, test. Соотношение разбиения: 60%, 20%, 20%. >"
            ),
            (
                "< В DreamML, по умолчанию, пропуски заполняются для категориальных "
                "признаков, значение - 'NA'. Для числовых признаков пропуски не "
                "заполняются. >"
            ),
            (
                "< В DreamML, по умолчанию, категориальные признаки обрабатываются "
                "с помощью доработанного LabelEncoder, после чего признаки передаются "
                "в качестве категориальных в модель, которая умеет обрабатывать категории. >"
            ),
            (
                "< В DreamML, по умолчанию, используется следующая цепочка отбора признаков: "
                "Gini -> PSI -> Permutation -> ShapUplift -> ShapDelta >"
            ),
            (
                "< В DreamML, по умолчанию, используются модели LightGBM, XGBoost, CatBoost, "
                "WhiteBox AutoML. >"
            ),
            (
                "< В DreamML, по умолчанию, используется BayesianOptimization для "
                "оптимизации гиперпараметров модели."
            ),
        ]
        stats = pd.DataFrame({"Название стадии": _stagies, "Описание": _descriptions})
        return stats


class BusinessCaseDescription(BaseEstimator, TransformerMixin, BaseTest):
    """
    Описание решаемой бизнес-задачи.

    Parameters
    ----------
    artifacts_config: dict
        Словарь с артефактами, необходимых для построения валидационного отчета.

    validation_test_config: dict
        Словарь с параметрами валидационных тестов.

    Attributes
    ----------
    used_features: List[str]
        Список используемых признаков.

    categorical_features: List[str]
        Список категориальных признаков.

    """

    def __init__(self, artifacts_config: dict, validation_test_config: dict):
        self.used_features = artifacts_config["used_features"]
        self.categorical_features = artifacts_config.get("categorical_features", list())
        self.validation_test_config = validation_test_config

    def _create_description(self, **data):
        stats = pd.DataFrame()
        stats["Параметр"] = [
            "Бизнес-задача",
            "Описание задачи",
            "Даты сбора данных",
            "Отбор наблюдений",
            "Описание целевой переменной",
            "Используемый ML-алгоритм",
        ]
        stats["train"] = "1"
        stats["valid"] = "1"
        stats["test"] = "1"
        stats["Out-Of-Time"] = "1"
        return stats