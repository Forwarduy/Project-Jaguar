from abc import ABC, abstractmethod
from typing import Any
from config import get_settings
from agents.result import AgentResult

class BaseAgent(ABC):
    name: str = "BaseAgent"

    def __init__(self):
        self.settings = get_settings()

    @abstractmethod
    def run(self, *args: Any, **kwargs: Any) -> AgentResult:
        pass

    def execute(self, *args: Any, **kwargs: Any) -> AgentResult:
        topic = kwargs.pop("topic", None)
        if topic is not None and not args:
            return self.run(topic, **kwargs)
        return self.run(*args, **kwargs)
