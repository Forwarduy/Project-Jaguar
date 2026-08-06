# agents/planning.py
from agents.base import BaseAgent
from agents.result import AgentResult
from agents.schemas import PlanningOutput
from agents.registry import registry


@registry.register("planning")
class PlanningAgent(BaseAgent):
    name: str = "PlanningAgent"

    def run(self, project_name: str = None, requirements: str = None, **kwargs) -> AgentResult:
        if not project_name:
            return AgentResult.fail("Project name is required")

        try:
            output: PlanningOutput = self._call_llm_structured(
                schema_cls=PlanningOutput,
                prompt=f"Plan project {project_name} with requirements: {requirements}",
                client=kwargs.get("client"),
            )
            return AgentResult.ok(
                content=f"Plan created for project: {output.project_name}",
                data=output.model_dump(),
            )
        except Exception as e:
            return AgentResult.fail(f"Planning execution failed: {e}")

    def execute(self, **kwargs) -> AgentResult:
        return self.run(**kwargs)
