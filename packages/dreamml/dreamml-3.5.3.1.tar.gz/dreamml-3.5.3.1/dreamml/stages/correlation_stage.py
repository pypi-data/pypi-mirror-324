from typing import List, Optional

from dreamml.configs.config_storage import ConfigStorage
from dreamml.data._dataset import DataSet
from dreamml.features.feature_extraction import DecisionTreeFeatureImportance
from dreamml.features.feature_selection._correlation_feature_selection import (
    CorrelationFeatureSelection,
)
from dreamml.modeling.models.estimators import BoostingBaseModel
from dreamml.pipeline.fitter import FitterBase
from dreamml.stages.algo_info import AlgoInfo
from dreamml.stages.stage import BaseStage
from dreamml.stages.feature_based_stage import FeatureBasedStage


class DecisionTreeFeatureImportanceStage(FeatureBasedStage):
    name = "dtree"

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
        self.threshold = config.corr_threshold
        self.remaining_features = config.remaining_features

    def _fit(
        self,
        model: BoostingBaseModel,
        used_features: List[str],
        data_storage: DataSet,
        models: List[BoostingBaseModel] = None,
    ) -> BaseStage:
        corr_transformer = DecisionTreeFeatureImportance(
            self.threshold, self.remaining_features
        )
        eval_sets = data_storage.get_eval_set(used_features)
        self.feature_importance = corr_transformer.fit_transform(*eval_sets["train"])
        self.used_features = sorted(corr_transformer.used_features)
        self.final_model = model
        return self


class CorrelationFeatureSelectionStage(FeatureBasedStage):
    name = "corr"

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
        self.coef = config.corr_coef
        self.remaining_features = config.remaining_features

    def _fit(
        self,
        model: BoostingBaseModel,
        used_features: List[str],
        data_storage: DataSet,
        models: List[BoostingBaseModel] = None,
    ) -> BaseStage:
        corr_coef_selection = CorrelationFeatureSelection(
            self.coef, used_features, self.remaining_features
        )
        eval_sets = data_storage.get_eval_set(used_features)
        corr_coef_selection.fit(*eval_sets["train"])
        self.used_features = sorted(corr_coef_selection.used_features)
        self.final_model = model
        return self