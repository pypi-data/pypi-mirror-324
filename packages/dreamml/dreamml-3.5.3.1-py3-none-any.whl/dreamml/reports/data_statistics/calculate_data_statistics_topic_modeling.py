from typing import Optional, Tuple
import numpy as np
import pandas as pd

from dreamml.logging import get_logger

_logger = get_logger(__name__)


class CalculateDataStatistics:

    def __init__(
        self, transformer, features: pd.Series, config: dict, task: str
    ) -> None:
        self.features = features
        self.transformer = transformer
        self.categorical = self.transformer.cat_features
        self.config = config
        self.task = task

    def _calculate_samples_stats(self, **eval_sets):
        results = []
        for key, sample in eval_sets.items():

            item = (
                sample[0][self.config["text_features"][0]]
                if "bertopic" in self.config["fitted_model"]
                else sample[0][self.config["text_features_preprocessed"][0]]
            )

            df = pd.DataFrame(
                {
                    f"{key}": ["True"],
                    "length": [len(item)],
                    "max_words": [item.apply(lambda x: len(x.split())).max()],
                    "min_words": [item.apply(lambda x: len(x.split())).min()],
                    "mean_words": [item.apply(lambda x: len(x.split())).mean()],
                }
            )
            results.append(df)
        return results

    def transform(self, **eval_sets) -> Tuple[Optional[pd.DataFrame]]:
        return self._calculate_samples_stats(**eval_sets)