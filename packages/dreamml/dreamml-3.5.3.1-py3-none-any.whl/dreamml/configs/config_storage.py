import sys
import warnings
from pathlib import Path
from typing import Dict, Union, List
from datetime import date
import pickle

import yaml
from hyperopt import hp

from dreamml.configs.config_checker import ConfigChecker
from dreamml.logging import get_logger, get_root_logger
from dreamml.modeling.models import *
from dreamml.modeling.models.boostaroota import BoostARoota
from dreamml.utils.errors import ConfigurationError
from dreamml.utils.temporary_directory import TempDirectory
from dreamml.utils.warnings import DMLWarning
from dreamml.configs._traffic_lights import default_traffic_lights, traffic_lights
from dreamml.configs._model_params import *

_logger = get_logger(__name__)

DREAMML_PATH = Path(__file__).parent.parent
NEVER_USED_FEATURES_PATH = DREAMML_PATH / "references" / "never_used_features.txt"

SUPPORTS_ALT_MODES_BY_TASK_DICT = {
    "regression": ["whitebox", "lama"],
    "binary": ["whitebox", "lama", "oot_potential"],
    "multiclass": ["lama"],
    "multilabel": [],
    "timeseries": ["etna"],
    "amts": [],
    "topic_modeling": [],
    "phrase_retrieval": [],
}


