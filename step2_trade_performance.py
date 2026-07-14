from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# ============================================================
# PATH SETUP
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "Outputs"
REPORT_DIR = BASE_DIR / "Report"

INPUT_FILE = OUTPUT_DIR / "trade_log_normalized.csv"

SUMMARY_FILE = OUTPUT_DIR / "trade_performance_summary.csv"
PAIR_FILE = OUTPUT_DIR / "pair_performance_usd.csv"
STRATEGY_FILE = OUTPUT_DIR / "strategy_performance_usd.csv"
REPORT_FILE = REPORT_DIR / "trade_performance_report.txt"


# ============================================================
# LOAD AND VALIDATE DATA
# ============================================================

def load_trade_data() -> pd.DataFrame:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input file not found: {INPUT_FILE}\n"
            "Please run step1_normalize_trade_pnl.py first."
        )

    trade_df = pd.read_csv(INPUT_FILE)

    required_columns = {
        "TradeID",
        "PairName",
        "StrategyName",
        "NetPnL_USD",
        "GrossPnL_USD",
        "Commission_USD",
        "ExitDateTime",
    }

    missing_columns = required_columns.difference(trade_df.columns)

    if missing_columns:
        raise ValueError(
            f"Required columns are missing: {sorted(missing_columns)}"
        )

    numeric_columns = [
        "NetPnL_USD",
        "GrossPnL_USD",
        "Commission_USD",
    ]

    for column in numeric_columns:
        trade_df[column] = pd.to_numeric(
            trade_df[column],
            errors="coerce",
        )

    trade_df["ExitDateTime"] = pd.to_datetime(
        trade_df["ExitDateTime"],
        errors="coerce",
    )

    if trade_df[numeric_columns].isna().any().any():
        raise ValueError(
            "Invalid numeric values found in normalized PnL columns."
        )

    trade_df = trade_df.sort_values(
        ["ExitDateTime", "TradeID"],
        na_position="last",
    ).reset_index(drop=True)

    return trade_df


# ============================================================
# PERFORMANCE CALCULATIONS
# ============================================================

def calculate_max_drawdown(pnl: pd.Series) -> tuple[float, pd.DataFrame]:
    cumulative_pnl = pnl.cumsum()

    equity_curve = pd.concat(
        [
            pd.Series([0.0]),
            cumulative_pnl.reset_index(drop=True),
        ],
        ignore_index=True,
    )

    running_peak = equity_curve.cummax()
    drawdown = equity_curve - running_peak
    max_drawdown = abs(float(drawdown.min()))

    curve_df = pd.DataFrame(
        {
            "TradeNumber": range(len(equity_curve)),
            "CumulativeNetPnL_USD": equity_curve,
            "RunningPeak_USD": running_peak,
            "Drawdown_USD": drawdown,
        }
    )

    return max_drawdown, curve_df


def calculate_summary(trade_df: pd.DataFrame) -> pd.DataFrame:
    pnl = trade_df["NetPnL_USD"]

    winning_trades = pnl[pnl > 0]
    losing_trades = pnl[pnl < 0]

    total_trades = len(trade_df)
    wins = len(winning_trades)
    losses = len(losing_trades)
    breakeven = int((pnl == 0).sum())

    win_rate = (wins / total_trades * 100) if total_trades else 0.0

    winning_pnl = float(winning_trades.sum())
    losing_pnl = abs(float(losing_trades.sum()))

    profit_factor = (
        winning_pnl / losing_pnl
        if losing_pnl > 0
        else np.inf
    )

    max_drawdown, _ = calculate_max_drawdown(pnl)

    summary = {
        "TotalTrades": total_trades,
        "WinningTrades": wins,
        "LosingTrades": losses,
        "BreakevenTrades": breakeven,
        "WinRate_Pct": win_rate,
        "TotalGrossPnL_USD": trade_df["GrossPnL_USD"].sum(),
        "TotalCommission_USD": trade_df["Commission_USD"].sum(),
        "TotalNetPnL_USD": pnl.sum(),
        "AverageNetPnL_USD": pnl.mean(),
        "MedianNetPnL_USD": pnl.median(),
        "BestTrade_USD": pnl.max(),
        "WorstTrade_USD": pnl.min(),
        "WinningPnL_USD": winning_pnl,
        "LosingPnL_USD": losing_pnl,
        "ProfitFactor": profit_factor,
        "MaxDrawdown_USD": max_drawdown,
    }

    return pd.DataFrame([summary])


