import os
import pickle
from pathlib import Path
from typing import List, Union

import pandas as pd
import yaml
from sklearn.preprocessing import LabelBinarizer
import numpy as np
from tqdm.auto import tqdm

from dreamml.configs.config_storage import ConfigStorage
from dreamml.features.feature_enrichment.timeseries_enrichment import (
    split_dml_transforms,
)
from dreamml.utils.get_last_experiment_directory import get_experiment_dir_path
from dreamml.logging import get_logger

from etna.core import load

_logger = get_logger(__name__)


class LogTargetTransformer:
    def __init__(self):
        self.fitted = None


class BaseArtifactsConfig:
    def __init__(self, config: dict):
        self.config = config
        self.model_name = self.config["model_name"]
        self.experiment_dir_path = self._get_experiment_dir_path()
        self.vectorizer_name = self.config.get("vectorizer_name")
        self.vectorizer = (
            self._get_vectorizer() if self.vectorizer_name is not None else None
        )
        self.estimator = self._get_model()
        self.data = self._get_data()
        self.experiment_config = self._get_config()
        self.encoder = self._get_encoder()
        self.target_name = self.experiment_config["target_name"]
        self.time_column = self.config.get("time_column")
        self.time_format = self.config.get("time_format")
        self.task = self.experiment_config["task"]
        self.subtask = self.experiment_config.get(
            "subtask", "tabular"
        )  # [tabular, nlp]

    def prepare_artifacts_config(self):
        artifacts_config = {
            "estimator": self.estimator,
            "vectorizer": self.vectorizer,
            "used_features": self.estimator.used_features,
            "categorical_features": self.estimator.categorical_features or [],
        }

        if not isinstance(artifacts_config["categorical_features"], list):
            artifacts_config["categorical_features"] = [
                artifacts_config["categorical_features"]
            ]

        artifacts_config["subtask"] = self.subtask
        text_column: Union[List[str], str] = self.config.get("text_column")
        text_preprocessed_column: Union[List[str], str] = self.config.get(
            "text_preprocessed_column"
        )

        if isinstance(text_column, str):
            text_column = [text_column]
        if isinstance(text_preprocessed_column, str):
            text_preprocessed_column = [text_preprocessed_column]

        artifacts_config["text_column"] = text_column
        artifacts_config["text_preprocessed_column"] = text_preprocessed_column

        artifacts_config["group_column"] = self.config.get("group_column")
        artifacts_config["time_column"] = self.time_column

        artifacts_config["path_to_save"] = os.path.join(
            self.experiment_dir_path, "docs", f"val_report_{self.model_name}.xlsx"
        )
        artifacts_config["create_pdf"] = self.config.get("create_pdf", False)

        artifacts_config["images_dir_path"] = os.path.join(
            self.experiment_dir_path, "images"
        )
        artifacts_config["task"] = self.experiment_config["task"]
        artifacts_config["custom_model"] = False
        artifacts_config["user_config"] = self.config
        artifacts_config["number_of_simulations_1_1"] = self.config.get(
            "number_of_simulations_1_1", 200
        )
        artifacts_config["number_of_simulations_3_2"] = self.config.get(
            "number_of_simulations_3_2", 100
        )

        eval_set = self.get_eval_set()

        if self.subtask == "nlp":
            eval_set, text_preprocessed_column = self._check_preprocessed_columns_nlp(
                eval_set, text_column, text_preprocessed_column
            )
            if len(text_column):
                artifacts_config["text_column"] = text_column[0]
                artifacts_config["text_preprocessed_column"] = text_preprocessed_column[
                    0
                ]

        return artifacts_config, eval_set

    def _check_preprocessed_columns_nlp(
        self, eval_set, text_column: List[str], text_preprocessed_column: List[str]
    ):
        for sample_name, (X_sample, y_sample) in eval_set.items():
            for text_feature_name in text_column:
                preproc_feature_name = f"{text_feature_name}_preprocessed"
                if (
                    preproc_feature_name not in text_preprocessed_column
                    or preproc_feature_name not in X_sample.columns
                ):
                    X_sample[preproc_feature_name] = X_sample[text_column]
                    text_preprocessed_column.append(preproc_feature_name)
        return eval_set, text_preprocessed_column

    def _get_experiment_dir_path(self):
        experiment_dir_path = get_experiment_dir_path(
            self.config["results_path"],
            experiment_dir_name=self.config.get("dir_name"),
            use_last_experiment_directory=self.config.get(
                "use_last_experiment_directory", False
            ),
        )
        return experiment_dir_path

    def _get_model(self):
        self.model_name = (
            self.model_name[:-4]
            if self.model_name.endswith(".pkl")
            else self.model_name
        )
        with open(
            os.path.join(self.experiment_dir_path, "models", f"{self.model_name}.pkl"),
            "rb",
        ) as f:
            estimator = pickle.load(f)
        return estimator

    def _get_vectorizer(self):
        self.vectorizer_name = (
            self.vectorizer_name[:-4]
            if self.vectorizer_name.endswith(".pkl")
            else self.vectorizer_name
        )
        if self.vectorizer_name == "bert_vectorizer":
            return None
        with open(
            os.path.join(
                self.experiment_dir_path, "models", f"{self.vectorizer_name}.pkl"
            ),
            "rb",
        ) as f:
            vectorizer = pickle.load(f)
        return vectorizer

    def _get_data(self):
        with open(
            os.path.join(self.experiment_dir_path, "data", f"eval_sets.pkl"), "rb"
        ) as f:
            data = pickle.load(f)

        for key, (X, y) in data.items():
            if self.vectorizer is not None:
                if self.vectorizer_name == "bert_vectorizer":
                    embedding_df = self.vectorizer.transform(X, return_embedds=True)
                else:
                    embedding_df = self.vectorizer.transform(X)

                X = pd.concat([X, embedding_df], axis=1)
                data[key] = (X, y)
            else:
                data[key] = (X, y)
        return data

    def _get_log_target_transformer(self):
        if self.task not in ["regression", "timeseries"]:
            return None

        try:
            with open(
                os.path.join(
                    self.experiment_dir_path, "models", f"log_target_transformer.pkl"
                ),
                "rb",
            ) as f:
                log_target_transformer = pickle.load(f)
            return log_target_transformer

        except FileNotFoundError:
            return LogTargetTransformer()

    def _get_config(self):
        try:
            with open(
                os.path.join(self.experiment_dir_path, "config", f"config.yaml"), "r"
            ) as f:
                experiment_config = yaml.unsafe_load(f)
        except FileNotFoundError as e:
            experiment_config = {}
            _logger.exception(e)
        return experiment_config

    def _get_encoder(self, default: bool = False):
        if default:
            encoder_path = f"{self.experiment_dir_path}/models/encoder.pkl"
        else:
            encoder_path = self.config.get("encoder")

        if encoder_path is None:
            return None

        if not encoder_path.endswith(".pkl"):
            encoder_path += ".pkl"

        with open(encoder_path, "rb") as f:
            encoder = pickle.load(f)

        return encoder

    def _transform_data(self, x, y):
        if self.encoder is not None:
            # By default we shouldn't use any encoder here because eval_sets were saved with already encoded data
            # this function remained just in case of future use
            x = self.encoder.transform(x)

        return x, y

    def get_eval_set(self):
        eval_set = {}
        for sample_name, (x, y) in self.data.items():
            x, y = self._transform_data(x, y)

            if self.time_column is not None:
                try:
                    x[self.time_column] = pd.to_datetime(
                        x[self.time_column], format=self.time_format
                    )
                except Exception as e:
                    _logger.debug(f"Error while processing time_column: {e}")

                try:
                    # Excel не может работать с локализованным форматом
                    x[self.time_column] = x[self.time_column].dt.tz_localize(None)
                except AttributeError:
                    _logger.warning(
                        f"Формат времени колонки {self.time_column} не определен: value at idx=0: {x[self.time_column].iloc[0]}"
                    )

            eval_set[sample_name] = (x, y)
        return eval_set


