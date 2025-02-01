import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr
from sklearn.metrics import mean_absolute_error, r2_score

from dreamml.modeling.metrics.metrics_mapping import metrics_mapping
from dreamml.modeling.metrics.utils import calculate_quantile_bins
from dreamml.modeling.models.estimators import BoostingBaseModel
from dreamml.utils.confidence_interval import calculate_conf_interval


class CalculateDataStatisticsAMTS:

    def __init__(self, encoder, config: dict) -> None:
        self.transformer = encoder
        # self.log_transformer = log_transformer
        self.categorical = self.transformer.cat_features
        self.config = config

    def _preprocessing_data(self, **eval_sets):
        """
        Данные об удалении выбросов по целевой переменной
        """

        msg = "Удалены выбросы по целевой переменной" "({} и {} перцентили).".format(
            self.config["min_percentile"], self.config["max_percentile"]
        )
        values = [
            msg if sample in ["train", "valid", "test2"] else "-"
            for sample in eval_sets
        ]
        return values

    def _calculate_samples_stats(self, log_scale: bool, prefix: str = "", **eval_sets):

        result = {}
        for data_name in eval_sets:
            data, target = eval_sets[data_name]

            if log_scale:
                target = self.log_transformer.inverse_transform(target)

            result[data_name] = [
                len(data),
                np.mean(target),
                np.std(target),
                np.min(target),
                np.percentile(target, 25),
                np.percentile(target, 50),
                np.percentile(target, 75),
                np.max(target),
            ]
        result = pd.DataFrame(result).T.reset_index()
        result.columns = [
            "Выборка",
            "# наблюдений",
            f"{prefix}target AVG-value",
            f"{prefix}target STD-value",
            f"{prefix}target MIN-value",
            f"{prefix}target 25% percentile",
            f"{prefix}target 50% percentile",
            f"{prefix}target 75% percentile",
            f"{prefix}target MAX-value",
        ]
        return result.fillna(0)

    def _calculate_variables_stats(self, **eval_sets) -> pd.DataFrame:
        sample_name = next(iter(eval_sets))
        data, _ = eval_sets[sample_name]

        result = data.describe().T.reset_index()
        result.columns = [
            "Variable name",
            "Number of filled value",
            "AVG-value",
            "STD-value",
            "MIN-value",
            "25% percentile-value",
            "50% percentile-value",
            "75% percentile-value",
            "MAX-value",
        ]
        if self.categorical:
            mask = result["Variable name"].isin(self.categorical)
            features = [
                "AVG-value",
                "STD-value",
                "MIN-value",
                "25% percentile-value",
                "50% percentile-value",
                "75% percentile-value",
                "MAX-value",
            ]
            result.loc[mask, features] = "."

        # print(result)

        return result.fillna(0)

    def _calculate_variables_types_stats(self) -> pd.DataFrame:
        target_name = self.config["target_name"]
        log_target = self.config.get("log_target", False)
        target_name = f"log({target_name})" if log_target else target_name

        stats = pd.DataFrame(
            {
                "Целевая переменная": [self.config["target_name"]],
                "loss_function": self.config["loss_function"],
                "eval_metric": self.config["eval_metric"],
                "# категорий": [len(self.transformer.cat_features)],
                # "# непрерывных": [self.gini.shape[0]],
            }
        )

        return stats.fillna(0)

    def transform(self, **eval_sets) -> None:
        # if self.log_transformer.fitted:
        #     res = (
        #         self._calculate_samples_stats(log_scale=True, prefix="", **eval_sets),
        #         self._calculate_samples_stats(
        #             log_scale=False, prefix="log-", **eval_sets
        #         ),
        #     )
        #     result = (
        #         *res,
        #         self._calculate_variables_types_stats(),
        #         self._calculate_variables_stats(**eval_sets),
        #     )
        # else:
        #     result = (
        #         self._calculate_samples_stats(log_scale=False, **eval_sets),
        #         self._calculate_variables_types_stats(),
        #         self._calculate_variables_stats(**eval_sets),
        #     )

        result = (
            self._calculate_samples_stats(log_scale=False, **eval_sets),
            self._calculate_variables_types_stats(),
            self._calculate_variables_stats(**eval_sets),
        )

        return result