"""
Phase 3 Verification Test Suite: Financial Tools & R Visualization Engine
Tests:
1. Live / Fallback market data and multiples retrieval via yfinance.
2. Historical revenue & financial series extraction.
3. Deterministic arithmetic & CAGR calculation via PythonREPLTool (Zero LLM hallucination).
4. Solvency & profitability ratio calculations.
5. High-resolution financial charting engine (R script or high-res Python fallback).
"""

import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.tools.yfinance_tool import FinancialMarketTool
from app.tools.python_repl_tool import PythonREPLTool
from app.tools.r_chart_tool import RFinancialChartTool

def test_phase3_tools():
    print("=" * 65)
    print("PHASE 3: FINANCIAL TOOLS & R VISUALIZATION ENGINE VERIFICATION")
    print("=" * 65)

    # 1. Test FinancialMarketTool - Company Overview
    print("\n[Step 1] Testing FinancialMarketTool.get_company_overview('AAPL')...")
    overview = FinancialMarketTool.get_company_overview("AAPL")
    assert overview["ticker"] == "AAPL", "Ticker mismatch"
    assert "company_name" in overview, "Company name missing"
    assert "current_price" in overview or "error" in overview, "Price field missing"
    print(f" -> Ticker: {overview['ticker']}")
    print(f" -> Company Name: {overview.get('company_name')}")
    print(f" -> Trailing P/E: {overview.get('trailing_pe')}")
    print(f" -> Market Cap: {overview.get('market_cap')}")

    # 2. Test FinancialMarketTool - Historical Financials
    print("\n[Step 2] Testing FinancialMarketTool.get_financial_history('AAPL', periods=5)...")
    history = FinancialMarketTool.get_financial_history("AAPL", periods=5)
    assert history["ticker"] == "AAPL"
    assert "series" in history
    assert len(history["series"]) >= 3, "Historical periods series too short"
    print(f" -> Metric: {history['metric_name']} ({history['unit']})")
    print(f" -> Historical Periods ({len(history['series'])}):")
    for pt in history["series"]:
        print(f"    - Period {pt['period']}: ${pt['value']}B")

    # 3. Test PythonREPLTool - CAGR Calculation
    print("\n[Step 3] Testing PythonREPLTool.calculate_cagr()...")
    start_rev = history["series"][0]["value"]
    end_rev = history["series"][-1]["value"]
    periods = len(history["series"]) - 1
    cagr = PythonREPLTool.calculate_cagr(start_rev, end_rev, periods)
    assert isinstance(cagr, float), "CAGR must be a float"
    print(f" -> Computed 5-Year Revenue CAGR: {cagr}% (from ${start_rev}B to ${end_rev}B over {periods} periods)")

    # 4. Test PythonREPLTool - Solvency & Margin Ratios
    print("\n[Step 4] Testing PythonREPLTool.calculate_ratios()...")
    sample_financials = {
        "revenue": 391.0,
        "net_income": 101.2,
        "free_cash_flow": 108.8,
        "total_debt": 106.6,
        "shareholder_equity": 66.8
    }
    ratios = PythonREPLTool.calculate_ratios(sample_financials)
    assert ratios["net_profit_margin_pct"] == 25.88, f"Unexpected net margin: {ratios['net_profit_margin_pct']}"
    assert ratios["fcf_margin_pct"] == 27.83, f"Unexpected FCF margin: {ratios['fcf_margin_pct']}"
    assert ratios["debt_to_equity"] == 1.6, f"Unexpected debt-to-equity: {ratios['debt_to_equity']}"
    print(f" -> Net Profit Margin: {ratios['net_profit_margin_pct']}%")
    print(f" -> Free Cash Flow Margin: {ratios['fcf_margin_pct']}%")
    print(f" -> Debt-to-Equity Ratio: {ratios['debt_to_equity']}x")

    # 5. Test PythonREPLTool - Safe Code Execution
    print("\n[Step 5] Testing PythonREPLTool.execute_code()...")
    code_expr = "round((391.0 - 274.5) / 274.5 * 100, 2)"
    exec_result = PythonREPLTool.execute_code(code_expr)
    assert exec_result == "42.44", f"Unexpected execution result: {exec_result}"
    print(f" -> Executed '{code_expr}' -> Result: {exec_result}%")

    # 6. Test R / Python Financial Charting Engine
    print("\n[Step 6] Testing RFinancialChartTool.generate_chart()...")
    chart_payload = {
        "ticker": "NVDA",
        "metric_name": "Data Center Revenue",
        "unit": "USD (in Billions)",
        "series": [
            {"period": "FY21", "value": 6.7},
            {"period": "FY22", "value": 10.6},
            {"period": "FY23", "value": 15.0},
            {"period": "FY24", "value": 47.5},
            {"period": "FY25", "value": 110.4}
        ]
    }
    chart_result = RFinancialChartTool.generate_chart(chart_payload, filename_prefix="datacenter_trend")
    assert chart_result["status"] == "SUCCESS", f"Chart generation failed: {chart_result}"
    assert Path(chart_result["chart_path"]).exists(), "Chart file not created on disk"
    
    chart_size = Path(chart_result["chart_path"]).stat().st_size
    assert chart_size > 5000, f"Chart image too small ({chart_size} bytes)"
    print(f" -> Chart Engine Used: {chart_result['engine']}")
    print(f" -> Output Path: {chart_result['chart_path']} (Size: {chart_size:,} bytes)")
    print(f" -> Relative URL: {chart_result['relative_url']}")

    print("\n" + "=" * 65)
    print("PHASE 3 VERIFICATION COMPLETE: ALL TOOLS & CHARTING TESTS PASSED (100%)")
    print("=" * 65)

if __name__ == "__main__":
    test_phase3_tools()
