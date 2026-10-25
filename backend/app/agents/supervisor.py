from typing import Dict, Any
from app.agents.state import AgentState

def supervisor_node(state: AgentState) -> Dict[str, Any]:
    """Coordinates agent lifecycle and monitors verification status."""
    history = state.get("node_history", []) + ["supervisor"]
    return {
        "current_node": "supervisor",
        "node_history": history
    }

def route_next_step(state: AgentState) -> str:
    """Routing logic for LangGraph conditional edges."""
    node_history = state.get("node_history", [])
    worker_history = [n for n in node_history if n != "supervisor"]
    last_worker = worker_history[-1] if worker_history else None

    # 1. Sequential pipeline execution
    if "researcher" not in worker_history:
        return "researcher"
    
    if "analyst" not in worker_history:
        return "analyst"

    if "writer" not in worker_history:
        return "writer"

    if "fact_checker" not in worker_history:
        return "fact_checker"

    # 2. Cyclical verification loop
    if state.get("verification_status") == "REVISION_REQUESTED":
        # If fact-checker rejected claims, route back to writer for revisions
        if last_worker == "fact_checker":
            return "writer"
        # If writer just revised draft, route back to fact-checker to re-audit
        elif last_worker == "writer":
            return "fact_checker"

    return "end"
