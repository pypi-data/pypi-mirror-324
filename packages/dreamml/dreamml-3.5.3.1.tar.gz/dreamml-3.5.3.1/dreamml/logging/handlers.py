import logging
import socket
from typing import Optional, Dict

import requests
from requests import RequestException

from dreamml.logging.formatters import MonitoringFormatter
from dreamml.logging import get_logger

_logger = get_logger(__name__)
_defaultMonitoringFormatter = MonitoringFormatter()


class MonitoringHandler(logging.Handler):
    def __init__(
        self, endpoint: Optional[str] = None, headers: Optional[Dict[str, str]] = None
    ):
        super().__init__()

        self.addFilter(lambda record: getattr(record, "monitoring", True))

        self.disabled = False

        self.hostname = socket.gethostname()
        self._set_endpoint(endpoint)
        self.headers = headers or {"Content-Type": "application/json"}

    def _set_endpoint(self, endpoint: Optional[str] = None):
        if endpoint is not None:
            pass
        else:
            #raise ValueError(f"MonitoringHandler couldn't be initialized without setting endpoint.")
            pass
        
        self.endpoint = endpoint

    def format(self, record):
        """
        Format the specified record.

        If a formatter is set, use it. Otherwise, use the default formatter
        for the monitoring.
        """
        if self.formatter:
            fmt = self.formatter
        else:
            fmt = _defaultMonitoringFormatter

        return fmt.format(record)

    def emit(self, record):
        if self.disabled:
            return

        msg = self.format(record)

        try:
            response = requests.post(
                self.endpoint,
                headers=self.headers,
                data=msg.encode("utf-8"),
                timeout=10,
            )
            response.raise_for_status()
        except requests.Timeout as e:
            _logger.warning(
                "Couldn't establish connection to monitoring service due to timeout. "
                f"Please, contact the cluster administrator. {e}",
                extra={"monitoring": False},
            )
            self.disabled = True
        except RequestException as e:
            _logger.warning(
                "Monitoring service is unavailable.", extra={"monitoring": False}
            )
            _logger.debug(e, extra={"monitoring": False})
            self.disabled = True