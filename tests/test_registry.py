import pytest
from agents.base import BaseAgent
from agents.registry import AgentRegistry, get_agent, list_agents, AGENT_REGISTRY


class DummyAgent(BaseAgent):
    name = "dummy"

    def run(self, **kwargs):
        pass


def test_registry_direct_register():
    reg = AgentRegistry()
    reg.register("dummy", DummyAgent)
    agent = reg.get("dummy")
    assert isinstance(agent, DummyAgent)


def test_registry_decorator_with_name():
    reg = AgentRegistry()

    @reg.register("custom_dummy")
    class CustomAgent(BaseAgent):
        def run(self, **kwargs):
            pass

    agent = reg.get("custom_dummy")
    assert isinstance(agent, CustomAgent)


def test_registry_decorator_without_args():
    reg = AgentRegistry()

    @reg.register
    class AutoNamedAgent(BaseAgent):
        name = "autonamed"

        def run(self, **kwargs):
            pass

    agent = reg.get("autonamed")
    assert isinstance(agent, AutoNamedAgent)


def test_registry_get_unknown():
    reg = AgentRegistry()
    with pytest.raises(KeyError):
        reg.get("non_existent_agent")


def test_registry_list_agents():
    reg = AgentRegistry()
    reg.register("dummy", DummyAgent)
    assert "dummy" in reg.list_agents()


def test_module_level_helpers():
    AGENT_REGISTRY.register("dummy_module", DummyAgent)
    assert "dummy_module" in list_agents()
    agent = get_agent("dummy_module")
    assert isinstance(agent, DummyAgent)
