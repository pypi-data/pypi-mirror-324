import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xgboost
from tqdm.auto import tqdm
from sklearn.model_selection import train_test_split

from dreamml.logging import get_logger
from dreamml.modeling.metrics import BaseMetric
from dreamml.utils._time import execution_time
from dreamml.reports.calibration.format_excel_writer import FormatExcelWriter
from dreamml.modeling.metrics.metrics_mapping import metrics_mapping

_logger = get_logger(__name__)


def _to_frame(X: pd.DataFrame, values: np.array, prefix: str) -> pd.DataFrame:
    """
    Функция для создания датафрейма с отранжированными значениями.
    Parameters:
    -----------
    X: pandas.DataFrame
        Матрица признаков.
    values: numpy.array
        Вектор с оценками важности признаков.
    prefix: string
        Префикс для колонки importance.
    Returns:
    --------
    df: pandas.DataFrame
        Датафрейм с отранжированными значениями.
    """
    df = pd.DataFrame({"feature": X.columns, f"{prefix}_importance": values})
    df = df.sort_values(by=f"{prefix}_importance", ascending=False)
    df = df.reset_index(drop=True)
    return df


def make_prediction(model_info: tuple, X: pd.DataFrame, task: str = "binary"):
    """
    Функция для построения pandas.DataFrame со значением целевой метки,
    прогнозами модели
    Parameters:
    -----------
    model_info: Tuple[sklearn.model, List[str]]
        Кортеж, первый элемент - обученный экземпляр модели,
        второй элемент - список используемых признаков модели.
    X: pandas.DataFrame
        Матрица признаков.
    y: pandas.Series
        Матрица целевой переменной.
    Returns:
    --------
    df: pandas.DataFrame
        Датафрейм с прогнозами.
    """
    estimator, features = model_info
    data = X[features]
    if isinstance(estimator, xgboost.core.Booster):
        # FIXME: old xgboost
        data = xgboost.DMatrix(data)
    if getattr(estimator, "transform", None):
        y_pred = estimator.transform(data)
    elif getattr(estimator, "predict_proba", None):
        if str(type(estimator)).endswith("RandomForestClassifier'>"):
            y_pred = estimator.predict_proba(data).fillna(-9999)[:, 1]
        else:
            y_pred = estimator.predict_proba(data)
            if task == "binary":
                y_pred = y_pred[:, 1]
    elif getattr(estimator, "predict", None):
        y_pred = estimator.predict(data)
    else:
        raise AttributeError(
            "Estimator must have `predict`, `predict_proba` or `transform` method"
        )
    return y_pred


def calculate_permutation_feature_importance(
    estimator,
    metric,
    y: pd.Series,
    X: pd.DataFrame,
    fraction_sample: float = 0.15,
    task: str = "binary",
) -> pd.DataFrame:
    """
    Функция для расчета важности переменных на основе перестановок.
    Подход к оценке важности признаков основан на изменении метрики
    при перемешивании значений данного признака. Если значение метрики
    уменьшается, значит признак важен для модели, если значение метрики
    увеличивается, то признак для модели не важен и его стоит исключить.
    Parameters:
    -----------
    estimator: sklearn.estimator
        Экземпляр модели, которая поддерживает API sklearn.
        Ожидается, что модель обучена, т.е. был вызван метод fit ранее.
    metric: func, sklearn.metrics
        Функция для оценки качества модели.
    X: pandas.DataFrame
        Матрица признаков.
    y: pandas.Series
        Вектор целевой переменной.
    fraction_sample: float, optional, default = 0.15
        Доля наблюдений от X для оценки важности признаков.
    Returns:
    --------
    X_transformed: pandas.DataFrame
        Преобразованная матрица признаков.
    """
    if fraction_sample > 1:
        raise ValueError(
            f"fraction_sample must be in range (0, 1], "
            f"but fraction_sample is {fraction_sample}"
        )
    if isinstance(X, pd.DataFrame):
        x = X.copy()
        x, _, y, _ = train_test_split(x, y, train_size=fraction_sample, random_state=1)
    else:
        raise TypeError(
            f"x_valid must be pandas.core.DataFrame, " f"but x_valid is {type(X)}"
        )
    feature_importance = np.zeros(x.shape[1])
    baseline_prediction = make_prediction(
        (estimator, x.columns),
        x,
        task,
    )

    baseline_score = metric(y, baseline_prediction)
    for num, feature in enumerate(tqdm(x.columns)):
        x[feature] = np.random.permutation(x[feature])
        score = metric(y, make_prediction((estimator, x.columns), x, task))
        feature_importance[num] = score
        x[feature] = X[feature]
    feature_importance = (baseline_score - feature_importance) / baseline_score  # * 100
    return _to_frame(x, feature_importance, "permutation")


