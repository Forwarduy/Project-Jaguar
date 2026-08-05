import pytest
from pydantic import ValidationError
from agents.schemas import ResearchOutput, PlanningStep, PlanningOutput, OutreachOutput


def test_research_output_schema():
    data = ResearchOutput(
        topic="AI Market Trends",
        key_findings=["Finding 1", "Finding 2"],
        sources_cited=["https://example.com"],
        confidence_score=0.95,
    )
    assert data.topic == "AI Market Trends"
    assert len(data.key_findings) == 2
    assert data.confidence_score == 0.95


def test_research_output_invalid_score():
    with pytest.raises(ValidationError):
        ResearchOutput(
            topic="Test",
            key_findings=["Test"],
            confidence_score=1.5,  # Exceeds le=1.0 constraint
        )


def test_planning_output_schema():
    step = PlanningStep(
        step_number=1,
        title="Setup",
        description="Initialize repo",
        estimated_hours=2.0,
    )
    plan = PlanningOutput(
        project_name="Jaguar",
        summary="Build system",
        steps=[step],
    )
    assert plan.project_name == "Jaguar"
    assert plan.steps[0].step_number == 1


def test_outreach_output_schema():
    outreach = OutreachOutput(
        subject="Hello",
        body="Body text",
        target_audience="Devs",
        call_to_action="Click here",
    )
    assert outreach.subject == "Hello"
    assert outreach.call_to_action == "Click here"
