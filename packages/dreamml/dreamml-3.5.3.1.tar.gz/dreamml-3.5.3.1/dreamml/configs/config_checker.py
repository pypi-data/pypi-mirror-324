import os
import sys
from pathlib import Path
from colorama import Fore, Style
import torch
from typing import Dict
import json

from dreamml.logging import get_logger
from dreamml.modeling.metrics import metrics_mapping

_logger = get_logger(__name__)

REFERENCE_CONFIG_PATH = (
    Path(__file__).parent.parent / "references/reference_config.json"
)


class ConfigChecker:
    def __init__(
        self,
        config: Dict,
    ):
        self.config = config
        self.reference_config = self._read_reference_config()
        self.is_clean_config = True
        self.is_clean_data = True
        _logger.info("Config Checker is running")

    @staticmethod
    def _read_reference_config():
        with open(REFERENCE_CONFIG_PATH) as file:
            return json.load(file)

    @staticmethod
    def _create_wrapper_msg(error_type, msg):
        _logger.info(
            f"{'='*100}\n{Fore.RED}{error_type}: {Style.RESET_ALL}{msg}\n{'='*100}"
        )

    def check_config(self):
        self._check_device()
        self._check_data_path()
        self._check_config_params()
        self._check_task()
        self._check_optimizer()
        self._check_validation()
        self._check_metric_params()
        self._check_vectorization_algos()

        if not self.is_clean_config:
            sys.exit(0)

        self._check_estimators()

        if not self.is_clean_config:
            sys.exit(0)

        self._check_eval_metric()
        self._check_loss_function()
        self._check_pyboost_device()
        self._check_conditions_for_bert()
        self._check_timeseries()

    def check_data(self, data: Dict):
        self._data_check_target(data)

    def _check_config_params(self):
        info_dict = {"int": int, "float": float}
        params_name = list(self.reference_config["default_params"].keys())
        params_value = [
            self.config.get(parameter_name) for parameter_name in params_name
        ]

        for parameter_name, parameter_value in zip(params_name, params_value):
            if parameter_value is None:
                default_parameter = self.reference_config["default_params"][
                    parameter_name
                ]["value"]
                self.config[parameter_name] = default_parameter
                _logger.info(
                    f"The default value '{default_parameter}' was selected for the '{parameter_name}'"
                )
            elif parameter_value == "auto":
                pass
            else:
                try:
                    change_type_func = self.reference_config["default_params"][
                        parameter_name
                    ]["type"]
                    change_func = info_dict[change_type_func]
                    parameter_value = change_func(parameter_value)
                    self.config[parameter_name] = parameter_value
                except Exception as e:
                    msg = f"Parameter '{parameter_name}' must be '{change_type_func}'"
                    self._create_wrapper_msg("ConfigurationError", msg)
                    self.is_clean_config = False

    def _check_data_path(self):
        """
        Метод проверки файлов в данными.
        """
        data_dict = {
            "dev_data_path": self.config.get("dev_data_path"),
            "oot_data_path": self.config.get("oot_data_path"),
            "train_data_path": self.config.get("train_data_path"),
            "valid_data_path": self.config.get("valid_data_path"),
            "test_data_path": self.config.get("test_data_path"),
        }

        for data_type, data_path in data_dict.items():
            if data_path is not None:
                try:
                    extension = os.path.splitext(data_path)[1].lstrip(".")
                except Exception as e:
                    msg = f"Error in the file path: {data_type}"
                    self._create_wrapper_msg("ConfigurationError", msg)
                    self.is_clean_config = False
                    continue
                if extension not in self.reference_config["file_extension"]:
                    _logger.info(
                        f"Spark session will be started for the file {data_type}"
                    )

    def _check_device(self):
        """
        Метод проверки device.
        1. CUDA работает только на NVIDIA-картах.
        """
        device = self.config.get("device", "auto").lower()
        if device not in self.reference_config["device"]:
            msg = "Please select a device from the list: ['auto', 'cpu', 'cuda']."
            self._create_wrapper_msg("ConfigurationError", msg)
            self.is_clean_config = False
            return

        is_available = torch.cuda.is_available()
        if device == "auto":
            device = "cuda" if is_available else "cpu"
        elif device != "cpu" and not is_available:
            msg = "GPU is not available. Please select another device."
            self._create_wrapper_msg("ConfigurationError", msg)
            self.is_clean_config = False

        _logger.debug(f"Selected '{device=}'.")
        self.config["device"] = device

    def _check_task(self):
        """
        Метод проверки task.
        """
        task = self.config.get("task")
        if task is None:
            msg = "Please select the task."
            self._create_wrapper_msg("ValueError", msg)
            self.is_clean_config = False

        if task not in self.reference_config["task"]:
            msg = f"Please select another task. DreamML supports: {self.reference_config['task']}"
            self._create_wrapper_msg("ConfigurationError", msg)
            self.is_clean_config = False

    def _check_target(self):
        """
        Метод проверки target_name.
        """
        target_name = self.config.get("target_name")
        task = self.config.get("task")

        if target_name is None:
            if task not in ["topic_modeling", "phrase_retrieval"]:
                msg = f"Please select the 'target_name'."
                self._create_wrapper_msg("ConfigurationError", msg)
                self.is_clean_config = False
        elif not isinstance(target_name, str) and task != "multilabel":
            msg = f"For task '{task}' 'target_name' must be as 'str'."
            self._create_wrapper_msg("ConfigurationError", msg)
            self.is_clean_config = False
        if target_name is not None and task in ["topic_modeling", "phrase_retrieval"]:
            self.config["target_name"] = None
            _logger.info(
                f"'None' was chosen as value 'target_name', because you have chosen '{task}' task."
            )

        if target_name == "multilabel" and target_name is not None:
            if not isinstance(target_name, list):
                msg = f"For task '{task}' 'target_name' must be as 'list'."
                self._create_wrapper_msg("ConfigurationError", msg)
                self.is_clean_config = False
            else:
                for sub_target in target_name:
                    if not isinstance(sub_target, str):
                        msg = f"For task '{task}' 'sub_target_name' must be as 'str'."
                        self._create_wrapper_msg("ConfigurationError", msg)
                        self.is_clean_config = False

    def _check_estimators(self):
        """
        Метод проверки сомвместимости estimators и task.
        """
        task = self.config.get("task")
        estimators = self.config.get("fitted_model")

        if estimators is None:
            msg = f"Please select fitted_model. DreamML supports: {self.reference_config['models']['estimators']}"
            self._create_wrapper_msg("ConfigurationError", msg)
            self.is_clean_config = False
        else:
            for estimator in estimators:
                if (
                    estimator
                    not in self.reference_config["models"]["estimators_by_task"][task]
                ):
                    supported_estimators = self.reference_config["models"][
                        "estimators_by_task"
                    ][task]
                    msg = (
                        f"Please select another 'fitted_model'. "
                        f"For the task '{task}' DreamML support: {supported_estimators}"
                    )
                    self._create_wrapper_msg("ConfigurationError", msg)
                    self.is_clean_config = False

    def _check_eval_metric(self):
        """
        Метод проверки eval_metric.
        """
        task = self.config.get("task")
        eval_metric = self.config.get("eval_metric")
        estimators = self.config.get("fitted_model")
        device = self.config.get("device", "auto").lower()

        if task == "multilabel":
            self.config["eval_metric"] = "logloss"
            return

        if "catboost" in estimators and eval_metric == "gini":
            if device == "cuda":
                msg = f"Cannot use custom 'eval_metric' for CATBOOST with {device.upper()} mode."
                self._create_wrapper_msg("ConfigurationError", msg)
                self.is_clean_config = False

        if eval_metric is None:
            default_eval_metric = self.reference_config["default_eval_metric_by_task"][
                self.config.get("task")
            ]
            self.config["eval_metric"] = default_eval_metric
            _logger.info(
                f"{default_eval_metric.upper()} was chosen as the "
                f"default eval_metric for the task {self.config.get('task')}"
            )
        else:
            for estimator in estimators:
                eval_metric_by_estimator = self.reference_config["eval_metric"][
                    "eval_metric_by_estimator"
                ][estimator]

                if estimator in ["xgboost", "catboost"] and eval_metric == "mse":
                    _logger.info(
                        f"'eval_metric' was changed for '{estimator.upper()}' on 'RMSE'"
                    )
                    continue

                if eval_metric not in eval_metric_by_estimator:
                    if eval_metric in metrics_mapping.custom_metrics:
                        continue
                    msg = f"{estimator.upper()} does not support {eval_metric.upper()} as 'eval_metric'"
                    self._create_wrapper_msg("ConfigurationError", msg)
                    self.is_clean_config = False

    def _check_loss_function(self):
        """
        Метод проверки loss_function.
        """
        loss_function = self.config.get("loss_function")
        estimators = self.config.get("fitted_model")

        if loss_function is None:
            default_loss_function = self.reference_config[
                "default_loss_function_by_task"
            ][self.config.get("task")]
            self.config["loss_function"] = default_loss_function
            _logger.info(
                f"{default_loss_function.upper()} was chosen as the "
                f"default loss_metric for the task {self.config.get('task')}"
            )
        else:
            for estimator in estimators:
                loss_function_by_estimator = self.reference_config["loss_function"][
                    "loss_function_by_estimator"
                ][estimator]
                if loss_function not in loss_function_by_estimator:
                    if loss_function in metrics_mapping.custom_metrics:
                        continue
                    msg = f"{estimator.upper()} does not support {loss_function.upper()} as 'loss_function'"
                    self._create_wrapper_msg("ConfigurationError", msg)
                    self.is_clean_config = False

    def _check_pyboost_device(self):
        device = self.config.get("device")
        estimators = self.config.get("fitted_model")

        if "pyboot" in estimators and device == "cpu":
            msg = (
                f"PyBoost supports only GPU mode. "
                f"Please remove PyBoost from fitted_model or change device type on GPU."
            )
            self._create_wrapper_msg("ConfigurationError", msg)
            self.is_clean_config = False

    def _check_optimizer(self):
        """
        Метод проверки optimizer.
        """
        optimizer = self.config.get("optimizer")

        if optimizer is None:
            optimizer = "auto"
            _logger.info(f"The 'optimizer' will be selected automatically")
            self.config["optimizer"] = optimizer
        elif optimizer not in self.reference_config["optimizer"]:
            msg = f"Please select another 'optimizer'. DreamML support: {self.reference_config['optimizer']}"
            self._create_wrapper_msg("ConfigurationError", msg)
            self.is_clean_config = False

    def _check_validation(self):
        """
        Метод проверки validation.
        """
        validation = self.config.get("validation")
        if validation is None:
            validation = "auto"
            _logger.info(f"The 'validation' will be selected automatically")
            self.config["validation"] = validation
        elif validation not in self.reference_config["validation"]:
            msg = f"Please select another 'validation'. DreamML support: {self.reference_config['validation']}"
            self._create_wrapper_msg("ConfigurationError", msg)
            self.is_clean_config = False

    def _check_timeseries(self):
        task = self.config.get("task")
        fitted_model = self.config.get("fitted_model")

        if task not in ("timeseries", "amts"):
            return

        group_column = self.config.get("group_column")
        time_column = self.config.get("time_column")
        split_by_group = self.config.get("split_by_group", False)
        split_by_time_period = self.config.get("split_by_time_period", False)
        oot_split_test = self.config.get("oot_split_test", False)
        oot_split_valid = self.config.get("oot_split_valid", False)
        time_series_split = self.config.get("time_series_split", False)
        time_series_window_split = self.config.get("time_series_window_split", False)

        if time_column is None:
            if (
                oot_split_test
                or oot_split_valid
                or time_series_split
                or time_series_window_split
                or split_by_time_period
            ):
                msg = f"Please select 'time_column'."
                self._create_wrapper_msg("ConfigurationError", msg)
                self.is_clean_config = False

        if group_column is None and split_by_group:
            msg = f"Please select 'group_column'."
            self._create_wrapper_msg("ConfigurationError", msg)
            self.is_clean_config = False

        if task == "amts" and "linear_reg" in fitted_model and split_by_group:
            msg = f"Cannot be used 'linear_reg' with 'group_column' in 'amts' task."
            self._create_wrapper_msg("ConfigurationError", msg)
            self.is_clean_config = False

    def _check_metric_params(self):
        """
        Метод проверки metric_params.
        """
        metric_params = self.config.get("metric_params")
        available_params = self.reference_config["metric_params"]

        if metric_params is not None:
            if not isinstance(metric_params, dict):
                msg = f"'metric_params' must be a dictionary with one of the keys is expected: {available_params}"
                self._create_wrapper_msg("ConfigurationError", msg)
                self.is_clean_config = False
            else:
                for metric_parameter in metric_params:
                    if metric_parameter not in available_params:
                        msg = (
                            f"The {metric_parameter} is not available for 'metric_params'. "
                            f"Please choose from {available_params}"
                        )
                        self._create_wrapper_msg("ConfigurationError", msg)
                        self.is_clean_config = False

    def _check_vectorization_algos(self):
        """
        Метод проверки vectorization_algos.
        """
        vectorization_algos = self.config.get("vectorization_algos")
        available_vectorization_algos = self.reference_config["vectorization_algos"]

        if vectorization_algos is not None:
            if not isinstance(vectorization_algos, list):
                msg = (
                    f"'vectorization_algos' must be a "
                    f"list with one of the value is expected: {available_vectorization_algos}"
                )
                self._create_wrapper_msg("ConfigurationError", msg)
                self.is_clean_config = False
            else:
                for vectorization_algos_name in vectorization_algos:
                    if vectorization_algos_name not in available_vectorization_algos:
                        msg = (
                            f"The {vectorization_algos_name} is not available for 'vectorization_algos'. "
                            f"Please choose from {available_vectorization_algos}"
                        )
                        self._create_wrapper_msg("ConfigurationError", msg)
                        self.is_clean_config = False

    def _check_conditions_for_bert(self):
        estimators = self.config.get("fitted_model")
        vectorization_algos = self.config.get("vectorization_algos")
        available_vectorization_algos = self.reference_config["vectorization_algos"]

        if vectorization_algos is not None:
            if "bert" in vectorization_algos:
                if len(vectorization_algos) != 1:
                    msg = (
                        f"You can select just only 'bert' in 'vectorization_algos' "
                        f"or another vectorization_algos: {available_vectorization_algos}"
                    )
                    self._create_wrapper_msg("ConfigurationError", msg)
                    self.is_clean_config = False

                if len(estimators) != 1:
                    msg = (
                        f"You can select just only one 'fitted_model' "
                        f"if you have chosen 'bert' as vectorization_algos"
                    )
                    self._create_wrapper_msg("ConfigurationError", msg)
                    self.is_clean_config = False

    def _data_check_target(self, data):
        """
        Метод проверки type of data target_name.
        """
        task = self.config.get("task")
        target_name = self.config.get("target_name")

        if task == "timeseries":
            target_name = "target"

        if target_name is None:
            return

        for sample, df in data.items():
            if task != "multilabel":
                if df[target_name].isna().sum() != 0:
                    msg = (
                        f"Cannot be used NaN value in target column for task '{task}'."
                    )
                    self._create_wrapper_msg("ValueError", msg)
                    self.is_clean_data = False

            if task in ["binary"]:
                if df[target_name].dtype == "float":
                    msg = f"Cannot be used 'float' value in target column for task '{task}'."
                    self._create_wrapper_msg("ValueError", msg)
                    self.is_clean_data = False