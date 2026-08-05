def _call_llm_structured(
    self,
    client: Any,
    schema_cls: Type[T],
    prompt: str,
    system_prompt: str = "",
    model: str = "claude-3-5-sonnet-20241022",
) -> T:
    # API Key check expected by test_research_agent_missing_api_key
    if not self.settings.anthropic_api_key.get_secret_value():
        raise ValueError("ANTHROPIC_API_KEY is not configured")
    ...
