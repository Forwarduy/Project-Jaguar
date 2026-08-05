# agents/planning.py
from agents.base import BaseAgent
from agents.result import AgentResult
from agents.schemas import PlanningOutput

class PlanningAgent(BaseAgent):
    def execute(self, project_name: str = None, requirements: str = None, **kwargs) -> AgentResult:
        if not project_name:
            return AgentResult.fail("Project name is required")

        try:
            output: PlanningOutput = self._call_llm_structured(
                prompt=f"Plan project {project_name} with requirements: {requirements}",
                response_schema=PlanningOutput
            )
            return AgentResult.ok(
                content=f"Plan created for project: {output.project_name}",
                data=output.model_dump()
            )
        except Exception as e:
            return AgentResult.fail(f"Planning execution failed: {e}")
