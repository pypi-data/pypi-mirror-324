import numpy as np
import pandas as pd
from typing import Optional, Dict

from dreamml.reports.reports._base import BaseReport
from ..data_statistics.calculate_data_statistics_amts import CalculateDataStatisticsAMTS
from .._amts_metrics import CalculateAMTSMetrics

from dreamml.visualization.plots import (
    plot_STL,
)

from dreamml.utils.saver import ArtifactSaver

# FIXME AMTS
drop_params = [
    "drop_features",
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
]


class AMTSDevelopmentReport(BaseReport):
    def __init__(
        self,
        models,
        other_models,
        oot_potential,
        experiment_path,
        config,
        analysis,
        artifact_saver: Optional[ArtifactSaver] = None,
        n_bins: Optional[dict] = None,
        bootstrap_samples: Optional[dict] = None,
        p_value: Optional[dict] = None,
        max_feat_per_model: Optional[dict] = None,
        predictions: Optional[dict] = None,
        cv_scores: Optional[dict] = None,
        etna_pipeline: Optional[dict] = None,
        etna_eval_set: Optional[dict] = None,
        vectorizers_dict: Optional[dict] = None,
    ):
        super().__init__(
            experiment_path,
            artifact_saver=artifact_saver,
            config=config,
            models=models,
            other_models=other_models,
            oot_potential=oot_potential,
        )
        self.split_by_group = self.config["split_by_group"]
        self.group_column = self.config["group_column"]
        self.analysis = analysis

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
        transformer = CalculateDataStatisticsAMTS(self.encoder, self.config)
        result = transformer.transform(**eval_sets)

        df_kpss_test = pd.DataFrame(self.analysis.analysis_result.kpss_test_dict)
        df_adfuller_test = pd.DataFrame(
            self.analysis.analysis_result.adfuller_test_dict
        )
        df_levene_test = pd.DataFrame(self.analysis.analysis_result.levene_dict)
        df_period = pd.DataFrame(self.analysis.analysis_result.period_dict)

        result = result + (
            df_kpss_test,
            df_adfuller_test,
            df_levene_test,
            df_period,
        )

        startows = [
            0,
            2 + result[0].shape[0],
            4 + result[0].shape[0] + result[1].shape[0],
            6 + np.sum(res.shape[0] for res in result[:3]),
            8 + np.sum(res.shape[0] for res in result[:4]),
            10 + np.sum(res.shape[0] for res in result[:5]),
            12 + np.sum(res.shape[0] for res in result[:6]),
            14 + np.sum(res.shape[0] for res in result[:7]),
        ]
        num_formats = [10, 10, None, None, None, None, None, None]

        for data, startrow, num_format in zip(result, startows, num_formats):
            data.to_excel(
                self.writer,
                startrow=startrow,
                sheet_name="Data_Statistics",
                index=False,
            )
            self.set_style(data, "Data_Statistics", startrow, num_format=None)

        self.add_numeric_format(result[0], "Data_Statistics", startrow=startows[0])

        for i, (segment_name, segment_params) in enumerate(
            self.analysis.analysis_result.stl_dict.items()
        ):
            plot_STL(
                segment_name=segment_name,
                stl_dict=segment_params,
                name=f"{self.experiment_path}/images/stl_{segment_name}",
            )
            ws = self.sheets["Data_Statistics"]
            ws.insert_image(
                f"A{len(data) + ((i+1) * 37)}",
                f"{self.experiment_path}/images/stl_{segment_name}.png",
            )

    # Compare Models
    def create_third_page(self, **eval_sets):
        transformer = CalculateAMTSMetrics(
            self.models, self.group_column, self.split_by_group
        )
        result = transformer.transform(**eval_sets)
        self.predictions = transformer.predictions_

        result = result.round(3)
        result.to_excel(self.writer, sheet_name="Compare Models", index=False)
        self.set_style(result, "Compare Models", 0)

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
        # self.create_second_page(**eval_sets)
        #
        # if isinstance(self.psi, pd.DataFrame):
        #     self.create_psi_report(**eval_sets)
        #
        self.create_third_page(**eval_sets)
        # if self.other_models:
        #     self.create_other_model_page(**eval_sets)
        # self.create_four_page(**eval_sets)
        # self.create_model_report(**eval_sets)
        self.writer.save()