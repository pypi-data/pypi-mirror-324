"""
Модуль с реализацией feature enrichment for timeseries
"""

from copy import deepcopy
from typing import Optional, List, Dict
import pandas as pd

from etna.datasets import TSDataset
from etna.transforms import HolidayTransform, LabelEncoderTransform

from dreamml.configs.config_storage import ConfigStorage
from dreamml.features.categorical import CategoricalFeaturesTransformer
from dreamml.features.feature_enrichment.timeseries_transforms import (
    RusHolidayTransform,
)
from dreamml.logging import get_logger


_logger = get_logger(__name__)

DML_TRANSFORMS = [RusHolidayTransform]
ETNA_FORBIDDEN_TRANSFORMS = [
    HolidayTransform
]  # PicklingError when using "Holiday" library


def split_dml_transforms(transforms: List):
    etna_transforms = [
        transform
        for transform in transforms
        if not isinstance(transform, tuple(DML_TRANSFORMS))
        and not isinstance(transform, tuple(ETNA_FORBIDDEN_TRANSFORMS))
    ]
    dml_transforms = [
        transform
        for transform in transforms
        if isinstance(transform, tuple(DML_TRANSFORMS))
    ]
    return etna_transforms, dml_transforms


def get_time_column_frequency(time_column_period: str):
    if time_column_period in ["day", "D"]:
        info = "calendar day frequency"
        freq = "D"
    elif time_column_period in ["week", "W"]:
        info = "weekly frequency"
        freq = "W"
    elif time_column_period in ["month", "M"]:
        info = "monthly frequency"
        freq = "M"
    elif time_column_period in ["quarter", "Q"]:
        info = "quarterly frequency"
        freq = "Q"
    elif time_column_period in ["quarter_start", "QS"]:
        info = "quarter-start frequency"
        freq = "QS"
    elif time_column_period in ["month_start", "MS"]:
        info = "month-start frequency"
        freq = "MS"
    elif time_column_period in ["semi_month", "SM"]:
        info = "semi-month frequency (15th of months)"
        freq = "SM"
    elif time_column_period in ["semi_month_start", "SMS"]:
        info = "semi-month start frequency (15th and start of months)"
        freq = "SMS"
    elif time_column_period in ["year", "Y"]:
        info = "yearly frequency"
        freq = "Y"
    elif time_column_period in ["year_end", "YE"]:
        info = "year-end frequency"
        freq = "YE"
    elif time_column_period in ["year_start", "YS"]:
        info = "year-start frequency"
        freq = "YS"
    elif time_column_period in ["hour", "h"]:
        info = "hourly frequency"
        freq = "H"
    elif time_column_period in ["min", "m", "T"]:
        info = "minutely frequency"
        freq = "min"
    elif time_column_period in ["sec", "s"]:
        info = "secondly frequency"
        freq = "S"
    elif time_column_period in ["millisec", "ms"]:
        info = "milliseconds"
        freq = "ms"
    elif time_column_period in ["microsec", "us"]:
        info = "microseconds"
        freq = "us"
    elif time_column_period in ["nanosec", "ns", "N"]:
        info = "nanoseconds"
        freq = "N"
    # elif time_column_period in ["month_end", "ME"]:  # pandas >= 2.*
    #     info = "month-end frequency"
    #     freq = "ME"
    # elif time_column_period in ["semi_month_end", "SME"]:  # pandas >= 2.*
    #     info = "semi-month end frequency (15th and end of months)"
    #     freq = "SME"
    else:
        info = "nonstandart frequency"
        freq = time_column_period
        debug_msg = f"Частота временного столбца: {freq} не из списка стандартных."
        _logger.debug(debug_msg)

    info_msg = f"Time column frequency: {freq} ({info})."
    _logger.info(info_msg)
    return freq


class TimeSeriesEnrichment:
    """
    Класс входных данных DreamML и их обогащения
    фичами из параметра конфига ts_transforms.
    """

    def __init__(
        self,
        data_dict: dict,
        config: ConfigStorage,
        transformer: Optional[CategoricalFeaturesTransformer] = None,
    ):
        self.config = config
        self.data_dict = data_dict
        self.transformer = transformer
        self.etna_required_columns = ["target", "segment", "timestamp"]
        self.drop_features = config.drop_features
        self.etna_transforms, self.dml_transforms = split_dml_transforms(
            config.ts_transforms
        )
        self.config.ts_transforms = self.dml_transforms
        self.frequency = get_time_column_frequency(config.time_column_period)
        self.known_future = self.config.known_future
        self.horizon = config.horizon
        self.use_etna = self.config.use_etna
        self.dev_data, self.dev_ts, self.exog_data = None, None, None

    def preprocessing_data(self):
        """Метод для предобработки данных."""
        preprocess = PreprocessDataset(self.data_dict, self.config)
        preprocess.transform()
        return preprocess.dev_data, preprocess.exog_data

    def transform(self):
        """Метод запуска пайплайна обогащения фичами."""

        dev_data, self.exog_data = self.preprocessing_data()
        dev_data, self.dev_ts = self._etna_feature_transform(dev_data)
        self.dev_data = self._dml_feature_transform(dev_data)

    def _etna_feature_transform(self, data: pd.DataFrame):
        """Метод для обогащения фичами трансформаций ETNA."""
        dev_ts: TSDataset = self._transform_to_ts_dataset(
            deepcopy(data).drop(columns=self.drop_features, axis=1)
        )
        dev_data: TSDataset = self._transform_to_ts_dataset(data)
        dev_data.fit_transform(transforms=self.etna_transforms)
        dev_data: pd.DataFrame = dev_data.to_pandas(True)
        return dev_data, dev_ts

    def _dml_feature_transform(self, data: pd.DataFrame):
        """Метод для обогащения фичами трансформаций DML."""
        if len(self.dml_transforms) > 0:
            for transform in self.dml_transforms:
                _, data = transform.transform(data)
        return data

    def _transform_to_ts_dataset(self, data: pd.DataFrame):
        """Метод для изменения типа датасета с pd.DataFrame в TSDataset."""
        ts_data = TSDataset.to_dataset(data)

        if self.exog_data is not None:
            regressor_ts = TSDataset.to_dataset(self.exog_data)
            ts_dataset = TSDataset(
                df=ts_data,
                freq=self.frequency,
                df_exog=regressor_ts,
                known_future=self.known_future,
            )
        else:
            ts_dataset = TSDataset(df=ts_data, freq=self.frequency)
        return ts_dataset

    def return_data_dict(self):
        """Метод финальной обработки и возврата датасетов."""

        etna_artifacts = {
            "dev_ts": self.dev_ts,
            "etna_transforms": self.etna_transforms,
        }
        data_dict = {
            "dev": self.dev_data,
            "etna_artifacts": etna_artifacts,
        }
        return data_dict


