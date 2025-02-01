from typing import Tuple, Any
from copy import deepcopy
import pandas as pd

from etna.pipeline import Pipeline
from etna.datasets import TSDataset

from dreamml.utils.prepare_artifacts_config import RegressionArtifactsConfig
from dreamml.configs.config_storage import ConfigStorage
from dreamml.features.feature_enrichment.timeseries_enrichment import (
    get_time_column_frequency,
)
from dreamml.logging import get_logger
from dreamml.modeling.models.estimators.boosting_base import BoostingBaseModel
from dreamml.features.categorical.categorical_encoder import (
    CategoricalFeaturesTransformer,
)


_logger = get_logger(__name__)


def prepare_artifacts_config_timeseries(config: dict) -> Tuple[Any, Any]:
    """
    Подготовка конфигурационного файла для передачи в
    объект валидационного отчета ValidationReport.

    Parameters
    ----------
    config: dict
        Конфигурационный файл config с указанием
        названия финальной модели и директории с
        артефактами вычислительного эксперимента.

    Returns
    -------
    artifacts_config: dict`
        Конфигурационный файл для отчета.

    """

    prepare_artifacts = RegressionArtifactsConfig(config=config)
    artifacts_config, data = prepare_artifacts.prepare_artifacts_config()
    return artifacts_config, data


class TimeSeriesPrediction:
    def __init__(self, artifacts_config, dml_transforms, etna_pipeline, etna_eval_sets):
        self.artifacts_config = artifacts_config
        self.dml_transforms: dict = dml_transforms
        self.etna_pipeline: Pipeline = etna_pipeline
        self.etna_transforms = self.etna_pipeline.transforms
        self.etna_eval_sets: dict = etna_eval_sets

        self.model: BoostingBaseModel = artifacts_config["estimator"]
        self.used_features: list = self.model.used_features
        self.config_storage: ConfigStorage = artifacts_config["config_storage"]
        self.transformer: CategoricalFeaturesTransformer = artifacts_config["encoder"]

        self.horizon = self.config_storage.horizon
        self.frequency = get_time_column_frequency(
            self.config_storage.time_column_period
        )
        self.use_etna = self.config_storage.use_etna
        self.dml_predictions = None
        self.etna_predictions = None

    def get_forecast(self):
        if (
            "oot_ts" in self.etna_eval_sets
            and self.etna_eval_sets["oot_ts"] is not None
        ):
            data: TSDataset = self.etna_eval_sets["oot_ts"]
        else:
            data: TSDataset = self.etna_eval_sets["test_ts"]

        if self.use_etna is True:
            predictions = self.etna_pipeline.forecast(data)
        else:
            predictions = data.make_future(
                future_steps=self.horizon, transforms=self.etna_transforms
            )
        return predictions.to_pandas(True)

    def _dml_feature_transform(self, data: pd.DataFrame):
        """Метод для обогащения фичами трансформаций DML."""
        if len(self.dml_transforms) > 0:
            for transform in self.dml_transforms:
                _, data = transform.transform(data)
        return data

    def transform(self):
        data = self.get_forecast()
        if self.use_etna:
            self.etna_predictions = deepcopy(data[["target", "timestamp", "segment"]])
        self.dml_predictions = self._get_dml_predict(data)

    def _get_dml_predict(self, data: pd.DataFrame):
        predictions = self._dml_feature_transform(data)
        predictions = self.transformer.transform(predictions)
        predictions["target"] = self.model.transform(predictions[self.used_features])
        predictions = predictions[["target", "timestamp", "segment"]]
        predictions = self.transformer.inverse_transform(predictions)
        predictions = TSDataset.to_dataset(predictions)
        predictions = TSDataset(df=predictions, freq=self.frequency)
        predictions.inverse_transform(transforms=self.etna_transforms)
        predictions = predictions.to_pandas(True)
        return predictions