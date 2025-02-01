from typing import List, Optional
import numpy as np
from sklearn.exceptions import NotFittedError
from xgboost.core import XGBoostError

from dreamml.configs.config_storage import ConfigStorage
from dreamml.data._dataset import DataSet
from dreamml.logging import get_logger
from dreamml.modeling.models.estimators import BoostingBaseModel
from dreamml.pipeline.fitter import FitterBase
from dreamml.stages.feature_based_stage import FeatureBasedStage
from dreamml.stages.algo_info import AlgoInfo
from dreamml.stages.stage import BaseStage, StageStatus

_logger = get_logger(__name__)


class BoostARootaStage(FeatureBasedStage):
    """
    Этап для отбора признаков по алгоритму BoostARoota.
    """

    name = "boostaroota"

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
        self.config_storage = config
        self.predictions = None

    @property
    def check_is_fitted(self):
        if not self.is_fitted:
            msg = (
                "This estimator is not fitted yet. Call 'fit' with "
                "appropriate arguments before using this estimator."
            )
            raise NotFittedError(msg)
        return True

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
        """
        Основная функция для запуска этапа.

        Parameters
        ----------
        model: dreamml.modeling.models.estimators.boosting_base.BoostingBaseModel
            Экземпляр модели для обучения.

        models: List[estimator]
            Список с моделями полученными на CV (здесь для совместимости)

        data_storage: DataSet
            Экземпляр класса-хранилища данных

        used_features: List
            Список используемых признаков.

        Returns
        -------
        self
        """
        logger = self._logger or _logger

        if self._status != StageStatus.FITTED:
            np.random.seed(self.config_storage.random_seed)
            self.used_features = self._set_used_features(
                data_storage=data_storage, used_features=used_features
            )
            min_n_features_to_stop = (
                self.config_storage.min_n_features_to_stop
            )  # default - 60
            min_n_features_to_start = (
                self.config_storage.min_n_features_to_start
            )  # default - 100
            max_boostaroota_stage_iters = (
                self.config_storage.max_boostaroota_stage_iters
            )  # default - 3
            data = data_storage.get_eval_set(
                self.used_features, vectorization_name=self.vectorization_name
            )
            if (
                self.config_storage.use_sampling
                and data_storage.get_dev_n_samples() >= 250000
            ):
                data["train"] = data_storage.sample(
                    self.used_features, vectorization_name=self.vectorization_name
                )
            br, br_params, _ = self.config_storage.get_model_by_str("boostaroota")
            if self.config_storage.boostaroota_type != "default":
                br_params["clf"] = "LGBM"
                br_params["shap_flag"] = True

            if type(min_n_features_to_start) == str:
                pass
            elif len(self.used_features) <= min_n_features_to_start:
                logger.info(
                    f"\nКоличество признаков менее требуемого для отбора, Отбор признаков не проводился.\n"
                    f"Признаков для построения моделей: {len(self.used_features)}; "
                    f"Отбор если более: {min_n_features_to_start}\n"
                )
            else:
                i = 0
                selected_features = []
                while i < max_boostaroota_stage_iters:
                    br_model = br(**br_params, logger=self._logger)
                    try:
                        br_model.fit(x=data["train"][0], y=data["train"][1])
                        selected_features = br_model.keep_vars_.values.tolist()
                        if len(selected_features) >= min_n_features_to_stop:
                            break
                    except XGBoostError as e:
                        logger.info(
                            f"{e}\n"
                            f"Parameter 'cutoff' increased to {br_params['cutoff'] * 2}"
                        )
                    br_params["cutoff"] *= 2
                    i += 1

                if len(selected_features) >= min_n_features_to_stop:
                    self.used_features = selected_features

                logger.info(
                    f"\nАлгоритм BoostaRoota отобрал {len(self.used_features)} признаков\n"
                    f"С параметрами:\n"
                    f"\tcutoff: {br_params['cutoff']}\n"
                    f"\titers: {br_params['iters']}\n"
                    f"\tmax_rounds: {br_params['max_rounds']}\n"
                    f"\tdelta: {br_params['delta']}\n"
                )

            self.final_model = model
            self.is_fitted = True

        return self

    def transform(self):
        self.check_is_fitted
        # estimator, used_features, feature_importance, predictions, cv_estimators
        return (
            self.final_model,
            self.used_features,
            self.feature_importance,
            self.predictions,
            self.models,
        )

    def _set_params(self, params: dict):
        raise NotImplementedError