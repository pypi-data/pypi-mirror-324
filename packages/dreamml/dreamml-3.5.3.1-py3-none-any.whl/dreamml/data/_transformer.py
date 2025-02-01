import re
import sys
import time
import warnings
from typing import Tuple, Dict, Optional
from pathlib import Path

import numpy as np
import pandas as pd

from dreamml.logging import get_logger
from dreamml.logging.monitoring import DataTransformedLogData
from pandas.core.dtypes.common import is_datetime64_any_dtype
from sklearn.model_selection import train_test_split
from sklearn.base import BaseEstimator, TransformerMixin

from dreamml.pipeline.fitter.utils import (
    choose_validation_type_by_data_size,
)
from dreamml.utils.errors import ConfigurationError
from dreamml.utils.warnings import DMLWarning
from dreamml.utils import ValidationType
from dreamml.data._dataset import DataSet
from dreamml.data.store import get_input
from dreamml.data.exceptions import ZeroDataFrameException, ColumnDoesntExist
from dreamml.data._enums import FrequencyEnums
from dreamml.configs.config_storage import ConfigStorage
from dreamml.utils.encode_categorical import encode_categorical
from dreamml.utils.encode_text import encode_text
from dreamml.utils.splitter import DataSplitter
from dreamml.features.feature_extraction._base import drop_features
from dreamml.data._hadoop import create_spark_session, stop_spark_session
from dreamml.features.feature_enrichment import TimeSeriesEnrichment
from dreamml.features.feature_enrichment.timeseries_transforms import (
    RusHolidayTransform,
)

_logger = get_logger(__name__)


