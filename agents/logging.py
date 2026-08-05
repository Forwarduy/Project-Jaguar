"""Structured JSON logging and auditing for Project Jaguar."""

import json
import logging
import sys
import uuid
from contextvars import ContextVar
from typing import Any, Dict, Optional

correlation_id_var: ContextVar[str] = ContextVar("correlation_id", default="")


class JsonFormatter(logging.Formatter):
    """Formatter that outputs JSON-encoded log strings with correlation IDs and audit context."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record into a structured JSON string."""
        log_record: Dict[str, Any] = {
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "timestamp": self.formatTime(record, self.datefmt),
        }
        
        corr_id = correlation_id_var.get()
        if corr_id:
            log_record["correlation_id"] = corr_id
            
        if hasattr(record, "extra_data") and isinstance(record.extra_data, dict):
            log_record.update(record.extra_data)
            
        return json.dumps(log_record)


def get_logger(name: str) -> logging.Logger:
    """Get a configured structured JSON logger instance."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False
    return logger


def set_correlation_id(corr_id: Optional[str] = None) -> str:
    """Set or generate a correlation ID for the current execution context."""
    new_id = corr_id or str(uuid.uuid4())
    correlation_id_var.set(new_id)
    return new_id
