from typing import Dict, List, Optional
import logging
from dataclasses import dataclass

import xgboost.callback
from colorama import Fore

from dreamml.logging import get_logger
from dreamml.utils.styling import ANSIColoringMixin

_logger = get_logger(__name__)


@dataclass
class ModelCallbackInfo(ANSIColoringMixin):
    iter: int

    # list - метрики, dict - метрика-значение
    # [{'mae': 55.91283587027287}, {'mae2': 30.0003}]
    train_metrics_list: List[Dict[str, float]]

    # dict - eval_set, list - метрики, dict - метрика-значение
    # {
    #     'validation_1': [{'mae': 55.91283587027287}],
    #     'validation_2': [{'mae': 54.0003}, {'rmse': 100.0003}],
    # }
    metrics_list_per_eval_set: Dict[str, List[Dict[str, float]]]

    use_colors: bool = False

    tail_str = f"|  "

    left_padding: str = " " * 4
    set_alignment_length: int = 18
    metric_alignment_length: int = 25
    metric_round: int = 4

    def __str__(self):
        train_set_name = "train set:"
        possibly_colored_train_set_name = self._add_ansi_color(
            train_set_name, Fore.GREEN
        )
        train_set_str = f"{self.left_padding}{possibly_colored_train_set_name:<{self.set_alignment_length}}{self.tail_str}"

        for train_metric in self.train_metrics_list:
            train_set_str += self._format_metric(train_metric, Fore.GREEN)

        eval_set_str = ""
        for eval_set_key in self.metrics_list_per_eval_set.keys():
            eval_set_name = f"{eval_set_key}:"
            possibly_colored_eval_set_name = self._add_ansi_color(
                eval_set_name, Fore.YELLOW
            )

            eval_set_str += f"{self.left_padding}{possibly_colored_eval_set_name:<{self.set_alignment_length}}{self.tail_str}"

            for eval_set_metric in self.metrics_list_per_eval_set[eval_set_key]:
                eval_set_str += self._format_metric(eval_set_metric, Fore.YELLOW)

            eval_set_str += "\n"

        iteration_str = f"iter {self.iter}:"
        output = f"{iteration_str}\n{train_set_str}\n{eval_set_str}"

        return output.rstrip()

    def _format_metric(self, metric: Dict[str, float], color: Optional[str]):
        # `metric` is assumed to be a dict {"metric_name": metric_value} with one key only
        metric_name = list(metric.keys())[0]
        possibly_colored_metric_name = self._add_ansi_color(metric_name, color)

        metric_value = metric[metric_name]

        metric_name_and_value_str = (
            f"{possibly_colored_metric_name} {metric_value:.{self.metric_round}f}"
        )

        s = f"{metric_name_and_value_str:<{self.metric_alignment_length}}{self.tail_str}"

        return s


@dataclass
class ModelCallbackInfoList:
    callback_list: List[ModelCallbackInfo]

    def __getitem__(self, index):
        return self.callback_list[index]

    def append(self, callback_info: ModelCallbackInfo):
        self.callback_list.append(callback_info)

    def __repr__(self):
        return "\n".join([repr(callback) for callback in self.callback_list])

    def __str__(self):
        return "\n".join([str(callback) for callback in self.callback_list])


class ModelLoggingCallback:
    def __init__(self, train_logger: Optional[logging.Logger] = None):
        super().__init__()
        self.callback_info_list = ModelCallbackInfoList([])
        self._logger = train_logger

    def _log(self, callback_info: ModelCallbackInfo):
        logger = self._logger or _logger
        logger.info(callback_info)


class XGBoostLoggingCallback(xgboost.callback.TrainingCallback, ModelLoggingCallback):
    """class callback for xgboost"""

    def __init__(self, train_logger: Optional[logging.Logger] = None):
        super().__init__()
        ModelLoggingCallback.__init__(self, train_logger=train_logger)

    def after_iteration(self, model, epoch, evals_log):
        """

        epoch -- iteration
        evals_log -- list datasets
        """
        callback_info = ModelCallbackInfo(epoch, [], {})

        for i, eval_set_name in enumerate(evals_log):
            for metric_name in evals_log[eval_set_name]:
                metric_value = evals_log[eval_set_name][metric_name][-1]
                if eval_set_name == "validation_0":
                    callback_info.train_metrics_list.append({metric_name: metric_value})
                else:
                    if eval_set_name not in callback_info.metrics_list_per_eval_set:
                        callback_info.metrics_list_per_eval_set[eval_set_name] = [
                            {metric_name: metric_value}
                        ]
                    else:
                        callback_info.metrics_list_per_eval_set[eval_set_name].append(
                            {metric_name: metric_value}
                        )

        self.callback_info_list.append(callback_info)
        self._log(callback_info)


