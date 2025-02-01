import os
from abc import abstractmethod
from pathlib import Path
from typing import Optional, Tuple
from copy import deepcopy
import pickle

import pandas as pd
import matplotlib.pyplot as plt

from dreamml.reports.calibration.format_excel_writer import FormatExcelWriter
from dreamml.modeling.metrics.utils import calculate_quantile_bins
from dreamml.logging import get_logger
from dreamml.utils.get_last_experiment_directory import get_experiment_dir_path

_logger = get_logger(__name__)


class BaseCalibrationReport:
    """
    Класс реализациия создания и сохранения отчета по калибровке модели

    Parameters:
    ----------
    calibrators: dict {<Имя калибровки>: <объект класса Calibration>}
        Словарь со всеми калибровками по которым нужно построить отчет

    config: dict
        словарь с параметрами запуска

    """

    def __init__(self, calibrations: dict, config: dict):

        self.calibrators = deepcopy(calibrations)
        self.reports = {}

        self.target_name = config.get("target_name", None)
        (
            self.target_name.lower()
            if isinstance(self.target_name, str)
            else self.target_name
        )
        self.model_id = config.get("model_id", "model_id").lower()

        if config.get("model_path"):
            model_path = Path(config["model_path"])
            self.model_name = model_path.stem
            self.current_path = model_path.parent / "calibration"
        else:
            self.model_name = config["model_name"]
            self.current_path = Path(
                get_experiment_dir_path(
                    config["results_path"],
                    experiment_dir_name=config.get("dir_name"),
                    use_last_experiment_directory=config.get(
                        "use_last_experiment_directory", False
                    ),
                )
            )

        self.images_dir_path = self.current_path / "images"
        self.docs_dir_path = self.current_path / "docs"
        self.models_dir_path = self.current_path / "models"

        os.makedirs(self.current_path, exist_ok=True)
        os.makedirs(self.images_dir_path, exist_ok=True)
        os.makedirs(self.docs_dir_path, exist_ok=True)
        os.makedirs(self.models_dir_path, exist_ok=True)

        self.writer = pd.ExcelWriter(
            path=self.current_path
            / "docs"
            / f"calibration_report_{self.model_name}.xlsx"
        )

    def _to_excel(
        self,
        df: pd.DataFrame,
        sheet_name: str,
        formats: dict = None,
        plot: bool = False,
        pos: Tuple = (0, 0),
        path_to_image: str = None,
    ):
        """
        Метод для записи произвольного датафрейма на лист excel книги

        Parameters
        ---------
        df: pd.DataFrame
            Датафрейм, который будет записат в excel книгу

        sheet_name: str
            имя страницы для записи

        formats: dict
            словарь с перечнем форматов для столбцов датафрейма

        plot: bool
            флаг - вставлять на страницу рисунок с именем {sheet_name}.png
            из  каталога self.save_path

        pos: Tuple
            координаты вехрнего левого угла таблицы

        path_to_image: str
            путь до рисунка для вставки, если None, то вставляется рисунок
            с именем {sheet_name}.png из  каталога self.save_path
        """
        # write table
        format_writer = FormatExcelWriter(self.writer)
        format_writer.write_data_frame(
            df=df, pos=pos, sheet=sheet_name, formats=formats
        )

        # insert plot
        if plot:
            sheet = self.writer.sheets[sheet_name]

            if path_to_image is not None:
                save_path = self.current_path / "images" / f"{path_to_image}.png"
                sheet.insert_image(f"P{pos[0]+1}", save_path)
            else:
                save_path = self.current_path / "images" / f"{sheet_name}.png"
                sheet.insert_image(f"A{df.shape[0] + 4}", save_path)

    def plot_calib_curves(
        self, df: pd.DataFrame, save_path: Optional[os.PathLike] = None
    ):
        """
        Метод для отрисовки и сохранения в файл двух графиков:
        calibration_curve и bin_curve

        Parameters
        ----------
        df: pd.DataFrame
            Датафрейм на основе которого будут построены графики
            Обязательные столбцы:
                - y_pred  - вектор прогнозов модели
                - y_calib - вектор прогноза калибровки
                - y_true  - вектор истинных значений

        save_path: os.PathLike
            имя для сохранения изображения в файл
        """
        plt.figure(figsize=(24, 6), dpi=80.0)
        plt.subplot(1, 2, 1)
        self.plot_bin_curve(df)
        plt.subplot(1, 2, 2)
        self.plot_calibration_curve(df)
        if save_path is not None:
            plt.savefig(save_path, bbox_inches="tight")

    def print_reports(self, **eval_sets):
        """
        Вывод на страницы excel книги отчетов по каждой калибровк на всех
        имеющихся выборках
        """
        int_number = "## ##0"
        float_number_high = "## ##0.00"
        float_number_low = "## ##0.00000"

        # Кастомный формат для таблицы
        table_format = {
            "num_format": {
                int_number: ["bin", "#obs"],
                float_number_high: ["mean proba", "calibration proba", "event rate"],
                float_number_low: [
                    "MAE",
                    "MAE calibrated",
                    "Brier",
                    "Brier calibrated",
                    "logloss",
                    "logloss calibrated",
                ],
            }
        }

        for calib_name in self.calibrators.keys():
            for ds_name in eval_sets.keys():
                report = self.reports[f"{calib_name}_{ds_name}"]
                self._to_excel(report, f"{calib_name}_{ds_name}", table_format, True)

    def create_comparison(self, **eval_sets):
        pass

    def print_equations(self):
        for name, calibration in self.calibrators.items():
            if name in ["linear", "logit"]:
                _logger.info(f"{name}: {calibration.get_equation()}")

    def create_equations(self):
        equations = pd.DataFrame(columns=["equation"])
        for name, calib in self.calibrators.items():
            if hasattr(calib, "get_equation"):
                equations.loc[name] = calib.get_equation()

        equations = equations.reset_index()
        self._to_excel(equations, "equations", None, False)

    def create_data_stats(self, **eval_sets):
        """
        Построение отчета о данных, которые использованы
        для обучения / валидации модели.

        Parameters:
        -----------
        **kwargs: Dict[str, Tuple(pd.DataFrame, pd.Series)]
            Словарь, где ключ - название датасета, значение -
            кортеж из (X, y), X - матрица признаков,
            y - вектор истинных ответов.
        """
        pass

    @staticmethod
    def create_calib_stats(df: pd.DataFrame):
        """
        Функция формирования датафрейма со статистикой по калибровке на
        конкретной выборке в разрезе бинов прогноза

        Parameters:
        ----------
        df: pd.DataFrame
            Датафрейм с 3-мя колонками:
                - y_pred  - вектор прогнозов модели
                - y_calib - вектор прогноза калибровки
                - y_true  - вектор истинных значений


        Return:
        -------
        pd.DataFrame
            Статистики по калибровке в разрезе бинов прогноза исходной модели
            Столбцы:
                - bin:                номер бина
                - mean proba:         средний прогноз модели в бине
                - calibration proba:  средний прогноз калибровки в бине
                - event rate:         доля целевых событий в бине
                - # obs:              количество наблюдений в бине
                - MAE:                взв. mean absolute error по прогнозу в бине
                - MAE calibrated:     взв. mean absolute error по калибровке в бине
                - Brier:              MSE прогноза на всех наблюдениях
                - Brier calibrated:   MSE калибровки на всех наблюдениях
                - logloss:            logloss прогнозана всех наблюдениях
                - logloss calibrated: logloss калибровки на всех наблюдениях
        """
        pass

    @staticmethod
    def plot_calibration_curve(pred_df: pd.DataFrame, title: str = None):
        """
        Функция построения графика для диагностирования необходимости калибровки:
        строит зависимость y_pred - y_true, разбив исходные векторы на бины
        Отрисовывает 2 графика,
         y_calibrated - y_true
         y_pred       - y_true

        Parameters:
        ----------
        df: pd.DataFrame
            Датафрейм с 3-мя колонками:
                - y_pred  - вектор прогнозов модели
                - y_calib - вектор прогноза калибровки
                - y_true  - вектор истинных значений

        """
        # порезать на бакеты
        pred_df["bin"] = calculate_quantile_bins(pred_df["y_pred"], 21)

        pred_df_grouped = pred_df.groupby(by="bin").mean()

        # plt.figure(figsize=(12,8))
        plt.plot(
            pred_df_grouped["y_pred"],
            pred_df_grouped["y_true"],
            marker="o",
            label="model",
            linewidth=3,
        )
        plt.plot(
            pred_df_grouped["y_calib"],
            pred_df_grouped["y_true"],
            marker="o",
            label="model calibrated",
            linewidth=4,
        )
        xlim = ylim = pred_df_grouped["y_true"].max()
        plt.plot([0, xlim], [0, ylim], "k--")
        plt.grid()
        plt.xlabel("mean prediction")
        plt.ylabel("mean target")
        plt.legend()
        if title is not None:
            plt.title(title)

    @staticmethod
    def plot_bin_curve(pred_df: pd.DataFrame, title: str = None):
        """
        Функция построения графика среднего прогноза в бинах
        Отрисовывает 3 графика,
            bin - event_rate
            bin - mean proba
            bin - mean calibration

        Parameters:
        ----------
        df: pd.DataFrame
            Датафрейм с 3-мя колонками:
                - y_pred  - вектор прогнозов модели
                - y_calib - вектор прогноза калибровки
                - y_true  - вектор истинных значений

        """
        # порезать на бакеты
        pred_df["bin"] = calculate_quantile_bins(pred_df["y_pred"], 21)

        pred_df_grouped = pred_df.groupby(by="bin").mean()

        # plt.figure(figsize=(12,8))
        plt.plot(
            pred_df_grouped["y_true"], "green", marker="o", label="y_true", linewidth=3
        )
        plt.plot(pred_df_grouped["y_pred"], marker="o", label="y_pred", linewidth=3)
        plt.plot(
            pred_df_grouped["y_calib"], marker="o", label="y_calibrated", linewidth=4
        )
        plt.grid()
        plt.xlabel("bin")
        plt.ylabel("mean prediction")
        plt.legend()
        if title is not None:
            plt.title(title)

    @abstractmethod
    def transform(self, **eval_sets):
        pass

    @abstractmethod
    def create_report(self, calibration_method_name, calibration_model, **eval_sets):
        """
        Создание отчетов по калибровкам на каждой выборке, сохранение объектов
        с калибровками

        Parameters
        ----------
        calibration_method_name: str
            Наименование метода калибровки

        calibration_model: Calibration
            Калибрующая модель

        eval_sets: dict{}
            словарь с keyword аргументами - выборкам, на которых необходимо
            создавать расчеты

        """
        pass

    def _save_calibrated_model(self, calibration_method_name, calibration_model):
        with open(
            self.models_dir_path
            / f"calibrated_{self.model_name}_{calibration_method_name}.pkl",
            "wb",
        ) as f:
            pickle.dump(calibration_model, f)