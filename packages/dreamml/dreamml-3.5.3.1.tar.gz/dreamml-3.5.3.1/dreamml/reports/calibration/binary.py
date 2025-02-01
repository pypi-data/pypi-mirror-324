import pickle
from abc import abstractmethod

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import log_loss, mean_absolute_error, mean_squared_error

from dreamml.modeling.metrics.utils import calculate_quantile_bins
from dreamml.logging import get_logger
from dreamml.reports.calibration.base import BaseCalibrationReport

_logger = get_logger(__name__)


class BinaryCalibrationReport(BaseCalibrationReport):
    """
    Класс реализациия создания и сохранения отчета по калибровке модели

    Parameters:
    ----------
    calibrators: dict {<Имя калибровки>: <объект класса Calibration>}
        Словарь со всеми калибровками по которым нужно построить отчет

    config: dict
        словарь с параметрами запуска

    """

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
        for sample_name, (X, y) in eval_sets.items():
            pred_df = pd.DataFrame(
                {
                    "y_true": y,
                    "y_pred": calibration_model.get_y_pred(X),
                    "y_calib": calibration_model.transform(X),
                }
            )

            report = self.create_calib_stats(pred_df)
            self.reports[f"{calibration_method_name}_{sample_name}"] = report

            self.plot_calib_curves(
                pred_df,
                self.images_dir_path / f"{calibration_method_name}_{sample_name}.png",
            )

    def create_comparison(self, **eval_sets):

        # формат для печати в excel
        float_percentage = "0.00%"
        float_number_low = "## ##0.00000"

        table_format = {
            "num_format": {
                float_number_low: [
                    "MAE_train",
                    "MAE_calibrated_train",
                    "MAE_valid",
                    "MAE_calibrated_valid",
                    "MAE_OOT",
                    "MAE_calibrated_OOT",
                    "Brier_train",
                    "Brier_calibrated_train",
                    "Brier_valid",
                    "Brier_calibrated_valid",
                    "Brier_OOT",
                    "Brier_calibrated_OOT",
                    "logloss_train",
                    "logloss_calibrated_train",
                    "logloss_valid",
                    "logloss_calibrated_valid",
                    "logloss_OOT",
                    "logloss_calibrated_OOT",
                ],
                float_percentage: [
                    "delta MAE_train",
                    "delta Brier_train",
                    "delta logloss_train",
                    "delta MAE_valid",
                    "delta Brier_valid",
                    "delta logloss_valid",
                    "delta MAE_OOT",
                    "delta Brier_OOT",
                    "delta logloss_OOT",
                ],
            }
        }

        plt.figure(figsize=(35, 30))
        summary = pd.DataFrame(index=list(self.calibrators.keys()))

        # comparison table
        sample_names = list(eval_sets.keys())
        for calibration_method_name, calibrator in self.calibrators.items():

            # weighted MAE
            for line_num, sample_name in enumerate(sample_names):
                report = self.reports[f"{calibration_method_name}_{sample_name}"]
                summary.loc[calibration_method_name, f"MAE_{sample_name}"] = report.loc[
                    "Total", "MAE"
                ]
                summary.loc[
                    calibration_method_name, f"MAE_calibrated_{sample_name}"
                ] = report.loc["Total", "MAE calibrated"]

            # brier score = mse for classification
            for sample_name in sample_names:
                report = self.reports[f"{calibration_method_name}_{sample_name}"]
                summary.loc[calibration_method_name, f"Brier_{sample_name}"] = (
                    report.loc["Total", "Brier"]
                )
                summary.loc[
                    calibration_method_name, f"Brier_calibrated_{sample_name}"
                ] = report.loc["Total", "Brier calibrated"]
            # logloss

            for sample_name in sample_names:
                report = self.reports[f"{calibration_method_name}_{sample_name}"]
                summary.loc[calibration_method_name, f"logloss_{sample_name}"] = (
                    report.loc["Total", "logloss"]
                )
                summary.loc[
                    calibration_method_name, f"logloss_calibrated_{sample_name}"
                ] = report.loc["Total", "logloss calibrated"]

            for sample_name in sample_names:
                # deltas
                # delta ECE
                summary[f"delta MAE_{sample_name}"] = (
                    summary[f"MAE_calibrated_{sample_name}"]
                    - summary[f"MAE_{sample_name}"]
                )

                # delta Brier
                summary[f"delta Brier_{sample_name}"] = (
                    summary[f"Brier_calibrated_{sample_name}"]
                    - summary[f"Brier_{sample_name}"]
                )

                # delta logloss
                summary[f"delta logloss_{sample_name}"] = (
                    summary[f"logloss_calibrated_{sample_name}"]
                    - summary[f"logloss_{sample_name}"]
                )

        # comparison plots
        plot_lines = len(eval_sets)
        subplot_pos = 1
        for sample_name, (x, y) in eval_sets.items():
            for calibration_method_name, calibrator in self.calibrators.items():
                # add subplot
                plt.subplot(2 * plot_lines, 7, subplot_pos)
                pred_df = pd.DataFrame(
                    {
                        "y_true": y,
                        "y_pred": calibrator.get_y_pred(x),
                        "y_calib": calibrator.transform(x),
                    }
                )
                self.plot_calibration_curve(
                    pred_df, f"{calibration_method_name}_{sample_name}"
                )
                plt.subplot(2 * plot_lines, 7, subplot_pos + plot_lines * 7)
                self.plot_bin_curve(pred_df, f"{calibration_method_name}_{sample_name}")

                subplot_pos += 1

        # save figure
        plt.savefig(
            self.images_dir_path / "calibration_comparison.png",
            bbox_inches="tight",
        )
        # reset index
        summary.insert(loc=0, column="calibration", value=summary.index)
        desc = [
            "Линейная регрессия на бинах прогноза",
            "Линейная регрессия на шансах в бинах прогноза",
            "Линейная регрессия на логарифме шансов в бинах прогноза",
            "Логистическая регрессия на всех наблюдениях",
            "Логистическая регрессия на шансах прогнозов наблюдений",
            "Логистическая регрессия на логарифме шансов прогнозов " "наблюдений",
            "Изотоническая регрессия",
        ]
        summary.insert(loc=1, column="description", value=desc)

        self._to_excel(
            summary,
            sheet_name="calibration_comparison",
            formats=table_format,
            plot=True,
        )

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
        data_dict = {}
        for data_name, (x, y) in eval_sets.items():
            data_dict[data_name] = [x.shape[0], np.sum(y), np.mean(y)]
        data_stats = pd.DataFrame(data_dict).T
        data_stats = data_stats.reset_index()
        data_stats.columns = ["выборка", "# наблюдений", "# events", "# eventrate"]

        # стандартные форматы чисел
        int_number = "## ##0"
        float_percentage = "0.00%"
        table_format = {
            "num_format": {
                int_number: ["# наблюдений", "# events"],
                float_percentage: ["# eventrate"],
            }
        }
        self._to_excel(data_stats, "Data sets", table_format)

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
        # stats
        df["bin"] = calculate_quantile_bins(df["y_pred"], n_bins=21)

        df_group = df.groupby(by="bin")
        stats = df_group.agg(
            {"y_pred": ["mean"], "y_calib": ["mean"], "y_true": ["mean", "count"]}
        )

        stats.columns = ["mean proba", "calibration proba", "event rate", "# obs"]

        # metrics:

        # expected calibration error = weighted mean absolute error
        mae = mean_absolute_error(
            stats["event rate"], stats["mean proba"], sample_weight=stats["# obs"]
        )
        mae_calib = mean_absolute_error(
            stats["event rate"],
            stats["calibration proba"],
            sample_weight=stats["# obs"],
        )
        stats.loc["Total", "MAE"] = mae
        stats.loc["Total", "MAE calibrated"] = mae_calib

        # mean square error = brier score
        stats.loc["Total", "Brier"] = mean_squared_error(df["y_true"], df["y_pred"])
        stats.loc["Total", "Brier calibrated"] = mean_squared_error(
            df["y_true"], df["y_calib"]
        )

        # logloss
        stats.loc["Total", "logloss"] = log_loss(df["y_true"], df["y_pred"], eps=1e-5)
        stats.loc["Total", "logloss calibrated"] = log_loss(
            df["y_true"], df["y_calib"], eps=1e-5
        )

        # total row
        stats.loc["Total", "mean proba"] = df["y_pred"].mean()
        stats.loc["Total", "calibration proba"] = df["y_calib"].mean()
        stats.loc["Total", "event rate"] = df["y_true"].mean()
        stats.loc["Total", "# obs"] = stats["# obs"].sum()

        stats.insert(loc=0, column="bin", value=stats.index)

        return stats.fillna(".")

    @abstractmethod
    def transform(self, **eval_sets):
        self.create_data_stats(**eval_sets)

        for method_name, calibration_model in self.calibrators.items():
            self.create_report(method_name, calibration_model, **eval_sets)
            self._save_calibrated_model(method_name, calibration_model)

        self.create_comparison(**eval_sets)
        self.create_equations()
        self.print_reports(**eval_sets)
        self.writer.save()