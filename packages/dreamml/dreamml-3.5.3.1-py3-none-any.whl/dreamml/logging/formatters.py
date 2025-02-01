import logging
import warnings

from dreamml.logging.monitoring import (
    ErrorLogData,
    MonitoringPayload,
    MonitoringLogData,
    ExceptionInfo,
    WarningLogData,
)
from dreamml.utils.styling import ANSIColoringMixin
from dreamml.utils.warnings import DMLWarning


class FileFormatter(logging.Formatter):
    def format(self, record):
        if isinstance(record.msg, ANSIColoringMixin):
            use_colors = record.msg.use_colors

            s = super().format(record)

            record.msg.use_colors = use_colors

        else:
            s = super().format(record)

        return s


class MonitoringFormatter(logging.Formatter):
    def formatException(self, exc_info):
        tb = exc_info[2]
        if tb is not None:
            filename, lineno = tb.tb_frame.f_code.co_filename, tb.tb_lineno
        else:
            filename, lineno = None, None

        exc_log_data = ExceptionInfo(
            type=exc_info[0],
            text=str(exc_info[1]),
            line=lineno,
            file=filename,
        )

        return exc_log_data

    def format(self, record):
        """
        Format the specified record as text for monitoring.
        """
        if record.exc_info:
            # Cache the exception log data to avoid converting it multiple times
            if not hasattr(record, "exc_log_data") or not record.exc_log_data:
                record.exc_log_data = self.formatException(record.exc_info)

        if not hasattr(record, "log_data"):
            if record.levelno >= logging.ERROR:
                exc_log_data = (
                    record.exc_log_data if hasattr(record, "exc_log_data") else None
                )
                record.log_data = ErrorLogData(
                    exception=exc_log_data, msg=record.getMessage()
                )

            elif record.levelno >= logging.WARNING:
                record.log_data = WarningLogData(msg=record.getMessage())

        if not hasattr(record, "log_data"):
            warnings.warn(
                "Couldn't gather log_data for monitoring. Instance of LogRecord has no `log_data` attribute. "
                "You probably need to pass `extra` argument to your monitoring logger: "
                '`logger.monitor(msg, extra={"log_data": LogData})` where LogData is subclass of MonitoringLogData.',
                DMLWarning,
                stacklevel=9,  # stacklevel to show where log function is called
            )
            return

        if not isinstance(record.log_data, MonitoringLogData):
            warnings.warn(
                f"Couldn't gather log_data for monitoring. Expected `log_data` to be "
                f"an instance of `{MonitoringLogData.__name__}`, but got {type(record.log_data)}",
                DMLWarning,
                stacklevel=9,  # stacklevel to show where log function is called
            )
            return

        payload = MonitoringPayload(message=record.log_data.model_dump_json())

        msg = payload.model_dump_json()

        return msg


class FormatterWithoutException(logging.Formatter):
    def format(self, record):
        """
        Format the specified record as text without exception info
        """
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        s = self.formatMessage(record)

        return s