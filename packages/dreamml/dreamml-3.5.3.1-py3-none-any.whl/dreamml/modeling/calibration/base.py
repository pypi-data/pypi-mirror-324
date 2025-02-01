import numpy as np
import pandas as pd

from typing import Callable, Tuple, Iterable, Any, Union

from copy import deepcopy

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.metrics import log_loss, mean_squared_error

from dreamml.modeling.metrics.metrics_mapping import metrics_mapping
from dreamml.modeling.calibration.binary_algorithms import (
    IsotonicCalibration,
    LinearCalibration,
    LogisticCalibration,
    DecisionTreeCalibration,
)
from dreamml.modeling.calibration.multilabel_algorithms import (
    DecisionTreeCalibrationForMultiLabel,
    LogisticCalibrationForMultiLabel,
    IsotonicCalibrationForMultilabel,
    LinearCalibrationForMultilabel,
)
from dreamml.logging import get_logger

_logger = get_logger(__name__)


class Calibration(BaseEstimator, TransformerMixin):
    """
    Класс-интерфейс для доступа к реализациям калибровки по единому api
    Parameters
    ----------
    model : Callable
        Модель для калибровки
    used_features : list
        Список фич отобранных исходя из значений конкретной метрики

    Attributes
    ----------
    model : Callable
        Модель для калибровки
    used_features : list
        Список фич отобранных исходя из значений конкретной метрики
    categorical_features : list
        Список категориальных фич

    """

    def __init__(
        self,
        model: Callable,
        method: str = "isotonic",
        is_weighted: bool = False,
        used_features: list = None,
    ):
        self.task = None
        if (
            hasattr(model, "predict")
            or hasattr(model, "predict_proba")
            or hasattr(model, "transform")
        ):
            self.model = deepcopy(model)
            self.method = method
            self.is_weighted = is_weighted
            self.used_features = used_features
            if used_features is None:
                self.used_features = getattr(self.model, "used_features", [])
            self.categorical_features = getattr(self.model, "categorical_features", [])
        else:
            raise AttributeError(
                "Model object must support prediction API via"
                " one of the methods: 'predict',"
                " 'predict_proba' or 'transform'"
            )

    def get_task_type(self, y: Union[pd.Series, pd.DataFrame]):
        if isinstance(y, pd.Series):
            unique_values = y.dropna().nunique()
            task = "binary" if unique_values == 2 else "multiclass"

        elif isinstance(y, pd.DataFrame):
            y_clean = y.dropna()
            if (
                not y_clean.empty
                and y_clean.applymap(lambda x: x in [0, 1]).all().all()
            ):
                task = "multilabel"
            else:
                raise ValueError(
                    f"Task MultiLabel with NaN values in target labels is not supported."
                )
        else:
            raise ValueError(
                f"Expected pd.DataFrame or pd.Series dtype, but got {type(y)}."
            )
        return task

    def get_y_pred(self, x: pd.DataFrame) -> Union[pd.Series, pd.DataFrame]:
        is_dreamml_model = (
            True if self.model.__module__.startswith("dreamml.modeling") else False
        )

        x = x[self.used_features] if is_dreamml_model else x

        if hasattr(self.model, "transform"):
            y_pred = self.model.transform(x)

        elif hasattr(self.model, "predict_proba"):
            y_pred = (
                self.model.predict_proba(x)[:, 1]
                if self.task == "binary"
                else self.model.predict_proba(x)
            )

        elif hasattr(self.model, "predict"):
            y_pred = self.model.predict(x)

        else:
            raise AttributeError(
                "Model object must support prediction API via"
                " one of the methods: 'predict',"
                " 'predict_proba' or 'transform'"
            )
        return y_pred

    def fit(self, x: pd.DataFrame, y: Union[pd.Series, pd.DataFrame]):

        self.task = self.get_task_type(y)

        if self.task == "binary":
            self._fit_binary(x, y)
        elif self.task == "multilabel":
            self._fit_multilabel(x, y)
        else:
            raise ValueError(
                f"Supports only binary, multilabel tasks, but got {self.task}"
            )

    def _fit_binary(self, x: pd.DataFrame, y: pd.Series):
        y_pred = self.get_y_pred(x)

        # изотоническая регрессия на наблюдениях
        if self.method == "isotonic":
            self.calibrator = IsotonicCalibration()
            self.calibrator.fit(y_pred, y)

        # логистическая регрессия на наблюдениях
        elif self.method == "logistic":
            # обучение логистической регрессии на наблюдениях
            self.calibrator = LogisticCalibration()
            self.calibrator.fit(y_pred, y)

        # линейная регрессия на бакетах
        elif self.method == "linear":
            self.calibrator = LinearCalibration(is_weighted=self.is_weighted)
            self.calibrator.fit(y_pred, y)

        # линейная регрессия на шансах
        elif self.method == "linear-odds":
            self.calibrator = LinearCalibration(
                is_odds=True, is_weighted=self.is_weighted
            )
            self.calibrator.fit(y_pred, y)

        # линейная регрессия на логарифме шансов
        elif self.method == "linear-ln-odds":
            self.calibrator = LinearCalibration(
                is_logit=True, is_weighted=self.is_weighted
            )
            self.calibrator.fit(y_pred, y)

        # логистическая регрессия на шансах
        elif self.method == "logistic-odds":
            self.calibrator = LogisticCalibration(is_odds=True)
            self.calibrator.fit(y_pred, y)

        # логистическая регрессия на логарифме шансов
        elif self.method == "logistic-ln-odds":
            self.calibrator = LogisticCalibration(is_logit=True)
            self.calibrator.fit(y_pred, y)

        # решающее дерево с линейными моделями в листах
        elif self.method == "dtree":
            self.calibrator = DecisionTreeCalibration(
                self.model,
            )
            self.calibrator.fit(x, y)

    def _fit_multilabel(self, x: pd.DataFrame, y: pd.DataFrame):
        y_pred = self.get_y_pred(x)

        # изотоническая регрессия на наблюдениях
        if self.method == "isotonic":
            self.calibrator = IsotonicCalibrationForMultilabel()
            self.calibrator.fit(y_pred, y)

        # решающее дерево с линейными моделями в листах
        if self.method == "dtree-sigmoid":
            check_nan_values(y)
            self.calibrator = DecisionTreeCalibrationForMultiLabel(
                self.model, calib_method="sigmoid"
            )
            self.calibrator.fit(x, y)

        # решающее дерево с линейными моделями в листах
        elif self.method == "dtree-isotonic":
            check_nan_values(y)
            self.calibrator = DecisionTreeCalibrationForMultiLabel(
                self.model, calib_method="isotonic"
            )
            self.calibrator.fit(x, y)

        # логистическая регрессия на наблюдениях
        elif self.method == "logistic":
            # обучение логистической регрессии на наблюдениях
            self.calibrator = LogisticCalibrationForMultiLabel()
            self.calibrator.fit(y_pred, y)

        # логистическая регрессия на шансах
        elif self.method == "logistic-odds":
            self.calibrator = LogisticCalibrationForMultiLabel(is_odds=True)
            self.calibrator.fit(y_pred, y)

        # логистическая регрессия на логарифме шансов
        elif self.method == "logistic-ln-odds":
            self.calibrator = LogisticCalibrationForMultiLabel(is_logit=True)
            self.calibrator.fit(y_pred, y)

        # линейная регрессия на бакетах
        elif self.method == "linear":
            self.calibrator = LinearCalibrationForMultilabel(
                is_weighted=self.is_weighted
            )
            self.calibrator.fit(y_pred, y)

        # линейная регрессия на шансах
        elif self.method == "linear-odds":
            self.calibrator = LinearCalibrationForMultilabel(
                is_odds=True, is_weighted=self.is_weighted
            )
            self.calibrator.fit(y_pred, y)

        # линейная регрессия на логарифме шансов
        elif self.method == "linear-ln-odds":
            self.calibrator = LinearCalibrationForMultilabel(
                is_logit=True, is_weighted=self.is_weighted
            )
            self.calibrator.fit(y_pred, y)

    def get_equation(self):
        if hasattr(self.calibrator, "get_equation"):
            return self.calibrator.get_equation()

    def evaluate(self, **kwargs):
        for ds_name, (x, y) in kwargs.items():
            y_pred = self.get_y_pred(x)
            if (
                self.method in ["dtree-sigmoid", "dtree-isotonic"]
                and self.task == "multilabel"
            ):
                y_calibrated = self.calibrator.transform(x)
            else:
                y_calibrated = self.calibrator.transform(y_pred)

            if self.task in ["multiclass", "multilabel"]:
                y = y.values if isinstance(y, pd.DataFrame) else y
                y_pred = y_pred.values if isinstance(y_pred, pd.DataFrame) else y_pred
                y_calibrated = (
                    y_calibrated.values
                    if isinstance(y_calibrated, pd.DataFrame)
                    else y_calibrated
                )
                brier = np.nanmean(
                    [
                        mean_squared_error(
                            y[~np.isnan(y[:, i]), i], y_pred[~np.isnan(y[:, i]), i]
                        )
                        for i in range(y.shape[1])
                    ]
                )
                brier_calib = np.nanmean(
                    [
                        mean_squared_error(
                            y[~np.isnan(y[:, i]), i],
                            y_calibrated[~np.isnan(y[:, i]), i],
                        )
                        for i in range(y.shape[1])
                    ]
                )
                logloss = np.nanmean(
                    [
                        log_loss(
                            y[~np.isnan(y[:, i]), i],
                            y_pred[~np.isnan(y[:, i]), i],
                            eps=1e-5,
                        )
                        for i in range(y.shape[1])
                    ]
                )
                logloss_calib = np.nanmean(
                    [
                        log_loss(
                            y[~np.isnan(y[:, i]), i],
                            y_calibrated[~np.isnan(y[:, i]), i],
                            eps=1e-5,
                        )
                        for i in range(y.shape[1])
                    ]
                )

            else:
                brier = mean_squared_error(y, y_pred)
                brier_calib = mean_squared_error(y, y_calibrated)
                logloss = log_loss(y, y_pred, eps=1e-5)
                logloss_calib = log_loss(y, y_calibrated, eps=1e-5)

            _logger.info(
                f"{ds_name} \t Brier: {round(brier, 8)} \t "
                f"Brier calibrated: {round(brier_calib, 8)} "
            )
            _logger.info(
                f"{ds_name} \t logloss: {round(logloss, 8)} \t"
                f" logloss calibrated: {round(logloss_calib, 8)} "
            )

    def transform(self, x: pd.DataFrame):
        if (
            self.method in ["dtree-sigmoid", "dtree-isotonic"]
            and self.task == "multilabel"
        ):
            y_calibrated = self.calibrator.transform(x)
        else:
            y_pred = self.get_y_pred(x)
            y_calibrated = self.calibrator.transform(y_pred)

        return y_calibrated

    def evaluate_model(self, reg_metric: bool = False, **eval_sets):
        """
        Печать в стандартный поток вывода оценки качества модели на eval_sets
        Для задачи бинарной классификации используется метрика GINI
        В словаре metrics под ключом названия метрики
        содержится функция её расчёта и количество знаков,
        до которых произойдёт округление

        Parameters
        ----------
        reg_metric: bool
            Флаг использовать метрики для оценки качества решения задачи регрессии
            или нет
        eval_sets: Dict[string, Tuple[pandas.DataFrame, pandas.Series]]
            Словарь, где ключ - название выборки, значение - кортеж с
            матрицей признаков и вектором истинных ответов.
        """

        metrics_to_eval = {}

        if not reg_metric:
            metrics_to_eval["GINI"] = metrics_mapping["gini"](task=self.task)

        elif reg_metric:
            metrics_to_eval = {
                "MAE": metrics_mapping["mae"](),
                "R2": metrics_mapping["r2"](),
                "RMSE": metrics_mapping["rmse"](),
            }

        for sample in eval_sets:
            data, y_true = eval_sets[sample]
            y_pred = self.transform(data)

            scores = {}
            for name, metric in metrics_to_eval.items():
                try:
                    scores[name] = metric(y_true, y_pred)
                except (ValueError, KeyError, IndexError):
                    scores[name] = np.nan

            metrics_output = ", ".join(
                [f"{name} = {value:.2f}" for name, value in scores.items()]
            )
            output_per_sample = f"{sample}-score: \t {metrics_output}"

            _logger.info(output_per_sample)


