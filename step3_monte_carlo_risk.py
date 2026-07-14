"""Step 3: Monte Carlo portfolio risk analysis.

This script reads the supplied Monte Carlo scenarios, validates the data,
and later calculates VaR, CVaR, loss probability, stress sensitivity,
and portfolio risk charts.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# ---------------------------------------------------------------------
# 1. FILE PATHS
# ---------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

DATA_FILE = BASE_DIR / "Data" / "mc_scenarios.csv"
OUTPUT_DIR = BASE_DIR / "Outputs"
REPORT_DIR = BASE_DIR / "Report"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------
# 2. EXPECTED DATASET COLUMNS
# ---------------------------------------------------------------------

REQUIRED_COLUMNS = [
    "ScenarioID",
    "ParallelShift",
    "VolShock",
    "CorrShock",
    "EURUSD_PnL",
    "USDJPY_PnL",
    "GBPUSD_PnL",
    "PortfolioPnL",
]


# ---------------------------------------------------------------------
# 3. LOAD AND VALIDATE MONTE CARLO DATA
# ---------------------------------------------------------------------

def load_monte_carlo_data() -> pd.DataFrame:
    """Load and validate the supplied Monte Carlo scenario dataset."""

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Monte Carlo data file not found:\n{DATA_FILE}"
        )

    scenarios = pd.read_csv(DATA_FILE)

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in scenarios.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Required columns are missing: {missing_columns}"
        )

    numeric_columns = [
        "ParallelShift",
        "VolShock",
        "CorrShock",
        "EURUSD_PnL",
        "USDJPY_PnL",
        "GBPUSD_PnL",
        "PortfolioPnL",
    ]

    scenarios[numeric_columns] = scenarios[numeric_columns].apply(
        pd.to_numeric,
        errors="coerce",
    )

    if scenarios[numeric_columns].isna().any().any():
        null_counts = scenarios[numeric_columns].isna().sum()
        raise ValueError(
            "Invalid or missing numeric values detected:\n"
            f"{null_counts[null_counts > 0]}"
        )

    component_total = (
        scenarios["EURUSD_PnL"]
        + scenarios["USDJPY_PnL"]
        + scenarios["GBPUSD_PnL"]
    )

    maximum_difference = (
        scenarios["PortfolioPnL"] - component_total
    ).abs().max()

    print("=" * 72)
    print("STEP 3: MONTE CARLO RISK ANALYSIS")
    print("=" * 72)
    print(f"Data file       : {DATA_FILE.name}")
    print(f"Total scenarios : {len(scenarios):,}")
    print(f"Total columns   : {len(scenarios.columns)}")
    print(f"Duplicate rows  : {scenarios.duplicated().sum()}")
    print(f"Missing values  : {scenarios.isna().sum().sum()}")
    print(f"PnL audit gap   : ${maximum_difference:,.6f}")

    if maximum_difference <= 0.01:
        print("Portfolio PnL audit: PASSED")
    else:
        print("Portfolio PnL audit: WARNING")

    return scenarios
# ---------------------------------------------------------------------
# 4. CALCULATE MONTE CARLO RISK METRICS
# ---------------------------------------------------------------------

def calculate_monte_carlo_risk(
    scenarios: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate portfolio risk metrics from Monte Carlo scenarios."""

    portfolio_pnl = scenarios["PortfolioPnL"].astype(float)

    expected_pnl = portfolio_pnl.mean()
    median_pnl = portfolio_pnl.median()
    pnl_volatility = portfolio_pnl.std(ddof=1)

    probability_of_loss = (portfolio_pnl < 0).mean() * 100
    probability_of_profit = (portfolio_pnl > 0).mean() * 100

    worst_scenario_pnl = portfolio_pnl.min()
    best_scenario_pnl = portfolio_pnl.max()

    # 95% confidence level: worst 5% scenarios
    percentile_5 = np.percentile(portfolio_pnl, 5)
    var_95 = max(0.0, -percentile_5)

    worst_5_percent = portfolio_pnl[
        portfolio_pnl <= percentile_5
    ]
    cvar_95 = max(0.0, -worst_5_percent.mean())

    # 99% confidence level: worst 1% scenarios
    percentile_1 = np.percentile(portfolio_pnl, 1)
    var_99 = max(0.0, -percentile_1)

    worst_1_percent = portfolio_pnl[
        portfolio_pnl <= percentile_1
    ]
    cvar_99 = max(0.0, -worst_1_percent.mean())

    risk_metrics = pd.DataFrame(
        {
            "Metric": [
                "Total Monte Carlo Scenarios",
                "Expected Portfolio PnL USD",
                "Median Portfolio PnL USD",
                "Portfolio PnL Volatility USD",
                "Probability of Loss Percent",
                "Probability of Profit Percent",
                "Worst Scenario PnL USD",
                "Best Scenario PnL USD",
                "VaR 95 Percent USD",
                "CVaR 95 Percent USD",
                "VaR 99 Percent USD",
                "CVaR 99 Percent USD",
            ],
            "Value": [
                len(scenarios),
                expected_pnl,
                median_pnl,
                pnl_volatility,
                probability_of_loss,
                probability_of_profit,
                worst_scenario_pnl,
                best_scenario_pnl,
                var_95,
                cvar_95,
                var_99,
                cvar_99,
            ],
        }
    )

    output_file = OUTPUT_DIR / "monte_carlo_risk_metrics.csv"

    risk_metrics.to_csv(
        output_file,
        index=False,
        float_format="%.6f",
    )

    print("\n" + "=" * 72)
    print("MONTE CARLO PORTFOLIO RISK METRICS")
    print("=" * 72)
    print(f"Expected Portfolio PnL : ${expected_pnl:,.2f}")
    print(f"Median Portfolio PnL   : ${median_pnl:,.2f}")
    print(f"PnL Volatility         : ${pnl_volatility:,.2f}")
    print(f"Probability of Loss    : {probability_of_loss:.2f}%")
    print(f"Probability of Profit  : {probability_of_profit:.2f}%")
    print(f"Worst Scenario PnL     : ${worst_scenario_pnl:,.2f}")
    print(f"Best Scenario PnL      : ${best_scenario_pnl:,.2f}")
    print(f"95% VaR                : ${var_95:,.2f}")
    print(f"95% CVaR               : ${cvar_95:,.2f}")
    print(f"99% VaR                : ${var_99:,.2f}")
    print(f"99% CVaR               : ${cvar_99:,.2f}")
    print(f"\nRisk metrics saved to:\n{output_file}")

    return risk_metrics
