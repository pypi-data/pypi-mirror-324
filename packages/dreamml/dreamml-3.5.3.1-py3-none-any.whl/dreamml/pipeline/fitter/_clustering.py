import pandas as pd
from typing import List, Dict, Optional
from dreamml.data._dataset import DataSet

from dreamml.pipeline.fitter import FitterBase
from dreamml.utils import ValidationType


class FitterClustering(FitterBase):

    def __init__(self):
        self.validation_type = ValidationType.HOLDOUT

    @staticmethod
    def _fit_final_model(
        estimator,
        data: Dict,
    ):
        estimator.fit(data["train"])
        estimator.evaluate_and_print(**data)
        return estimator

    def train(
        self,
        estimator,
        data_storage: DataSet,
        metric: callable,
        used_features: List = None,
        sampling_flag: bool = None,
        vectorization_name: Optional[str] = None,
    ):
        data: Dict = data_storage.get_eval_set(vectorization_name=vectorization_name)
        estimator = self._fit_final_model(estimator, data)
        estimators = [estimator]
        return estimator, estimators, None

    def get_validation_target(self, data_storage: DataSet):
        raise NotImplementedError

    def calculate_importance(
        self,
        estimators,
        data_storage: DataSet,
        used_features: List = None,
        splitter_df: pd.DataFrame = None,
        fraction_sample: float = 1,
        vectorization_name: Optional[str] = None,
    ) -> pd.DataFrame:
        raise NotImplementedError