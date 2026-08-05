from unittest.mock import MagicMock
import pytest
from agents.base import BaseAgent
from agents.schemas import ResearchOutput


class ResilienceTestAgent(BaseAgent):
    """Concrete agent subclass for resilience unit tests."""
    name: str = "ResilienceTestAgent"

    def run(self, **kwargs):
        pass


def test_call_llm_structured_success():
    agent = ResilienceTestAgent()

    mock_client = MagicMock()
    mock_block = MagicMock()
    mock_block.type = "tool_use"
    mock_block.name = "submit_structured_output"
    mock_block.input = {
        "topic": "Testing Resilience",
        "key_findings": ["Pass 1", "Pass 2"],
        "sources_cited": ["https://example.com/resilience"],
        "confidence_score": 0.95,
    }

    mock_response = MagicMock()
    mock_response.content = [mock_block]
    mock_client.messages.create.return_value = mock_response

    res = agent._call_llm_structured(
        client=mock_client,
        schema_cls=ResearchOutput,
        prompt="Analyze resilience patterns",
    )
    assert res.topic == "Testing Resilience"
