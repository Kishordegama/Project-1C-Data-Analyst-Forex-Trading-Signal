"""Master runner for Project 1C Forex Trading Signal Analysis.

This script executes the verified project modules in the correct order:

Step 1: Normalize trade PnL into USD.
Step 2: Calculate trade performance and drawdown.
Step 3: Calculate Monte Carlo portfolio risk.
"""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "Outputs"
REPORT_DIR = BASE_DIR / "Report"

PROJECT_STEPS = [

        (
        "STEP 0: SOURCE DATA VALIDATION AND EDA",
        "step0_source_data_eda.py",
    ),
    (
        "STEP 1: TRADE PNL NORMALIZATION",
        "step1_normalize_trade_pnl.py",
    ),
    (
        "STEP 2: TRADE PERFORMANCE ANALYSIS",
        "step2_trade_performance.py",
    ),
    (
        "STEP 3: MONTE CARLO RISK ANALYSIS",
        "step3_monte_carlo_risk.py",
    ),
]


def run_project_step(
    step_name: str,
    script_name: str,
) -> None:
    """Execute one verified project analysis script."""

    script_path = BASE_DIR / script_name

    if not script_path.exists():
        raise FileNotFoundError(
            f"Required project script not found:\n{script_path}"
        )

    print("\n" + "=" * 78)
    print(step_name)
    print("=" * 78)
    print(f"Running: {script_name}\n")

    subprocess.run(
        [
            sys.executable,
            str(script_path),
        ],
        cwd=BASE_DIR,
        check=True,
    )

    print(f"\nCompleted successfully: {script_name}")


def main() -> None:
    """Run the complete verified Project 1C analysis pipeline."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 78)
    print("PROJECT 1C: FOREX TRADING SIGNAL AND RISK ANALYTICS")
    print("=" * 78)
    print(f"Project directory: {BASE_DIR}")
    print(f"Python executable: {sys.executable}")
    print(f"Total analysis steps: {len(PROJECT_STEPS)}")

    for step_name, script_name in PROJECT_STEPS:
        run_project_step(
            step_name,
            script_name,
        )

    print("\n" + "=" * 78)
    print("PROJECT 1C MASTER PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 78)
    print("All verified CSV outputs, charts, and reports were regenerated.")
    print(f"Outputs folder: {OUTPUT_DIR}")
    print(f"Reports folder: {REPORT_DIR}")


if __name__ == "__main__":
    main()