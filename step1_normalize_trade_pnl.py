"""Step 1: normalize trade PnL into one comparable currency (USD).

Run this file from anywhere. It reads Data/trade_log.csv relative to the
script location and creates Outputs/trade_log_normalized.csv.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "Data" / "trade_log.csv"
OUTPUT_DIR = BASE_DIR / "Outputs"
OUTPUT_FILE = OUTPUT_DIR / "trade_log_normalized.csv"

SUPPORTED_PAIRS = {"EUR/USD", "GBP/USD", "AUD/USD", "USD/JPY", "USD/INR"}


def _validate_trade_log(trades: pd.DataFrame) -> None:
    required_columns = {
        "TradeID",
        "PairName",
        "Direction",
        "EntryPrice",
        "ExitPrice",
        "EntryDateTime",
        "ExitDateTime",
        "PositionSize",
        "PnL",
        "PnL_Pips",
        "Commission",
    }
    missing = sorted(required_columns.difference(trades.columns))
    if missing:
        raise ValueError(f"trade_log.csv is missing columns: {missing}")

    unsupported = sorted(set(trades["PairName"]) - SUPPORTED_PAIRS)
    if unsupported:
        raise ValueError(f"Unsupported currency pairs: {unsupported}")

    invalid_directions = sorted(set(trades["Direction"]) - {"LONG", "SHORT"})
    if invalid_directions:
        raise ValueError(f"Direction must be LONG or SHORT: {invalid_directions}")


def normalize_trade_pnl(trades: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with corrected pips and gross/net PnL in USD.

    Dataset assumption: Commission is already denominated in USD.
    """
    result = trades.copy()
    result.columns = result.columns.str.strip()
    result["PairName"] = result["PairName"].astype(str).str.strip().str.upper()
    result["Direction"] = result["Direction"].astype(str).str.strip().str.upper()

    _validate_trade_log(result)

    numeric_columns = [
        "EntryPrice",
        "ExitPrice",
        "PositionSize",
        "PnL",
        "PnL_Pips",
        "Commission",
    ]
    for column in numeric_columns:
        result[column] = pd.to_numeric(result[column], errors="raise")

    result["EntryDateTime"] = pd.to_datetime(result["EntryDateTime"], errors="raise")
    result["ExitDateTime"] = pd.to_datetime(result["ExitDateTime"], errors="raise")

    if (result["EntryPrice"] <= 0).any() or (result["ExitPrice"] <= 0).any():
        raise ValueError("EntryPrice and ExitPrice must be greater than zero.")
    if (result["PositionSize"] <= 0).any():
        raise ValueError("PositionSize must be greater than zero.")

    long_move = result["ExitPrice"] - result["EntryPrice"]
    short_move = result["EntryPrice"] - result["ExitPrice"]
    signed_move = np.where(result["Direction"].eq("LONG"), long_move, short_move)

    result["OriginalPnL"] = result["PnL"]
    result["OriginalPnL_Pips"] = result["PnL_Pips"]
    result["SignedPriceMove"] = signed_move

    # JPY pairs conventionally use 0.01 as one pip; the other supplied pairs
    # use 0.0001 in this project dataset.
    result["PipSize"] = np.where(result["PairName"].eq("USD/JPY"), 0.01, 0.0001)
    result["CorrectedPnL_Pips"] = result["SignedPriceMove"] / result["PipSize"]

    result["GrossPnL_QuoteCurrency"] = (
        result["SignedPriceMove"] * result["PositionSize"]
    )

    # XXX/USD is already USD. USD/XXX is converted back to USD at ExitPrice.
    result["QuoteToUSD_Divisor"] = np.where(
        result["PairName"].str.endswith("/USD"), 1.0, result["ExitPrice"]
    )
    result["GrossPnL_USD"] = (
        result["GrossPnL_QuoteCurrency"] / result["QuoteToUSD_Divisor"]
    )
    result["Commission_USD"] = result["Commission"]
    result["NetPnL_USD"] = result["GrossPnL_USD"] - result["Commission_USD"]
    result["PnL_Unit"] = "USD"

    return result


def print_audit(normalized: pd.DataFrame) -> None:
    pair_summary = (
        normalized.groupby("PairName", as_index=False)
        .agg(
            Trades=("TradeID", "count"),
            GrossPnL_USD=("GrossPnL_USD", "sum"),
            Commission_USD=("Commission_USD", "sum"),
            NetPnL_USD=("NetPnL_USD", "sum"),
        )
        .sort_values("NetPnL_USD", ascending=False)
    )

    print("\n" + "=" * 72)
    print("STEP 1 — TRADE PnL NORMALIZATION AUDIT")
    print("=" * 72)
    print(f"Rows processed       : {len(normalized):,}")
    print(f"Duplicate TradeIDs   : {normalized['TradeID'].duplicated().sum():,}")
    print(f"Original PnL total   : {normalized['OriginalPnL'].sum():,.2f} (mixed units)")
    print(f"Gross PnL (USD)      : {normalized['GrossPnL_USD'].sum():,.2f}")
    print(f"Commission (USD)     : {normalized['Commission_USD'].sum():,.2f}")
    print(f"Net PnL (USD)        : {normalized['NetPnL_USD'].sum():,.2f}")
    print("\nPair-level USD summary:")
    print(pair_summary.to_string(index=False, float_format=lambda value: f"{value:,.2f}"))
    print("\nAssumption: the Commission column is already in USD.")
    print(f"Saved: {OUTPUT_FILE}")


def main() -> None:
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Input file not found: {DATA_FILE}\n"
            "Place this script in the Project 1C root folder beside Data and Outputs."
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    trade_log = pd.read_csv(DATA_FILE)
    normalized = normalize_trade_pnl(trade_log)
    normalized.to_csv(OUTPUT_FILE, index=False, date_format="%Y-%m-%d %H:%M:%S")
    print_audit(normalized)


if __name__ == "__main__":
    main()
