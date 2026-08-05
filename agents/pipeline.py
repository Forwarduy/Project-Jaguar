"""Sequential and contextual agent execution pipeline for Project-Jaguar."""

from typing import Any, List, Optional, Union
from agents.base import BaseAgent
from agents.result import AgentResult


class AgentPipeline:
    """Executes a series of agents sequentially with fail-fast enforcement."""

    def __init__(
        self,
        registry: Optional[Any] = None,
        steps: Optional[List[Union[BaseAgent, str]]] = None,
    ):
        if isinstance(registry, list) and steps is None:
            steps = registry
            registry = None

        self.registry = registry
        self.steps: List[BaseAgent] = []
        if steps:
            for step in steps:
                self.add_step(step)

    def add_step(self, step: Union[BaseAgent, str]) -> "AgentPipeline":
        """Adds an agent instance or registered agent name to the execution chain."""
        if isinstance(step, str):
            agent_factory = None
            if self.registry and hasattr(self.registry, "get"):
                agent_factory = self.registry.get(step)
            if not agent_factory:
                from agents.registry import AgentRegistry

                agent_factory = AgentRegistry.get(step)

            if agent_factory is None:
                raise ValueError(f"Agent '{step}' not found in registry")

            if isinstance(agent_factory, BaseAgent):
                self.steps.append(agent_factory)
            elif callable(agent_factory):
                self.steps.append(agent_factory())
            else:
                raise TypeError(f"Registered agent '{step}' is invalid.")
        elif isinstance(step, BaseAgent):
            self.steps.append(step)
        else:
            raise TypeError(
                f"Invalid step type: {type(step)}. Expected BaseAgent instance or registered agent name."
            )
        return self

    def run(self, initial_input: str = "", **kwargs: Any) -> AgentResult:
        """Executes all pipeline steps sequentially with fail-fast mechanics."""
        if not self.steps:
            return AgentResult.fail("Pipeline execution failed: No steps configured in pipeline")

        current_input = initial_input
        last_result = None

        for step in self.steps:
            if current_input:
                try:
                    last_result = step.run(current_input, **kwargs)
                except TypeError:
                    last_result = step.run(input_data=current_input, **kwargs)
            else:
                last_result = step.run(**kwargs)

            if not last_result.success:
                return last_result
            current_input = last_result.content

        return last_result or AgentResult.fail("Pipeline completed without result")

    def run_chain(
        self, chain_spec: Union[str, List[str]], initial_input: str = "", **kwargs: Any
    ) -> AgentResult:
        """Configures and executes a chain specified by a comma-separated string or list."""
        if isinstance(chain_spec, str):
            agent_names = [name.strip() for name in chain_spec.split(",") if name.strip()]
        elif isinstance(chain_spec, list):
            agent_names = chain_spec
        else:
            return AgentResult.fail("Invalid chain specification format")

        if not agent_names:
            return AgentResult.fail("Chain specification is empty")

        self.steps = []
        for name in agent_names:
            self.add_step(name)

        return self.run(initial_input=initial_input, **kwargs)

    def execute(self, **kwargs: Any) -> AgentResult:
        """Execution wrapper for backwards compatibility across test suites."""
        return self.run(**kwargs)
