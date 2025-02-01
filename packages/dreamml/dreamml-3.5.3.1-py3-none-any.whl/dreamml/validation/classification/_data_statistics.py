import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from dreamml.validation._base import BaseTest


class DataStatisticsTest(BaseEstimator, TransformerMixin, BaseTest):
    """
    Расчет статистик по данным. Содержит:

    - статистику по каждой выборке train / valid / ... :
      количество наблюдений в каждой выборке, количество
      целевыйх событий, доля целевого события;

    - статиску по переменным: название целевой переменной,
      количество категориальных признаков, количество непрерывных
      признаков;

    - статистику по переменным: название переменной, количество
      заполненных значений, минимальное значение, среднее значение,
      максимальное значение, перцентили 25, 50, 75.

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

    def __init__(
        self,
        artifacts_config: dict,
        validation_test_config: dict,
    ):
        self.used_features = artifacts_config["used_features"]
        self.categorical_features = artifacts_config.get("categorical_features", list())
        self.artifacts_config = artifacts_config
        self.multiclass_artifacts = self.artifacts_config["multiclass_artifacts"]

    def _calculate_samples_stats(self, **eval_sets):
        """
        Расчет статистики по выборке data и вектора target.
        Расчитывается количество наблюдений, количество целевых событий
        и доля целевого события.

        Parameters:
        -----------
        eval_sets: Dict[string, Tuple[pandas.DataFrame, pandas.Series]]
            Словарь с выборками, для которых требуется рассчитать статистику.
            Ключ словаря - название выборки (train / valid / ...), значение -
            кортеж с матрицей признаков (data) и вектором ответов (target).

        Returns:
        --------
        result: pandas.DataFrame
            Датафрейм с рассчитанной статистикой.

        """
        if self.artifacts_config["task"] in ["binary"]:
            result = {}
            for data_name in eval_sets:
                data, target = eval_sets[data_name]
                result[data_name] = [len(data), np.sum(target), np.mean(target)]
            result = pd.DataFrame(result).T.reset_index()
            result.columns = ["Выборка", "# наблюдений", "# events", "# eventrate"]
            return result.fillna(0)

        elif self.artifacts_config["task"] in ["multiclass", "multilabel"]:
            columns = ["Выборка", "# наблюдений"]
            if isinstance(eval_sets["train"][1], pd.Series):
                eval_set_cols = eval_sets["train"][1].to_frame().columns.tolist()
            else:
                eval_set_cols = eval_sets["train"][1].columns.tolist()
            columns.extend([f"# events {class_name}" for class_name in eval_set_cols])
            columns.extend(
                [f"# eventrate {class_name}" for class_name in eval_set_cols]
            )

            result = {}
            for data_name in eval_sets:
                data, target = eval_sets[data_name]
                if isinstance(eval_sets[data_name][1], pd.Series):
                    target = target.to_frame()

                events = np.sum(target).tolist()
                event_rate = np.mean(target).tolist()
                result[data_name] = [len(data)] + events + event_rate

            result = pd.DataFrame(result).T.reset_index()
            assert len(columns) == result.shape[1]
            result.columns = columns
            return result.fillna(0)

        else:
            raise ValueError('Task must be in ["binary", "multiclass" or "multilabel"]')

    @staticmethod
    def _calculate_variables_stats(**data) -> pd.DataFrame:
        """
        Расчет статистик по переменным. Рассчитывается количество
        заполненных значений признака, среднее значение признака,
        стандартное отклонение признака, минимальное значение
        признака, 25-ый перцентиль признака, медиана признака,
        75-ый перцентиль признака, максимальное значение признака.

        Parameters:
        -----------
        data: Dict[string, Tuple[pandas.DataFrame, pandas.Series]]
            Словарь с выборками, для которых требуется рассчитать статистику.
            Ключ словаря - название выборки (train / valid / ...), значение -
            кортеж с матрицей признаков (data) и вектором ответов (target).

        Returns:
        --------
        result: pandas.DataFrame
            Датафрейм с рассчитанной статистикой.

        """
        sample_name = next(iter(data))
        x, _ = data[sample_name]

        result = x.describe().T.reset_index()
        result.columns = [
            "Variable name",
            "Number of filled value",
            "AVG-value",
            "STD-value",
            "MIN-value",
            "25% percentile-value",
            "50% percentile-value",
            "75% percentile-value",
            "MAX-value",
        ]
        return result.fillna(0)

    def _calculate_variables_types_stats(self, **data) -> pd.DataFrame:
        """
        Расчет статистик по типам переменным. Рассчитывается количество
        категориальных переменных, количество непрерывных переменных
        и название целевой переменной.

        Parameters:
        -----------
        data: Dict[string, Tuple[pandas.DataFrame, pandas.Series]]
            Словарь с выборками, для которых требуется рассчитать статистику.
            Ключ словаря - название выборки (train / valid / ...), значение -
            кортеж с матрицей признаков (data) и вектором ответов (target).

        Returns:
        --------
        stats: pandas.DataFrame
            Датафрейм с рассчитанной статистикой.

        """
        sample_name = next(iter(data))
        _, y = data[sample_name]

        if self.multiclass_artifacts is not None:
            target_name = self.multiclass_artifacts["target_name"]
        elif isinstance(y, pd.DataFrame):
            target_name = y.columns.tolist()
        else:
            target_name = y.name

        stats = pd.DataFrame(
            {
                "Целевая переменная": [target_name],
                "# категорий": [len(self.categorical_features)],
                "# непрерывных": [
                    len(self.used_features) - len(self.categorical_features)
                ],
            }
        )
        return stats.fillna(0)

    def transform(self, **data):
        """
        Parameters
        ----------
        data: Dict[string, Tuple[pandas.DataFrame, pandas.Series]]
            Словарь с выборками, для которых требуется рассчитать статистику.
            Ключ словаря - название выборки (train / valid / ...),
            значение - кортеж с матрицей признаков (data) и вектором
            ответов (target).

        Returns
        -------
        result: Tuple[pd.DataFrame]
            Кортеж с полученными статистиками.

        """
        if self.artifacts_config["task"] == "multiclass":
            data = self.label_binarizing(**self.multiclass_artifacts, **data)

        result = (
            self._calculate_samples_stats(**data),
            self._calculate_variables_types_stats(**data),
            self._calculate_variables_stats(**data),
        )
        return result