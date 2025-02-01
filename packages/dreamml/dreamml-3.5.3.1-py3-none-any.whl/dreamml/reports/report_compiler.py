import time
import uuid
from pathlib import Path
import pandas as pd

from dreamml.data._dataset import DataSet
from dreamml.logging import get_logger
from dreamml.logging.monitoring import ReportStartedLogData, ReportFinishedLogData
from dreamml.pipeline.pipeline import MainPipeline
from dreamml.reports.reports import (
    RegressionDevelopmentReport,
    AMTSDevelopmentReport,
    TopicModelingDevReport,
    ClassificationDevelopmentReport,
)
from dreamml.configs.config_storage import ConfigStorage
from dreamml.features.categorical.categorical_encoder import (
    CategoricalFeaturesTransformer,
)
from dreamml.features.feature_extraction._transformers import LogTargetTransformer


_logger = get_logger(__name__)


def get_report(
    pipeline: MainPipeline,
    data_storage: DataSet,
    config_storage: ConfigStorage,
    encoder: CategoricalFeaturesTransformer,
    etna_eval_set=None,
    etna_pipeline=None,
    analysis=None,
) -> None:
    """
    Функция для сохранения совместимости между пайплайном обучения версии 2.0 и старыми отчётами.

    Parameters
    ----------
    pipeline: MainPipeline
        Объект пайплайна обучения

    data_storage: DataSet
        Объект для хранения данных
    config_storage: ConfigStorage
        Объект для хранения параметров эксперимента
    encoder: CategoricalFeaturesTransformer
        Обработчик категориальных фич
    etna_eval_set: Optional[Dict[TSDataset]]
        Объект для хранения данных для timeseries
    etna_pipeline: EtnaPipeline
        Pipeline для timeseries
    """
    prepared_model_dict = {**pipeline.prepared_model_dict, "encoder": encoder}
    other_models_dict = {
        k: v["estimator"] for k, v in pipeline.other_model_dict.items()
    }
    oot_potential = pipeline.oot_potential
    config_for_report = {
        k: v
        for k, v in config_storage.get_all_params().items()
        if not isinstance(v, dict)
    }
    config_for_report["metric_params"] = config_storage.metric_params
    config_for_report["metric_col_name"] = config_for_report["eval_metric"][:15]
    config_for_report["task"] = config_storage.task
    config_for_report["subtask"] = config_storage.subtask
    config_for_report["target_with_nan_values"] = config_storage.target_with_nan_values
    config_for_report["show_save_paths"] = config_storage.show_save_paths
    config_for_report["samples_to_plot"] = config_storage.samples_to_plot
    config_for_report["max_classes_plot"] = config_storage.max_classes_plot
    config_for_report["plot_multi_graphs"] = config_storage.plot_multi_graphs
    config_for_report["group_column"] = config_storage.group_column
    config_for_report["split_by_group"] = config_storage.split_by_group
    config_for_report["use_etna"] = config_storage.use_etna

    # nlp
    total_vectorizers_dict = pipeline.total_vectorizers_dict
    config_for_report["text_features"] = data_storage.text_features
    config_for_report["text_features_preprocessed"] = (
        data_storage.text_features_preprocessed
    )

    dev_report_dict = {
        "binary": ClassificationDevelopmentReport,
        "multiclass": ClassificationDevelopmentReport,
        "multilabel": ClassificationDevelopmentReport,
        "regression": RegressionDevelopmentReport,
        "timeseries": RegressionDevelopmentReport,
        "amts": AMTSDevelopmentReport,
        "topic_modeling": TopicModelingDevReport,
    }

    report_params_dict = {
        "models": prepared_model_dict,
        "other_models": other_models_dict,
        "oot_potential": oot_potential,
        "experiment_path": pipeline.experiment_path,
        "config": config_for_report,
        "artifact_saver": pipeline.artifact_saver,
        "n_bins": 20,
        "bootstrap_samples": 200,
        "p_value": 0.05,
        "max_feat_per_model": 50,
        "predictions": None,
        "cv_scores": pipeline.prepared_cv_scores,
        "etna_pipeline": etna_pipeline,
        "etna_eval_set": etna_eval_set,
        "analysis": analysis,
        "vectorizers_dict": total_vectorizers_dict,
    }

    if config_storage.task in ("regression", "timeseries"):
        prepare_for_regression(pipeline, prepared_model_dict)

    report = dev_report_dict[config_storage.task](**report_params_dict)

    report_id = uuid.uuid4().hex
    start_time = time.time()
    _logger.monitor(
        f"Processing development report for {config_storage.task} task.",
        extra={
            "log_data": ReportStartedLogData(
                task=config_storage.task,
                development=True,
                custom_model=False,
                experiment_name=Path(pipeline.experiment_path).name,
                report_id=report_id,
                user_config=config_storage.user_config,
            )
        },
    )
    eval_sets = data_storage.get_eval_set()
    report.transform(**eval_sets)
    elapsed_time = time.time() - start_time
    _logger.monitor(
        f"Development report for {config_storage.task} task is created in {elapsed_time:.1f} seconds.",
        extra={
            "log_data": ReportFinishedLogData(
                report_id=report_id,
                elapsed_time=elapsed_time,
            )
        },
    )


def prepare_for_regression(pipeline, prepared_model_dict) -> None:
    """
    Функция подготовки словаря с моделями для запуска отчёта о разработке

    Parameters
    ----------
    pipeline
    prepared_model_dict
    log_target_transformer
    """
    corr_importance = pipeline.total_feature_importance_dict.get("0_dtree", None)
    if corr_importance is not None:
        if isinstance(corr_importance, pd.DataFrame):
            prepared_model_dict["corr_importance"] = corr_importance

    prepared_model_dict["log_target_transformer"] = LogTargetTransformer()