class PreprocessDataset:
    """
    Класс подготовки датасетов к формату ETNA,
    Проверка соответствия датасета для задачи TimeSeries.
    """

    def __init__(self, data_dict: Dict[str, pd.DataFrame], config: ConfigStorage):
        self.config = config
        self.horizon = config.horizon
        self.dev_data = data_dict["dev"]
        self.oot_data = data_dict["oot"] if "oot" in data_dict else None
        self.exog_data = data_dict["exog"] if "exog" in data_dict else None

    def transform(self):

        # Объединяем dev_data и oot_data
        self.dev_data = self._concat_dev_oot_data(self.dev_data, self.oot_data)
        self.oot_data = None

        # Проверяем датасет с экзогенными данными
        if self.exog_data is not None:
            self._check_exog_data()

        # Обрабатываем категориальные столбцы
        self.transform_categorical_columns(self.dev_data)

    def _concat_dev_oot_data(
        self, dev_data: pd.DataFrame, oot_data: Optional[pd.DataFrame] = None
    ) -> pd.DataFrame:
        """
        Метод для проверки oot_data и объединения с dev_data:
        1. Для dev_data и oot_data обязательны столбцы ['timestamp', 'target' и 'segment']
        2. Количество групп в oot_data должно равняться количеству групп в dev_data.
        3. Размер oot_data должен равняться горизонту предсказаний по всем группам
        4. Даты в oot_data не должны пересекаться с датами в dev_data
        """
        for etna_column in ["timestamp", "target", "segment"]:
            if etna_column not in dev_data or (
                oot_data is not None and etna_column not in oot_data
            ):
                raise ValueError(
                    "Для dev_data и oot_data обязательны столбцы 'timestamp', 'target' и 'segment'."
                )

        if oot_data is not None:
            if oot_data["segment"].nunique() != dev_data["segment"].nunique():
                raise ValueError(
                    "Количество групп в oot выборке должно равняться количеству групп в dev выборке."
                )

            min_required_len_per_group = self.horizon
            min_required_len_oot_data = (
                min_required_len_per_group * oot_data["segment"].nunique()
            )
            if len(oot_data) != min_required_len_oot_data:
                raise ValueError(
                    "Размер oot_data должен равняться горизонту предсказаний по всем группам."
                )

            dev_unique_dates = set(dev_data["timestamp"].unique().tolist())
            oot_unique_dates = set(oot_data["timestamp"].unique().tolist())
            if len(dev_unique_dates & oot_unique_dates) > 0:
                raise ValueError(
                    "Даты в oot_data не должны пересекаться с датами в dev_data."
                )

            dev_data = pd.concat([dev_data, oot_data], axis=0, ignore_index=True)
        return dev_data

    def _check_exog_data(self):
        """
        Метод для проверки соответствия датафрейма с экзогенными данными.
        1. Для exog_data обязательны столбцы ['timestamp' и 'segment']
        2. Отсутствие целевого временного ряда (`target_name`)
        3. В данном датасете должны/могут присутствовать данные как "из прошлого", так и "из будущего"
        4. Отсутствие тех же столбцов что есть в датасете с целевым временным рядом  (Кроме п.1 и п.2).
        5. Чтобы указать столбцы-регрессоры в данном датасете, нужно использовать ключ `known_future`.
        Остальные столбцы считаются за дополнительные.
        """
        for etna_column in ["timestamp", "segment"]:
            if etna_column not in self.exog_data.columns:
                raise ValueError(
                    "Для exog_data обязательны столбцы 'timestamp' и 'segment'."
                )

        if "target" in self.exog_data.columns:
            raise ValueError(
                "Целевой столбец не должен быть в датасете с экзогенными данными."
            )

        for column in self.exog_data.columns:
            if column in self.dev_data.columns and column not in [
                "timestamp",
                "target",
                "segment",
            ]:
                raise ValueError(
                    f"Столбец {column} присутствует в dev_data и exog_data."
                )

    def transform_categorical_columns(self, data: pd.DataFrame):
        """Функция нахождения категориальных фичей и добавления трансформаций в список трансформаций."""
        category_columns = data.select_dtypes(include=["category"]).columns.tolist()
        for column in set(category_columns):
            transform = LabelEncoderTransform(
                in_column=column, out_column="auto", return_type="numeric"
            )
            self.config.ts_transforms.extend(transform)
        return data