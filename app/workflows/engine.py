from typing import Callable, List, Dict, Any
from sqlmodel import Session

class WorkflowEngine:
    def __init__(self, session: Session, workflow_name: str):
        self.session = session
        self.workflow_name = workflow_name
        self.steps: List[Callable[[Dict[str, Any]], Dict[str, Any]]] = []
        self.state: Dict[str, Any] = {}

    def add_step(self, step_func: Callable[[Dict[str, Any]], Dict[str, Any]]):
        """Agrega un paso (función) al pipeline de ejecución."""
        self.steps.append(step_func)

    def execute(self, initial_state: Dict[str, Any]) -> "WorkflowEngine":
        """Ejecuta secuencialmente todos los pasos del workflow."""
        self.state = initial_state
        for step in self.steps:
            self.state = step(self.state)
        return self

    def get_state(self) -> Dict[str, Any]:
        """Devuelve el estado actual de la ejecución."""
        return self.state
