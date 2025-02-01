"""Алгоритмы векторизации: TF-IDF, Word2Vec, FastText, Glove."""

import pickle
from typing import Dict


class BaseVectorizationParams:
    def get_common_params(self):
        return {}

    def get_default_params(self):
        common_params = self.get_common_params()
        default_params = self.get_params()
        common_params.update(default_params)
        return common_params

    def get_params(self):
        raise NotImplementedError("This method should be overridden by subclasses")

    def merge_with_user_params(self, default_params, user_params):
        merged_params = default_params.copy()
        merged_params.update(user_params)
        return merged_params

    @staticmethod
    def get_user_params(vectorization_name: str, params: str) -> Dict:
        if isinstance(params, str) and params.split(".")[-1] in ["pickle", "pkl"]:
            with open(params, "rb") as f:
                params = pickle.load(f)
        if isinstance(params, dict):
            if vectorization_name not in params:
                return {}
            return params[vectorization_name]
        else:
            raise Exception(
                "Гиперпараметры можно задать с помощью словаря (dict) или с помощью пути до pickle файла (.pkl, .pickle)"
            )


class TfidfParams(BaseVectorizationParams):
    def get_params(self):
        tf_idf_params = {
            "concat_text_features": True,
            "model_path": None,
            "lowercase": True,
            "analyzer": "word",  # {"word", "char", "char_wb"}
            "use_idf": True,
            "ngram_range": (1, 1),
            "max_features": 50000,
        }
        return tf_idf_params


class Word2VecParams(BaseVectorizationParams):
    def get_params(self):
        word2vec_params = {
            "concat_text_features": True,
            "model_path": None,
            "vector_size": None,
        }
        return word2vec_params


class FastTextParams(BaseVectorizationParams):
    def get_params(self):
        fasttext_params = {
            "concat_text_features": True,
            "model_path": None,
            "vector_size": None,
        }
        return fasttext_params


class GloveParams(BaseVectorizationParams):
    def get_params(self):
        glove_params = {
            "concat_text_features": True,
            "model_path": None,
            "vector_size": None,
        }
        return glove_params


class BagOfWordsParams(BaseVectorizationParams):
    def get_params(self):
        bow_params = {
            "concat_text_features": True,
            "model_path": None,
            "vector_size": None,
        }
        return bow_params