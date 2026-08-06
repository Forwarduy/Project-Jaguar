from sqlmodel import Session
from app.workflows.engine import WorkflowEngine
from app.agents.market_analyzer import MarketAnalyzerAgent

def run_market_research_workflow(session: Session, query: str, target_market: str) -> dict:
    engine = WorkflowEngine(session=session, workflow_name="market_research_pipeline")
    
    agent = MarketAnalyzerAgent()

    def step_analyze_market(state: dict) -> dict:
        result = agent.run({
            "query": state["query"],
            "target_market": state["target_market"]
        })
        state["market_analysis"] = result.model_dump()
        return state

    engine.add_step(step_analyze_market)

    initial_state = {
        "query": query,
        "target_market": target_market
    }

    execution = engine.execute(initial_state)
    return execution.get_state()