def plot_permutation_importance(
    df: pd.DataFrame, x_column: str, save_path: str
) -> None:
    """
    Построение графика важности фич по перестановкам.
    Parameters:
    -----------
    df: pandas.DataFrame
        Датафрейм со списком фич (features) и значением
        permutation importance (permutation_importance)
    x_column: str
        имя колонки, со значениями, которые откладывать по оси X
    name: string
        Имя файла для сохранения графика.
    Returns:
    -----------
    lines:
        Список `.Line2D` объектов, графически представляющие данные.
    """
    plt.figure(figsize=(10, 6))
    plt.grid()
    n = len(df.columns) - 1
    color = iter(plt.cm.rainbow(np.linspace(0, 1, n)))
    leg = []
    for col in df.drop(x_column, axis=1).columns:
        c = next(color)
        plt.plot(df[x_column], df[col], c=c, linewidth=3, marker="o", markersize=12)
        leg.append(col)
    plt.legend(leg)
    plt.xticks(df[x_column], rotation="vertical")
    plt.xlabel(x_column)
    plt.ylabel("permutation_importance")
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight")


from abc import ABC, abstractmethod


class Checker(ABC):
    """
    Абстрактный класс - родитель, для всех классов реализаций валидационных проверок
    """

    def __init__(self):
        """
        Конструктор абстрактного класса - родителя
        """
        pass

    @abstractmethod
    def validate(self):
        """
        Абстрактный метод, реализующий единый интерфейс доступа к запуску процедуры проверки
        """
        pass


