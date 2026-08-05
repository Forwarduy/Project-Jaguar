# agents/outreach.py
from agents.base import BaseAgent
from agents.result import AgentResult
from agents.schemas import OutreachOutput

class OutreachAgent(BaseAgent):
    def execute(self, target_audience: str = None, goal: str = None, **kwargs) -> AgentResult:
        if not target_audience or not goal:
            return AgentResult.fail("Target audience and goal are required")

        try:
            output: OutreachOutput = self._call_llm_structured(
                prompt=f"Outreach for {target_audience} regarding {goal}",
                response_schema=OutreachOutput
            )
            return AgentResult.ok(
                content=f"Outreach strategy generated for: {output.target_audience}",
                data=output.model_dump()
            )
        except Exception as e:
            return AgentResult.fail(f"Outreach execution failed: {e}")
