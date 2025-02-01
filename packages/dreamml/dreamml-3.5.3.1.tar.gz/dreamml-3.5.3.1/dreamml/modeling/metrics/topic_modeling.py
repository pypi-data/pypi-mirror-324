import numpy as np
from scipy.spatial.distance import cosine
from typing import Optional
from gensim.models import CoherenceModel
from sklearn.metrics import silhouette_score
from sklearn.metrics.pairwise import cosine_distances

from dreamml.modeling.metrics._base_metric import BaseMetric, OptimizableMetricMixin
from dreamml.data import TopicModelingData


class TopicModelingMetric(BaseMetric):
    _task_type: str = "topic_modeling"

    def __init__(
        self,
        model_name: Optional[str] = None,
        task: Optional[str] = None,
        **params,
    ):
        super().__init__(
            model_name=model_name,
            task=task,
            **params,
        )

    def __call__(self, topic_modeling_data: TopicModelingData):
        return self._score_function(topic_modeling_data)


class LogPerplexity(TopicModelingMetric, OptimizableMetricMixin):
    name = "log_perplexity"
    maximize = False

    def _score_function(self, topic_modeling_data: TopicModelingData):
        perplexity = topic_modeling_data.base_model.log_perplexity(
            topic_modeling_data.corpus
        )
        return perplexity


class Coherence(TopicModelingMetric, OptimizableMetricMixin):
    name = "coherence"
    maximize = True

    def _score_function(self, topic_modeling_data: TopicModelingData):

        if topic_modeling_data.model_type == "bertopic":
            topic_info = topic_modeling_data.base_model.get_topic_info()
            topics = []
            for topic_id in range(len(topic_info)):
                topic = topic_modeling_data.base_model.get_topic(topic_id)
                if topic:
                    topics.append([word for word, _ in topic])

            cm = CoherenceModel(
                topics=topics,
                texts=topic_modeling_data.tokenized_docs,
                dictionary=topic_modeling_data.dictionary,
                coherence="u_mass",
            )

        elif topic_modeling_data.model_type in ("lda", "ensembelda"):
            cm = CoherenceModel(
                model=topic_modeling_data.base_model,
                corpus=topic_modeling_data.corpus,
                coherence="u_mass",
            )

        return cm.get_coherence()


class AverageDistance(TopicModelingMetric, OptimizableMetricMixin):
    name = "average_distance"
    maximize = True

    def _score_function(self, topic_modeling_data: TopicModelingData):

        if topic_modeling_data.model_type == "bertopic":
            topic_embeddings = topic_modeling_data.base_model.topic_embeddings_
            cosine_dist = cosine_distances(topic_embeddings)
            average_distance = np.mean(
                cosine_dist[np.triu_indices_from(cosine_dist, k=1)]
            )

        if topic_modeling_data.model_type in ("lda", "ensembelda"):
            topic_vectors = topic_modeling_data.base_model.get_topics()
            num_topics = len(topic_vectors)
            distances = []

            for i in range(num_topics):
                for j in range(i + 1, num_topics):
                    dist = cosine(topic_vectors[i], topic_vectors[j])
                    distances.append(dist)
            average_distance = np.mean(distances)

        return average_distance


class SilhouetteScore(TopicModelingMetric, OptimizableMetricMixin):
    name = "silhouette_score"
    maximize = True

    def _score_function(self, topic_modeling_data: TopicModelingData):
        embeddings = (
            topic_modeling_data.base_model.embedding_model.embedding_model.encode(
                topic_modeling_data.docs
            )
        )
        silhouette_avg = silhouette_score(embeddings, topic_modeling_data.pred_topics)
        return silhouette_avg