# agents/__init__.py
from agents.base import BaseAgent
from agents.result import AgentResult

# Ensure these submodules exist before exposing them here:
from agents.research import ResearchAgent  # Ensure agents/research.py exists
from agents.planning import PlanningAgent  # Ensure agents/planning.py exists
from agents.outreach import OutreachAgent  # Ensure agents/outreach.py exists

__all__ = [
    "BaseAgent",
    "AgentResult",
    "ResearchAgent",
    "PlanningAgent",
    "OutreachAgent",
]
