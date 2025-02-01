import os
import sys
import shutil
from datetime import datetime
from typing import Optional, List
import logging

from dreamml.logging.formatters import FileFormatter, FormatterWithoutException
from dreamml.logging.handlers import MonitoringHandler
from dreamml.logging import get_root_logger, MONITOR


class DMLLogger(logging.getLoggerClass()):
    def __init__(self, name):
        super().__init__(name)
        self._used_warnings = []

        logging.addLevelName(MONITOR, "MONITOR")

        self.temp_file_handler = None
        os.makedirs(os.path.join(os.getcwd(), ".dml_log"), exist_ok=True)
        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        self.temp_log_path = os.path.join(
            os.getcwd(), ".dml_log", f"run{current_datetime}.log"
        )
        self._file_formatter = FileFormatter(
            fmt="[{asctime}] - {levelname} - {name} - {message}",
            datefmt="%Y-%m-%d %H:%M:%S",
            style="{",
        )

    def start_logging_session(self):
        if self.temp_file_handler:
            self.removeHandler(self.temp_file_handler)
            self.temp_file_handler.close()

        self.temp_file_handler = logging.FileHandler(self.temp_log_path)
        self.temp_file_handler.setFormatter(self._file_formatter)

        self.addHandler(self.temp_file_handler)

    def set_experiment_log_file(self, log_file_path):
        if self.temp_file_handler is not None:
            self.removeHandler(self.temp_file_handler)
            self.temp_file_handler.close()

            if os.path.exists(self.temp_log_path):
                try:
                    shutil.move(self.temp_log_path, log_file_path)
                except PermissionError:
                    shutil.copy(self.temp_log_path, log_file_path)
                except Exception as e:
                    self.warning(
                        f"Couldn't move {self.temp_file_handler} to experiment directory. {e}"
                    )
                    return

        file_handler = logging.FileHandler(log_file_path)
        file_handler.setFormatter(self._file_formatter)

        self.debug(f"Saving experiment logs to {log_file_path}")

        self.addHandler(file_handler)

    def monitor(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'MONITOR'.

        logger.monitor("Houston, we have a %s", "major disaster")
        """
        if self.isEnabledFor(MONITOR):
            self._log(MONITOR, msg, args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """
        Log warning only once
        """
        if msg in self._used_warnings:
            return

        super().warning(msg, *args, **kwargs)
        self._used_warnings.append(msg)


class CombinedLogger:
    def __init__(self, loggers: List[logging.Logger]):
        self.loggers = [logger for logger in loggers if logger is not None]

    def log(self, level, msg, *args, **kwargs):
        for logger in self.loggers:
            if hasattr(logger, level):
                log_method = getattr(logger, level)

                log_method(msg, *args, **kwargs)
            else:
                raise AttributeError(f"Logger '{logger.name}' has no method '{level}'.")

    def __getattr__(self, name: str):
        if name.upper() in logging._nameToLevel:

            def wrapper(msg, *args, **kwargs):
                self.log(name, msg, *args, **kwargs)

            return wrapper
        else:
            raise AttributeError(f"No such log level: '{name}'.")


def init_logging(name: str, log_file: Optional[str] = None):
    """Should be used for root logger, i.e. parent handlers are not processed"""
    logging.setLoggerClass(DMLLogger)

    logger = logging.getLogger(name)
    logger.propagate = False

    logger.setLevel(logging.INFO)

    if logger.handlers:
        raise RuntimeError(
            f"Tried to initialize logger '{name}' the second time. "
            f"This logger already has {len(logger.handlers)} handlers."
        )

    formatter = FormatterWithoutException(
        fmt="[{asctime}] {message}",
        datefmt="%Y-%m-%d %H:%M:%S",
        style="{",
    )

    # instancing loggers for std and set them filters for message types
    stdout_streamhandler = logging.StreamHandler(stream=sys.stdout)
    stdout_streamhandler.addFilter(lambda record: record.levelno < logging.WARNING)
    stdout_streamhandler.setFormatter(formatter)

    stderr_streamhandler = logging.StreamHandler(stream=sys.stderr)
    stderr_streamhandler.addFilter(lambda record: record.levelno >= logging.WARNING)
    stderr_streamhandler.setFormatter(formatter)

    logger.addHandler(stdout_streamhandler)
    logger.addHandler(stderr_streamhandler)

    if log_file is not None:
        logger.set_experiment_log_file(log_file)

    monitoring_handlder = MonitoringHandler()
    monitoring_handlder.setLevel(MONITOR)

    logger.addHandler(monitoring_handlder)

    return logger


def capture_warnings(capture):
    logger = logging.getLogger("py.warnings")

    root_logger = get_root_logger()

    if not logger.handlers:
        for handler in root_logger.handlers:
            logger.addHandler(handler)

    logger.setLevel(root_logger.level)
    logger.propagate = False

    logging.captureWarnings(capture)