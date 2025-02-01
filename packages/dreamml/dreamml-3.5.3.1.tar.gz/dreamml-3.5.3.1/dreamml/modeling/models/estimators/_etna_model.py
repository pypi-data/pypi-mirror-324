"""
Обертка для ETNA
"""

import time
from typing import Union

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from etna.datasets import TSDataset
from etna.models import CatBoostPerSegmentModel
from etna.models import CatBoostMultiSegmentModel
from etna.pipeline import Pipeline
from etna.analysis import plot_forecast

from dreamml.logging import get_logger

_logger = get_logger(__name__)


class EtnaPipeline:

    def __init__(
        self,
        dev_ts: TSDataset,
        train_ts: TSDataset,
        test_ts: TSDataset,
        oot_ts: TSDataset,
        horizon,
        transforms,
        frequency,
        model_type="multi_segment",
        use_etna: bool = False,
    ):
        self.model_name = "ETNA"
        self.dev_ts = dev_ts
        self.train_ts = train_ts
        self.test_ts = test_ts
        self.oot_ts = oot_ts
        self.horizon = horizon
        self.transforms = transforms
        self.frequency = frequency
        self.model_type = model_type
        self.pipeline = self._get_pipeline()
        self.frequency = frequency
        self.use_etna = use_etna
        self.fitted = False

    def _get_estimator(
        self, model_type: str
    ) -> Union[CatBoostPerSegmentModel, CatBoostMultiSegmentModel]:
        if model_type == "per_segment":
            return CatBoostPerSegmentModel()
        elif model_type == "multi_segment":
            return CatBoostMultiSegmentModel()

    def _get_pipeline(self):
        model = self._get_estimator(self.model_type)
        pipeline = Pipeline(
            model=model, transforms=self.transforms, horizon=self.horizon
        )
        return pipeline

    def fit(self, train_ts: TSDataset) -> None:
        _logger.info(f"{time.ctime()}, start fitting ETNA")
        self.pipeline.fit(train_ts)
        self.fitted = True

    def transform(
        self, data: Union[TSDataset, pd.DataFrame], return_dataset: bool = False
    ) -> np.array:
        if isinstance(data, pd.DataFrame):
            try:
                data, _ = self.dev_ts.train_test_split(
                    train_start=data["timestamp"].min(),
                    train_end=data["timestamp"].max(),
                )
            except:
                _, data = self.dev_ts.train_test_split(
                    train_start=data["timestamp"].min(),
                    train_end=data["timestamp"].max(),
                )
        prediction = self.pipeline.predict(ts=data, return_components=False)
        pred_df = prediction.to_pandas(True)
        return pred_df if return_dataset else pred_df["target"]

    def forecast(
        self,
        data: Union[TSDataset, pd.DataFrame],
        return_dataset: bool = False,
    ) -> np.array:
        if isinstance(data, pd.DataFrame):
            try:
                data, _ = self.dev_ts.train_test_split(
                    train_start=data["timestamp"].min(),
                    train_end=data["timestamp"].max(),
                )
            except:
                _, data = self.dev_ts.train_test_split(
                    test_start=data["timestamp"].min(), test_end=data["timestamp"].max()
                )
        forecast = self.pipeline.forecast(ts=data, return_components=False)
        forecast_df = forecast.to_pandas(True)
        return forecast_df if return_dataset else forecast_df["target"]

    def plot_forecast(self, train_ts: TSDataset, test_ts: TSDataset):
        if self.use_etna:
            train_data = self.train_ts.to_pandas(True).copy()
            if train_data["segment"].nunique() < 10:
                plot_forecast(
                    self.pipeline.forecast(train_ts),
                    test_ts,
                    train_ts,
                    n_train_samples=20,
                )
            else:
                _logger.info("Selected random 10 segments to plot.")
                segments = np.random.choice(
                    train_data["segment"].unique(), size=10, replace=False
                )
                plot_forecast(
                    self.pipeline.forecast(train_ts),
                    test_ts,
                    train_ts,
                    n_train_samples=20,
                    segments=segments,
                )
            plt.show()

    def get_etna_eval_set(self):
        eval_set = {
            "dev_ts": self.dev_ts,
            "train_ts": self.train_ts,
            "test_ts": self.test_ts,
            "oot_ts": self.oot_ts,
        }
        return eval_set