from unittest.mock import patch
from config import Settings
from agents.planning import PlanningAgent
from agents.schemas import PlanningStep, PlanningOutput


def test_planning_agent_missing_project_name():
    agent = PlanningAgent()
    res = agent.execute()
    assert not res.success
    assert "required" in res.error.lower()


@patch("agents.base.get_settings")
@patch.object(PlanningAgent, "_call_llm_structured")
def test_planning_agent_success(mock_structured_call, mock_get_settings):
    mock_get_settings.return_value = Settings(anthropic_api_key="test-key")
    mock_structured_call.return_value = PlanningOutput(
        project_name="Jaguar Migration",
        summary="Migrate legacy pipeline",
        steps=[
            PlanningStep(
                step_number=1,
                title="Audit",
                description="Audit legacy code",
                estimated_hours=4.0,
            )
        ],
    )

    agent = PlanningAgent()
    res = agent.execute(project_name="Jaguar Migration", requirements="Audit and migrate")

    assert res.success
    assert res.data["project_name"] == "Jaguar Migration"
    assert res.data["steps"][0]["title"] == "Audit"
