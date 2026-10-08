import json
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any
from app.core.config import settings

class RFinancialChartTool:
    """Orchestrates R ggplot2 scripts to generate publication-grade financial charts."""

    @staticmethod
    def generate_chart(chart_payload: Dict[str, Any], filename_prefix: str = "chart") -> Dict[str, Any]:
        """
        Executes Rscript to render a ggplot2 financial chart.
        Gracefully falls back to high-res Python plotting if Rscript is not present.
        """
        ticker = chart_payload.get("ticker", "TICKER")
        output_filename = f"{ticker.lower()}_{filename_prefix}.png"
        output_path = settings.OUTPUT_DIR / output_filename
        
        # Temp JSON path for R script input
        temp_json_path = settings.OUTPUT_DIR / f"{ticker.lower()}_{filename_prefix}_payload.json"
        with open(temp_json_path, "w", encoding="utf-8") as f:
            json.dump(chart_payload, f, indent=2)

        r_script_path = settings.RSCRIPTS_DIR / "financial_plots.R"
        rscript_cmd = shutil.which(settings.RSCRIPT_PATH) or shutil.which("Rscript")

        # 1. Attempt Rscript execution
        if rscript_cmd and r_script_path.exists():
            try:
                cmd = [rscript_cmd, str(r_script_path), str(temp_json_path), str(output_path)]
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                return {
                    "engine": "R (ggplot2)",
                    "chart_path": str(output_path),
                    "relative_url": f"/outputs/{output_filename}",
                    "status": "SUCCESS",
                    "stdout": result.stdout.strip()
                }
            except Exception as e:
                pass  # Fall through to Python fallback engine

        # 2. Resilient Python Fallback Engine (Emulating R ggplot2 style)
        try:
            import matplotlib
            matplotlib.use("Agg")  # Non-interactive backend
            import matplotlib.pyplot as plt

            series = chart_payload.get("series", [])
            periods = [str(item["period"]) for item in series]
            values = [float(item["value"]) for item in series]

            fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)
            
            # Styling inspired by ggplot2 theme_minimal
            fig.patch.set_facecolor("#ffffff")
            ax.set_facecolor("#ffffff")
            
            # Line & Area fill
            ax.plot(periods, values, color="#2563eb", linewidth=2.5, marker="o", markersize=6, zorder=3)
            ax.fill_between(periods, values, color="#3b82f6", alpha=0.15, zorder=2)

            # Data labels
            for p, v in zip(periods, values):
                ax.annotate(f"${v:.1f}B", (p, v), textcoords="offset points", xytext=(0, 10),
                            ha="center", fontsize=9, fontweight="bold", color="#1e293b")

            metric_name = chart_payload.get("metric_name", "Financial Metric")
            unit = chart_payload.get("unit", "USD")
            
            ax.set_title(f"{ticker}: {metric_name} Trend", fontsize=14, fontweight="bold", color="#0f172a", pad=15, loc="left")
            ax.set_ylabel(unit, fontsize=10, fontweight="bold", color="#475569")
            ax.set_xlabel("Reporting Period", fontsize=10, fontweight="bold", color="#475569")
            
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.spines["left"].set_visible(False)
            ax.spines["bottom"].set_color("#cbd5e1")
            ax.grid(axis="y", color="#e2e8f0", linestyle="--", linewidth=0.7)
            ax.tick_params(colors="#475569")

            plt.tight_layout()
            plt.savefig(output_path, dpi=300)
            plt.close()

            return {
                "engine": "R-Equivalent (Python Fallback)",
                "chart_path": str(output_path),
                "relative_url": f"/outputs/{output_filename}",
                "status": "SUCCESS"
            }
        except Exception as e:
            return {
                "engine": "NONE",
                "chart_path": "",
                "status": "FAILED",
                "error": str(e)
            }
