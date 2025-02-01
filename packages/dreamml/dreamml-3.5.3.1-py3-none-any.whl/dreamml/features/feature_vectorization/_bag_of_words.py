from typing import List, Optional
import pandas as pd
from gensim.corpora.dictionary import Dictionary
from nltk import word_tokenize
from dreamml.features.feature_vectorization._base import BaseVectorization


class BowVectorization(BaseVectorization):
    name = "bow"

    def __init__(self, text_features: List[str], **kwargs):
        super().__init__(text_features, "bow", **kwargs)
        self.vectorizers = {feature: None for feature in self.text_features}

    def fit(
        self,
        x: pd.DataFrame,
        y: pd.Series,
        x_val: Optional[pd.DataFrame] = None,
        y_val: Optional[pd.Series] = None,
    ):
        self.set_used_features()

    def transform(self, x: pd.DataFrame, _: bool = False):
        bow_corpus_dict = dict()
        for feature in self.text_features:
            corpus = [word_tokenize(text) for text in x[feature]]
            dictionary = Dictionary(corpus)
            bow_corpus = [dictionary.doc2bow(doc) for doc in corpus]

            bow_corpus_dict[feature] = {"dict": dictionary, "bow_corpus": bow_corpus}
        return bow_corpus_dict