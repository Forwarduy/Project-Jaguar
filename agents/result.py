from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class AgentResult(BaseModel):
    success: bool
    content: str = ""
    error: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @property
    def data(self) -> Optional[Dict[str, Any]]:
        """Propiedad alias para mantener compatibilidad con tests que inspeccionan .data"""
        if not self.success and not self.metadata and self.content == "":
            return None
        return {"research": self.content, **self.metadata}
