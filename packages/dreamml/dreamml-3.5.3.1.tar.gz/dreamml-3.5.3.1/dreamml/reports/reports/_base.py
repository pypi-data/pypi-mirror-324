import json
import os
import socket
import sys
from copy import deepcopy
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
from xlsxwriter.utility import xl_col_to_name

import dreamml as dml
from dreamml.logging import get_logger
from dreamml.utils.saver import ArtifactSaver
from dreamml.utils.vectorization_eval_set import get_eval_set_with_embeddings

_logger = get_logger(__name__)


class BaseReport:
    """
    Набор правил и стилей для форматирования отчета.

    Parameters
    ----------
    saver: dspl.utils.INFOSaver
        экземпляр сохранения выходных файлов

    """

    def __init__(
        self,
        experiment_path,
        artifact_saver: ArtifactSaver,
        config: dict,
        models,
        other_models,
        oot_potential,
        vectorizers_dict: Optional = None,
    ):
        self.DREAMML_CONFIGURATION_SHEET_NAME = "Конфигурация DreamML"
        self.MODEL_NAME_COL = "Название модели"

        self.models = deepcopy(models)
        self.encoder = self.models.pop("encoder")
        self.other_models = deepcopy(other_models)
        self.oot_potential = deepcopy(oot_potential)
        self.config = config
        self.experiment_path = experiment_path
        self.task = config.get("task", "???")
        self.artifact_saver = artifact_saver
        self.vectorizers_dict = (
            deepcopy(vectorizers_dict) if vectorizers_dict != {} else None
        )

        # if_sheet_exists="overlay", позволяет перезаписать текущую ячейку - ValueError: Append mode is not
        #  supported with xlsxwriter!
        self.writer = pd.ExcelWriter(
            path=f"{self.experiment_path}/docs/{self.artifact_saver.dev_report_name}.xlsx",
            options={"nan_inf_to_errors": True},
        )
        self.sheets = self.writer.sheets
        self.wb = self.writer.book
        self.predictions = None
        self.target_with_nan_values = config.get("target_with_nan_values", False)
        self.show_save_paths: bool = config.get("show_save_paths", False)
        self.samples_to_plot: list = config.get(
            "samples_to_plot", ["train", "valid", "test", "OOT"]
        )
        self.max_classes_plot: int = config.get("max_classes_plot", 5)
        self.plot_multi_graphs: bool = config.get("plot_multi_graphs", True)

    def add_table_borders(
        self, data, sheet_name: str, startrow: int = 0, num_format: int = 10
    ):
        """
        Установка границ таблицы на листе Excel.

        Parameters
        ----------
        data: pandas.DataFrame
            Набор данных для записи в Excel.

        sheet_name: string
            Название листа в Excel-книге для записи данных.

        startrow: integer, optional, default = 0
            Номер строки, с которой начинать запись данных.

        num_format: integer, optional, default = 10
            Числовой формат записи данных.

        """
        ws = self.sheets[sheet_name]
        last_col = data.columns[-1]

        # запись последнего столбца в data
        if num_format:
            sheet_format = self.wb.add_format({"right": 1, "num_format": num_format})
        else:
            sheet_format = self.wb.add_format({"right": 1})

        for cell_number, data_value in enumerate(data[last_col]):
            row_idx, col_idx = startrow + cell_number + 1, data.shape[1] - 1

            # FIXME адаптировать для задач multiclass & multilabel
            if isinstance(data_value, pd.Series):
                content = data_value.to_string(index=False).replace("\n", ", ")
                ws.write(row_idx, col_idx, content, sheet_format)
            else:
                ws.write(row_idx, col_idx, data_value, sheet_format)

        # запись последней строки в data
        sheet_format = self.wb.add_format({"bottom": 1})
        for cell_number, data_value in enumerate(data.values[-1]):
            row_idx, col_idx = startrow + data.shape[0], cell_number

            # FIXME адаптировать для задач multiclass & multilabel
            if isinstance(data_value, pd.Series):
                data_value = data_value.to_string(index=False).replace("\n", ", ")
            if isinstance(data_value, list):
                data_value = ", ".join(data_value)
            ws.write(row_idx, col_idx, data_value, sheet_format)

        # запись элемента последней строки и последнего столбца в data
        if num_format:
            sheet_format = self.wb.add_format(
                {"right": 1, "bottom": 1, "num_format": num_format}
            )
        else:
            sheet_format = self.wb.add_format({"right": 1, "bottom": 1})

        row_idx, col_idx = startrow + data.shape[0], data.shape[1] - 1

        # FIXME адаптировать для задач multiclass & multilabel
        if isinstance(data.values[-1, -1], pd.Series):
            content = data.values[-1, -1].to_string(index=False).replace("\n", ", ")
            ws.write(row_idx, col_idx, content, sheet_format)
        else:
            ws.write(row_idx, col_idx, data.values[-1, -1], sheet_format)

    def add_cell_width(self, data, sheet_name: str):
        """
        Установка ширины ячейки на листе Excel.

        Parameters
        ----------
        data: pandas.DataFrame
            Набор данных для записи в Excel.

        sheet_name: string
            Название листа в Excel-книге для записи данных.

        """
        ws = self.sheets[sheet_name]
        for cell_number, table_column in enumerate(data.columns):
            max_value_len = data[table_column].astype("str").str.len().max()
            cell_len = max(max_value_len, len(table_column)) + 2
            ws.set_column(cell_number, cell_number, cell_len)

    def add_header_color(
        self, data, sheet_name: str, startrow: int = 0, color: str = "77d496"
    ):
        """
        Установка цвета заголовка на листе Excel.

        Parameters
        ----------
        data: pandas.DataFrame
            Набор данных для записи в Excel.

        sheet_name: string
            Название листа в Excel-книге для записи данных.

        startrow: integer, optional, default = 0
            Номер строки, с которой начинать запись данных.

        color: string, optional, default = "77d496"
            RGB-цвет заголовка.

        """
        ws = self.sheets[sheet_name]
        sheet_format = self.wb.add_format(
            {
                "bold": True,
                "text_wrap": True,
                "fg_color": color,
                "border": 1,
                "align": "center",
            }
        )

        for cell_number, data_value in enumerate(data.columns.values):
            ws.write(startrow, cell_number, data_value, sheet_format)

    def add_numeric_format(
        self,
        data,
        sheet_name: str,
        startrow: int = 0,
        startcol: int = 0,
        min_value: int = 10,
        color: str = "#000000",
    ):
        """
        Установка формата для числовой таблицы.

        Parameters
        ----------
        data: pandas.DataFrame
            Набор данных для записи в Excel.

        sheet_name: string
            Название листа в Excel-книге для записи данных.

        startrow: integer, optional, default = 0
            Номер строки, с которой начинать запись данных.

        startcol: integer, optional, default = 0
            Номер столбца, с которого начинать запись данных.

        set_top: integer, optional, default = 0

        min_value: interger, optional, default = 10
            Минимальное значение, формат записи которого "х",
            если значение в ячейке Excel-книге меньше min_value,
            то формат записи - "x.yy".

        color: string, optional, default = "#000000"
            RGB-цвет шрифта.

        """
        ws = self.sheets[sheet_name]

        for col_number, column in enumerate(data.columns[1:]):
            if col_number == data.shape[1] - 2:
                fmt = {"right": 1}
            else:
                fmt = {}

            for row_number, value in enumerate(data[column]):
                try:
                    if row_number == data.shape[0] - 1:
                        fmt.update({"bottom": 1, "font_color": color})

                    if np.abs(value) > min_value or np.abs(value) in range(min_value):
                        fmt.update({"num_format": 1, "font_color": color})
                        sheet_format = self.wb.add_format(fmt)
                    elif np.abs(value) <= min_value:
                        fmt.update({"num_format": 2, "font_color": color})
                        sheet_format = self.wb.add_format(fmt)

                except np.core._exceptions.UFuncTypeError:
                    fmt = {"right": 1}
                    sheet_format = self.wb.add_format(fmt)

                ws.write(
                    startrow + row_number + 1,
                    startcol + col_number + 1,
                    value,
                    sheet_format,
                )

    def add_text_color(
        self, sheet_name: str, startcol: int, endcol: int, color: str = "C8C8C8"
    ):
        """
        Добавление отдельного цвета текста на на листе Excel.

        Parameters
        ----------
        sheet_name: string
            Название листа в Excel-книге для записи данных.

        startcol: integer
            Номер столбца, с которого начинать запись данных.

        endcol: integer
            Номер столбца, на котором закончить запись данных.

        color: string, optional, default = "C8C8C8"
            RGB-цвет шрифта.

        """
        ws = self.sheets[sheet_name]
        cols = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        startcol, endcol = cols[startcol], cols[endcol]

        sheet_format = self.wb.add_format({"font_color": color})
        ws.set_column(f"{startcol}:{endcol}", None, sheet_format)

    def add_eventrate_format(
        self, data, sheet_name: str, startcol: int = 7, startrow: int = 0, fmt: int = 10
    ):
        """
        Добавление формата для eventrate на листах Excel.

        Parameters
        ----------
        data: pandas.Series
            Столбец со значениями eventrate.

        sheet_name: string
            Название листа в Excel-книге для записи данных.

        startcol: integer, optional, default = 7
            Номер столбца, в котором требуется установить формат.
            Опциональный параметр, по умолчанию используется стобец 4.

        fmt: integer, optional, default = 10
            Код формата xlsxwriter.

        """
        ws = self.sheets[sheet_name]
        sheet_format = self.wb.add_format({"num_format": fmt})

        for cell_number, data_value in enumerate(data):
            ws.write(1 + cell_number + startrow, startcol, data_value, sheet_format)

        sheet_format = self.wb.add_format({"num_format": fmt, "bottom": True})
        ws.write(len(data) + startrow, startcol, data_value, sheet_format)

    def add_bottom_table_borders(
        self, data, sheet_name: str, startrow: int = 0, fmt_col_4: int = 10
    ):
        """
        Установка верхней и нижней границ таблицы на листе Excel.

        Parameters
        ----------
        data: pandas.Series
            Столбец со значениями таблицы.

        sheet_name: string
            Название листа в Excel-книге для записи данных.

        startrow: integer, optional, default = 0
            Номер строки, с которой начинать запись данных.

        """
        ws = self.sheets[sheet_name]

        for cell_number, data_value in enumerate(data):
            if isinstance(data_value, str):
                fmt = {"bottom": 1, "left": 1, "right": 1, "top": 1, "bold": True}
            elif data_value > 100:
                fmt = {
                    "bottom": 1,
                    "left": 1,
                    "right": 1,
                    "top": 1,
                    "num_format": 1,
                    "bold": True,
                }
            elif data_value < 100 and cell_number != 4:
                fmt = {
                    "bottom": 1,
                    "left": 1,
                    "right": 1,
                    "top": 1,
                    "num_format": 2,
                    "bold": True,
                }
            elif cell_number == 4:
                fmt = {
                    "bottom": 1,
                    "left": 1,
                    "right": 1,
                    "top": 1,
                    "num_format": fmt_col_4,
                    "bold": True,
                }
            else:
                fmt = {"bottom": 1, "left": 1, "right": 1, "top": 1, "bold": True}
            sheet_format = self.wb.add_format(fmt)
            ws.write(startrow, cell_number, data_value, sheet_format)

    def create_compare_models_url(self, data, sheet_name: str, fmt_col_4: int = 10):
        """
        Создание ссылки на лист Compare Models и добавление
        на лист с отчетом для пары модель / выборка.

        Parameters
        ----------
        data: pandas.DataFrame
            Набор данных для записи в Excel.

        sheet_name: string
            Название листа в Excel-книге для записи данных.

        """
        destination_sheet = None
        for destination_sheet in self.sheets:
            if "compare models" in destination_sheet.lower():
                break
        if destination_sheet is None:
            _logger.warning("Лист Compare Models не найден.")
            return

        ws = self.sheets[sheet_name]

        # last column in destination sheet
        cell_name = xl_col_to_name(len(self.sheets[destination_sheet].table[0]) - 1)
        string = "Ссылка на лист сравнения моделей"
        url = f"internal:'{destination_sheet}'!{cell_name}1"

        df = data.loc[max(data.index)]
        ws.write_url(f"A{len(data) + 2}", url, string=string)
        self.add_bottom_table_borders(
            df, sheet_name, data.shape[0], fmt_col_4=fmt_col_4
        )
        self.add_cell_width(data, sheet_name)

    def create_model_url(self, **eval_sets):
        """
        Создание ссылки на лист с отчетом модель / выборка и
        добавление на лист Compare Models.

        Parameters
        ----------
        eval_sets: Dict[string, Tuple[pandas.DataFrame, pandas.Series]]
            Словарь с выборками, для которых требуется рассчитать статистику.
            Ключ словаря - название выборки (train / valid / ...), значение -
            кортеж с матрицей признаков (data) и вектором ответов (target).

        """
        metrics = set([self.config.get("metric_col_name")] + ["PR-AUC"])
        for metric in metrics:
            ws = self.sheets[f"Compare Models {metric}"]
            cols = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            sheet_format = self.wb.add_format({"left": True, "right": True})
            train_sheets = [sheet for sheet in self.sheets if "train" in sheet]

            for sheet_number, sheet_name in enumerate(train_sheets):
                url = f"internal:'{sheet_name}'!A1"
                string = f"Ссылка на лист {sheet_name}"
                cell_number = len(eval_sets) + 2

                if "test" in eval_sets:
                    cell_number += 2
                if "OOT" in eval_sets:
                    cell_number += 2

                cell_name = cols[cell_number]
                ws.write_url(
                    f"{cell_name}{sheet_number + 2}", url, sheet_format, string
                )

            sheet_format = self.wb.add_format(
                {"left": True, "right": True, "bottom": True}
            )
            ws.write_url(f"{cell_name}{sheet_number + 2}", url, sheet_format, string)

    def set_style(
        self,
        data,
        sheet_name: str,
        startrow: int = 0,
        color: str = "77d496",
        num_format: Optional[int] = None,
    ):
        """
        Установка базового стиля для всех листов Excel-книги.
        Базовый стиль включает в себя:
            - установку границ таблицы;
            - установку оптимального размера ячейки;
            - установку цвета заголовка таблицы;
            - форматирование шрифтов.

        Parameters
        ----------
        data: pandas.DataFrame
            Набор данных для записи в Excel.

        sheet_name: string
            Название листа в Excel-книге для записи данных.

        startrow: integer, optional, default = 0
            Номер строки, с которой начинать запись данных.

        color: string, optional, default = "77d496"
            RGB-цвет заголовка.

        num_format: integer, optional, default = None
            Числовой формат записи данных.

        """
        self.add_table_borders(data, sheet_name, startrow, num_format)
        self.add_header_color(data, sheet_name, startrow, color)
        self.add_cell_width(data, sheet_name)

    def create_dml_info_page(self):
        # FIXME: duplicating code fragment with report_classification.py
        kernel_folder_path = Path(sys.executable).parent.parent
        kernel_name = os.path.basename(kernel_folder_path)
        kernel_version = ""
        try:
            kernel_path = os.path.join(kernel_folder_path, "jh_kernel", "kernel.json")
            with open(kernel_path, "r") as file:
                kernel = json.load(file)
            kernel_version = kernel["display_name"]
        except FileNotFoundError:
            kernel_version = kernel_name

        host_name = socket.gethostname()
        df = pd.DataFrame(
            {
                "Module": ["DreamML", "Kernel", "Host_name"],
                "Version": [dml.__version__, kernel_version, host_name],
            }
        )
        df.to_excel(self.writer, sheet_name="V", index=False)
        self.set_style(df, "V", 0)

        ws = self.sheets["V"]
        msg = "Made in DreamML"
        ws.write(df.shape[0] + 4, 0, msg, self.wb.add_format({"italic": True}))

    def create_zero_page(self):
        """
        Нулевая страница отчета - содержит конфигурацию запуска DreamML
        """
        config_for_report = dict(
            [(k, str(v)) for k, v in self.config.items() if not isinstance(v, dict)]
        )
        prep_lists = dict(
            [
                (k, ", ".join(str(x) for x in v))
                for k, v in self.config.items()
                if isinstance(v, list)
            ]
        )
        config_for_report.update(prep_lists)

        config_df = pd.Series(config_for_report).to_frame().reset_index()
        config_df.columns = ["parameter", "value"]

        config_df.to_excel(
            self.writer,
            sheet_name=self.DREAMML_CONFIGURATION_SHEET_NAME,
            index=False,
            startrow=0,
        )
        self.add_table_borders(
            config_df, sheet_name=self.DREAMML_CONFIGURATION_SHEET_NAME, num_format=None
        )
        self.add_header_color(
            config_df, sheet_name=self.DREAMML_CONFIGURATION_SHEET_NAME, color="77d496"
        )
        self.add_cell_width(
            config_df,
            sheet_name=self.DREAMML_CONFIGURATION_SHEET_NAME,
        )


