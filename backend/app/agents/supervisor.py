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
    
    # 1. First step: Research 10-K disclosures
    if "researcher" not in node_history:
        return "researcher"
    
    # 2. Second step: Quantitative market analysis & R chart
    if "analyst" not in node_history:
        return "analyst"

    # 3. Third step: Synthesize investment memo
    if "writer" not in node_history:
        return "writer"

    # 4. Fourth step: Fact check
    if "fact_checker" not in node_history:
        return "fact_checker"

    # 5. Review feedback loop
    if state.get("verification_status") == "REVISION_REQUESTED":
        return "writer"

    return "end"
