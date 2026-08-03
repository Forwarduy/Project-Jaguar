from .research import ResearchAgent
from .planning import PlanningAgent
from .outreach import OutreachAgent

AGENT_REGISTRY = {
    "research": ResearchAgent,
    "plan": PlanningAgent,
    "outreach": OutreachAgent,
}
