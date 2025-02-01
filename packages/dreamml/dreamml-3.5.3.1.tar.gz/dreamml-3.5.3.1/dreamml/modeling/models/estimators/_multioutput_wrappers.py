from collections import defaultdict
from typing import List, Tuple, Dict, Callable, Union

import numpy as np
import pandas as pd
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import LabelBinarizer
from sklearn.utils.fixes import delayed
from sklearn.base import clone
from joblib import Parallel


class OneVsRestClassifierWrapper(OneVsRestClassifier):
    def __init__(
        self,
        estimator,
        *,
        n_jobs=None,
        verbose=0,
        get_best_iteration_func: Callable,
        n_estimators: Union[int, List[int]]
    ):
        super().__init__(estimator=estimator, n_jobs=n_jobs)
        self.verbose = verbose
        self._best_iteration_per_binary: List[int] = []
        self.get_best_iteration_func = get_best_iteration_func
        self.n_estimators = n_estimators

    def _fit_binary(self, estimator, X, y, class_idx: int, **fit_params):
        """Fit a single binary estimator."""
        unique_y = np.unique(y)
        if len(unique_y) == 1:
            raise ValueError("The number of classes must be greater than 1.")
        else:
            estimator = clone(estimator)

            estimator.set_params(n_estimators=self.n_estimators[class_idx])
            estimator.fit(X, y, **fit_params)
            best_iteration = self.get_best_iteration_func(estimator)

        return estimator, class_idx, best_iteration

    def _init_sklearn_label_binarizer(self, y):
        self.label_binarizer_ = LabelBinarizer(sparse_output=True)
        self.label_binarizer_.fit_transform(y)
        self.classes_ = self.label_binarizer_.classes_

    def _remove_nan_values(
        self,
        eval_set_for_class_idx: List[Tuple[pd.DataFrame, pd.Series]],
        X: pd.DataFrame,
        y_slice_for_class_idx: pd.Series,
    ):
        """
        Обертка OVR используется в случае наличия None значений в таргете.
        Игнорируем строки с None значениями в таргете для обучения и валидации.
        """
        mask_y = y_slice_for_class_idx.isna()
        X = X[~mask_y]
        y_slice_for_class_idx = y_slice_for_class_idx[~mask_y]

        for idx, (X_sample, y_sample) in enumerate(eval_set_for_class_idx):
            mask_y_sample = y_sample.isna()
            X_sample = X_sample[~mask_y_sample]
            y_sample = y_sample[~mask_y_sample]
            eval_set_for_class_idx[idx] = (X_sample, y_sample)

        return eval_set_for_class_idx, X, y_slice_for_class_idx

    def fit(self, X, y, **fit_params):

        num_classes = y.shape[1]
        self._best_iteration_per_binary = [0 for _ in range(num_classes)]

        if isinstance(self.n_estimators, int):
            self.n_estimators = [self.n_estimators for _ in range(num_classes)]

        eval_set = fit_params.pop("eval_set", [(X, y)])
        eval_set_sliced = get_eval_set_sliced(eval_set, num_classes)

        self._init_sklearn_label_binarizer(y.fillna(value=0))

        delayed_func_kwargs_list = []
        for class_idx in range(num_classes):
            eval_set_for_class_idx = eval_set_sliced[class_idx]
            y_slice_for_class_idx = (
                y.iloc[:, class_idx] if isinstance(y, pd.DataFrame) else y[:, class_idx]
            )

            eval_set_for_class_idx, X_without_nan, y_slice_for_class_idx = (
                self._remove_nan_values(
                    eval_set_for_class_idx, X, y_slice_for_class_idx
                )
            )

            fit_params["eval_set"] = eval_set_for_class_idx
            y_slice = y_slice_for_class_idx

            delayed_func_kwargs = dict(
                estimator=self.estimator,
                X=X_without_nan,
                y=y_slice,
                class_idx=class_idx,
                **fit_params
            )
            delayed_func_kwargs_list.append(delayed_func_kwargs)

        parallel = Parallel(n_jobs=self.n_jobs, verbose=self.verbose)

        delayed_func = delayed(self._fit_binary)

        artifacts = parallel(
            delayed_func(**kwargs) for kwargs in delayed_func_kwargs_list
        )

        self.estimators_ = [artifact[0] for artifact in artifacts]
        for estimator, class_idx, best_iteration in artifacts:
            self._best_iteration_per_binary[class_idx] = best_iteration

        if hasattr(self.estimators_[0], "n_features_in_"):
            self.n_features_in_ = self.estimators_[0].n_features_in_
        if hasattr(self.estimators_[0], "feature_names_in_"):
            self.feature_names_in_ = self.estimators_[0].feature_names_in_

        return self

    @property
    def best_iteration(self) -> List[int]:
        return self._best_iteration_per_binary


def get_eval_set_sliced(
    eval_sets: List[Tuple[pd.DataFrame, pd.DataFrame]], num_classes: int
) -> Dict[int, List[Tuple[pd.DataFrame, pd.Series]]]:
    """
    eval_set: [(X, y), (X_valid, y_valid)]

    Хотим для каждого класса получить список: [(X, y_sliced), (X_valid, y_valid_sliced)],
    где y_sliced - колонка таргета
    """

    eval_sets_by_class_idx = defaultdict(list)
    for X, y in eval_sets:
        for class_idx in range(num_classes):
            y_slice = (
                y.iloc[:, class_idx] if isinstance(y, pd.DataFrame) else y[:, class_idx]
            )

            eval_sets_by_class_idx[class_idx].append((X, y_slice))

    return eval_sets_by_class_idx