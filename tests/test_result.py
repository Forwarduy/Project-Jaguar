"""Tests para AgentResult."""
from agents.result import AgentResult


def test_success_result_str():
    result = AgentResult.ok("hola")
    assert result.success is True
    assert str(result) == "hola"


def test_error_result_str():
    result = AgentResult.fail("algo falló")
    assert result.success is False
    assert str(result) == "❌ algo falló"
