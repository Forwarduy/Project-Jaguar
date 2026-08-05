from unittest.mock import MagicMock
import pytest
import anthropic
from agents.base import BaseAgent
from agents.schemas import ResearchOutput
from agents.result import AgentResult


class ResilienceTestAgent(BaseAgent):
    name = "ResilienceTestAgent"

    def run(self, **kwargs) -> AgentResult:
        return AgentResult.ok(data={"status": "success"})


def test_call_llm_with_retry_success():
    agent = ResilienceTestAgent()
    mock_client = MagicMock()
    
    mock_response = MagicMock()
    mock_response.content = "Success response"
    mock_client.messages.create.return_value = mock_response

    result = agent._call_llm_with_retry(mock_client, model="claude-3-5-sonnet-20241022", messages=[])
    
    assert result.content == "Success response"
    assert mock_client.messages.create.call_count == 1


def test_call_llm_with_retry_failure_and_retry():
    agent = ResilienceTestAgent()
    mock_client = MagicMock()

    # Simulate rate limit failure twice, then success
    mock_response = MagicMock()
    mock_response.content = "Recovered response"
    
    rate_limit_error = anthropic.RateLimitError(
        message="Rate limit exceeded",
        response=MagicMock(status_code=429),
        body={}
    )
    
    mock_client.messages.create.side_effect = [
        rate_limit_error,
        rate_limit_error,
        mock_response
    ]

    result = agent._call_llm_with_retry(mock_client, model="claude-3-5-sonnet-20241022", messages=[])
    
    assert result.content == "Recovered response"
    assert mock_client.messages.create.call_count == 3


def test_call_llm_structured_success():
    agent = ResilienceTestAgent()

    # Mock client and structured tool output response
    mock_client = MagicMock()
    mock_block = MagicMock()
    mock_block.type = "tool_use"
    mock_block.name = "submit_structured_output"
    mock_block.input = {
        "topic": "Testing Resilience",
        "key_findings": ["Pass 1", "Pass 2"],
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
    assert len(res.key_findings) == 2
    assert res.confidence_score == 0.95
    assert mock_client.messages.create.call_count == 1


def test_call_llm_structured_missing_tool_call_raises_value_error():
    agent = ResilienceTestAgent()

    # Mock client returning plain text instead of expected tool call
    mock_client = MagicMock()
    mock_block = MagicMock()
    mock_block.type = "text"
    mock_block.text = "Just plain text response"

    mock_response = MagicMock()
    mock_response.content = [mock_block]
    mock_client.messages.create.return_value = mock_response

    with pytest.raises(ValueError, match="LLM failed to return structured tool execution output."):
        agent._call_llm_structured(
            client=mock_client,
            schema_cls=ResearchOutput,
            prompt="Analyze resilience patterns",
        )
