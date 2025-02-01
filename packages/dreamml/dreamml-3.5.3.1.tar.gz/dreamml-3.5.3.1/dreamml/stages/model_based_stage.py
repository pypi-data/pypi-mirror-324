from __future__ import annotations

from abc import ABC
from typing import List

from dreamml.configs.config_storage import ConfigStorage
from dreamml.stages.algo_info import AlgoInfo
from dreamml.modeling.metrics.metrics_mapping import metrics_mapping
from dreamml.stages.stage import BaseStage

from dreamml.modeling.models.estimators import BaseModel
from dreamml.data._dataset import DataSet
from dreamml.pipeline.fitter import FitterBase


class ModelBasedStage(BaseStage, ABC):
    """
    Абстрактный класс для этапов, которым для выполнения фабричного метода необходима обученная модель.
    Им нужен один из fitter-ов, который обучает модель либо на HO, либо на CV

    """

    def __init__(
        self,
        algo_info: AlgoInfo,
        config: ConfigStorage,
        fitter: FitterBase,
        vectorization_name: str = None,
    ):
        super().__init__(
            algo_info=algo_info,
            config=config,
            fitter=fitter,
            vectorization_name=vectorization_name,
        )
        self.eval_metric = metrics_mapping.get(config.eval_metric)(
            task=config.task, **config.metric_params
        )
        self.metric_params = config.metric_params


class BaseModelStage(ModelBasedStage):
    """
    Простой этап обучения модели на заданных фичах
    """

    name = "base"

    def __init__(
        self,
        algo_info: AlgoInfo,
        config: ConfigStorage,
        fitter: FitterBase,
        vectorization_name,
    ):
        super().__init__(
            algo_info=algo_info,
            config=config,
            fitter=fitter,
            vectorization_name=vectorization_name,
        )
        self.config = config

    def _set_used_features(self, data_storage: DataSet, used_features: List = None):
        used_features = None
        if not used_features:
            data = data_storage.get_eval_set(vectorization_name=self.vectorization_name)

            if self.vectorization_name == "bow":
                used_features = list(data["train"][0].keys())
            else:
                used_features = data["train"][0].columns.tolist()
        # FIXME 2601
        if self.vectorization_name != "bow":
            used_features = self._drop_text_features(data_storage, used_features)

        if "bertopic" in self.config.fitted_model:
            used_features = data["train"][0].columns.tolist()

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
        self.start_model = self._init_model(used_features=self.used_features)
        self.final_model, self.models, _ = self.fitter.train(
            estimator=self.start_model,
            data_storage=data_storage,
            metric=self.eval_metric,
            used_features=self.used_features,
            vectorization_name=self.vectorization_name,
        )
        self.final_model.used_features = self.used_features
        self.prediction = self.prediction_out(data_storage)
        return self

    def _set_params(self):
        raise NotImplementedError