from typing import TypedDict, List, Dict, Any, Optional

class AgentState(TypedDict):
    """Shared state dictionary tracked across all LangGraph nodes."""
    session_id: str
    ticker: str
    query: str
    retrieved_chunks: List[Dict[str, Any]]
    market_data: Dict[str, Any]
    financial_ratios: Dict[str, Any]
    chart_info: Dict[str, Any]
    draft_memo: str
    citations: List[Dict[str, Any]]
    verification_status: str  # "PENDING", "VERIFIED", "REVISION_REQUESTED"
    verification_feedback: Optional[str]
    iteration_count: int
    current_node: str
    node_history: List[str]
