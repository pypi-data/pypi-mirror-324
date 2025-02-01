from typing import List
import pandas as pd
import numpy as np
from numpy import hstack

from dreamml.features.feature_vectorization._base import BaseVectorization


class GloveVectorization(BaseVectorization):
    name = "glove"

    def __init__(self, text_features: List[str], **kwargs):
        super().__init__(text_features, "glove", **kwargs)
        if self.model_path is None:
            msg = f"Required parameters for glove: model_path"
            raise ValueError(msg)

    def fit(self, x: pd.DataFrame, y: pd.Series):
        if self.concat_text_features:
            self.feature_columns["text"] = [
                self._remove_preprocessed_prefix(f"{self.name}_{idx}")
                for idx in range(self.vector_size)
            ]
        else:
            for feature in self.text_features:
                self.feature_columns[feature] = [
                    self._remove_preprocessed_prefix(f"{self.name}_{feature}_{idx}")
                    for idx in range(self.vector_size)
                ]
        self.set_used_features()

    def transform(self, x: pd.DataFrame):
        self._check_pretrained_loaded_vectorizer()

        embeddings_list = []
        columns_list = []

        if self.concat_text_features:
            concat_text_features_series = (
                x[self.text_features].astype(str).agg(" ".join, axis=1)
            )
            columns_list = self.feature_columns["text"]
            embeddings_list = [
                np.array(
                    [self._get_vector(text) for text in concat_text_features_series]
                )
            ]
        else:
            for feature in self.text_features:
                columns = self.feature_columns[feature]
                glove_matrix = np.array([self._get_vector(text) for text in x[feature]])
                embeddings_list.append(glove_matrix)
                columns_list.extend(columns)

        embeddings_df = pd.DataFrame(
            data=hstack(embeddings_list), columns=columns_list, index=x.index
        )
        return embeddings_df