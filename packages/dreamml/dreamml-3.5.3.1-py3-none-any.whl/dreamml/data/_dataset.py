from copy import deepcopy
from typing import Union, List, Optional, Dict
import pandas as pd
from dreamml.configs.config_storage import ConfigStorage
from dreamml.features.feature_extraction._transformers import LogTargetTransformer
from dreamml.features.feature_extraction._outliers import (
    filter_outliers_by_train_valid,
    get_min_max_perc,
    filter_outliers_by_perc,
)
from dreamml.data._utils import get_sample_frac
from dreamml.data._enums import FrequencyEnums
import numpy as np

from dreamml.logging import get_logger

np.random.seed(27)
_logger = get_logger(__name__)


class DataSet:
    """
    Класс входных данных DreamML.
    """

    def __init__(
        self,
        dev_data: pd.DataFrame,
        oot_data: pd.DataFrame or None,
        config: ConfigStorage,
        indexes: tuple,
        cat_features: list,
        text_features: list,
        text_features_preprocessed: list,
    ):

        self.dev_data = dev_data
        self.oot_data = oot_data
        self.target_name = config.target_name
        if self.target_name is None:
            self.dev_target = None
        else:
            self.dev_target = self.dev_data[self.target_name]
        if oot_data is not None:
            if self.target_name is None:
                self.oot_target = None
            else:
                self.oot_target = self.oot_data[self.target_name]
        self.cat_features = cat_features
        self.text_features = text_features
        self.text_features_preprocessed = text_features_preprocessed
        self.drop_features = list(
            set(config.drop_features if config.drop_features is not None else [])
        )
        self.task = config.task

        self.features = self.dev_data.columns
        self.folds = config.cv_n_folds
        self.sample_strategy = config.sample_strategy
        self.indexes = indexes
        self.group_column = config.group_column
        self.split_by_group = config.split_by_group

        self.time_column = config.time_column
        if (
            self.time_column
            and self.task != "amts"
            and self.time_column not in self.drop_features
        ):
            self.drop_features.append(self.time_column)

        self.oot_data_path = config.oot_data_path
        self.multitarget = config.multitarget
        self.never_used_features = config.never_used_features
        self.etna_artifacts = None
        self.train_indexes_before_augmentations = None
        self.outliers_config = {
            "min_percentile": config.min_percentile,
            "max_percentile": config.max_percentile,
        }
        self.horizon = config.horizon
        self.time_column_frequency = config.get("time_column_frequency")
        self.embeddings: dict = {}
        self.text_augs: list = config.text_augmentations
        self._service_fields = config._service_fields

    def __len__(self):
        return len(self.dev_data)

    def set_embedding_sample(
        self, vectorization_name: str, sample_name: str, embeddings_df: pd.DataFrame
    ):
        if vectorization_name not in [
            "tf-idf",
            "glove",
            "fasttext",
            "word2vec",
            "bert",
            "bow",
        ]:
            msg = f"{vectorization_name.title()} is not in the list of available ones."
            raise ValueError(msg)
        elif vectorization_name not in self.embeddings:
            self.embeddings[vectorization_name] = {}
        self.embeddings[vectorization_name][sample_name] = embeddings_df

    def _get_embedding_sample(self, vectorization_name: str, sample_name: str):
        if vectorization_name == "all":
            concat_all_embedds_df = pd.DataFrame()
            for vec_name, embedds in self.embeddings.items():
                concat_all_embedds_df = pd.concat(
                    [concat_all_embedds_df, embedds[sample_name]], axis=1
                )
            return concat_all_embedds_df

        elif vectorization_name not in self.embeddings:
            msg = f"{vectorization_name} embeddings is missing in embeddings."
            raise ValueError(msg)
        elif sample_name not in self.embeddings[vectorization_name]:
            msg = f"{sample_name.title()} sample is missing in {vectorization_name} embeddings."
            raise ValueError(msg)
        else:
            return self.embeddings[vectorization_name][sample_name]

    def sample(self, used_features=None, vectorization_name=None):
        """
        Реализация Reservoir Sampling для сэмплирования больших датасетов

        Parameters
        ----------
        used_features list or None
            Список используемых признаков.
        Returns
        -------
        Сэмплированный датасет признаков и таргетов.
        """
        if used_features is None:
            used_features = list(self.dev_data.drop(self.target_name, axis=1).columns)
        data, target = self.get_train(used_features, vectorization_name)
        k = get_sample_frac(data.shape[0])
        reservoir = np.array(data.iloc[:k].index)
        for i in range(k + 1, data.shape[0]):
            r = np.random.randint(0, i)
            if r < k:
                reservoir[r] = data.iloc[[i]].index.values

        return data.loc[reservoir][used_features], target.loc[reservoir]

    def get_eval_set(
        self,
        used_features: List[str] = None,
        vectorization_name: str = None,
        drop_service_fields: bool = True,
    ):
        if self.task == "amts":
            return self.get_amts_data()

        eval_set = self.get_clean_eval_set(used_features, vectorization_name)

        never_used_features_cleaned = []
        garbage_features = []
        if self.multitarget:
            garbage_features.extend(self.multitarget)
        if not used_features:
            garbage_features.extend(self.drop_features)
            if self.group_column not in garbage_features and self.task == "timeseries":
                garbage_features.extend([self.group_column])
            if vectorization_name not in [None, "all"] and self.task in [
                "multiclass",
                "binary",
            ]:
                garbage_features.extend(self.text_features)
        if self.never_used_features:
            for feature in self.never_used_features:
                never_used_features_cleaned.append(feature.split("\n")[0])
        if self.task in ["regression"]:
            eval_set = filter_outliers_by_train_valid(
                eval_set, self.get_cv_data_set(), self.outliers_config
            )

        extra_features_to_drop = []
        for sample in eval_set:
            data, target = eval_set[sample]

            if vectorization_name != "bow":
                garbage_features = [
                    col for col in garbage_features if col in data.columns
                ]
                data = data.drop(garbage_features, axis=1)
                extra_features_to_drop = list(
                    set(data.columns) & set(never_used_features_cleaned)
                )
                if extra_features_to_drop:
                    data = data.drop(extra_features_to_drop, axis=1)

                if drop_service_fields:
                    _existed_service_fields = [
                        _field
                        for _field in self._service_fields
                        if _field in data.columns
                    ]
                    data = data.drop(_existed_service_fields, axis=1)

            eval_set[sample] = (data, target)

        if extra_features_to_drop or garbage_features:
            _logger.debug(f"Drop features: {garbage_features + extra_features_to_drop}")

        return eval_set

    def get_dropped_data(self, used_features=None):
        eval_set = self.get_clean_eval_set(used_features)
        if self.task in ("regression", "timeseries"):
            eval_set = filter_outliers_by_train_valid(
                eval_set, self.get_cv_data_set(), self.outliers_config
            )

        dropped_data = {}
        drop_f = [
            f
            for f in self.never_used_features
            if f in eval_set["train"][0].columns and f not in self.drop_features
        ]
        drop_f.extend(self.drop_features)
        if drop_f:
            for sample in eval_set:
                try:
                    dropped_data[sample] = eval_set[sample][0][drop_f]
                except KeyError:
                    pass

        return dropped_data

    def get_dev_n_samples(self):
        return self.dev_data.shape[0]

    def get_data_shapes(self):
        dev_data, cols = self.dev_data.shape
        oot_data = self.oot_data.shape[0] if self.oot_data is not None else None
        return dev_data, oot_data, cols

    def get_set(
        self, used_features=None, type_of_data="train", vectorization_name=None
    ):
        if used_features is None:
            if self.target_name is None:
                used_features = list(self.dev_data.columns)
            else:
                used_features = list(
                    self.dev_data.drop(self.target_name, axis=1).columns
                )
            if vectorization_name is not None:
                if vectorization_name == "bow":
                    vectorization_columns = list(
                        self._get_embedding_sample(
                            vectorization_name, sample_name="train"
                        ).keys()
                    )
                else:
                    vectorization_columns = self._get_embedding_sample(
                        vectorization_name, sample_name="train"
                    ).columns.tolist()
                used_features.extend(vectorization_columns)

        if type_of_data == "OOT":
            data = self.oot_data
            target = self.oot_target
            data = self._concat_embeddings(
                data, vectorization_name, type_of_data, used_features
            )
            return data[used_features], target
        elif type_of_data == "train_cv":
            return self.get_train_cv(used_features, vectorization_name)
        else:
            if type_of_data == "train":
                idx = self.indexes[0]
            elif type_of_data == "valid":
                idx = self.indexes[1]
            elif type_of_data == "test":
                idx = self.indexes[2]
            else:
                idx = None
            data = self.dev_data
            data = data.loc[idx]
            data = self._concat_embeddings(
                data, vectorization_name, type_of_data, used_features
            )
            if self.target_name is None:
                target = None
            else:
                target = self.dev_target.loc[idx]

            if vectorization_name == "bow":
                return data, target

            return data[used_features], target

    def _concat_embeddings(
        self,
        data: pd.DataFrame,
        vectorization_name: Optional[str],
        sample_name: str,
        used_features: List[str],
    ):
        used_features_cp = deepcopy(used_features)
        if vectorization_name is None:
            return data

        elif vectorization_name == "all":
            for vec_name, embedding_df in self.embeddings.items():
                sample_embedding_df = self._get_embedding_sample(
                    vectorization_name=vec_name, sample_name=sample_name
                )
                data = pd.concat(
                    [data, sample_embedding_df], axis=1, ignore_index=False
                )
                embedding_columns = sample_embedding_df.columns.tolist()

        else:
            sample_embedding_df = self._get_embedding_sample(
                vectorization_name=vectorization_name, sample_name=sample_name
            )
            if vectorization_name == "bow":
                return sample_embedding_df
            data = pd.concat([data, sample_embedding_df], axis=1, ignore_index=False)
            embedding_columns = sample_embedding_df.columns.tolist()

        return data

    def get_train_cv(self, used_features, vectorization_name=None):
        train_idx, valid_idx = self.indexes[0], self.indexes[1]
        data = self.dev_data
        target = self.dev_target

        train_data = self._concat_embeddings(
            data=data.loc[train_idx],
            vectorization_name=vectorization_name,
            sample_name="train",
            used_features=used_features,
        )

        valid_data = self._concat_embeddings(
            data=data.loc[valid_idx],
            vectorization_name=vectorization_name,
            sample_name="valid",
            used_features=used_features,
        )

        if self.target_name is None:
            train_cv = pd.concat([train_data[used_features], valid_data[used_features]])
        else:
            train_cv = pd.concat(
                [train_data[used_features], valid_data[used_features]]
            ), pd.concat([target.loc[train_idx], target.loc[valid_idx]])

        if self.task in ("regression", "timeseries"):
            min_perc, max_perc = get_min_max_perc(self.outliers_config, train_cv[1])
            train_cv = filter_outliers_by_perc(*train_cv, min_perc, max_perc)
        return train_cv

    def get_train(self, used_features=None, vectorization_name=None):
        return self.get_set(used_features, "train", vectorization_name)

    def get_valid(self, used_features=None, vectorization_name=None):
        return self.get_set(used_features, "valid", vectorization_name)

    def get_test(self, used_features=None, vectorization_name=None):
        return self.get_set(used_features, "test", vectorization_name)

    def get_oot(self, used_features=None, vectorization_name=None):
        return self.get_set(used_features, "OOT", vectorization_name)

    def get_cv_data_set(self, used_features=None, vectorization_name=None):
        return self.get_set(used_features, "train_cv", vectorization_name)

    def get_cv_splitter_df(self, splitter_columns: List[str]) -> pd.DataFrame:
        """
        Получает pd.DataFrame с колонками необходимыми для разбиения в случае кросс-валидации.

        Returns
        -------
        result: pd.DataFrame
        """
        if len(splitter_columns) == 0:
            splitter_columns = (
                self.target_name
                if isinstance(self.target_name, list)
                else [self.target_name]
            )

        return self.get_cv_data_set(splitter_columns)[0]

    def get_clean_eval_set(self, used_features=None, vectorization_name=None):
        """
        Создание словаря eval_set, где ключ - название выборки,
        значение - кортеж с матрицей признаков и вектором целевой
        переменной.
        """

        eval_set = {
            "train": (self.get_train(used_features, vectorization_name)),
            "valid": (self.get_valid(used_features, vectorization_name)),
            "test": (self.get_test(used_features, vectorization_name)),
        }
        if self.oot_data is not None:
            eval_set["OOT"] = self.get_oot(used_features, vectorization_name)
        return eval_set

    def get_amts_data(self) -> Dict:
        """
        Возвращает полный набор данных первичного обчуения для модели AMTS (train, valid, oot)

        Returns
        -------
        return: pd.DataFrame
        """
        trend_dev = np.array([i for i in range(len(self.dev_data))])
        if self.oot_data_path is None:

            df_train = pd.DataFrame(
                {
                    "ds": self.dev_data[: -self.horizon][self.time_column],
                    "trend": trend_dev[: -self.horizon],
                }
            )
            df_valid = pd.DataFrame(
                {
                    "ds": self.dev_data[-self.horizon :][self.time_column],
                    "trend": trend_dev[-self.horizon :],
                }
            )

            if self.time_column_frequency == FrequencyEnums.DAYS:
                columns = [
                    "is_weekend",
                    "is_holiday",
                    "is_pre_holiday",
                    "is_pre_pre_holiday",
                ]
                for column in columns:
                    df_train[column] = self.dev_data[: -self.horizon][
                        f"{self.time_column}_{column}"
                    ]
                for column in columns:
                    df_valid[column] = self.dev_data[-self.horizon :][
                        f"{self.time_column}_{column}"
                    ]

            if self.split_by_group:
                df = pd.concat([df_train, df_valid], axis=0)
                df[self.group_column] = self.dev_data[self.group_column]
                return {"train": (df, self.dev_data[self.target_name])}

            return {
                "train": (df_train, self.dev_data[: -self.horizon][self.target_name]),
                "valid": (df_valid, self.dev_data[-self.horizon :][self.target_name]),
            }

        else:
            trend_oot = np.array(
                [i for i in range(len(trend_dev), len(trend_dev) + len(self.oot_data))]
            )
            df_train = pd.DataFrame(
                {"ds": self.dev_data[self.time_column], "trend": trend_dev}
            )
            df_oot = pd.DataFrame(
                {"ds": self.oot_data[self.time_column], "trend": trend_oot}
            )

            if self.time_column_frequency == FrequencyEnums.DAYS:
                for df, basis_data in [
                    (df_train, self.dev_data),
                    (df_oot, self.oot_data),
                ]:
                    df["is_weekend"] = basis_data[f"{self.time_column}_is_weekend"]
                    df["is_holiday"] = basis_data[f"{self.time_column}_is_holiday"]
                    df["is_pre_holiday"] = basis_data[
                        f"{self.time_column}_is_pre_holiday"
                    ]
                    df["is_pre_pre_holiday"] = basis_data[
                        f"{self.time_column}_is_pre_pre_holiday"
                    ]

            if self.split_by_group:
                df = pd.concat([df_train, df_oot], axis=0)
                df[self.group_column] = self.dev_data[self.group_column]
                return {"train": (df, self.dev_data[self.target_name])}

            return {
                "train": (df_train, self.dev_data[self.target_name]),
                "oot": (df_oot, self.oot_data[self.target_name]),
            }

    def get_amts_final_data(self):
        """
        Возвращает полный набор данных финального обучения для модели AMTS (train, valid, oot)

        Returns
        -------
        return: pd.DataFrame
        """
        trend_dev = np.array([i for i in range(len(self.dev_data))])
        if self.oot_data_path is None:

            df_train = pd.DataFrame(
                {
                    "ds": self.dev_data[self.time_column],
                    "trend": trend_dev,
                }
            )
            df_valid = pd.DataFrame(
                {
                    "ds": self.dev_data[self.time_column],
                    "trend": trend_dev,
                }
            )

            if self.time_column_frequency == FrequencyEnums.DAYS:
                columns = [
                    "is_weekend",
                    "is_holiday",
                    "is_pre_holiday",
                    "is_pre_pre_holiday",
                ]
                for column in columns:
                    df_train[column] = self.dev_data[f"{self.time_column}_{column}"]
                for column in columns:
                    df_valid[column] = self.dev_data[f"{self.time_column}_{column}"]

            if self.split_by_group:
                df = pd.concat([df_train, df_valid], axis=0)
                df[self.group_column] = self.dev_data[self.group_column]
                return {"train": (df, self.dev_data[self.target_name])}

            return {
                "train": (df_train, self.dev_data[self.target_name]),
                "valid": (df_valid, self.dev_data[self.target_name]),
            }

        else:
            trend_oot = np.array(
                [i for i in range(len(trend_dev), len(trend_dev) + len(self.oot_data))]
            )
            df_train = pd.DataFrame(
                {"ds": self.dev_data[self.time_column], "trend": trend_dev}
            )
            df_oot = pd.DataFrame(
                {"ds": self.oot_data[self.time_column], "trend": trend_oot}
            )

            if self.time_column_frequency == FrequencyEnums.DAYS:
                for df, basis_data in [
                    (df_train, self.dev_data),
                    (df_oot, self.oot_data),
                ]:
                    df["is_weekend"] = basis_data[f"{self.time_column}_is_weekend"]
                    df["is_holiday"] = basis_data[f"{self.time_column}_is_holiday"]
                    df["is_pre_holiday"] = basis_data[
                        f"{self.time_column}_is_pre_holiday"
                    ]
                    df["is_pre_pre_holiday"] = basis_data[
                        f"{self.time_column}_is_pre_pre_holiday"
                    ]

            if self.split_by_group:
                df = pd.concat([df_train, df_oot], axis=0)
                df[self.group_column] = self.dev_data[self.group_column]
                return {"train": (df, self.dev_data[self.target_name])}

            return {
                "train": (df_train, self.dev_data[self.target_name]),
                "oot": (df_oot, self.oot_data[self.target_name]),
            }