class RegressionArtifactsConfig(BaseArtifactsConfig):
    def __init__(self, config: dict):
        super().__init__(config)
        self.log_target_transformer = self._get_log_target_transformer()

    def _transform_data(self, x, y):
        x, y = super()._transform_data(x, y)

        if self.log_target_transformer.fitted:
            y = self.log_target_transformer.inverse_transform(y)

        return x, y

    def prepare_artifacts_config(self):
        artifacts_config, eval_set = super().prepare_artifacts_config()
        artifacts_config["log_target_transformer"] = self.log_target_transformer

        try:
            metric_name = self.config["metric"]["metric"]
        except (KeyError, ValueError):
            metric_name = None

        if metric_name is None:
            metric_name = "rmse"

        artifacts_config["metric_name"] = metric_name

        return artifacts_config, eval_set


class StatisticalArtifactsConfig(BaseArtifactsConfig):
    def __init__(self, config: dict):
        super().__init__(config)

    def prepare_artifacts_config(self):
        artifacts_config, eval_set = super().prepare_artifacts_config()

        try:
            metric_name = self.config["metric"]["metric"]
        except (KeyError, ValueError):
            metric_name = None

        if metric_name is None:
            metric_name = "rmse"

        artifacts_config["metric_name"] = metric_name

        return artifacts_config, eval_set


