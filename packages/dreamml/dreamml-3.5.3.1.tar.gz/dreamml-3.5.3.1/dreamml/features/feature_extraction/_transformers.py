import numpy as np
import pandas as pd
from tqdm.auto import tqdm
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.tree import DecisionTreeRegressor
from sklearn.exceptions import NotFittedError

from dreamml.utils.errors import MissedColumnError


class LogTargetTransformer(BaseEstimator, TransformerMixin):
    """
    Преобразование целевой переменной в логарифмированную шкалу.

    Parameters
    ----------
    bias: float, optional, default = 0
        Смещение, добавляется к аргументу логарифма.
        Опциональный параметр, по умолчанию равен 0.

    tolerance: float, optional, default = 1e-5
        Значение, добавляемое к аргументу логарифма, для того,
        чтобы избежать ситуаций np.log(0).

    Attributes
    ----------
    target_min: float
        Минимальное значение целевой переменной.

    fitted: bool
        Флаг применения метода fit к целевой переменной.

    """

    def __init__(self, bias: float = 0, tolerance: float = 1e-5):
        self.bias = bias
        self.tolerance = tolerance
        self.target_min = None
        self.fitted = None

    @property
    def check_is_fitted(self):
        if not self.fitted:
            msg = (
                "This estimator is not fitted yet. Call 'fit' with "
                "appropriate arguments before using this estimator."
            )
            raise NotFittedError(msg)
        return True

    def fit(self, target: pd.Series) -> None:
        """
        Расчет минимального значения целевой переменной для
        корректного расчета логарифма на отрицательных значениях.

        Parameters
        ----------
        target: pandas.Series, shape = [n_samples, ]
            Вектор целевой переменной.

        Returns
        -------
        self

        """
        self.target_min = target.min()
        self.fitted = True
        return self

    def transform(self, target: pd.Series) -> pd.Series:
        """
        Логарифмическое преобразование целевой переменной.

        Parameters
        ----------
        target: pandas.Series, shape = [n_samples, ]
            Вектор целевой переменной.

        Returns
        -------
        log_target: pandas.Series, shape = [n_samples, ]
            Вектор прологарифмированной целевой переменной.

        """
        self.check_is_fitted
        return np.log(target - self.target_min + 1 + self.bias) + 1

    def inverse_transform(self, target: pd.Series) -> pd.Series:
        """
        Преобразование прологарифмированной целевой переменной к
        значениям в исходном диапазоне.

        Parameters
        ----------
        log_target: pandas.Series, shape = [n_samples, ]
            Вектор прологарифмированной целевой переменной.

        Returns
        -------
        target: pandas.Series, shape = [n_samples, ]
            Вектор целевой переменной.

        """
        self.check_is_fitted
        return np.exp(target - 1) + self.target_min - self.tolerance - 1


class DecisionTreeFeatureImportance(BaseEstimator, TransformerMixin):
    """
    Отбор признаков на основе решающего дерева.

    Parameters
    ----------
    threshold: float
        Порог для отбора переменных по корреляции.
        Если коэффициент корреляции для переменной выше
        порога - переменная макрируется 1 (использовать для
        дальнейшего анализа), если ниже порога - маркируется 0
        (не использовать для дальнейшего анализа).

    cat_features: List[string], optional, default = None
        Список категориальных признаков.
        Опциональный параметр, по умолчанию, не используется.

    remaining_features: List[str], default=[]
        Признаки, которые в любом случае должны остаться в датасете после отбора

    Attributes
    ----------
    scores_: Dict[str, float]
        Словарь со значениями корреляции,
        ключ словаря - название признака, значение - correlation-score.

    """

    def __init__(self, threshold, remaining_features=[], cat_features=None):
        self.threshold = threshold
        self.remaining_features = remaining_features
        self.cat_features = cat_features
        self.scores = {}

    @property
    def check_is_fitted(self):
        if not self.scores:
            msg = (
                "This estimator is not fitted yet. Call 'fit' with "
                "appropriate arguments before using this estimator."
            )
            raise NotFittedError(msg)
        return True

    @staticmethod
    def calculate_tree(feature: pd.Series, target: pd.Series) -> float:
        """
        Обучение решающего пня и вычисление корреляции между
        прогнозами, полученным с помощью решающего пня, и вектором
        целевой переменной.

        Parameters
        ----------
        feature: pandas.Series, shape = [n_samples, ]
            Вектор значений признака.

        target: pandas.Series, shape = [n_samples, ]
            Вектор целевой переменной.

        Returns
        -------
        score: float
            Значение корреляции.

        """
        feature = feature.fillna(-9999).values.reshape(-1, 1)
        tree = DecisionTreeRegressor(max_depth=3)
        tree.fit(feature, target)

        prediction = tree.predict(feature)
        score = np.corrcoef(prediction, target)

        return np.round(100 * score[0, 1], 2)

    def fit(self, data, target=None):
        """
        Вычисление коэффициента корреляции для всех признаков.

        Parameters
        ----------
        data: pandas.DataFrame, shape = [n_samples, n_features]
            Матрица признаков для обучения.

        target: pandas.Series, shape = [n_samples, ]
            Вектор целевой переменной.

        Returns
        -------
        self

        """
        if self.cat_features:
            missed_cols = list(set(self.cat_features) - set(data.columns))
            if missed_cols:
                raise MissedColumnError(f"Missed {list(missed_cols)} columns in data.")

            numeric_features = list(set(data.columns) - set(self.cat_features))
        else:
            numeric_features = data.columns

        for feature in tqdm(numeric_features):
            self.scores[feature] = self.calculate_tree(data[feature], target)

        return self

    def transform(self, data, target=None):
        """
        Отбор переменных по self.threshold.
        Если коффициент корреляции для переменной выше порога,
        то переменная помечается 1 (использовать для дальнейшего анализа),
        если ниже порога - маркируется 0 (не использовать для
        дальнейшего анализа).

        Parameters
        ----------
        data: pandas.DataFrame, shape = [n_samples, n_features]
            Матрица признаков для обучения.

        target: pandas.Series, shape = [n_samples, ]
            Вектор целевой переменной.

        Returns
        -------
        scores: pandas.DataFrame, shape = [n_features, 3]
            Датафрейм с корреляционным-анализом переменных.

        """
        self.check_is_fitted
        scores = pd.Series(self.scores)
        scores = pd.DataFrame({"Variable": scores.index, "Correlation": scores.values})
        scores["Correlation_abs"] = np.abs(scores["Correlation"])
        scores["Selected"] = scores.apply(
            lambda row: (
                1
                if row["Correlation_abs"] > self.threshold
                or row["Variable"] in self.remaining_features
                else 0
            ),
            axis=1,
        )
        scores = scores.sort_values(by="Correlation_abs", ascending=False)
        scores = scores.drop("Correlation_abs", axis=1)
        scores = scores.fillna(0)

        if self.cat_features:
            cat_features_scores = pd.DataFrame(
                {
                    "Variable": self.cat_features,
                    "Correlation": "категориальный признак",
                    "Selected": 1,
                }
            )
            scores = scores.append(cat_features_scores)

        mask = scores["Selected"] == 1
        self.used_features = scores.loc[mask, "Variable"].tolist()

        return scores.reset_index(drop=True)