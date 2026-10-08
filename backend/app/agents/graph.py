from typing import Dict, Any
from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.supervisor import supervisor_node, route_next_step
from app.agents.researcher import researcher_node
from app.agents.analyst import analyst_node
from app.agents.writer import writer_node
from app.agents.fact_checker import fact_checker_node

def build_financial_research_graph():
    """Builds and compiles the LangGraph multi-agent cyclical state machine."""
    workflow = StateGraph(AgentState)

    # 1. Register agent nodes
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("analyst", analyst_node)
    workflow.add_node("writer", writer_node)
    workflow.add_node("fact_checker", fact_checker_node)

    # 2. Set entry point
    workflow.set_entry_point("supervisor")

    # 3. Define transitions & cyclical feedback loops
    workflow.add_conditional_edges(
        "supervisor",
        route_next_step,
        {
            "researcher": "researcher",
            "analyst": "analyst",
            "writer": "writer",
            "fact_checker": "fact_checker",
            "end": END
        }
    )

    # Workers report back to supervisor to evaluate next routing step
    workflow.add_edge("researcher", "supervisor")
    workflow.add_edge("analyst", "supervisor")
    workflow.add_edge("writer", "supervisor")
    workflow.add_edge("fact_checker", "supervisor")

    return workflow.compile()

# Pre-compiled multi-agent application graph
research_app = build_financial_research_graph()

def execute_research_workflow(session_id: str, ticker: str, query: str) -> AgentState:
    """Synchronous execution helper for running the full agent graph."""
    initial_state: AgentState = {
        "session_id": session_id,
        "ticker": ticker.upper(),
        "query": query,
        "retrieved_chunks": [],
        "market_data": {},
        "financial_ratios": {},
        "chart_info": {},
        "draft_memo": "",
        "citations": [],
        "verification_status": "PENDING",
        "verification_feedback": None,
        "iteration_count": 0,
        "current_node": "supervisor",
        "node_history": []
    }

    final_state = research_app.invoke(initial_state)
    return final_state
