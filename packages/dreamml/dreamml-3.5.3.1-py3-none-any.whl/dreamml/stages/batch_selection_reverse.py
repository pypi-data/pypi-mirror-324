from typing import List, Dict
import numpy as np
import pandas as pd
from tqdm.auto import tqdm
from sklearn.exceptions import NotFittedError
from operator import ge, le

from dreamml.configs.config_storage import ConfigStorage
from dreamml.data._dataset import DataSet
from dreamml.logging.logger import CombinedLogger
from dreamml.logging import get_logger
from dreamml.modeling.models.estimators import BoostingBaseModel
from dreamml.pipeline.fitter import FitterBase
from dreamml.stages.stage import BaseStage
from dreamml.utils.confidence_interval import create_bootstrap_scores
from dreamml.utils.confidence_interval import calculate_conf_interval
from dreamml.features.feature_selection.select_subset_features import (
    select_subset_features_reverse,
)
from dreamml.stages.model_based_stage import ModelBasedStage
from dreamml.stages.algo_info import AlgoInfo
from dreamml.utils import ValidationType
from dreamml.features.feature_selection._shap_importance import ShapFeatureSelection


_logger = get_logger(__name__)


class BatchSelectionReverseModelStage(ModelBasedStage):
    """
    Этап пакетного TOP@ отборп признаков и построение моделей.
    """

    name = "batch_r"

    def __init__(
        self,
        algo_info: AlgoInfo,
        config: ConfigStorage,
        fitter: FitterBase,
        vectorization_name: str = None,
        stage_params: str = "step_10",
    ):
        super().__init__(
            algo_info=algo_info,
            config=config,
            fitter=fitter,
            vectorization_name=vectorization_name,
        )
        # General params
        self.config_storage = config
        self.predictions = None
        self.stage_all_models_dict = None
        self.stage_params = self.config_storage.get_batch_selection_model_params()[
            stage_params
        ]
        self.all_cv_mean_scores = {}
        self.maximize = self.eval_metric.maximize
        self.metric_comp = ge if self.maximize else le
        self.choose_best_model = max if self.maximize else min
        self.remaining_features = config.remaining_features

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
            data = data_storage.get_eval_set(
                used_features, vectorization_name=self.vectorization_name
            )
            used_features = data["train"][0].columns.tolist()

        used_features = self._drop_text_features(data_storage, used_features)
        return used_features

    def _stop_criteria(
        self, y_pred: pd.Series, y_true: pd.Series, criteria: str = None
    ) -> float:
        """
        Расчет порога для остановки построения моделей.

        Parameters
        ----------
        y_pred: pd.Series
            Вектор предсказаний модели.

        y_true: pd.Series
            Вектор истинных значений.

        criteria: str
            'model_score' - Остановиться при построении модели лучшего качества чем базовая.
            'model_ci' - Остановиться при попадании в дов интервал метрики качества базовой модели

        Returns
        -------
        result: float
            Порог для остановки построения моделей.

        """
        if criteria == "model_score":
            self.eval_metric(y_true, y_pred)
        elif criteria == "model_ci":
            bootstrap_samples = self.config_storage.bootstrap_samples
            random_seed = self.config_storage.random_seed
            scores = create_bootstrap_scores(
                y_true,
                y_true,
                y_pred,
                self.eval_metric,
                bootstrap_samples,
                random_seed,
                task=self.task,
            )
            ci = calculate_conf_interval(scores)
            return ci[0]
        else:
            return np.inf

    def _batch_feature_selection(
        self, model, data_storage, used_features, features_step: int = 10
    ):
        """
        Функция для построения и выбора лучшей модели.

        Parameters
        ----------
        model: dreamml.modeling.models.estimators.boosting_base.BoostingBaseModel
            Экземпляр модели для обучения.

        data_storage: DataSet
            Экземпляр класса-хранилища данных

        used_features: List
            Список используемых признаков.

        features_step: int
            Шаг по количеству признаков для построения моделей


        Returns
        -------
        recommend_final_model: dreamml.modeling.models.estimators.boosting_base.BoostingBaseModel
            Рекомендованная модель.

        models_dict: Dict
            Словарь со всеми построенными моделями (содержит estimator и предсказания)
        """
        models_dict = {}
        sample_for_validation = (
            self.config_storage.sample_for_validation
        )  # valid, test, oot; valid на cv -> OOF
        data = data_storage.get_eval_set(
            used_features, vectorization_name=self.vectorization_name
        )

        model_ = self._init_model(used_features=used_features, hyperparams=model.params)
        model_, _, y_pred = self.fitter.train(
            estimator=model_,
            data_storage=data_storage,
            metric=self.eval_metric,
            used_features=used_features,
            vectorization_name=self.vectorization_name,
        )
        shap = ShapFeatureSelection(
            model_,
            self.config_storage.eval_metric,
            metric_params=self.metric_params,
            task=self.task,
        )

        feature_importance = shap._calculate_feature_importance(
            data_storage.get_train(
                used_features, vectorization_name=self.vectorization_name
            )[0]
        )
        n_features = np.arange(
            feature_importance.shape[0],
            self.stage_params["min_features"],
            -self.stage_params["features_step"],
        )

        # Определение выборки для подсчета метрики, останова и выбора лучшей модели
        if sample_for_validation == "test":
            y_true = data["test"][1]
        elif sample_for_validation == "oot":
            y_true = data["OOT"][1]
        else:  # "valid"
            y_true = self.fitter.get_validation_target(
                data_storage, vectorization_name=self.vectorization_name
            )

        # Процесс построения моделей с отбором по TOP@ признаков
        for _ in tqdm(n_features):
            selected_features = select_subset_features_reverse(
                feature_importance,
                self.remaining_features,
                bot_k=self.stage_params["features_step"],
            )
            if len(selected_features) == 0:
                break
            model_for_step = self._init_model(
                used_features=selected_features, hyperparams=model_.params
            )
            model_candidate, _, pred = self.fitter.train(
                estimator=model_for_step,
                data_storage=data_storage,
                metric=self.eval_metric,
                used_features=selected_features,
                vectorization_name=self.vectorization_name,
            )

            shap = ShapFeatureSelection(
                model_candidate,
                self.config_storage.eval_metric,
                metric_params=self.metric_params,
                task=self.task,
            )

            feature_importance = shap._calculate_feature_importance(
                data_storage.get_train(
                    selected_features, vectorization_name=self.vectorization_name
                )[0]
            )
            model_name = f"{model_candidate.model_name}.{len(selected_features)}_reverse.S{features_step}"
            self.add_cv_score(model_name)

            if sample_for_validation == "test":
                pred = model_candidate.transform(data["test"][0])
            if sample_for_validation == "oot":
                pred = model_candidate.transform(data["OOT"][0])

            models_dict[model_name] = {
                "estimator": model_candidate,
                "predictions": pred,
            }

        models_scores = {
            key: self.eval_metric(y_true, models_dict[key]["predictions"])
            for key in models_dict
        }

        if len(models_scores) == 0:
            return model_, models_dict

        # Вычисление доверительного интервала для лучшей модели
        best_model = self.choose_best_model(models_scores, key=models_scores.get)
        best_model_pred = models_dict[best_model]["predictions"]
        best_model_scores = create_bootstrap_scores(
            y_true,
            y_true,
            best_model_pred,
            self.eval_metric,
            task=self.task,
        )
        best_model_ci = calculate_conf_interval(best_model_scores)

        recommend_final_model = self.choose_recommend_final_model(
            best_model_ci, models_dict, models_scores, best_model
        )
        logger = CombinedLogger([self._logger or _logger])
        logger.info(
            f"Best model after {self.name}{self.stage_params['features_step']} stage: {best_model}"
        )
        logger.info(
            f"Recommended model after {self.name}{self.stage_params['features_step']} stage: {recommend_final_model}"
        )

        return models_dict[recommend_final_model]["estimator"], models_dict

    @staticmethod
    def choose_recommend_final_model(
        best_model_ci, models_dict, models_scores, best_model
    ):
        """
        Выбор всех подходящих моделей
        """
        suitable_models_list = [
            key
            for key in models_scores
            if best_model_ci[0] <= models_scores[key] <= best_model_ci[1]
        ]
        if not suitable_models_list:
            suitable_models_list.append(best_model)
        suitable_models_dict = {
            key: len(models_dict[key]["estimator"].used_features)
            for key in suitable_models_list
        }
        return min(suitable_models_dict, key=suitable_models_dict.get)

    def add_cv_score(self, model_name: str):
        """
        Метод добавляет в словарь cv_score значение cv_score, если была выбрана Cross-Validation
        Parameters
        ----------
        model_name: str
            Название модели
        """
        if self.fitter.validation_type == ValidationType.CV:
            self.all_cv_mean_scores[model_name] = self.fitter.cv_mean_score

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
        np.random.seed(self.config_storage.random_seed)
        if not used_features:
            used_features = model.used_features
        self.used_features = self._set_used_features(
            data_storage=data_storage, used_features=used_features
        )

        # TODO максимизация и минимизация метрики в данном случае нужна для permutation importance, не для Shap
        final_model, models_dict = self._batch_feature_selection(
            model=model,
            data_storage=data_storage,
            used_features=used_features,
            features_step=self.stage_params["features_step"],
        )

        self.final_model = final_model
        self.stage_all_models_dict = models_dict
        self.used_features = final_model.used_features
        self.prediction = self.prediction_out(data_storage)
        self.is_fitted = True

        return self