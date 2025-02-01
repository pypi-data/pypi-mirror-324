from abc import ABC, abstractmethod
from typing import List
from pathlib import Path
import pandas as pd
import numpy as np
import gensim
import fasttext
from nltk import word_tokenize
from gensim.models import FastText, KeyedVectors
from navec import Navec
from dreamml.logging import get_logger


_logger = get_logger(__name__)


class BaseVectorization(ABC):
    def __init__(self, text_features: List[str], vectorizer_type: str, **kwargs):
        self.text_features = text_features
        self.vectorizer_type = vectorizer_type
        self.concat_text_features = kwargs.pop("concat_text_features")
        self.model_path = kwargs.pop("model_path")
        self.binary: bool = kwargs.pop("binary") if "binary" in kwargs else False
        self.params = kwargs
        self.vector_size = kwargs.get("vector_size", None)
        self.feature_columns = {}
        self.used_features = []
        self.vectorizer = None

        if self.vector_size is None and self.vectorizer_type not in ("tf-idf", "bow"):
            raise ValueError(f"<vector_size> parameter not found.")

        if vectorizer_type in [
            "fasttext",
            "word2vec",
        ] and gensim.__version__.startswith("3.8"):
            kwargs["size"] = kwargs.pop(
                "vector_size"
            )  # Для совместимости gensim==3.8.x

        # Загрузка предобученной модели либо обучение векторизатора с нуля:

        # 1. Пользователь указать путь к модели - загружаем предобученную модель:
        #    - TF-IDF: Не загружаем модель, обучаем свой векторизатор
        #    - Word2Vec: | Required params: model_path, vector_size
        #    - Fasttext: | Required params: model_path, vector_size
        #    - Glove: | Required params: model_path, vector_size

        # 2. Пользователь не указал путь к модели - обучаем свой векторизатор:
        #    - TF-IDF Обучаем всегда | Required params: max_features
        #    - Word2Vec: | Required params: vector_size
        #    - Fasttext: | Required params: vector_size
        #    - Glove: Не обучаем, требуем model_path

        if self.model_path is not None:
            self._load_model()

    def _load_model(self):
        model_loader = VectorizerModelLoader(
            self.vectorizer_type, self.model_path, self.binary
        )
        self.vectorizer = model_loader.load_model()
        _logger.debug(f"Loaded pretrained vectorizer from '{self.model_path}'.")

    @abstractmethod
    def fit(self, x: pd.DataFrame, y: pd.Series):
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    def transform(self, x: pd.DataFrame):
        raise NotImplementedError("This method should be overridden by subclasses")

    def _get_vector(self, text):
        words = word_tokenize(text)
        vectors = [self.vectorizer[word] for word in words if word in self.vectorizer]
        if vectors:
            return np.mean(vectors, axis=0)
        else:
            return np.zeros(self.vector_size)

    def set_used_features(self):
        for _, feature_list in self.feature_columns.items():
            self.used_features.extend(feature_list)

    @staticmethod
    def _remove_preprocessed_prefix(feature_name: str, prefix: str = "_preprocessed"):
        return (
            feature_name.replace(prefix, "") if prefix in feature_name else feature_name
        )

    def _check_pretrained_loaded_vectorizer(self):
        if self.vectorizer is None and self.model_path is not None:
            self._load_model()


class VectorizerModelLoader:
    def __init__(self, model_type, model_path, binary=False):
        """
        Универсальный класс для загрузки предобученных моделей векторизаторов.

        :param model_type: Тип модели ('word2vec', 'glove', 'fasttext', 'gensim', и т.д.)
        :param model_path: Путь к файлу модели.
        :param binary: Указывается для моделей Word2Vec и FastText, если модель сохранена в бинарном формате.
        """
        self.model_type = model_type.lower()
        self.model_path = model_path
        self.binary = binary

    def load_model(self):
        file_extension = Path(self.model_path).suffix

        if (
            "navec" in self.model_path and file_extension == ".tar"
        ):  # Glove navec rus model
            model = Navec.load(self.model_path)
        elif self.model_type == "glove":
            model = self._load_glove_model(self.model_path)
        elif self.model_type == "word2vec":
            model = gensim.models.KeyedVectors.load_word2vec_format(
                self.model_path, binary=self.binary
            )
        elif self.model_type == "fasttext":
            if file_extension == ".model":
                try:
                    model = FastText.load(self.model_path)
                except:  # Загружает более старые версии fasttext, которые есть в sberosc
                    model = KeyedVectors.load(self.model_path)
            else:
                model = fasttext.load_model(self.model_path)
        elif self.model_type == "gensim":
            model = gensim.models.Word2Vec.load(self.model_path)
        else:
            raise ValueError(f"Unsupported model type: {self.model_type}")
        return model

    def _load_glove_model(self, glove_file_path):
        """
        Загрузка GloVe модели из текстового файла.

        :param glove_file_path: Путь к текстовому файлу GloVe.
        :return: Возвращает объект gensim KeyedVectors.
        """
        glove_model = {}
        with open(glove_file_path, "r", encoding="utf-8") as f:
            for line in f:
                split_line = line.split()
                word = split_line[0]
                embedding = np.array([float(val) for val in split_line[1:]])
                glove_model[word] = embedding

        # Конвертация в формат gensim
        word_vectors = gensim.models.KeyedVectors(vector_size=len(embedding))
        word_vectors.add_vectors(list(glove_model.keys()), list(glove_model.values()))
        return word_vectors