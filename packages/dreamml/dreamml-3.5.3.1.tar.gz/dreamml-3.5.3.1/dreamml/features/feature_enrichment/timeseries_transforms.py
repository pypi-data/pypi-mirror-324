"""
Модуль с реализацией feature transform for timeseries
"""

import pandas as pd
from pathlib import Path
from datetime import timedelta
from pandas import DataFrame
from typing import List, Union, Tuple
from statsmodels.tsa.seasonal import seasonal_decompose
from dreamml.features.feature_enrichment.get_production_calendar_features import (
    RusProductionCalendar,
)


CALENDAR_PATH = (
    Path(__file__).parent.parent.parent
    / "references/production_calendars_2020_2024.json"
)
ALLOWED_DATETIME_TYPES = [
    "hour",
    "minute",
    "second",
    "day",
    "month",
    "year",
    "day_of_week",
    "days_in_month",
    "quarter",
    "week_of_year",
    "is_weekend",
    "season",
    "is_holiday",
    "is_pre_holiday",
    "is_pre_pre_holiday",
]


def transform_time_column_to_datetime(data: DataFrame, column_name: str, format: str):
    """Изменение типа столбца на datetime."""
    assert column_name in data.columns, f"Столцба {column_name} нет в датафрейме"
    try:
        data[column_name] = pd.to_datetime(data[column_name], format=format)
    except ValueError:
        raise Exception(f"column: {column_name}. Указан неверный столбец или формат")
    return data


class BaseTimeSeriesTransform:
    """
    Базовый класс для трансформации фичей.
    """

    def __init__(self, in_columns: Union[str, List[str]], **kwargs):
        self.in_columns = (
            [in_columns] if not isinstance(in_columns, List) else in_columns
        )
        self.types = kwargs.get("types", [])
        self.format = kwargs.get("format", "%Y-%m-%d")
        self.window = kwargs.get("window", 3)
        self.num_components = kwargs.get("num_components", 1)
        self.period = kwargs.get("period", 1)
        self.model_type = kwargs.get("model_type", "additive")
        self.lags = kwargs.get("lags", [1])
        if self.lags == [] or self.lags is None:
            raise ValueError("lags should not be empty")

    def transform(
        self,
        data: DataFrame,
        unique_groups: List[str],
        group_column: str,
        horizon: int,
        used_features: List[str] = None,
        pretransformed_columns: List[str] = [],
    ) -> Tuple[List[str], DataFrame]:
        raise NotImplementedError("Subclasses must implement the transform method")