def calculate_group_performance(
    trade_df: pd.DataFrame,
    group_column: str,
) -> pd.DataFrame:
    records = []

    for group_name, group_df in trade_df.groupby(group_column):
        pnl = group_df["NetPnL_USD"]

        winning_pnl = pnl[pnl > 0]
        losing_pnl = pnl[pnl < 0]

        total_trades = len(group_df)
        wins = len(winning_pnl)
        losses = len(losing_pnl)

        win_rate = (
            wins / total_trades * 100
            if total_trades
            else 0.0
        )

        positive_total = float(winning_pnl.sum())
        negative_total = abs(float(losing_pnl.sum()))

        profit_factor = (
            positive_total / negative_total
            if negative_total > 0
            else np.inf
        )

        records.append(
            {
                group_column: group_name,
                "TotalTrades": total_trades,
                "WinningTrades": wins,
                "LosingTrades": losses,
                "WinRate_Pct": win_rate,
                "GrossPnL_USD": group_df["GrossPnL_USD"].sum(),
                "Commission_USD": group_df["Commission_USD"].sum(),
                "NetPnL_USD": pnl.sum(),
                "AverageTrade_USD": pnl.mean(),
                "BestTrade_USD": pnl.max(),
                "WorstTrade_USD": pnl.min(),
                "ProfitFactor": profit_factor,
            }
        )

    result_df = pd.DataFrame(records)

    return result_df.sort_values(
        "NetPnL_USD",
        ascending=False,
    ).reset_index(drop=True)


# ============================================================
# CHARTS
# ============================================================

def create_bar_chart(
    performance_df: pd.DataFrame,
    category_column: str,
    title: str,
    output_file: Path,
) -> None:
    chart_df = performance_df.sort_values(
        "NetPnL_USD",
        ascending=True,
    )

    colors = [
        "#2E8B57" if value >= 0 else "#C94C4C"
        for value in chart_df["NetPnL_USD"]
    ]

    plt.figure(figsize=(11, 6))

    bars = plt.barh(
        chart_df[category_column],
        chart_df["NetPnL_USD"],
        color=colors,
        edgecolor="black",
    )

    plt.axvline(0, color="black", linewidth=1)

    plt.title(title, fontsize=15)
    plt.xlabel("Net Profit / Loss (USD)")
    plt.ylabel(category_column)

    plt.grid(
        axis="x",
        linestyle="--",
        alpha=0.4,
    )

    for bar, value in zip(
        bars,
        chart_df["NetPnL_USD"],
    ):
        horizontal_position = (
            value + 15 if value >= 0 else value - 15
        )

        plt.text(
            horizontal_position,
            bar.get_y() + bar.get_height() / 2,
            f"${value:,.2f}",
            va="center",
            ha="left" if value >= 0 else "right",
            fontsize=9,
        )

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close()


def create_equity_drawdown_chart(
    trade_df: pd.DataFrame,
) -> float:
    max_drawdown, curve_df = calculate_max_drawdown(
        trade_df["NetPnL_USD"]
    )

    figure, axes = plt.subplots(
        2,
        1,
        figsize=(13, 8),
        sharex=True,
        gridspec_kw={"height_ratios": [2, 1]},
    )

    axes[0].plot(
        curve_df["TradeNumber"],
        curve_df["CumulativeNetPnL_USD"],
        color="#1F77B4",
        linewidth=2,
        label="Cumulative Net PnL",
    )

    axes[0].plot(
        curve_df["TradeNumber"],
        curve_df["RunningPeak_USD"],
        color="#2E8B57",
        linestyle="--",
        label="Running Peak",
    )

    axes[0].axhline(0, color="black", linewidth=1)
    axes[0].set_title("Trade Equity Curve (USD)", fontsize=15)
    axes[0].set_ylabel("Cumulative Net PnL (USD)")
    axes[0].legend()
    axes[0].grid(True, linestyle="--", alpha=0.4)

    axes[1].fill_between(
        curve_df["TradeNumber"],
        curve_df["Drawdown_USD"],
        0,
        color="#C94C4C",
        alpha=0.7,
    )

    axes[1].set_title(
        f"Drawdown | Maximum Drawdown: ${max_drawdown:,.2f}"
    )
    axes[1].set_xlabel("Trade Number")
    axes[1].set_ylabel("Drawdown (USD)")
    axes[1].grid(True, linestyle="--", alpha=0.4)

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "equity_curve_drawdown.png",
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    curve_df.to_csv(
        OUTPUT_DIR / "equity_curve_data.csv",
        index=False,
    )

    return max_drawdown


def create_pnl_distribution(trade_df: pd.DataFrame) -> None:
    plt.figure(figsize=(10, 6))

    plt.hist(
        trade_df["NetPnL_USD"],
        bins=20,
        color="#4682B4",
        edgecolor="black",
        alpha=0.85,
    )

    plt.axvline(
        trade_df["NetPnL_USD"].mean(),
        color="red",
        linestyle="--",
        linewidth=2,
        label=(
            "Average: "
            f"${trade_df['NetPnL_USD'].mean():,.2f}"
        ),
    )

    plt.axvline(0, color="black", linewidth=1)

    plt.title("Trade Net PnL Distribution (USD)", fontsize=15)
    plt.xlabel("Net Profit / Loss (USD)")
    plt.ylabel("Number of Trades")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.4)

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "trade_net_pnl_distribution_usd.png",
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()


