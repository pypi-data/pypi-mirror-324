from typing import List, Dict, Optional
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
from dreamml.stages.stage import BaseStage
from dreamml.utils.confidence_interval import create_bootstrap_scores
from dreamml.utils.confidence_interval import calculate_conf_interval
from dreamml.features.feature_selection.select_subset_features import (
    select_subset_features,
)
from dreamml.stages.model_based_stage import ModelBasedStage
from dreamml.stages.algo_info import AlgoInfo
from dreamml.pipeline.fitter import FitterBase
from dreamml.utils import ValidationType

_logger = get_logger(__name__)


class BatchSelectionModelStage(ModelBasedStage):
    """
    Этап пакетного TOP@ отбора признаков и построение моделей.
    """

    name = "batch"

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
            return self.eval_metric(y_true, y_pred)
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
        self,
        model,
        feature_importance,
        data_storage,
        used_features,
        features_step: int = 10,
        min_features: int = 10,
    ):
        """
        Функция для построения и выбора лучшей модели.

        Parameters
        ----------
        model: dreamml.modeling.models.estimators.boosting_base.BoostingBaseModel
            Экземпляр модели для обучения.

        feature_importance: pd.DataFrame
            Таблица с названиями признаков и с метрикой их важности

        data_storage: DataSet
            Экземпляр класса-хранилища данных

        used_features: List
            Список используемых признаков.

        features_step: int
            Шаг по количеству признаков для построения моделей

        min_features: int
            Количество признаков с которого стартует алгоритм.

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
        n_features = np.arange(min_features, feature_importance.shape[0], features_step)
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
        # Определение выборки для подсчета метрики, останова и выбора лучшей модели
        if sample_for_validation == "test":
            y_pred = model_.transform(data["test"][0])
            y_true = data["test"][1]
            metric_to_stop = self._stop_criteria(
                y_pred, y_true, self.config_storage.stop_criteria
            )
        elif sample_for_validation == "oot":
            y_pred = model_.transform(data["OOT"][0])
            y_true = data["OOT"][1]
            metric_to_stop = self._stop_criteria(
                y_pred, y_true, self.config_storage.stop_criteria
            )
        else:  # "valid"
            y_true = self.fitter.get_validation_target(
                data_storage, vectorization_name=self.vectorization_name
            )
            metric_to_stop = self._stop_criteria(
                y_pred, y_true, self.config_storage.stop_criteria
            )

        # Процесс построения моделей с отбором по TOP@ признаков
        for n in tqdm(n_features):
            selected_features = select_subset_features(
                feature_importance, self.remaining_features, top_k=n
            )
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

            model_name = f"{model_candidate.model_name}.{len(selected_features)}.S{features_step}"
            self.add_cv_score(model_name)

            if sample_for_validation == "test":
                pred = model_candidate.transform(data["test"][0])
            if sample_for_validation == "oot":
                pred = model_candidate.transform(data["OOT"][0])

            models_dict[model_name] = {
                "estimator": model_candidate,
                "predictions": pred,
            }

            metric = self.eval_metric(y_true, pred)

            if self.metric_comp(metric, metric_to_stop):
                break
        else:  # Если остановки не произошло, то добавить базовую модель
            model_name = (
                f"{model_.model_name}.{feature_importance.shape[0]}.S{features_step}"
            )
            self.add_cv_score(model_name)
            models_dict[model_name] = {"estimator": model_, "predictions": y_pred}
            # Выбор наилучшей модели
        if self.task in ["regression", "timeseries"]:
            models_scores = {
                key: self.eval_metric(y_true, models_dict[key]["predictions"])
                for key in models_dict
            }
        else:
            models_scores = {
                key: self.eval_metric(y_true, models_dict[key]["predictions"])
                for key in models_dict
            }

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

        if self.fitter.validation_type == ValidationType.CV:
            splitter_df = data_storage.get_cv_splitter_df(
                self.fitter.cv.get_required_columns()
            )
        else:
            splitter_df = None

        # TODO максимизация и минимизация метрики в данном случае нужна для permutation importance, не для Shap
        importance_ = self.fitter.calculate_importance(
            estimators=model,
            data_storage=data_storage,
            used_features=used_features,
            splitter_df=splitter_df,
            fraction_sample=self.stage_params["fraction_sample"],
            vectorization_name=self.vectorization_name,
        )

        final_model, models_dict = self._batch_feature_selection(
            model=model,
            feature_importance=importance_,
            data_storage=data_storage,
            used_features=used_features,
            features_step=self.stage_params["features_step"],
            min_features=self.stage_params["min_features"],
        )

        self.final_model = final_model
        self.stage_all_models_dict = models_dict
        self.used_features = final_model.used_features
        self.prediction = self.prediction_out(data_storage)
        self.is_fitted = True

        return self

    def _set_params(self, params: dict):
        raise NotImplementedError