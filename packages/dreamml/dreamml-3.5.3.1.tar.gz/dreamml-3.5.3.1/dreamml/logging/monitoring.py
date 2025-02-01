import json
import os
import uuid
import warnings
from datetime import datetime
from enum import Enum
import socket
from typing import Optional, Type, Dict, Any

from pydantic import BaseModel, field_validator, field_serializer

import dreamml
from dreamml.utils.warnings import DMLWarning

MAX_MESSAGE_LEN = 2**21


class MonitoringPayload(BaseModel):

    app_id: str = "dml-ser"
    type_id: str = "Tech"
    subtype_id: str = "INFO"
    message: str


class MonitoringEvent(Enum):
    """
    `Enum`, который хранит возможные виды событий в DreamML для мониторинга
    """

    Error = 0
    Warning = 1
    PipelineStarted = 2
    PipelineFinished = 3
    StageFinished = 4
    TrainingFinished = 5
    DataLoaded = 6
    DataTransformed = 7
    FeaturesGenerated = 8
    ReportStarted = 9
    ReportFinished = 10
    ValidationTestFinished = 11


class MonitoringLogData(BaseModel):
    event_id: MonitoringEvent
    datetime: str
    hostname: str = socket.gethostname()
    user: str = os.environ.get("USER", "Unknown")
    dml_version: str = dreamml.__version__
    session_id: str = uuid.uuid4().hex

    class Config:
        extra = "forbid"

    def __init__(self, /, **data):
        event_id = data.pop("event_id", None)
        if event_id is not None:
            warnings.warn(
                f"Tried to set {event_id=} which should be explicitly defined in {self.__class__.__name__}.",
                DMLWarning,
                stacklevel=2,
            )

        data["datetime"] = data.get("datetime", datetime.now())

        super().__init__(**data)

    # noinspection PyNestedDecorators
    @field_validator("datetime", mode="before")
    @classmethod
    def type_is_exception(cls, dt: datetime):
        if isinstance(dt, datetime):
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        else:
            raise ValueError(
                f"Datetime passed to {cls.__name__} must be an instance of datetime.datetime"
            )


class ExceptionInfo(BaseModel):
    type: str
    text: str
    line: Optional[int] = None
    file: Optional[str] = None

    # noinspection PyNestedDecorators
    @field_validator("type", mode="before")
    @classmethod
    def type_is_exception(cls, v: Type[Exception]):
        if isinstance(v, type) and issubclass(v, Exception):
            return v.__name__
        else:
            raise ValueError(
                f"Exception passed to {cls.__name__} must be subclass of Exception."
            )


class ErrorLogData(MonitoringLogData):
    event_id: MonitoringEvent = MonitoringEvent.Error
    exception: Optional[ExceptionInfo] = None
    msg: str


class WarningLogData(MonitoringLogData):
    event_id: MonitoringEvent = MonitoringEvent.Warning
    msg: str


class UserConfigLogData(BaseModel):
    user_config: Dict[str, Any]

    @field_serializer("user_config")
    def serialize_user_config(self, user_config: Dict[str, Any], _info):
        def safe_serialize(val):
            try:
                json.dumps(val)
                return val
            except (TypeError, OverflowError):
                # If not serializable, convert to str
                return str(val)

        return {key: safe_serialize(value) for key, value in user_config.items()}

    # noinspection PyNestedDecorators
    @field_validator("user_config", mode="before")
    @classmethod
    def user_config_serializable(cls, d: Dict[str, Any]):
        if not isinstance(d, dict) or any(not isinstance(key, str) for key in d):
            raise ValueError(f"User configuration must be a dict with string keys.")

        return d


class PipelineStartedLogData(MonitoringLogData, UserConfigLogData):
    event_id: MonitoringEvent = MonitoringEvent.PipelineStarted
    experiment_name: str
    from_checkpoint: bool = False


class PipelineFinishedLogData(MonitoringLogData):
    event_id: MonitoringEvent = MonitoringEvent.PipelineFinished
    experiment_name: str
    elapsed_time: float


class StageFinishedLogData(MonitoringLogData):
    event_id: MonitoringEvent = MonitoringEvent.StageFinished
    experiment_name: str
    stage_name: str
    stage_id: str
    elapsed_time: float


class TrainingFinishedLogData(MonitoringLogData):
    event_id: MonitoringEvent = MonitoringEvent.TrainingFinished
    model: str
    metrics: Dict[str, Dict[str, float]]
    elapsed_time: float


class DataLoadedLogData(MonitoringLogData):
    event_id: MonitoringEvent = MonitoringEvent.DataLoaded
    name: str
    length: int
    features_num: int
    nan_count: int
    elapsed_time: float


class DataTransformedLogData(MonitoringLogData):
    event_id: MonitoringEvent = MonitoringEvent.DataTransformed
    name: str
    length: int
    features_num: int
    nan_count: int
    elapsed_time: float


class FeaturesGeneratedLogData(MonitoringLogData):
    event_id: MonitoringEvent = MonitoringEvent.FeaturesGenerated
    length: int
    features_num: int
    nan_count: int
    elapsed_time: float


class ReportStartedLogData(MonitoringLogData, UserConfigLogData):
    event_id: MonitoringEvent = MonitoringEvent.ReportStarted
    task: str
    development: bool
    custom_model: bool
    experiment_name: Optional[str] = None
    report_id: str


class ReportFinishedLogData(MonitoringLogData):
    event_id: MonitoringEvent = MonitoringEvent.ReportFinished
    report_id: str
    elapsed_time: float


class ValidationTestFinishedLogData(MonitoringLogData):
    event_id: MonitoringEvent = MonitoringEvent.ValidationTestFinished
    report_id: str
    test_name: str
    elapsed_time: float