def signal_last(it: Iterable[Any]) -> Iterable[Tuple[bool, Any]]:
    """
    Функция, отвечающая за отслеживания последней итерации в цикле
     https://betterprogramming.pub/is-this-the-last-element-of-my-python-for-loop-784f5ff90bb5
    Parameters
    ----------
    it : Iterable[Any]
        Любой итерируемый объект
    Returns
    -------
    Iterable[Tuple[bool, Any]]
        Возвращает кортеж с двумя значениями
        Флаг, является ли итерация в цикле последней: True - да, False - нет
        ret_var - Элемент итерируемого объекта

    """
    iterable = iter(it)
    ret_var = next(iterable)
    for val in iterable:
        yield False, ret_var
        ret_var = val
    yield True, ret_var


def check_nan_values(y_true: pd.DataFrame):
    if y_true.isna().sum().sum() > 0:
        raise ValueError(
            "Калибровка модели с NaN значениями в таргете не поддерживается."
        )


def calculate_macro_score_with_nan_values(
    score_function: Callable,
    y_true: Union[pd.DataFrame, np.ndarray],
    y_pred: Union[pd.DataFrame, np.ndarray],
    eps: float = None,
):
    """
    Расчет macro метрики с/без NaN значениями для задачи MultiLabel Classification.

    Parameters
    ----------
    y_true: np.ndarray - матрица таргетов (n_samples, n_classes)
    y_pred: np.ndarray - матрица предсказанных вероятностей (n_samples, n_classes)

    Returns
    -------
    Macro метрика по всем классам
    """
    y_true = y_true.values if isinstance(y_true, pd.DataFrame) else y_true
    y_pred = y_pred.values if isinstance(y_pred, pd.DataFrame) else y_pred

    metric_list = []
    num_classes = y_true.shape[1]
    mask = ~np.isnan(y_true)

    for class_idx in range(num_classes):
        mask_by_class_idx = mask[:, class_idx]
        y_true_idx_class = y_true[:, class_idx][mask_by_class_idx]
        y_pred_idx_class = y_pred[:, class_idx][mask_by_class_idx]

        if len(np.unique(y_true_idx_class)) == 1:
            continue
        if len(np.unique(y_pred_idx_class)) == 1:
            metric_list.append(
                0
            )  # FIXME: непонятно как считается macro метрика. Посмотреть реализацию в sklearn.
            continue
            # FIXME: не должно быть в y_pred_idx_class одно уникальное значение
        if eps is not None:
            metric_list.append(
                score_function(
                    y_true=y_true_idx_class, y_pred=y_pred_idx_class, eps=eps
                )
            )
        else:
            metric_list.append(
                score_function(y_true=y_true_idx_class, y_pred=y_pred_idx_class)
            )
    return np.mean(metric_list)