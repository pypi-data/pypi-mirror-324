import json
import logging
import traceback
from typing import Sequence

LEVELS = {
    logging.DEBUG: 7,
    logging.INFO: 6,
    logging.WARNING: 4,
    logging.ERROR: 3,
    logging.CRITICAL: 2,
}


DEFAULT_EXCLUDED_FIELDS = (
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "id",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info" "thread",
    "threadName",
)


class GELFFormatter(logging.Formatter):
    def __init__(
        self,
        hostname: str,
        service: str,
        debug: bool = False,
        include_extra_fields: bool = True,
        excluded_fields: Sequence[str] = DEFAULT_EXCLUDED_FIELDS,
        gelf_version: str = "1.1",
        json_encoder: json.JSONEncoder = None,
    ):
        self.debug = debug
        self.hostname = hostname
        self.include_extra_fields = include_extra_fields
        self.excluded_fields = excluded_fields
        self.gelf_version = gelf_version
        self.additional_fields = {"service": service}
        self.json_encoder = json_encoder or json.JSONEncoder()

    def extract_exc_info(self, record: logging.LogRecord):
        info = {}
        if record.exc_info:
            info["full_message"] = "\n".join(
                traceback.format_exception(*record.exc_info)
            )
        elif record.exc_text is not None:
            # QueueHandler, if used, formats the record, so that exc_info will always be empty:
            # https://docs.python.org/3/library/logging.handlers.html#logging.handlers.QueueHandler
            info["full_message"] = record.exc_text
        return info

    def extract_debug_info(self, record: logging.LogRecord):
        return {
            "_file": record.filename,
            "_line": record.lineno,
            "_module": record.module,
            "_func": record.funcName,
            "_logger_name": record.name,
        }

    def extract_extra_fields(self, record: logging.LogRecord):
        extra = {}
        for field, value in record.__dict__.items():
            if not field.startswith("_") and not field in self.excluded_fields:
                extra["_" + field] = value
        for field, value in self.additional_fields.items():
            if not field.startswith("_") and not field in self.excluded_fields:
                extra["_" + field] = value
        return extra

    def format(self, record):
        output = {
            "version": self.gelf_version,
            "short_message": record.getMessage(),
            "timestamp": record.created,
            "level": LEVELS[record.levelno],
            "host": self.hostname,
            "logger": record.name,
            **self.extract_exc_info(record),
        }

        if self.debug:
            output.update(self.extract_debug_info(record))

        if self.include_extra_fields:
            output.update(self.extract_extra_fields(record))

        return self.json_encoder.encode(output)