class RusHolidayTransform:
    """
    Добавляет столбец, содержащий атрибут даты.

    time_column: столбец содержащий даты
    types: новые фичи
    """

    def __init__(
        self,
        in_column: str = "timestamp",
        types: List[str] = None,
        out_column: str = None,
    ):
        self.time_column = in_column
        self.out_column = self.time_column if out_column is None else out_column
        self.types = (
            types
            if types is not None
            else ["is_weekend", "is_holiday", "is_pre_holiday", "is_pre_pre_holiday"]
        )
        self.production_calendar_path = CALENDAR_PATH
        self.dreamml_calendar = RusProductionCalendar(self.production_calendar_path)
        self.format = "%Y-%m-%d"

        if isinstance(self.time_column, list):
            raise ValueError(f"Expecting type str not List")

        for type in self.types:
            if type not in ALLOWED_DATETIME_TYPES:
                raise ValueError(
                    f"Тип {type} отсутствует в списке преобразований:\n{ALLOWED_DATETIME_TYPES}"
                )

    def transform(
        self,
        data: DataFrame,
    ) -> Tuple[List[str], DataFrame]:

        added_features = []
        data = transform_time_column_to_datetime(data, self.time_column, self.format)

        for date_type in self.types:
            added_feature_name = f"{self.out_column}_{date_type}"

            if date_type == "second":
                data[added_feature_name] = data[self.time_column].dt.second
            elif date_type == "minute":
                data[added_feature_name] = data[self.time_column].dt.minute
            elif date_type == "hour":
                data[added_feature_name] = data[self.time_column].dt.hour
            elif date_type == "day":
                data[added_feature_name] = data[self.time_column].dt.day
            elif date_type == "month":
                data[added_feature_name] = data[self.time_column].dt.month
            elif date_type == "year":
                data[added_feature_name] = data[self.time_column].dt.year
            elif date_type == "day_of_week":
                data[added_feature_name] = data[self.time_column].dt.day_of_week
            elif date_type == "days_in_month":
                data[added_feature_name] = data[self.time_column].dt.days_in_month
            elif date_type == "quarter":
                data[added_feature_name] = data[self.time_column].dt.quarter
            elif date_type == "week_of_year":
                data[added_feature_name] = data[self.time_column].dt.isocalendar().week
            elif date_type == "season":
                data[added_feature_name] = data[self.time_column].dt.month.apply(
                    lambda x: (
                        0
                        if x in [12, 1, 2]
                        else (  # Зима
                            1
                            if x in [3, 4, 5]
                            else (  # Весна
                                2
                                if x in [6, 7, 8]
                                else 3 if x in [9, 10, 11] else None  # Лето
                            )
                        )  # Зима
                    )
                )
            elif date_type == "is_weekend":
                data[added_feature_name] = data[self.time_column].apply(
                    self.dreamml_calendar.check_date_is_weekend
                )
            elif date_type == "is_holiday":
                data[added_feature_name] = data[self.time_column].apply(
                    self.dreamml_calendar.check_date_is_holiday
                )
            elif date_type == "is_pre_holiday":
                holiday_series = data[f"{self.out_column}_is_holiday"]
                holiday_series = pd.Series(
                    list(holiday_series), index=list(data[self.time_column])
                )
                holiday_list = list(holiday_series[holiday_series == 1].index)
                pre_holiday_list = [date - timedelta(days=1) for date in holiday_list]
                data[added_feature_name] = (
                    data[self.time_column].isin(pre_holiday_list).astype(int)
                )
            elif date_type == "is_pre_pre_holiday":
                holiday_series = data[f"{self.out_column}_is_holiday"]
                holiday_series = pd.Series(
                    list(holiday_series), index=list(data[self.time_column])
                )
                holiday_list = list(holiday_series[holiday_series == 1].index)
                pre_pre_holiday_list = [
                    date - timedelta(days=2) for date in holiday_list
                ]
                data[added_feature_name] = (
                    data[self.time_column].isin(pre_pre_holiday_list).astype(int)
                )

            added_features.append(added_feature_name)

            try:
                data[added_feature_name] = data[added_feature_name].astype(int)
            except:
                continue

        return added_features, data


class LagTransform(BaseTimeSeriesTransform):
    """
    Добавляет столбец, содержащий лаговые значения временного ряда.
    """

    def __init__(self, in_columns: Union[List[str], str], **kwargs):
        super().__init__(in_columns, **kwargs)

    def transform(
        self,
        data: DataFrame,
        unique_groups: List[str],
        group_column: str,
        horizon: int,
        used_features: List[str] = None,
        pretransformed_columns: List[str] = [],
    ) -> Tuple[List[str], DataFrame]:
        added_features = []

        for group in unique_groups:
            mask = data[group_column] == group
            grouped_data = data.loc[mask, :]

            shift_columns = [
                f"{column}_lag_{lag}"
                for column in self.in_columns
                for lag in self.lags
                if f"{column}_lag_{lag}" not in pretransformed_columns
            ]

            for lag_column_name in shift_columns:
                if used_features is None or lag_column_name in used_features:
                    added_features.append(lag_column_name)

                    column, lag = lag_column_name.split("_lag_")
                    lag = int(lag)

                    data.loc[mask, lag_column_name] = grouped_data.loc[:, column].shift(
                        lag + horizon
                    )
                    try:
                        data.loc[mask, lag_column_name] = data.loc[
                            mask, lag_column_name
                        ].astype(float)
                    except:  # FIXME
                        continue

        return added_features, data


