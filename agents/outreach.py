# agents/outreach.py
from agents.base import BaseAgent
from agents.result import AgentResult
from agents.schemas import OutreachOutput


class OutreachAgent(BaseAgent):
    name: str = "OutreachAgent"

    def run(self, target_audience: str = None, goal: str = None, **kwargs) -> AgentResult:
        if not target_audience or not goal:
            return AgentResult.fail("Target audience and goal are required")

        try:
            output: OutreachOutput = self._call_llm_structured(
                schema_cls=OutreachOutput,
                prompt=f"Outreach for {target_audience} regarding {goal}",
                client=kwargs.get("client"),
            )
            return AgentResult.ok(
                content=f"Outreach strategy generated for: {output.target_audience}",
                data=output.model_dump(),
            )
        except Exception as e:
            return AgentResult.fail(f"Outreach execution failed: {e}")

    def execute(self, **kwargs) -> AgentResult:
        return self.run(**kwargs)
