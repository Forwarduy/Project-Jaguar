# agents/research.py
from agents.base import BaseAgent
from agents.result import AgentResult
from agents.schemas import ResearchOutput

class ResearchAgent(BaseAgent):
    name: str = "ResearchAgent"

    def execute(self, topic: str = None, **kwargs) -> AgentResult:
        if not topic:
            return AgentResult.fail("Topic is required")

        try:
            output: ResearchOutput = self._call_llm_structured(
                client=kwargs.get("client"),
                schema_cls=ResearchOutput,
                prompt=f"Research topic: {topic}",
            )
            return AgentResult.ok(
                content=f"Research completed for: {output.topic}",
                data=output.model_dump()
            )
        except Exception as e:
            return AgentResult.fail(f"Research execution failed: {e}")

    def run(self, **kwargs) -> AgentResult:
        return self.execute(**kwargs)
