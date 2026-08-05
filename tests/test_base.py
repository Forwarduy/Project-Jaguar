"""Tests for BaseAgent and core execution mechanisms."""

import pytest
from agents.base import BaseAgent
from agents.result import AgentResult


class DummyConcreteAgent(BaseAgent):
    def run(self, input_data=None):
        if input_data == "error":
            raise ValueError("Intentional error")
        return AgentResult.ok(content=f"Processed: {input_data}")


def test_base_agent_execution_success():
    agent = DummyConcreteAgent(name="TestAgent")
    assert agent.name == "TestAgent"
    res = agent.execute("hello")
    assert res.success is True
    assert res.content == "Processed: hello"


def test_base_agent_execution_failure_handling():
    agent = DummyConcreteAgent()
    res = agent.execute("error")
    assert res.success is False
    assert "Intentional error" in res.error
