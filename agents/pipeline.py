"""Pipeline orchestration engine for managing multi-agent execution sequences with persistence."""

from typing import Any, Callable, List, Optional
from agents.storage import SessionStore


class AgentPipeline:
    """Orchestrates a sequence of agent steps with state preservation and session checkpointing."""

    def __init__(
        self,
        steps: Optional[List[Callable[[Any], Any]]] = None,
        session_id: Optional[str] = None,
        storage_dir: Optional[str] = None,
    ):
        self.steps = steps or []
        self.session_id = session_id
        self.store = SessionStore(storage_dir=storage_dir)
        self.current_step_index = 0

    def add_step(self, step_func: Callable[[Any], Any]) -> "AgentPipeline":
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


# Alias for compatibility with tests using Pipeline
Pipeline = AgentPipeline
