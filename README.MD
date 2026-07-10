# 📈 Forex Market Risk Analysis Dashboard

![Forex Market Dashboard](page%201forex.jpeg)

## 📌 Project Overview

This project is an end-to-end Financial Data Analytics solution developed using **Python** and **Microsoft Power BI**.

The project analyzes historical Forex market data, evaluates trading performance, performs portfolio risk analysis using Monte Carlo Simulation, and presents actionable insights through an interactive Power BI dashboard.

The objective is to transform raw financial datasets into meaningful business intelligence that supports better trading and investment decisions.

---

# 🎯 Project Objectives

- Analyze historical Forex market prices.
- Evaluate trading Profit & Loss (PnL).
- Perform Monte Carlo Portfolio Risk Simulation.
- Analyze trading sessions across global markets.
- Compare trading strategy performance.
- Build an interactive Business Intelligence dashboard using Power BI.
- Generate insights through Python-based Exploratory Data Analysis (EDA).

---

# 🛠 Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Data Analysis |
| Pandas | Data Cleaning |
| NumPy | Numerical Computing |
| Matplotlib | Data Visualization |
| Microsoft Power BI | Dashboard Development |
| DAX | KPI Calculations |
| CSV | Data Storage |

---

# 📂 Dataset Information

The project consists of four datasets.

## 1️⃣ Forex Price Data

Historical Forex market prices.

### Columns

- DateTime
- PairName
- Open
- High
- Low
- Close
- Volume

---

## 2️⃣ Monte Carlo Simulation Data

Portfolio risk simulation dataset.

### Columns

- ScenarioID
- PortfolioPnL
- VolShock
- CorrShock
- EURUSD_PnL
- GBPUSD_PnL
- USDJPY_PnL

---

## 3️⃣ Trade Log

Trading history dataset.

### Columns

- TradeID
- PairName
- EntryPrice
- ExitPrice
- EntryDateTime
- ExitDateTime
- HoldingDays
- PnL
- SignalType
- StrategyName

---

## 4️⃣ Time Dimension

Custom Time Dimension table used for Trading Session Analysis.

### Columns

- Hour
- Session
- IsOverlap
- TimeKey

---

# 🐍 Python Analysis

Python was used for:

- Data Cleaning
- Missing Value Detection
- Duplicate Detection
- Exploratory Data Analysis (EDA)
- Summary Statistics
- Financial Visualization

Generated outputs include:

- Forex Price Trend
- Profit & Loss Distribution
- Currency Pair Analysis

---

# 📷 Python Analysis Outputs

## 📈 Forex Price Trend

![Forex Price Trend](forex%20close%20tren.jpeg)

---

## 📉 Trade PnL Distribution

![Trade PnL Distribution](loss%20distribution.jpeg)

---

## 💱 Currency Pair Analysis

![Currency Pair Analysis](currency%20pair.jpeg)

---

# 🧩 Data Model

The Power BI report is built using four connected tables.

- forex_price_data
- mc_scenarios
- trade_log
- DimTime

The **DimTime** table is related to the Trade Log to perform Trading Session Analysis and Time Intelligence calculations.

## Data Model

![Data Model](data%20model%20page%205.jpeg)

---
# 📊 Power BI Dashboard

The Power BI report contains **4 interactive dashboard pages**, each designed to provide actionable insights into Forex trading performance, portfolio risk, and market behavior.

---

# 📈 Dashboard Page 1 – Forex Market Analysis

This page provides a comprehensive overview of the Forex market using interactive KPIs and visualizations.

### Key Features

- Current Price KPI
- Highest Price KPI
- Lowest Price KPI
- Average Price KPI
- Forex Price Trend
- Profit & Loss by Currency Pair
- Buy/Sell Signal Distribution
- Currency Pair Filter
- Date Filter

### Dashboard Preview

![Forex Market Dashboard](page%201forex.jpeg)

---

# 📉 Dashboard Page 2 – Monte Carlo Risk Analysis

This dashboard evaluates portfolio performance using Monte Carlo Simulation and visualizes investment risk.

### Key Features

- Average Portfolio PnL
- Maximum Portfolio PnL
- Minimum Portfolio PnL
- Monte Carlo Portfolio Simulation
- Risk vs Return Scatter Plot
- Scenario Filter
- Interactive Tooltips

### Dashboard Preview

![Monte Carlo Dashboard](page%202%20monte%20carlo.jpeg)

---

# 🌍 Dashboard Page 3 – Trading Session Analysis

This page analyzes trading performance across major Forex trading sessions.

### Sessions Covered

- London
- New York
- Tokyo
- Sydney

### Key Features

- Trading Session Heatmap
- Session-wise Profit & Loss
- Trading Volume Analysis
- Session Overlap KPI
- Hourly Performance Analysis
- Interactive Filters

### Dashboard Preview

![Trading Session Dashboard](page%203%20treding.jpeg)

---

# 📊 Dashboard Page 4 – Strategy Performance Analysis

This dashboard compares the performance of multiple trading strategies.

