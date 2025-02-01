from typing import Optional, List

import numpy as np
import pandas as pd
from tqdm.auto import tqdm
from sklearn.model_selection import train_test_split
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.exceptions import NotFittedError
from dreamml.utils.errors import MissedColumnError


class PSI(BaseEstimator, TransformerMixin):
    """
    Вычисление PSI и отбор признаков на их основе.

    Parameters
    ----------
    threshold: float
        Порог для отбора переменных по PSI.
        Если PSI для переменной выше порога - переменная макрируется
        0 (не использовать для дальнейшего анализа), если ниже
        порога - маркируется 1 (использовать для дальнейшего анализа).

    n_bins: int, optional, default = 20
        Количество бинов, на которые разбивается выборка.

    min_value: float, optional, default = 0.005
        Значение которое используется, если рассчитанный psi = 0.

    bin_type: string, optional, default = "quanitles"
        Способ разбиения на бины: "quantiles", "bins" or "continuous".
        При выборе "quantiles" - выборка будет разбита на n_bins
        квантилей, при выборке "bins" - выборка будет разбита на
        n_bins бакетов с равным шагом между бакетами,
        при выборе "continuous" - выборка будет разбита на бакеты с одинаковыми границами для двух выборок (train/test
        или test/oot), где в каждом бакете не меннее определенной доли выборки (по умолчанию 5%).
        Иные значения приводят к возникновению ValueError.

    Attributes
    ----------
    scores_: Dict[str, float]
        Словарь со значениями PSI,
        ключ словаря - название признака, значение - PSI-score.

    used_features: List[str]
        Список отобранных признаокв.

    """

    def __init__(
        self,
        threshold: float,
        categorical_features: Optional[List[str]] = None,
        remaining_features: List[str] = [],
        bin_type: str = "quantiles",
        min_value: float = 0.005,
        n_bins: int = 20,
        used_features=None,
    ):

        self.threshold = threshold
        self.categorical_features = categorical_features
        self.remaining_features = remaining_features
        self.min_value = min_value
        self.n_bins = n_bins
        if bin_type in ["quantiles", "bins", "continuous"]:
            self.bin_type = bin_type
        else:
            raise ValueError(
                "Incorrect bin_type value. Expected 'quantiles', 'bins' or 'continuous', "
                f"but {bin_type} is transferred."
            )
        self.scores = {}
        self.used_features = used_features

    @property
    def check_is_fitted(self):
        if not self.scores:
            msg = (
                "This estimator is not fitted yet. Call 'fit' with "
                "appropriate arguments before using this estimator."
            )
            raise NotFittedError(msg)
        return True

    def calculate_bins(
        self, expected: pd.Series, actual: pd.Series, threshold: float = 0.05
    ) -> np.array:
        """
        Вычисление границ бинов для разбиения выборки.

        Parameters
        ----------
        expected: pandas.Series, shape = [n_samples_e, ]
            Наблюдения из train-выборки.

        actual: pandas.Series, shape = [n_samples_o, ]
            Наблюдения из test-выборки.
            (требуется для разбиения по тактике "continuous")

        threshold: float
            Минимальная доля выборки в бакете.
            (требуется для разбиения по тактике "continuous")

        Returns
        -------
        bins: numpy.array, shape = [self.n_bins + 1]
            Список с границами бинов.

        """
        if self.bin_type == "quantiles":
            bins = np.linspace(0, 100, self.n_bins + 1)
            bins = [np.nanpercentile(expected, x) for x in bins]
        elif self.bin_type == "continuous":
            min_expected_len = (
                int(len(expected) * threshold)
                if len(expected) * threshold > 5
                else len(expected)
            )
            min_actual_len = (
                int(len(actual) * threshold)
                if len(actual) * threshold > 5
                else len(actual)
            )
            bins = sorted(
                self.calculate_continuous_bins(
                    expected, actual, min_expected_len, min_actual_len
                )
            )
        else:
            bins = np.linspace(expected.min(), expected.max(), self.n_bins + 1)

        return np.unique(bins)

    def calculate_continuous_bins(
        self,
        expected: pd.Series,
        actual: pd.Series,
        min_expected_len: int,
        min_actual_len: int,
        result: List = None,
    ):
        """
        Вычисление границ бинов по тактике "continuous". Выборка будет разбита на бакеты с одинаковыми границами
        для двух выборок expected/actual (train/test или test/oot),
        где в каждом бакете не меннее определенной доли выборки (по умолчанию 5%).

        Parameters
        ----------
        expected: pandas.Series, shape = [n_samples_e, ]
            Наблюдения из train-выборки.

        actual: pandas.Series, shape = [n_samples_o, ]
            Наблюдения из test-выборки.

        min_expected_len: int
            Минимальное количество значений в бакете для выборки expected.

        min_actual_len: int
            Минимальное количество значений в бакете для выборки actual.

        result: List
            Переменная для хранения результатов.

        Returns
        -------
        result: List
            Список с границами бинов.

        """
        if not result:
            result = []

        median_value = np.median(expected)

        left_test = expected[expected <= median_value]
        left_oot = actual[actual <= median_value]
        right_test = expected[expected > median_value]
        right_oot = actual[actual > median_value]
        if (
            len(left_test) >= min_expected_len
            and len(left_oot) >= min_actual_len
            and len(right_test) >= min_expected_len
            and len(right_oot) >= min_actual_len
        ):
            if median_value not in result:
                result.append(median_value)
            result = self.calculate_continuous_bins(
                left_test, left_oot, min_expected_len, min_actual_len, result
            )
            result = self.calculate_continuous_bins(
                right_test, right_oot, min_expected_len, min_actual_len, result
            )

        return result

    def calculate_psi_in_bin(self, expected_score, actual_score) -> float:
        """
        Вычисление значения psi для одного бакета.

        Осуществляется проверка на равенство нулю expected_score и
        actual_score: если один из аргументов равен нулю, то его
        значение заменяется на self.min_value.

        Parameters
        ----------
        expected_score: float
            Ожидаемое значение.

        actual_score: float
            Наблюдаемое значение.

        Returns
        -------
        value: float
            Значение psi в бине.

        """
        if expected_score == 0:
            expected_score = self.min_value
        if actual_score == 0:
            actual_score = self.min_value

        value = expected_score - actual_score
        value = value * np.log(expected_score / actual_score)

        return value

    def calculate_psi(self, expected: pd.Series, actual: pd.Series, bins) -> float:
        """
        Расчет PSI для одной переменной.

        Parameters
        ----------
        expected: pandas.Series, shape = [n_samples_e, ]
            Наблюдения из train-выборки.

        actual: pandas.Series, shape = [n_samples_o, ]
            Наблюдения из test-выборки.

        bins: pandas.Series, shape = [self.n_bins, ]
            Бины для расчета PSI.

        Returns
        -------
        psi_score: float
            PSI-значение для данной пары выборок.

        """
        expected_score = np.histogram(expected.fillna(-9999), bins)[0]
        expected_score = expected_score / expected.shape[0]

        actual_score = np.histogram(actual.fillna(-9999), bins)[0]
        actual_score = actual_score / actual.shape[0]

        psi_score = np.sum(
            self.calculate_psi_in_bin(exp_score, act_score)
            for exp_score, act_score in zip(expected_score, actual_score)
        )

        return psi_score

    def calculate_numeric_psi(self, expected: pd.Series, actual: pd.Series) -> float:
        """
        Вычисление PSI для числовой переменной.

        Parameters
        ----------
        expected: pandas.Series, shape = [n_samples_e, ]
            Наблюдения из train-выборки.

        actual: pandas.Series, shape = [n_samples_o, ]
            Наблюдения из test-выборки.

        Returns
        -------
        psi_score: float
            PSI-значение для данной пары выборок.

        """
        bins = self.calculate_bins(expected, actual)
        psi_score = self.calculate_psi(expected, actual, bins)
        return psi_score

    def calculate_categorical_psi(
        self, expected: pd.Series, actual: pd.Series
    ) -> float:
        """
        Вычисление PSI для категориальной переменной.
        PSI рассчитывается для каждого уникального значения категории.

        Parameters
        ----------
        expected: pandas.Series, shape = [n_samples_e, ]
            Наблюдения из train-выборки.

        actual: pandas.Series, shape = [n_samples_o, ]
            Наблюдения из test-выборки.

        Returns
        -------
        psi_score: float
            PSI-значение для данной пары выборок.

        """
        bins = np.unique(expected).tolist()
        expected_score = expected.value_counts(normalize=True)
        actual_score = actual.value_counts(normalize=True)

        expected_score = expected_score.sort_index().values
        actual_score = actual_score.sort_index().values

        psi_score = np.sum(
            self.calculate_psi_in_bin(exp_score, act_score)
            for exp_score, act_score in zip(expected_score, actual_score)
        )
        return psi_score

    def fit(self, data, target=None):
        """
        Вычисление PSI-значения для всех признаков.

        Parameters
        ----------
        data: pandas.DataFrame, shape = [n_samples, n_features]
            Матрица признаков для обучения.

        target: pandas.DataFrame, shape = [n_samples, n_features]
            Матрица признаков для тестирования.

        Returns
        -------
        self

        """
        missed_columns = list(set(data.columns) - set(target.columns))

        if missed_columns:
            raise MissedColumnError(f"Missed {list(missed_columns)} columns in data.")

        if self.categorical_features:
            numeric_features = list(set(data.columns) - set(self.categorical_features))
            self.categorical_features = list(
                set(data.columns) & set(self.categorical_features)
            )
            for feature in self.categorical_features:
                self.scores[feature] = self.calculate_categorical_psi(
                    data[feature], target[feature]
                )
        else:
            numeric_features = data.columns

        if self.used_features is not None:
            numeric_features = [f for f in numeric_features if f in self.used_features]

        for feature in tqdm(numeric_features):
            self.scores[feature] = self.calculate_numeric_psi(
                data[feature], target[feature]
            )
        return self

    def transform(self, data, target=None) -> pd.DataFrame:
        """
        Отбор переменных по self.threshold.
        Если PSI-score для переменной выше порога, то переменная
        помечается 0 (не использовать для дальнейшего анализа), если ниже
        порога - маркируется 1 (использовать для дальнейшего анализа).

        Parameters
        ----------
        data: pandas.DataFrame, shape = [n_samples, n_features]
            Матрица признаков для обучения.

        target: pandas.DataFrame, shape = [n_samples, n_features]
            Матрица признаков для тестирования.

        Returns
        -------
        scores: pandas.DataFrame, shape = [n_features, 3]
            Датафрейм с PSI-анализом переменных.

        """
        self.check_is_fitted
        scores = pd.Series(self.scores)
        scores = pd.DataFrame({"Variable": scores.index, "PSI": scores.values})
        scores["Selected"] = scores.apply(
            lambda row: (
                1
                if row["PSI"] < self.threshold
                or row["Variable"] in self.remaining_features
                else 0
            ),
            axis=1,
        )
        scores = scores.sort_values(by="PSI")

        mask = scores["Selected"] == 1
        # self.used_features = scores.loc[mask, "Variable"].tolist()

        return scores.reset_index(drop=True)


