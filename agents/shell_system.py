"""Interactive shell system and REPL command dispatcher for Project-Jaguar."""

import shlex
import sys
from typing import Any, Dict, List, Optional
from agents.base import BaseAgent
from agents.result import AgentResult
from agents.pipeline import AgentPipeline
from agents.registry import AGENT_REGISTRY


class SystemValidationError(Exception):
    """Raised when system or environment validation checks fail."""

    pass


def verify_runtime_environment(strict: bool = False) -> bool:
    """Validates Python runtime and system requirements for execution."""
    if sys.version_info < (3, 9):
        if strict:
            raise SystemValidationError("Python 3.9 or higher is required.")
        return False
    return True


class ShellSystem(BaseAgent):
    """Interactive command processor and REPL handler for registered agents."""

    def __init__(
        self,
        name: str = "shell_system",
        registry: Optional[Any] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(name=name, **kwargs)
        self.registry = registry if registry is not None else AGENT_REGISTRY

    def parse_command(self, raw_input: str) -> Dict[str, Any]:
        """Parses a raw command string into an action and argument list."""
        if not raw_input:
            return {"action": "empty", "args": []}
        
        trimmed = str(raw_input).strip()
        if not trimmed:
            return {"action": "empty", "args": []}

        try:
            tokens = shlex.split(trimmed)
        except ValueError:
            tokens = trimmed.split()

        if not tokens:
            return {"action": "empty", "args": []}

        return {"action": tokens[0].lower(), "args": tokens[1:]}

    def execute_command(self, raw_input: str = "") -> AgentResult:
        """Executes a single REPL shell command and returns an AgentResult."""
        parsed = self.parse_command(raw_input)
        action = parsed["action"]
        args = parsed["args"]

        if action == "empty":
            return AgentResult.ok(
                content="Shell ready.",
                metadata={"action": "empty"}
            )

        if action in ("exit", "quit"):
            return AgentResult.ok(
                content="Exiting shell session.",
                metadata={"action": "exit", "should_exit": True},
            )

        if action == "help":
            help_text = (
                "Available Commands:\n"
                "  list                  - List all registered agents\n"
                "  run <agent> [input]   - Execute a single agent\n"
                "  chain <a1,a2> [input] - Execute a sequence of agents\n"
                "  help                  - Show available commands\n"
                "  exit / quit           - Exit interactive shell"
            )
            return AgentResult.ok(content=help_text, metadata={"action": "help"})

        if action == "list":
            agents: List[str] = []
            if hasattr(self.registry, "list_agents"):
                agents = self.registry.list_agents()
            elif hasattr(self.registry, "keys"):
                agents = list(self.registry.keys())
            elif isinstance(self.registry, dict):
                agents = list(self.registry.keys())

            formatted_list = (
                "\n".join(f"- {name}" for name in agents)
                if agents
                else "No agents registered."
            )
            return AgentResult.ok(
                content=f"Registered Agents:\n{formatted_list}",
                data={"agents": agents},
                metadata={"action": "list"},
            )

        if action == "run":
            if not args:
                return AgentResult.fail(
                    content="Usage: run <agent_name> [input_data]",
                    error="Missing agent_name argument"
                )
            agent_name = args[0]
            initial_input = " ".join(args[1:]) if len(args) > 1 else ""
            pipeline = AgentPipeline(registry=self.registry)
            return pipeline.run_chain(chain_spec=agent_name, initial_input=initial_input)

        if action == "chain":
            if not args:
                return AgentResult.fail(
                    content="Usage: chain <agent1,agent2,...> [initial_input]",
                    error="Missing chain specification argument"
                )
            chain_spec = args[0]
            initial_input = " ".join(args[1:]) if len(args) > 1 else ""
            pipeline = AgentPipeline(registry=self.registry)
            return pipeline.run_chain(chain_spec=chain_spec, initial_input=initial_input)

        agent_factory = None
        if hasattr(self.registry, "get"):
            try:
                agent_factory = self.registry.get(action)
            except KeyError:
                agent_factory = None

        if agent_factory is not None:
            initial_input = " ".join(args)
            pipeline = AgentPipeline(registry=self.registry)
            return pipeline.run_chain(chain_spec=action, initial_input=initial_input)

        return AgentResult.fail(
            content=f"Unknown command: '{action}'. Type 'help' for available commands.",
            error=f"Unknown command '{action}'"
        )

    def execute(self, input_data: str = "", **kwargs: Any) -> AgentResult:
        """Executes the shell system command or defaults to empty shell result."""
        try:
            return self.execute_command(input_data)
        except Exception as exc:
            return AgentResult.fail(
                content=f"Shell system execution failed: {str(exc)}",
                error=str(exc)
            )

    def run(self, input_data: str = "", **kwargs: Any) -> AgentResult:
        """Main entry point satisfying the BaseAgent contract."""
        return self.execute(input_data=input_data, **kwargs)
