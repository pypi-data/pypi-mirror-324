import pandas as pd
import numpy as np
from sklearn.preprocessing import OrdinalEncoder


class DmlOrdinalEncoder:
    def __init__(self):
        self.encoder = OrdinalEncoder(dtype=np.integer)

    def fit(self, data: pd.DataFrame, feature: str):
        self.encoder = OrdinalEncoder().fit(data[[feature]])
        return self

    def transform(self, data: pd.DataFrame, feature: str):
        data[feature] = self.encoder.transform(data[[feature]])
        data[feature] = data[feature].astype(np.integer)
        return data

    def inverse_transform(self, data: pd.DataFrame, feature: str):
        if feature in data.columns:
            data[feature] = self.encoder.inverse_transform(data[[feature]])
        return data