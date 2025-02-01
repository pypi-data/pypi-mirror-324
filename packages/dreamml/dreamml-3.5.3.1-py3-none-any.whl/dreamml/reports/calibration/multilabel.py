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


class MultiLabelCalibrationReport(BaseCalibrationReport):
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
        super().__init__(calibrations, config)
        self.reports_macro = {}

    def create_report(self, calibration_method_name, calibration_model, **eval_sets):

        for sample_name, (X, y) in eval_sets.items():
            classes = y.columns.to_list()
            y_pred = calibration_model.get_y_pred(X)
            y_calib = calibration_model.transform(X)

            y = y.values if isinstance(y, pd.DataFrame) else y
            y_pred = y_pred.values if isinstance(y_pred, pd.DataFrame) else y_pred
            y_calib = y_calib.values if isinstance(y_calib, pd.DataFrame) else y_calib

            class_report = {}
            for class_idx, class_name in enumerate(classes):
                y_true_class = y[:, class_idx]
                y_pred_class = y_pred[:, class_idx]
                y_calib_classes = y_calib[:, class_idx]

                pred_df = pd.DataFrame(
                    {
                        "y_true": y_true_class,
                        "y_pred": y_pred_class,
                        "y_calib": y_calib_classes,
                    }
                )

                report = self.create_calib_stats(pred_df)
                class_report[class_name] = report

                self.plot_calib_curves(
                    pred_df,
                    self.images_dir_path
                    / f"{calibration_method_name}_{sample_name}_{class_name}.png",
                )

            self.reports[f"{calibration_method_name}_{sample_name}"] = class_report

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

        plt.figure(figsize=(49, 40), dpi=80.0)
        summary = pd.DataFrame(index=list(self.calibrators.keys()))

        # comparison table
        sample_names = list(eval_sets.keys())
        for calibration_method_name, calibrator in self.calibrators.items():

            # weighted MAE
            for line_num, sample_name in enumerate(sample_names):
                class_reports = self.reports[f"{calibration_method_name}_{sample_name}"]

                total_average_mae, total_average_mae_calibrated = [], []

                for class_name, report in class_reports.items():
                    total_average_mae.append(report.loc["Total", "MAE"])
                    total_average_mae_calibrated.append(
                        report.loc["Total", "MAE calibrated"]
                    )

                summary.loc[calibration_method_name, f"MAE_{sample_name}"] = np.mean(
                    total_average_mae
                )
                summary.loc[
                    calibration_method_name, f"MAE_calibrated_{sample_name}"
                ] = np.mean(total_average_mae_calibrated)

            # brier score = mse for classification
            for sample_name in sample_names:
                class_reports = self.reports[f"{calibration_method_name}_{sample_name}"]
                total_average_brier, total_average_brier_calibrated = [], []

                for class_name, report in class_reports.items():
                    total_average_brier.append(report.loc["Total", "Brier"])
                    total_average_brier_calibrated.append(
                        report.loc["Total", "Brier calibrated"]
                    )

                summary.loc[calibration_method_name, f"Brier_{sample_name}"] = np.mean(
                    total_average_brier
                )
                summary.loc[
                    calibration_method_name, f"Brier_calibrated_{sample_name}"
                ] = np.mean(total_average_brier_calibrated)

            # logloss
            for sample_name in sample_names:
                class_reports = self.reports[f"{calibration_method_name}_{sample_name}"]
                total_average_logloss, total_average_logloss_calibrated = [], []

                for class_name, report in class_reports.items():
                    total_average_logloss.append(report.loc["Total", "logloss"])
                    total_average_logloss_calibrated.append(
                        report.loc["Total", "logloss calibrated"]
                    )

                summary.loc[calibration_method_name, f"logloss_{sample_name}"] = (
                    np.mean(total_average_logloss)
                )
                summary.loc[
                    calibration_method_name, f"logloss_calibrated_{sample_name}"
                ] = np.mean(total_average_logloss_calibrated)

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
                plt.subplot(2 * plot_lines, 7, subplot_pos)
                y_pred = calibrator.get_y_pred(x)
                y_calib = calibrator.transform(x)

                self.plot_calibration_curve_multilabel(
                    y_true=y,
                    y_pred=y_pred,
                    y_pred_calib=y_calib,
                    title=f"{calibration_method_name}_{sample_name}",
                )
                plt.subplot(2 * plot_lines, 7, subplot_pos + plot_lines * 7)
                self.plot_bin_curve_multilabel(
                    y_true=y,
                    y_pred=y_pred,
                    y_pred_calib=y_calib,
                    title=f"{calibration_method_name}_{sample_name}",
                )
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
        row_idx = 0
        for name, calib in self.calibrators.items():
            if hasattr(calib, "get_equation") and calib.get_equation() is not None:
                result = calib.get_equation()
                calib_name_df = pd.DataFrame({"calib_model": [name]})
                equations = pd.DataFrame(
                    {
                        "class_name": list(result.keys()),
                        "equation": list(result.values()),
                    }
                )
                self._to_excel(
                    df=calib_name_df,
                    sheet_name="equations",
                    formats=None,
                    plot=False,
                    pos=(row_idx, 0),
                )
                self._to_excel(
                    df=equations,
                    sheet_name="equations",
                    formats=None,
                    plot=False,
                    pos=(row_idx + 2, 0),
                )
                row_idx += len(equations) + 5

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

        col_number = 0
        for sample_name, sample_eval_sets in self._multilabel_to_binary_generator(
            **eval_sets
        ):
            data_dict = {}

            for class_name, (x_sample, y_sample_class) in sample_eval_sets.items():
                data_dict[class_name] = [
                    x_sample.shape[0],
                    np.sum(y_sample_class),
                    np.mean(y_sample_class),
                ]
            data_stats = pd.DataFrame(data_dict).T
            data_stats = data_stats.reset_index()
            data_stats.columns = ["класс", "# наблюдений", "# events", "# eventrate"]

            # стандартные форматы чисел
            int_number = "## ##0"
            float_percentage = "0.00%"
            table_format = {
                "num_format": {
                    int_number: ["# наблюдений", "# events"],
                    float_percentage: ["# eventrate"],
                }
            }
            sample_name_df = pd.DataFrame({"Выборка": [sample_name]})
            self._to_excel(
                df=sample_name_df, sheet_name="DataStatistics", pos=(0, col_number)
            )
            self._to_excel(
                df=data_stats,
                sheet_name="DataStatistics",
                formats=table_format,
                pos=(2, col_number),
            )
            col_number += data_stats.shape[0]

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

    @staticmethod
    def plot_calibration_curve_multilabel(
        y_true: pd.DataFrame,
        y_pred: pd.DataFrame,
        y_pred_calib: pd.DataFrame,
        title: str = None,
    ):
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
        classes = y_true.columns.tolist()
        y_true = y_true.values if isinstance(y_true, pd.DataFrame) else y_true
        y_pred = y_pred.values if isinstance(y_pred, pd.DataFrame) else y_pred
        y_pred_calib = (
            y_pred_calib.values
            if isinstance(y_pred_calib, pd.DataFrame)
            else y_pred_calib
        )

        color_mapping = plt.cm.get_cmap("tab20c_r", len(classes))

        for class_idx, class_name in enumerate(classes):
            pred_df = pd.DataFrame(
                {
                    "y_true": y_true[:, class_idx],
                    "y_pred": y_pred[:, class_idx],
                    "y_calib": y_pred_calib[:, class_idx],
                }
            )

            # порезать на бакеты
            pred_df["bin"] = calculate_quantile_bins(pred_df["y_pred"], 21)
            pred_df_grouped = pred_df.groupby(by="bin").mean()

            plt.plot(
                pred_df_grouped["y_pred"],
                pred_df_grouped["y_true"],
                marker="o",
                label=f"{class_name} model",
                linewidth=1,
                color=color_mapping(class_idx),
            )
            plt.plot(
                pred_df_grouped["y_calib"],
                pred_df_grouped["y_true"],
                marker="x",
                label=f"{class_name} model calibrated",
                linewidth=1,
                color=color_mapping(class_idx),
            )
            xlim = ylim = max(
                y_true.max().max(), y_pred.max().max(), y_pred_calib.max().max()
            )
            plt.plot([0, xlim], [0, ylim], "k--", linewidth=1)
            plt.grid()
            plt.xlabel("mean prediction")
            plt.ylabel("mean target")
            plt.legend()
            if title is not None:
                plt.title(title)

    @staticmethod
    def plot_bin_curve_multilabel(
        y_true: pd.DataFrame,
        y_pred: pd.DataFrame,
        y_pred_calib: pd.DataFrame,
        title: str = None,
    ):
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

        # plt.figure(figsize=(12, 8))
        classes = y_true.columns.tolist()
        y_true = y_true.values if isinstance(y_true, pd.DataFrame) else y_true
        y_pred = y_pred.values if isinstance(y_pred, pd.DataFrame) else y_pred
        y_pred_calib = (
            y_pred_calib.values
            if isinstance(y_pred_calib, pd.DataFrame)
            else y_pred_calib
        )

        color_mapping = plt.cm.get_cmap("tab20c_r", len(classes))

        for class_idx, class_name in enumerate(classes):
            pred_df = pd.DataFrame(
                {
                    "y_true": y_true[:, class_idx],
                    "y_pred": y_pred[:, class_idx],
                    "y_calib": y_pred_calib[:, class_idx],
                }
            )

            # порезать на бакеты
            pred_df["bin"] = calculate_quantile_bins(pred_df["y_pred"], 21)
            pred_df_grouped = pred_df.groupby(by="bin").mean()

            plt.plot(
                pred_df_grouped["y_true"],
                marker="o",
                label=f"{class_name} y_true",
                linewidth=1,
                color=color_mapping(class_idx),
            )
            plt.plot(
                pred_df_grouped["y_pred"],
                marker="o",
                label=f"{class_name} y_pred",
                linewidth=1,
                color=color_mapping(class_idx),
            )
            plt.plot(
                pred_df_grouped["y_calib"],
                marker="o",
                label=f"{class_name} y_calibrated",
                linewidth=1,
                color=color_mapping(class_idx),
            )

        plt.grid()
        plt.xlabel("bin")
        plt.ylabel("mean value")
        plt.legend()
        if title is not None:
            plt.title(title)

    @staticmethod
    def _multilabel_to_binary_generator(**eval_sets):
        for sample_name, (x_sample, y_sample) in eval_sets.items():
            sample_eval_sets = {}
            assert isinstance(y_sample, pd.DataFrame)
            classes = y_sample.columns.tolist()

            for class_idx, class_name in enumerate(classes):
                y_sample_class = y_sample.iloc[:, class_idx]
                sample_eval_sets[class_name] = (x_sample, y_sample_class)

            yield sample_name, sample_eval_sets

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

                row_count = 0
                for class_name, report_table in report.items():
                    class_name_df = pd.DataFrame({"class_name": [class_name]})
                    image_name = f"{calib_name}_{ds_name}_{class_name}"

                    self._to_excel(
                        class_name_df,
                        f"{calib_name}_{ds_name}",
                        table_format,
                        False,
                        pos=(row_count, report_table.shape[1] + 2),
                    )
                    self._to_excel(
                        report_table,
                        f"{calib_name}_{ds_name}",
                        table_format,
                        True,
                        pos=(row_count, 0),
                        path_to_image=image_name,
                    )
                    row_count += report_table.shape[0] + 4

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