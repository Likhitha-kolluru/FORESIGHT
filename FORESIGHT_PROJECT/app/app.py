import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="FORESIGHT",
    page_icon="🏠",
    layout="wide"
)

css_file = Path(__file__).parent / "style.css"

with open(css_file, "r", encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

base_path = Path(__file__).parent.parent
output_path = base_path / "outputs"

sales = pd.read_csv(
    output_path / "clean_sales.csv"
)

sku = pd.read_csv(
    output_path / "sku_master.csv"
)

risk_data = pd.read_csv(
    output_path / "risk_results.csv"
)

weekly_forecast = pd.read_csv(
    output_path / "weekly_forecast.csv"
)

next_week_forecast = pd.read_csv(
    output_path / "next_week_forecast.csv"
)

sales["Date"] = pd.to_datetime(
    sales["Date"],
    errors="coerce"
)

weekly_forecast["Date"] = pd.to_datetime(
    weekly_forecast["Date"],
    errors="coerce"
)

if "Forecast_Date" in next_week_forecast.columns:
    next_week_forecast["Forecast_Date"] = pd.to_datetime(
        next_week_forecast["Forecast_Date"],
        errors="coerce"
    )

sales = sales.merge(
    sku[
        [
            "SKU",
            "Product_Name",
            "Category",
            "Subcategory"
        ]
    ],
    on="SKU",
    how="left"
)

risk_data = risk_data.merge(
    sku[
        [
            "SKU",
            "Product_Name",
            "Category",
            "Subcategory"
        ]
    ],
    on="SKU",
    how="left"
)

st.sidebar.title("🏠 FORESIGHT")

st.sidebar.markdown(
    "Demand & Inventory Intelligence"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Sales Analytics",
        "Demand Forecast",
        "Inventory Risk",
        "Executive Summary"
    ]
)


# =========================================================
# HOME
# =========================================================

