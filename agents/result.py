from pydantic import BaseModel


class AgentResult(BaseModel):
    success: bool
    content: str = ""
    error: str | None = None

    @classmethod
    def ok(cls, content: str) -> "AgentResult":
        return cls(success=True, content=content)

    @classmethod
    def fail(cls, error: str) -> "AgentResult":
        return cls(success=False, error=error)

    def __str__(self) -> str:
        return self.content if self.success else f"❌ {self.error}"
