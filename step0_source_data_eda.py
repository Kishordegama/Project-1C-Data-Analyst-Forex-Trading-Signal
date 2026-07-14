"""Step 0: source-data validation and exploratory analysis.

This script validates the three supplied Project 1C datasets and creates
the Forex close-price trend chart. Trade PnL analysis is intentionally
handled after USD normalization in Steps 1 and 2.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "Data"
OUTPUT_DIR = BASE_DIR / "Outputs"
REPORT_DIR = BASE_DIR / "Report"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)


DATASET_CONFIG = {
    "Forex Price Data": {
        "path": DATA_DIR / "forex_price_data.csv",
        "required_columns": [
            "DateTime",
            "PairName",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
        ],
    },
    "Monte Carlo Data": {
        "path": DATA_DIR / "mc_scenarios.csv",
        "required_columns": [
            "ScenarioID",
            "ParallelShift",
            "VolShock",
            "CorrShock",
            "EURUSD_PnL",
            "USDJPY_PnL",
            "GBPUSD_PnL",
            "PortfolioPnL",
        ],
    },
    "Trade Log Data": {
        "path": DATA_DIR / "trade_log.csv",
        "required_columns": [
            "TradeID",
            "PairName",
            "StrategyName",
            "SignalType",
            "Direction",
            "EntryPrice",
            "ExitPrice",
            "EntryDateTime",
            "ExitDateTime",
            "PositionSize",
            "PnL",
            "PnL_Pips",
            "HoldingDays",
            "Commission",
            "IsOpen",
        ],
    },
}


def load_and_validate_datasets() -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    """Load all source datasets and validate their structures."""

    datasets: dict[str, pd.DataFrame] = {}
    audit_records = []

    for dataset_name, config in DATASET_CONFIG.items():
        file_path = config["path"]
        required_columns = config["required_columns"]

        if not file_path.exists():
            raise FileNotFoundError(
                f"Required dataset was not found:\n{file_path}"
            )

        dataframe = pd.read_csv(file_path)

        missing_columns = [
            column
            for column in required_columns
            if column not in dataframe.columns
        ]

        if missing_columns:
            raise ValueError(
                f"{dataset_name} is missing columns: {missing_columns}"
            )

        datasets[dataset_name] = dataframe

        audit_records.append(
            {
                "Dataset": dataset_name,
                "FileName": file_path.name,
                "Rows": len(dataframe),
                "Columns": len(dataframe.columns),
                "MissingValues": int(dataframe.isna().sum().sum()),
                "DuplicateRows": int(dataframe.duplicated().sum()),
                "ValidationStatus": "PASSED",
            }
        )

    forex_data = datasets["Forex Price Data"].copy()

    forex_data["DateTime"] = pd.to_datetime(
        forex_data["DateTime"],
        errors="coerce",
    )

    numeric_columns = [
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
    ]

    forex_data[numeric_columns] = forex_data[numeric_columns].apply(
        pd.to_numeric,
        errors="coerce",
    )

    if forex_data[["DateTime", *numeric_columns]].isna().any().any():
        raise ValueError(
            "Forex dataset contains invalid date or numeric values."
        )

    forex_data = forex_data.sort_values(
        by=["PairName", "DateTime"],
    ).reset_index(drop=True)

    datasets["Forex Price Data"] = forex_data

    audit_table = pd.DataFrame(audit_records)

    audit_file = OUTPUT_DIR / "source_data_quality_summary.csv"

    audit_table.to_csv(
        audit_file,
        index=False,
    )

    print("=" * 78)
    print("STEP 0: SOURCE DATA VALIDATION AND EDA")
    print("=" * 78)
    print(audit_table.to_string(index=False))
    print(f"\nData-quality summary saved to:\n{audit_file}")

    return datasets, audit_table


def create_forex_price_chart(
    forex_data: pd.DataFrame,
) -> Path:
    """Create the verified Forex closing-price trend chart."""

    figure, axis = plt.subplots(figsize=(14, 7))

    for pair_name, pair_data in forex_data.groupby(
        "PairName",
        sort=True,
    ):
        axis.plot(
            pair_data["DateTime"],
            pair_data["Close"],
            linewidth=2.2,
            label=pair_name,
        )

    date_locator = mdates.AutoDateLocator()

    axis.xaxis.set_major_locator(date_locator)
    axis.xaxis.set_major_formatter(
        mdates.ConciseDateFormatter(date_locator)
    )

    axis.set_title(
        "Forex Close Price Trend",
        fontsize=18,
        fontweight="bold",
        pad=16,
    )

    axis.set_xlabel(
        "Date",
        fontsize=12,
        fontweight="bold",
    )

    axis.set_ylabel(
        "Close Price",
        fontsize=12,
        fontweight="bold",
    )

    axis.grid(
        linestyle="--",
        alpha=0.30,
    )

    axis.legend(
        title="Currency Pair",
        frameon=True,
    )

    figure.tight_layout()

    chart_file = OUTPUT_DIR / "forex_price_trend.png"

    figure.savefig(
        chart_file,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close(figure)

    print(f"\nForex price-trend chart saved to:\n{chart_file}")

    return chart_file


def write_eda_report(
    datasets: dict[str, pd.DataFrame],
    audit_table: pd.DataFrame,
) -> Path:
    """Write the Step 0 source-data validation report."""

    forex_data = datasets["Forex Price Data"]
    monte_carlo_data = datasets["Monte Carlo Data"]
    trade_log_data = datasets["Trade Log Data"]

    currency_pairs = sorted(
        forex_data["PairName"].astype(str).unique()
    )

    report_lines = [
        "=" * 78,
        "OFFICIAL PROJECT REPORT: STEP 0 SOURCE DATA VALIDATION AND EDA",
        "=" * 78,
        "",
        audit_table.to_string(index=False),
        "",
        "FOREX DATA COVERAGE",
        "-" * 78,
        f"Start date       : {forex_data['DateTime'].min()}",
        f"End date         : {forex_data['DateTime'].max()}",
        f"Currency pairs   : {', '.join(currency_pairs)}",
        f"Price rows       : {len(forex_data):,}",
        "",
        "PROJECT DATA VOLUMES",
        "-" * 78,
        f"Monte Carlo scenarios : {len(monte_carlo_data):,}",
        f"Trade-log records      : {len(trade_log_data):,}",
        "",
        "METHODOLOGY NOTE",
        "-" * 78,
        (
            "Raw trade PnL is not aggregated in Step 0 because the supplied "
            "trade log contains multiple quote currencies."
        ),
        (
            "Step 1 converts every trade into comparable USD PnL before "
            "performance analysis is completed in Step 2."
        ),
        "",
        "GENERATED OUTPUTS",
        "-" * 78,
        "Outputs/source_data_quality_summary.csv",
        "Outputs/forex_price_trend.png",
        "Report/step0_source_data_eda_report.txt",
        "",
        "=" * 78,
        "STEP 0 STATUS: SUCCESSFUL AND VERIFIED",
        "=" * 78,
    ]

    report_file = (
        REPORT_DIR / "step0_source_data_eda_report.txt"
    )

    report_file.write_text(
        "\n".join(report_lines),
        encoding="utf-8",
    )

    print(f"\nStep 0 EDA report saved to:\n{report_file}")

    return report_file


def main() -> None:
    datasets, audit_table = load_and_validate_datasets()

    create_forex_price_chart(
        datasets["Forex Price Data"]
    )

    write_eda_report(
        datasets,
        audit_table,
    )

    print("\nStep 0 completed successfully.")


if __name__ == "__main__":
    main()