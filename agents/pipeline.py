"""Sequential and contextual agent execution pipeline for Project-Jaguar."""

from typing import Any, List, Optional, Union
from agents.base import BaseAgent
from agents.result import AgentResult
from agents.registry import AgentRegistry


class AgentPipeline:
    """Executes a series of agents sequentially with fail-fast enforcement."""

    def __init__(self, steps: Optional[List[Union[BaseAgent, str]]] = None):
        self.steps: List[BaseAgent] = []
        if steps:
            for step in steps:
                self.add_step(step)

    def add_step(self, step: Union[BaseAgent, str]) -> "AgentPipeline":
        """Adds an agent or registered agent name to the execution chain."""
        if isinstance(step, str):
            agent_cls = AgentRegistry.get(step)
            self.steps.append(agent_cls())
        elif isinstance(step, BaseAgent):
            self.steps.append(step)
        else:
            raise TypeError(f"Invalid step type: {type(step)}. Expected BaseAgent instance or string registered key.")
        return self

    def run(self, initial_input: str = "", **kwargs: Any) -> AgentResult:
        """Executes all pipeline steps sequentially.

        Passes output content down the chain and stops immediately if any agent fails.
        """
        if not self.steps:
            return AgentResult.fail("Pipeline execution failed: No steps configured in pipeline")

        current_input = initial_input
        last_result = None

        for step in self.steps:
            last_result = step.run(input_data=current_input, **kwargs)
            if not last_result.success:
                return last_result
            current_input = last_result.content

        return last_result or AgentResult.fail("Pipeline completed without result")

    def execute(self, **kwargs: Any) -> AgentResult:
        """Execution wrapper for backwards compatibility across test suites."""
        return self.run(**kwargs)