class ClassificationArtifactsConfig(BaseArtifactsConfig):
    def __init__(self, config: dict):
        super().__init__(config)

    def prepare_artifacts_config(self):
        artifacts_config, eval_set = super().prepare_artifacts_config()

        metric_name, metric_col_name, self.experiment_params = self._get_metric_params()
        artifacts_config["metric_name"] = metric_name
        artifacts_config["metric_col_name"] = metric_col_name
        artifacts_config["metric_params"] = self.experiment_params

        if self.task == "binary":
            if "labels" not in artifacts_config["metric_params"]:
                artifacts_config["metric_params"]["labels"] = [0, 1]

        if self.task == "multiclass":
            artifacts_config["multiclass_artifacts"] = {}

            if "labels" not in artifacts_config["metric_params"]:
                msg = "Отсутствуют labels для multiclass."
                raise ValueError(msg)

            labels = artifacts_config["metric_params"]["labels"]
            arange_labels = np.arange(len(labels))
            artifacts_config["multiclass_artifacts"][
                "label_binarizer"
            ] = LabelBinarizer().fit(arange_labels)
            artifacts_config["multiclass_artifacts"]["labels"] = labels
            artifacts_config["multiclass_artifacts"]["task"] = self.task
            artifacts_config["multiclass_artifacts"]["target_name"] = self.target_name

        if self.task == "timeseries":
            artifacts_config["config_storage"] = self._get_config_storage()
            artifacts_config["encoder"] = self._get_encoder(default=True)

        return artifacts_config, eval_set

    def _get_metric_params(self):
        metric_name = self.config.get(
            "eval_metric", self.experiment_config["eval_metric"]
        )
        params = {
            "at_k": self.config.get("at_k"),
            "thr": self.config.get("thr"),
            "beta": self.config.get("beta"),
        }
        experiment_params = self.experiment_config.get("metric_params", {})
        for key in params:
            if params[key] is not None:
                experiment_params[key] = params[key]

        metric_col_name = metric_name[:15]
        return metric_name, metric_col_name, experiment_params

    def get_timeseries_artifacts(self):
        _, dml_transforms = split_dml_transforms(
            self.experiment_config["ts_transforms"]
        )
        try:
            path_to_etna_pipeline = Path(
                self.experiment_dir_path, "etna_pipeline", "etna_pipeline.zip"
            )
            etna_pipeline = load(path_to_etna_pipeline)
        except FileNotFoundError:
            etna_pipeline = None

        try:
            etna_eval_sets = pickle.load(
                open(f"{self.experiment_dir_path}/data/etna_eval_sets.pkl", "rb")
            )
        except FileNotFoundError:
            etna_eval_sets = None
        return dml_transforms, etna_pipeline, etna_eval_sets

    def _get_config_storage(self):
        return ConfigStorage(self.experiment_config)