import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# ==========================================
# LOAD DATASETS
# ==========================================

forex_df = pd.read_csv("Data/forex_price_data.csv")
mc_df = pd.read_csv("Data/mc_scenarios.csv")
trade_df = pd.read_csv("Data/trade_log.csv")

# Convert DateTime column
forex_df["DateTime"] = pd.to_datetime(forex_df["DateTime"])

# ==========================================
# DATA PREVIEW
# ==========================================

print("=" * 50)
print("FOREX DATA")
print("=" * 50)
print(forex_df.head())
print(forex_df.info())

print("\n")

print("=" * 50)
print("MONTE CARLO DATA")
print("=" * 50)
print(mc_df.head())
print(mc_df.info())

print("\n")

print("=" * 50)
print("TRADE LOG DATA")
print("=" * 50)
print(trade_df.head())
print(trade_df.info())

# ==========================================
# SUMMARY STATISTICS
# ==========================================

print("\n")
print("=" * 60)
print("FOREX PRICE SUMMARY")
print("=" * 60)
print(forex_df.describe())

print("\n")
print("=" * 60)
print("MONTE CARLO SUMMARY")
print("=" * 60)
print(mc_df.describe())

print("\n")
print("=" * 60)
print("TRADE LOG SUMMARY")
print("=" * 60)
print(trade_df.describe())

# ==========================================
# MISSING VALUES
# ==========================================

print("\n")
print("=" * 50)
print("MISSING VALUES")
print("=" * 50)

print("\nForex Data")
print(forex_df.isnull().sum())

print("\nMonte Carlo Data")
print(mc_df.isnull().sum())

print("\nTrade Log Data")
print(trade_df.isnull().sum())

# ==========================================
# DUPLICATE RECORDS
# ==========================================

print("\n")
print("=" * 50)
print("DUPLICATE RECORDS")
print("=" * 50)

print("Forex :", forex_df.duplicated().sum())
print("Monte Carlo :", mc_df.duplicated().sum())
print("Trade Log :", trade_df.duplicated().sum())

# ==========================================
# GRAPH 1 : FOREX PRICE TREND
# ==========================================

plt.figure(figsize=(14,6))

for pair in forex_df["PairName"].unique():
    temp = forex_df[forex_df["PairName"] == pair]
    plt.plot(
        temp["DateTime"],
        temp["Close"],
        linewidth=2,
        label=pair
    )

plt.title("Forex Close Price Trend", fontsize=16)
plt.xlabel("Date")
plt.ylabel("Close Price")

plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))

plt.xticks(rotation=45)

plt.grid(True, linestyle="--", alpha=0.5)

plt.legend()

plt.tight_layout()

plt.savefig(
    "Outputs/forex_price_trend.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
# ==========================================
# GRAPH 2 : TRADE PnL DISTRIBUTION
# ==========================================

plt.figure(figsize=(10,6))

plt.hist(
    trade_df["PnL"],
    bins=20,
    edgecolor="black"
)

plt.title("Trade Profit & Loss Distribution", fontsize=16)
plt.xlabel("Profit / Loss")
plt.ylabel("Number of Trades")

plt.grid(True, linestyle="--", alpha=0.5)

plt.tight_layout()

plt.savefig(
    "Outputs/pnl_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
# ==========================================
# GRAPH 3 : CURRENCY PAIR TOTAL PnL
# ==========================================

pair_pnl = trade_df.groupby("PairName")["PnL"].sum()

plt.figure(figsize=(10,6))
pair_pnl.plot(
    kind="bar",
    color="skyblue",
    edgecolor="black"
)

plt.title("Total PnL by Currency Pair", fontsize=16)
plt.xlabel("Currency Pair")
plt.ylabel("Total Profit / Loss")

plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()

plt.savefig(
    "Outputs/pairwise_pnl.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
print(mc_df.columns)
print(mc_df.head)