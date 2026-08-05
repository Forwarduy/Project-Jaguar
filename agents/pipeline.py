"""Sequential and contextual agent execution pipeline for Project-Jaguar."""

from typing import Any, List, Optional, Union
from agents.base import BaseAgent
from agents.result import AgentResult


class AgentPipeline:
    """Executes a series of agents sequentially with fail-fast enforcement."""

    def __init__(
        self,
        registry: Optional[Any] = None,
        steps: Optional[List[Union[BaseAgent, str, dict]]] = None,
    ):
        if isinstance(registry, list) and steps is None:
            steps = registry
            registry = None

        self.registry = registry
        self.steps: List[BaseAgent] = []
        self._step_args: List[Optional[str]] = []

        if steps:
            for step in steps:
                self.add_step(step)

    def _lookup_agent(self, agent_name: str) -> Any:
        """Looks up an agent by name from instance registry or global registry."""
        agent_factory = None

        if self.registry is not None and hasattr(self.registry, "get"):
            try:
                agent_factory = self.registry.get(agent_name)
            except KeyError:
                agent_factory = None

        if agent_factory is None:
            try:
                from agents.registry import AGENT_REGISTRY

                agent_factory = AGENT_REGISTRY.get(agent_name)
            except Exception:
                agent_factory = None

        if agent_factory is None:
            try:
                from agents.registry import AgentRegistry

                reg = AgentRegistry()
                agent_factory = reg.get(agent_name)
            except Exception:
                agent_factory = None

        if agent_factory is None:
            raise KeyError(f"Agent '{agent_name}' not found in registry")

        if isinstance(agent_factory, BaseAgent):
            return agent_factory
        if callable(agent_factory):
            return agent_factory()
        return agent_factory

    def add_step(self, step: Union[BaseAgent, str, dict]) -> "AgentPipeline":
        """Adds an agent instance, registered agent name, or step spec dictionary to the pipeline."""
        if isinstance(step, str):
            self.steps.append(self._lookup_agent(step))
            self._step_args.append(None)
        elif isinstance(step, BaseAgent):
            self.steps.append(step)
            self._step_args.append(None)
        elif isinstance(step, dict):
            agent_ref = step.get("agent") or step.get("name") or step.get("step")
            if not agent_ref:
                raise KeyError("Step dictionary missing 'agent' key")
            step_arg = step.get("arg") or step.get("input") or step.get("input_data")

            if isinstance(agent_ref, str):
                agent_inst = self._lookup_agent(agent_ref)
            elif isinstance(agent_ref, BaseAgent):
                agent_inst = agent_ref
            elif callable(agent_ref):
                agent_inst = agent_ref()
            else:
                agent_inst = agent_ref

            self.steps.append(agent_inst)
            self._step_args.append(step_arg)
        else:
            raise TypeError(f"Invalid step type: {type(step)}")

        return self

    def run(self, initial_input: str = "", **kwargs: Any) -> AgentResult:
        """Executes all pipeline steps sequentially with fail-fast mechanics."""
        if not self.steps:
            return AgentResult.fail("Pipeline execution failed: No steps provided")

        current_input = initial_input
        last_result = None

        for i, agent in enumerate(self.steps):
            step_arg = self._step_args[i] if i < len(self._step_args) else None
            exec_input = step_arg if step_arg is not None else current_input

            if hasattr(agent, "run"):
                try:
                    last_result = agent.run(exec_input, **kwargs)
                except TypeError:
                    last_result = agent.run(input_data=exec_input, **kwargs)
            elif callable(agent):
                last_result = agent(exec_input, **kwargs)
            else:
                return AgentResult.fail(f"Invalid agent step: {agent}")

            if not last_result or not getattr(last_result, "success", False):
                return last_result or AgentResult.fail("Step execution failed")

            current_input = getattr(last_result, "content", "") or current_input

        return last_result or AgentResult.fail("Pipeline completed without result")

    def run_chain(
        self, chain_spec: Union[str, List[Any]], initial_input: str = "", **kwargs: Any
    ) -> AgentResult:
        """Configures and executes a chain specified by a string, list, or step dictionaries."""
        self.steps = []
        self._step_args = []

        if isinstance(chain_spec, str):
            steps_list = [s.strip() for s in chain_spec.split(",") if s.strip()]
        elif isinstance(chain_spec, list):
            steps_list = chain_spec
        else:
            return AgentResult.fail("No steps provided: invalid chain specification format")

        if not steps_list:
            return AgentResult.fail("No steps provided in chain specification")

        for step in steps_list:
            self.add_step(step)

        return self.run(initial_input=initial_input, **kwargs)

    def execute(self, initial_input: str = "", **kwargs: Any) -> AgentResult:
        """Execution wrapper for backwards compatibility across test suites."""
        return self.run(initial_input=initial_input, **kwargs)