class ConfigStorage:
    """
    Основной класс для обработки конфига и установки дефолтных значений параметров
    """

    def __init__(self, config: Dict, config_file_path: str = None):
        root_logger = get_root_logger()
        root_logger.start_logging_session()

        self.config_checker = ConfigChecker(config)
        self.config_checker.check_config()

        if not self.config_checker.is_clean_config:
            raise ConfigurationError("Error in config")
        else:
            config = self.config_checker.config

        self.user_config = config

        if config_file_path:
            loaded_config = self.load_config_file(config_file_path)
            config = {**loaded_config, **config}

        self.random_seed = config.get("random_seed")
        self.device = config.get("device")
        self.use_compression = config.get("use_compression", False)

        # Выборка для разработки модели
        self.dev_data_path = config.get("dev_data_path")

        # Выборка для Out-Of-Time
        self.oot_data_path = config.get("oot_data_path")

        # Пользовательсякая выборка для train
        self.train_data_path = config.get("train_data_path")

        # Пользовательсякая выборка для valid
        self.valid_data_path = config.get("valid_data_path")

        # Пользовательсякая выборка для test
        self.test_data_path = config.get("test_data_path")

        # Директория для сохранения всех экспериментов
        path = config.get("path", "results/")
        self.path = str(Path(path).resolve())

        # Дир. с экспериментом для запуска с чекпоинта
        self.check_point_path = config.get("check_point_path")

        # Путь временной директории
        self.temp_dir_path = config.get("temp_dir_path", "./dml_spark_temp_dir")

        # Директория для сохранения необработанных данных
        self.data_path = config.get("data_path")

        # --- Общие параметры ---

        self.model_id = config.get("model_id", "dml")  # ID разрабатываемой модели
        self.task = config["task"]
        self.eval_metric = config.get("eval_metric")
        self.loss_function = config.get("loss_function")
        self.metric_params = config.get("metric_params", {})

        # Схема валидации модели: "auto", "hold-out", "cv"
        self.validation = config.get("validation")

        # Количество деревьев для обучения моделей
        self.n_estimators = config.get("n_estimators")

        # Количество итераций оптимизатора гиперпараметров моделей
        self.n_iterations = config.get("n_iterations")

        # Итоговое количество итераций оптимизатора гиперпараметров моделей
        self.n_iterations_used = (
            self.n_iterations if isinstance(self.n_iterations, int) else None
        )

        # см. self.set_stage_list(config)
        self.stage_list = config.get("stage_list", [])

        self.boostaroota_type = config.get("boostaroota_type", None)
        self.fitted_model = config.get("fitted_model", [])

        # --- Названия колонок ---

        # Название столбца с целевой меткой
        self.target_name = config.get("target_name")

        # Признаки, не участвующие в обучении
        self.drop_features = config.get("drop_features", [])

        # Служебные фичи для удаления, имя для группировки nlp семплов также написано в fitter
        self._service_fields = ["_group_nlp_aug_field"]

        self.never_used_features = config.get(
            "never_used_features", self._set_default_never_used_features()
        )

        # Признаки, которые должны остаться после отбора
        self.remaining_features = config.get("remaining_features", [])

        # Категориальные признаки
        self.categorical_features = config.get("categorical_features", [])
        if self.categorical_features is None:
            self.categorical_features = []

        # -------------------------NLP-------------------------------
        #  Параметры векторизации
        self.vectorization_params = config.get("vectorization_params", {})
        self.embedding_normalization = config.get("embedding_normalization", None)

        # Текстовые признаки
        self.text_features = config.get("text_features", [])
        self.text_features: List[str] = (
            [self.text_features]
            if isinstance(self.text_features, str)
            else self.text_features
        )
        self.text_features_preprocessed = []

        # Список этапов предобработки текста
        self.text_preprocessing_stages = config.get("text_preprocessing_stages", [])

        # Аугментация текстовых фичей
        self.text_augmentations = config.get("text_augmentations", [])

        # Доля объектов train выборки, которые будут аугментированы
        self.aug_p = config.get("aug_p")

        # Параметры для обучения базовой модели Bert
        self.bert_model_path = config.get("bert_model_path", None)
        self.max_length = config.get("max_length")
        self.unfreeze_layers = config.get("unfreeze_layers", "all")
        self.sampler_type = config.get("sampler_type", "weighted_random")
        self.optimizer_type = config.get("optimizer_type", "adamw")
        self.scheduler_type = config.get("scheduler_type", "linear")
        self.learning_rate = config.get("learning_rate")
        self.epochs = config.get("epochs")
        self.batch_size = config.get("batch_size")
        self.weight_decay = config.get("weight_decay")
        # --------------------------------------------------------------

        # Название столбца для разбиений с учетом группы
        self.group_column = config.get("group_column")

        # Название столбца для разбиений по времени
        self.time_column = config.get("time_column")

        # Формат колонки с временем
        self.time_column_format = config.get("time_column_format")

        # Указание периода времени для разбиения (день, неделя, месяц, год)
        # "day", "week", "month", "unique_month", "year" и т.д.
        # Если равен `min`, то разбиение будет среди уникальных значений колонки `time_column`
        self.time_column_period = config.get("time_column_period")

        # Разбиение по группам
        self.split_by_group = config.get("split_by_group", False)

        # Разбиение по периоду времени
        self.split_by_time_period = config.get("split_by_time_period", False)

        # Перемешивать ли выборки при разбиении
        self.shuffle = config.get(
            "shuffle", self.task not in ("timeseries", "amts", "topic_modeling")
        )

        # Сохранять ли распределение target при разбиениях (при классификации)
        self.stratify = config.get("stratify", self.task == "binary")

        # --- Параметры разбиения train-vaid-test-oot ---

        # Пропорции разбиения на train/valid/test
        self.split_params = config.get("split_params", [0.6, 0.2, 0.2])

        # Выделение test-выборки в соответствие с time_column
        self.oot_split_test = config.get("oot_split_test", False)

        # Выделение valid-выборки в соответствие с time_column
        self.oot_split_valid = config.get("oot_split_valid", False)

        # Выделение oot-выборки в случае, если не указан oot_data_path
        self.split_oot_from_dev = config.get("split_oot_from_dev", True)

        # Количество последних значений в time_column для выделения OOT выборки
        self.oot_split_n_values = config.get("oot_split_n_values")

        # --- Параметры разбиения для кросс-валидации ---

        # Разбиение на кросс-валидации для time series вида forward chaining
        self.time_series_split = config.get("time_series_split", False)

        # Разбиение на кросс-валидации для time series вида sliding window
        self.time_series_window_split = config.get("time_series_window_split", False)

        # Параметры разбиения time-series
        self.time_series_split_test_size = config.get(
            "time_series_split_test_size", None
        )
        self.time_series_split_gap = config.get("time_series_split_gap")

        # Количество групп (folds) для валидации модели
        self.cv_n_folds = config.get("cv_n_folds")

        self.validation_params = {
            "cv_params": config.get("validation_params", {}).get("cv_params", {})
        }

        # Используется ли кастомная кросс-валидация
        self.custom_cv = False
        # ---------------------------------------------------------------------------

        # Стратегия сэмплирования
        self.sample_strategy = config.get("sample_strategy")

        # см. self.set_stage_list(config)
        self.stage_list = config.get("stage_list", [])

        self.boostaroota_type = config.get("boostaroota_type", None)
        self.fitted_model = config.get("fitted_model", [])

        # Алгоритмы векторизации
        self.vectorization_algos = config.get("vectorization_algos", [])
        self.vectorization_params = config.get("vectorization_params", {})
        self.embedding_normalization = config.get("embedding_normalization", None)

        # Обязательные параметры для обучения базовой модели Bert
        self.bert_model_path = config.get("bert_model_path", None)
        self.max_length = config.get("max_length")
        self.unfreeze_layers = config.get("unfreeze_layers", "all")
        self.sampler_type = config.get("sampler_type", "weighted_random")
        self.optimizer_type = config.get("optimizer_type", "adamw")
        self.scheduler_type = config.get("scheduler_type", "linear")
        self.learning_rate = config.get("learning_rate")
        self.epochs = config.get("epochs")
        self.batch_size = config.get("batch_size")
        self.weight_decay = config.get("weight_decay")

        # Аугментация текстовых фичей
        self.use_sampling = config.get("use_sampling", False)
        self.text_augmentations = config.get("text_augmentations", [])

        # Доля объектов датасета, которые будут аугментированы
        self.aug_p = config.get("aug_p")

        # Optimizer: "auto", "distributed", "local", "optuna", "bayesian"
        self.optimizer = config.get("optimizer")

        # Временной лимит по работе оптимизатора в секундах
        self.optimizer_timeout = config.get("optimizer_timeout")

        # Для multilabel через OneVsRestClassifierWrapper
        self.parallelism = config.get(
            "parallelism", len(self.target_name) if self.task == "multilabel" else -1
        )

        # --- Параметры порогов отсечения ---

        # Порог для отбора признаков по метрике Джини
        self.gini_threshold = config.get("gini_threshold")
        self.gini_selector_abs_difference = config.get("gini_selector_abs_difference")
        self.gini_selector_rel_difference = config.get("gini_selector_rel_difference")
        self.gini_selector_valid_sample = config.get(
            "gini_selector_valid_sample", "valid"
        )

        # Порог для отбора перестановками
        self.permutation_threshold = config.get("permutation_threshold")
        self.permutation_top_n = config.get("permutation_top_n")

        # Порог для отбора признаков по метрике PSI
        self.psi_threshold = config.get("psi_threshold")
        self.psi_sample = config.get("psi_sample", "valid")

        # Порог для отбора признаков по корреляции
        self.corr_threshold = config.get("corr_threshold")
        self.corr_coef = config.get("corr_coef")

        # Порог для сохранения фич из словаря/странички отчёта other_models
        self.feature_threshold = config.get("other_models_feature_threshold")

        # min feat after Boostaroota
        self.min_n_features_to_stop = config.get("min_n_features_to_stop")

        # min feat to start Boostaroota
        self.min_n_features_to_start = config.get("min_n_features_to_start")

        # Не более итераций BR
        self.max_boostaroota_stage_iters = config.get("max_boostaroota_stage_iters")
        self.bootstrap_samples = config.get("bootstrap_samples")

        # Критерий остановки для batch_selection
        self.stop_criteria = config.get("stop_criteria", "model_score")

        # valid, test, oot
        self.sample_for_validation = config.get("sample_for_validation", "valid")

        self.weights_column = config.get("weights_column", None)

        # переопределится в трансформере, веса dev-данных
        self.weights = None

        # Параметры сохранения данных в Persistent storage
        self.save_to_ps = config.get("save_to_ps", False)
        self.save_to_ps_params = config.get("save_to_ps_params", {})

        # Параметры для совместимости
        self.multitarget = config.get("multitarget", [])

        # Регрессия
        self.min_percentile = config.get("min_percentile")
        self.max_percentile = config.get("max_percentile")
        self.log_target = config.get("log_target", False)

        # Multilabel
        self.target_with_nan_values = config.get("target_with_nan_values", False)

        # Multitarget report parameters
        self.show_save_paths: bool = config.get("show_save_paths", False)
        self.samples_to_plot: list = config.get(
            "samples_to_plot", ["train", "valid", "test", "OOT"]
        )
        self.plot_multi_graphs: bool = config.get("plot_multi_graphs", True)
        self.max_classes_plot: int = config.get("max_classes_plot")

        # TimeSeries

        # Трансформации ETNA для обогащения датасета фичами
        self.ts_transforms = config.get("ts_transforms", [])

        # Горизонт прогнозирования
        self.horizon = config.get("horizon")

        # Путь до датасета с экзогенными данными
        self.path_to_exog_data = config.get("path_to_exog_data", None)

        # Экзогенные столбцы в датасете exog_data
        self.known_future = config.get("known_future", "all")

        # Гранулярность временного столбца
        self.time_column_frequency = config.get("time_column_frequency", "D")

        # Трансформации ETNA для обогащения датасета фичами
        self.ts_transforms = config.get("ts_transforms", [])

        # Горизонт прогнозирования
        self.horizon = config.get("horizon", 5)

        # Путь до датасета с экзогенными данными
        self.path_to_exog_data = config.get("path_to_exog_data", None)

        # Экзогенные столбцы в датасете exog_data
        self.known_future = config.get("known_future", "all")

        # Гранулярность временного столбца
        self.time_column_frequency = config.get("time_column_frequency", "day")

        # Topic Modeling
        self.num_topics = config.get("num_topics")
        self.lda_passes = config.get("lda_passes")
        self.alpha = config.get("alpha")
        self.eta = config.get("eta")

        self.num_models = config.get("num_models")
        self.iterations = config.get("iterations")

        self.n_neighbors = config.get("n_neighbors")
        self.n_components = config.get("n_components")
        self.min_dist = config.get("min_dist")
        self.metric_umap = config.get("metric_umap", "euclidean")
        self.umap_epochs = config.get("umap_epochs")

        self.min_cluster_size = config.get("min_cluster_size")
        self.max_cluster_size = config.get("max_cluster_size")
        self.min_samples = config.get("min_samples")
        self.metric_hdbscan = config.get("metric_hdbscan", "euclidean")
        self.cluster_selection_method = config.get("cluster_selection_method", "eom")
        self.prediction_data = config.get("prediction_data", True)

        # Флаги использования моделей альтернативного моделирования

        # Флаг использования WhiteBox AutoML
        self.use_whitebox_automl = config.get("use_whitebox_automl", False)

        # Флаг использования OOT Potential
        self.use_oot_potential = config.get("use_oot_potential", False)

        self.use_lama = config.get("use_lama", False)
        self.use_etna = config.get("use_etna", False)

        # Валидация использования альтмода
        self._validate_using_alt_modes()

        # LAMA
        self.lama_time = config.get("lama_time")
        self.lama_hyper_params = {"lama_time": self.lama_time}
        self.lama_bounds_params = {}

        self.traffic_lights_config = config.get(
            "traffic_lights", *default_traffic_lights
        )
        self.traffic_lights = traffic_lights
        self.traffic_lights.update({self.eval_metric: self.traffic_lights_config})

        # Отображение результатов обучения
        self.verbose = config.get("verbose", False)

        self.models_params = {}

        model_params_pairs = [
            ("xgboost", XGBoostParams),
            ("lightgbm", LightGBMParams),
            ("catboost", CatBoostParams),
            ("pyboost", PyBoostParams),
            ("whitebox_automl", WhiteBoxAutoMLParams),
            ("boostaroota", BoostarootaParams),
            ("prophet", ProphetParams),
            ("linear_reg", LinearRegParams),
            ("log_reg", LogRegParams),
            ("lda", LDAParams),
            ("ensembelda", EnsembeldaParams),
            ("bertopic", BERTopicParams),
            ("bert", BertParams),
        ]
        for model_name, param_class in model_params_pairs:
            if model_name in self.fitted_model:
                self.models_params[model_name] = param_class(self)

        # Гипер параметры моделей и сетки оптимизатора
        for model_name in self.models_params.keys():
            setattr(
                self, f"{model_name}_hyper_params", None
            )  # см. метод set_models_and_opt_params
            setattr(self, f"{model_name}_bounds_params", None)

        self._check_never_used_features()
        self.set_save_to_ps_params()
        self.set_models_and_opt_params(config)
        self.set_stage_list(config)

        self.ignore_third_party_warnings = config.get(
            "ignore_third_party_warnings", True
        )

        if self.ignore_third_party_warnings:
            warnings.filterwarnings("ignore")
            warnings.filterwarnings("default", category=DMLWarning)

        self.subtask = self._identify_subtask()

    def _check_never_used_features(self):
        for feature in self.categorical_features:
            if feature in self.never_used_features:
                msg = f"The feature {feature} is found in never_used_features. "
                msg += f"Please remove the featrue {feature} from "
                msg += f"the categorical_features parameter or from the never_used_features file."
                raise ValueError(msg)

    def _identify_subtask(self):
        if len(self.vectorization_algos) > 0 and len(self.text_features) > 0:
            return "nlp"
        return "tabular"

    def get(self, name: str, default=None):
        return getattr(self, name, default)

    def set(self, name: str, value):
        setattr(self, name, value)

    def __getitem__(self, value):
        return getattr(self, value, None)

    def set_save_to_ps_params(
        self,
        storage_name: Union[str, None] = "storage_name_to_save",
        table_name: Union[str, None] = "table_name_to_save",
        prefix: Union[str, None] = "dml",
        suffix: Union[str, None] = date.today().strftime("%Y%m%d"),
    ):
        # Название таблиц имеет формат: (storage_name).(prefix)_(model_id)_(table_name)_(train/valid/test)_(suffix)_(n)"
        self.save_to_ps_params = {
            "storage_name": storage_name,
            "table_name": table_name,
            "prefix": prefix,
            "suffix": suffix,
        }

    def set_save_to_ps_params(self):
        default_params = {
            "storage_name": "storage_name_to_save",
            "table_name": "table_name_to_save",
            "prefix": "dml",
            "suffix": date.today().strftime("%Y%m%d"),
            "model_id": self.model_id,
        }
        # Название таблиц имеет формат: (storage_name).(prefix)_(model_id)_(table_name)_(train/valid/test)_(suffix)_(n)"
        for key, value in default_params.items():
            if key not in self.save_to_ps_params:
                self.save_to_ps_params[key] = value

    @staticmethod
    def _set_default_never_used_features() -> List:
        try:
            with open(NEVER_USED_FEATURES_PATH, "r", encoding="utf-8") as file:
                never_used_features = file.read().strip().split("\n")
        except FileNotFoundError:
            never_used_features = []
            warnings.warn(
                f"Файл с названиями неиспользуемых признаков (never_used_features.txt) не найден. "
                f"Файл по умолчанию расположен в {NEVER_USED_FEATURES_PATH}",
                DMLWarning,
                stacklevel=2,
            )

        return never_used_features

    @staticmethod
    def _set_parameters_dict(params_name: str, config: Dict) -> Dict:
        params = config.get(params_name, {})
        if isinstance(params, str) and params.split(".")[-1] in ["pickle", "pkl"]:
            with open(params, "rb") as f:
                return pickle.load(f)
        elif isinstance(params, dict):
            return params
        else:
            raise Exception(
                "Гиперпараметры можно задать с помощью словаря (dict) или с помощью пути до pickle файла (.pkl, .pickle)"
            )

    def set_models_and_opt_params(self, config: Dict):
        for model_name, model_params in self.models_params.items():
            hyper_params = model_params.get_hyper_params()
            bounds_params = model_params.get_bounds()
            fixed_params = model_params.get_fixed_params()

            # Обогащeние словаря с фиксированными гиперпараметрами
            for k in hyper_params:
                if k not in fixed_params:
                    fixed_params[k] = hyper_params[k]

                # Объединение пользовательских параметров с дефолтными
                user_bounds = self._set_parameters_dict(
                    f"{model_name}_bounds_params", config
                )
                bounds_params = model_params.merge_with_user_params(
                    bounds_params, user_bounds
                )

                setattr(self, f"{model_name}_hyper_params", hyper_params)
                setattr(self, f"{model_name}_bounds_params", bounds_params)
                setattr(self, f"{model_name}_fixed_params", fixed_params)

    def set_stage_list(self, config):
        """
        Если поданы словари _fix - стадия оптимизации пропускается и заменяется на fix.
        Если это не так, то появляется ошибка.
        Если не поданы словари fix на вход, стадии не изменяются
        """
        self.stage_list = config.get("stage_list", [])
        models_list = self.fitted_model
        if (
            self._set_parameters_dict("xgboost_fixed_params", config) == {}
            and self._set_parameters_dict("lightgbm_fixed_params", config) == {}
            and self._set_parameters_dict("catboost_fixed_params", config) == {}
            and self._set_parameters_dict("pyboost_fixed_params", config) == {}
            and self._set_parameters_dict("log_reg_fixed_params", config) == {}
        ):
            pass
        elif (
            (self._set_parameters_dict("xgboost_fixed_params", config) != {})
            + (self._set_parameters_dict("lightgbm_fixed_params", config) != {})
            + (self._set_parameters_dict("catboost_fixed_params", config) != {})
            + (self._set_parameters_dict("pyboost_fixed_params", config) != {})
            + (self._set_parameters_dict("log_reg_fixed_params", config) != {})
        ) == len(models_list):
            if "opt" in self.stage_list:
                self.stage_list[self.stage_list.index("opt")] = "fix"
            else:
                pass
        elif self.task == "timeseries":
            pass
        else:
            raise Exception(
                "Полный пропуск оптимизации доступен только для всех моделей одновременно"
            )

        # Для boostaroota
        self.min_n_features_to_start = "tmp"

    @staticmethod
    def get_batch_selection_model_params():
        shap_fraction_sample = 1.0

        params = {
            "step_10": {
                "features_step": 10,
                "min_features": 40,
                "fraction_sample": shap_fraction_sample,
            },
            "step_5": {
                "features_step": 5,
                "min_features": 10,
                "fraction_sample": shap_fraction_sample,
            },
            "step_10_down": {
                "features_step": 10,
                "min_features": 40,
                "fraction_sample": shap_fraction_sample,
            },
            "step_5_down": {
                "features_step": 5,
                "min_features": 20,
                "fraction_sample": shap_fraction_sample,
            },
            "step_1_down": {
                "features_step": 1,
                "min_features": 1,
                "fraction_sample": shap_fraction_sample,
            },
        }

        return params

    def get_model_by_str(self, model_name: str):
        """
        Возвращает обертку, гиперпараметры и параметры для оптимизации модели.
        """
        models_dict = {
            "xgboost": XGBoostModel,
            "lightgbm": LightGBMModel,
            "catboost": CatBoostModel,
            "pyboost": PyBoostModel,
            "whitebox": None,
            "boostaroota": BoostARoota,
            "log_reg": LogRegModel,
            "lda": LDAModel,
            "ensembelda": EnsembeldaModel,
            "bertopic": BERTopicModel,
            "bert": BertModel,
        }

        model = models_dict[model_name.lower()]
        model_hyper_params = getattr(self, f"{model_name.lower()}_hyper_params")
        model_bounds_params = getattr(self, f"{model_name.lower()}_bounds_params")

        return model, model_hyper_params, model_bounds_params

    @staticmethod
    def get_hyperopt_grid(bound_params):
        bound_steps_grid = {  # Шаг подбора гиперпараметров
            "lr": 0.025,  # "pyboost"
            "learning_rate": 0.025,  # "xgboost"
            "min_child_weight": 10,  # "xgboost"
            "colsample_bytree": 0.05,  # "xgboost"
            "subsample": 0.05,  # "xgboost"
            "reg_lambda": 0.1,  # "xgboost", "lightgbm"
            "reg_alpha": 0.1,  # "xgboost", "lightgbm"
            "gamma": 0.05,  # "xgboost"
            "colsample_bylevel": 0.1,  # "catboost"
            "min_split_gain": 0.05,  # "lightgbm"
        }

        hyperopt_grid = {}
        for x in bound_params:
            if x in ["lr", "learning_rate"]:
                hyperopt_grid[x] = hp.loguniform(
                    x, bound_params[x][0], bound_params[x][1]
                )
            else:
                hyperopt_grid[x] = hp.quniform(
                    x,
                    bound_params[x][0],
                    bound_params[x][1],
                    bound_steps_grid.get(x, 1.0),
                )

        return hyperopt_grid

    @staticmethod
    def get_bert_grid_params(bound_params):
        bert_bound_params = {
            "learning_rate": (2e-6, 1e-4),
            "epochs": (2, 5),
            "batch_size": (8, 32),
            "weight_decay": (2e-5, 2e-3),
            "sampler_type": (
                "weighted_random",
                "random",
                "sequential",
                "subset_random",
            ),
            "optimizer_type": ("adamw", "adam", "rmsprop", "sgd"),
            "scheduler_type": (
                "linear",
                "exponential",
                "step",
                "reduce_on_plateau",
                "one_cycle_lr",
                "cyclic_lr",
            ),
        }

        for param_name, param in bound_params.items():
            if param_name not in bert_bound_params:
                bert_bound_params[param_name] = param

        return bert_bound_params

    @staticmethod
    def get_logistic_grid_params(bound_params):
        logistic_bound_params = {
            "penalty": ("l1", "l2", "elasticnet", "none"),
            "C": (1e-5, 1e5),
            "solver": ("liblinear", "saga", "lbfgs", "newton-cg", "sag"),
            "max_iter": (100, 2000),
            "tol": (1e-6, 1e-2),
        }

        for param_name, param in bound_params.items():
            if param_name not in logistic_bound_params:
                logistic_bound_params[param_name] = param

        return logistic_bound_params

    def get_temp_dir(self) -> TempDirectory:
        """
        Возвращает объект создания временной папки.
        """
        temp_dir = TempDirectory(path=self.temp_dir_path)
        return temp_dir

    def get_all_params(self):
        """
        Возвращает словарь со всеми параметрами конфига и их текущими значениями.
        """
        result = {}
        for attribute, value in self.__dict__.items():
            result[attribute] = value
        return result

    def save_config_file(self, path: str = "./config.yaml"):
        dict_to_save = self.get_all_params()
        with open(path, "w", encoding="utf-8") as file:
            yaml.dump(dict_to_save, file, allow_unicode=True)

    @staticmethod
    def load_config_file(path: str = "./config.yaml"):
        try:
            with open(path, "r", encoding="utf-8") as file:
                loaded_data = yaml.unsafe_load(file)
        except FileNotFoundError as e:
            _logger.exception(f"FileNotFoundError {e}")
            loaded_data = {}
        return loaded_data

    def _validate_using_alt_modes(self):

        use_alt_modes_dict = {
            "whitebox": self.use_whitebox_automl,
            "lama": self.use_lama,
            "oot_potential": self.use_oot_potential,
            "etna": self.use_etna,
        }

        supports_task_list = SUPPORTS_ALT_MODES_BY_TASK_DICT[self.task]

        for alt_mode, flag in use_alt_modes_dict.items():
            if flag and alt_mode not in supports_task_list:
                raise ValueError(
                    f"\nАльтмод {alt_mode} не поддерживается для задачи {self.task}.\n"
                    f"Поддерживаемые AltModes для текущей задачи: {supports_task_list}."
                )