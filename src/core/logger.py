import json
import logging
import sys
from contextvars import ContextVar
from datetime import datetime, timezone

_request_id: ContextVar[str] = ContextVar("request_id", default="")


def set_request_id(value: str) -> None:
  _request_id.set(value)


def get_request_id() -> str:
  return _request_id.get()


class JsonFormatter(logging.Formatter):
  def format(self, record: logging.LogRecord) -> str:
    entry = {
      "timestamp": datetime.now(tz=timezone.utc).isoformat(),
      "level": record.levelname,
      "logger": record.name,
      "message": record.getMessage(),
      "request_id": get_request_id(),
    }
    if hasattr(record, "props"):
      entry.update(record.props)
    return json.dumps(entry, ensure_ascii=False)


def setup_logger() -> logging.Logger:
  logger = logging.getLogger("api")
  logger.setLevel(logging.INFO)
  if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)
  return logger


logger = setup_logger()
