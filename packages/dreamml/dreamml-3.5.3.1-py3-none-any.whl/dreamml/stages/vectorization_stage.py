from typing import List, Optional
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler

from dreamml.configs.config_storage import ConfigStorage
from dreamml.data._dataset import DataSet
from dreamml.pipeline.fitter import FitterBase
from dreamml.stages.algo_info import AlgoInfo
from dreamml.stages.stage import BaseStage
from dreamml.configs._vectorization_params import (
    TfidfParams,
    Word2VecParams,
    FastTextParams,
    GloveParams,
    BagOfWordsParams,
)
from dreamml.features.feature_vectorization import (
    BowVectorization,
    FastTextVectorization,
    GloveVectorization,
    TfidfVectorization,
    Word2VecVectorization,
)
from dreamml.logging import get_logger

seed = 27
np.random.seed(seed)
_logger = get_logger(__name__)


VECTORIZATION_REGISTRY = {
    "tf-idf": (TfidfParams, TfidfVectorization),
    "word2vec": (Word2VecParams, Word2VecVectorization),
    "fasttext": (FastTextParams, FastTextVectorization),
    "glove": (GloveParams, GloveVectorization),
    "bert": (None, None),
    "bow": (BagOfWordsParams, BowVectorization),
}


class VectorizationStage(BaseStage):
    name = "vectorization"

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
        self.config = config
        self.vectorizer_params = self._get_vectorizer_params()
        self.vectorizer = VECTORIZATION_REGISTRY[self.vectorization_name][1]
        self.drop_features = config.drop_features
        self.text_augmentations = config.text_augmentations

    def _get_vectorizer_params(self):
        vectorizer_params = {}
        if VECTORIZATION_REGISTRY[self.vectorization_name][0] is not None:
            params_instance = VECTORIZATION_REGISTRY[self.vectorization_name][0]()
            default_params = params_instance.get_default_params()
            user_params = params_instance.get_user_params(
                vectorization_name=self.vectorization_name,
                params=self.config.vectorization_params,
            )
            vectorizer_params = params_instance.merge_with_user_params(
                default_params=default_params, user_params=user_params
            )
        return vectorizer_params

    def _set_used_features(self, data_storage: DataSet, used_features: List = None):
        if not used_features:
            data = data_storage.get_eval_set(vectorization_name=None)
            used_features = data["train"][0].columns.tolist()
        return used_features

    def _fit(
        self,
        model,
        used_features: List[str],
        data_storage: DataSet,
        models=None,
    ) -> BaseStage:
        _logger.info(
            f"Stage vectorization info: starting fit: {self.vectorization_name}"
        )
        self.used_features = self._set_used_features(
            data_storage=data_storage, used_features=used_features
        )
        text_features = data_storage.text_features_preprocessed
        self.eval_sets = data_storage.get_eval_set(used_features=text_features)

        if (
            self.vectorization_name == "bert"
        ):  # В этом случае model - это vectorizer и estimator
            self.start_model = self._init_model(used_features=self.used_features)
            x_train, y_train = self.eval_sets["train"]
            train_indexes_before_augmentations = (
                data_storage.train_indexes_before_augmentations
            )
            x_train, y_train = (
                x_train.loc[train_indexes_before_augmentations],
                y_train.loc[train_indexes_before_augmentations],
            )
            self.start_model.fit(x_train, y_train, *self.eval_sets["valid"])
            self.start_model.evaluate_and_print(**self.eval_sets)
            self.final_model = self.start_model
            self.final_model.used_features = self.start_model.used_features

        else:
            self.vectorizer = self.vectorizer(text_features, **self.vectorizer_params)
            self.vectorizer.fit(*self.eval_sets["train"])

        self._set_embeddings(data_storage)
        return self

    def _set_embeddings(self, data_storage: DataSet):
        _logger.info(
            f"Stage vectorization info: starting transform: {self.vectorization_name}"
        )
        for sample_name, (X_sample, y_sample) in self.eval_sets.items():
            if self.vectorization_name == "bert":
                embeddings_df = self.final_model.transform(
                    X_sample, return_embedds=True
                )
            else:
                embeddings_df = self.vectorizer.transform(X_sample)

            if self.embedding_normalization is not None:
                debug_msg = f"Embedding normalization debug: {self.vectorization_name}-{sample_name}-{self.embedding_normalization}"
                _logger.debug(debug_msg)
                embeddings_df = self._normalize_embeddings(
                    embeddings_df, self.embedding_normalization
                )
            data_storage.set_embedding_sample(
                vectorization_name=self.vectorization_name,
                sample_name=sample_name,
                embeddings_df=embeddings_df,
            )

    @staticmethod
    def _normalize_embeddings(
        embeddings_df: pd.DataFrame, norm_type: str
    ):  # FIXME: а если несколько текстовых фичей, они конкатенируются и нормировать неправильно
        if norm_type == "l2_norm":
            embeddings_df = embeddings_df.fillna(embeddings_df.mean())
            norms = np.linalg.norm(embeddings_df, axis=1, keepdims=True)
            norms[norms == 0] = 1
            embeddings_df = embeddings_df / norms
        elif norm_type == "std_scaler":
            scaler = StandardScaler()
            embeddings_df = pd.DataFrame(
                scaler.fit_transform(embeddings_df),
                columns=embeddings_df.columns,
                index=embeddings_df.index,
            )
        elif norm_type == "min_max_scaler":
            scaler = MinMaxScaler()
            embeddings_df = pd.DataFrame(
                scaler.fit_transform(embeddings_df),
                columns=embeddings_df.columns,
                index=embeddings_df.index,
            )
        elif norm_type == "clipping":
            embeddings_df = embeddings_df.clip(lower=-1, upper=1)
        else:
            raise ValueError(f"Неизвестный тип нормализации эмбеддингов: {norm_type}")
        return embeddings_df