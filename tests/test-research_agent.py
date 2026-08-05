from unittest.mock import patch
from pydantic import SecretStr
from config import Settings
from agents.research import ResearchAgent
from agents.schemas import ResearchOutput


def test_research_agent_missing_topic():
    agent = ResearchAgent()
    res = agent.execute()
    assert not res.success
    assert "required" in res.error.lower()


@patch("agents.base.get_settings")
@patch.object(ResearchAgent, "_call_llm_structured")
def test_research_agent_success(mock_structured_call, mock_get_settings):
    mock_get_settings.return_value = Settings(anthropic_api_key=SecretStr("test-key"))
    mock_structured_call.return_value = ResearchOutput(
        topic="Distributed Systems",
        key_findings=["Consensus protocols are vital", "Eventual consistency trade-offs"],
        sources_cited=["https://arxiv.org"],
        confidence_score=0.98,
    )

    agent = ResearchAgent()
    res = agent.execute(topic="Distributed Systems")

    assert res.success
    assert res.data["topic"] == "Distributed Systems"
    assert len(res.data["key_findings"]) == 2
    assert res.data["confidence_score"] == 0.98
