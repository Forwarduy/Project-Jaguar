from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """Clase base para todos los agentes. No instanciable directamente:
    cada subclase debe implementar su propio run()."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def run(self, *args, **kwargs) -> str:
        """Cada agente define su propia firma (topic, goal, campaign, etc.)
        según lo que necesite — el contrato es: recibe input, devuelve str."""
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name!r}>"
