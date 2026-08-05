"""Unit tests for Project Jaguar structured logging and auditing."""

import json
import logging
import pytest
from agents.logging import get_logger, set_correlation_id, JsonFormatter


def test_json_formatter():
    """Test that JsonFormatter outputs valid JSON with required base fields."""
    formatter = JsonFormatter()
    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="test.py",
        lineno=1,
        msg="Test execution message",
        args=(),
        exc_info=None
    )
    output = formatter.format(record)
    data = json.loads(output)
    
    assert data["level"] == "INFO"
    assert data["message"] == "Test execution message"
    assert data["logger"] == "test_logger"
    assert "timestamp" in data


def test_correlation_id_context():
    """Test correlation ID context variable setting and inclusion in logs."""
    corr_id = "jaguar-corr-xyz-987"
    set_correlation_id(corr_id)
    
    formatter = JsonFormatter()
    record = logging.LogRecord(
        name="audit_logger",
        level=logging.INFO,
        pathname="test.py",
        lineno=1,
        msg="Audited secured action",
        args=(),
        exc_info=None
    )
    output = formatter.format(record)
    data = json.loads(output)
    
    assert data["correlation_id"] == corr_id


def test_get_logger_creation():
    """Test that get_logger creates and configures a structured logger properly."""
    logger = get_logger("jaguar.enterprise.audit")
    assert logger.name == "jaguar.enterprise.audit"
    assert len(logger.handlers) > 0
    assert logger.propagate is False
