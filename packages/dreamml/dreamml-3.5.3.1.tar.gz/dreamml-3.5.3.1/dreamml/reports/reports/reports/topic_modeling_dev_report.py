from typing import Optional, Dict

import pandas as pd
from tqdm.auto import tqdm

from dreamml.reports.reports._base import BaseReport

from .._topic_modeling_metrics import CalculateTopicModelingMetrics
from ..data_statistics.calculate_data_statistics_topic_modeling import (
    CalculateDataStatistics as TopicModeling_DS,
)
from ..detailed_metrics.calculate_detailed_metrics_topic_modeling import (
    CalculateDetailedMetricsTopicModeling,
)
from dreamml.pipeline.cv_score import CVScores
from dreamml.utils.saver import ArtifactSaver
from dreamml.logging import get_logger

_logger = get_logger(__name__)

CV_SCORE_COL = "cv score"
MODEL_NAME_COL = "Название модели"

drop_params = [
    "never_used_features",
    "categorical_features",
    "feature_threshold",
    "validation",
    "split_by_time_period",
    "shuffle",
    "stratify",
    "split_params",
    "oot_split_test",
    "oot_split_valid",
    "split_oot_from_dev",
    "oot_split_n_values",
    "time_series_split",
    "time_series_window_split",
    "time_series_split_test_size",
    "time_series_split_gap",
    "cv_n_folds",
    "sample_strategy",
    "boostaroota_type",
    "use_sampling",
    "gini_threshold",
    "gini_selector_abs_difference",
    "gini_selector_rel_difference",
    "gini_selector_valid_sample",
    "permutation_threshold",
    "permutation_top_n",
    "psi_threshold",
    "psi_sample",
    "min_n_features_to_stop",
    "min_n_features_to_start",
    "max_boostaroota_stage_iters",
    "bootstrap_samples",
    "stop_criteria",
    "sample_for_validation",
    "weights_column",
    "weights",
    "min_percentile",
    "max_percentile",
    "show_save_paths",
    "samples_to_plot",
    "plot_multi_graphs",
    "max_classes_plot",
    "path_to_exog_data",
    "known_future",
    "time_column_frequency",
    "use_whitebox_automl",
    "use_oot_potential",
    "use_lama",
    "use_etna",
    "corr_threshold",
    "corr_coef",
    "n_estimators",
    "verbose",
    "lama_time",
    "save_to_ps",
    "multitarget",
    "ignore_third_party_warnings",
    "metric_col_name",
    "group_column",
    "time_column",
    "time_column_format",
    "time_column_period",
    "split_by_group",
    "custom_cv",
    "unfreeze_layers",
    "sampler_type",
    "optimizer_type",
    "scheduler_type",
    "learning_rate",
    "epochs",
    "batch_size",
    "weight_decay",
    "text_augmentations",
    "aug_p",
    "log_target",
    "target_with_nan_values",
    "ts_transforms",
    "horizon",
    "whitebox_automl_hyper_params",
    "whitebox_automl_bounds_params",
    "prophet_hyper_params",
    "prophet_bounds_params",
]


class TopicModelingDevReport(BaseReport):
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
        self.models_metrics_df = None
        self.cv_scores = cv_scores

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

        for key in drop_params:
            config_for_report.pop(key, None)

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

    def create_first_page(self, **eval_sets):
        sheet_name = "Data_Statistics"
        features = eval_sets["train"][0].columns.to_series()
        transformer = TopicModeling_DS(
            self.encoder, features, self.config, task=self.task
        )
        result = transformer.transform(**eval_sets)

        startows = [0, 3, 6]
        num_formats = [None, None, None]

        for data, startrow, num_format in zip(result, startows, num_formats):
            data.to_excel(
                self.writer,
                startrow=startrow,
                sheet_name=sheet_name,
                index=False,
            )
            self.set_style(data, "Data_Statistics", startrow, num_format=num_format)

    def create_third_page(self, metric_name, metric_col_name, **eval_sets):
        transformer = CalculateTopicModelingMetrics(
            self.models,
            bootstrap_samples=self.bootstrap_samples,
            p_value=self.p_value,
            config=self.config,
            metric_name=metric_name,
            metric_col_name=metric_col_name,
            task=self.task,
            vectorizers=self.vectorizers_dict,
        )
        transformer.predictions_ = self.predictions
        result = transformer.transform(**eval_sets)

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

    def create_model_report(self, **eval_sets):
        metric_params = self.config.get("metric_params")
        metric_name = self.config.get("eval_metric")

        for model_name in tqdm(self.models):
            sheet_name = f"{model_name}"[:30]

            umap_params = {
                "n_neighbors": self.config.get("n_neighbors") or 15,
                "min_dist": self.config.get("min_dist") or 0.1,
                "metric": self.config.get("metric_umap") or "euclidean",
                "n_epochs": self.config.get("umap_epochs"),
            }

            transformer = CalculateDetailedMetricsTopicModeling(
                self.models,
                self.experiment_path,
                self.vectorizers_dict,
                self.config["text_features"][0],
                metric_name,
                metric_params,
                umap_params=umap_params,
            )

            data = transformer.transform(model_name)

            data.to_excel(
                self.writer,
                startrow=32,
                sheet_name=sheet_name,
                index=False,
            )

            sheets = self.writer.sheets
            ws = sheets[sheet_name]
            sheet_format = self.wb.add_format(
                {
                    "bold": True,
                    "text_wrap": True,
                    "fg_color": "77d496",
                    "border": 1,
                    "align": "center",
                    "valign": "vcenter",
                }
            )
            ws.merge_range("A30:D30", "Топ-10 слов по каждому кластеру.", sheet_format)
            try:
                ws.insert_image(
                    "A1", f"{self.experiment_path}/images/umap_{model_name}.png"
                )
            except Exception as e:
                pass

    def transform(self, **eval_sets):
        self.create_dml_info_page()
        self.create_zero_page()
        self.create_first_page(**eval_sets)

        self.create_third_page(
            self.config.get("eval_metric"),
            self.config.get("metric_col_name"),
            **eval_sets,
        )

        # self.create_traffic_light_page(
        #     self.config.get("eval_metric"),
        #     self.config.get("metric_col_name"),
        #     **eval_sets,
        # )

        # if self.other_models:
        #     self.create_other_model_page(
        #         self.config.get("eval_metric"),
        #         self.config.get("metric_col_name"),
        #         **eval_sets,
        #     )

        # self.create_fourth_page(**eval_sets)
        # self.create_fifth_page(**eval_sets)
        self.create_model_report(**eval_sets)
        self.writer.save()