class DataTransformer(BaseEstimator, TransformerMixin):
    """
    Трансформер для входных данных пайплайна обучения DreamML.
    Пайплайн считывает и обрабатывает данные для обучения модели
    и для тестирования модели (Out-Of-Time выборка). Выполняется
    разбиение обучающей выборки на train-valid-test части, выбор
    части выборки для PSI-анализа, удаление мусорных признаков
    и обработка категориальных признаков.

    Parameters
    ----------
    config: ConfigStorage
        Глобальный конфигурационный файл DreamML.

    spark_config: pyspark.conf.SparkConf, optional, default = None.
        Конфигурация Spark-сессии. Опциональный параметр.
        По умолчанию, используется сессия с spark.driver.maxResultSize=32g
        и spark.executor.memory=16g.

    seed: int, optional, default = 27.
        Значение random_state / random_seed. Опциональный параметр.
        По умолчанию, используется значение 27.

    Attributes
    ----------
    cat_transformer: dreamml.features.categorical
        Трансформер для обработки категориальных признаков.

    text_transformer: dreamml.features.text
        Трансформер для обработки текстовых признаков.

    """

    def __init__(
        self, config: ConfigStorage, spark_config=None, seed: int = 27
    ) -> None:
        self.config = config
        self.spark_config = spark_config
        self.seed = seed
        self.cat_transformer = None
        self.text_transformer = None
        self.log_target = config.log_target
        self.target_name = config.target_name
        self.task = config.task
        self.subtaks = config.subtask
        self.shuffle = config.shuffle
        self.text_augs = config.text_augmentations
        self.aug_p = config.aug_p
        self._custom_data_split = self.config.dev_data_path is None
        self._check_dev_train_val_test_path()
        self.etna_artifacts = {}
        self.text_features_preprocessed = []
        self.train_indexes_before_augmentations = None

    def _is_spark_needed(self):
        # FIXME: is these all? Should import these or get from config
        local_file_types = ["csv", "pkl", "pickle", "parquet", "xlsx"]

        data_paths = [
            self.config.dev_data_path,
            self.config.oot_data_path,
            self.config.train_data_path,
            self.config.valid_data_path,
            self.config.test_data_path,
            self.config.path_to_exog_data,
        ]

        for path in data_paths:
            if path is None:
                continue

            data_ext = Path(path).suffix[1:]
            if data_ext not in local_file_types:
                return True

        return False

    def _get_data(self):
        data_dict = {}

        if self._is_spark_needed():
            temp_dir = self.config.get_temp_dir()
            spark = create_spark_session(
                spark_config=self.spark_config, temp_dir=temp_dir
            )
        else:
            temp_dir = None
            spark = None

        if self._custom_data_split:
            df_train = self._get_train_data(spark)
            data_dict["train"] = df_train
            self._calculate_time_frequency(data_dict["train"])

            df_test = self._get_test_data(spark)
            data_dict["test"] = df_test

            df_valid = self._get_valid_data(spark)

            if not df_valid.empty:
                data_dict["valid"] = df_valid
            else:
                # continue without valid if validation_type=='cv' or raise error if validation_type=='hold-out'
                validation_type = self._get_validation_type(data_dict)
                self._check_validation_type(validation_type, data_dict)
        else:
            data_dict["dev"] = self._get_dev_data(spark)
            self._calculate_time_frequency(data_dict["dev"])

        if self.config.oot_data_path:
            data_dict["oot"] = self._get_oot_data(spark)

        if self.config.task == "timeseries":
            if self.config.path_to_exog_data is not None:
                data_dict["exog"] = self._get_exog_data(spark)

            data_dict = self._rename_timeseries_dataset(data_dict)
            data_dict = self._check_group_column(data_dict)

            self.config.time_column = "timestamp"
            self.config.group_column = "segment"
            self.config.target_name = "target"

        for key, df in data_dict.items():
            if len(df) == 0:
                _logger.exception(f"Input data with {key=} is empty.")
                raise ZeroDataFrameException()

        if spark is not None:
            stop_spark_session(spark=spark, temp_dir=temp_dir)

        self.config.config_checker.check_data(data_dict)
        if not self.config.config_checker.is_clean_data:
            raise ConfigurationError("Data configuration problem")

        return data_dict

    def _rename_timeseries_dataset(self, data_dict: Dict[str, pd.DataFrame]):
        """Метод переименования столбцов для ETNA."""

        # Сохраняем оригинальные названия столбцов
        self.etna_artifacts["original_columns"] = {
            "timestamp": self.config.time_column,
            "target": self.config.target_name,
            "segment": self.config.group_column,
        }

        etna_required_columns = ["timestamp", "target", "segment"]
        original_columns = [
            self.config.time_column,
            self.config.target_name,
            self.config.group_column,
        ]

        for sample_name, sample in data_dict.items():
            for original_column, etna_column in zip(
                original_columns, etna_required_columns
            ):
                if original_column is not None and original_column in sample.columns:
                    sample.rename({original_column: etna_column}, axis=1, inplace=True)
                    data_dict[sample_name] = sample
        return data_dict

    def _check_group_column(self, data_dict: Dict[str, pd.DataFrame]):
        """
        Метод проверки столбца группировки. Если group_column = None,
        то создается фиктивный столбец 'segment' = group_column_value.
        """
        for sample_name, sample in data_dict.items():
            if (
                sample["timestamp"].nunique() != len(sample)
                and self.config.group_column is None
            ):
                raise ValueError(
                    "В датасете присутствуют одинаковые даты, что является признаком наличия "
                    "нескольких временных рядов.\n"
                    'Укажите столбец группировки в параметре конфига "group_column".'
                )
            elif (
                sample["timestamp"].nunique() == len(sample)
                and self.config.group_column is None
            ):
                sample["segment"] = "main"

            data_dict[sample_name] = sample
        return data_dict

    def _get_dev_data(self, spark=None):
        df, _ = get_input(data_path="dev_data_path", config=self.config, spark=spark)

        return df

    def _get_oot_data(self, spark=None):
        df, _ = get_input(data_path="oot_data_path", config=self.config, spark=spark)

        return df

    def _get_exog_data(self, spark=None):
        df, _ = get_input(
            data_path="path_to_exog_data", config=self.config, spark=spark
        )

        return df

    def _get_train_data(self, spark=None):
        df, _ = get_input(data_path="train_data_path", config=self.config, spark=spark)

        return df

    def _get_valid_data(self, spark=None):
        if not self.config.valid_data_path:
            df = pd.DataFrame()
        else:
            df, _ = get_input(
                data_path="valid_data_path", config=self.config, spark=spark
            )

        return df

    def _get_test_data(self, spark=None):
        df, _ = get_input(data_path="test_data_path", config=self.config, spark=spark)

        return df

    def _get_validation_type(self, data_dict) -> ValidationType:
        validation = self.config.validation

        if validation == "auto":
            assert "valid" not in data_dict
            data_size = data_dict["train"].shape[0] + data_dict["test"].shape[0]

            return choose_validation_type_by_data_size(data_size)
        else:
            return ValidationType(validation)

    def _check_validation_type(self, validation_type: ValidationType, data_dict):
        if validation_type == ValidationType.HOLDOUT:
            # TODO: Создавать val выборку самим на основе split_params?
            msg = (
                "Тип валидации установлен на hold-out. "
                "Необходима отдельная валидационная выборка. Укажите путь в valid_data_path."
            )
            raise Exception(msg)
        elif validation_type == ValidationType.CV:
            # Нужно для того, чтобы eval_sets содержали непустую valid выборку. На пайплайн обучения не влияет.
            data_dict["train"], data_dict["valid"] = train_test_split(
                data_dict["train"], test_size=0.2, shuffle=False
            )
        else:
            raise ValueError(
                f"Can't transform data with validaton type = {validation_type.value}."
            )

    def _split_oot_from_dev(self, data_dict):
        split_column = self.config.time_column

        if self._custom_data_split:
            split_values = pd.concat(
                [data_dict.get(key)[split_column] for key in ["train", "valid", "test"]]
            ).unique()
        else:
            split_values = data_dict["dev"][split_column].unique()
        self.config.oot_split_n_values = (
            self.config.horizon
            if self.task == "timeseries"
            else self.config.oot_split_n_values
        )
        last_n_values = sorted(split_values)[-self.config.oot_split_n_values :]

        oot_parts = []
        for key, df in data_dict.items():
            if key in ["dev", "train", "valid", "test"]:
                mask = df[split_column].isin(last_n_values)

                oot_parts.append(df[mask])
                data_dict[key] = df[~mask].reset_index(drop=True)

        data_dict["oot"] = pd.concat(oot_parts, ignore_index=True)

    @staticmethod
    def _merge_train_valid_test(data_dict):
        merged_data = pd.concat(
            [data_dict.get(key) for key in ["train", "valid", "test"]],
            ignore_index=True,
        )

        data_dict["dev"] = merged_data

    def _get_train_valid_test_indexes(self, data_dict):
        if self._custom_data_split:
            dev_indexes = data_dict["dev"].index
            valid_start = len(data_dict["train"])
            valid_end = valid_start + len(data_dict.get("valid", []))

            indexes = (
                dev_indexes[:valid_start],
                dev_indexes[valid_start:valid_end],
                dev_indexes[valid_end:],
            )
        else:
            splitter = DataSplitter(
                split_fractions=self.config.split_params,
                shuffle=self.shuffle,
                group_column=self.config.group_column,
                target_name=self.config.target_name,
                stratify=self.config.stratify,
                task=self.task,
                time_column=self.config.time_column,
                split_by_group=self.config.split_by_group,
            )
            indexes = splitter.transform(data_dict["dev"])

        return indexes

    def _check_dev_train_val_test_path(self):
        """
        Проверка неконфликтности путей данных в конфиге.

        Если подаётся dev_data_path, то поля train_data_path, valid_data_path и test_data_path должны быть пустыми.
        Если dev_data_path не подаётся, то хотя бы train_data_path и test_data_path должны быть заполнены.
        """
        if self._custom_data_split:
            if not (self.config.train_data_path and self.config.test_data_path):
                msg = (
                    "При отсутствующем поле dev_data_path "
                    "поля train_data_path и test_data_path должны быть заполнены"
                )
                raise Exception(msg)
        else:
            if (
                self.config.train_data_path
                or self.config.valid_data_path
                or self.config.test_data_path
            ):
                msg = (
                    "При поданном поле dev_data_path "
                    "поля train_data_path, valid_data_path и test_data_path должны быть пустыми"
                )
                raise Exception(msg)

    def _check_feature_names(self, data):
        """
        Проверка валидности имен признаков. (LightGBM принимает в именах только [A-Za-z0-9_])
        Если признаки невалидны, то убирает из конфига LightGBM и WB AutoML.

        Parameters
        ----------
        data: Dict[str, Tuple[pd.DataFrame, pd.Series]]
            Словарь с данными для обучения модели.

        """
        features_names = data["train"][0].columns
        invalid_column_list = []
        # Список не поддерживаемых символов
        # https://github.com/microsoft/LightGBM/
        # blob/b8e38ec1eb8020052d5b39e31e9f2cb6366fb873/include/LightGBM/utils/common.h#L848
        for col in features_names:
            if re.search(r'[",:\[\]{}]', col):
                invalid_column_list.append(col)

        if invalid_column_list:
            if "lightgbm" in self.config.fitted_model:
                self.config.fitted_model.remove("lightgbm")
                warnings.warn(
                    "Модель lightgbm убрана из списка обучаемых моделей, так как в датасете присутствуют "
                    'признаки с недопустимыми названиями, в названиях недопустимы символы: ",:[]{}',
                    DMLWarning,
                    stacklevel=2,
                )
            if self.config.use_whitebox_automl:
                self.config.use_whitebox_automl = False
                warnings.warn(
                    "Модель WhiteBox AutoML убрана из списка обучаемых моделей, так как в датасете присутствуют "
                    'признаки с недопустимыми названиями, в названиях недопустимы символы: ",:[]{}',
                    DMLWarning,
                    stacklevel=2,
                )
            warnings.warn(
                f"Признаки с недопустимыми названиями: {invalid_column_list}",
                DMLWarning,
                stacklevel=2,
            )

    def _check_model_availability(self):
        msg = "Отсутствуют модели для обучения!"
        if not self.config.fitted_model and not self.config.use_whitebox_automl:
            raise Exception(msg)

    def _transform_time_column_to_datetime(self, df: pd.DataFrame):
        """
        Функция трансформации столбца в формат datetime.
        """
        if self.config.time_column not in df.columns:
            raise Exception(f"Столцба {self.config.time_column} нет в датафрейме")

        if is_datetime64_any_dtype(df[self.config.time_column].dtype):
            df = self._remove_timezone(df)
            return df

        try:
            df[self.config.time_column] = pd.to_datetime(
                df[self.config.time_column],
                format=self.config.time_column_format,
                utc=True,
            )
            df = self._remove_timezone(df)
        except ValueError as e:
            raise ValueError(
                f"Вероятно указан неверный формат даты или столбец не содержит даты. {e}"
            )
        return df

    def _remove_timezone(self, df: pd.DataFrame):
        if df[self.config.time_column].dt.tz:
            df[self.config.time_column] = df[self.config.time_column].dt.tz_localize(
                None
            )
        return df

    def transform(self) -> DataSet:
        """
        Полный пайплайн получения и обработки данных.

        Returns
        -------
        dataset: DataSet
            Объект класса DataSet. Используется для хранения данных обучения
            и другой информации, связанной с ней.

        """
        np.random.seed(self.seed)

        data_dict = self._get_data()
        start_time = time.time()

        if self._custom_data_split:
            self._merge_train_valid_test(data_dict)

        if self.task == "timeseries":
            timeseries_feature_enrichment = TimeSeriesEnrichment(
                data_dict, self.config, self.cat_transformer
            )
            timeseries_feature_enrichment.transform()
            data_dict = timeseries_feature_enrichment.return_data_dict()
            etna_artifacts = data_dict.pop("etna_artifacts")
            self.etna_artifacts.update(etna_artifacts)

        dev_data = data_dict["dev"]
        oot_data = data_dict.get("oot")

        if (
            self.task == "amts"
            and self.config.get("time_column_frequency") == FrequencyEnums.DAYS
        ):
            holiday_transform_atms = RusHolidayTransform(
                in_column=self.config.time_column
            )
            added_features, dev_data = holiday_transform_atms.transform(data=dev_data)
            if oot_data is not None:
                added_features, oot_data = holiday_transform_atms.transform(
                    data=oot_data
                )

        if (
            data_dict.get("oot") is None
            and self.config.time_column is not None
            and self.config.oot_data_path is not None
        ):
            self._split_oot_from_dev(data_dict)
            dev_data = data_dict["dev"]
            oot_data = data_dict["oot"]

        indexes = self._get_train_valid_test_indexes(data_dict)
        self.train_indexes_before_augmentations = indexes[
            0
        ]  # Сохраняем train sample indexes до аугментаций
        del data_dict

        # QUESTION: не хорошо в конфиге хранить веса
        if self.config.weights_column is not None:
            self.config.weights = dev_data[self.config.weights_column]

        # -- Применяем трансформации к данным --
        # * Кодирование категориальных признаков
        dev_data, oot_data, self.cat_transformer = self.encode_categorical_compat(
            dev_data, oot_data, indexes
        )
        self.config.categorical_features = self.cat_transformer.cat_features

        # * NLP предобработка текстовых признаков
        if self.subtaks == "nlp":
            dev_data, oot_data, self.text_transformer, indexes = (
                self.encode_text_compat(dev_data, oot_data, indexes)
            )
            self.config.text_features = self.text_transformer.text_features
            self.config.text_features_preprocessed = (
                self.text_transformer.text_features_preprocessed
            )

        # * Применение datetime формата к временному признаку
        if self.config.time_column is not None:
            dev_data = self._transform_time_column_to_datetime(dev_data)
            if oot_data is not None:
                oot_data = self._transform_time_column_to_datetime(oot_data)

        # ~~~ AMTS ~~~
        if self.config.task == "amts":
            self.config.categorical_features = [
                features
                for features in self.config.categorical_features
                if features != self.config.time_column
            ]

        # -- DATASET --
        dataset = DataSet(
            dev_data,
            oot_data,
            self.config,
            indexes,
            self.config.categorical_features,
            self.config.text_features,
            self.config.text_features_preprocessed,
        )
        dataset.etna_artifacts = self.etna_artifacts
        dataset.train_indexes_before_augmentations = (
            self.train_indexes_before_augmentations
        )

        # Добавляем labels в metric_params
        if self.task == "binary":
            self.config.metric_params["labels"] = [0, 1]
        elif self.task == "multiclass":
            self.config.metric_params["labels"] = self.cat_transformer.encoders[
                self.target_name
            ].encoder.classes_
        else:
            self.config.metric_params["labels"] = None

        data = dataset.get_eval_set(drop_service_fields=False)

        self._check_feature_names(data)
        self._check_model_availability()
        self._check_nan_values_and_zero_columns(data)

        # -- logs --
        elapsed_time = time.time() - start_time
        _logger.monitor(
            f"Data transformed in {elapsed_time:.1f} seconds.",
            extra={
                "log_data": DataTransformedLogData(
                    name="dev_data",
                    length=len(dev_data),
                    features_num=dev_data.shape[1],
                    nan_count=dev_data.isna().sum().sum(),
                    elapsed_time=elapsed_time,
                )
            },
        )

        if self.config.categorical_features:
            _logger.debug(f"Categorical features: {self.config.categorical_features}")

        if self.subtaks == "nlp":
            _logger.debug(f"Text features: {self.config.text_features}")
            _logger.debug(
                f"Text features preprocessed: {self.config.text_features_preprocessed}"
            )

        return dataset

    def _check_nan_values_and_zero_columns(self, data: dict):
        """Проверка на наличие NaN значений и полностью пустых столбцов в target."""

        if self.task == "multilabel" and self.config.target_with_nan_values is False:
            for sample_name, sample in data.items():
                df_targets = sample[1]

                nan_columns = df_targets.columns[df_targets.isna().any()].tolist()
                if nan_columns:
                    raise ValueError(
                        f"Target contains NaN values in sample '{sample_name}' in columns: {', '.join(nan_columns)}.\n"
                        f"Set config option 'target_with_nan_values = True' or handle NaN values in targets."
                    )

                zero_columns = df_targets.columns[(df_targets == 0).all()].tolist()
                if zero_columns:
                    raise ValueError(
                        f"Target contains columns  with all zeros in sample '{sample_name}'"
                        f" in columns: {', '.join(zero_columns)}.\n"
                        f"The number of classes must be greater than 1. Please handle all zeros columns in targets."
                    )

    def get_compat_dataframes(
        self, dev_data: pd.DataFrame, oot_data: Optional[pd.DataFrame]
    ) -> Tuple[pd.DataFrame, Optional[pd.DataFrame], dict]:
        """
        Функция для обратной совместимости с DreamML до 2.0
        Чтобы в encode_categorical приходили датасеты без фич на удаление-drop_features

        Parameters
        ----------
        dev_data: pd.DataFrame
            Выборка для обучения
        oot_data: Optional[pd.DataFrame]
            Отложенная выборка

        Returns
        -------
        data: Tuple[pd.DataFrame, Optional[pd.DataFrame]]
            Либо только обучающая выборка, либо к ней прибавляется отложенная выборка
        """
        if self.config.target_name is None:
            compat_set = {"dev": (dev_data, None)}
        else:
            compat_set = {"dev": (dev_data, dev_data[self.config.target_name])}
        if isinstance(oot_data, pd.DataFrame):
            if self.config.target_name is None:
                compat_set = {"oot": (oot_data, None)}
            else:
                compat_set["oot"] = (oot_data, oot_data[self.config.target_name])
        compat_conf = {
            "task": self.config.task,
            "drop_features": self.config.drop_features,
            "target_name": self.config.target_name,
            "multitarget": self.config.multitarget,
            "time_column": self.config.time_column,
            "oot_data_path": self.config.oot_data_path,
            "never_used_features": self.config.never_used_features,
        }
        compat_set, dropped_data = drop_features(compat_conf, compat_set)

        if self.config.target_name is None:
            compat_dev_data = compat_set["dev"][0]
        else:
            compat_dev_data = compat_set["dev"][0].join(compat_set["dev"][1])

        if compat_set.get("oot"):
            if self.config.target_name is None:
                compat_oot_data = compat_set["oot"][0]
            else:
                compat_oot_data = compat_set["oot"][0].join(compat_set["oot"][1])
            return (
                compat_dev_data,
                compat_oot_data,
                dropped_data,
            )
        return compat_dev_data, None, dropped_data

    def encode_categorical_compat(self, dev_data, oot_data, indexes):
        compat_dev_data, compat_oot_data, dropped_data = self.get_compat_dataframes(
            dev_data, oot_data
        )

        dev_data, oot_data, transformer = encode_categorical(
            self.config, compat_dev_data, compat_oot_data, indexes
        )

        if dropped_data:
            dev_data = dev_data.join(dropped_data["dev"])
            if isinstance(oot_data, pd.DataFrame):
                oot_data = oot_data.join(dropped_data["oot"])

        return dev_data, oot_data, transformer

    def encode_text_compat(self, dev_data, oot_data, indexes):
        dev_data, oot_data, transformer, new_indexes = encode_text(
            self.config,
            dev_data,
            oot_data,
            indexes,
            self.text_augs,
            self.aug_p,
        )
        return dev_data, oot_data, transformer, new_indexes

    def _calculate_time_frequency(self, data):
        if self.task != "amts":
            return

        if self.config.split_by_group:
            try:
                group = data[self.config.group_column][0]
            except Exception as e:
                raise ColumnDoesntExist(column_name=self.config.group_column, data=data)
            df = data[data[self.config.group_column] == group]
            data = df

        try:
            time_column: pd.Series = pd.to_datetime(data[self.config.time_column])
        except Exception as e:
            raise ColumnDoesntExist(column_name=self.config.time_column, data=data)

        diff = time_column.diff().dropna()
        most_common_freq = diff.mode()[0]

        seconds = most_common_freq.total_seconds()
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        months, days = divmod(days, 5)

        components = {
            FrequencyEnums.SECONDS: int(seconds),
            FrequencyEnums.MINUTES: int(minutes),
            FrequencyEnums.HOURS: int(hours),
            FrequencyEnums.DAYS: int(days),
            FrequencyEnums.MONTHS: int(months),
        }

        for unit, value in components.items():
            if value > 0:
                self.config.prophet_hyper_params["time_column_frequency"] = unit
                self.config.set("time_column_frequency", unit)
        return