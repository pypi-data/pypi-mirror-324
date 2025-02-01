import pandas as pd
import numpy as np
from scipy.special import logit, expit

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.tree import DecisionTreeClassifier

from dreamml.modeling.metrics.utils import calculate_quantile_bins


class IsotonicCalibration(BaseEstimator, TransformerMixin):
    """
    Построение модели изотонической регресии на наблюдениях:
    y_pred -> y_target
    """

    def __init__(self):
        self.calibration = IsotonicRegression(out_of_bounds="clip")

    def fit(self, y_pred: pd.Series, y_true: pd.Series):
        self.calibration.fit(y_pred, y_true)
        return self

    def transform(self, y_pred):
        return self.calibration.transform(y_pred)


class LogisticCalibration(BaseEstimator, TransformerMixin):
    """
    Построение модели логистической регресии
    y_pred -> y_target
    """

    def __init__(self, is_logit=False, is_odds=False):
        self.calibration = LogisticRegression()
        self.is_logit = is_logit
        self.is_odds = is_odds

    def _fit_odds(self, y_pred: pd.Series, y_true: pd.Series):
        x = np.array(y_pred / (1 - y_pred)).reshape(-1, 1)
        self.calibration.fit(x, y_true)

    def _fit_logit(self, y_pred: pd.Series, y_true: pd.Series):
        x = logit(np.array(y_pred).reshape(-1, 1))
        self.calibration.fit(x, y_true)

    def _fit_logreg(self, y_pred: pd.Series, y_true: pd.Series):
        x = np.array(y_pred).reshape(-1, 1)
        self.calibration.fit(x, y_true)

    def fit(self, y_pred: pd.Series, y_true: pd.Series):

        if self.is_odds:
            self._fit_odds(y_pred, y_true)
        elif self.is_logit:
            self._fit_logit(y_pred, y_true)
        else:
            self._fit_logreg(y_pred, y_true)

        return self

    def get_equation(self):
        k = float(self.calibration.coef_)
        b = float(self.calibration.intercept_)

        if self.is_odds:
            return f"1/(1+ exp(-{k}*(x/1-x) + {b}))"
        elif self.is_logit:
            return f"1/(1+ exp(-{k}*ln(x/1-x) + {b}))"
        else:
            return f"1/(1+exp(-{k}*x + {b}))"

    def transform(self, y_pred):
        if self.is_odds:
            x = np.array(y_pred / (1 - y_pred)).reshape(-1, 1)
        elif self.is_logit:
            x = logit(np.array(y_pred).reshape(-1, 1))
        else:
            x = np.array(y_pred).reshape(-1, 1)

        return self.calibration.predict_proba(x)[:, 1]


class LinearCalibration(BaseEstimator, TransformerMixin):
    """
    Построение модели линейной регресии на средних из бинов прогноза
    y_bin_mean_prediction -> y_bin_mean_target
    """

    def __init__(
        self, is_weighted: bool = False, is_logit: bool = False, is_odds=False
    ):
        self.calibration = LinearRegression()
        self.is_weighted = is_weighted
        self.is_logit = is_logit
        self.is_odds = is_odds

    def fit(self, y_pred, y_true):

        # данные для обучения
        pred_df = pd.DataFrame({"y_true": y_true, "y_pred": y_pred})
        pred_df["pred_bin"] = calculate_quantile_bins(
            y_pred, 20, percentile_implementation=True
        )
        pred_df_grouped = pred_df.groupby(by="pred_bin").agg(
            {"y_pred": "mean", "y_true": ["mean", "sum"]}
        )

        pred_df_grouped.columns = ["y_pred", "y_true", "#events"]
        pred_df_grouped["events_share"] = (
            pred_df_grouped["#events"] / pred_df_grouped["#events"].sum()
        )

        # handling critical values
        pred_df_grouped["y_pred"].replace({1: 0.9999, 0: 0.0001}, inplace=True)
        pred_df_grouped["y_true"].replace({1: 0.9999, 0: 0.0001}, inplace=True)

        x = np.array(pred_df_grouped["y_pred"]).reshape(-1, 1)
        y = pred_df_grouped["y_true"]

        # запомнить средний ER в бине прогноза - для взвешивания
        weights = pred_df_grouped["events_share"]

        if self.is_odds:
            x = np.array(x / (1 - x))
            y = np.array(y / (1 - y))

        if self.is_logit:
            x = logit(x)
            y = logit(y)

        if self.is_weighted:
            self.calibration.fit(x, y, sample_weight=weights)
        else:
            self.calibration.fit(x, y)

        return self

    def get_equation(self):
        k = float(self.calibration.coef_)
        b = float(self.calibration.intercept_)

        if self.is_odds:
            return f"y_odds = {k}*(x/(1-x)) + {b}"
        elif self.is_logit:
            return f"y_ln_odds = {k}*ln(x/1-x) + {b}"
        else:
            return f"y = {k}*x + {b}"

    def transform(self, y_pred):
        x = np.array(y_pred).reshape(-1, 1)

        if self.is_logit:
            x = logit(x)
            pred = self.calibration.predict(x)
            pred = expit(pred)

        elif self.is_odds:
            x = x / (1 - x)
            pred = self.calibration.predict(x)
            pred = pred / (pred + 1)
        else:
            pred = self.calibration.predict(x)

        return pred


class DecisionTreeCalibration(BaseEstimator, TransformerMixin):
    """
    Выполнение калибровки решеающим деревом и линейными моделями в листах
    """

    def __init__(self, model, tree_max_depth=3, rs=17):
        self.model = model
        self.rs = rs
        self.dt_calib = DecisionTreeClassifier(
            max_depth=tree_max_depth, random_state=rs
        )
        self.logits = {}

    def fit(self, X: pd.DataFrame, y: pd.Series):

        # Обучить дерево решений
        self.dt_calib.fit(X[self.model.used_features], y)
        leafs = self.dt_calib.apply(X[self.model.used_features])

        # Обучить логистическую регрессию для каждого листа
        for leaf in np.unique(leafs):
            lr = LogisticRegression(random_state=self.rs)

            X_sub = X[leafs == leaf]
            y_pred_sub = self.model.transform(X_sub)
            y_sub = y[leafs == leaf]

            lr.fit(y_pred_sub.reshape(-1, 1), y_sub)
            self.logits[leaf] = lr

    def transform(self, X: pd.DataFrame):

        pred_df = pd.DataFrame(
            {
                "y_pred": self.model.transform(X),
                "leaf": self.dt_calib.apply(X[self.model.used_features]),
            },
            index=X.index,
        )

        y_calib = pd.Series()

        # для каждого листа применить свой логит
        for lf in np.unique(pred_df.leaf):
            idx_sub = pred_df[pred_df.leaf == lf].index
            y_pred_sub = np.array(pred_df[pred_df.leaf == lf].y_pred).reshape(-1, 1)

            y_calib_sub = pd.Series(
                self.logits[lf].predict_proba(y_pred_sub)[:, 1], index=idx_sub
            )

            y_calib = y_calib.append(y_calib_sub)
        return y_calib