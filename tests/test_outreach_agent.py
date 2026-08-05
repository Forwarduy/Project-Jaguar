from unittest.mock import patch
from agents.outreach import OutreachAgent
from agents.schemas import OutreachOutput


def test_outreach_agent_missing_params():
    agent = OutreachAgent()
    res = agent.execute()
    assert not res.success


@patch.object(OutreachAgent, "_call_llm_structured")
def test_outreach_agent_success(mock_structured_call):
    mock_structured_call.return_value = OutreachOutput(
        subject="Partnership Proposal",
        body="Let's collaborate on AI agents.",
        target_audience="CTOs",
        call_to_action="Schedule a call",
    )

    agent = OutreachAgent()
    res = agent.execute(target_audience="CTOs", goal="Partnership")

    assert res.success
    assert res.data["subject"] == "Partnership Proposal"
    assert res.data["target_audience"] == "CTOs"