if page == "Home":

    st.markdown(
        '<div class="main-title">🏠 FORESIGHT</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">AI-Powered Demand & Inventory Intelligence Platform</div>',
        unsafe_allow_html=True
    )

    total_revenue = sales["Revenue"].sum()
    total_units = sales["Units_Sold"].sum()
    active_skus = sku["SKU"].nunique()

    high_risk_skus = risk_data[
        risk_data["Risk_Level"] != "Healthy"
    ]["SKU"].nunique()

    value_at_risk = risk_data[
        "Final_Value_At_Risk"
    ].sum()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">TOTAL REVENUE</div>
                <div class="kpi-value">₹{total_revenue:,.0f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">UNITS SOLD</div>
                <div class="kpi-value">{total_units:,.0f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">ACTIVE SKUs</div>
                <div class="kpi-value">{active_skus}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">HIGH RISK SKUs</div>
                <div class="kpi-value">{high_risk_skus}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        '<div class="section-title">Inventory Value at Risk</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">ESTIMATED VALUE AT RISK</div>
            <div class="kpi-value">₹{value_at_risk:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">Primary Objectives</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            """
            <div class="info-card">
                <div class="info-title">📈 Demand Forecasting</div>
                <div class="info-text">
                    Predict future weekly demand at SKU level.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="info-card">
                <div class="info-title">⚠️ Stockout Early Warning</div>
                <div class="info-text">
                    Identify products that may fall below safety stock.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="info-card">
                <div class="info-title">📦 Overstock Detection</div>
                <div class="info-text">
                    Identify products with excess inventory.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="info-card">
                <div class="info-title">🎯 Inventory Recommendations</div>
                <div class="info-text">
                    Suggest reorder, markdown or monitoring actions.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ---------------------------------------------------------
    # BUSINESS PERFORMANCE
    # ---------------------------------------------------------

    st.markdown(
        '<div class="section-title">Business Performance</div>',
        unsafe_allow_html=True
    )

    monthly_revenue = (
        sales.groupby(
            sales["Date"].dt.to_period("M")
        )["Revenue"]
        .sum()
        .reset_index()
    )

    monthly_revenue["Date"] = (
        monthly_revenue["Date"].dt.to_timestamp()
    )

    monthly_revenue = monthly_revenue.sort_values("Date")

    monthly_revenue["Month"] = (
        monthly_revenue["Date"].dt.strftime("%b %Y")
    )

    revenue_chart = monthly_revenue[
        ["Month", "Revenue"]
    ].copy()

    revenue_chart = revenue_chart.set_index("Month")

    st.line_chart(
        revenue_chart,
        height=400
    )

    # ---------------------------------------------------------
    # REVENUE BY CATEGORY
    # ---------------------------------------------------------

    st.markdown(
        '<div class="section-title">Revenue by Category</div>',
        unsafe_allow_html=True
    )

    category_revenue = (
        sales.groupby("Category")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(
        category_revenue,
        height=400
    )

    # ---------------------------------------------------------
    # INVENTORY RISK
    # ---------------------------------------------------------

    st.markdown(
        '<div class="section-title">Inventory Risk</div>',
        unsafe_allow_html=True
    )

    risk_count = (
        risk_data["Risk_Level"]
        .value_counts()
        .reindex(
            [
                "Healthy",
                "High Overstock",
                "High Stockout",
                "High Both"
            ],
            fill_value=0
        )
    )

    st.dataframe(
        risk_count.rename("SKU Count"),
        width="stretch",
        hide_index=False
    )


# =========================================================
# SALES ANALYTICS
# =========================================================

elif page == "Sales Analytics":

    st.markdown(
        '<div class="main-title">Sales Analytics</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Historical sales performance analysis</div>',
        unsafe_allow_html=True
    )

    total_revenue = sales["Revenue"].sum()
    total_units = sales["Units_Sold"].sum()
    average_price = sales["Price"].mean()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">TOTAL REVENUE</div>
                <div class="kpi-value">₹{total_revenue:,.0f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">UNITS SOLD</div>
                <div class="kpi-value">{total_units:,.0f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">AVERAGE PRICE</div>
                <div class="kpi-value">₹{average_price:,.2f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ---------------------------------------------------------
    # MONTHLY REVENUE
    # ---------------------------------------------------------

    st.markdown(
        '<div class="section-title">Monthly Revenue</div>',
        unsafe_allow_html=True
    )

    monthly_revenue = (
        sales.groupby(
            sales["Date"].dt.to_period("M")
        )["Revenue"]
        .sum()
        .reset_index()
    )

    monthly_revenue["Date"] = (
        monthly_revenue["Date"].dt.to_timestamp()
    )

    monthly_revenue = monthly_revenue.sort_values("Date")

    monthly_revenue["Month"] = (
        monthly_revenue["Date"].dt.strftime("%b %Y")
    )

    revenue_chart = monthly_revenue[
        ["Month", "Revenue"]
    ].copy()

    revenue_chart = revenue_chart.set_index("Month")

    st.line_chart(
        revenue_chart,
        height=400
    )

    # ---------------------------------------------------------
    # REVENUE BY CATEGORY
    # ---------------------------------------------------------

    st.markdown(
        '<div class="section-title">Revenue by Category</div>',
        unsafe_allow_html=True
    )

    category_revenue = (
        sales.groupby("Category")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(
        category_revenue,
        height=400
    )

    # ---------------------------------------------------------
    # TOP PRODUCTS
    # ---------------------------------------------------------

    st.markdown(
        '<div class="section-title">Top Products by Revenue</div>',
        unsafe_allow_html=True
    )

    top_products = (
        sales.groupby(
            ["SKU", "Product_Name"]
        )["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    top_products["Revenue"] = (
        top_products["Revenue"].round(2)
    )

    st.dataframe(
        top_products,
        width="stretch",
        hide_index=True
    )


# =========================================================
# DEMAND FORECAST
# =========================================================

elif page == "Demand Forecast":

    st.markdown(
        '<div class="main-title">Demand Forecast</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Weekly SKU-level demand forecasting</div>',
        unsafe_allow_html=True
    )

    sku_list = sorted(
        weekly_forecast["SKU"].dropna().unique()
    )

    selected_sku = st.selectbox(
        "Select SKU",
        sku_list
    )

    sku_data = weekly_forecast[
        weekly_forecast["SKU"] == selected_sku
    ].copy()

    sku_data = sku_data.sort_values("Date")

    product_info = sku[
        sku["SKU"] == selected_sku
    ]

    if not product_info.empty:

        product_name = product_info.iloc[0]["Product_Name"]
        category = product_info.iloc[0]["Category"]

        st.write(
            f"**Product:** {product_name}"
        )

        st.write(
            f"**Category:** {category}"
        )

    # ---------------------------------------------------------
    # ACTUAL VS FORECAST
    # ---------------------------------------------------------

    st.markdown(
        '<div class="section-title">Actual vs Forecast</div>',
        unsafe_allow_html=True
    )

    chart_columns = [
        "Date",
        "Units_Sold",
        "Baseline_Forecast",
        "Model_Forecast"
    ]

    available_chart_columns = [
        col
        for col in chart_columns
        if col in sku_data.columns
    ]

    chart_data = sku_data[
        available_chart_columns
    ].copy()

    chart_data = chart_data.set_index("Date")

    st.line_chart(
        chart_data,
        height=400
    )

    # ---------------------------------------------------------
    # NEXT WEEK FORECAST
    # ---------------------------------------------------------

    st.markdown(
        '<div class="section-title">Next Week Forecast</div>',
        unsafe_allow_html=True
    )

    next_forecast = next_week_forecast[
        next_week_forecast["SKU"] == selected_sku
    ].copy()

    if not next_forecast.empty:

        forecast_value = (
            next_forecast.iloc[0]["Forecast_Next_Week"]
        )

        forecast_date = (
            next_forecast.iloc[0]["Forecast_Date"]
            if "Forecast_Date" in next_forecast.columns
            else None
        )

        if pd.notna(forecast_date):

            forecast_date_text = (
                forecast_date.strftime("%d %b %Y")
            )

        else:

            forecast_date_text = "Next week"

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">
                    FORECAST FOR {forecast_date_text.upper()}
                </div>
                <div class="kpi-value">
                    {forecast_value:,.2f} units
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ---------------------------------------------------------
    # FORECAST DATA
    # ---------------------------------------------------------

    st.markdown(
        '<div class="section-title">Forecast Data</div>',
        unsafe_allow_html=True
    )

    display_data = sku_data[
        available_chart_columns
    ].copy()

    if "Baseline_Forecast" in display_data.columns:

        display_data["Baseline_Forecast"] = (
            display_data["Baseline_Forecast"].round(2)
        )

    if "Model_Forecast" in display_data.columns:

        display_data["Model_Forecast"] = (
            display_data["Model_Forecast"].round(2)
        )

    st.dataframe(
        display_data.tail(20),
        width="stretch",
        hide_index=True
    )


# =========================================================
# INVENTORY RISK
# =========================================================

elif page == "Inventory Risk":

    st.markdown(
        '<div class="main-title">Inventory Risk</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Stockout and overstock risk analysis</div>',
        unsafe_allow_html=True
    )

    risk_count = (
        risk_data["Risk_Level"]
        .value_counts()
        .reindex(
            [
                "Healthy",
                "High Overstock",
                "High Stockout",
                "High Both"
            ],
            fill_value=0
        )
    )

    st.markdown(
        '<div class="section-title">Risk Distribution</div>',
        unsafe_allow_html=True
    )

    st.dataframe(
        risk_count.rename("SKU Count"),
        width="stretch",
        hide_index=False
    )

    risk_levels = [
        "All"
    ] + sorted(
        risk_data["Risk_Level"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_risk = st.selectbox(
        "Filter by Risk Level",
        risk_levels
    )

    if selected_risk == "All":

        filtered_risk = risk_data.copy()

    else:

        filtered_risk = risk_data[
            risk_data["Risk_Level"] == selected_risk
        ].copy()

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">PRODUCTS SHOWN</div>
                <div class="kpi-value">{len(filtered_risk)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        stockout_count = filtered_risk[
            filtered_risk["Stockout_Risk"] == True
        ].shape[0]

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">STOCKOUT RISK</div>
                <div class="kpi-value">{stockout_count}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        overstock_count = filtered_risk[
            filtered_risk["Overstock_Risk"] == True
        ].shape[0]

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">OVERSTOCK RISK</div>
                <div class="kpi-value">{overstock_count}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:

        filtered_value = filtered_risk[
            "Final_Value_At_Risk"
        ].sum()

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">VALUE AT RISK</div>
                <div class="kpi-value">₹{filtered_value:,.0f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ---------------------------------------------------------
    # INVENTORY RISK DETAILS
    # ---------------------------------------------------------

    st.markdown(
        '<div class="section-title">Inventory Risk Details</div>',
        unsafe_allow_html=True
    )

    columns_to_show = [
        "SKU",
        "Product_Name",
        "Category",
        "Current_Stock",
        "On_Order",
        "Lead_Time_Days",
        "Forecast_Next_Week",
        "Safety_Stock",
        "Risk_Level",
        "Recommended_Action",
        "Final_Value_At_Risk"
    ]

    available_columns = [
        col
        for col in columns_to_show
        if col in filtered_risk.columns
    ]

    display_risk = filtered_risk[
        available_columns
    ].copy()

    if "Forecast_Next_Week" in display_risk.columns:

        display_risk["Forecast_Next_Week"] = (
            display_risk["Forecast_Next_Week"].round(2)
        )

    if "Final_Value_At_Risk" in display_risk.columns:

        display_risk["Final_Value_At_Risk"] = (
            display_risk["Final_Value_At_Risk"].round(2)
        )

    st.dataframe(
        display_risk,
        width="stretch",
        height=500,
        hide_index=True
    )


# =========================================================
# EXECUTIVE SUMMARY
# =========================================================

elif page == "Executive Summary":

    st.markdown(
        '<div class="main-title">Executive Summary</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Business-focused demand and inventory insights</div>',
        unsafe_allow_html=True
    )

    total_revenue = sales["Revenue"].sum()

    high_risk_skus = risk_data[
        risk_data["Risk_Level"] != "Healthy"
    ]["SKU"].nunique()

    value_at_risk = risk_data[
        "Final_Value_At_Risk"
    ].sum()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">TOTAL REVENUE</div>
                <div class="kpi-value">₹{total_revenue:,.0f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">HIGH RISK SKUs</div>
                <div class="kpi-value">{high_risk_skus}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">VALUE AT RISK</div>
                <div class="kpi-value">₹{value_at_risk:,.0f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ---------------------------------------------------------
    # RISK SUMMARY
    # ---------------------------------------------------------

    st.markdown(
        '<div class="section-title">Risk Summary</div>',
        unsafe_allow_html=True
    )

    risk_count = (
        risk_data["Risk_Level"]
        .value_counts()
        .reindex(
            [
                "Healthy",
                "High Overstock",
                "High Stockout",
                "High Both"
            ],
            fill_value=0
        )
    )

    st.dataframe(
        risk_count.rename("SKU Count"),
        width="stretch",
        hide_index=False
    )

    # ---------------------------------------------------------
    # RECOMMENDED ACTIONS
    # ---------------------------------------------------------

    st.markdown(
        '<div class="section-title">Recommended Actions</div>',
        unsafe_allow_html=True
    )

    action_count = (
        risk_data["Recommended_Action"]
        .value_counts()
        .rename("SKU Count")
    )

    st.dataframe(
        action_count,
        width="stretch",
        hide_index=False
    )

    # ---------------------------------------------------------
    # TOP PRODUCTS
    # ---------------------------------------------------------

    st.markdown(
        '<div class="section-title">Top Products Requiring Attention</div>',
        unsafe_allow_html=True
    )

    attention = risk_data[
        risk_data["Risk_Level"] != "Healthy"
    ].copy()

    attention = attention.sort_values(
        "Final_Value_At_Risk",
        ascending=False
    )

    columns_to_show = [
        "SKU",
        "Product_Name",
        "Category",
        "Risk_Level",
        "Recommended_Action",
        "Forecast_Next_Week",
        "Final_Value_At_Risk"
    ]

    available_columns = [
        col
        for col in columns_to_show
        if col in attention.columns
    ]

    attention = attention[
        available_columns
    ].head(10)

    if "Forecast_Next_Week" in attention.columns:

        attention["Forecast_Next_Week"] = (
            attention["Forecast_Next_Week"].round(2)
        )

    if "Final_Value_At_Risk" in attention.columns:

        attention["Final_Value_At_Risk"] = (
            attention["Final_Value_At_Risk"].round(2)
        )

    st.dataframe(
        attention,
        width="stretch",
        hide_index=True
    )

    # ---------------------------------------------------------
    # KEY BUSINESS INSIGHTS
    # ---------------------------------------------------------

    st.markdown(
        '<div class="section-title">Key Business Insights</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="info-card">
            <div class="info-title">📈 Demand</div>
            <div class="info-text">
                The forecasting model provides SKU-level weekly demand
                estimates to support inventory planning.
            </div>
        </div>

        <div class="info-card">
            <div class="info-title">⚠️ Stockout Risk</div>
            <div class="info-text">
                Products projected below their safety stock during lead time
                are identified for reorder attention.
            </div>
        </div>

        <div class="info-card">
            <div class="info-title">📦 Overstock</div>
            <div class="info-text">
                Products with inventory significantly above expected demand
                are identified for possible markdown or clearance.
            </div>
        </div>

        <div class="info-card">
            <div class="info-title">🎯 Action</div>
            <div class="info-text">
                Risk results are converted into simple actions such as
                Reorder Now, Markdown / Clear, Watch / Volatile and Healthy.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )