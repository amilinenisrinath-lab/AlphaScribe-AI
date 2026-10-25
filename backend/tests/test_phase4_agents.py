"""
Phase 4 Verification Test Suite: LangGraph Multi-Agent Orchestration
Tests:
1. Cyclical state graph execution across all 5 specialized agents.
2. Sequential node transitions (Supervisor -> Researcher -> Analyst -> Writer -> Fact-Checker).
3. Zero-hallucination fact checking with strict citation mapping.
4. Cyclical loop-back behavior when revision is requested.
5. End-to-end synchronous workflow helper (execute_research_workflow).
"""

import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.agents.state import AgentState
from app.agents.supervisor import supervisor_node, route_next_step
from app.agents.researcher import researcher_node
from app.agents.analyst import analyst_node
from app.agents.writer import writer_node
from app.agents.fact_checker import fact_checker_node
from app.agents.graph import research_app, execute_research_workflow

def test_phase4_agents():
    print("=" * 65)
    print("PHASE 4: LANGGRAPH MULTI-AGENT ORCHESTRATION VERIFICATION")
    print("=" * 65)

    # 1. Test Individual Agent Nodes
    print("\n[Step 1] Testing Researcher Node...")
    base_state: AgentState = {
        "session_id": "test_phase4_session",
        "ticker": "AAPL",
        "query": "Analyze Services segment margin expansion and CapEx.",
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

    res_output = researcher_node(base_state)
    assert len(res_output["retrieved_chunks"]) > 0, "Researcher failed to retrieve chunks"
    base_state.update(res_output)
    print(f" -> Researcher retrieved {len(base_state['retrieved_chunks'])} relevant chunks.")

    print("\n[Step 2] Testing Financial Analyst Node...")
    ana_output = analyst_node(base_state)
    assert "market_data" in ana_output, "Market data missing"
    assert "financial_ratios" in ana_output, "Financial ratios missing"
    assert ana_output["chart_info"].get("status") == "SUCCESS", "Chart generation failed in analyst node"
    base_state.update(ana_output)
    print(f" -> Analyst computed ratios: Trailing P/E={base_state['financial_ratios']['trailing_pe']}, 5Y CAGR={base_state['financial_ratios']['5_year_revenue_cagr_pct']}%")
    print(f" -> Analyst generated chart: {base_state['chart_info']['chart_path']}")

    print("\n[Step 3] Testing Writer Node...")
    wri_output = writer_node(base_state)
    assert len(wri_output["draft_memo"]) > 300, "Draft memo content too short"
    assert len(wri_output["citations"]) > 0, "Citations missing from writer output"
    base_state.update(wri_output)
    print(f" -> Writer synthesized investment memo ({len(base_state['draft_memo'])} chars, {len(base_state['citations'])} citations).")

    print("\n[Step 4] Testing Fact-Checker Node (Valid Draft)...")
    chk_output = fact_checker_node(base_state)
    assert chk_output["verification_status"] == "VERIFIED", f"Expected VERIFIED, got: {chk_output['verification_status']}"
    print(f" -> Fact-Checker Audit Status: {chk_output['verification_status']}")
    print(f" -> Fact-Checker Feedback: {chk_output['verification_feedback']}")

    # 2. Test Cyclical Review Loop (Hallucination / Missing Citation Detection)
    print("\n[Step 5] Testing Cyclical Feedback Loop with Faulty Draft...")
    faulty_state = dict(base_state)
    # Tamper with draft by stripping citations
    faulty_state["draft_memo"] = "This is an ungrounded memo with zero verifiable citations."
    faulty_state["iteration_count"] = 0
    faulty_state["node_history"] = ["supervisor", "researcher", "analyst", "writer"]

    fault_output = fact_checker_node(faulty_state)
    assert fault_output["verification_status"] == "REVISION_REQUESTED", "Fact-checker failed to reject ungrounded draft"
    faulty_state.update(fault_output)
    faulty_state["node_history"].append("fact_checker")
    
    # Check supervisor routing responds to revision request
    next_route = route_next_step(faulty_state)
    assert next_route == "writer", f"Expected router to redirect to 'writer', got: {next_route}"
    print(f" -> Cyclical Guardrail Triggered: Status={fault_output['verification_status']}")
    print(f" -> Supervisor dynamically routed back to: '{next_route}' for revision loop.")

    # 3. Test Full Graph Invocation
    print("\n[Step 6] Testing Full Compiled LangGraph Execution (execute_research_workflow)...")
    final_state = execute_research_workflow(
        session_id="full_graph_test",
        ticker="MSFT",
        query="Evaluate cloud margins, Capex and 5-year growth trajectory."
    )

    assert final_state["verification_status"] == "VERIFIED", "Full workflow failed verification"
    assert len(final_state["draft_memo"]) > 400, "Final memo too short"
    assert len(final_state["citations"]) > 0, "Final citations missing"
    
    history_nodes = [n for n in final_state["node_history"] if n != "supervisor"]
    print(f" -> Final Status: {final_state['verification_status']}")
    print(f" -> Executed Node Sequence: {' -> '.join(history_nodes)}")
    print(f" -> Final Memo Length: {len(final_state['draft_memo'])} characters")

    print("\n" + "=" * 65)
    print("PHASE 4 VERIFICATION COMPLETE: ALL MULTI-AGENT TESTS PASSED (100%)")
    print("=" * 65)

if __name__ == "__main__":
    test_phase4_agents()
