from scipy import stats
import pandas as pd

class KSTest:
    def __init__(self, estimator):
        self.estimator = estimator

    def transform(self, **data):
        result_dict = {}

        for sample in data.keys():
            y_true = data[sample][1].values
            y_pred = self.estimator.transform(data[sample][0])

            y_pred_pos = [y_pred[i] for i in range(len(y_true)) if y_true[i] == 1]
            y_pred_neg = [y_pred[i] for i in range(len(y_true)) if y_true[i] == 0]
            ks_stat, p_value = stats.ks_2samp(y_pred_pos, y_pred_neg)

            traffic_light = "red"
            if 0.01 <= p_value <= 0.05:
                traffic_light = "yellow"
            if p_value < 0.01:
                traffic_light = "green"
            result_dict.update({sample: [ks_stat, traffic_light]})

        result_traffic_light = "green"
        for key, value in result_dict.items():
            if value[1] == "yellow":
                result_traffic_light = "yellow"
            if value[1] == "red":
                result_traffic_light = "red"
                break

        result = pd.DataFrame(result_dict)
        return result, result_traffic_light