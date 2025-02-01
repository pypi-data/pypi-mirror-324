import pickle
import os
from typing import Dict

from dreamml.logging import get_logger
from dreamml.stages.stage import BaseStage

_logger = get_logger(__name__)


class CheckPoint:
    def __init__(self, experiment_path: str):
        self.experiment_path = experiment_path
        self.checkpoint_path = os.path.join(experiment_path, "cpts")

    def save_stage(self, stage_name: str, stage: BaseStage, pipeline_params: Dict):
        stage_path = os.path.join(self.checkpoint_path, f"{stage_name}.stage")

        if hasattr(stage, "vectorizer") and stage.vectorizer is not None:
            if (
                hasattr(stage.vectorizer, "model_path")
                and stage.vectorizer.model_path is not None
            ):
                stage.vectorizer.vectorizer = None  # Удаляем модель для экономии места
                log_msg = f"Из векторизатора {stage.vectorizer.name} удалена загруженная модель для экономии места."
                _logger.debug(log_msg)

        with open(stage_path, "wb") as file:
            pickle.dump(stage, file)

        pipeline_params_path = os.path.join(self.checkpoint_path, f"pipeline_params")
        with open(pipeline_params_path, "wb") as file:
            pickle.dump(pipeline_params, file)

    def load_stage(self, stage_name: str):
        stage_path = os.path.join(self.checkpoint_path, f"{stage_name}.stage")
        with open(stage_path, "rb") as file:
            stage = pickle.load(file)
        _logger.info(f"{stage_name} successfully loaded from {stage_path}")

        return stage

    def load_pipeline_params(self):
        pipeline_params_path = os.path.join(self.checkpoint_path, "pipeline_params")
        with open(pipeline_params_path, "rb") as file:
            pipeline_params = pickle.load(file)

        return pipeline_params