import os
import platform
import contextlib
import sys
import uuid
import time
import subprocess
import shutil
import pickle
from datetime import date
from typing import Optional, List
from copy import deepcopy
from pathlib import Path

import yaml
from pyspark.sql import functions as F
from IPython.display import display, Javascript
import ipynbname

import dreamml
from dreamml.data._hadoop import create_spark_session, stop_spark_session
from dreamml.configs.config_storage import ConfigStorage
from dreamml.logging import get_logger

ETNA_PIPELINE_DIR = "etna_pipeline"
OTHER_MODELS_DIR = "other_models"
_logger = get_logger(__name__)


# TODO переделать всё в один класс, когда переделаем регрессию под новый вид
class BaseSaver:
    """
    Базовый класс от которого наследуются.
    Нужен для обратной совместимости между новым пайплайном для классификации и старым для регрессии
        Перед тем, как сохранить данные, объект проверяет наличие  каталога
    path. Если каталог отсутствуют - то создается структура каталогов
    ({path} - {experiment_number} - config / docs / images / models),
    если каталог присутствует, то создается структура
    ({experiment_number} - config / docs / images / models).

    Предназначение каталогов
    ------------------------
    - {path} - каталог, для сохранения выходной информации всех запусков.
    - {path}/{experiment_number} - каталог, для сохранения выходной
                                   информации данного эксперимента.
    - {path}/{experiment_number}/config - каталог для записи конфига.
    - {path}/{experiment_number}/docs - каталог для записи отчета.
    - {path}/{experiment_number}/images - каталог для записи графиков.
    - {path}/{experiment_number}/models - каталог для записи моделей.
    - {path}/{experiment_number}/cpts - каталог для сохранения чекпоинтов
     папйплайна обучения
    - {path}/{experiment_number}/other_models - каталог для сохранения моделей
     с этапов обучения множества моделей (batch stage)

    Parameters
    ----------
    models: dict
        Словарь, где ключ - название модели,
        значение - экземпляр модели со стандартизованным
        API для DS-Template.

    config: ConfigStorage
        Класс с конфигурацией эксперимента.

    path: string, optional, default = "runs"
        Путь для сохранения выходных файлов эксперимента.

    prefix_name: string, optional = ""
        Префикс для директории с артефактами моделирования.
        По умолчанию, не используется. Предназначен для обучения
        моделей в цикле.

    Attributes
    ----------
    experiment_path: string
        Путь с номером эксперимента.

    """

    def __init__(self, path: str):
        self._results_path = path
        self._dml_version_file = "dml_version.txt"
        self._experiment_path = None
        self._run_number = None
        self._run_string = "_run_"

    @property
    def run_number(self):
        if self._run_number is None:
            raise ValueError("Experiment dir is not created yet!")

        return self._run_number

    @property
    def run_prefix(self) -> str:
        return "dml"

    @property
    def experiment_dir_name(
        self,
    ) -> str:
        return f"{self.run_prefix}{self._run_string}{self.run_number}"

    def get_run_number_from_experiment_dir(self, name):
        return name.split(self._run_string)[-1]

    @property
    def experiment_path(self):
        if self._experiment_path is None:
            raise ValueError("Experiment dir is not created yet!")

        return self._experiment_path

    def save_dependencies(self) -> None:
        """
        Сохранение необходимый зависимостей для
        воспроизведения работы модели.

        """
        output = subprocess.check_output(
            [sys.executable, "-m", "pip", "freeze"]
        ).decode("utf-8")

        with open(f"{self.experiment_path}/requirements.txt", "w") as f:
            f.write(output)

    @staticmethod
    def get_notebook_path_and_save():
        """
        Определение названия текущего Jupyter-Notebook.

        Returns
        -------
        ipynb_name: str
            Название ноутбука, в котором производятся расчеты.

        """
        if platform.system() == "Windows":
            nb_path = ipynbname.path()
            return nb_path
        else:
            magic = str(uuid.uuid1()).replace("-", "")
            print(magic)

            display(Javascript("IPython.notebook.save_checkpoint();"))
            nb_name = None

            tries = 0
            while nb_name is None:
                with contextlib.suppress(Exception):
                    time.sleep(1)
                    nb_name = subprocess.check_output(
                        f"grep -l {magic} *.ipynb", shell=True
                    )
                    nb_name = nb_name.decode().strip()

                tries += 1

                if tries > 1500:
                    raise RuntimeError(
                        "Can't determine the name of the current notebook."
                    )

            return os.path.join(os.getcwd(), nb_name)

    def _is_dml_results_dir(self, path: str) -> bool:
        """
        Проверяет является ли указанный путь папкой с экспериментом DreamML
        с помощью проверки наличия файла `self._dml_version_file` в директории.

        :param path: Путь для проверки
        :return: bool
        """
        dml_version_path = os.path.join(path, self._dml_version_file)
        return os.path.isdir(path) and os.path.exists(dml_version_path)

    def _save_dml_version(self, path: str) -> None:
        """
        Сохраняет в папку по указанному пути файл с текущей версией DreamML.

        :param path:
        :return:
        """
        dml_version_path = os.path.join(path, self._dml_version_file)

        with open(dml_version_path, "w") as f:
            f.write(dreamml.__version__)

    def get_dreamml_experiment_dirs(self) -> List[str]:
        """
        Возвращает список папок с экспериментами DreamML
        """
        dml_dirs = [
            p
            for p in os.listdir(self._results_path)
            if self._is_dml_results_dir(os.path.join(self._results_path, p))
        ]

        return dml_dirs

    def create_experiment_dir(self) -> None:
        """
        Создание основного каталога для сохранения элемнетов, полученных
        в ходе эксперимента, и подкаталогов для хранения выходных данных
        о конкретном эксперименте. При вызове - осуществляется попытка
        создать каталога self.path и self.path/1/, если каталог уже
        существует - то осуществляется поиск максимального вложенного
        каталога в self.path и создается каталог с номером на 1 больше.

        """
        os.makedirs(self._results_path, exist_ok=True)

        dml_dirs = self.get_dreamml_experiment_dirs()

        self._run_number = len(dml_dirs) + 1
        self._experiment_path = os.path.join(
            self._results_path, self.experiment_dir_name
        )

        if os.path.exists(self._experiment_path):
            for try_idx in range(1, 100):
                dir_ = self._experiment_path + f"({try_idx})"
                if not os.path.exists(dir_):
                    self._experiment_path = dir_
                    break

        os.makedirs(self.experiment_path, exist_ok=True)

        dirs_to_create = [
            "models",
            "models/hyperparams",
            "models/used_features",
            "config",
            "images",
            "notebooks",
            "docs",
            "data",
            "cpts",
            "logs",
        ]

        for d in dirs_to_create:
            dir_path = os.path.join(self.experiment_path, d)
            os.mkdir(dir_path)

        self._save_dml_version(self.experiment_path)

    @staticmethod
    def save_dict_to_txt(dictionary, filename, mode):
        """
        Словарь вида:
           {
           model_name1 : {
                           'features' : list,
                           'hyperparams' : dict
                       }
           model_name2 : {
                           'features' : list,
                           'hyperparams' : dict
                       }
           }
        """
        with open(filename, mode, encoding="utf-8") as f:
            for model in dictionary:
                f.writelines(model)
                f.writelines(":\n")
                for item in dictionary[model]:
                    f.writelines("\t" + item + " : " + str(dictionary[model][item]))
                    f.writelines("\n")
                f.writelines("\n")
            f.writelines(37 * "#")
            f.writelines("\n\n")


