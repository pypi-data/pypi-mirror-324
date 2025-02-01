from typing import Optional

from dreamml.pipeline.fitter import FitterBase
from dreamml.stages.batch_selection_model_stage import BatchSelectionModelStage
from dreamml.configs.config_storage import ConfigStorage
from dreamml.stages.algo_info import AlgoInfo


class BatchSelectionModelStage10(BatchSelectionModelStage):
    """
    Этап пакетного TOP@ отборп признаков и построение моделей.
    """

    name = "batch10"

    def __init__(
        self,
        algo_info: AlgoInfo,
        config: ConfigStorage,
        fitter: Optional[FitterBase] = None,
        stage_params: str = "step_10",
        vectorization_name: str = None,
    ):
        super().__init__(
            algo_info=algo_info,
            config=config,
            fitter=fitter,
            vectorization_name=vectorization_name,
            stage_params=stage_params,
        )


class BatchSelectionModelStage5(BatchSelectionModelStage):
    """
    Этап пакетного TOP@ отборп признаков и построение моделей.
    """

    name = "batch5"

    def __init__(
        self,
        algo_info: AlgoInfo,
        config: ConfigStorage,
        fitter: Optional[FitterBase] = None,
        stage_params: str = "step_5",
        vectorization_name: str = None,
    ):
        super().__init__(
            algo_info=algo_info,
            config=config,
            fitter=fitter,
            vectorization_name=vectorization_name,
            stage_params=stage_params,
        )