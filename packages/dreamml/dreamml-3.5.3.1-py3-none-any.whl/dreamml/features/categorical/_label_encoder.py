from copy import deepcopy
import pandas as pd
from sklearn.preprocessing import LabelEncoder


class DmlLabelEncoder:
    def __init__(self):
        self.encoder = LabelEncoder()

    def fit(self, data: pd.DataFrame, feature: str):
        self.encoder = self.encoder.fit(data[feature])
        return self

    def transform(self, data: pd.DataFrame, feature: str):
        x_transformed = deepcopy(data)
        x_transformed[feature] = self.encoder.transform(x_transformed[feature])
        return x_transformed

    def inverse_transform(self, data: pd.DataFrame, feature: str):
        x_transformed = deepcopy(data)
        if feature in x_transformed.columns:
            x_transformed[feature] = self.encoder.inverse_transform(
                x_transformed[feature]
            )
        return x_transformed