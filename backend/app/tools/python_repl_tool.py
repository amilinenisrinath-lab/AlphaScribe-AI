import math
from typing import Dict, Any

class PythonREPLTool:
    """Sandboxed deterministic code runner for financial arithmetic and ratios."""

    @staticmethod
    def calculate_cagr(start_val: float, end_val: float, periods: int) -> float:
        """Calculates Compound Annual Growth Rate (CAGR)."""
        if start_val <= 0 or periods <= 0:
            return 0.0
        return round(((end_val / start_val) ** (1.0 / periods) - 1.0) * 100.0, 2)

    @staticmethod
    def calculate_ratios(data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculates standard financial and solvency ratios."""
        ratios = {}
        
        # Net Margin
        rev = data.get("revenue")
        net_inc = data.get("net_income")
        if rev and net_inc and rev > 0:
            ratios["net_profit_margin_pct"] = round((net_inc / rev) * 100.0, 2)

        # Free Cash Flow Margin
        fcf = data.get("free_cash_flow")
        if rev and fcf and rev > 0:
            ratios["fcf_margin_pct"] = round((fcf / rev) * 100.0, 2)

        # Debt to Equity
        debt = data.get("total_debt")
        equity = data.get("shareholder_equity")
        if debt is not None and equity and equity > 0:
            ratios["debt_to_equity"] = round(debt / equity, 2)

        return ratios

    @staticmethod
    def execute_code(code_str: str) -> str:
        """Executes safe math expression string in restricted scope."""
        allowed_globals = {
            "math": math,
            "min": min,
            "max": max,
            "sum": sum,
            "round": round,
            "abs": abs
        }
        try:
            # Evaluate expression safely
            result = eval(code_str, {"__builtins__": {}}, allowed_globals)
            return str(result)
        except Exception as e:
            return f"Execution error: {str(e)}"
