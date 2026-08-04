from pydantic import BaseModel, ConfigDict


class AgentResult(BaseModel):
    """
    Objeto de transferencia de datos inmutable que representa 
    el resultado estandarizado de la ejecución de cualquier agente.
    """
    model_config = ConfigDict(frozen=True)

    success: bool
    content: str = ""
    error: str | None = None

    @classmethod
    def ok(cls, content: str) -> "AgentResult":
        """Crea un resultado exitoso cargado con el contenido generado."""
        return cls(success=True, content=content)

    @classmethod
    def fail(cls, error: str) -> "AgentResult":
        """Crea un resultado fallido con la descripción del error."""
        return cls(success=False, error=error)

    def __str__(self) -> str:
        return self.content if self.success else f"❌ {self.error}"
