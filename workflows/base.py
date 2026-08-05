from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseWorkflow(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        """Nombre único del flujo de trabajo."""
        pass

    @abstractmethod
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecuta la lógica de negocio coordinando los agentes y

        registrando los estados en la base de datos.
        """
        pass
