from typing import Any
from copy import deepcopy

import pandas as pd
import numpy as np

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.calibration import CalibratedClassifierCV
from sklearn.multiclass import OneVsRestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.tree import DecisionTreeClassifier


class MultiLabelCalibrationWrapper:
    def __init__(self, calibration_class: Any):
        self.calibration_class = calibration_class
        self.calibration_models = {}
        self.classes = None

    def fit(self, y_pred: pd.DataFrame, y_true: pd.DataFrame):
        self.classes = y_true.columns.tolist()
        for class_idx, class_name in enumerate(self.classes):
            y_true_ = y_true.iloc[:, class_idx]
            y_pred_ = y_pred[:, class_idx]
            calib_model = deepcopy(self.calibration_class).fit(y_pred_, y_true_)
            self.calibration_models[class_name] = calib_model
        return self

    def transform(self, y_pred):
        y_pred_calibrated = pd.DataFrame()
        y_pred = y_pred.values if isinstance(y_pred, pd.DataFrame) else y_pred

        for class_idx, class_name in enumerate(self.classes):
            calib_model = self.calibration_models[class_name]
            y_pred_ = y_pred[:, class_idx]
            y_pred_calibrated[class_name] = calib_model.transform(y_pred_)
        return y_pred_calibrated

    def get_equation(self):
        equations_by_each_class = {}
        for class_name, calibration in self.calibration_models.items():
            if hasattr(calibration, "get_equation"):
                equations_by_each_class[class_name] = calibration.get_equation()
        return equations_by_each_class


class DecisionTreeCalibrationForMultiLabel(BaseEstimator, TransformerMixin):
    """
    Выполнение калибровки решеающим деревом и sklearn.calibration.CalibratedClassifierCV
    для MultiLabel.
    """

    def __init__(
        self,
        model,
        tree_max_depth=5,
        rs=17,
        n_jobs: int = None,
        calib_method: str = "sigmoid",
    ):
        self.model = model
        self.rs = rs
        self.dt_calib = DecisionTreeClassifier(
            max_depth=tree_max_depth, random_state=rs
        )

        self.logits = {}
        self.n_jobs = n_jobs
        self.calib_method = calib_method
        self.classes = None

    def fit(self, X: pd.DataFrame, y: pd.DataFrame):

        self.classes = y.columns.tolist()
        self.dt_calib = OneVsRestClassifier(self.dt_calib, n_jobs=self.n_jobs)
        self.dt_calib = CalibratedClassifierCV(
            base_estimator=self.dt_calib,
            cv=None,
            method=self.calib_method,
        )
        self.dt_calib = MultiOutputClassifier(self.dt_calib, n_jobs=self.n_jobs)
        self.dt_calib.fit(X[self.model.used_features], y)

    def transform(self, X: pd.DataFrame):
        y_calib = self.dt_calib.predict_proba(X[self.model.used_features])
        y_calib = np.array([preds_by_class[:, 1] for preds_by_class in y_calib]).T
        return pd.DataFrame(data=y_calib, columns=self.classes)