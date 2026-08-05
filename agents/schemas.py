from typing import List, Optional
from pydantic import BaseModel, Field


class ResearchOutput(BaseModel):
    """Structured output for ResearchAgent."""

    topic: str
    key_findings: List[str] = Field(description="List of main research findings")
    sources_cited: List[str] = Field(default_factory=list)
    confidence_score: float = Field(ge=0.0, le=1.0)


class PlanningStep(BaseModel):
    step_number: int
    title: str
    description: str
    estimated_hours: Optional[float] = None


class PlanningOutput(BaseModel):
    """Structured output for PlanningAgent."""

    project_name: str
    summary: str
    steps: List[PlanningStep]


class OutreachOutput(BaseModel):
    """Structured output for OutreachAgent."""

    subject: str
    body: str
    target_audience: str
    call_to_action: str