### Strategies Included

- ML_RF
- ML_XGB
- MACD Trend
- RSI Reversal
- Moving Average Cross
- RL PPO
- Composite Strategy

### Key Features

- Strategy-wise Profit & Loss
- Strategy Performance Comparison
- Signal Distribution
- Win Rate Analysis
- Strategy Filters
- Interactive Dashboard

### Dashboard Preview

![Strategy Dashboard](page%204%20strategy.jpeg)

---

# 📈 Key Insights

The dashboard provides several valuable business insights.

### Forex Market Insights

- Historical Forex prices were analyzed across multiple currency pairs.
- Market trends can be monitored using interactive visualizations.
- Currency-wise Profit & Loss comparison helps identify stronger-performing assets.

### Portfolio Risk Analysis

- Monte Carlo Simulation evaluates portfolio uncertainty.
- Risk and return relationships are visualized using scatter plots.
- Portfolio performance can be analyzed under multiple simulated scenarios.

### Trading Session Analysis

- Trading activity is compared across London, New York, Tokyo, and Sydney sessions.
- Session overlap analysis highlights high-volume trading periods.
- Hourly trading performance supports better decision-making.

### Strategy Performance

- Multiple trading strategies are evaluated side by side.
- Profitability differences between strategies are clearly visualized.
- Interactive filters help analyze strategy-specific performance.

---

# 📌 Project Highlights

✔ Interactive Power BI Dashboard

✔ Python-Based Data Analysis

✔ Financial Risk Analytics

✔ Monte Carlo Simulation

✔ Trading Session Intelligence

✔ Strategy Performance Evaluation

✔ Business Intelligence Reporting

---
# 📁 Project Structure

```text
Project-1C-Data-Analyst-Forex-Trading-Signal/
│
├── forex_price_data.csv
├── mc_scenarios.csv
├── trade_log.csv
├── page 1forex.jpeg
├── page 2 monte carlo.jpeg
├── page 3 treding.jpeg
├── page 4 strategy.jpeg
├── data model page 5.jpeg
├── forex close tren.jpeg
├── loss distribution.jpeg
├── currency pair.jpeg
├── analysis.py
├── Project_1C_Dashboard.pbix
├── README.md
├── requirements.txt
└── LICENSE
```

---

# ⚙ Installation

Clone the repository.

```bash
git clone https://github.com/Kishordegama/Project-1C-Data-Analyst-Forex-Trading-Signal.git
```

Move into the project directory.

```bash
cd Project-1C-Data-Analyst-Forex-Trading-Signal
```

Install all required libraries.

```bash
pip install -r requirements.txt
```

Run the Python analysis.

```bash
python analysis.py
```

Open the Power BI dashboard.

```
Project_1C_Dashboard.pbix
```

---

# 📦 Python Libraries

The project uses the following Python libraries.

- pandas
- numpy
- matplotlib

Install them using:

```bash
pip install -r requirements.txt
```

---

# 🚀 Future Improvements

The project can be extended with several advanced features.

- Live Forex API Integration
- Real-Time Dashboard Refresh
- AI-Based Price Prediction
- Machine Learning Forecasting Models
- Automated Risk Alerts
- Trading Signal Recommendation Engine
- Publish Dashboard to Microsoft Power BI Service
- Mobile Dashboard Support
- Real-Time Currency Tracking
- Cloud-Based Data Pipeline

---

# 💼 Skills Demonstrated

This project demonstrates practical knowledge in:

### Programming

- Python

### Data Analysis

- Data Cleaning
- Exploratory Data Analysis (EDA)
- Financial Analytics
- Statistical Analysis

### Data Visualization

- Matplotlib
- Microsoft Power BI

### Business Intelligence

- Dashboard Design
- KPI Development
- Interactive Reports
- Data Storytelling

### Power BI

- DAX
- Data Modeling
- Relationships
- Slicers
- Drill Through
- KPI Cards
- Interactive Charts

### Financial Analytics

- Forex Market Analysis
- Trading Performance Analysis
- Portfolio Risk Assessment
- Monte Carlo Simulation
- Strategy Performance Evaluation

---

# 📈 Business Value

This dashboard helps users to:

- Monitor Forex Market Performance
- Analyze Trading Profit & Loss
- Evaluate Portfolio Risk
- Compare Trading Strategies
- Analyze Global Trading Sessions
- Support Data-Driven Investment Decisions

---

# 👨‍💻 Author

## Kishor Degama

**Aspiring Data Analyst**

### Skills

- Python
- SQL
- Microsoft Power BI
- Excel
- Data Visualization
- Financial Analytics
- Business Intelligence
- Dashboard Development

---

# ⭐ If You Like This Project

If you found this project helpful, please consider giving it a ⭐ on GitHub.

It motivates me to continue building more Data Analytics and Business Intelligence projects.

---

## Thank You

Thank you for visiting this repository.

I hope this project provides useful insights into Forex Market Analytics, Risk Analysis, and Interactive Business Intelligence using Python and Microsoft Power BI.

Happy Learning!
