from typing import Optional
from sqlmodel import SQLModel, Field

class WorkflowStateModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    workflow_name: str
    current_state_json: str
    step_name: Optional[str] = None
