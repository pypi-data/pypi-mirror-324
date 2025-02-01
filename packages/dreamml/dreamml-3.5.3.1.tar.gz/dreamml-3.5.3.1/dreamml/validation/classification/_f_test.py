import pandas as pd

class FTest:
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
            if metric >= 0.6:
                traffic_light = "yellow"
            if metric >= 0.8:
                traffic_light = "green"
            result_dict.update({sample: [metric, traffic_light]})

        result_traffic_light = "green"
        for key, value in result_dict.items():
            if value[1] == "yellow":
                result_traffic_light = "yellow"
            if value[1] == "red":
                result_traffic_light = "red"
                break

        result = pd.DataFrame(result_dict)
        return result, result_traffic_light