from typing import Type, List, Optional

from dreamml.configs.config_storage import ConfigStorage
from dreamml.features.feature_selection._gini_importance import compare_gini_features
from dreamml.pipeline.fitter import FitterBase
from dreamml.stages.algo_info import AlgoInfo
from dreamml.stages.stage import BaseStage
from dreamml.data._dataset import DataSet
from dreamml.stages.feature_based_stage import FeatureBasedStage
from dreamml.modeling.models.estimators import BoostingBaseModel


class GiniSelectionStage(FeatureBasedStage):
    """
    Стейдж отбора фич на основе GiniImportance
    """

    name = "gini"

    def __init__(
        self,
        algo_info: AlgoInfo,
        config: ConfigStorage,
        fitter: Optional[FitterBase] = None,
        vectorization_name: str = None,
    ):
        super().__init__(
            algo_info=algo_info,
            config=config,
            fitter=fitter,
            vectorization_name=vectorization_name,
        )
        self.gini_threshold = config.gini_threshold
        self.categorical_features = []
        self.remaining_features = config.remaining_features
        self.valid_sample = config.gini_selector_valid_sample
        self.gini_absolute_diff = config.gini_selector_abs_difference
        self.gini_relative_diff = config.gini_selector_rel_difference

    def _set_params(self, params: dict):
        raise NotImplementedError

    def _fit(
        self,
        model: BoostingBaseModel,
        used_features: List[str],
        data_storage: DataSet,
        models: List[BoostingBaseModel] = None,
    ) -> BaseStage:
        eval_sets = data_storage.get_eval_set(
            used_features, vectorization_name=self.vectorization_name
        )
        self.final_model = model
        self.categorical_features = data_storage.cat_features
        conf = {
            "gini_threshold": 30,
            "categorical_features": self.categorical_features,
            "valid_sample": self.valid_sample,
            "gini_absolute_diff": self.gini_absolute_diff,
            "gini_relative_diff": self.gini_relative_diff,
            "remaining_features": self.remaining_features,
        }
        feature_importance, u_features = compare_gini_features(eval_sets, conf)
        final_features = list(sorted(u_features))
        self.feature_importance = feature_importance
        self.used_features = final_features
        return self