def choose_psi_sample(eval_sets: dict, config: dict) -> dict:
    """
    Выбор выборки для расчета PSI.
    Выбор осуществляется на основании параметра `psi_sample` в
    конфигурационном файле эксперимента. Если значение равно
    `valid` / `test` - то выбирается данная выборка целиком,
    значение равно `OOT` - то выборка разбивается на 2
    непересекающихся выборки, одна из которых используется
    для расчета PSI, другая используется для независимой
    оценки качества.

    Parameters
    ----------
    eval_sets: Dict[str, Tuple[pd.DataFrame, pd.Series]]
        pass

    config: dict
        Словарь с конфигурацией эксперимента.

    Returns
    -------
    eval_sets: Dict[str, Tuple[pd.DataFrame, pd.Series]]
        Преобразованный словарь с eval_set.

    psi_sample: pd.DataFrame
        Выборка для расчета PSI.

    """
    psi_sample_name = config.get("psi_sample", "OOT")

    if psi_sample_name in [None, "train"]:
        return eval_sets, eval_sets["train"][0]

    if psi_sample_name in ["valid", "test"]:
        return eval_sets, eval_sets[psi_sample_name][0]

    elif psi_sample_name == "OOT":
        oot_evaluate, oot_psi = train_test_split(
            eval_sets["OOT"][0], train_size=0.5, random_state=1
        )
        oot_target_evaluate, oot_target_psi = train_test_split(
            eval_sets["OOT"][1], train_size=0.5, random_state=1
        )
        eval_sets["OOT"] = (oot_evaluate, oot_target_evaluate)
        eval_sets["OOT_psi"] = (oot_psi, oot_target_psi)

        return eval_sets, oot_psi

    else:
        raise ValueError(f"Unknown psi-sample name! Please choose: {eval_sets.keys()}")