import logging
from typing import List, Optional
import gensim
from gensim.models import LdaModel
import gensim.corpora as corpora
from scipy.sparse import csr_matrix
from typing import Dict, Any

from dreamml.modeling.models.estimators import BaseModel
from dreamml.data import TopicModelingData


class LDAModel(BaseModel):
    model_name = "lda"

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
            "topic_modeling": LdaModel,
        }
        return estimators

    def fit(self, data):

        if self.vectorization_name == "bow":
            self.topic_modeling_data.dictionary = data[0][self.used_features[0]]["dict"]
            self.topic_modeling_data.corpus = data[0][self.used_features[0]][
                "bow_corpus"
            ]
        elif self.vectorization_name == "tfidf":
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
            alpha=self.params["alpha"],
            eta=self.params["eta"],
            random_state=self.params["random_state"],
            per_word_topics=True,
        )

        self.topic_modeling_data.base_model = self.estimator
        self.fitted = True

    def transform(self, data):
        if self.vectorization_name == "bow":
            self.topic_modeling_data.corpus = data[self.used_features[0]]["bow_corpus"]
        elif self.vectorization_name == "tfidf":
            X = data[self.used_features]
            sparse_matrix = csr_matrix(X.values)
            self.topic_modeling_data.corpus = gensim.matutils.Sparse2Corpus(
                sparse_matrix, documents_columns=True
            )

        pred_topics = self.estimator.get_document_topics(
            self.topic_modeling_data.corpus, minimum_probability=0
        )
        return pred_topics

    def serialize(self) -> dict:
        data = super().serialize()

        additional_dict = {
            "topic_modeling_data": self.topic_modeling_data,
        }

        data["additional"].update(additional_dict)

        return data

    @classmethod
    def deserialize(cls, data):
        instance = super().deserialize(data)

        instance.topic_modeling_data = data["additional"]["topic_modeling_data"]

        return instance

    def evaluate_and_print(self, **eval_sets):
        pass