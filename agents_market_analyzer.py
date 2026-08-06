from typing import Type
from pydantic import BaseModel, Field
from app.agents.base import BaseAgent

class MarketInput(BaseModel):
    query: str
    target_market: str

class MarketOutput(BaseModel):
    viability_score: float = Field(description="Puntuación de 0.0 a 10.0")
    analysis_summary: str = Field(description="Resumen ejecutivo del análisis")
    key_risks: list[str] = Field(description="Lista de riesgos identificados")

class MarketAnalyzerAgent(BaseAgent[MarketInput, MarketOutput]):
    def __init__(self):
        super().__init__(
            agent_name="MarketAnalyzerAgent",
            system_prompt="Eres un analista de mercados experto impulsado por Claude, especializado en viabilidad comercial y evaluación de riesgos."
        )

    def fmt_input(self, data: dict) -> MarketInput:
        return MarketInput(
            query=data.get("query", ""),
            target_market=data.get("target_market", "Global")
        )

    def get_output_schema(self) -> Type[MarketOutput]:
        return MarketOutput