class LightGBMLoggingCallback(ModelLoggingCallback):
    """class callback for lgbm"""

    def __call__(self, evr):
        """
        evr.iteration -- iteration
        evr.evaluation_result_list -- tuple(set_name, metric_name, metric_value)
        """
        callback_info = ModelCallbackInfo(evr.iteration, [], {})

        for i, eval_tuple in enumerate(evr.evaluation_result_list):
            eval_set_name = eval_tuple[0]
            metric_name = eval_tuple[1]
            metric_value = eval_tuple[2]

            if eval_set_name == "valid_0":
                callback_info.train_metrics_list.append({metric_name: metric_value})
            elif "valid" in eval_set_name:
                number_of_set = int(eval_set_name[-1])
                if eval_set_name not in callback_info.metrics_list_per_eval_set:
                    callback_info.metrics_list_per_eval_set[eval_set_name] = [
                        {metric_name: metric_value}
                    ]
                else:
                    callback_info.metrics_list_per_eval_set[eval_set_name].append(
                        {metric_name: metric_value}
                    )

        self.callback_info_list.append(callback_info)
        self._log(callback_info)


class CatBoostLoggingCallback(ModelLoggingCallback):
    """class callback for catboost"""

    def after_iteration(self, evr):
        """
        evr.iteration -- iteration
        evr.metrics -- list datasets
        """
        callback_info = ModelCallbackInfo(evr.iteration, [], {})

        for eval_set_name in evr.metrics:
            if eval_set_name == "learn":
                # it's the same as validation_0 in current implementation
                continue

            elif eval_set_name == "validation_0":
                iteration_metrics_per_eval_set = {}
                for metric_name, metric_value in evr.metrics[eval_set_name].items():
                    iteration_metrics_per_eval_set[metric_name.lower()] = metric_value[
                        -1
                    ]

                callback_info.train_metrics_list.append(iteration_metrics_per_eval_set)

            else:

                if eval_set_name not in callback_info.metrics_list_per_eval_set:
                    callback_info.metrics_list_per_eval_set[eval_set_name] = []

                iteration_metrics_per_eval_set = {}
                for metric_name, metric_value in evr.metrics[eval_set_name].items():
                    iteration_metrics_per_eval_set[metric_name.lower()] = metric_value[
                        -1
                    ]

                callback_info.metrics_list_per_eval_set[eval_set_name].append(
                    iteration_metrics_per_eval_set
                )

        self.callback_info_list.append(callback_info)
        self._log(callback_info)

        return True


class PyBoostLoggingCallback(ModelLoggingCallback):
    """class callback for pyboost"""

    _sets_list = ["train", "valid"]

    def before_train(self, evr):
        """Actions to be mad before ech iteration starts

        Args:
            evr: dict

        Returns:

        """
        return

    def before_iteration(self, evr):
        """Actions to be mad before ech iteration starts

        Args:
            evr: dict

        Returns:

        """
        return

    def after_iteration(self, evr):
        """
        Actions to be made after each iteration finishes

        Args:
            evr: dict

        Returns:
            bool, if train process should be terminated
        """
        num_iter = evr["num_iter"]
        callback_info = ModelCallbackInfo(num_iter, [], {})

        metric_class = evr["model"].metric
        metric_name = (
            metric_class.name
            if hasattr(metric_class, "name")
            else (
                metric_class.alias
                if hasattr(metric_class, "alias")
                else metric_class.__class__.__name__
            )
        )
        if num_iter > 0:
            scores = dict(zip(self._sets_list, evr["iter_score"]))
            callback_info.train_metrics_list.append({metric_name: scores["train"]})
            if "valid" not in callback_info.metrics_list_per_eval_set:
                callback_info.metrics_list_per_eval_set["valid"] = [
                    {metric_name: scores["valid"]}
                ]
            else:
                callback_info.metrics_list_per_eval_set["valid"].append(
                    {metric_name: scores["valid"]}
                )

        self.callback_info_list.append(callback_info)
        self._log(callback_info)

        return False

    def after_train(self, evr):
        """Actions to be made before train finishes

        Args:
            evr:

        Returns:

        """
        return