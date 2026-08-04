from abc import ABC, abstractmethod
from .result import AgentResult


class BaseAgent(ABC):
    """Clase base para todos los agentes. No instanciable directamente:
    cada subclase debe implementar su propio run()."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def run(self, input_text: str, **kwargs) -> AgentResult:
        """Contrato estandarizado: recibe una entrada de texto principal (topic, goal, campaign)
        y argumentos opcionales, devolviendo siempre un AgentResult."""
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(name={self.name!r})>"