# Permutation importance class
class PermutationImportanceChecker(Checker):
    """
    Класс реализации проверки важности признаков на основе перестановок.
    Расчитывается относительное изменения метрики gini при случайном
    перемешивании значений признака. Проверка выполняется для каждого признака
    вошедшего в модель
    Parameters:
    ----------
    writer: pd.ExcelWriter
        Объект класса excel-writer для записи отчета (файл для отчета должен
        быть создан предварительно)
    model_name: str
        Имя модели для отображения в названи файлов
    model
        Объект scikit-learn like обученной модели
    features_list:list
        Список фичей, которые использует модель
    cat_features: list
        Список категориальных признаков
    drop_features: list
        Список мусорных признаков для исключения из анализа
    current_path: str
        Путь к рабочей директории для сохранения изображений и файла с отчетом
    """

    def __init__(
        self,
        writer: pd.ExcelWriter,
        model,
        features_list: list,
        cat_features: list,
        plot_size=(10, 10),
        current_path=None,
        images_dir_path=None,
        metric_name: str = "gini",
        metric_col_name: str = "gini",
        metric_params: dict = None,
        task: str = "binary",
    ):
        self.writer = writer
        # self.model_name = model_name
        self.features_list = features_list
        self.cat_features = cat_features
        # self.drop_features = drop_features
        self.model = model
        self.metric_name = metric_name
        self.metric: BaseMetric = metrics_mapping.get(metric_name)(
            task=task, **metric_params
        )
        self.metric_params = metric_params
        self.plot_size = plot_size
        self.images_dir_path = images_dir_path
        self.current_path = current_path
        self.task = task

    def _to_excel(self, df: pd.DataFrame, sheet_name: str, plot=False) -> None:
        """
        Функция записи датафрейма в excel файл на указанный лист и позицию
        Parameters:
        ----------
        df: pd.DataFrame
            Датафрейм для записи в файл
        sheet_name: str
            Имя листа, на который осуществить запись
        plot: bool
            Флаг необходимости добавить на страницу с отчетом график из файла
        """
        float_number_low = "## ##0.0000"
        # Кастомный формат для таблицы
        fmt = {
            "num_format": {
                float_number_low: [
                    "permutation_importance_test",
                    "permutation_importance_valid",
                    "permutation_importance_OOT",
                ]
            }
        }
        bold_row = {"bold": {True: df.index[df["feature"] == "factors_relevancy"]}}
        excelWriter = FormatExcelWriter(self.writer)
        excelWriter.write_data_frame(
            df, (0, 0), sheet=sheet_name, formats=fmt, row_formats=bold_row
        )
        # apply conditional format to highlight validation_report test results
        for col in [
            "permutation_importance_test",
            "permutation_importance_valid",
            "permutation_importance_OOT",
        ]:
            if col in df.columns:
                excelWriter.set_col_cond_format_tail(
                    df, (0, 0), col, lower=200, upper=0.0, order="reverse"
                )

        if plot:
            # Permutation importance plot
            sheet = self.writer.sheets[sheet_name]
            file_path = os.path.join(self.images_dir_path, f"{sheet_name}.png")
            sheet.insert_image(f"A{df.shape[0] + 4}", file_path)
        # Описание теста
        sheet.write_string(
            "E2",
            "Permutation importance - метрика важности "
            "признака в построенной модели",
        )
        sheet.write_string(
            "E3",
            "Считается как относительное изменение метрики"
            " качества модели ("
            + self.metric_name
            + ") при перемешивании значений признака",
        )
        sheet.write_string(
            "E5",
            "Factors relevancy - доля факторов с "
            "важностью 20% и более от фактора с максимальной важностью",
        )
        sheet.write_string("E7", "* - данный тест информативный")

    def _calc_perm_importance(self, **data) -> pd.DataFrame:
        """
        Расчет важности признаков вошедших в модели на основе метода
        перестановок.
        Считает на датасетах :
            test/valid
            oot
        Parameters:
        -----------
        **data: Dict[str, Tuple(pd.DataFrame, pd.Series)]
            Словарь, где ключ - название датасета, значение -
            кортеж из (X, y), X - матрица признаков,
            y - вектор истинных ответов.
        Returns:
        -------
        pd.DataFrame
            датасет с полсчитанной важностью признаков вида:
                - feature_name
                - Permutation importance test/valid
                - Permutatuin importance oot
        """
        X_test, y_test = data.get("test", (None, None))
        X_valid, y_valid = data.get("valid", (None, None))
        X_test2, y_test2 = data.get("test2", (None, None))
        X_OOT, y_OOT = data.get("OOT", (None, None))
        perm_importance_final = pd.DataFrame()
        # Посчитать PI на test или valid
        if X_test is not None:
            perm_importance_final = calculate_permutation_feature_importance(
                self.model,
                self.metric,
                X=X_test[self.features_list],
                y=y_test,
                fraction_sample=0.95,
                task=self.task,
            )
            perm_importance_final.rename(
                columns={"permutation_importance": "permutation_importance_test"},
                inplace=True,
            )
            perm_importance_final.set_index("feature", inplace=True)
        elif X_valid is not None:
            perm_importance_final = calculate_permutation_feature_importance(
                self.model,
                self.metric,
                X=X_valid[self.features_list],
                y=y_valid,
                fraction_sample=0.95,
                task=self.task,
            )
            perm_importance_final.rename(
                columns={"permutation_importance": "permutation_importance_valid"},
                inplace=True,
            )
            perm_importance_final.set_index("feature", inplace=True)
        # Посчитать PI на OOT при наличии
        if X_OOT is not None:
            perm_importance = calculate_permutation_feature_importance(
                self.model,
                self.metric,
                X=X_OOT[self.features_list],
                y=y_OOT,
                fraction_sample=0.95,
                task=self.task,
            )
            perm_importance.rename(
                columns={"permutation_importance": "permutation_importance_OOT"},
                inplace=True,
            )
            perm_importance.set_index("feature", inplace=True)
            perm_importance_final = pd.concat(
                [perm_importance_final, perm_importance], axis=1
            )
        # Посчитать PI на test2 при наличии
        if X_test2 is not None:
            perm_importance = calculate_permutation_feature_importance(
                self.model,
                self.metric,
                X=X_test2[self.features_list],
                y=y_test2,
                fraction_sample=0.95,
                task=self.task,
            )
            perm_importance.rename(
                columns={"permutation_importance": "permutation_importance_test2"},
                inplace=True,
            )
            perm_importance.set_index("feature", inplace=True)
            perm_importance_final = pd.concat(
                [perm_importance_final, perm_importance], axis=1
            )
        return perm_importance_final

    @execution_time
    def validate(self, **data) -> pd.DataFrame:
        """
        Запуск процедуры расчета важности признаков.
        Добавляет в итоговоый датасет factors relevancy :
            доля признаков с важностью 20% и более от признака
            с максимальным значением важности
        Рисует и сохраняет график permutation importance plot.
        Записывает результат проврки на страницу excel отчета
        "Permutation importance"
        Parameters:
        ----------
        **data: Dict[str, Tuple(pd.DataFrame, pd.Series)]
            Словарь, где ключ - название датасета, значение -
            кортеж из (X, y), X - матрица признаков,
            y - вектор истинных ответов.
                Returns:
        -------
        pd.DataFrame
            Итоговый датасет с полсчитанной важностью признаков вида:
                - feature_name
                - Permutation importance test/valid
                - Permutatuin importance oot
        """
        _logger.info("Calculating permutation importance...")
        PI = self._calc_perm_importance(**data)
        psi = []
        cols = []
        for col in PI.columns:
            PI_share = 100 * PI[col] / PI[col].max()
            psi.append(100 * ((PI_share > 20).sum()) / PI_share.count())
            cols.append(col)
        psi_df = pd.DataFrame(data=[psi], columns=cols, index=["factors_relevancy"])
        # сохранить график :
        # сортирвока по относительному изменению
        PI = PI.sort_values(by=PI.columns[0], ascending=False)
        PI_plot = PI.reset_index()
        PI_plot.rename(columns={"index": "feature"}, inplace=True)

        # permutation importance
        sheet_name = "Permutation importance"
        save_path = os.path.join(self.images_dir_path, f"{sheet_name}.png")
        plot_permutation_importance(PI_plot, x_column="feature", save_path=save_path)

        # добавить в таблицу строку с релевантностью факторов в %
        PI = PI.append(psi_df)
        PI.reset_index(inplace=True)
        PI.rename(columns={"index": "feature"}, inplace=True)
        # self._to_excel(PI, sheet_name, plot=True)

        return PI