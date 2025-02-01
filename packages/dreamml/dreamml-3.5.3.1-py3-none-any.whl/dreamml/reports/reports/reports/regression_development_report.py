import pandas as pd
from typing import Optional, Dict
from tqdm.auto import tqdm
from xlsxwriter.utility import xl_col_to_name
from scipy.stats import pearsonr, spearmanr

from dreamml.modeling.metrics.metrics_mapping import metrics_mapping
from dreamml.reports.reports._base import BaseReport
from dreamml.reports.reports._base import create_used_features_stats
from .._regression_metrics import CalculateRegressionMetrics
from .._regression_metrics import CalculateDetailedMetrics as Regression_DM
from .._regression_metrics import CalculateDataStatistics as Regression_DS
from dreamml.utils.saver import ArtifactSaver
from dreamml.visualization.plots import (
    plot_regression_graph,
)

CV_SCORE_COL = "cv score"
MODEL_NAME_COL = "Название модели"


class RegressionDevelopmentReport(BaseReport):
    """
    Отчет о разработанных моделях в DreamML.

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

    experiment_path: str
        Путь до папки с экспериментом

    config: dict
        Конфигурационный файл параметров эксперимента.

    n_bins: integer, optional, default = 20
        Количество бинов для разбиения вектора прогнозов.

    """

    def __init__(
        self,
        models,
        other_models,
        oot_potential,
        experiment_path: str,
        config,
        n_bins: int = 20,
        artifact_saver: Optional[ArtifactSaver] = None,
        etna_pipeline: Optional[dict] = None,
        etna_eval_set: Optional[dict] = None,
        vectorizers_dict: Optional[dict] = None,
        bootstrap_samples: Optional[dict] = None,
        p_value: Optional[dict] = None,
        max_feat_per_model: Optional[dict] = None,
        predictions: Optional[dict] = None,
        cv_scores: Optional[dict] = None,
        analysis: Optional[dict] = None,
    ):
        super().__init__(
            experiment_path,
            artifact_saver=artifact_saver,
            config=config,
            models=models,
            other_models=other_models,
            oot_potential=oot_potential,
        )
        self.corr = self.models.pop("corr_importance", None)
        self.psi = self.models.pop("psi_importance", None)

        self.target_transformer = self.models.pop("log_target_transformer")

        self.config = config
        self.n_bins = n_bins
        self.etna_pipeline = etna_pipeline
        self.etna_eval_set = etna_eval_set

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
        transformer = Regression_DS(
            self.encoder, self.target_transformer, self.corr, self.config
        )
        result = transformer.transform(**eval_sets)

        if len(result) < 4:
            startows = [
                0,
                2 + result[0].shape[0],
                4 + result[0].shape[0] + result[1].shape[0],
            ]
            num_formats = [10, None, None]
        else:
            startows = [
                0,
                2 + result[0].shape[0],
                4 + result[0].shape[0] + result[1].shape[0],
                6 + result[0].shape[0] + result[1].shape[0] + result[2].shape[0],
            ]
            num_formats = [10, 10, None, None]

        for data, startrow, num_format in zip(result, startows, num_formats):
            data.to_excel(
                self.writer,
                startrow=startrow,
                sheet_name="Data_Statistics",
                index=False,
            )
            self.set_style(data, "Data_Statistics", startrow, num_format=None)

        self.add_numeric_format(result[0], "Data_Statistics", startrow=startows[0])
        # self.add_numeric_format(result[2], "Data_Statistics", startrow=startows[-1])
        sheet_format = self.wb.add_format({"right": True, "bottom": True})

        ws = self.sheets["Data_Statistics"]
        ws.write(len(result[0]), 9, result[0].values[-1, -1], sheet_format)

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
        self.corr.to_excel(self.writer, "Correlation-Importance", index=False)
        self.set_style(self.corr, "Correlation-Importance", 0)
        ws = self.sheets["Correlation-Importance"]

        ws.write_string("E2", "Selected - флаг, означающий включение признака в модель")
        ws.write_string("E3", "Selected = 1 - признак включен в модель")
        ws.write_string("E4", "Selected = 0 - признак не включен в модель")
        ws.write_string(
            "E6", "Категориальные переменные автоматически участвуют в обучении"
        )
        ws.set_column(4, 4, 62)

        if self.corr.shape[1] > 3:
            self.add_eventrate_format(
                self.corr["Correlation-Train"],
                "Correlation-Importance",
                startcol=1,
                fmt=2,
            )
            self.add_eventrate_format(
                self.corr["Correlation-Valid"],
                "Correlation-Importance",
                startcol=2,
                fmt=2,
            )
        else:
            self.add_eventrate_format(
                self.corr["Correlation"], "Correlation-Importance", startcol=1, fmt=2
            )

    def create_psi_report(self, **eval_sets):
        """
        Опциональная страница в отчете со статистикой PSI.
        Страница создается, если PSI-был рассчитан и находится в self.models.

        """
        self.psi.to_excel(self.writer, sheet_name="PSI-Importance", index=False)
        self.set_style(self.psi, "PSI-Importance", 0)
        ws = self.sheets["PSI-Importance"]

        ws.write_string("E2", "Selected - флаг, означающий включение признака в модель")
        ws.write_string("E3", "Selected = 1 - признак включен в модель")
        ws.write_string("E4", "Selected = 0 - признак не включен в модель")
        ws.set_column(4, 4, 62)
        self.add_eventrate_format(
            self.psi["PSI"], "PSI-Importance", startcol=1, fmt="0.0000"
        )

    def create_third_page(self, **eval_sets):
        """
        Третья [четвертая] страница отчета - метрики задачи
        регрессии для каждой модели из self.models и каждая
        выборки из eval_sets.

        Parameters
        ----------
        eval_sets: Dict[string, Tuple[pandas.DataFrame, pandas.Series]]
            Словарь с выборками, для которых требуется рассчитать статистику.
            Ключ словаря - название выборки (train / valid / ...), значение -
            кортеж с матрицей признаков (data) и вектором ответов (target).

        """
        transformer = CalculateRegressionMetrics(
            models=self.models,
            log_transformer=self.target_transformer,
            vectorizers=self.vectorizers_dict,
        )
        result = transformer.transform(**eval_sets)
        self.predictions = transformer.predictions_

        if self.config["use_etna"]:
            scores_df = self._get_etna_pipline_metrics()
            scores_df.to_excel(
                self.writer,
                sheet_name="Compare Models",
                index=False,
                startrow=len(result) + 2,
            )

        startcol, endcol = 2 + len(eval_sets), 2 + 3 * len(eval_sets) - 1
        result = result.round(
            3
        )  # Округление, потому что дальше не работает код числового формата
        result.to_excel(self.writer, sheet_name="Compare Models", index=False)
        self.set_style(result, "Compare Models", 0)

        cols = [col for col in result.columns if "MAE" in col]
        cols = cols + [MODEL_NAME_COL, "детали о модели"]
        df_a = result.drop("детали о модели", axis=1)
        df_b = result.drop(cols, axis=1)

        ws = self.sheets["Compare Models"]

        # FIXME: Далее идет код, переводящий клетки Excel в числовые,
        #  но функции написаны ужасны и это приводит к смещению данных

        # серый цвет для метрик PR-AUC, Log-Loss
        # self.add_text_color("Compare Models", startcol, endcol)
        # self.add_numeric_format(df_a, "Compare Models", 0, min_value=100)
        # self.add_numeric_format(
        #     df_b, "Compare Models", 0, 1 + len(eval_sets), color="C8C8C8"
        # )

    def _get_etna_pipline_metrics(self):
        etna_used_features = (
            self.etna_pipeline.pipeline.model._base_model.model.feature_names_
        )
        num_features = len(etna_used_features)
        scores_dict, metrics = {
            "Название модели": "etna_pipeline",
            "# признаков": num_features,
        }, {}

        for name in ["mae", "mape", "rmse", "r2"]:
            if name not in metrics:
                metrics[name] = metrics_mapping[name]()
        metrics["pearsonr"] = pearsonr
        metrics["spearmanr"] = spearmanr

        sample_names = ["train_ts", "valid_ts", "test_ts"]
        if "oot_ts" in self.etna_eval_set and self.etna_eval_set["oot_ts"] is not None:
            sample_names.append("oot_ts")
        for metric_name, metric in metrics.items():
            for sample_name in sample_names:
                column_name = f"{metric_name} {sample_name}"
                if (
                    sample_name in self.etna_eval_set
                    and self.etna_eval_set[sample_name] is not None
                ):
                    sample = self.etna_eval_set[sample_name]
                    y_true = sample.to_pandas(flatten=True)["target"]
                    y_pred = self.etna_pipeline.transform(sample, return_dataset=False)
                    score = metric(y_true, y_pred)
                    if isinstance(score, tuple):
                        score = score[0]
                    score = [round(score, 2)]
                    # score = [round(100 * score, 2)]
                else:
                    score = "-"
                scores_dict[column_name] = score
        scores_dict["детали о модели"] = "-"
        scores_df = pd.DataFrame(scores_dict)
        return scores_df

    def create_other_model_page(self, **eval_sets):
        """
        Третья [четвертая] страница отчета - метрики регрессии
        классификации для каждой модели из self.other_models (модели построенные на batch selection stages)
        и каждая выборки из eval_sets.

        Parameters
        ----------
        eval_sets: Dict[string, Tuple[pandas.DataFrame, pandas.Series]]
            Словарь с выборками, для которых требуется рассчитать статистику.
            Ключ словаря - название выборки (train / valid / ...), значение -
            кортеж с матрицей признаков (data) и вектором ответов (target).
        """
        transformer = CalculateRegressionMetrics(
            models=self.other_models,
            log_transformer=self.target_transformer,
        )
        result = transformer.transform(**eval_sets)
        result = result.round(decimals=2)

        df_a = result.drop("детали о модели", axis=1)

        df_a.to_excel(self.writer, sheet_name="Other Models", index=False)
        self.set_style(df_a, "Other Models", 0)

        self.add_numeric_format(df_a, "Other Models", startrow=0, min_value=100)

        ws = self.sheets["Other Models"]

        msg = "На данном листе представлены все модели полученные на стадиях динамического отбора признаков."
        ws.write(df_a.shape[0] + 5, 0, msg)
        msg = (
            "Данные модели автоматически сохраняются на диск и хранятся в папке с экспериментом в директории "
            "other_models. По умолчанию порог для сохранения до 100 фич в модели."
        )
        ws.write(df_a.shape[0] + 6, 0, msg)
        msg = "Рекомендовано выбирать модель от 20 до 40 признаков, при условии отсутствия просадок в качестве."
        ws.write(df_a.shape[0] + 7, 0, msg)

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
        transformer = Regression_DM(self.target_transformer, self.n_bins)
        for model in tqdm(self.models):
            for sample in eval_sets:
                sheet_name = f"{sample} {model}"
                y_true, y_pred = eval_sets[sample][1], self.predictions[model][sample]

                if self.target_transformer.fitted:
                    y_true = self.target_transformer.inverse_transform(y_true)

                data = transformer.transform(y_true, y_pred)
                data.to_excel(self.writer, sheet_name=sheet_name, index=False)

                self.set_style(data, sheet_name, 0)
                self.add_numeric_format(data, sheet_name, min_value=100)
                self.create_compare_models_url(data, sheet_name)
                self.create_model_url(**eval_sets)

                # график
                ws = self.sheets[sheet_name]

                plot_regression_graph(
                    y_true, y_pred, f"{self.experiment_path}/images/{sheet_name}"
                )
                ws.insert_image(
                    f"A{len(data) + 7}",
                    f"{self.experiment_path}/images/{sheet_name}.png",
                )

    def create_four_page(self, **eval_sets):
        """
        Четвертая [пятая] страница отчета - список используемых признаков.
        """
        df = create_used_features_stats(self.models, **eval_sets)
        df.to_excel(self.writer, sheet_name="Used Features", index=False)
        self.set_style(df, "Used Features", 0)

    def create_model_url(self, **eval_sets):
        """
        Создание ссылки на лист с отчетом модель / выборка и
        добавление на лист Compare Models.

        Parameters
        ----------
        data: pandas.core.frame.DataFrame
            Матрица с рассчитанными метриками.

        eval_sets: Dict[string, Tuple[pandas.DataFrame, pandas.Series]]
            Словарь с выборками, для которых требуется рассчитать статистику.
            Ключ словаря - название выборки (train / valid / ...), значение -
            кортеж с матрицей признаков (data) и вектором ответов (target).

        """
        ws = self.sheets["Compare Models"]
        cols = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        sheet_format = self.wb.add_format({"left": True, "right": True})
        train_sheets = [sheet for sheet in self.sheets if "train" in sheet]

        for sheet_number, sheet_name in enumerate(train_sheets):
            url = f"internal:'{sheet_name}'!A1"
            string = f"Ссылка на лист {sheet_name}"

            # last column in sheet
            cell_name = xl_col_to_name(len(ws.table[0]) - 1)

            ws.write_url(f"{cell_name}{sheet_number + 2}", url, sheet_format, string)

        sheet_format = self.wb.add_format({"left": True, "right": True, "bottom": True})
        ws.write_url(f"{cell_name}{sheet_number + 2}", url, sheet_format, string)

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
        if self.corr is not None:
            self.create_second_page(**eval_sets)

        if isinstance(self.psi, pd.DataFrame):
            self.create_psi_report(**eval_sets)

        self.create_third_page(**eval_sets)
        if self.other_models:
            self.create_other_model_page(**eval_sets)
        self.create_four_page(**eval_sets)
        self.create_model_report(**eval_sets)
        self.writer.save()