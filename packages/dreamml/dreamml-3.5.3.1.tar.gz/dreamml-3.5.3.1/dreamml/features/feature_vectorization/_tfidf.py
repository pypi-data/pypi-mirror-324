from typing import List
from scipy.sparse import hstack
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from dreamml.features.feature_vectorization._base import BaseVectorization


class TfidfVectorization(BaseVectorization):
    name = "tf-idf"

    def __init__(self, text_features: List[str], **kwargs):
        super().__init__(text_features, "tf-idf", **kwargs)
        if self.concat_text_features:
            self.vectorizers = {"text": TfidfVectorizer(**self.params)}
        else:
            self.vectorizers = {
                feature: TfidfVectorizer(**self.params)
                for feature in self.text_features
            }

    def fit(self, x: pd.DataFrame, y: pd.Series):
        if self.concat_text_features:
            concat_text_features_series = (
                x[self.text_features].astype(str).agg(" ".join, axis=1)
            )
            vectorizer = self.vectorizers["text"]
            vectorizer.fit(concat_text_features_series)
            self.feature_columns["text"] = [
                self._remove_preprocessed_prefix(f"{self.name}_{idx}")
                for idx in range(vectorizer.get_feature_names_out().size)
            ]
        else:
            for feature in self.text_features:
                self.vectorizers[feature].fit(x[feature])
                self.feature_columns[feature] = [
                    self._remove_preprocessed_prefix(f"{self.name}_{feature}_{idx}")
                    for idx in range(
                        self.vectorizers[feature].get_feature_names_out().size
                    )
                ]
        self.set_used_features()

    def transform(self, x: pd.DataFrame):
        embeddings_list = []
        columns_list = []

        if self.concat_text_features:
            concat_text_features_series = (
                x[self.text_features].astype(str).agg(" ".join, axis=1)
            )
            vectorizer = self.vectorizers["text"]
            columns_list = self.feature_columns["text"]
            embeddings_list = [vectorizer.transform(concat_text_features_series)]
        else:
            for feature in self.text_features:
                vectorizer = self.vectorizers[feature]
                columns = self.feature_columns[feature]
                tfidf_matrix = vectorizer.transform(x[feature])
                embeddings_list.append(tfidf_matrix)
                columns_list.extend(columns)

        embeddings_df = pd.DataFrame(
            data=hstack(embeddings_list).toarray(), columns=columns_list, index=x.index
        )
        return embeddings_df