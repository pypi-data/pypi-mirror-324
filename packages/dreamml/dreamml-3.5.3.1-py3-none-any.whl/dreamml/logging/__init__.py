import logging
from functools import wraps
from typing import Any, Optional


def get_logger(name: str) -> Any:
    return logging.getLogger(name)


def get_root_logger():
    return logging.getLogger("dreamml")


def set_verbosity(verbosity: int):
    get_root_logger().setLevel(verbosity)
    logging.getLogger("py.warnings").setLevel(verbosity)


class _Propagate:
    value = False


def set_propagate(value):
    _Propagate.value = value


def get_propagate():
    return _Propagate.value


def log_exceptions(logger: Optional[logging.Logger] = None):
    """
    Декоратор для логирования ошибок в функции.
    """
    if logger is None:
        logger = get_root_logger()

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.exception(e)
                raise

        return wrapper

    return decorator


MONITOR = logging.WARNING - 5