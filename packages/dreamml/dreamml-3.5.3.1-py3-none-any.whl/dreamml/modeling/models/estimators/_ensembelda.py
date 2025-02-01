import logging
from typing import List, Optional
import gensim
from gensim.models import EnsembleLda
import gensim.corpora as corpora
from scipy.sparse import csr_matrix
from typing import Dict, Any

from dreamml.logging import get_logger
from dreamml.modeling.models.estimators import BaseModel
from dreamml.data import TopicModelingData

_logger = get_logger(__name__)


class EnsembeldaModel(BaseModel):
    model_name = "ensembelda"

    """
    Модель ensembelda со стандартизованным API для DreamML

    Parameters
    ----------
    estimator_params : dict
        Словарь с гиперпараметрами
    used_features : list
        Список фич отобранных исходя из значений конкретной метрики
    params : dict
        Словарь с дополнительными параметрами (optional_params, ...)

    Attributes
    ----------
    params : dict
        Словарь с гиперпараметрами
    task : str
        Название задачи (topic_modeling, ...)
    model_name : str
        Название алгоритма (lda, ensembelda, bertopic ...)
    used_features : list
        Список фич отобранных исходя из значений конкретной метрики
    estimator : callable
        Экземпляр обученной модели.
    categorical_features : list
        Список категориальных фич
    fitted : bool
        Была ли обучена модель, то есть был вызван метод fit.
        True - да, False - нет

    """

    def __init__(
        self,
        estimator_params: Dict[str, Any],
        task: str,
        used_features: List[str],
        categorical_features: List[str],
        metric_name,
        metric_params,
        parallelism: int = -1,
        train_logger: Optional[logging.Logger] = None,
        **params,
    ):
        super().__init__(
            estimator_params,
            task,
            used_features,
            categorical_features,
            metric_name,
            metric_params,
            parallelism=parallelism,
            train_logger=train_logger,
            **params,
        )
        self.estimator_class = self._estimators.get(self.task)
        self.topic_modeling_data = TopicModelingData()
        self.topic_modeling_data.model_type = self.model_name

    @property
    def _estimators(self):
        estimators = {
            "topic_modeling": EnsembleLda,
        }
        return estimators

    def fit(self, data):

        if self.vectorization_name == "bow":
            self.topic_modeling_data.dictionary = data[0][self.used_features[0]]["dict"]
            self.topic_modeling_data.corpus = data[0][self.used_features[0]][
                "bow_corpus"
            ]
        elif self.vectorization_name == "tf-idf":
            X = data[0][self.used_features]
            sparse_matrix = csr_matrix(X.values)
            self.topic_modeling_data.corpus = gensim.matutils.Sparse2Corpus(
                sparse_matrix, documents_columns=True
            )
            self.topic_modeling_data.dictionary = corpora.Dictionary(
                [X.columns.tolist()]
            )

        self.estimator = self.estimator_class(
            corpus=self.topic_modeling_data.corpus,
            id2word=self.topic_modeling_data.dictionary,
            passes=self.params["passes"],
            num_topics=self.params["num_topics"],
            num_models=self.params["num_models"],
            iterations=self.params["iterations"],
            random_state=self.params["random_state"],
            per_word_topics=True,
        )

        self.estimator.recluster(eps=0.5)
        self.topic_modeling_data.base_model = self.estimator
        self.fitted = True

    def transform(self, data):
        if self.vectorization_name == "bow":
            self.topic_modeling_data.corpus = data[self.used_features[0]]["bow_corpus"]
            pred_topics = []
            for doc in self.topic_modeling_data.corpus:
                topic_dist = self.estimator[doc]
                pred_topics.append(topic_dist)
        elif self.vectorization_name == "tf-idf":
            X = data[self.used_features]
            sparse_matrix = csr_matrix(X.values)
            self.topic_modeling_data.corpus = gensim.matutils.Sparse2Corpus(
                sparse_matrix, documents_columns=True
            )
            pred_topics = []
            for doc in self.topic_modeling_data.corpus:
                topic_dist = self.estimator[doc]
                pred_topics.append(topic_dist)

        return pred_topics

    def evaluate_and_print(self, **eval_sets):
        pass