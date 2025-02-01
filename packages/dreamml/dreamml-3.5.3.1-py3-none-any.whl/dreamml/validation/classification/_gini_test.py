import numpy as np
import pandas as pd

class GiniTest:
    def __init__(self, estimator, metric):
        self.estimator = estimator
        self.metric = metric

    def transform(self, **data):

        result_dict = {}

        for sample in data.keys():
            y_true = data[sample][1]
            y_pred = self.estimator.transform(data[sample][0])
            metric = self.metric(y_true, y_pred)

            traffic_light = "red"
            if metric >= 0.4:
                traffic_light = "yellow"
            if metric >= 0.6:
                traffic_light = "green"
            result_dict.update({sample: [metric, traffic_light]})

        gini_degradation = (result_dict["train"][0] - result_dict["test"][0]) / result_dict["test"][0]
        traffic_light_gini_degradation = "red"
        if gini_degradation <= 0.3:
            traffic_light_gini_degradation = "yellow"
        if gini_degradation <= 0.1:
            traffic_light_gini_degradation = "green"
        result_dict.update({"gini_degradation": [gini_degradation, traffic_light_gini_degradation]})

        result = pd.DataFrame(result_dict)
        return result, traffic_light_gini_degradation