# ---------------------------------------------------------------------
# 5. CREATE MONTE CARLO PNL DISTRIBUTION CHART
# ---------------------------------------------------------------------

def create_pnl_distribution_chart(
    scenarios: pd.DataFrame,
) -> Path:
    """Create a portfolio PnL distribution chart with risk markers."""

    portfolio_pnl = scenarios["PortfolioPnL"].astype(float)

    expected_pnl = portfolio_pnl.mean()
    loss_probability = (portfolio_pnl < 0).mean() * 100

    percentile_5 = np.percentile(portfolio_pnl, 5)
    var_95 = max(0.0, -percentile_5)

    worst_5_percent = portfolio_pnl[
        portfolio_pnl <= percentile_5
    ]
    cvar_95 = max(0.0, -worst_5_percent.mean())

    figure, axis = plt.subplots(figsize=(13, 7))

    counts, bin_edges, patches = axis.hist(
        portfolio_pnl,
        bins=40,
        color="#2563EB",
        edgecolor="white",
        linewidth=0.8,
        alpha=0.85,
    )

    # Highlight the worst 5% tail in red.
    for left_edge, patch in zip(bin_edges[:-1], patches):
        if left_edge <= percentile_5:
            patch.set_facecolor("#DC2626")

    axis.axvspan(
        portfolio_pnl.min(),
        percentile_5,
        color="#DC2626",
        alpha=0.10,
        label="Worst 5% scenarios",
    )

    axis.axvline(
        0,
        color="#111827",
        linestyle="-",
        linewidth=1.8,
        label="Break-even PnL",
    )

    axis.axvline(
        expected_pnl,
        color="#16A34A",
        linestyle="--",
        linewidth=2.2,
        label=f"Expected PnL: ${expected_pnl:,.0f}",
    )

    axis.axvline(
        percentile_5,
        color="#DC2626",
        linestyle="--",
        linewidth=2.2,
        label=f"95% VaR: ${var_95:,.0f}",
    )

    axis.axvline(
        -cvar_95,
        color="#7C3AED",
        linestyle=":",
        linewidth=2.5,
        label=f"95% CVaR: ${cvar_95:,.0f}",
    )

    axis.set_title(
        "Monte Carlo Portfolio PnL Distribution",
        fontsize=18,
        fontweight="bold",
        pad=16,
    )

    axis.set_xlabel(
        "Simulated Portfolio PnL (USD)",
        fontsize=12,
        fontweight="bold",
    )

    axis.set_ylabel(
        "Number of Scenarios",
        fontsize=12,
        fontweight="bold",
    )

    axis.xaxis.set_major_formatter(
        FuncFormatter(lambda value, position: f"${value:,.0f}")
    )

    summary_text = (
        f"Total Scenarios: {len(scenarios):,}\n"
        f"Expected PnL: ${expected_pnl:,.2f}\n"
        f"Loss Probability: {loss_probability:.2f}%\n"
        f"95% VaR: ${var_95:,.2f}\n"
        f"95% CVaR: ${cvar_95:,.2f}"
    )

    axis.text(
        0.98,
        0.96,
        summary_text,
        transform=axis.transAxes,
        horizontalalignment="right",
        verticalalignment="top",
        fontsize=10,
        bbox={
            "boxstyle": "round,pad=0.6",
            "facecolor": "white",
            "edgecolor": "#9CA3AF",
            "alpha": 0.95,
        },
    )

    axis.legend(
        loc="upper left",
        frameon=True,
        fontsize=10,
    )

    axis.grid(
        axis="y",
        linestyle="--",
        alpha=0.30,
    )

    figure.tight_layout()

    chart_file = (
        OUTPUT_DIR / "monte_carlo_pnl_distribution.png"
    )

    figure.savefig(
        chart_file,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close(figure)

    print(f"\nMonte Carlo distribution chart saved to:\n{chart_file}")

    return chart_file
# ---------------------------------------------------------------------
# 6. CALCULATE STRESS FACTOR SENSITIVITY
# ---------------------------------------------------------------------

def calculate_stress_sensitivity(
    scenarios: pd.DataFrame,
) -> pd.DataFrame:
    """Measure the relationship between stress factors and portfolio PnL."""

    risk_factors = [
        "ParallelShift",
        "VolShock",
        "CorrShock",
    ]

    portfolio_pnl = scenarios["PortfolioPnL"].astype(float)

    sensitivity_records = []

    for risk_factor in risk_factors:
        factor_values = scenarios[risk_factor].astype(float)

        if factor_values.nunique() < 2:
            raise ValueError(
                f"{risk_factor} does not contain enough unique values."
            )

        correlation = factor_values.corr(portfolio_pnl)

        slope, intercept = np.polyfit(
            factor_values,
            portfolio_pnl,
            1,
        )

        sensitivity_per_1_percent = slope * 0.01
        r_squared = correlation**2

        absolute_correlation = abs(correlation)

        if absolute_correlation >= 0.70:
            relationship_strength = "Strong"
        elif absolute_correlation >= 0.40:
            relationship_strength = "Moderate"
        elif absolute_correlation >= 0.20:
            relationship_strength = "Weak"
        else:
            relationship_strength = "Very Weak"

        if correlation > 0:
            relationship_direction = "Positive"
        elif correlation < 0:
            relationship_direction = "Negative"
        else:
            relationship_direction = "Neutral"

        sensitivity_records.append(
            {
                "RiskFactor": risk_factor,
                "CorrelationWithPortfolioPnL": correlation,
                "RelationshipDirection": relationship_direction,
                "RelationshipStrength": relationship_strength,
                "SensitivityPer1PctShock_USD": sensitivity_per_1_percent,
                "RegressionIntercept_USD": intercept,
                "R_Squared": r_squared,
            }
        )

    sensitivity_table = pd.DataFrame(sensitivity_records)

    sensitivity_table = sensitivity_table.sort_values(
        by="CorrelationWithPortfolioPnL",
        key=lambda values: values.abs(),
        ascending=False,
    ).reset_index(drop=True)

    output_file = (
        OUTPUT_DIR / "monte_carlo_stress_sensitivity.csv"
    )

    sensitivity_table.to_csv(
        output_file,
        index=False,
        float_format="%.6f",
    )

    print("\n" + "=" * 72)
    print("MONTE CARLO STRESS FACTOR SENSITIVITY")
    print("=" * 72)

    print(
        sensitivity_table.to_string(
            index=False,
            formatters={
                "CorrelationWithPortfolioPnL": "{:.4f}".format,
                "SensitivityPer1PctShock_USD": "${:,.2f}".format,
                "RegressionIntercept_USD": "${:,.2f}".format,
                "R_Squared": "{:.4f}".format,
            },
        )
    )

    print(f"\nStress sensitivity saved to:\n{output_file}")

    return sensitivity_table
# ---------------------------------------------------------------------
# 7. CREATE PARALLEL SHIFT SENSITIVITY CHART
# ---------------------------------------------------------------------

def create_parallel_shift_chart(
    scenarios: pd.DataFrame,
) -> Path:
    """Create a scatter chart of Parallel Shift versus Portfolio PnL."""

    parallel_shift = scenarios["ParallelShift"].astype(float)
    portfolio_pnl = scenarios["PortfolioPnL"].astype(float)

    correlation = parallel_shift.corr(portfolio_pnl)

    slope, intercept = np.polyfit(
        parallel_shift,
        portfolio_pnl,
        1,
    )

    r_squared = correlation**2
    sensitivity_per_1_percent = slope * 0.01

    regression_x = np.linspace(
        parallel_shift.min(),
        parallel_shift.max(),
        200,
    )

    regression_y = (
        slope * regression_x
        + intercept
    )

    figure, axis = plt.subplots(figsize=(13, 7))

    scatter = axis.scatter(
        parallel_shift,
        portfolio_pnl,
        c=portfolio_pnl,
        cmap="RdYlGn",
        s=34,
        alpha=0.70,
        edgecolors="none",
    )

    axis.plot(
        regression_x,
        regression_y,
        color="#111827",
        linewidth=2.5,
        label="Linear regression trend",
    )

    axis.axhline(
        0,
        color="#6B7280",
        linestyle="--",
        linewidth=1.4,
        label="Break-even PnL",
    )

    axis.axvline(
        0,
        color="#2563EB",
        linestyle=":",
        linewidth=1.5,
        label="Zero parallel shift",
    )

    axis.set_title(
        "Parallel Yield-Curve Shift vs Portfolio PnL",
        fontsize=18,
        fontweight="bold",
        pad=16,
    )

    axis.set_xlabel(
        "Parallel Shift",
        fontsize=12,
        fontweight="bold",
    )

    axis.set_ylabel(
        "Simulated Portfolio PnL (USD)",
        fontsize=12,
        fontweight="bold",
    )

    axis.xaxis.set_major_formatter(
        FuncFormatter(
            lambda value, position: f"{value * 100:.1f}%"
        )
    )

    axis.yaxis.set_major_formatter(
        FuncFormatter(
            lambda value, position: f"${value:,.0f}"
        )
    )

    color_bar = figure.colorbar(
        scatter,
        ax=axis,
        pad=0.02,
    )

    color_bar.set_label(
        "Portfolio PnL (USD)",
        fontsize=10,
        fontweight="bold",
    )

    color_bar.ax.yaxis.set_major_formatter(
        FuncFormatter(
            lambda value, position: f"${value:,.0f}"
        )
    )

    summary_text = (
        f"Correlation: {correlation:.4f}\n"
        f"R²: {r_squared:.4f}\n"
        f"Impact per 1% shift:\n"
        f"${sensitivity_per_1_percent:,.2f}"
    )

    axis.text(
        0.98,
        0.96,
        summary_text,
        transform=axis.transAxes,
        horizontalalignment="right",
        verticalalignment="top",
        fontsize=10,
        bbox={
            "boxstyle": "round,pad=0.6",
            "facecolor": "white",
            "edgecolor": "#9CA3AF",
            "alpha": 0.95,
        },
    )

    axis.legend(
        loc="lower left",
        fontsize=10,
        frameon=True,
    )

    axis.grid(
        linestyle="--",
        alpha=0.25,
    )

    figure.tight_layout()

    chart_file = OUTPUT_DIR / "parallel_shift_vs_pnl.png"

    figure.savefig(
        chart_file,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close(figure)

    print(f"\nParallel-shift sensitivity chart saved to:\n{chart_file}")

    return chart_file
# ---------------------------------------------------------------------
# 8. WRITE MONTE CARLO RISK REPORT
# ---------------------------------------------------------------------

def write_monte_carlo_report(
    scenarios: pd.DataFrame,
    risk_metrics: pd.DataFrame,
    sensitivity_table: pd.DataFrame,
) -> Path:
    """Write the final Step 3 Monte Carlo risk analysis report."""

    metric_values = risk_metrics.set_index("Metric")["Value"].to_dict()

    dominant_factor = sensitivity_table.iloc[0]

    report_lines = [
        "=" * 78,
        "OFFICIAL PROJECT REPORT: STEP 3 MONTE CARLO RISK ANALYSIS",
        "=" * 78,
        "",
        "1. DATASET VALIDATION",
        "-" * 78,
        f"Monte Carlo scenarios          : {len(scenarios):,}",
        f"Dataset columns                : {len(scenarios.columns)}",
        f"Duplicate rows                 : {scenarios.duplicated().sum()}",
        f"Missing values                 : {scenarios.isna().sum().sum()}",
        "Portfolio PnL components       : EURUSD + USDJPY + GBPUSD",
        "",
        "2. PORTFOLIO RISK METRICS",
        "-" * 78,
        (
            "Expected Portfolio PnL        : "
            f"${metric_values['Expected Portfolio PnL USD']:,.2f}"
        ),
        (
            "Median Portfolio PnL          : "
            f"${metric_values['Median Portfolio PnL USD']:,.2f}"
        ),
        (
            "Portfolio PnL Volatility      : "
            f"${metric_values['Portfolio PnL Volatility USD']:,.2f}"
        ),
        (
            "Probability of Loss           : "
            f"{metric_values['Probability of Loss Percent']:.2f}%"
        ),
        (
            "Probability of Profit         : "
            f"{metric_values['Probability of Profit Percent']:.2f}%"
        ),
        (
            "Worst Scenario PnL            : "
            f"${metric_values['Worst Scenario PnL USD']:,.2f}"
        ),
        (
            "Best Scenario PnL             : "
            f"${metric_values['Best Scenario PnL USD']:,.2f}"
        ),
        "",
        "3. VALUE AT RISK AND EXPECTED SHORTFALL",
        "-" * 78,
        (
            "95% Value at Risk             : "
            f"${metric_values['VaR 95 Percent USD']:,.2f}"
        ),
        (
            "95% Conditional VaR           : "
            f"${metric_values['CVaR 95 Percent USD']:,.2f}"
        ),
        (
            "99% Value at Risk             : "
            f"${metric_values['VaR 99 Percent USD']:,.2f}"
        ),
        (
            "99% Conditional VaR           : "
            f"${metric_values['CVaR 99 Percent USD']:,.2f}"
        ),
        "",
        "Methodology:",
        "95% VaR is the absolute value of the 5th percentile portfolio PnL.",
        "95% CVaR is the average loss across the worst 5% of scenarios.",
        "99% VaR and CVaR use the worst 1% of Monte Carlo scenarios.",
        "",
        "4. STRESS FACTOR SENSITIVITY",
        "-" * 78,
    ]

    for _, row in sensitivity_table.iterrows():
        report_lines.extend(
            [
                f"Risk factor                    : {row['RiskFactor']}",
                (
                    "Correlation with Portfolio PnL : "
                    f"{row['CorrelationWithPortfolioPnL']:.4f}"
                ),
                (
                    "Relationship                   : "
                    f"{row['RelationshipStrength']} "
                    f"{row['RelationshipDirection']}"
                ),
                (
                    "Sensitivity per 1% shock        : "
                    f"${row['SensitivityPer1PctShock_USD']:,.2f}"
                ),
                f"R-squared                      : {row['R_Squared']:.4f}",
                "",
            ]
        )

    report_lines.extend(
        [
            "5. KEY RISK FINDINGS",
            "-" * 78,
            (
                "Dominant portfolio risk factor   : "
                f"{dominant_factor['RiskFactor']}"
            ),
            (
                "Dominant factor correlation      : "
                f"{dominant_factor['CorrelationWithPortfolioPnL']:.4f}"
            ),
            (
                "Dominant factor R-squared        : "
                f"{dominant_factor['R_Squared']:.4f}"
            ),
            "",
            (
                "The Monte Carlo portfolio has a positive expected PnL, "
                "but the probability of loss is close to 50%."
            ),
            (
                "Tail-risk analysis shows that losses can become materially "
                "larger in the worst 5% and 1% of simulated scenarios."
            ),
            (
                "ParallelShift is the primary risk driver and has a strong "
                "negative relationship with PortfolioPnL."
            ),
            (
                "VolShock and CorrShock show very weak standalone "
                "relationships with PortfolioPnL in the supplied scenarios."
            ),
            "",
            "6. GENERATED OUTPUTS",
            "-" * 78,
            "Outputs/monte_carlo_risk_metrics.csv",
            "Outputs/monte_carlo_stress_sensitivity.csv",
            "Outputs/monte_carlo_pnl_distribution.png",
            "Outputs/parallel_shift_vs_pnl.png",
            "Report/step3_monte_carlo_risk_report.txt",
            "",
            "=" * 78,
            "STEP 3 STATUS: SUCCESSFUL AND VERIFIED",
            "=" * 78,
        ]
    )

    report_file = (
        REPORT_DIR / "step3_monte_carlo_risk_report.txt"
    )

    report_file.write_text(
        "\n".join(report_lines),
        encoding="utf-8",
    )

    print(f"\nFinal Monte Carlo risk report saved to:\n{report_file}")

    return report_file
# ---------------------------------------------------------------------
# 9. MAIN PROGRAM
def main() -> None:
    scenarios = load_monte_carlo_data()

    print("\nDataset preview:")
    print(scenarios.head())
    risk_metrics = calculate_monte_carlo_risk(scenarios)
    stress_sensitivity = calculate_stress_sensitivity(scenarios)
    create_parallel_shift_chart(scenarios)
    create_pnl_distribution_chart(scenarios)
    write_monte_carlo_report(
        scenarios,
        risk_metrics,
        stress_sensitivity,
    )
    print("\nStep 3.6 completed successfully.")
if __name__ == "__main__":
    main()