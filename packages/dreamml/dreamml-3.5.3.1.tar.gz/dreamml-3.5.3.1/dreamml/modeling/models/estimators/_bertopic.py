from pathlib import Path
import logging
from typing import List, Optional
import gensim.corpora as corpora
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from typing import Dict, Any
from hdbscan import HDBSCAN
from umap import UMAP

from dreamml.modeling.models.estimators import BaseModel
from dreamml.data import TopicModelingData


class BERTopicModel(BaseModel):
    model_name = "bertopic"

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
        self.model_path = str(
            Path(__file__).parent.parent.parent.parent / "references/models/e5"
        )
        self.topic_modeling_data = TopicModelingData()
        self.topic_modeling_data.model_type = self.model_name

        self.umap_model = None
        self.hdbscan_model = None

        self.umap_params = self.get_umap_params(estimator_params)
        self.hdbscan_params = self.get_hdbscan_params(estimator_params)

    @property
    def _estimators(self):
        estimators = {
            "topic_modeling": BERTopic,
        }
        return estimators

    def get_umap_params(self, params):
        return {
            "n_neighbors": params["n_neighbors"],
            "n_components": params["n_components"],
            "min_dist": params["min_dist"],
            "metric": params["metric_umap"],
            "n_epochs": params["umap_epochs"],
        }

    def get_hdbscan_params(self, params):
        return {
            "min_cluster_size": params["min_cluster_size"],
            "max_cluster_size": params["max_cluster_size"],
            "min_samples": params["min_samples"],
            "metric": params["metric_hdbscan"],
            "cluster_selection_method": params["cluster_selection_method"],
            "prediction_data": params["prediction_data"],
        }

    def fit(self, data):
        X = data[0][self.used_features[0]].values
        self.topic_modeling_data.docs = X
        self.topic_modeling_data.tokenized_docs = [doc.split() for doc in X]
        self.topic_modeling_data.dictionary = corpora.Dictionary(
            [doc.split() for doc in X]
        )

        embedding_model = SentenceTransformer(self.model_path, similarity_fn_name="dot")

        self.umap_model = UMAP(**self.umap_params)
        self.hdbscan_model = HDBSCAN(**self.hdbscan_params)

        self.estimator = self.estimator_class(
            language="multilingual",
            embedding_model=embedding_model,
            umap_model=self.umap_model,
            hdbscan_model=self.hdbscan_model,
            verbose=True,
        )
        self.estimator.fit(X)

        self.topic_modeling_data.base_model = self.estimator
        self.fitted = True

    def transform(self, data):
        X = data[self.used_features[0]].values
        self.topic_modeling_data.docs = X
        self.topic_modeling_data.tokenized_docs = [doc.split() for doc in X]
        self.topic_modeling_data.dictionary = corpora.Dictionary(
            [doc.split() for doc in X]
        )

        probs, pred_topics = self.estimator.transform(X)
        return pred_topics

    def evaluate_and_print(self, **eval_sets):
        topics, probs = self.estimator.transform(self.topic_modeling_data.docs)
        self.topic_modeling_data.pred_topics = topics