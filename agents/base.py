import asyncio
from abc import ABC, abstractmethod
from typing import Any
from .result import AgentResult


class BaseAgent(ABC):
    """Clase base para todos los agentes. No instanciable directamente:
    cada subclase debe implementar su propio run()."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def run(self, input_text: str, **kwargs: Any) -> AgentResult:
        """Contrato estandarizado: recibe una entrada de texto principal (topic, goal, campaign)
        y argumentos opcionales, devolviendo siempre un AgentResult."""
        pass

    async def arun(self, input_text: str, **kwargs: Any) -> AgentResult:
        """Ejecución asíncrona por defecto delegando la ejecución síncrona a un hilo secundario.
        Las subclases pueden sobrescribirlo con soporte nativo para async/await."""
        return await asyncio.to_thread(self.run, input_text, **kwargs)

    def __call__(self, input_text: str, **kwargs: Any) -> AgentResult:
        """Permite invocar el agente directamente como una función."""
        return self.run(input_text, **kwargs)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(name={self.name!r})>"
