from copy import deepcopy
import pandas as pd
from typing import Dict, Tuple


def get_eval_set_with_embeddings(
    vectorizer, eval_set: Dict[str, Tuple[pd.DataFrame, pd.Series]]
):
    for sample_name, (X_sample, y_sample) in eval_set.items():
        embeddings_df = vectorizer.transform(X_sample)
        if vectorizer.name == "bow":
            eval_set[sample_name] = (embeddings_df, y_sample)
            continue
        X_sample = pd.concat([X_sample, embeddings_df], axis=1)
        eval_set[sample_name] = (X_sample, y_sample)
    return eval_set