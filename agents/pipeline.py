"""Pipeline orchestration engine for managing multi-agent execution sequences with persistence."""

from typing import Any, Callable, List, Optional
import anthropic
from agents.storage import SessionStore
from agents.result import AgentResult
from config import get_settings


class Pipeline:
    """Orchestrates a sequence of agent steps with state preservation and session checkpointing."""

    def __init__(
        self,
        steps: Optional[List[Callable[[Any], Any]]] = None,
        session_id: Optional[str] = None,
        storage_dir: Optional[str] = None,
        registry: Optional[Any] = None,
    ):
        self.steps = steps or []
        self.session_id = session_id
        self.store = SessionStore(storage_dir=storage_dir)
        self.registry = registry
        self.current_step_index = 0

    def add_step(self, step_func: Callable[[Any], Any]) -> "Pipeline":
        """Add an execution step to the pipeline."""
        self.steps.append(step_func)
        return self

    def run(self, initial_input: Any = None) -> Any:
        """Execute all steps sequentially and checkpoint state if a session ID is configured."""
        current_data = initial_input

        for index, step_func in enumerate(self.steps):
            self.current_step_index = index
            current_data = step_func(current_data)

            if self.session_id:
                state = {
                    "step_index": self.current_step_index,
                    "last_output": str(current_data),
                }
                self.store.save_checkpoint(self.session_id, state)

        return current_data

    def run_chain(self, chain_spec: str, initial_input: Any = None) -> AgentResult:
        """Execute a comma-separated chain of agent names using the provided registry and return an AgentResult."""
        agent_names = [name.strip() for name in chain_spec.split(",") if name.strip()]
        current_data = initial_input

        # Cliente construido una sola vez por cadena y reenviado a cada agente que
        # acepte client=... (los agentes que no lo necesitan simplemente lo ignoran
        # gracias al fallback TypeError de abajo). Si no hay API key, queda en