class ArtifactSaver(BaseSaver):
    """
    Saver для сохранения выходных файлов пайплайна.
    Перед тем, как сохранить данные, объект проверяет наличие  каталога
    path. Если каталог отсутствуют - то создается структура каталогов
    ({path} - {experiment_number} - config / docs / images / models),
    если каталог присутствует, то создается структура
    ({experiment_number} - config / docs / images / models).

    Предназначение каталогов
    ------------------------
    - {path} - каталог, для сохранения выходной информации всех запусков.
    - {path}/{experiment_number} - каталог, для сохранения выходной
                                   информации данного эксперимента.
    - {path}/{experiment_number}/config - каталог для записи конфига.
    - {path}/{experiment_number}/docs - каталог для записи отчета.
    - {path}/{experiment_number}/images - каталог для записи графиков.
    - {path}/{experiment_number}/models - каталог для записи моделей.
    - {path}/{experiment_number}/cpts - каталог для сохранения чекпоинтов
     папйплайна обучения
    - {path}/{experiment_number}/other_models - каталог для сохранения моделей
     с этапов обучения множества моделей (batch stage)

    Parameters
    ----------
    config: ConfigStorage
        Класс с конфигурацией эксперимента.

    Attributes
    ----------
    dir_: string
        Путь с номером эксперимента.

    """

    def __init__(self, config: ConfigStorage) -> None:
        super().__init__(config.path)
        self.config = config
        self._custom_data_split = self.config.dev_data_path is None
        self.target_name = config.target_name
        self.model_id = config.model_id.lower()
        self.task = config.task

    @property
    def run_prefix(self):
        target_part = (
            self.target_name if isinstance(self.target_name, str) else self.task
        )

        return f"{self.model_id}_{target_part}".lower()

    @property
    def dev_report_name(self):
        return f"{self.model_id}_dev_report_run_{self.run_number}"

    def create_experiment_dir(self) -> None:
        """
        Создание основного каталога для сохранения элемнетов, полученных
        в ходе эксперимента, и подкаталогов для хранения выходных данных
        о конкретном эксперименте. При вызове - осуществляется попытка
        создать каталога self.path и self.path/1/, если каталог уже
        существует - то осуществляется поиск максимального вложенного
        каталога в self.path и создается каталог с номером на 1 больше.

        """
        super(ArtifactSaver, self).create_experiment_dir()
        os.mkdir(f"{self.experiment_path}/{OTHER_MODELS_DIR}/")
        os.mkdir(f"{self.experiment_path}/{OTHER_MODELS_DIR}/hyperparams/")
        os.mkdir(f"{self.experiment_path}/{OTHER_MODELS_DIR}/used_features/")
        if self.task == "timeseries":
            os.mkdir(f"{self.experiment_path}/{ETNA_PIPELINE_DIR}/")

    def save_data(
        self, data: dict, dropped_data: dict = None, etna_eval_set: dict = None
    ) -> None:
        """
        Сохранение словаря с данными.
        Предполагается, что данные сохраняются после
        разбиения на train / valid / test для обеспечения
        полной воспроизводимости результатов моделирования.

        Parameters
        ----------
        dropped_data: dict
            Словарь с набором данных, где ключ - название
            выборки, значение датафрейм с удалёнными фичами
            из флага drop_features
        data: dict
            Словарь с набором данных, где ключ - название
            выборки, значение - кортеж с матрицей признаков
            и вектором целевой переменной.

        """

        # FIXME AMTS
        if self.config.task == "amts":
            eval_sets_path = os.path.join(self.experiment_path, "data", "eval_sets.pkl")
            print("Saving dict with data to:", eval_sets_path)
            pickle.dump(data, open(eval_sets_path, "wb"))
            if self.config.save_to_ps:
                self.save_data_to_hdfs(data=data, **self.config.save_to_ps_params)
            return

        if etna_eval_set is not None:
            pickle.dump(
                etna_eval_set,
                open(f"{self.experiment_path}/data/etna_eval_sets.pkl", "wb"),
            )
            _logger.info(f"Saved to {self.experiment_path}/data/etna_eval_sets.pkl")

        if dropped_data and not dropped_data["train"].empty:
            for key in data:
                for name in list(dropped_data[key].columns):
                    data[key][0][name] = dropped_data[key][name]
        eval_sets_path = os.path.join(self.experiment_path, "data", "eval_sets.pkl")
        _logger.info(f"Saving dict with data to: {eval_sets_path}")
        pickle.dump(data, open(eval_sets_path, "wb"))
        if self.config.save_to_ps:
            self.save_data_to_hdfs(data=data, **self.config.save_to_ps_params)

    def save_data_to_hdfs(
        self,
        data: dict,
        spark_config=None,
        storage_name: str = None,
        table_name: str = None,
        prefix: str = "dml",
        suffix: str = date.today().strftime("%Y%m%d"),
        model_id: str = None,
    ) -> None:
        """
        Сохранение данных в HDFS.

        Parameters
        ----------
        data: dict
            Словарь с набором данных, где ключ - название
            выборки, значение - кортеж с матрицей признаков
            и вектором целевой переменной.

        spark_config: SparkConf
            Конфигурации спарк сессии

        Название таблиц имеет формат: (cluster_name).(prefix)_(model_id)_(table_name)_(train/valid/test)_(suffix)_(n)"

        storage_name: str
            Название хранилища для сохранения данных

        table_name: str
            Название таблицы для сохранения данных

        prefix: str
            Префикс к названию таблицы, для удобства пользования (по учолчанию: 'dml')

        suffix: str
            Суффикс после названия таблицы и выборки, для удобства пользования (по учолчанию: сегодняшняя дата)

        model_id: str
            id модели, для удобства пользования
        """
        # !!! Должен быть полный датасет, без дропнутых признаков.
        if not storage_name:
            if self._custom_data_split:
                storage_name = self.config.train_data_path.split(".")[0]
            else:
                storage_name = self.config.dev_data_path.split(".")[0]

        if not table_name:
            if self._custom_data_split:
                table_name = self.config.train_data_path.split(".")[1]
            else:
                table_name = self.config.dev_data_path.split(".")[1]

        prefix = prefix + "_" if prefix else ""
        suffix = "_" + suffix if suffix else ""
        model_id = model_id + "_" if model_id else ""

        temp_dir = self.config.get_temp_dir()
        spark = create_spark_session(spark_config=spark_config, temp_dir=temp_dir)
        list_of_tables = spark.catalog.listTables(storage_name)

        list_of_table_names = [x.name for x in list_of_tables]

        # Создаем датафреймы для записи в Persistent Storage.
        data_to_save = {}
        for k in data.keys():
            if k.upper() != "OOT":
                df = data[k][0]
                df[self.config.target_name] = data[k][1]
                data_to_save[k] = spark.createDataFrame(df)

        n = 0
        for k in data_to_save.keys():
            result_name = f"{prefix}{model_id}{table_name}_{k}{suffix}"  # result_name - имя итогового датафрейма.

            # Находим следующий свободный номер для датафрейма.
            if n == 0:
                while result_name in list_of_table_names:
                    n += 1
                    result_name = f"{prefix}{model_id}{table_name}_{k}{suffix}_{n}"
            else:
                result_name = f"{prefix}{model_id}{table_name}_{k}{suffix}_{n}"

            # Берем существующий датафрейм с последним номером и новый, считаем на них статистики
            # (количество строк, столбцов и среднее значение по целевой переменной).
            if n == 0:
                table_name_for_comparison = (
                    None  # table_name_for_comparison - имя существующего датафрейма
                )
            elif n == 1:
                table_name_for_comparison = (
                    f"{prefix}{model_id}{table_name}_{k}{suffix}"
                )
            else:
                table_name_for_comparison = (
                    f"{prefix}{model_id}{table_name}_{k}{suffix}_{n - 1}"
                )

            if table_name_for_comparison:
                df_for_comparison = spark.table(
                    f"{storage_name}.{table_name_for_comparison}"
                )

                df_for_comparison.cache()
                data_to_save_stats = (
                    data_to_save[k]
                    .select(F.mean(F.col(self.config["target_name"])).alias("mean"))
                    .collect()
                )
                df_for_comparison_stats = df_for_comparison.select(
                    F.mean(F.col(self.config["target_name"])).alias("mean")
                ).collect()
                stats_df = {
                    "rows": {
                        "old": df_for_comparison.count(),
                        "new": data_to_save[k].count(),
                    },
                    "cols": {
                        "old": len(df_for_comparison.columns),
                        "new": len(data_to_save[k].columns),
                    },
                    "mean": {
                        "old": df_for_comparison_stats[0]["mean"],
                        "new": data_to_save_stats[0]["mean"],
                    },
                }

                # Сравниваем количество строк, столбцов и среднее значение по целевой переменной и если все равны,
                # то перезаписываем поледний датафрейм, если нет, то создаем новый.
                if (
                    stats_df["rows"]["new"] == stats_df["rows"]["old"]
                    and stats_df["cols"]["new"] == stats_df["cols"]["old"]
                    and stats_df["mean"]["new"] == stats_df["mean"]["old"]
                ):
                    result_name = table_name_for_comparison

            data_to_save[k].write.saveAsTable(
                f"{storage_name}.{result_name}", mode="Overwrite"
            )
            _logger.info(f"Saved to Persistent Storage: {storage_name}.{result_name}")

        stop_spark_session(spark, temp_dir=temp_dir)

    def save_artifacts(
        self,
        models: dict,
        other_models: dict = None,
        feature_threshold=100,
        encoder=None,
        ipynb_name: Optional[str] = None,
        etna_pipeline: Optional = None,
        vectorizers: Optional = None,
    ) -> None:
        """
        Сохранение моделей и объектов моделирования.
        Предполагается, что в models расположены все
        объекты, необходимые для воспроизведения модели:
        transformers, encoders, estimators, ....

        Parameters
        ----------
        models: dict
            Словарь с объектами, необходимыми для воспроизведения
            работы модели. Ключ словаря - название стадии обработки
            данных (transformer / encoder / ... /), значение - обученный
            объект.
        other_models: dict
            Словарь с моделями, которые получены на этапе обучения множества моделей (e.g. Batch Stage)
        ipynb_name: Optional[str]
            Путь до jupyter ноутбука c экспериментом
        feature_threshold: int
            Порог сложности моделей из other_models для сохранения
        encoder:
            Энкодер для переменных
        ipynb_name: str
            Название ноутбука
        etna_pipeline: Optional[EntaPipeline]
            Объект класса EtnaPipeline для задачи timeseries
        vectorizers: Optional[Dict[str, BaseVectorization]]
            Словарь с векторизаторами текстовых признаков для задачи multiClass, binary classification
        """
        models_ = deepcopy(models)
        imp = [col for col in models_ if "importance" in col]
        for col in imp:
            _ = models_.pop(col)

        summary_stages_info = dict()
        for model in models_:
            pickle.dump(
                models_[model], open(f"{self.experiment_path}/models/{model}.pkl", "wb")
            )

            pickle.dump(
                models_[model].params,
                open(
                    f"{self.experiment_path}/models/hyperparams/{model}.hyperparams.pkl",
                    "wb",
                ),
            )

            pickle.dump(
                models_[model].used_features,
                open(
                    f"{self.experiment_path}/models/used_features/{model}.used_features.pkl",
                    "wb",
                ),
            )

            summary_stages_info[model] = {
                "used_features": models_[model].used_features,
                "hyperparams": models_[model].params,
            }
        self.save_dict_to_txt(
            summary_stages_info,
            f"{self.experiment_path}/summary_stages_info.txt",
            mode="w",
        )

        if encoder:
            pickle.dump(
                encoder, open(f"{self.experiment_path}/models/encoder.pkl", "wb")
            )

        if other_models:
            self.save_other_models(other_models, feature_threshold=feature_threshold)
        self.config.save_config_file(path=f"{self.experiment_path}/config/config.yaml")

        self.save_dependencies()
        shutil.copy2(
            ipynb_name, f"{self.experiment_path}/notebooks/fit_model_notebook.ipynb"
        )

        if etna_pipeline is not None:
            self.save_etna_pipeline(etna_pipeline)

        if isinstance(vectorizers, dict) and len(vectorizers) != 0:
            self.save_vectorizers(vectorizers)

    def save_other_models(self, other_models: dict, feature_threshold: int = 100):
        """
        Метод сохранения моделей с этапа обучения множества моделей,
         которые ниже определённого порога сложности
        Parameters
        ----------
        other_models: dict
            Словарь с моделями с этапа обучения множества моделей
        feature_threshold: int
            Порог сложности моделей для сохранения
        """
        chosen_models = {
            n: m["estimator"]
            for n, m in other_models.items()
            if len(m["estimator"].used_features) <= feature_threshold
        }
        other_models_path = Path(self.experiment_path) / OTHER_MODELS_DIR
        summary_stages_info = dict()
        for model_ in chosen_models:
            with open(other_models_path / f"{model_}.pkl", "wb") as f:
                pickle.dump(chosen_models[model_], f)
            with open(
                other_models_path / f"hyperparams/{model_}.hyperparams.pkl", "wb"
            ) as f:
                pickle.dump(chosen_models[model_].params, f)
            with open(
                other_models_path / f"used_features/{model_}.used_features.pkl", "wb"
            ) as f:
                pickle.dump(chosen_models[model_].used_features, f)
            summary_stages_info[model_] = {
                "used_features": chosen_models[model_].used_features,
                "hyperparams": chosen_models[model_].params,
            }
        self.save_dict_to_txt(
            summary_stages_info,
            f"{self.experiment_path}/summary_stages_info.txt",
            mode="a",
        )

    def save_etna_pipeline(self, etna_pipeline):
        etna_pipeline.save(
            Path(self.experiment_path) / ETNA_PIPELINE_DIR / "etna_pipeline.zip"
        )

    def save_vectorizers(self, vectorizers: dict):
        for vec_name, vectorizer in vectorizers.items():
            pickle.dump(
                vectorizer, open(f"{self.experiment_path}/models/{vec_name}.pkl", "wb")
            )


