from typing import Optional

from dreamml.pipeline.fitter import FitterBase
from dreamml.stages.batch_selection_reverse import BatchSelectionReverseModelStage
from dreamml.configs.config_storage import ConfigStorage
from dreamml.stages.algo_info import AlgoInfo


class BatchSelectionReverseModelStage10(BatchSelectionReverseModelStage):
    """
    Этап пакетного TOP@ отборп признаков и построение моделей.
    """

    name = "batch10_down"

    def __init__(
        self,
        algo_info: AlgoInfo,
        config: ConfigStorage,
        fitter: Optional[FitterBase] = None,
        vectorization_name: str = None,
        stage_params: str = "step_10_down",
    ):
        super().__init__(
            algo_info=algo_info,
            config=config,
            fitter=fitter,
            vectorization_name=vectorization_name,
            stage_params=stage_params,
        )


class BatchSelectionReverseModelStage5(BatchSelectionReverseModelStage):
    """
    Этап пакетного TOP@ отборп признаков и построение моделей.
    """

    name = "batch5_down"

    def __init__(
        self,
        algo_info: AlgoInfo,
        config: ConfigStorage,
        fitter: Optional[FitterBase] = None,
        vectorization_name: str = None,
        stage_params: str = "step_5_down",
    ):
        super().__init__(
            algo_info=algo_info,
            config=config,
            fitter=fitter,
            vectorization_name=vectorization_name,
            stage_params=stage_params,
        )


class BatchSelectionReverseModelStage1(BatchSelectionReverseModelStage):
    """
    Этап пакетного TOP@ отборп признаков и построение моделей.
    """

    name = "batch1_down"

    def __init__(
        self,
        algo_info: AlgoInfo,
        config: ConfigStorage,
        experiment_path: str,
        fitter: Optional[FitterBase] = None,
        vectorization_name: str = None,
        stage_params: str = "step_1_down",
    ):
        super().__init__(
            algo_info=algo_info,
            config=config,
            fitter=fitter,
            vectorization_name=vectorization_name,
            stage_params=stage_params,
        )