class MeanTransform(BaseTimeSeriesTransform):
    """
    Добавляет столбец, содержащий скользящее среднее для временного ряда.
    """

    def __init__(self, in_columns: Union[List[str], str], **kwargs):
        super().__init__(in_columns, **kwargs)

    def transform(
        self,
        data: DataFrame,
        unique_groups: List[str],
        group_column: str,
        horizon: int,
        used_features: List[str] = None,
        pretransformed_columns: List[str] = [],
    ) -> Tuple[List[str], DataFrame]:
        added_features = []

        for group in unique_groups:
            mask = data[group_column] == group
            grouped_data = data[mask]

            shift_columns = [
                f"{column}_mean_window_{self.window}_lag_{lag}"
                for column in self.in_columns
                for lag in self.lags
                if f"{column}_mean_window_{self.window}_lag_{lag}"
                not in pretransformed_columns
            ]

            for mean_column_name in shift_columns:
                if used_features is None or mean_column_name in used_features:
                    added_features.append(mean_column_name)

                    column_name, lag = mean_column_name.split("_lag_")
                    column, mean_window = column_name.split("_mean_window_")
                    lag = int(lag)

                    data.loc[mask, mean_column_name] = (
                        grouped_data.loc[:, column]
                        .shift(horizon)
                        .rolling(window=self.window)
                        .mean()
                        .shift(lag)
                    )

                    try:
                        data.loc[mask, mean_column_name] = data.loc[
                            mask, mean_column_name
                        ].astype(float)
                    except:
                        continue

        return added_features, data


class DifferenceTransform(BaseTimeSeriesTransform):
    """
    Добавляет столбец, содержащий разности между последовательными
    значениями временного ряда.
    """

    def __init__(self, in_columns: Union[str, List[str]], **kwargs):
        super().__init__(in_columns, **kwargs)

    def transform(
        self,
        data: DataFrame,
        unique_groups: List[str],
        group_column: str,
        horizon: int,
        used_features: List[str] = None,
        pretransformed_columns: List[str] = [],
    ) -> Tuple[List[str], DataFrame]:
        added_features = []

        for group in unique_groups:
            mask = data[group_column] == group
            grouped_data = data[mask]

            shift_columns = [
                f"{column}_diff_lag_{lag}"
                for column in self.in_columns
                for lag in self.lags
                if f"{column}_diff_lag_{lag}" not in pretransformed_columns
            ]

            for diff_column_name in shift_columns:
                if used_features is None or diff_column_name in used_features:
                    added_features.append(diff_column_name)

                    column, lag = diff_column_name.split("_diff_lag_")
                    lag = int(lag)

                    data.loc[mask, diff_column_name] = (
                        grouped_data.loc[:, column]
                        .shift(horizon)
                        .diff(self.period)
                        .shift(lag)
                    )

                    try:
                        data.loc[mask, diff_column_name] = data.loc[
                            mask, diff_column_name
                        ].astype(float)
                    except:
                        continue
        return added_features, data


class ExponentialWeightedMeanTransform(BaseTimeSeriesTransform):
    """
    Рассчитывает экспоненциально взвешенное скользящее среднее для временного ряда.
    """

    def __init__(self, in_columns: Union[str, List[str]], alpha: float, **kwargs):
        super().__init__(in_columns, **kwargs)
        self.alpha = alpha
        self.lags = kwargs.get("lags", [0])

    def transform(
        self,
        data: DataFrame,
        unique_groups: List[str],
        group_column: str,
        horizon: int,
        used_features: List[str] = None,
        pretransformed_columns: List[str] = [],
    ) -> Tuple[List[str], DataFrame]:
        added_features = []

        for group in unique_groups:
            mask = data[group_column] == group
            grouped_data = data[mask]

            shift_columns = [
                f"{column}_ewm_alpha_{self.alpha}_lag_{lag}"
                for column in self.in_columns
                for lag in self.lags
                if f"{column}_ewm_alpha_{self.alpha}_lag_{lag}"
                not in pretransformed_columns
            ]

            for ewm_column_name in shift_columns:
                if used_features is None or ewm_column_name in used_features:
                    added_features.append(ewm_column_name)

                    column_name, lag = ewm_column_name.split("_lag_")
                    column, ewm_alpha = column_name.split("_ewm_alpha_")
                    lag = int(lag)

                    data.loc[mask, ewm_column_name] = (
                        grouped_data.loc[:, column]
                        .shift(horizon)
                        .ewm(alpha=self.alpha)
                        .mean()
                        .shift(lag)
                    )

                    try:
                        data.loc[mask, ewm_column_name] = data.loc[
                            mask, ewm_column_name
                        ].astype(float)
                    except:
                        continue

        return added_features, data


