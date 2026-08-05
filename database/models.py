from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel


class AgentStateModel(SQLModel, table=True):
    __tablename__ = "agent_states"

    id: Optional[int] = Field(default=None, primary_key=True)
    agent_id: str = Field(index=True, unique=True)
    name: str
    status: str = Field(default="IDLE")  # IDLE, BUSY, ERROR, etc.
    state_payload: str = Field(default="{}")  # Almacenamiento JSON serializado del estado
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class WorkflowExecutionModel(SQLModel, table=True):
    __tablename__ = "workflow_executions"

    id: Optional[int] = Field(default=None, primary_key=True)
    execution_id: str = Field(index=True, unique=True)  # Correlation ID
    workflow_name: str
    status: str = Field(default="PENDING")  # PENDING, SUCCESS, FAILED
    input_payload: str = Field(default="{}")
    output_payload: str = Field(default="{}")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class ArtifactModel(SQLModel, table=True):
    __tablename__ = "artifacts"

    id: Optional[int] = Field(default=None, primary_key=True)
    artifact_id: str = Field(index=True, unique=True)
    execution_id: str = Field(index=True)
    title: str
    content: str  # Reportes, planes estratégicos o documentos generados
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
