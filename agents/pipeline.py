"""Sequential pipeline runner for chaining multi-agent tasks."""

from typing import Any, Dict, List
from rich.console import Console

from agents.registry import AgentRegistry
from agents.result import AgentResult

console = Console()


class AgentPipeline:
    """Executes a series of agents in sequence, passing outputs down the chain."""

    def __init__(self, registry: AgentRegistry):
        self.registry = registry

    def run_chain(self, steps: List[Dict[str, Any]]) -> AgentResult:
        """
        Run steps sequentially.
        Each step format: {"agent": "research", "arg": "initial topic"}
        If a step omits "arg", the output of the previous step is automatically injected.
        """
        previous_output = None

        for idx, step in enumerate(steps, 1):
            agent_name = step.get("agent")
            if not agent_name:
                return AgentResult(
                    success=False,
                    content=f"Pipeline aborted at step {idx}: missing agent name.",
                )

            agent_target = self.registry.get(agent_name)
            if not agent_target:
                return AgentResult(
                    success=False,
                    content=f"Pipeline aborted: agent '{agent_name}' not found.",
                )

            agent = agent_target() if callable(agent_target) else agent_target

            # Use explicit arg if provided; otherwise fall back to previous agent output
            arg = step.get("arg")
            if arg is None:
                arg = previous_output

            kwargs = step.get("kwargs", {})
            try:
                if kwargs:
                    res = agent.run(arg, **kwargs)
                else:
                    res = agent.run(arg)

                content = getattr(res, "content", res)
                previous_output = str(content)
            except Exception as exc:
                return AgentResult(
                    success=False,
                    content=f"Pipeline failed at step {idx} ({agent_name}): {exc}",
                )

        return AgentResult(success=True, content=previous_output or "")
