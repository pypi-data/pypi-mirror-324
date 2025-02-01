import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import umap

from dreamml.logging import get_logger

_logger = get_logger(__name__)


class CalculateDetailedMetricsTopicModeling:

    def __init__(
        self,
        models,
        experiment_path: str,
        vectorizers_dict: dict,
        text_feature: str,
        metric_name: str = "gini",
        metric_params: dict = None,
        umap_params: dict = None,
    ):
        self.models = models
        self.model = None
        self.experiment_path = experiment_path
        self.vectorizers_dict = vectorizers_dict
        self.text_feature = text_feature
        self.metric_name = metric_name
        self.metric_params = metric_params

        self.num_topics = 0
        self.topic_words = dict()
        self.umap_params = umap_params or {}

    def make_umap_plot(self, model_type, model_name):
        if model_type == "lda":
            topic_distributions = np.array(
                [
                    self.model.estimator.get_document_topics(doc, minimum_probability=0)
                    for doc in self.model.topic_modeling_data.corpus
                ]
            )
            doc_topic_dist = np.array(
                [[topic[1] for topic in doc] for doc in topic_distributions]
            )

            umap_model = umap.UMAP(n_components=2, random_state=27, **self.umap_params)
            umap_values = umap_model.fit_transform(doc_topic_dist)

            plt.figure(figsize=(8, 5))
            plt.scatter(
                umap_values[:, 0],
                umap_values[:, 1],
                c=np.argmax(doc_topic_dist, axis=1),
                cmap="viridis",
                s=50,
            )
            plt.title(f"UMAP визуализация распределения тем {model_name}")
            plt.colorbar(label="Темы")
            plt.grid(True)
            plt.savefig(f"{self.experiment_path}/images/umap_{model_name}.png")
            plt.close()

        if model_type == "bertopic":
            fig = self.model.estimator.visualize_topics()
            fig.write_image(f"{self.experiment_path}/images/umap_{model_name}.png")
            pass

    def transform(self, model_name):
        vectorizer = None
        vocab = None
        self.model = self.models[f"{model_name}"]

        try:
            vectorizer = self.vectorizers_dict["tf-idf_vectorizer"]
            vocab = vectorizer.vectorizers[self.text_feature].vocabulary_
        except Exception as e:
            pass

        try:
            vectorizer = self.vectorizers_dict["bow_vectorizer"]
        except Exception as e:
            pass

        if self.model.model_name == "bertopic":
            self.make_umap_plot(self.model.model_name, model_name)
            top_n_words = self.model.estimator.get_topics()
            for topic_name, words in top_n_words.items():
                if topic_name != -1:
                    self.topic_words.update(
                        {
                            str(topic_name): [
                                re.sub(r"[^а-яА-Яa-zA-Z]+", "", words[i][0])
                                for i in range(0, 10)
                            ]
                        }
                    )

        if self.model.model_name == "lda" or self.model.model_name == "ensembelda":
            if self.model.model_name == "lda":
                self.make_umap_plot("lda", model_name)
            topics_info = self.model.estimator.print_topics()
            self.num_topics = len(topics_info)
            for topic_name, words in topics_info:
                if vectorizer.name == "bow":
                    self.topic_words.update(
                        {
                            str(topic_name): [
                                re.sub(r"[^а-яА-Яa-zA-Z]+", "", word)
                                for word in words.split("+")
                            ]
                        }
                    )

                else:
                    self.topic_words.update(
                        {
                            str(topic_name): [
                                self.get_value_by_key(
                                    vocab,
                                    int(re.search(r"tf-idf_(\d+)", word).group(1)),
                                )
                                for word in words.split("+")
                            ]
                        }
                    )

        return pd.DataFrame(data=self.topic_words)

    @staticmethod
    def get_value_by_key(d, value):
        for k, v in d.items():
            if v == value:
                return k