# ============================================================
# TEXT REPORT
# ============================================================

def save_report(
    summary_df: pd.DataFrame,
    pair_df: pd.DataFrame,
    strategy_df: pd.DataFrame,
) -> None:
    summary = summary_df.iloc[0]

    profit_factor = summary["ProfitFactor"]

    profit_factor_text = (
        "Infinite"
        if np.isinf(profit_factor)
        else f"{profit_factor:.2f}"
    )

    with open(
        REPORT_FILE,
        "w",
        encoding="utf-8",
    ) as report:
        report.write(
            "PROJECT 1C - TRADE PERFORMANCE REPORT\n"
        )
        report.write("=" * 72 + "\n\n")

        report.write("OVERALL PERFORMANCE\n")
        report.write("-" * 72 + "\n")
        report.write(
            f"Total Trades          : {int(summary['TotalTrades'])}\n"
        )
        report.write(
            f"Winning Trades        : {int(summary['WinningTrades'])}\n"
        )
        report.write(
            f"Losing Trades         : {int(summary['LosingTrades'])}\n"
        )
        report.write(
            f"Win Rate              : {summary['WinRate_Pct']:.2f}%\n"
        )
        report.write(
            f"Gross PnL             : ${summary['TotalGrossPnL_USD']:,.2f}\n"
        )
        report.write(
            f"Commission            : ${summary['TotalCommission_USD']:,.2f}\n"
        )
        report.write(
            f"Net PnL               : ${summary['TotalNetPnL_USD']:,.2f}\n"
        )
        report.write(
            f"Average Trade         : ${summary['AverageNetPnL_USD']:,.2f}\n"
        )
        report.write(
            f"Best Trade            : ${summary['BestTrade_USD']:,.2f}\n"
        )
        report.write(
            f"Worst Trade           : ${summary['WorstTrade_USD']:,.2f}\n"
        )
        report.write(
            f"Profit Factor         : {profit_factor_text}\n"
        )
        report.write(
            f"Maximum Drawdown      : ${summary['MaxDrawdown_USD']:,.2f}\n\n"
        )

        report.write("PAIR PERFORMANCE\n")
        report.write("-" * 72 + "\n")
        report.write(
            pair_df.to_string(
                index=False,
                float_format=lambda value: f"{value:,.2f}",
            )
        )

        report.write("\n\nSTRATEGY PERFORMANCE\n")
        report.write("-" * 72 + "\n")
        report.write(
            strategy_df.to_string(
                index=False,
                float_format=lambda value: f"{value:,.2f}",
            )
        )

        report.write("\n\nNOTES\n")
        report.write("-" * 72 + "\n")
        report.write(
            "All performance values use the normalized USD PnL generated "
            "by Step 1.\n"
        )
        report.write(
            "Commission is deducted from GrossPnL_USD to calculate "
            "NetPnL_USD.\n"
        )


# ============================================================
# MAIN EXECUTION
# ============================================================

def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    trade_df = load_trade_data()

    summary_df = calculate_summary(trade_df)

    pair_df = calculate_group_performance(
        trade_df,
        "PairName",
    )

    strategy_df = calculate_group_performance(
        trade_df,
        "StrategyName",
    )

    summary_df.to_csv(SUMMARY_FILE, index=False)
    pair_df.to_csv(PAIR_FILE, index=False)
    strategy_df.to_csv(STRATEGY_FILE, index=False)

    create_bar_chart(
        pair_df,
        "PairName",
        "Net PnL by Currency Pair (USD)",
        OUTPUT_DIR / "pair_net_pnl_usd.png",
    )

    create_bar_chart(
        strategy_df,
        "StrategyName",
        "Net PnL by Trading Strategy (USD)",
        OUTPUT_DIR / "strategy_net_pnl_usd.png",
    )

    create_equity_drawdown_chart(trade_df)
    create_pnl_distribution(trade_df)

    save_report(
        summary_df,
        pair_df,
        strategy_df,
    )

    print("\n" + "=" * 72)
    print("STEP 2 - TRADE PERFORMANCE ANALYSIS COMPLETED")
    print("=" * 72)

    print(
        summary_df.to_string(
            index=False,
            float_format=lambda value: f"{value:,.2f}",
        )
    )

    print("\nFiles created:")

    created_files = [
        SUMMARY_FILE,
        PAIR_FILE,
        STRATEGY_FILE,
        OUTPUT_DIR / "pair_net_pnl_usd.png",
        OUTPUT_DIR / "strategy_net_pnl_usd.png",
        OUTPUT_DIR / "equity_curve_drawdown.png",
        OUTPUT_DIR / "trade_net_pnl_distribution_usd.png",
        OUTPUT_DIR / "equity_curve_data.csv",
        REPORT_FILE,
    ]

    for file_path in created_files:
        print(f"- {file_path}")


if __name__ == "__main__":
    main()