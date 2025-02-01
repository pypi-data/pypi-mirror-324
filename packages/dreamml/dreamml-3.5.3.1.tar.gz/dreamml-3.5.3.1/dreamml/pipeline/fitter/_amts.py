import pandas as pd
from typing import List, Dict, Optional
from dreamml.data._dataset import DataSet
from dreamml.pipeline.fitter import FitterBase

from dreamml.logging import get_logger

_logger = get_logger(__name__)


class FitterAMTS(FitterBase):
    def __init__(self):
        pass

    @staticmethod
    def _fit_final_model(
        estimator,
        amts_data: Dict,
    ):
        estimator.fit(amts_data, final=True)
        return estimator

    @staticmethod
    def _fit(estimator, amts_data: Dict):
        estimator.fit(amts_data)
        estimator.evaluate_and_print(**amts_data)

    def train(
        self,
        estimator,
        data_storage: DataSet,
        metric: callable,
        used_features: List = None,
        sampling_flag: bool = None,
        vectorization_name: Optional[str] = None,
    ):
        amts_train_data = data_storage.get_amts_data()
        amts_final_data = data_storage.get_amts_final_data()

        _logger.info(
            f"Initial training of the '{estimator.model_name}' model has been launched"
        )
        self._fit(estimator, amts_train_data)

        _logger.info(
            f"The final training of the '{estimator.model_name}' model has been launched"
        )
        estimator = self._fit_final_model(estimator, amts_final_data)

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