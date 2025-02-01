"""
Обертка для фреймворка ETNA
"""

from etna.datasets import TSDataset

from dreamml.configs.config_storage import ConfigStorage
from dreamml.data._dataset import DataSet
from dreamml.modeling.models.estimators._etna_model import EtnaPipeline
from dreamml.features.feature_enrichment.timeseries_enrichment import (
    get_time_column_frequency,
)
from dreamml.logging import get_logger

_logger = get_logger(__name__)


class ETNA:
    def __init__(
        self,
        config_storage: ConfigStorage,
        data_storage: DataSet,
    ):
        self.data_storage = data_storage
        self.drop_features = config_storage.drop_features
        self.etna_transforms = data_storage.etna_artifacts["etna_transforms"]
        self.dev_ts: TSDataset = data_storage.etna_artifacts["dev_ts"]
        self.horizon = config_storage.horizon
        self.frequency = get_time_column_frequency(config_storage.time_column_period)
        self.known_future = config_storage.known_future
        self.eval_set = data_storage.get_clean_eval_set()
        self.use_etna = config_storage.use_etna

    def _prepare_eval_set(self):
        sample_dates = {}
        for sample_name, sample in self.eval_set.items():
            sample_dates[sample_name] = (
                sample[0]["timestamp"].min(),
                sample[0]["timestamp"].max(),
            )

        train_ts, test_ts, oot_ts = self._train_test_oot_split(
            self.dev_ts, sample_dates
        )
        return train_ts, test_ts, oot_ts

    def _train_test_oot_split(self, dev_ts: TSDataset, sample_dates: dict):
        train_ts, test_ts = dev_ts.train_test_split(
            train_start=sample_dates["train"][0],
            train_end=sample_dates["valid"][1],
            test_start=sample_dates["test"][0],
            test_end=sample_dates["test"][1],
        )
        oot_ts = None
        if "OOT" in sample_dates:
            _, oot_ts = dev_ts.train_test_split(
                train_start=sample_dates["train"][0],
                train_end=sample_dates["valid"][1],
                test_start=sample_dates["OOT"][0],
                test_end=sample_dates["OOT"][1],
            )
        return train_ts, test_ts, oot_ts

    def add_etna_model(self, model_type: str = "multi_segment"):
        train_ts, test_ts, oot_ts = self._prepare_eval_set()

        etna_pipeline = EtnaPipeline(
            dev_ts=self.dev_ts,
            horizon=self.horizon,
            transforms=self.etna_transforms,
            frequency=self.frequency,
            model_type=model_type,
            train_ts=train_ts,
            test_ts=test_ts,
            oot_ts=oot_ts,
            use_etna=self.use_etna,
        )

        if self.use_etna:
            etna_pipeline.fit(train_ts)

        self.data_storage.etna_pipeline = etna_pipeline
        return etna_pipeline