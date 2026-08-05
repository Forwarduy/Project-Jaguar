    def _call_llm_structured(
        self,
        client: Any,
        schema_cls: Type[BaseModel],
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
    ) -> BaseModel:
        """Helper to invoke an LLM and enforce structured JSON output using tool use / schemas."""
        settings = get_settings()
        if not settings.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY is not configured")
        
        target_model = model or settings.anthropic_model
        # ... resto del método de llamada al LLM
