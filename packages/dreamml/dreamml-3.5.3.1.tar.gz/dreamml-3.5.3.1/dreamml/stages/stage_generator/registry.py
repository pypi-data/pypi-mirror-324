from dreamml.modeling.models.estimators import *
from dreamml.stages.lama_stage import LAMAStage
from dreamml.stages.correlation_stage import (
    CorrelationFeatureSelectionStage,
    DecisionTreeFeatureImportanceStage,
)
from dreamml.stages.gini_selection_stage import GiniSelectionStage
from dreamml.stages.model_based_stage import BaseModelStage
from dreamml.stages.permutation_importance_stage import PermutationImportanceStage
from dreamml.stages.boostaroota_stage import BoostARootaStage
from dreamml.stages.optimization_stage import OptimizationStage
from dreamml.stages.batch_selection_with_params import BatchSelectionModelStage10
from dreamml.stages.batch_selection_with_params import BatchSelectionModelStage5
from dreamml.stages.batch_selection_reverse_with_params import (
    BatchSelectionReverseModelStage10,
)
from dreamml.stages.batch_selection_reverse_with_params import (
    BatchSelectionReverseModelStage5,
)
from dreamml.stages.batch_selection_reverse_with_params import (
    BatchSelectionReverseModelStage1,
)
from dreamml.stages.fix_stage import FixStage
from dreamml.stages.vectorization_stage import VectorizationStage

LIGHTGBM = "lightgbm"
XGBOOST = "xgboost"
CATBOOST = "catboost"
PYBOOST = "pyboost"
LAMA_ = "lama"
PROPHET = "prophet"
LINEARREG = "linear_reg"
LOGREG = "log_reg"
VECTORIZATION = "vectorization"
LDA = "lda"
ENSEMBELDA = "ensembelda"
BERTOPIC = "bertopic"
BERT = "bert"


estimators_registry = {
    LIGHTGBM: LightGBMModel,
    XGBOOST: XGBoostModel,
    CATBOOST: CatBoostModel,
    PYBOOST: PyBoostModel,
    LAMA_: LAMA,
    PROPHET: AMTSModel,
    LINEARREG: LinearRegModel,
    LOGREG: LogRegModel,
    LDA: LDAModel,
    ENSEMBELDA: EnsembeldaModel,
    BERTOPIC: BERTopicModel,
    BERT: BertModel,
}

stages_registry = {
    "gini": GiniSelectionStage,
    "permutation": PermutationImportanceStage,
    "base": BaseModelStage,
    "boostaroota": BoostARootaStage,
    "opt": OptimizationStage,
    "batch10": BatchSelectionModelStage10,
    "batch5": BatchSelectionModelStage5,
    "corr": CorrelationFeatureSelectionStage,
    "dtree": DecisionTreeFeatureImportanceStage,
    "LAMA": LAMAStage,
    "batch10_down": BatchSelectionReverseModelStage10,
    "batch5_down": BatchSelectionReverseModelStage5,
    "batch1_down": BatchSelectionReverseModelStage1,
    # "psi": PSISelectionStage,
    "fix": FixStage,
    "vectorization": VectorizationStage,
}