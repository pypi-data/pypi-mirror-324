import pandas as pd
from sklearn.metrics import mutual_info_score

class CIECTest:
    def __init__(self, estimator):
        self.estimator = estimator

    def transform(self, **data):

        result_dict = {}

        for sample in data.keys():
            y_true = data[sample][1].values
            y_pred_proba = self.estimator.transform(data[sample][0])
            y_pred = [1 if pred >= 0.5 else 0 for pred in y_pred_proba]

            total_entropy = mutual_info_score(y_true, y_pred)
            entropy_y = mutual_info_score(y_true, y_true)
            ciec = (total_entropy / entropy_y)

            traffic_light = "red"
            if 0.4 <= ciec < 0.6:
                traffic_light = "yellow"
            if ciec >= 0.6:
                traffic_light = "green"
            result_dict.update({sample: [ciec, traffic_light]})

        result_traffic_light = "green"
        for key, value in result_dict.items():
            if value[1] == "yellow":
                result_traffic_light = "yellow"
            if value[1] == "red":
                result_traffic_light = "red"
                break

        result = pd.DataFrame(result_dict)
        return result, result_traffic_light