📈 Forex Market Risk Analysis Dashboard
![Forex Market Dashboard](<page1_forex.jpeg>)

An end-to-end Financial Data Analytics project built using Python and Microsoft Power BI.

This project analyzes Forex market data, trading performance, portfolio risk, and trading sessions using interactive Power BI dashboards and Python-based Exploratory Data Analysis (EDA).

📌 Project Overview

This project demonstrates how Python and Microsoft Power BI can be combined to perform financial market analysis.

The dashboard provides interactive visualizations for:

Forex Market Analysis
Monte Carlo Portfolio Risk Simulation
Trading Session Performance
Trading Strategy Performance
Financial Business Intelligence Dashboard
🎯 Project Objectives
Analyze historical Forex price movements.
Evaluate trading Profit & Loss.
Simulate portfolio risk using Monte Carlo Simulation.
Analyze trading sessions across different markets.
Compare strategy-wise trading performance.
Build an interactive Power BI dashboard.
🛠 Technologies Used
Tool	Purpose
Python	Data Analysis
Pandas	Data Cleaning
NumPy	Numerical Computing
Matplotlib	Data Visualization
Microsoft Power BI	Dashboard Development
CSV	Data Storage
📂 Dataset Information
1️⃣ Forex Price Data

Historical Forex market prices.

Columns include:

DateTime
PairName
Open
High
Low
Close
Volume
2️⃣ Monte Carlo Simulation Data

Portfolio risk simulation.

Columns include:

ScenarioID
PortfolioPnL
VolShock
CorrShock
EURUSD_PnL
GBPUSD_PnL
USDJPY_PnL
3️⃣ Trade Log

Trading history dataset.

Columns include:

TradeID
PairName
EntryPrice
ExitPrice
EntryDateTime
ExitDateTime
HoldingDays
PnL
SignalType
StrategyName
4️⃣ Time Dimension

Custom Time Dimension table.

Columns include:

Hour
Session
IsOverlap
TimeKey
🐍 Python Analysis

Python was used for:

Data Cleaning
Missing Value Detection
Duplicate Detection
Exploratory Data Analysis (EDA)
Summary Statistics
Financial Visualization

Generated Charts:

Forex Price Trend
PnL Distribution
Currency Pair PnL Comparison
🧩 Data Model

The Power BI model contains four tables:

forex_price_data
mc_scenarios
trade_log
DimTime

The DimTime table is related to the Trade Log for Trading Session Analysis.

📸 Data Model


(![Data Model](<data_model.jpeg>))

📊 Power BI Dashboard

The report contains 5 interactive pages.

📈 Page 1 – Forex Market Dashboard
Features
Current Price KPI
Highest Price KPI
Lowest Price KPI
Average Price KPI
Forex Price Trend
PnL by Currency Pair
Signal Distribution
Currency Pair Filter
Date Filter

![Forex Market Dashboard](<page1_forex.jpeg>)


📉 Page 2 – Monte Carlo Risk Analysis
Features
Average Portfolio PnL
Maximum Portfolio PnL
Minimum Portfolio PnL
Portfolio Simulation
Risk vs Return Scatter Plot
Scenario Range Slider
Interactive Tooltip

![Monte Carlo Risk Analysis](<page2_monte_carlo.jpeg>)


🌍 Page 3 – Trading Session Analysis
Features
Trading Session Heatmap
Session-wise PnL
Overlap Premium KPI

Sessions Covered:

London
New York
Tokyo
Sydney

![Trading Session Analysis](<page3_trading_session.jpeg>)


📊 Page 4 – Strategy Performance Analysis
Features
Strategy-wise Profit & Loss
Strategy Distribution
Signal Filter

Strategies Included:

ML_RF
ML_XGB
MACD_Trend
RSI_Reversal
MA_Cross
RL_PPO
Composite

![Strategy Performance Dashboard](<page4_strategy.jpeg>)

📷 Python Output Screenshots
Forex Price Trend


![Forex Price Trend](<forex_price_trend.jpeg>)
Trade PnL Distribution
![Trade PnL Distribution](<pnl_distribution.jpeg>)


Currency Pair PnL

![Currency Pair Analysis](<currency_pair.jpeg>)

📈 Key Insights
Analyzed historical Forex prices.
Compared multiple currency pairs.
Simulated 1000 Monte Carlo scenarios.
Visualized portfolio risk.
Compared trading sessions.
Evaluated strategy performance.
Built an interactive Power BI dashboard.
📁 Project Structure
Forex-Market-Risk-Analysis/
│
├── Data/
│   ├── forex_price_data.csv
│   ├── mc_scenarios.csv
│   ├── trade_log.csv
│
├── Outputs/
│   ├── forex_price_trend.png
│   ├── pnl_distribution.png
│   ├── pairwise_pnl.png
│   ├── forex_dashboard.png
│   ├── monte_carlo_dashboard.png
│   ├── trading_session_dashboard.png
│   ├── strategy_dashboard.png
│   └── data_model.png
│
├── analysis.py
├── Project_1C_Dashboard.pbix
├── README.md
├── requirements.txt
└── LICENSE
🚀 Future Improvements
Live Forex API Integration
Real-Time Dashboard Refresh
AI-Based Price Prediction
Automated Risk Alerts
Trading Signal Recommendation
Publish Dashboard to Power BI Service
💼 Skills Demonstrated
Python Programming
Data Cleaning
Exploratory Data Analysis (EDA)
Financial Analytics
Monte Carlo Simulation
Microsoft Power BI
DAX
Data Modeling
Interactive Dashboard Design
Business Intelligence
👨‍💻 Author
Kishor Degama

Aspiring Data Analyst

Skills
Python
SQL
Power BI
Excel
Data Visualization
Financial Analytics
