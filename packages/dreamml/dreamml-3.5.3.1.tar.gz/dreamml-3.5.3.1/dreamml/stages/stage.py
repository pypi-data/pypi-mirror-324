from __future__ import annotations
from enum import Enum
import abc
import logging
from abc import ABC
from collections.abc import Mapping
from copy import deepcopy
from typing import Tuple, Dict, Optional, List, Any

import pandas as pd

from dreamml.logging import get_logger, get_propagate
from dreamml.features.feature_extraction._transformers import LogTargetTransformer
from dreamml.modeling.models.estimators import BaseModel
from dreamml.pipeline.fitter import FitterBase
from dreamml.stages.algo_info import AlgoInfo
from dreamml.data._dataset import DataSet
from dreamml.utils import ValidationType

from dreamml.configs.config_storage import ConfigStorage

_logger = get_logger(__name__)


class StageStatus(Enum):
    """
    `Enum`, который хранит состояние стейджа
    """

    FITTED = "fitted"
    NOT_FITTED = "not_fitted"
    ERROR = "error"  # TODO: сейчас не используется. На будущее, когда будет обработка ошибок в стейджах


class BaseStage(ABC):
    name: str

    """
    Абстрактный класс для этапов Pipeline.
    Все стейджи должны быть наследованы от этого класса и реализовать все абстрактные методы.
    Все стейджи должны уметь принимать конфигурации от пользователя.
    Все стейджи должны иметь конфигурации по умолчанию, если не заданы конфигурации от пользователя.
    Все стейджи должны работать с объектом класса DataSet

    """

    def __init__(
        self,
        algo_info: AlgoInfo,
        config: ConfigStorage,
        fitter: Optional[FitterBase] = None,
        vectorization_name: str = None,
    ):
        self.experiment_path = None
        self.task = config.task
        self.start_model = None
        self.final_model = None
        self.models = None
        # TODO Должен обязательно заполняться used_features, можно через абстрактный класс set_used_features
        self.used_features = None
        # TODO Должен обязательно заполняться feature_importance
        self.feature_importance = None
        self.model_type = None
        self.prediction = None
        self.algo_info = algo_info
        self.random_stage = config.random_seed
        self.is_fitted = False
        self.cv_mean_score = 0
        self.fitter = fitter
        self.metric_name = config.eval_metric
        self.metric_params = config.metric_params
        self.weights = config.weights
        self.target_with_nan_values = config.target_with_nan_values
        self._log_target_transformer = (
            LogTargetTransformer() if config.log_target else None
        )
        self.parallelism = config.parallelism
        self.vectorization_name = vectorization_name
        self.embedding_normalization = config.embedding_normalization

        self._status: StageStatus = StageStatus.NOT_FITTED
        self._id: Optional[str] = None
        self._logger: Optional[logging.Logger] = None

    @property
    @abc.abstractmethod
    def name(self):
        raise NotImplementedError

    @property
    def id(self):
        if self._id is None:
            raise ValueError(f"You must set `id` first.")
        return self._id

    @id.setter
    def id(self, new_id):
        self._id = new_id

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, new_status: StageStatus):
        if isinstance(new_status, StageStatus):
            self._status = new_status
        else:
            raise ValueError(
                f"{new_status=} is expected to be an instance of {StageStatus}"
            )

    def _init_model(
        self,
        used_features: list,
        hyperparams: Mapping[str, Any] = None,
        fix_stage: bool = None,
    ) -> BaseModel:
        """
        Функция инициализации модели из атрибута algo_info

        Parameters
        ----------
        used_features:list
            Список используемых фич
        hyperparams: dict
            Гиперпараметры модели

        Returns
        -------
        model: BaseModel
            Проинициализированная модель
        """
        self.model_type = self.algo_info.algo_class

        if fix_stage:
            estimator_params = deepcopy(self.algo_info.fixed_params)
        else:
            estimator_params = deepcopy(self.algo_info.algo_params)

        if hyperparams:
            for param in hyperparams:
                if param == "n_estimators":
                    logging.debug(
                        f"{estimator_params.get(param)=} left as is. Skipping value in _init_model {hyperparams[param]=}."
                    )

                    continue

                estimator_params[param] = hyperparams[param]

        return self.model_type(
            estimator_params=estimator_params,
            task=self.task,
            used_features=used_features,
            categorical_features=self.algo_info.cat_features,
            metric_name=self.metric_name,
            metric_params=self.metric_params,
            weights=self.weights,
            target_with_nan_values=self.target_with_nan_values,
            log_target_transformer=self._log_target_transformer,
            parallelism=self.parallelism,
            train_logger=self._logger,
            vectorization_name=self.vectorization_name,
            text_features=self.algo_info.text_features,
            augmentation_params=self.algo_info.augmentation_params,
        )

    def init_logger(self, log_file: Optional[str] = None):
        if self._id is None:
            raise ValueError(
                "To initialize stage logger you must set stage.id to some unique value in the current run."
            )

        self._logger = logging.getLogger(f"{__name__}.{self.id}")
        self._logger.propagate = get_propagate()

        if len(self._logger.handlers) > 0:
            handlers = self._logger.handlers
            for handler in handlers:
                self._logger.removeHandler(handler)

        if log_file is not None:
            formatter = logging.Formatter(
                fmt="[%(asctime)s] - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            file_handler = logging.FileHandler(log_file, delay=True)
            file_handler.setFormatter(formatter)

            self._logger.addHandler(file_handler)

    def fit_transform(
        self,
        model: BaseModel,
        used_features: list,
        data_storage: DataSet,
        models: list = None,
    ) -> Tuple[BaseModel, list, pd.DataFrame, pd.DataFrame, list]:
        """
        Метод, который вызывается во время исполнения pipeline у каждого стейджа.

        Parameters
        ----------
        model:BaseModel
            Экземпляр модели
        used_features
            Список используемых фич
        data_storage
            Данные для обучения
        models: list
            Список моделей полученных на фолдах кросс-валидации
        Returns
        -------
        Tuple[BoostingBaseModel, list]
            Обученная модель и список фич
        """
        return self.fit(
            model=model,
            used_features=used_features,
            data_storage=data_storage,
            models=models,
        ).transform()

    @abc.abstractmethod
    def _fit(
        self,
        model: BaseModel,
        used_features: List[str],
        data_storage: DataSet,
        models: List[BaseModel] = None,
    ) -> BaseStage:
        """
        Абстрактный фабричный метод, который вызывается в self.fit.
        Реализуется у каждого стейджа по своему

        Parameters
        ----------
        models:list
            Список моделей полученных на каждом fold кросс-валидации
        model: BaseModel
            Обёртка DreamML над sklearn-like моделями
        used_features: list
            Список используемых при обучении фич
        data_storage: DataSet
            Объект содержащий информацию о выборках для обучения и тестирования модели
        """
        # TODO забирать cv_score в каждом стейдже в этом методе
        raise NotImplementedError

    def fit(
        self,
        model: BaseModel,
        used_features: Optional[list],
        data_storage: DataSet,
        models=None,
    ) -> BaseStage:
        """
        Метод, который вызывает фабричный метод self._fit и который в конце ставит флаг successful=True.
        Вызывается в self.fit_transform

        Parameters
        ----------
        models:list
            Список моделей полученных на каждом fold кросс-валидации
        model: BaseModel
            Обёртка DreamML над sklearn-like моделями
        used_features: list
            Список используемых при обучении фич
        data_storage: DataSet
            Объект содержащий информацию о выборках для обучения и тестирования модели

        Returns
        -------
        self: BaseStage
            Возвращает ссылку на свой объект

        """
        if self.is_fitted:
            return self

        logger = self._logger or _logger
        # logger.monitor("Start fitting stage")
        self._fit(
            model=model,
            used_features=used_features,
            data_storage=data_storage,
            models=models,
        )
        if self.fitter is not None and self.fitter.validation_type == ValidationType.CV:
            self.cv_mean_score = self.fitter.cv_mean_score
        self.is_fitted = True
        return self

    def transform(self) -> Tuple[BaseModel, list, pd.DataFrame, pd.DataFrame, list]:
        return (
            self.final_model,
            self.used_features,
            self.feature_importance,
            self.prediction,
            self.models,
        )

    def prediction_out(self, dataset: DataSet):
        """
        Возвращает значения для переменных prediction_dict

        Parameters
        ----------
        dataset: Dict[string, Tuple[pandas.DataFrame, pandas.Series]]
            Словарь, где ключ - название выборки, значение - кортеж с
            матрицей признаков и вектором истинных ответов.
        """

        prediction_dict = {}
        used_features = self.used_features
        eval_set = dataset.get_eval_set(
            used_features, vectorization_name=self.vectorization_name
        )

        if self.task == "amts":
            eval_set = dataset.get_amts_data()

        if ("valid" in eval_set) and (len(eval_set["valid"][0]) == 0):
            del eval_set["valid"]
        for sample in eval_set:
            data, target = eval_set[sample]
            prediction = self.final_model.transform(data)
            prediction_dict[sample] = prediction
        return prediction_dict

    def _drop_text_features(
        self, data_storage: DataSet, used_features: Optional[List[str]]
    ):
        if used_features is not None:
            drop_text_features = (
                data_storage.text_features_preprocessed + data_storage.text_features
            )
            used_features = [
                feature
                for feature in used_features
                if feature not in drop_text_features
            ]
            if len(used_features) == 0:
                used_features = None
        return used_features