from typing import List, Optional

import numpy as np
import pandas as pd
from tqdm.auto import tqdm
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.tree import DecisionTreeClassifier
from sklearn.exceptions import NotFittedError
from sklearn.metrics import roc_auc_score

from dreamml.modeling.metrics.metrics_mapping import metrics_mapping
from dreamml.utils.errors import MissedColumnError


CATEGORY = "категориальный признак"


class GiniFeatureImportance(BaseEstimator, TransformerMixin):
    """
    Вычисление GINI для каждого признака и отбор признаков на их основе.

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
        Способ разбиения на бины: "quantiles" or "bins".
        При выборе "quantiles" - выборка будет разбита на n_bins
        квантилей, при выборке "bins" - выборка будет разбита на
        n_bins бакетов с равным шагом между бакетами.
        Иные значения приводят к возникновению ValueError.

    Attributes
    ----------
    scores_: Dict[str, float]
        Словарь со значениями PSI,
        ключ словаря - название признака, значение - PSI-score.

    """

    def __init__(self, threshold, remaining_features=[], cat_features=None):
        self.threshold = threshold
        self.remaining_features = remaining_features
        self.cat_features = cat_features
        self.used_features = None
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

    def fit(self, data, target):
        """
        Вычисление метрики GINI для всех признаков.

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
        if self.cat_features:

            missed_columns = list(set(self.cat_features) - set(data.columns))
            if missed_columns:
                raise MissedColumnError(
                    f"Missed {list(missed_columns)} columns in data."
                )

            numeric_features = list(set(data.columns) - set(self.cat_features))
        else:
            numeric_features = data.columns

        for feature in tqdm(numeric_features):
            auc = roc_auc_score(target, data[feature].fillna(-9999))
            self.scores[feature] = (2 * np.abs(auc - 0.5)) * 100

        return self

    def transform(self, data, target=None):
        """
        Отбор переменных по self.threshold.
        Если GINI для переменной выше порога, то переменная
        помечается 1 (использовать для дальнейшего анализа), если ниже
        порога - маркируется 0 (не использовать для дальнейшего анализа).

        Parameters
        ----------
        data: pandas.DataFrame, shape = [n_samples, n_features]
            Матрица признаков для обучения.

        target: pandas.DataFrame, shape = [n_samples, n_features]
            Матрица признаков для тестирования.

        Returns
        -------
        scores: pandas.DataFrame, shape = [n_features, 3]
            Датафрейм с GINI-анализом переменных.

        """
        self.check_is_fitted
        scores = pd.Series(self.scores)
        scores = pd.DataFrame({"Variable": scores.index, "GINI": scores.values})
        scores["Selected"] = scores.apply(
            lambda row: (
                1
                if row["GINI"] > self.threshold
                or row["Variable"] in self.remaining_features
                else 0
            ),
            axis=1,
        )
        scores = scores.sort_values(by="GINI", ascending=False)

        if self.cat_features:
            cat_features_scores = pd.DataFrame(
                {"Variable": self.cat_features, "GINI": CATEGORY, "Selected": 1}
            )
            scores = scores.append(cat_features_scores)

        mask = scores["Selected"] == 1
        self.used_features = scores.loc[mask, "Variable"].tolist()

        return scores.reset_index(drop=True)


def compare_gini_features(eval_sets, config):
    """
    Отбор признаков из набора данных train.
    Отбираются признаки, которые имеют величину меньше gini_absolute_diff (п.п.)
    для абсолютного изменения и меньше gini_relative_diff (%) для относительного
    изменения важности признаков по отношению к набору данных, который указан
    в конфигурационном файле с ключом valid_sample.

    Parameters
    ----------
    eval_sets: Dict[string, Tuple[pandas.DataFrame, pandas.Series]]
        Словарь с выборками, для которых требуется рассчитать статистику.
        Ключ словаря - название выборки (train / valid / ...), значение -
        кортеж с матрицей признаков (data) и вектором ответов (target).

    config: dict, optional, default = config_file
        Словарь с конфигурацией запуска кернела.

    Returns
    -------
    g_merge: pandas.DataFrame
        Набор данных с важностями признаков,
        абсолютной и отностиельной разницой между ними
        и с флагом подтверждающим отобран признак или нет.

    used_features: List[string]
        Преобразовнный список используемых признаков.

    """
    transformer = GiniFeatureImportance(
        threshold=config["gini_threshold"],
        remaining_features=config["remaining_features"],
        cat_features=config["categorical_features"],
    )
    u_features = {}
    valid_name = config.get("valid_sample", "valid")
    train = transformer.fit_transform(*eval_sets["train"])
    u_features["train"] = transformer.used_features
    valid = transformer.fit_transform(*eval_sets[valid_name])
    u_features[valid_name] = transformer.used_features

    g_merge = train.merge(valid, on="Variable", suffixes=("_train", f"_{valid_name}"))
    g_merge, used_features = compute_difference(g_merge, config, u_features)

    g_merge["Selected"] = 0
    mask = g_merge["Variable"].isin(used_features)
    g_merge.loc[mask, "Selected"] = 1
    g_merge = g_merge.drop(["Selected_train", f"Selected_{valid_name}"], axis=1)
    g_merge.fillna("Не применяется", inplace=True)

    cols = [
        "Variable",
        "GINI_train",
        f"GINI_{valid_name}",
        "absolute_diff",
        "relative_diff",
        "Selected",
    ]
    g_merge = g_merge[cols]

    return g_merge, used_features


def compute_difference(g_merge, config, u_features):
    """
    Вычисление абсолютной и относительной разницы между важностями признаков
    из наборов данных train и указанного в качестве valid_sample в config

    Parameters
    ----------
    g_merge: pandas.DataFrame
        Набор данных созданный в результате объединения
        train и датасета указанно в качестве valid_sample

    config: dict, optional, default = config_file
        Словарь с конфигурацией запуска кернела.

    u_features: Dict[List[string]]
        Словарь со списками признаков из наборов данных train
        и указанного в конфигурационном файле под ключём valid_sample
        отобранных по gini_threshold

    Returns
    -------
    g_merge: pandas.DataFrame
        Набор данных с важностями признаков,
        абсолютной и отностиельной разницой между ними
        и с флагом подтверждающим отобран признак или нет.

    used_features: List[string]
        Преобразовнный список используемых признаков.
    """
    absolute_diff = config.get("gini_absolute_diff", 5)
    relative_diff = config.get("gini_relative_diff", 30)
    valid_name = config.get("valid_sample", "valid")

    mask = g_merge["GINI_train"] == "категориальный признак"
    cat_merge = g_merge.loc[mask]
    num_merge = g_merge.loc[~mask]
    num_merge["GINI_train"] = num_merge["GINI_train"].replace(0, np.nan)

    num_merge["absolute_diff"] = np.abs(
        num_merge[f"GINI_{valid_name}"] - num_merge["GINI_train"]
    )
    num_merge["relative_diff"] = (
        100 * num_merge["absolute_diff"] / (num_merge["GINI_train"])
    )
    num_merge.fillna(0, inplace=True)
    num_merge.sort_values("GINI_train", ascending=False, inplace=True)

    mask = (num_merge["absolute_diff"] >= absolute_diff) | (
        num_merge["relative_diff"] >= relative_diff
    )
    bad_features = num_merge.loc[mask, "Variable"].tolist()
    used_features = [
        feature
        for feature in u_features["train"]
        if feature not in bad_features and feature in u_features[valid_name]
    ]

    g_merge = pd.concat((num_merge, cat_merge))
    return g_merge, used_features


class GiniFeatureSelectionCV(BaseEstimator, TransformerMixin):
    """
    Отбор признаков с помощью метрики GINI на кросс-валидации.

    Parameters
    ----------
    cv: sklearn.model_selection.generator
        Генератор для разбиения данных в рамках кросс-валидации.

    threshold: int, optional, default = 5
        Порог для отбора признаков. Опциональный параметр.
        По умолчанию, используется значение threshold = 5.

    cat_features: List[str], optional, default = None
        Список категориальных признаков. Опциональный параметр.
        По умолчанию, категориальные признаки не используются.

    abs_difference: np.number, optional, default = 10
        Абсолютная разница в допустимой разнице метрики на
        обучающей выборке и валидационной выборке. Опциональный параметр.
        По умолчанию, используется значение abs_difference = 10.

    rel_difference: np.number, optional, default = 30
        Относительная разница в допустимой разнице метрики на
        обучающей выборке и валидационной выборке. Опциональный параметр.
        По умолчанию, используется значение rel_difference = 30.

    Attributes
    ----------
    const: np.number
        Значение константы, на которую заменяются пропуски в данных.

    used_features: List[str]
        Список отобранных признаков.

    scores: pd.DataFrame
        Датафрейм со значением метрики GINI.

    """

    def __init__(
        self,
        cv,
        threshold: np.number = 5,
        cat_features: Optional[List[str]] = None,
        abs_difference: np.number = 10,
        rel_difference: np.number = 30,
    ):

        self.cv = cv
        self.threshold = threshold
        self.abs_difference = abs_difference
        self.rel_difference = rel_difference
        self.cat_features = cat_features
        self.const = np.finfo(np.float32).min
        self.used_features = None
        self.scores = None

    @staticmethod
    def _to_frame(data: dict, prefix: str = "train") -> pd.DataFrame:
        """
        # ToDO
        """
        if prefix:
            prefix = f"{prefix}-"

        importance = pd.Series(data)
        importance = importance.to_frame().reset_index()
        importance.columns = ["Variable", f"{prefix}importance"]

        return importance

    def _calculate_fold_metric(self, data, target):
        """
        # ToDO
        """
        importance = pd.DataFrame()
        for train_idx, valid_idx in tqdm(self.cv.split(splitter_df)):
            x_train, x_valid = data.loc[train_idx], data.loc[valid_idx]
            y_train, y_valid = target.loc[train_idx], target.loc[valid_idx]

            fold_train_importance = self._calculate_metric(data=x_train, target=y_train)
            fold_valid_importance = self._calculate_metric(data=x_valid, target=y_valid)
            fold_train_importance = self._to_frame(
                fold_train_importance, prefix="train"
            )
            fold_valid_importance = self._to_frame(
                fold_valid_importance, prefix="valid"
            )

            fold_importance = pd.concat(
                [fold_train_importance, fold_valid_importance], axis=1
            )
            importance = pd.concat([importance, fold_importance])

        importance = importance.iloc[:, 1:]
        importance = importance.groupby(["Variable"])
        importance = importance[["train-importance", "valid-importance"]].mean()
        importance = importance.reset_index().sort_values(
            by="valid-importance", ascending=False
        )
        importance = importance.reset_index(drop=True)

        importance["abs_delta"] = (
            importance["train-importance"] - importance["valid-importance"]
        )
        importance["abs_delta"] = np.abs(importance["abs_delta"])

        importance["rel_delta"] = (
            importance["abs_delta"] / importance["train-importance"]
        )
        importance = importance.fillna(0)

        return importance

    def _calculate_metric(self, data, target):
        """
        # ToDO
        """
        scores = {}
        for feature in data.columns:
            score = metrics_mapping["gini"]()(
                y_true=target,
                y_pred=data[feature].fillna(self.const),
            )
            scores[feature] = 100 * np.abs(score)

        return scores

    def fit(self, X, y):
        """
        # ToDO
        """
        if self.cat_features:
            missed_columns = list(set(self.cat_features) - set(X.columns))
            if missed_columns:
                raise MissedColumnError(
                    f"Missed {list(missed_columns)} columns in data."
                )
            numeric_features = list(set(X.columns) - set(self.cat_features))
        else:
            numeric_features = X.columns

        self.scores = self._calculate_fold_metric(data=X[numeric_features], target=y)
        return self

    def transform(self, X, y=None):
        """
        # ToDO
        """
        scores = self.scores
        scores["Selected"] = 0
        mask = (scores[["train-importance", "valid-importance"]] >= self.threshold).max(
            axis=1
        )
        additive_mask = (scores["abs_delta"] <= self.abs_difference) & (
            scores["rel_delta"] <= self.rel_difference
        )
        mask = (mask) & (additive_mask)
        scores.loc[mask, "Selected"] = 1
        scores = scores.fillna(0)

        if self.cat_features:
            cat_scores = pd.DataFrame(
                {
                    "Variable": self.cat_features,
                    "train-importance": CATEGORY,
                    "valid-importance": CATEGORY,
                    "abs_delta": CATEGORY,
                    "rel_delta": CATEGORY,
                    "Selected": 1,
                }
            )
            scores = scores.append(cat_scores)

        mask = scores["Selected"] == 1
        self.used_features = scores.loc[mask, "Variable"].tolist()

        return scores, self.used_features


class DecisionTreeFeatureSelectionCV(BaseEstimator, TransformerMixin):
    """
    Отбор признаков с помощью решающего дерева на кросс-валидации.

    Parameters
    ----------
    cv: sklearn.model_selection.generator
        Генератор для разбиения данных в рамках кросс-валидации.

    threshold: int, optional, default = 5
        Порог для отбора признаков. Опциональный параметр.
        По умолчанию, используется значение threshold = 5.

    cat_features: List[str], optional, default = None
        Список категориальных признаков. Опциональный параметр.
        По умолчанию, категориальные признаки не используются.

    """

    def __init__(
        self,
        cv,
        group_column: str,
        threshold: np.number = 5,
        cat_features: Optional[List[str]] = None,
        abs_difference: np.number = 10,
        rel_difference: np.number = 30,
    ):

        self.cv = cv
        self.group_column = group_column
        self.threshold = threshold
        self.cat_features = cat_features
        self.const = np.finfo(np.float32).min
        self.abs_difference = abs_difference
        self.rel_difference = rel_difference
        self.used_features = None
        self.scores = None

    @staticmethod
    def _to_frame(data: dict, prefix: str = "train") -> pd.DataFrame:
        """
        # ToDO
        """
        if prefix:
            prefix = f"{prefix}-"

        importance = pd.Series(data)
        importance = importance.to_frame().reset_index()
        importance.columns = ["Variable", f"{prefix}importance"]

        return importance

    def _calculate_metric(self, data, target):
        """
        # ToDO
        """
        scores = {}
        for feature in data.columns:

            feature_ = data[feature]
            feature_ = feature_.fillna(self.const).values.reshape(-1, 1)
            tree = DecisionTreeClassifier(max_depth=3, random_state=27)
            tree.fit(feature_, target)

            prediction = tree.predict_proba(feature_)[:, 1]

            score = metrics_mapping["gini"]()(y_true=target, y_pred=prediction)
            scores[feature] = 100 * np.abs(score)

        return scores

    def fold_calculate(self, data, importance, target, train_idx, valid_idx):
        x_train, x_valid = data.loc[train_idx], data.loc[valid_idx]
        y_train, y_valid = target.loc[train_idx], target.loc[valid_idx]
        fold_train_importance = self._calculate_metric(data=x_train, target=y_train)
        fold_valid_importance = self._calculate_metric(data=x_valid, target=y_valid)
        fold_train_importance = self._to_frame(fold_train_importance, prefix="train")
        fold_valid_importance = self._to_frame(fold_valid_importance, prefix="valid")
        fold_importance = pd.concat(
            [fold_train_importance, fold_valid_importance], axis=1
        )
        importance = pd.concat([importance, fold_importance])
        return importance

    def _calculate_fold_metric(self, data, target):
        """
        # ToDO
        """
        importance = pd.DataFrame()
        if self.group_column is not None and str(self.group_column).strip():
            for train_idx, valid_idx in tqdm(self.cv.split(splitter_df)):
                importance = self.fold_calculate(
                    data, importance, target, train_idx, valid_idx
                )
        else:
            for train_idx, valid_idx in tqdm(self.cv.split(splitter_df)):
                importance = self.fold_calculate(
                    data, importance, target, train_idx, valid_idx
                )

        importance = importance.iloc[:, 1:]
        importance = importance.groupby(["Variable"])
        importance = importance[["train-importance", "valid-importance"]].mean()
        importance = importance.reset_index().sort_values(
            by="valid-importance", ascending=False
        )
        importance = importance.reset_index(drop=True)

        importance["abs_delta"] = (
            importance["train-importance"] - importance["valid-importance"]
        )
        importance["abs_delta"] = np.abs(importance["abs_delta"])

        importance["rel_delta"] = (
            importance["abs_delta"] / importance["train-importance"]
        )
        importance = importance.fillna(0)

        return importance

    def fit(self, X, y):
        """
        # ToDO
        """
        if self.cat_features:
            missed_columns = list(set(self.cat_features) - set(X.columns))
            if missed_columns:
                raise MissedColumnError(
                    f"Missed {list(missed_columns)} columns in data."
                )
            numeric_features = list(set(X.columns) - set(self.cat_features))
        else:
            numeric_features = X.columns

        self.scores = self._calculate_fold_metric(data=X[numeric_features], target=y)
        return self

    def transform(self, X, y=None):
        """
        # ToDO
        """
        scores = self.scores
        scores["Selected"] = 0
        mask = (scores[["train-importance", "valid-importance"]] >= self.threshold).max(
            axis=1
        )
        additive_mask = (scores["abs_delta"] <= self.abs_difference) & (
            scores["rel_delta"] <= self.rel_difference
        )
        mask = (mask) & (additive_mask)
        scores.loc[mask, "Selected"] = 1
        scores = scores.fillna(0)

        if self.cat_features:
            cat_scores = pd.DataFrame(
                {
                    "Variable": self.cat_features,
                    "train-importance": CATEGORY,
                    "valid-importance": CATEGORY,
                    "abs_delta": CATEGORY,
                    "rel_delta": CATEGORY,
                    "Selected": 1,
                }
            )
            scores = scores.append(cat_scores)

        mask = scores["Selected"] == 1
        self.used_features = scores.loc[mask, "Variable"].tolist()

        return scores, self.used_features