class ArtifactSaverCompat(BaseSaver):
    """
    Аналог ArtifactSaver нужный для обратной совместимости с модулями не обновлёнными в релизе 2.0
    Saver для сохранения выходных файлов пайплайна.
    Перед тем, как сохранить данные, объект проверяет наличие  каталога
    path. Если каталог отсутствуют - то создается структура каталогов
    ({path} - {experiment_number} - config / docs / images / models),
    если каталог присутствует, то создается структура
    ({experiment_number} - config / docs / images / models).

    Предназначение каталогов
    ------------------------
    - {path} - каталог, для сохранения выходной информации всех запусков.
    - {path}/{experiment_number} - каталог, для сохранения выходной
                                   информации данного эксперимента.
    - {path}/{experiment_number}/config - каталог для записи конфига.
    - {path}/{experiment_number}/docs - каталог для записи отчета.
    - {path}/{experiment_number}/images - каталог для записи графиков.
    - {path}/{experiment_number}/models - каталог для записи моделей.

    Parameters
    ----------
    models: dict
        Словарь, где ключ - название модели,
        значение - экземпляр модели со стандартизованным
        API для DS-Template.

    config: dict
        Словарь с конфигурацией эксперимента.

    path: string, optional, default = "runs"
        Путь для сохранения выходных файлов эксперимента.

    prefix_name: string, optional = ""
        Префикс для директории с артефактами моделирования.
        По умолчанию, не используется. Предназначен для обучения
        моделей в цикле.

    Attributes
    ----------
    dir_: string
        Путь с номером эксперимента.

    """

    def __init__(self, config: dict, path: str = "runs", prefix_name: str = "") -> None:
        super().__init__(path)
        self.config = config
        self.target_name = config.get("target_name", "")
        self.model_id = config.get("model_id", "model_id").lower()
        if self.target_name:
            self.target_name = f"{self.model_id}_{self.target_name}{prefix_name}_run_"
            self.target_name = self.target_name.lower()

        self.create_experiment_dir()

    def save_data(self, data: dict, dropped_data: dict) -> None:
        """
        Сохранение словаря с данными.
        Предполагается, что данные сохраняются после
        разбиения на train / valid / test для обеспечения
        полной воспроизводимости результатов моделирования.

        Parameters
        ----------
        data: dict
            Словарь с набором данных, где ключ - название
            выборки, значение - кортеж с матрицей признаков
            и вектором целевой переменной.

        """
        if not dropped_data["train"].empty:
            for key in data.keys():
                for name in list(dropped_data[key].columns):
                    data[key][0][name] = dropped_data[key][name]
        pickle.dump(data, open(f"{self.experiment_path}/data/eval_sets.pkl", "wb"))
        _logger.info(f"Saved to {self.experiment_path}/data/eval_sets.pkl")
        if self.config.get("save_to_ps"):
            self.save_data_to_hdfs(data=data, **self.config["save_to_ps_params"])

    def save_data_to_hdfs(
        self,
        data: dict,
        spark_config=None,
        storage_name: str = None,
        table_name: str = None,
        prefix: str = "dml",
        suffix: str = date.today().strftime("%Y%m%d"),
        model_id: str = None,
    ) -> None:
        """
        Сохранение данных в HDFS.

        Parameters
        ----------
        data: dict
            Словарь с набором данных, где ключ - название
            выборки, значение - кортеж с матрицей признаков
            и вектором целевой переменной.

        spark_config: SparkConf
            Конфигурации спарк сессии

        Название таблиц имеет формат: (cluster_name).(prefix)_(model_id)_(table_name)_(train/valid/test)_(suffix)_(n)"

        storage_name: str
            Название хранилища для сохранения данных

        table_name: str
            Название таблицы для сохранения данных

        prefix: str
            Префикс к названию таблицы, для удобства пользования (по учолчанию: 'dml')

        suffix: str
            Суффикс после названия таблицы и выборки, для удобства пользования (по учолчанию: сегодняшняя дата)

        model_id: str
            id модели, для удобства пользования
        """
        # !!! Должен быть полный датасет, без дропнутых признаков.
        if not storage_name:
            if self.config.dev_data_path:
                storage_name = self.config.dev_data_path.split(".")[0]
            else:
                storage_name = self.config.train_data_path.split(".")[0]

        if not table_name:
            if self.config.dev_data_path:
                table_name = self.config.dev_data_path.split(".")[1]
            else:
                table_name = self.config.train_data_path.split(".")[1]

        prefix = prefix + "_" if prefix else ""
        suffix = "_" + suffix if suffix else ""
        model_id = model_id + "_" if model_id else ""

        spark = create_hive_session(conf=spark_config)
        list_of_tables = spark.catalog.listTables(storage_name)

        list_of_table_names = [x.name for x in list_of_tables]

        # Создаем датафреймы для записи в Persistent Storage.
        data_to_save = {}
        for k in data.keys():
            if k.upper() != "OOT":
                df = deepcopy(data[k][0])
                df[self.config["target_name"]] = deepcopy(data[k][1])
                data_to_save[k] = spark.createDataFrame(df)

        n = 0
        for k in data_to_save.keys():
            result_name = f"{prefix}{model_id}{table_name}_{k}{suffix}"  # result_name - имя итогового датафрейма.

            # Находим следующий свободный номер для датафрейма.
            if n == 0:
                while result_name in list_of_table_names:
                    n += 1
                    result_name = f"{prefix}{model_id}{table_name}_{k}{suffix}_{n}"
            else:
                result_name = f"{prefix}{model_id}{table_name}_{k}{suffix}_{n}"

            # Берем существующий датафрейм с последним номером и новый, считаем на них статистики
            # (количество строк, столбцов и среднее значение по целевой переменной).
            if n == 0:
                table_name_for_comparison = (
                    None  # table_name_for_comparison - имя существующего датафрейма
                )
            elif n == 1:
                table_name_for_comparison = (
                    f"{prefix}{model_id}{table_name}_{k}{suffix}"
                )
            else:
                table_name_for_comparison = (
                    f"{prefix}{model_id}{table_name}_{k}{suffix}_{n - 1}"
                )

            if table_name_for_comparison:
                df_for_comparison = spark.table(
                    f"{storage_name}.{table_name_for_comparison}"
                )

                df_for_comparison.cache()
                data_to_save_stats = (
                    data_to_save[k]
                    .select(F.mean(F.col(self.config["target_name"])).alias("mean"))
                    .collect()
                )
                df_for_comparison_stats = df_for_comparison.select(
                    F.mean(F.col(self.config["target_name"])).alias("mean")
                ).collect()
                stats_df = {
                    "rows": {
                        "old": df_for_comparison.count(),
                        "new": data_to_save[k].count(),
                    },
                    "cols": {
                        "old": len(df_for_comparison.columns),
                        "new": len(data_to_save[k].columns),
                    },
                    "mean": {
                        "old": df_for_comparison_stats[0]["mean"],
                        "new": data_to_save_stats[0]["mean"],
                    },
                }

                # Сравниваем количество строк, столбцов и среднее значение по целевой переменной и если все равны,
                # то перезаписываем поледний датафрейм, если нет, то создаем новый.
                if (
                    stats_df["rows"]["new"] == stats_df["rows"]["old"]
                    and stats_df["cols"]["new"] == stats_df["cols"]["old"]
                    and stats_df["mean"]["new"] == stats_df["mean"]["old"]
                ):
                    result_name = table_name_for_comparison

            data_to_save[k].write.saveAsTable(
                f"{storage_name}.{result_name}", mode="Overwrite"
            )
            _logger.info(f"Saved to Persistent Storage: {storage_name}.{result_name}")

        spark.stop()

    def save_artifacts(self, models: dict, ipynb_name: Optional[str] = None) -> None:
        """
        Сохранение моделей и объектов моделирования.
        Предполагается, что в models расположены все
        объекты, необходимые для воспроизведения модели:
        transformers, encoders, estimators, ....

        Parameters
        ----------
        models: dict
            Словарь с объектами, необходимыми для воспроизведения
            работы модели. Ключ словаря - название стадии обработки
            данных (transformer / encoder / ... /), значение - обученный
            объект.

        """
        models_ = deepcopy(models)

        imp = [col for col in models_ if "importance" in col]
        for col in imp:
            _ = models_.pop(col)

        summary_stages_info = dict()
        for model in models_:
            pickle.dump(
                models_[model], open(f"{self.experiment_path}/models/{model}.pkl", "wb")
            )

            pickle.dump(
                models_[model].params,
                open(
                    f"{self.experiment_path}/hyperparams/{model}.hyperparams.pkl", "wb"
                ),
            )

            pickle.dump(
                models_[model].used_features,
                open(
                    f"{self.experiment_path}/used_features/{model}.used_features.pkl",
                    "wb",
                ),
            )

            summary_stages_info[model] = {
                "features": models_[model].used_features,
                "hyperparams": models_[model].params,
            }
        self.save_dict_to_txt(
            summary_stages_info,
            f"{self.experiment_path}/summary_stages_info.txt",
            mode="w",
        )

        with open(f"{self.experiment_path}/config/config.yaml", "w") as file:
            yaml.dump(self.config, file)

        self.save_dependencies()
        shutil.copy2(
            ipynb_name, f"{self.experiment_path}/notebooks/fit_model_notebook.ipynb"
        )