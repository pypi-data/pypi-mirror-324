from typing import List, Union, Optional

from dreamml.configs.config_storage import ConfigStorage
from dreamml.data._dataset import DataSet
from dreamml.modeling.models.estimators import BaseModel
from dreamml.modeling.models.estimators._lightautoml import LAMA
from dreamml.stages.algo_info import AlgoInfo
from dreamml.stages.model_based_stage import ModelBasedStage
from dreamml.stages.stage import BaseStage
from dreamml.pipeline.fitter import FitterBase


class LAMAStage(ModelBasedStage):
    name = "LAMA"

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
        self.lama_time = config.lama_time
        self.loss_function = config.loss_function
        self.eval_metric = config.eval_metric
        self.lama_conf = {
            "lama_time": self.lama_time,
            "loss_function": self.loss_function,
            "eval_metric": self.eval_metric,
        }

    def _set_used_features(self, data_storage: DataSet, used_features: List = None):
        if not used_features:
            data = data_storage.get_eval_set(vectorization_name=self.vectorization_name)
            used_features = data["train"][0].columns.tolist()

        used_features = self._drop_text_features(data_storage, used_features)
        return used_features

    def _fit(
        self,
        model: BaseModel,
        used_features: List[str],
        data_storage: DataSet,
        models: List[BaseModel] = None,
    ) -> BaseStage:
        self.used_features = self._set_used_features(
            data_storage=data_storage, used_features=used_features
        )
        self.start_model = LAMA(self.lama_conf)
        data = data_storage.get_eval_set(vectorization_name=self.vectorization_name)
        train = data["train"][0][self.used_features], data["train"][1]
        valid = data["valid"][0][self.used_features], data["valid"][1]
        self.start_model.fit(*train, *valid)
        self.final_model = self.start_model
        self.prediction = self.prediction_out(data_storage)

        return self