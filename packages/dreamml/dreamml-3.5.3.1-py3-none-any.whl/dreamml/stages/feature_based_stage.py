from abc import ABC
from typing import Optional

from dreamml.data._dataset import DataSet
from dreamml.modeling.models.estimators import BaseModel
from dreamml.configs.config_storage import ConfigStorage
from dreamml.pipeline.fitter import FitterBase
from dreamml.stages.algo_info import AlgoInfo
from dreamml.stages.stage import BaseStage, StageStatus


class SharedStateMixin:
    _shared_state = {}

    @classmethod
    def _set_shared_state(cls, state):
        cls._shared_state[cls] = state

    @classmethod
    def _get_shared_state(cls, default=None):
        return cls._shared_state.get(cls, default)


class FeatureBasedStage(BaseStage, SharedStateMixin, ABC):
    """
    Абстрактный класс для этапов, которым для выполнения фабричного метода не нужна обученная модель.
    Не обучают модель, хранят одно состояние на все инстансы класса.
    """

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
        self.prediction = None

    def fit(
        self,
        model: BaseModel,
        used_features: Optional[list],
        data_storage: DataSet,
        models=None,
    ):
        shared_state = self._get_shared_state(default={})

        if shared_state.get("status") == StageStatus.FITTED:
            self._status = shared_state["status"]
            self.final_model = shared_state["final_model"]
            self.used_features = shared_state["used_features"]
            self.feature_importance = shared_state["feature_importance"]
            self.prediction = shared_state["prediction"]
            self.models = shared_state["models"]

            return self
        else:

            super().fit(
                model=model,
                used_features=used_features,
                data_storage=data_storage,
                models=models,
            )

            new_state = {
                "status": self._status,
                "final_model": self.final_model,
                "used_features": self.used_features,
                "feature_importance": self.feature_importance,
                "prediction": self.prediction,
                "models": self.models,
            }

            self._set_shared_state(new_state)

            return self