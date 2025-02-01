import os
import pickle
from pathlib import Path
from typing import Dict

from dreamml.utils.get_last_experiment_directory import get_experiment_dir_path
from dreamml.data._hadoop import create_spark_session, stop_spark_session
from dreamml.data.store import get_input
from dreamml.utils.splitter import DataSplitter
from dreamml.utils.temporary_directory import TempDirectory


def get_model_path_from_config(config: Dict):
    if config.get("model_path"):
        model_path = config["model_path"]
    else:
        experiment_dir_path = get_experiment_dir_path(
            config["results_path"],
            experiment_dir_name=config.get("dir_name"),
            use_last_experiment_directory=config.get(
                "use_last_experiment_directory", False
            ),
        )

        model_path = os.path.join(
            experiment_dir_path, "models", f"{config['model_name']}.pkl"
        )

    return model_path


def get_encoder_path_from_config(config: Dict):
    if config.get("encoder_path"):
        model_path = config["encoder_path"]
    else:
        experiment_dir_path = get_experiment_dir_path(
            config["results_path"],
            experiment_dir_name=config.get("dir_name"),
            use_last_experiment_directory=config.get(
                "use_last_experiment_directory", False
            ),
        )

        model_path = os.path.join(experiment_dir_path, "models", f"encoder.pkl")

    return model_path


def _load_pickle(path: str):
    with open(path, "rb") as f:
        obj = pickle.load(f)

    return obj


def load_model(path: str):
    ext = Path(path).suffix
    if ext in [".pkl", ".pickle"]:
        obj = _load_pickle(path)
    else:
        raise ValueError(f"Can't load model. Unsupported file extension: {ext}")

    return obj


def get_eval_sets_from_config(config: Dict):
    dev_data_path = config.get("dev_data_path")

    if dev_data_path is None:
        experiment_dir_path = get_experiment_dir_path(
            config["results_path"],
            experiment_dir_name=config.get("dir_name"),
            use_last_experiment_directory=config.get(
                "use_last_experiment_directory", False
            ),
        )

        eval_sets_path = os.path.join(experiment_dir_path, "data", f"eval_sets.pkl")

        if os.path.exists(eval_sets_path):
            return _load_pickle(eval_sets_path)

    else:
        encoder_path = get_encoder_path_from_config(config)
        encoder = load_model(encoder_path) if os.path.exists(encoder_path) else None

        spark = None
        temp_dir = None

        local_file_extenstions = [".csv", ".pkl", ".pickle", ".parquet"]

        if Path(dev_data_path).suffix not in local_file_extenstions:
            temp_dir = TempDirectory()
            spark = create_spark_session(spark_config=None, temp_dir=temp_dir)

        dev_data, target = get_input(
            spark=spark, data_path="dev_data_path", config=config
        )

        if encoder is not None:
            dev_data = encoder.transform(dev_data)

        splitter = DataSplitter(
            split_fractions=[0.6, 0.2, 0.2],
            shuffle=True,
            group_column=None,
            target_name=config.get("target_name"),
            stratify=True,
        )

        train_idx, valid_idx, test_idx = splitter.transform(dev_data, target)

        eval_sets = {
            "train": (dev_data.loc[train_idx], target.loc[train_idx]),
            "valid": (dev_data.loc[valid_idx], target.loc[valid_idx]),
            "test": (dev_data.loc[test_idx], target.loc[test_idx]),
        }
        # Обрабатываем случай необходимости запуска спарк-сессии

        if config.get("oot_data_path") is not None:
            oot_data_path = config["oot_data_path"]
            if (
                Path(oot_data_path).suffix not in local_file_extenstions
                and spark is None
            ):
                temp_dir = TempDirectory()
                spark = create_spark_session(spark_config=None, temp_dir=temp_dir)
            oot, oot_target = get_input(
                spark=spark, data_path="oot_data_path", config=config
            )
            if encoder is not None:
                oot = encoder.transform(oot)
            eval_sets["OOT"] = oot, oot_target

        if spark is not None:
            stop_spark_session(spark=spark, temp_dir=temp_dir)

        return eval_sets