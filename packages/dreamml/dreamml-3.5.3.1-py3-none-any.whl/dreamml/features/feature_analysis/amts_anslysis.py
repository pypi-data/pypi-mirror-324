import numpy as np
from statsmodels.tsa.stattools import adfuller, kpss, acf
from statsmodels.tsa.seasonal import STL
from scipy.stats import levene
from dreamml.data._dataset import DataSet


class AMTSAnalysisResult:
    def __init__(self):
        self.kpss_test_dict = {}
        self.adfuller_test_dict = {}
        self.stl_dict = {}
        self.levene_dict = {}
        self.period_dict = {}


class AMTSAnalysis:
    def __init__(self, data_storage: DataSet):
        self.data_storage: DataSet = data_storage
        self.time_column = data_storage.time_column
        self.target_name = data_storage.target_name
        self.split_by_group = data_storage.split_by_group
        self.group_column = data_storage.group_column
        amts_data = self.data_storage.get_eval_set()
        self.df = amts_data["train"][0]
        self.df[self.data_storage.target_name] = amts_data["train"][1]

        self.p_value_th = 0.05
        self.analysis_result = AMTSAnalysisResult()

    def analysis(self):
        self.kpss_test(self)
        self.adfuller_test(self)
        self.calculate_period(self)
        self.stl_decomposition(self)
        self.levene_test(self)
        pass

    @staticmethod
    def kpss_test(self):
        """
        Тест KPSS на стационарность
        """
        if self.split_by_group:
            for group_name, df_group in self.df.groupby(self.data_storage.group_column):
                try:
                    result = kpss(df_group[self.target_name])
                except Exception as e:
                    pass
                _dict = {
                    f"segment_{group_name}": {
                        "test": "Тест KPSS на стационарность",
                        "test_statistics": None,
                        "p_value": None,
                        "output": None,
                    }
                }
                _dict[f"segment_{group_name}"]["test_statistics"] = result[0]
                _dict[f"segment_{group_name}"]["p_value"] = result[1]
                _dict[f"segment_{group_name}"]["output"] = (
                    "stationary" if result[1] > self.p_value_th else "nonstationary"
                )
                self.analysis_result.kpss_test_dict.update(_dict)
        else:
            result = kpss(self.df[self.target_name])
            _dict = {
                f"segment_0": {
                    "test": "Тест KPSS на стационарность",
                    "test_statistics": result[0],
                    "p_value": result[1],
                    "output": (
                        "stationary" if result[1] > self.p_value_th else "nonstationary"
                    ),
                }
            }
            self.analysis_result.kpss_test_dict.update(_dict)

    @staticmethod
    def adfuller_test(self):
        """
        Тест Дики-Фуллера на стационарность
        """
        if self.split_by_group:
            for group_name, df_group in self.df.groupby(self.data_storage.group_column):
                try:
                    result = adfuller(df_group[self.target_name])
                except Exception as e:
                    pass
                _dict = {
                    f"segment_{group_name}": {
                        "test": "Тест Дики-Фуллера на стационарность",
                        "test_statistics": None,
                        "p_value": None,
                        "output": None,
                    }
                }
                _dict[f"segment_{group_name}"]["test_statistics"] = result[0]
                _dict[f"segment_{group_name}"]["p_value"] = result[1]
                _dict[f"segment_{group_name}"]["output"] = (
                    "stationary" if result[1] > self.p_value_th else "nonstationary"
                )
                self.analysis_result.adfuller_test_dict.update(_dict)
        else:
            result = adfuller(self.df[self.target_name])
            _dict = {
                f"segment_0": {
                    "test": "Тест Дики-Фуллера на стационарность",
                    "test_statistics": result[0],
                    "p_value": result[1],
                    "output": (
                        "stationary" if result[1] > self.p_value_th else "nonstationary"
                    ),
                }
            }
            self.analysis_result.adfuller_test_dict.update(_dict)

    @staticmethod
    def stl_decomposition(self):
        """
        STL разложение
        """
        if self.data_storage.split_by_group:
            for group_name, df_group in self.df.groupby(self.data_storage.group_column):
                _dict = {
                    f"segment_{group_name}": {
                        "timeseries": None,
                        "target": None,
                        "trend": None,
                        "seasonal": None,
                        "resid": None,
                    }
                }
                stl_result = STL(
                    df_group[self.data_storage.target_name],
                    period=self.analysis_result.period_dict[f"segment_{group_name}"][
                        "lag"
                    ],
                ).fit()
                _dict[f"segment_{group_name}"]["timeseries"] = np.array(df_group["ds"])
                _dict[f"segment_{group_name}"]["target"] = np.array(
                    df_group[self.data_storage.target_name]
                )
                _dict[f"segment_{group_name}"]["trend"] = np.array(stl_result.trend)
                _dict[f"segment_{group_name}"]["seasonal"] = np.array(
                    stl_result.seasonal
                )
                _dict[f"segment_{group_name}"]["resid"] = np.array(stl_result.resid)
                self.analysis_result.stl_dict.update(_dict)
        else:
            stl_result = STL(
                self.df[self.target_name],
                period=self.analysis_result.period_dict["segment_0"]["lag"],
            ).fit()

            _dict = {
                f"segment_0": {
                    "timeseries": np.array(self.df["ds"]),
                    "target": np.array(self.df[self.data_storage.target_name]),
                    "trend": np.array(stl_result.trend),
                    "seasonal": np.array(stl_result.seasonal),
                    "resid": np.array(stl_result.resid),
                }
            }
            self.analysis_result.stl_dict.update(_dict)

    @staticmethod
    def levene_test(self):
        """
        Тест Левена на однородность дисперсии остатков
        """
        if self.data_storage.split_by_group:
            for group_name, df_group in self.df.groupby(self.data_storage.group_column):
                n = len(self.analysis_result.stl_dict[f"segment_{group_name}"]["resid"])
                group_1 = self.analysis_result.stl_dict[f"segment_{group_name}"][
                    "resid"
                ][: int(n * 0.2)]
                group_2 = self.analysis_result.stl_dict[f"segment_{group_name}"][
                    "resid"
                ][int(n * 0.2) : int(n * 0.4)]
                group_3 = self.analysis_result.stl_dict[f"segment_{group_name}"][
                    "resid"
                ][int(n * 0.4) : int(n * 0.6)]
                group_4 = self.analysis_result.stl_dict[f"segment_{group_name}"][
                    "resid"
                ][int(n * 0.6) : int(n * 0.8)]
                group_5 = self.analysis_result.stl_dict[f"segment_{group_name}"][
                    "resid"
                ][int(n * 0.8) : int(n * 1)]

                test_statistics, p_value = levene(
                    group_1, group_2, group_3, group_4, group_5
                )
                _dict = {
                    f"segment_{group_name}": {
                        "test": "Тест Левена на однородность дисперсии остатков",
                        "test_statistics": None,
                        "p_value": None,
                        "output": None,
                    }
                }
                _dict[f"segment_{group_name}"]["test_statistics"] = test_statistics
                _dict[f"segment_{group_name}"]["p_value"] = p_value
                _dict[f"segment_{group_name}"]["output"] = (
                    "heteroscedasticity"
                    if p_value > self.p_value_th
                    else "homoscedasticity"
                )
                self.analysis_result.levene_dict.update(_dict)

        else:
            n = len(self.analysis_result.stl_dict["segment_0"]["resid"])
            group_1 = self.analysis_result.stl_dict["segment_0"]["resid"][
                : int(n * 0.2)
            ]
            group_2 = self.analysis_result.stl_dict["segment_0"]["resid"][
                int(n * 0.2) : int(n * 0.4)
            ]
            group_3 = self.analysis_result.stl_dict["segment_0"]["resid"][
                int(n * 0.4) : int(n * 0.6)
            ]
            group_4 = self.analysis_result.stl_dict["segment_0"]["resid"][
                int(n * 0.6) : int(n * 0.8)
            ]
            group_5 = self.analysis_result.stl_dict["segment_0"]["resid"][
                int(n * 0.8) : int(n * 1)
            ]

            test_statistics, p_value = levene(
                group_1, group_2, group_3, group_4, group_5
            )
            _dict = {
                f"segment_0": {
                    "test": "Тест Левена на однородность дисперсии остатков",
                    "test_statistics": test_statistics,
                    "p_value": p_value,
                    "output": (
                        "heteroscedasticity"
                        if p_value > self.p_value_th
                        else "homoscedasticity"
                    ),
                }
            }
            self.analysis_result.levene_dict.update(_dict)

    @staticmethod
    def calculate_period(self):
        """
        Вычисление периодичности временного рядя
        """
        if self.split_by_group:
            for group_name, df_group in self.df.groupby(self.data_storage.group_column):
                if len(df_group[self.target_name]) > 50:
                    acf_result = acf(df_group[self.target_name], nlags=50)
                    max_lag, max_acf = 0, 0
                    for i in range(3, 50):
                        acf_sum, count = 0, 0
                        for j in range(i, 50, i):
                            count += 1
                            acf_sum += acf_result[j]
                            if max_acf < (acf_sum / count):
                                max_lag, max_acf = i, (acf_sum / count)
                else:
                    max_lag = 5
                    max_acf = 5

                _dict = {
                    f"segment_{group_name}": {
                        "test:": "Lag с наибольшей автокорреляцией",
                        "lag": None,
                        "max_acf": None,
                    }
                }
                _dict[f"segment_{group_name}"]["lag"] = max_lag
                _dict[f"segment_{group_name}"]["max_acf"] = max_acf
                self.analysis_result.period_dict.update(_dict)
        else:
            if len(self.df[self.target_name]) > 50:
                acf_result = acf(self.df[self.target_name], nlags=50)
                max_lag, max_acf = 0, 0
                for i in range(3, 50):
                    acf_sum, count = 0, 0
                    for j in range(i, 50, i):
                        count += 1
                        acf_sum += acf_result[j]
                        if max_acf < (acf_sum / count):
                            max_lag, max_acf = i, (acf_sum / count)
            else:
                max_lag = 5
                max_acf = 5

            _dict = {
                f"segment_0": {
                    "test:": "Lag с наибольшей автокорреляцией",
                    "lag": max_lag,
                    "max_acf": max_acf,
                }
            }
            self.analysis_result.period_dict.update(_dict)