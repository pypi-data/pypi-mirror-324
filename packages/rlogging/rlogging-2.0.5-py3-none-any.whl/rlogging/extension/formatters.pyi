import logging
from _typeshed import Incomplete
from rlogging import utils as utils
from typing import Any

class RsFormatter(logging.Formatter): ...

class JsonFormatter(RsFormatter):
    DEFAULT_EXCLUDE_FIELDS: Incomplete
    include_fields: Incomplete
    exclude_fields: Incomplete
    default_extra: Incomplete
    json_serializer: Incomplete
    json_default: Incomplete
    json_cls: Incomplete
    def __init__(self, include_fields: set[str] | None = None, exclude_fields: set[str] | None = None, default_extra: dict[str, Any] | None = None, *args, **kwargs) -> None: ...
    def get_data_from_record(self, record: logging.LogRecord) -> dict: ...
    def format(self, record: logging.LogRecord): ...

class ElkFormatter(JsonFormatter):
    def get_data_from_record(self, record: logging.LogRecord) -> dict: ...
