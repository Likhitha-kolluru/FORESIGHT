# FORESIGHT – Demand & Inventory Intelligence Platform

FORESIGHT is a Data Science and Analytics project that uses sales and inventory data to support demand forecasting and inventory planning.

The project provides:

- Sales and revenue analysis
- SKU-level demand forecasting
- Seasonal-naive baseline comparison
- Random Forest forecasting
- Stockout risk detection
- Overstock risk detection
- Inventory value-at-risk estimation
- Recommended inventory actions
- Interactive Streamlit dashboard

## Project Objectives

1. Analyze historical sales data.
2. Identify important sales and demand patterns.
3. Forecast weekly demand at SKU level.
4. Compare the forecasting model with a seasonal-naive baseline.
5. Identify products with stockout risk.
6. Identify products with overstock risk.
7. Estimate inventory value at risk.
8. Provide recommended actions for inventory planning.
9. Build an interactive dashboard using Streamlit.

## Technology Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Random Forest Regressor
- Matplotlib
- Streamlit
- Jupyter Notebook
- GitHub

## Project Structure

```text
FORESIGHT_PROJECT/
│
├── app/
│   ├── app.py
│   └── style.css
│
├── data/
│   ├── calendar.csv
│   ├── inventory_snapshots.csv
│   ├── sales_daily.csv
│   └── sku_master.csv
│
├── documentation/
│   ├── FORESIGHT.docx
│   └── FORESIGHT.pdf
│
├── models/
│
├── notebooks/
│   └── FORESIGHT_Project.ipynb
│
├── outputs/
│   ├── clean_sales.csv
│   ├── cv_results.csv
│   ├── next_week_forecast.csv
│   ├── risk_results.csv
│   ├── sku_master.csv
│   └── weekly_forecast.csv
│
├── README.md
└── requirements.txt
