from typing import List

from dreamml.configs.config_storage import ConfigStorage
from dreamml.stages.algo_info import AlgoInfo
from dreamml.data._dataset import DataSet
from dreamml.pipeline.fitter import FitterBase
from dreamml.stages.model_based_stage import ModelBasedStage
from dreamml.modeling.models.estimators import BoostingBaseModel
from dreamml.stages.stage import BaseStage


class FixStage(ModelBasedStage):
    """
    Простой этап обучения модели на заданных фичах
    """

    name = "fix"

    def __init__(
        self,
        algo_info: AlgoInfo,
        config: ConfigStorage,
        fitter: FitterBase = None,
        vectorization_name: str = None,
    ):
        super().__init__(
            algo_info=algo_info,
            config=config,
            fitter=fitter,
            vectorization_name=vectorization_name,
        )

    def _set_used_features(self, data_storage: DataSet, used_features: List = None):
        if not used_features:
            data = data_storage.get_eval_set(vectorization_name=self.vectorization_name)
            used_features = data["train"][0].columns.tolist()

        used_features = self._drop_text_features(data_storage, used_features)
        return used_features

    def _fit(
        self,
        model: BoostingBaseModel,
        used_features: List[str],
        data_storage: DataSet,
        models: List[BoostingBaseModel] = None,
    ) -> BaseStage:
        self.used_features = self._set_used_features(
            data_storage=data_storage, used_features=used_features
        )
        self.start_model = self._init_model(
            used_features=self.used_features, fix_stage=True
        )
        self.final_model, self.models, _ = self.fitter.train(
            estimator=self.start_model,
            data_storage=data_storage,
            metric=self.eval_metric,
            vectorization_name=self.vectorization_name,
        )
        self.final_model.used_features = self.used_features
        self.prediction = self.prediction_out(data_storage)
        return self

    def _set_params(self):
        raise NotImplementedError