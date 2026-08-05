# agents/research.py
from agents.base import BaseAgent
from agents.result import AgentResult
from agents.schemas import ResearchOutput


class ResearchAgent(BaseAgent):
    name: str = "ResearchAgent"

    def run(self, topic: str = None, **kwargs) -> AgentResult:
        if not topic:
            return AgentResult.fail("Topic is required")

        try:
            output: ResearchOutput = self._call_llm_structured(
                schema_cls=ResearchOutput,
                prompt=f"Research topic: {topic}",
                client=kwargs.get("client"),
            )
            return AgentResult.ok(
                content=f"Research output for topic: {output.topic}",
                data=output.model_dump(),
            )
        except Exception as e:
            return AgentResult.fail(f"Research execution failed: {e}")

    def execute(self, **kwargs) -> AgentResult:
        return self.run(**kwargs)
