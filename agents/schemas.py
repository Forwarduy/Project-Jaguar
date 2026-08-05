from typing import List, Optional
from pydantic import BaseModel, Field


class ResearchOutput(BaseModel):
    topic: str
    key_findings: List[str]
    sources_cited: List[str]
    confidence_score: float = Field(ge=0.0, le=1.0)


class PlanningStep(BaseModel):
    step_number: int
    title: str
    description: str
    estimated_hours: float


class PlanningOutput(BaseModel):
    project_name: str
    summary: str
    steps: List[PlanningStep]


class OutreachOutput(BaseModel):
    subject: str
    body: str
    target_audience: str
    call_to_action: str
