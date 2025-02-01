import os.path
from copy import deepcopy
from typing import Optional, Dict, Tuple
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelBinarizer
from tqdm.auto import tqdm

from dreamml.reports.reports._base import BaseReport
from dreamml.reports.reports._base import create_used_features_stats

from .._classification_metrics import CalculateClassificationMetrics
from .._classification_metrics import CalculateDataStatistics as Binary_DS
from .._classification_metrics import CalculateDetailedMetrics as Binary_DM
from dreamml.pipeline.cv_score import CVScores
from dreamml.utils.saver import ArtifactSaver
from dreamml.visualization.plots import (
    plot_binary_graph,
    plot_multi_graph,
    plot_token_length_distribution_for_text_features,
)
from dreamml.logging import get_logger
from dreamml.validation.classification import (
    ValidationReport,
    prepare_artifacts_config,
)
from dreamml.validation.nlp.classification.part_3_specification.test_3_1_tokens_importance_check import (
    ModelTokensImportanceAnalysis,
)
from dreamml.modeling.models.estimators import BaseModel

_logger = get_logger(__name__)

CV_SCORE_COL = "cv score"
MODEL_NAME_COL = "Название модели"


class ClassificationDevelopmentReport(BaseReport):
    """
    Отчет о разработанных моделях в DS-Template.

    Отчет содержит:
        - статистику по данным, которые использовались для построения
          моделей: статистика по выборкам (train / valid / ...) и
          признакам;

        - отчет об однофакторном анализе переменных (отбор
          переменных, с помощью метрики Джини);

        - сравнение построенных моделей по метрикам GINI, PR_AUC,
          Log-Loss на выборках (train / valid / ...);

        - детальные метрики для пары модель / выборка.

    Parameters
    ----------
    models: dict
        Словарь с экземплярами построенных моделей.

    other_models: dict
        Словарь с экземплярами построенных моделей на этапе batch selection stages.

    experiment_path: str
        Путь к директории с экспериментом

    config: dict
        Конфигурационный файл параметров эксперимента.

    n_bins: integer, optional, default = 20
        Количество бинов для разбиения вектора прогнозов.

    bootstrap_samples: int
        Количество бутстрап выборок для построения доверительных интервалов.

    p_value: float
        Размер критической зоны для доверительных интервалов (по p_value / 2 с каждой стороны).

    max_feat_per_model: int
        Максимальное количество признаков в модели для построения валидационного светофора.
    cv_scores: CVScores
        Объект класса CVScore, котором хранится значение cv score для основных моделей pipeline и для other models
        Значение cv score - средние значение метрики между фолодов на кросс валидации для каждой модели.
        key: str - название модели
        value: float - значение метрики
    """

    def __init__(
        self,
        models,
        other_models,
        oot_potential,
        experiment_path,
        config,
        n_bins: int = 20,
        bootstrap_samples: int = 200,
        p_value: float = 0.05,
        max_feat_per_model: int = 50,
        predictions: Optional[Dict] = None,
        cv_scores: CVScores = None,
        artifact_saver: Optional[ArtifactSaver] = None,
        vectorizers_dict: Optional[dict] = None,
        etna_pipeline: Optional[dict] = None,
        etna_eval_set: Optional[dict] = None,
        analysis: Optional[dict] = None,
    ):
        super().__init__(
            experiment_path=experiment_path,
            artifact_saver=artifact_saver,
            config=config,
            models=models,
            other_models=other_models,
            oot_potential=oot_potential,
            vectorizers_dict=vectorizers_dict,
        )
        if "psi_importance" in self.models:
            self.psi = self.models.pop("psi_importance")
        else:
            self.psi = None

        self.n_bins = n_bins
        self.bootstrap_samples = bootstrap_samples
        self.p_value = p_value
        self.max_feat_per_model = (
            max_feat_per_model if vectorizers_dict is None else 10_000
        )
        self.predictions = predictions or {}
        # Таблица с моделями и метриками для некоторых листов в excel, создается в create_third_page
        self.models_metrics_df = None
        self.cv_scores = cv_scores

    def create_first_page(self, **eval_sets):
        """
        Первая страница отчета - статистика по исследуемым данным.

        Отчет содержит:
            - статистику по выборкам, которые были использованы для
              построения / валидации / тестирования модели: название
              выборки, количество наблюдений, количество целевых
              событий и долю целевого события в выборке.

            - общую статистику по переменным: название целевой переменной,
              количество категориальных переменных, количество
              непрерывных переменных.

            - детальную статистику по каждой переменным: количество
              непропущенных значений, среднее значение переменной,
              стандартное отклонение по переменной,
              перцентили (0, 25, 50, 75, 100).

        Parameters
        ----------
        eval_sets: Dict[string, Tuple[pandas.DataFrame, pandas.Series]]
            Словарь с выборками, для которых требуется рассчитать статистику.
            Ключ словаря - название выборки (train / valid / ...), значение -
            кортеж с матрицей признаков (data) и вектором ответов (target).

        """
        sheet_name = "Data_Statistics"
        features = eval_sets["train"][0].columns.to_series()
        transformer = Binary_DS(self.encoder, features, self.config, task=self.task)
        result = transformer.transform(**eval_sets)

        startows = [  # TODO restyle: startows -> startrows
            0,
            2 + result[0].shape[0],
            4 + result[0].shape[0] + result[1].shape[0],
        ]
        num_formats = [10, None, None]

        for data, startrow, num_format in zip(result, startows, num_formats):
            data.to_excel(
                self.writer,
                startrow=startrow,
                sheet_name=sheet_name,
                index=False,
            )
            self.set_style(data, "Data_Statistics", startrow, num_format=num_format)

        if self.task in ["multiclass", "multilabel"]:
            if self.task == "multiclass":
                eval_set_cols = self.config["metric_params"]["labels"]
            else:
                eval_set_cols = eval_sets["train"][1].columns.tolist()
            classes = [f"# eventrate {class_name}" for class_name in eval_set_cols]

            for column_number, column in enumerate(classes):
                self.add_eventrate_format(
                    result[0][column],
                    "Data_Statistics",
                    startcol=len(classes) + 2 + column_number,
                    fmt="0.00%",
                )

        self.add_numeric_format(result[2], "Data_Statistics", startrow=startows[-1])
        self._write_distrib_text_feature_hist(eval_sets, sheet_name)
        self._write_token_importance_text_feature_graph(eval_sets, sheet_name)

    def create_second_page(self, **eval_sets):
        """
        Вторая страница отчета - статистика по однофакторному
        анализу разделяющей способности переменных, измеренной
        метрикой Джини.

        Parameters
        ----------
        eval_sets: Dict[string, Tuple[pandas.DataFrame, pandas.Series]]
            Словарь с выборками, для которых требуется рассчитать статистику.
            Ключ словаря - название выборки (train / valid / ...), значение -
            кортеж с матрицей признаков (data) и вектором ответов (target).

        """
        self.gini.to_excel(self.writer, "GINI-Importance", index=False)
        self.set_style(self.gini, "GINI-Importance", 0)
        ws = self.sheets["GINI-Importance"]

        ws.write_string("H2", "Selected - флаг, означающий включение признака в модель")
        ws.write_string("H3", "Selected = 1 - признак включен в модель")
        ws.write_string("H4", "Selected = 0 - признак не включен в модель")
        ws.write_string(
            "H6", "Категориальные переменные автоматически участвуют в обучении"
        )

        ws.set_column(7, 7, 62)
        gini_columns = [col for col in self.gini.columns if "GINI" in col]
        for column_number, column in enumerate(gini_columns):
            self.add_eventrate_format(
                self.gini[column], "GINI-Importance", startcol=1 + column_number, fmt=2
            )

    def create_psi_report(self, **eval_sets):
        """
        Опциональная страница в отчете со статистикой PSI.
        Страница создается, если PSI-был рассчитан и находится в self.models.

        Parameters
        ----------
        eval_sets: Dict[string, Tuple[pandas.DataFrame, pandas.Series]]
            Словарь с выборками, для которых требуется рассчитать статистику.
            Ключ словаря - название выборки (train / valid / ...), значение -
            кортеж с матрицей признаков (data) и вектором ответов (target).

        """
        self.psi.to_excel(self.writer, sheet_name="PSI-Importance", index=False)
        self.set_style(self.psi, "PSI-Importance", 0)
        ws = self.sheets["PSI-Importance"]

        ws.write_string("F2", "Selected - флаг, означающий включение признака в модель")
        ws.write_string("F3", "Selected = 1 - признак включен в модель")
        ws.write_string("F4", "Selected = 0 - признак не включен в модель")
        ws.set_column(5, 5, 62)
        self.add_eventrate_format(
            self.psi["PSI"], "PSI-Importance", startcol=1, fmt="0.0000"
        )

    def create_third_page(
        self, metric_name, metric_col_name, def_gini_flag=False, **eval_sets
    ):
        """
        Третья [четвертая] страница отчета - метрики бинарной
        классификации для каждой модели из self.models и каждая
        выборки из eval_sets.

        Parameters
        ----------
        eval_sets: Dict[string, Tuple[pandas.DataFrame, pandas.Series]]
            Словарь с выборками, для которых требуется рассчитать статистику.
            Ключ словаря - название выборки (train / valid / ...), значение -
            кортеж с матрицей признаков (data) и вектором ответов (target).
        metric_name:
            Имя метрики, которая будет считаться
        """
        transformer = CalculateClassificationMetrics(
            self.models,
            bootstrap_samples=self.bootstrap_samples,
            p_value=self.p_value,
            config=self.config,
            metric_name=metric_name,
            task=self.task,
            predictions=self.predictions,
            vectorizers=self.vectorizers_dict,
        )
        result = transformer.transform(**eval_sets)
        self.predictions = transformer.predictions_

        if not def_gini_flag:
            result = self.add_cv_scores(
                result, self.cv_scores.stage_models, metric_name, metric_col_name
            )

        result = result.round(decimals=2)

        self.models_metrics_df = result

        result.to_excel(
            self.writer, sheet_name="Compare Models " + metric_col_name, index=False
        )
        self.set_style(result, "Compare Models " + metric_col_name, 0)

        df_a = result.drop("детали о модели", axis=1)

        self.add_numeric_format(
            df_a, "Compare Models " + metric_col_name, startrow=0, min_value=100
        )

        ws = self.sheets["Compare Models " + metric_col_name]
        best_test_format = self.wb.add_format({"fg_color": "F0D3F7"})
        best_oot_format = self.wb.add_format({"fg_color": "B7C3F3"})
        self.cv_score_legend(result, ws, 20)

        best_model_info = transformer.get_best_models(stats_df=result, **eval_sets)
        if "OOT" in eval_sets.keys():
            for cell_number, data_value in enumerate(result.columns.values):
                ws.write(
                    best_model_info["test"]["index"] + 1,
                    cell_number,
                    result[data_value][best_model_info["test"]["index"]],
                    best_test_format,
                )

            for cell_number, data_value in enumerate(result.columns.values):
                ws.write(
                    best_model_info["oot"]["index"] + 1,
                    cell_number,
                    result[data_value][best_model_info["oot"]["index"]],
                    best_oot_format,
                )

            if best_model_info["test"]["name"] == best_model_info["oot"]["name"]:
                ws.write(result.shape[0] + 2, 1, best_model_info["oot"]["name"])
                ws.write(
                    result.shape[0] + 2,
                    0,
                    "Лучшая модель для выборки Test и OOT",
                    best_oot_format,
                )

                list_of_args = ["train", "test", "OOT"]
                list_of_letters = ["D", "E", "F"]
                for i in range(len(list_of_args)):
                    sheet_name = f"{list_of_args[i]} {best_model_info['oot']['name']}"
                    url = f"internal:'{sheet_name}'!A1"
                    string = f"Ссылка: {list_of_args[i]}"
                    ws.write_url(
                        f"{list_of_letters[i]}{result.shape[0] + 2 + 1}",
                        url=url,
                        string=string,
                    )

            else:
                ws.write(result.shape[0] + 2, 1, best_model_info["test"]["name"])
                ws.write(result.shape[0] + 3, 1, best_model_info["oot"]["name"])
                ws.write(
                    result.shape[0] + 2,
                    0,
                    "Лучшая модель для выборки Test",
                    best_test_format,
                )
                ws.write(
                    result.shape[0] + 3,
                    0,
                    "Лучшая модель для выборки OOT",
                    best_oot_format,
                )

                list_of_args = ["train", "test", "OOT"]
                list_of_letters = ["D", "E", "F"]
                for i in range(len(list_of_args)):
                    sheet_name = f"{list_of_args[i]} {best_model_info['test']['name']}"
                    url = f"internal:'{sheet_name}'!A1"
                    string = f"Ссылка: {list_of_args[i]}"
                    ws.write_url(
                        f"{list_of_letters[i]}{result.shape[0] + 2 + 1}",
                        url=url,
                        string=string,
                    )
                    sheet_name = f"{list_of_args[i]} {best_model_info['oot']['name']}"
                    url = f"internal:'{sheet_name}'!A1"
                    string = f"Ссылка: {list_of_args[i]}"
                    ws.write_url(
                        f"{list_of_letters[i]}{result.shape[0] + 3 + 1}",
                        url=url,
                        string=string,
                    )
        else:
            for cell_number, data_value in enumerate(result.columns.values):
                ws.write(
                    best_model_info["test"]["index"] + 1,
                    cell_number,
                    result[data_value][best_model_info["test"]["index"]],
                    best_test_format,
                )
            ws.write(result.shape[0] + 2, 1, best_model_info["test"]["name"])
            ws.write(
                result.shape[0] + 2,
                0,
                "Лучшая модель для выборки Test",
                best_test_format,
            )

            list_of_args = ["train", "test"]
            list_of_letters = ["D", "E"]
            for i in range(len(list_of_args)):
                sheet_name = f"{list_of_args[i]} {best_model_info['test']['name']}"
                url = f"internal:'{sheet_name}'!A1"
                string = f"Ссылка: {list_of_args[i]}"
                ws.write_url(
                    f"{list_of_letters[i]}{result.shape[0] + 2 + 1}",
                    url=url,
                    string=string,
                )

        msg = "Данный выбор лучшей модели носит рекомендательный характер!"
        ws.write(result.shape[0] + 10, 0, msg, self.wb.add_format({"bold": True}))
        msg = "Определение лучшей модели происходит по методике:"
        ws.write(result.shape[0] + 11, 0, msg)
        msg = (
            "Для модели с самой высокой метрикой "
            + metric_name
            + " на выборке Test строится доверительный интервал"
        )
        ws.write(result.shape[0] + 12, 0, msg)
        msg = (
            "Из всех моделей чья метрика  "
            + metric_name
            + " на выборке Test попадает в данный доверительный интервал "
            "выбирается модель с минимальным количеством признаков"
        )
        ws.write(result.shape[0] + 13, 0, msg)
        msg = "При наличии Out-of-time выборки, для нее строится все тоже самое."
        ws.write(result.shape[0] + 14, 0, msg)

        msg = "Рекомендовано выбирать модель от 20 до 40 признаков, при условии отсутствия просадок в качестве."
        ws.write(result.shape[0] + 16, 0, msg)
        msg = "Дополнительные модели полученные на стадиях динамического отбора признаков представлены по ссылке:"
        ws.write(result.shape[0] + 17, 0, msg)

        url = "internal:'Other Models'!A1"
        string = "Ссылка на лист Other Models"
        ws.write_url(f"A{result.shape[0] + 18 + 1}", url=url, string=string)

        # Доверительные интервалы
        bold_cell_format = self.wb.add_format(
            {"bold": True, "top": 1, "bottom": 1, "left": 1, "right": 1}
        )
        bold_cell_format.set_align("right")
        normal_cell_format = self.wb.add_format(
            {"top": 1, "bottom": 1, "left": 1, "right": 1}
        )
        ws.write(
            result.shape[0] + 6,
            0,
            "Доверительные интервалы:",
            self.wb.add_format({"bold": True}),
        )
        ws.write(result.shape[0] + 7, 0, "Test", bold_cell_format)
        ws.write(
            result.shape[0] + 7,
            1,
            round(best_model_info["test"]["ci"][0], 2),
            normal_cell_format,
        )
        ws.write(
            result.shape[0] + 7,
            2,
            round(best_model_info["test"]["ci"][1], 2),
            normal_cell_format,
        )
        if "OOT" in eval_sets.keys():
            ws.write(result.shape[0] + 8, 0, "OOT", bold_cell_format)
            ws.write(
                result.shape[0] + 8,
                1,
                round(best_model_info["oot"]["ci"][0], 2),
                normal_cell_format,
            )
            ws.write(
                result.shape[0] + 8,
                2,
                round(best_model_info["oot"]["ci"][1], 2),
                normal_cell_format,
            )

        ws.write(
            result.shape[0] + 7,
            4,
            f"Alpha = {self.p_value} (по {self.p_value / 2} с каждой стороны)",
        )
        ws.set_column(0, 0, 37)

    def cv_score_legend(self, result, ws, add_row):
        if CV_SCORE_COL not in result.columns.tolist():
            return
        msg = "Колонка cv_score показывает среднее значение метрики между фолдами кросс-валидации"
        ws.write(result.shape[0] + add_row, 0, msg, self.wb.add_format({"bold": False}))
        msg = "0 в колонке cv_score означает не возможность посчитать его для конкретной модели"
        ws.write(
            result.shape[0] + add_row + 1, 0, msg, self.wb.add_format({"bold": False})
        )

    @staticmethod
    def add_cv_scores(
        metrics: pd.DataFrame, cv_scores: dict, metric_name: str, metric_col_name: str
    ) -> pd.DataFrame:
        """
        Добавление колонки cv scores вместо gini valid в лист compare models GINI
        Parameters
        ----------
        metrics: pd.DataFrame
            Датафрейм со значением метрики GINI для каждой модели и каждой выборки
        cv_scores: dict
            Словарь со значениями cv score для разных моделей

        Returns
        -------
        with_cv_score: pd.DataFrame
            Датафрейм со столбцом cv scores вместо gini valid

        """
        if not cv_scores:
            return metrics
        with_cv_score = deepcopy(metrics)
        cv_scores_df = pd.DataFrame(
            list(cv_scores.items()), columns=[MODEL_NAME_COL, CV_SCORE_COL]
        )
        with_cv_score = with_cv_score.merge(cv_scores_df, on=MODEL_NAME_COL, how="left")
        with_cv_score = with_cv_score.fillna(0)
        # TODO добавить возможность считать cv_score для разных метрик
        index1 = with_cv_score.columns.tolist().index(metric_name + " valid")
        index2 = with_cv_score.columns.tolist().index(CV_SCORE_COL)
        new_order = with_cv_score.columns.tolist()
        new_order[index1] = new_order.pop(index2)
        return with_cv_score[new_order]

    def create_other_model_page(self, metric_name, metric_col_name, **eval_sets):
        """
        Третья [четвертая] страница отчета - метрики бинарной
        классификации для каждой модели из self.other_models (модели построенные на batch selection stages)
        и каждая выборки из eval_sets.

        Parameters
        ----------
        eval_sets: Dict[string, Tuple[pandas.DataFrame, pandas.Series]]
            Словарь с выборками, для которых требуется рассчитать статистику.
            Ключ словаря - название выборки (train / valid / ...), значение -
            кортеж с матрицей признаков (data) и вектором ответов (target).
        """
        transformer = CalculateClassificationMetrics(
            self.other_models,
            bootstrap_samples=self.bootstrap_samples,
            p_value=self.p_value,
            config=self.config,
            metric_name=metric_name,
            task=self.task,
            vectorizers=self.vectorizers_dict,
        )
        result = transformer.transform(**eval_sets)

        result = self.add_cv_scores(
            result, self.cv_scores.other_models, metric_name, metric_col_name
        )
        result = result.round(decimals=2)

        df_a = result.drop("детали о модели", axis=1)

        df_a.to_excel(self.writer, sheet_name="Other Models", index=False)
        self.set_style(df_a, "Other Models", 0)

        self.add_numeric_format(df_a, "Other Models", startrow=0, min_value=100)

        ws = self.sheets["Other Models"]
        msg = "На данном листе представлены все модели полученные на стадиях динамического отбора признаков."
        ws.write(df_a.shape[0] + 3, 0, msg)
        msg = (
            "Данные модели автоматически сохраняются на диск и хранятся в папке с экспериментом в директории "
            "other_models. По умолчанию порог для сохранения до 100 фич в модели."
        )
        ws.write(df_a.shape[0] + 4, 0, msg)
        msg = "Рекомендовано выбирать модель от 20 до 40 признаков, при условии отсутствия просадок в качестве."
        ws.write(df_a.shape[0] + 5, 0, msg)

        self.cv_score_legend(df_a, ws, 7)

    def create_oot_pot_page(self):
        """
        Третья [четвертая] страница отчета - метрики бинарной
        классификации для каждой модели из self.other_models (модели построенные на batch selection stages)
        и каждая выборки из eval_sets.

        Parameters
        ----------
        eval_sets: Dict[string, Tuple[pandas.DataFrame, pandas.Series]]
            Словарь с выборками, для которых требуется рассчитать статистику.
            Ключ словаря - название выборки (train / valid / ...), значение -
            кортеж с матрицей признаков (data) и вектором ответов (target).
        """
        if self.config.get("use_oot_potential", False) and self.config.get(
            "oot_data_path", False
        ):
            df_a = pd.DataFrame(data=[self.oot_potential[0]])
            df_shap = self.oot_potential[1]
            df_a.to_excel(self.writer, sheet_name="OOT Potential", index=False)
            df_shap.to_excel(
                self.writer,
                sheet_name="OOT Potential",
                startrow=df_a.shape[0] + 2,
                index=False,
            )

            self.set_style(df_a, "OOT Potential", 0)
            self.add_numeric_format(df_a, "OOT Potential", startrow=0, min_value=100)
            self.set_style(df_shap, "OOT Potential", df_a.shape[0] + 2)

            ws = self.sheets["OOT Potential"]
            msg = "Введем показатель потенциал данных OOT."
            ws.write("E4", msg)
            msg = "Используется как оценка сверху для выбранной модели."
            ws.write("E5", msg)
            msg = "Данное число может быть нерелевантным из-за большого отношения dev и oot выборок"
            ws.write("E6", msg)
            msg = "или различия в распределениях dev и oot выборок."
            ws.write("E7", msg)

            msg = (
                "Adversarial Validation используется для оценки сходства распределений."
            )
            ws.write("E9", msg)
            msg = "При числе, близком к нулю, выборки dev и oot примерно из одного распределения."
            ws.write("E10", msg)

    def create_traffic_light_page(self, metric_name, metric_col_name, **eval_sets):
        """
        Страница отчета с валидационными тестами.
        Строится итоговый светофор для каждой модели соответствующей заявленной сложности.

        Parameters
        ----------
        eval_sets: Dict[string, Tuple[pandas.DataFrame, pandas.Series]]
            Словарь с выборками, для которых требуется рассчитать статистику.
            Ключ словаря - название выборки (train / valid / ...), значение -
            кортеж с матрицей признаков (data) и вектором ответов (target).
        """
        df = self.models_metrics_df
        n = 6 if "OOT" in eval_sets.keys() else 5
        # TODO сделать динамическое расширение, т.к. в регрессии больше колонок с метриками
        url_col = "K" if "OOT" in eval_sets.keys() else "J"

        traffic_light_df = pd.DataFrame(
            columns=df.columns[:n].to_list()
            + ["Тест 1", "Тест 2", "Тест 3", "Тест 4", "Итог"]
            + df.columns[-1:].to_list()
        )

        models_for_traffic_light = df[df["# признаков"] <= self.max_feat_per_model][
            MODEL_NAME_COL
        ].to_numpy()

        for model_idx, model in enumerate(models_for_traffic_light):
            experiment_path = Path(self.experiment_path)
            experiment_dir_name = str(experiment_path.name)
            results_path = str(experiment_path.parent)

            model_: BaseModel = self.models[model]
            vectorizer_name = None
            if model_.vectorization_name is not None:
                if model_.vectorization_name != "bert":
                    vectorizer_name = f"{model_.vectorization_name}_vectorizer"

            config = {
                "dir_name": experiment_dir_name,
                "results_path": results_path,
                "model_name": model,
                "vectorizer_name": vectorizer_name,
                "task": self.task,
                "subtask": self.config.get("subtask", "tabular"),
                "text_column": self.config.get("text_column", []),
                "text_preprocessed_column": self.config.get(
                    "text_preprocessed_column", []
                ),
            }
            artifacts_config, data = prepare_artifacts_config(config)
            artifacts_config["metric_name"] = metric_name
            artifacts_config["metric_col_name"] = metric_col_name
            artifacts_config["metric_params"] = self.config.get("metric_params")
            artifacts_config["task"] = self.config.get("task")
            artifacts_config["subtask"] = self.config.get("subtask")
            artifacts_config["text_column"] = self.config.get("text_column", [])
            artifacts_config["text_preprocessed_column"] = self.config.get(
                "text_preprocessed_column", []
            )

            # TODO сделать выбор между классами отчётов
            report = ValidationReport(
                config=config, create_file=False, **artifacts_config
            )

            traffic_light = report.create_traffic_light(**data)
            traffic_light_df.loc[model_idx] = (
                df[df[MODEL_NAME_COL] == model][df.columns[:n]].values[0].tolist()
                + traffic_light
                + df[df[MODEL_NAME_COL] == model][df.columns[-1:]].values[0].tolist()
            )

        traffic_light_df.to_excel(
            self.writer, sheet_name="Validation " + metric_col_name, index=False
        )
        try:
            self.set_style(traffic_light_df, "Validation " + metric_col_name, 0)
        except IndexError:
            _logger.exception("Невозможно применить форматирование к таблице в excel.")

        ws = self.sheets["Validation " + metric_col_name]

        # Раскраска светофора
        red_format = self.wb.add_format({"bg_color": "CC0000"})
        yellow_format = self.wb.add_format({"bg_color": "FFFF33"})
        green_format = self.wb.add_format({"bg_color": "66CC99"})
        ws.conditional_format(
            "A2:Z100",
            {
                "type": "cell",
                "criteria": "equal to",
                "value": '"red"',
                "format": red_format,
            },
        )
        ws.conditional_format(
            "A2:Z100",
            {
                "type": "cell",
                "criteria": "equal to",
                "value": '"yellow"',
                "format": yellow_format,
            },
        )
        ws.conditional_format(
            "A2:Z100",
            {
                "type": "cell",
                "criteria": "equal to",
                "value": '"green"',
                "format": green_format,
            },
        )

        # Гипрессылки
        sheet_format = self.wb.add_format({"left": True, "right": True, "bottom": True})
        for model_idx, model in enumerate(models_for_traffic_light):
            url = f"internal:'train {model}'!A1"
            string = f"Ссылка на лист train {model}"
            ws.write_url(f"{url_col}{model_idx + 2}", url, sheet_format, string)

        msg = "Лист с валидационными тестами"
        ws.write(traffic_light_df.shape[0] + 3, 0, msg)
        msg = "Тест 2 - тест 2.1 на качество модели."
        ws.write(traffic_light_df.shape[0] + 4, 0, msg)
        msg = "Тест 3 - тест 3.1 калибровка модели."
        ws.write(traffic_light_df.shape[0] + 5, 0, msg)
        msg = "Тест 5 - результат тестов 5.2, 5.6, 5.7 на стабильность модели."
        ws.write(traffic_light_df.shape[0] + 6, 0, msg)
        msg = "Тест на качество данных не проводился, так как он не зависит от модели и имеет итоговою оценку"
        ws.write(traffic_light_df.shape[0] + 7, 0, msg)
        msg = "только желтый или зеленый. Данный тест проводится в полном валидационном отчете."
        ws.write(traffic_light_df.shape[0] + 8, 0, msg)

    def create_fourth_page(self, **eval_sets):
        """
        Третья [четвертая] страница отчета - метрики бинарной
        классификации для каждой модели из self.models и каждая
        выборки из eval_sets.

        Parameters
        ----------
        eval_sets: Dict[string, Tuple[pandas.DataFrame, pandas.Series]]
            Словарь с выборками, для которых требуется рассчитать статистику.
            Ключ словаря - название выборки (train / valid / ...), значение -
            кортеж с матрицей признаков (data) и вектором ответов (target).

        """
        transformer = CalculateClassificationMetrics(
            self.models,
            bootstrap_samples=self.bootstrap_samples,
            p_value=self.p_value,
            config=self.config,
            metric_name="precision_recall_auc",
            task=self.task,
            vectorizers=self.vectorizers_dict,
        )
        result = transformer.transform(**eval_sets)

        result = result.round(decimals=2)

        result.to_excel(self.writer, sheet_name="Compare Models PR-AUC", index=False)
        self.set_style(result, "Compare Models PR-AUC", 0)

        df_a = result.drop("детали о модели", axis=1)

        self.add_numeric_format(
            df_a, "Compare Models PR-AUC", startrow=0, min_value=100
        )

    def create_fifth_page(self, **eval_sets):
        """
        Четвертая [пятая] страница отчета - список используемых признаков.
        """
        result = create_used_features_stats(
            self.models, self.vectorizers_dict, **eval_sets
        )

        if isinstance(result, pd.DataFrame):
            result.to_excel(self.writer, sheet_name="Used Features", index=False)
            self.set_style(result, "Used Features", 0)
        else:
            for vec_name, df in result.items():
                sheet_name = f"UF {vec_name}"[:30]
                df.to_excel(self.writer, sheet_name=sheet_name, index=False)
                self.set_style(df, sheet_name, 0)

    def create_model_report(self, **eval_sets):
        """
        Страницы с отчетом для пары модель / выборка из eval_sets.

        Parameters
        ----------
        eval_sets: Dict[string, Tuple[pandas.DataFrame, pandas.Series]]
            Словарь с выборками, для которых требуется рассчитать статистику.
            Ключ словаря - название выборки (train / valid / ...), значение -
            кортеж с матрицей признаков (data) и вектором ответов (target).

        """

        metric_params = self.config.get("metric_params")
        metric_name = self.config.get("eval_metric")

        for model in tqdm(self.models):
            for sample in eval_sets:
                sheet_name = f"{sample} {model}"
                y_true, y_pred = eval_sets[sample][1], self.predictions[model][sample]

                transformer = Binary_DM(
                    self.n_bins, metric_name, metric_params, task=self.task
                )
                data = transformer.transform(y_true, y_pred)

                if self.task in ["binary", "multiclass"]:
                    self._write_graphs_binary_multiclass(
                        eval_sets,
                        y_true,
                        y_pred,
                        data,
                        sheet_name,
                        metric_params["labels"],
                    )
                elif self.task == "multilabel":
                    self._write_graphs_multilabel(
                        sample, eval_sets, y_true, y_pred, data, sheet_name
                    )
                else:
                    raise ValueError(
                        'Supports only "multilabel", "multiclass" and "binary" tasks.'
                    )

    def _write_graphs_binary_multiclass(
        self, eval_sets, y_true, y_pred, data, sheet_name, labels
    ):
        sheet_name = sheet_name[:30] if len(sheet_name) >= 30 else sheet_name
        data.to_excel(self.writer, sheet_name=sheet_name, index=False)
        self.set_style(data, sheet_name, 0)
        self.add_numeric_format(data, sheet_name, min_value=200)
        if self.task == "binary":
            self.add_eventrate_format(data["eventrate"], sheet_name)
        self.create_compare_models_url(data, sheet_name, fmt_col_4=2)
        self.create_model_url(**eval_sets)

        ws = self.sheets[sheet_name]
        if self.task == "binary":
            plot_binary_graph(
                y_true, y_pred, f"{self.experiment_path}/images/{sheet_name}.png"
            )
            ws.insert_image(
                f"A{len(data) + 5}",
                f"{self.experiment_path}/images/{sheet_name}.png",
            )

        elif self.task == "multiclass" and self.plot_multi_graphs:
            arange_labels = np.arange(len(labels))
            # labels_dict = dict(zip(arange_labels, labels))
            label_binarizer = LabelBinarizer().fit(arange_labels)
            # labels_in_sample = [
            #     labels_dict[label]
            #     for label in arange_labels
            #     if label in y_true.unique()
            # ]
            labels_in_sample = arange_labels
            y_true_binarized = pd.DataFrame(
                data=label_binarizer.transform(y_true), columns=labels_in_sample
            )

            pic_path = f"{self.experiment_path}/images/{sheet_name}_macro.png"
            plot_multi_graph(
                y_true=y_true_binarized.values,
                y_pred_proba=y_pred,
                save_path=pic_path,
                classes=labels_in_sample,
            )
            ws.insert_image(
                f"A{len(data) + 5}",
                f"{self.experiment_path}/images/{sheet_name}_macro.png",
            )

    def _write_graphs_multilabel(
        self, sample, eval_sets, y_true, y_pred, data, sheet_name: str
    ):
        for class_idx, item in enumerate(data):
            y_true_class = y_true.iloc[:, class_idx]
            y_pred_class = y_pred[:, class_idx]

            if self.target_with_nan_values is True:
                y_true_mask = y_true_class.isnull()
                y_true_class = y_true_class[~y_true_mask]
                y_pred_class = y_pred_class[~y_true_mask]

            class_name = item[0]
            score = item[1]
            startrow = class_idx * 25
            table_name = pd.DataFrame(columns=[class_name, sample])
            score.to_excel(
                self.writer, sheet_name=sheet_name, index=False, startrow=startrow
            )
            self.set_style(score, sheet_name, startrow=startrow)
            self.add_numeric_format(score, sheet_name, min_value=100, startrow=startrow)
            self.add_eventrate_format(score["eventrate"], sheet_name, startrow=startrow)
            self.create_compare_models_url(score, sheet_name)
            self.create_model_url(**eval_sets)
            ws = self.sheets[sheet_name]

            # График по каждому классу
            if sample in self.samples_to_plot and class_idx < self.max_classes_plot:
                pic_path = (
                    f"{self.experiment_path}/images/{sheet_name}_{class_name}.png"
                )
                plot_binary_graph(y_true_class, y_pred_class, pic_path)
                table_name.to_excel(
                    self.writer,
                    sheet_name=sheet_name,
                    index=False,
                    startrow=startrow,
                    startcol=27,
                )
                ws.insert_image(
                    f"AA{3+ startrow}",
                    f"{self.experiment_path}/images/{sheet_name}_{class_name}.png",
                )
                if self.show_save_paths:
                    _logger.debug(
                        f"Saving graph {self.experiment_path}/images/{sheet_name}_{class_name}.png"
                    )

        if self.plot_multi_graphs:
            # График общий
            pic_path = f"{self.experiment_path}/images/{sheet_name}_macro.png"
            plot_multi_graph(
                y_true=y_true.values,
                y_pred_proba=y_pred,
                save_path=pic_path,
                classes=y_true.columns.tolist(),
            )
            ws.insert_image(
                f"A{25 * len(data) + 5}",
                f"{self.experiment_path}/images/{sheet_name}_macro.png",
            )
            if self.show_save_paths:
                _logger.debug(
                    f"Saving graph {self.experiment_path}/images/{sheet_name}_multi.png"
                )

    def _write_distrib_text_feature_hist(self, eval_set, sheet_name):
        ws = self.sheets[sheet_name]
        rownum = 7

        text_features = (
            self.config["text_features"] + self.config["text_features_preprocessed"]
        )

        if text_features:
            for sample_name, (x_sample, _) in eval_set.items():
                for text_feature in text_features:
                    save_path = f"{self.experiment_path}/images/{sheet_name}_{sample_name}_{text_feature}.png"

                    plot_token_length_distribution_for_text_features(
                        sample_name, text_feature, x_sample, save_path, n_bins=50
                    )
                    ws.insert_image(f"J{rownum}", save_path)
                    rownum += 20

    def _write_token_importance_text_feature_graph(self, eval_set, sheet_name):
        ws = self.sheets[sheet_name]
        rownum = 7

        text_features_preprocessed = self.config["text_features_preprocessed"]

        for text_feature in text_features_preprocessed:
            eval_set_cp = deepcopy(eval_set)

            for sample_name, (X_sample, y_sample) in eval_set_cp.items():
                eval_set_cp[sample_name] = (X_sample[text_feature], y_sample)

            images_dir_path = f"{self.experiment_path}/images/"
            split_test = ModelTokensImportanceAnalysis(None, images_dir_path)
            chi_results = split_test.calculate_stats(eval_set_cp, text_feature)[1]
            for col in chi_results.columns:
                save_path = f"{images_dir_path}{text_feature}_{col}.png"
                if os.path.exists(save_path):
                    ws.insert_image(f"U{rownum}", save_path)
                    rownum += 40

    def transform(self, **eval_sets):
        """
        Создание отчета о разработанных моделях.

        Parameters
        ----------
        eval_sets: Dict[string, Tuple[pandas.DataFrame, pandas.Series]]
            Словарь с выборками, для которых требуется рассчитать статистику.
            Ключ словаря - название выборки (train / valid / ...), значение -
            кортеж с матрицей признаков (data) и вектором ответов (target).

        """
        self.create_dml_info_page()
        self.create_zero_page()
        self.create_first_page(**eval_sets)
        # self.create_second_page(**eval_sets)  # Gini metric
        if isinstance(self.psi, pd.DataFrame):
            self.create_psi_report(**eval_sets)
        if (
            self.task in ("binary", "multiclass", "multilabel")
            and self.config.get("eval_metric") != "gini"
        ):
            self.create_third_page("gini", "gini", def_gini_flag=True, **eval_sets)
            self.create_traffic_light_page("gini", "gini", **eval_sets)

        self.create_third_page(
            self.config.get("eval_metric"),
            self.config.get("metric_col_name"),
            **eval_sets,
        )
        self.create_traffic_light_page(
            self.config.get("eval_metric"),
            self.config.get("metric_col_name"),
            **eval_sets,
        )

        if self.other_models:
            self.create_other_model_page(
                self.config.get("eval_metric"),
                self.config.get("metric_col_name"),
                **eval_sets,
            )
        self.create_oot_pot_page()
        self.create_fourth_page(**eval_sets)
        self.create_fifth_page(**eval_sets)
        self.create_model_report(**eval_sets)
        self.writer.save()