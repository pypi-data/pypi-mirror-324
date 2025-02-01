from copy import deepcopy
from pathlib import Path
from typing import Sequence, Dict, Optional, Type

from dreamml.data._dataset import DataSet
from dreamml.logging import get_logger
from dreamml.modeling.cv import BaseCrossValidator
from dreamml.stages.algo_info import AlgoInfo
from dreamml.stages.stage_generator.registry import stages_registry, estimators_registry
from dreamml.configs.config_storage import ConfigStorage
from dreamml.pipeline.fitter.utils import get_fitter

_logger = get_logger(__name__)


class StageGenerator:
    """
    Класс генератора пайпланов.
    Берёт на себя функцию заполнения стейджей пользовательскими конфигурациями
    Должен выстраивать последовательность действий для каждой модели.
    Чтобы взять стейдж, ему нужно знать, какие стейджи существуют.
    Он будет брать из какого-то реестра стейджей, которые уже заполнены стандартными параметрами.
    А после этого заполнять их пользовательскими конфигурациями
    """

    def __init__(
        self,
        config: ConfigStorage,
        experiment_path: str,
        custom_cv: Optional[Type[BaseCrossValidator]] = None,
    ):
        self.config = config
        self.experiment_path = experiment_path
        self.custom_cv = custom_cv

    def _get_stage_list(self, data_storage: DataSet) -> Sequence:
        """
        Метод, который создаёт список объектов стейджей.
        -------
        Returns
        stages: Iterable
            Список стейджей для запуска в пайплайне
        """
        stages = []
        stage_idx = 0

        vectorization_algos = self.config.vectorization_algos
        fitted_model = self.config.fitted_model
        stage_list = self.config.stage_list

        if len(vectorization_algos) == 0:
            vectorization_algos = [None]

        current_vectorization_name = None
        for vectorization_name in vectorization_algos:
            for algo in fitted_model:
                stage_list_cp = stage_list.copy()

                if (
                    "vectorization" in stage_list_cp
                    and vectorization_name == current_vectorization_name
                ):
                    stage_list_cp.remove("vectorization")
                else:
                    current_vectorization_name = vectorization_name

                for stg in stage_list_cp:
                    algo = "bert" if vectorization_name == "bert" else algo
                    if self.check_conflict(algo, stg):
                        continue
                    estimator_class = estimators_registry.get(algo)
                    algo_info = AlgoInfo(
                        estimator_class,
                        deepcopy(getattr(self.config, f"{algo}_hyper_params")),
                        [],
                        [],
                        (self.config.text_augmentations, self.config.aug_p),
                        deepcopy(getattr(self.config, f"{algo}_bounds_params")),
                        deepcopy(getattr(self.config, f"{algo}_fixed_params")),
                    )
                    fitter = get_fitter(
                        self.config,
                        data_size=len(data_storage),
                        custom_cv=self.custom_cv,
                        vectorization_name=vectorization_name,
                    )
                    algo_info.cat_features.extend(data_storage.cat_features)

                    if (
                        algo in ["bert"]
                        and len(data_storage.text_features_preprocessed) != 0
                    ):
                        algo_info.text_features.extend(
                            data_storage.text_features_preprocessed
                        )
                    else:
                        algo_info.text_features.extend(data_storage.text_features)

                    _logger.debug(
                        f"algo: {algo} | text_features: {algo_info.text_features}"
                    )

                    stage = stages_registry.get(stg)(
                        algo_info=algo_info,
                        config=self.config,
                        fitter=fitter,
                        vectorization_name=vectorization_name,
                    )
                    stage.experiment_path = self.experiment_path

                    stage_identifier = f"{stage_idx}_{stage.name}"
                    stage.id = stage_identifier

                    log_path = (
                        Path(f"{self.experiment_path}")
                        / "logs"
                        / f"{stage_identifier}.log"
                    )
                    stage.init_logger(log_file=log_path)

                    stages.append(stage)
                    stage_idx += 1

        _logger.debug(
            f"Created stages list:\n"
            + "\n".join(
                [
                    f"{idx+1} {stage.name} {stage.algo_info.algo_class.model_name}"
                    for idx, stage in enumerate(stages)
                ]
            )
        )

        return stages

    def get_pipeline_params(self, data_storage: DataSet) -> Dict:
        stage_list = self._get_stage_list(data_storage)

        pipeline_params = dict()
        for i, stage in enumerate(stage_list):
            pipeline_params[stage.id] = {
                "stage": stage,
                "stage_idx": i,
            }

        return pipeline_params

    def check_conflict(self, algo, stage):
        """
        Cheking for a conflict between algos and stages

        input
            algo - name of ML algo
            stage - name of stage for ML algo

        return
            True - if there is a conflict
            False - if not a conflict
        """
        if algo == "linear_reg" and stage in (
            "dtree",
            "corr",
            "permutation",
            "opt",
            "batch5",
            "batch5_down",
            "batch10",
            "batch10_down",
        ):
            return True
        elif algo == "log_reg" and stage in (
            "batch5",
            "batch5_down",
            "batch10",
            "batch10_down",
        ):
            return True
        elif algo == "bert" and stage not in ("vectorization", "opt"):
            return True
        elif self.config.task == "multilabel" and stage in (
            "batch5",
            "batch5_down",
            "batch10",
            "batch10_down",
        ):
            if self.config.target_with_nan_values:
                return True  # Используется обертка OneVsRestWrapper, которая не имеет TreeExplainer
            elif not self.config.target_with_nan_values and algo == "lightgbm":
                return True  # Только для lightgbm используется обертка OneVsRestWrapper, которая не имеет TreeExplainer
            else:
                return False
        else:
            return False