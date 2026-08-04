def test_registry_has_all_three_commands():
    assert set(AGENT_REGISTRY.keys()) == {"research", "plan", "planning", "outreach"}

def test_registry_maps_to_correct_classes():
    assert AGENT_REGISTRY["research"] is ResearchAgent
    assert AGENT_REGISTRY["plan"] is PlanningAgent
    assert AGENT_REGISTRY["planning"] is PlanningAgent  # alias
    assert AGENT_REGISTRY["outreach"] is OutreachAgent