class RollingStdTransform(BaseTimeSeriesTransform):
    """
    RollingStdTransform: Рассчитывает стандартное отклонение с использованием окна для временного ряда.
    """

    def __init__(self, in_columns: Union[List[str], str], **kwargs):
        super().__init__(in_columns, **kwargs)

    def transform(
        self,
        data: DataFrame,
        unique_groups: List[str],
        group_column: str,
        horizon: int,
        used_features: List[str] = None,
        pretransformed_columns: List[str] = [],
    ) -> Tuple[List[str], DataFrame]:
        added_features = []

        for group in unique_groups:
            mask = data[group_column] == group
            grouped_data = data[mask]

            shift_columns = [
                f"{column}_rolling_std_window_{self.window}_lag_{lag}"
                for column in self.in_columns
                for lag in self.lags
                if f"{column}_rolling_std_window_{self.window}_lag_{lag}"
                not in pretransformed_columns
            ]

            for std_column_name in shift_columns:
                if used_features is None or std_column_name in used_features:
                    added_features.append(std_column_name)

                    column_name, lag = std_column_name.split("_lag_")
                    column, rolling_std_window = column_name.split(
                        "_rolling_std_window_"
                    )
                    lag = int(lag)

                    data.loc[mask, std_column_name] = (
                        grouped_data.loc[:, column]
                        .shift(horizon)
                        .rolling(window=self.window)
                        .std()
                        .shift(lag)
                    )

                    try:
                        data.loc[mask, std_column_name] = data.loc[
                            mask, std_column_name
                        ].astype(float)
                    except:
                        continue

        return added_features, data


class DecomposeTransform(BaseTimeSeriesTransform):
    """
    DecomposeTransform: Разложение временного ряда на 3 компоненты: тренд, сезонность и шум.
    """

    def __init__(self, in_columns: str, **kwargs):
        super().__init__(in_columns, **kwargs)

    def transform(
        self,
        data: DataFrame,
        unique_groups: List[str],
        group_column: str,
        horizon: int,
        used_features: List[str] = None,
        pretransformed_columns: List[str] = [],
    ) -> Tuple[List[str], DataFrame]:
        added_features = []

        for group in unique_groups:
            mask = data[group_column] == group
            grouped_data = data[mask]

            shift_columns_trend = [
                f"{column}_trend_period_{self.period}_lag_{lag}"
                for column in self.in_columns
                for lag in self.lags
                if f"{column}_trend_period_{self.period}_lag_{lag}"
                not in pretransformed_columns
            ]
            shift_columns_seasonality = [
                f"{column}_seasonality_period_{self.period}_lag_{lag}"
                for column in self.in_columns
                for lag in self.lags
                if f"{column}_seasonality_period_{self.period}_lag_{lag}"
                not in pretransformed_columns
            ]
            shift_columns_residual = [
                f"{column}_residual_period_{self.period}_lag_{lag}"
                for column in self.in_columns
                for lag in self.lags
                if f"{column}_residual_period_{self.period}_lag_{lag}"
                not in pretransformed_columns
            ]

            for idx, trend_column_name in enumerate(shift_columns_trend):
                seasonality_column_name = shift_columns_seasonality[idx]
                residual_column_name = shift_columns_residual[idx]
                if used_features is None or trend_column_name in used_features:
                    added_features.append(trend_column_name)
                    added_features.append(seasonality_column_name)
                    added_features.append(residual_column_name)

                    column_name, lag = trend_column_name.split("_lag_")
                    column, trend_period = column_name.split("_trend_period_")
                    lag = int(lag)

                    decomposition = seasonal_decompose(
                        grouped_data.loc[:, column].fillna(
                            grouped_data.loc[:, column].median()
                        ),
                        period=self.period,
                        model=self.model_type,
                    )

                    grouped_data.loc[:, trend_column_name] = decomposition.trend
                    grouped_data.loc[:, seasonality_column_name] = (
                        decomposition.seasonal
                    )
                    grouped_data.loc[:, residual_column_name] = decomposition.resid
                    data.loc[mask, trend_column_name] = grouped_data.loc[
                        :, trend_column_name
                    ].shift(lag + horizon)
                    data.loc[mask, seasonality_column_name] = grouped_data.loc[
                        :, seasonality_column_name
                    ].shift(lag + horizon)
                    data.loc[mask, residual_column_name] = grouped_data.loc[
                        :, residual_column_name
                    ].shift(lag + horizon)

                    try:
                        data.loc[mask, trend_column_name] = data.loc[
                            mask, trend_column_name
                        ].astype(float)
                        data.loc[mask, seasonality_column_name] = data.loc[
                            mask, seasonality_column_name
                        ].astype(float)
                        data.loc[mask, residual_column_name] = data.loc[
                            mask, residual_column_name
                        ].astype(float)
                    except:
                        continue

        return added_features, data