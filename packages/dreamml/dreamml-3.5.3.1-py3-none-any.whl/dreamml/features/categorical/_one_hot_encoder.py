import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
import logging


class DmlOneHotEncoder:
    def __init__(self):
        self.encoder = OneHotEncoder(sparse=False, dtype=np.integer)

    def fit(self, data: pd.DataFrame, feature: str):
        self.encoder = self.encoder.fit(data[[feature]])
        return self

    def transform(self, data: pd.DataFrame, feature: str):
        x_transformed = pd.DataFrame(
            data=self.encoder.transform(data[[feature]]),
            columns=self.encoder.get_feature_names_out(),
        )
        data = pd.concat([data, x_transformed], axis=1)
        data.drop(columns=[feature], axis=1, inplace=True)

        return data

    def inverse_transform(self, data: pd.DataFrame, feature: str):
        one_hot_columns = [
            column
            for column in self.encoder.get_feature_names_out()
            if column in data.columns
        ]
        if len(one_hot_columns) == len(self.encoder.get_feature_names_out()):
            data[feature] = self.encoder.inverse_transform(data[one_hot_columns])
            for drop_column in one_hot_columns:
                data.drop(columns=[drop_column], axis=1, inplace=True)
        else:
            missing_columns = list(
                set(one_hot_columns) & set(self.encoder.get_feature_names_out())
            )
            message = f"Columns {missing_columns} not in data for one_hot_encoder inverse_transform."
            logging.info(message)

        return data