def create_used_features_stats(
    models: dict, vectorizers_dict: Optional[dict] = None, **eval_sets
):
    """
    Создание датафрейма со списком используемых признаков для каждой
    модели. Если признак используется в модели - маркируется 1,
    иначе - маркируется 0.

    Parameters
    ----------
    eval_sets: Dict[string, Tuple[pandas.DataFrame, pandas.Series]]
        Словарь с выборками, для которых требуется рассчитать статистику.
        Ключ словаря - название выборки (train / valid / ...), значение -
        кортеж с матрицей признаков (data) и вектором ответов (target).

    models: dict
        Словарь с экземплярами моделей.

    vectorizers_dict: Optional[dict] default: None
        Словарь с экземплярами векторизаторов.

    Returns
    -------
    df: pandas.DataFrame, shape = [n_features, len(models)]
        Датафрейм с флагами использования признаков.

    """
    if vectorizers_dict is not None:
        dfs_dict = {}

        for vec_name, vectorizer in vectorizers_dict.items():
            eval_set_cp = deepcopy(eval_sets)
            eval_set_cp = get_eval_set_with_embeddings(vectorizer, eval_set_cp)

            df = pd.DataFrame({"Variable": eval_set_cp["train"][0].columns.tolist()})

            for model_name, model in models.items():
                used_features = model.used_features
                vectorizer_name = f"{model.vectorization_name}_vectorizer"

                if vectorizer_name == vec_name:
                    df[f"{model_name} include variable"] = (
                        df["Variable"].isin(used_features).astype(int)
                    )
                    dfs_dict[vec_name] = df

        return dfs_dict

    else:
        df = pd.DataFrame({"Variable": eval_sets["train"][0].columns.tolist()})

        for model in models:
            used_features = models[model].used_features
            df[f"{model} include variable"] = (
                df["Variable"].isin(used_features).astype(int)
            )

        return df

    def _create_business_task_description_page(self, **data):
        """
        Страница с описанием бизнес-задачи

        """
        _logger.info("0. Сбор статистики о решаемой бизнес-задаче.")
        bcd = BusinessCaseDescription(
            self.artifacts_config, self.validation_test_config
        )
        stats = bcd._create_description(**data)
        stats.to_excel(self.writer, sheet_name="Описание бизнес-задачи", index=False)
        self.sheet_descriptions["Описание бизнес-задачи"] = ""

        ws = self.writer.sheets["Описание бизнес-задачи"]

        b_task_cell_format = NamedStyle(name="b_task_cell_format")
        b_task_cell_format.font = Font(color="808080")
        b_task_cell_format.alignment = Alignment(
            wrap_text=True, horizontal="center", vertical="center"
        )
        brd = Side(border_style="thin", color="000000")
        b_task_cell_format.border = Border(left=brd, right=brd, top=brd, bottom=brd)

        self.wb.add_named_style(b_task_cell_format)

        b_task_row_title_format = NamedStyle(name="b_task_row_title_format")
        b_task_row_title_format.font = Font(bold=True)
        b_task_row_title_format.alignment = Alignment(
            horizontal="center", vertical="center"
        )
        brd = Side(border_style="thin", color="000000")
        b_task_row_title_format.border = Border(
            left=brd, right=brd, top=brd, bottom=brd
        )

        self.wb.add_named_style(b_task_row_title_format)

        b_task_col_title_format = NamedStyle(name="b_task_col_title_format")
        b_task_col_title_format.font = Font(bold=True)
        b_task_col_title_format.fill = PatternFill(
            start_color="00CC99", end_color="00CC99", fill_type="solid"
        )
        b_task_col_title_format.alignment = Alignment(
            horizontal="center", vertical="center"
        )
        brd = Side(border_style="thin", color="000000")
        b_task_col_title_format.border = Border(
            left=brd, right=brd, top=brd, bottom=brd
        )

        self.wb.add_named_style(b_task_col_title_format)

        business_task_text = (
            "<Заполните название модели> \n"
            "например: Модель прогнозирования стоимости арендной ставки коммерческой недвижимости"
        )
        task_description_text = (
            "<Заполните описание модели: цель моделирования, \n"
            "для какого бизнес процесса строится модель, какие данные используются > \n"
            "например: Модель прогнозирования стоимости арендной ставки коммерческой недвижимости. \n"
            "Модель строится на данных ЦОД по информации об открытии/закрытии новых ВСП банка."
        )
        report_dt_description_text = (
            "<Укажите отчетные даты> \n" "например: 31.01.2022, 28.02.2022, 31.03.2022"
        )
        target_description_text = "<Заполните определние целевого события/переменной>"
        data_selection_text = (
            "<Заполните критерии отбора популяции: фильтры, исключения>\n"
            "например: 1. Офисы, открытые на отчетную дату."
        )
        used_algo_text = "<DreamML XGBRegressor>"
        ws.merge_cells("B2:E2")
        ws.merge_cells("B3:E3")
        ws.merge_cells("B4:D4")
        ws.merge_cells("B5:D5")
        ws.merge_cells("B6:E6")
        ws.merge_cells("B7:E7")

        ws["B2"] = business_task_text
        ws["B3"] = task_description_text
        ws["B4"] = report_dt_description_text
        ws["B5"] = data_selection_text
        ws["B6"] = target_description_text
        ws["B7"] = used_algo_text
        ws["E4"] = report_dt_description_text
        ws["E5"] = data_selection_text
        ws["A1"] = "Параметр"
        ws["A2"] = "Бизнес-задача"
        ws["A3"] = "Описание задачи"
        ws["A4"] = "Даты сбора данных"
        ws["A5"] = "Отбор наблюдений"
        ws["A6"] = "Описание целевой переменной"
        ws["A7"] = "Используемый ML-алгоритм"
        ws["B1"] = "Выборка train"
        ws["C1"] = "Выборка valid"
        ws["D1"] = "Выборка test"
        ws["E1"] = "Выборка Out-Of-Time"

        for row in ws["B2":"E7"]:
            for cell in row:
                cell.style = "b_task_cell_format"
        for row in ws["A1":"E1"]:
            for cell in row:
                cell.style = "b_task_col_title_format"
        for row in ws["A2":"A7"]:
            for cell in row:
                cell.style = "b_task_row_title_format"

        for i in range(1, 6):
            ws.column_dimensions[get_column_letter(i)].width = 30
        for i in range(1, 8):
            ws.row_dimensions[i].height = 75

        # Гиперссылка на оглавление
        ws[f"A9"] = "<<< Вернуться к оглавлению"
        ws[f"A9"].hyperlink = f"#'Оглавление'!A1"
        ws[f"A9"].style = "Hyperlink"

    def _create_pipeline_description_page(self, **data):
        """
        Страница с описанием всех стадий пайплайна
        """

        _stagies = [
            "Cбор данных",
            "Разбиение выборки на обучение / валидацию / тест",
            "Способ обработки пропусков",
            "Способ обработки категориальных признаков",
            "Способ отбора признаков",
            "Построенные модели",
            "Оптимизация гиперпараметров модели",
        ]
        _descriptions = [
            "< Прикрепите скрипт для сбора обучающей выборки >",
            (
                "< В DreamML, по умолчанию, разбиение производится на 3 части: "
                "train, valid, test. Соотношение разбиения: 60%, 20%, 20%. >"
            ),
            (
                "< В DreamML, по умолчанию, пропуски заполняются для категориальных "
                "признаков, значение - 'NA'. Для числовых признаков пропуски не "
                "заполняются. >"
            ),
            (
                "< В DreamML, по умолчанию, категориальные признаки обрабатываются "
                "с помощью доработанного LabelEncoder, после чего признаки передаются "
                "в качестве категориальных в модель, которая умеет обрабатывать категории. >"
            ),
            (
                "< В DreamML, по умолчанию, используется следующая цепочка отбора признаков: "
                "Tree importance -> PSI -> Permutation -> ShapUplift -> ShapDelta >"
            ),
            (
                "< В DreamML, по умолчанию, используются модели LightGBM, XGBoost, CatBoost, "
                "WhiteBox AutoML. >"
            ),
            (
                "< В DreamML, по умолчанию, используется BayesianOptimization для "
                "оптимизации гиперпараметров модели."
            ),
        ]
        stats = pd.DataFrame({"Название стадии": _stagies, "Описание": _descriptions})

        stats.to_excel(self.writer, sheet_name="Описание пайплайна", index=False)
        self.sheet_descriptions["Описание пайплайна"] = (
            "Страница с описанием всех стадий пайплайна"
        )

        self.add_table_borders(stats, sheet_name="Описание пайплайна")
        self.add_cell_width(sheet_name="Описание пайплайна")
        self.add_header_color(stats, sheet_name="Описание пайплайна", color="00CC99")
        self.add_numeric_format(
            stats[["Описание"]], sheet_name="Описание пайплайна", startcol=1
        )

        ws = self.sheets["Описание пайплайна"]
        # Гиперссылка на оглавление
        ws[f"A{stats.shape[0] + 3}"] = "<<< Вернуться к оглавлению"
        ws[f"A{stats.shape[0] + 3}"].hyperlink = f"#'Оглавление'!A1"
        ws[f"A{stats.shape[0] + 3}"].style = "Hyperlink"