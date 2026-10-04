import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Retail Sales Analytics Dashboard",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

/* Main container */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

/* Main title */
.main-title {
    font-size: 38px;
    font-weight: 800;
    margin-bottom: 0px;
}

/* Subtitle */
.subtitle {
    font-size: 16px;
    color: #808080;
    margin-bottom: 20px;
}

/* KPI cards */
.kpi-card {
    padding: 20px;
    border-radius: 14px;
    border: 1px solid rgba(128,128,128,0.25);
    background: rgba(128,128,128,0.05);
    text-align: center;
    min-height: 125px;
}

.kpi-title {
    font-size: 14px;
    color: #888;
    margin-bottom: 8px;
}

.kpi-value {
    font-size: 25px;
    font-weight: 700;
}

/* Section headings */
.section-title {
    font-size: 24px;
    font-weight: 700;
    margin-top: 15px;
    margin-bottom: 5px;
}

/* Footer */
.footer {
    text-align: center;
    color: #888;
    padding-top: 25px;
    padding-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    df = pd.read_csv("cleaned_retail_sales.csv")

    # Convert date
    df["order_date"] = pd.to_datetime(
        df["order_date"],
        errors="coerce"
    )

    # Create Revenue if not already present
    if "Revenue" not in df.columns:
        df["Revenue"] = df["sales_amount"]

    # Date features
    df["year"] = df["order_date"].dt.year
    df["month_num"] = df["order_date"].dt.month
    df["month_name"] = df["order_date"].dt.month_name()
    df["quarter"] = df["order_date"].dt.quarter
    df["day_name"] = df["order_date"].dt.day_name()

    return df


df = load_data()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🛍️ Retail Sales Analytics Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
    Interactive analysis of sales performance, customers, products,
    profitability and regional trends
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.title("🔎 Dashboard Filters")

st.sidebar.caption(
    "Use the filters below to explore the retail sales data."
)


# ---------------- DATE FILTER ----------------

min_date = df["order_date"].min().date()
max_date = df["order_date"].max().date()

date_range = st.sidebar.date_input(
    "Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)


# ---------------- REGION FILTER ----------------

regions = sorted(
    df["region"].dropna().unique().tolist()
)

selected_regions = st.sidebar.multiselect(
    "Region",
    options=regions,
    default=regions
)


# ---------------- CATEGORY FILTER ----------------

categories = sorted(
    df["product_category"].dropna().unique().tolist()
)

selected_categories = st.sidebar.multiselect(
    "Product Category",
    options=categories,
    default=categories
)


# ---------------- GENDER FILTER ----------------

genders = sorted(
    df["gender"].dropna().unique().tolist()
)

selected_genders = st.sidebar.multiselect(
    "Gender",
    options=genders,
    default=genders
)


# ---------------- PAYMENT FILTER ----------------

payment_methods = sorted(
    df["payment_method"].dropna().unique().tolist()
)

selected_payments = st.sidebar.multiselect(
    "Payment Method",
    options=payment_methods,
    default=payment_methods
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()

if len(date_range) == 2:

    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])

    filtered_df = filtered_df[
        (filtered_df["order_date"] >= start_date)
        &
        (filtered_df["order_date"] <= end_date)
    ]


filtered_df = filtered_df[
    filtered_df["region"].isin(selected_regions)
    &
    filtered_df["product_category"].isin(selected_categories)
    &
    filtered_df["gender"].isin(selected_genders)
    &
    filtered_df["payment_method"].isin(selected_payments)
]


# ============================================================
# EMPTY FILTER CHECK
# ============================================================

if filtered_df.empty:

    st.warning(
        "No records match the selected filters. "
        "Please change your filter selection."
    )

    st.stop()


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_revenue = filtered_df["Revenue"].sum()

total_profit = filtered_df["profit"].sum()

total_orders = len(filtered_df)

total_quantity = filtered_df["quantity"].sum()

unique_customers = filtered_df["customer_id"].nunique()

profit_margin = (
    total_profit / total_revenue * 100
    if total_revenue != 0
    else 0
)


# ============================================================
# KPI CARDS
# ============================================================

st.markdown(
    '<div class="section-title">📌 Business Overview</div>',
    unsafe_allow_html=True
)

k1, k2, k3, k4, k5 = st.columns(5)


with k1:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Revenue</div>
            <div class="kpi-value">₹{total_revenue/1_000_000:.2f}M</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with k2:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Profit</div>
            <div class="kpi-value">₹{total_profit/1_000_000:.2f}M</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with k3:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Orders</div>
            <div class="kpi-value">{total_orders:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with k4:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Unique Customers</div>
            <div class="kpi-value">{unique_customers:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with k5:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Profit Margin</div>
            <div class="kpi-value">{profit_margin:.2f}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.write("")


# ============================================================
# MONTHLY SALES TREND
# ============================================================

st.markdown(
    '<div class="section-title">📈 Sales Performance</div>',
    unsafe_allow_html=True
)


monthly_sales = (
    filtered_df
    .set_index("order_date")
    .resample("MS")["Revenue"]
    .sum()
    .reset_index()
)


fig_monthly = px.line(
    monthly_sales,
    x="order_date",
    y="Revenue",
    markers=True,
    title="Monthly Revenue Trend"
)

fig_monthly.update_layout(
    xaxis_title="Month",
    yaxis_title="Revenue",
    hovermode="x unified"
)

st.plotly_chart(
    fig_monthly,
    use_container_width=True
)


# ============================================================
# CATEGORY + REGION
# ============================================================

col1, col2 = st.columns(2)


# ---------------- CATEGORY REVENUE ----------------

with col1:

    category_revenue = (
        filtered_df
        .groupby("product_category", as_index=False)["Revenue"]
        .sum()
        .sort_values("Revenue", ascending=False)
    )

    fig_category = px.bar(
        category_revenue,
        x="product_category",
        y="Revenue",
        title="Revenue by Product Category"
    )

    fig_category.update_layout(
        xaxis_title="Product Category",
        yaxis_title="Revenue"
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )


# ---------------- REGION REVENUE ----------------

with col2:

    region_revenue = (
        filtered_df
        .groupby("region", as_index=False)["Revenue"]
        .sum()
        .sort_values("Revenue", ascending=False)
    )

    fig_region = px.bar(
        region_revenue,
        x="region",
        y="Revenue",
        title="Revenue by Region"
    )

    fig_region.update_layout(
        xaxis_title="Region",
        yaxis_title="Revenue"
    )

    st.plotly_chart(
        fig_region,
        use_container_width=True
    )


# ============================================================
# PRODUCT PERFORMANCE
# ============================================================

st.markdown(
    '<div class="section-title">📦 Product Performance</div>',
    unsafe_allow_html=True
)


top_products = (
    filtered_df
    .groupby("product_name", as_index=False)["quantity"]
    .sum()
    .sort_values("quantity", ascending=False)
    .head(10)
)


fig_products = px.bar(
    top_products.sort_values("quantity"),
    x="quantity",
    y="product_name",
    orientation="h",
    title="Top 10 Best-Selling Products"
)

fig_products.update_layout(
    xaxis_title="Quantity Sold",
    yaxis_title="Product"
)

st.plotly_chart(
    fig_products,
    use_container_width=True
)


# ============================================================
# CUSTOMER ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">👥 Customer Analysis</div>',
    unsafe_allow_html=True
)

col3, col4 = st.columns(2)


# ---------------- GENDER ----------------

with col3:

    gender_data = (
        filtered_df["gender"]
        .value_counts()
        .reset_index()
    )

    gender_data.columns = [
        "Gender",
        "Count"
    ]

    fig_gender = px.pie(
        gender_data,
        names="Gender",
        values="Count",
        hole=0.45,
        title="Customer Distribution by Gender"
    )

    st.plotly_chart(
        fig_gender,
        use_container_width=True
    )


# ---------------- AGE DISTRIBUTION ----------------

with col4:

    fig_age = px.histogram(
        filtered_df,
        x="age",
        nbins=20,
        title="Customer Age Distribution"
    )

    fig_age.update_layout(
        xaxis_title="Age",
        yaxis_title="Number of Customers"
    )

    st.plotly_chart(
        fig_age,
        use_container_width=True
    )


# ============================================================
# PROFIT ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">💰 Profitability Analysis</div>',
    unsafe_allow_html=True
)


col5, col6 = st.columns(2)


# ---------------- PROFIT BY CATEGORY ----------------

with col5:

    category_profit = (
        filtered_df
        .groupby(
            "product_category",
            as_index=False
        )["profit"]
        .sum()
        .sort_values(
            "profit",
            ascending=False
        )
    )

    fig_profit = px.bar(
        category_profit,
        x="product_category",
        y="profit",
        title="Profit by Product Category"
    )

    fig_profit.update_layout(
        xaxis_title="Product Category",
        yaxis_title="Profit"
    )

    st.plotly_chart(
        fig_profit,
        use_container_width=True
    )


# ---------------- DISCOUNT VS PROFIT ----------------

with col6:

    fig_discount = px.scatter(
        filtered_df,
        x="discount_pct",
        y="profit",
        opacity=0.55,
        title="Discount vs Profit",
        hover_data=[
            "product_name",
            "product_category"
        ]
    )

    fig_discount.update_layout(
        xaxis_title="Discount Percentage",
        yaxis_title="Profit"
    )

    st.plotly_chart(
        fig_discount,
        use_container_width=True
    )


# ============================================================
# GEOGRAPHICAL PERFORMANCE
# ============================================================

st.markdown(
    '<div class="section-title">🌍 Geographical Performance</div>',
    unsafe_allow_html=True
)


city_sales = (
    filtered_df
    .groupby("city", as_index=False)["Revenue"]
    .sum()
    .sort_values(
        "Revenue",
        ascending=False
    )
    .head(10)
)


fig_city = px.bar(
    city_sales.sort_values("Revenue"),
    x="Revenue",
    y="city",
    orientation="h",
    title="Top 10 Cities by Revenue"
)

fig_city.update_layout(
    xaxis_title="Revenue",
    yaxis_title="City"
)

st.plotly_chart(
    fig_city,
    use_container_width=True
)


# ============================================================
# CUSTOMER EXPERIENCE
# ============================================================

st.markdown(
    '<div class="section-title">⭐ Customer Experience</div>',
    unsafe_allow_html=True
)


col7, col8 = st.columns(2)


# ---------------- SATISFACTION ----------------

with col7:

    satisfaction_data = (
        filtered_df[
            "customer_satisfaction"
        ]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    satisfaction_data.columns = [
        "Satisfaction",
        "Count"
    ]

    fig_satisfaction = px.bar(
        satisfaction_data,
        x="Satisfaction",
        y="Count",
        title="Customer Satisfaction Distribution"
    )

    st.plotly_chart(
        fig_satisfaction,
        use_container_width=True
    )


# ---------------- RETURNS ----------------

with col8:

    return_data = (
        filtered_df[
            "return_flag"
        ]
        .astype(str)
        .value_counts()
        .reset_index()
    )

    return_data.columns = [
        "Return Status",
        "Count"
    ]

    fig_returns = px.pie(
        return_data,
        names="Return Status",
        values="Count",
        hole=0.45,
        title="Product Return Distribution"
    )

    st.plotly_chart(
        fig_returns,
        use_container_width=True
    )


# ============================================================
# ORDER + PAYMENT ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">🧾 Order & Payment Analysis</div>',
    unsafe_allow_html=True
)


col9, col10 = st.columns(2)


# ---------------- ORDER STATUS ----------------

with col9:

    order_status = (
        filtered_df[
            "order_status"
        ]
        .value_counts()
        .reset_index()
    )

    order_status.columns = [
        "Order Status",
        "Count"
    ]

    fig_order = px.bar(
        order_status,
        x="Order Status",
        y="Count",
        title="Order Status Distribution"
    )

    st.plotly_chart(
        fig_order,
        use_container_width=True
    )


# ---------------- PAYMENT METHOD ----------------

with col10:

    payment_data = (
        filtered_df[
            "payment_method"
        ]
        .value_counts()
        .reset_index()
    )

    payment_data.columns = [
        "Payment Method",
        "Count"
    ]

    fig_payment = px.bar(
        payment_data,
        x="Payment Method",
        y="Count",
        title="Payment Method Preferences"
    )

    fig_payment.update_layout(
        xaxis_tickangle=-35
    )

    st.plotly_chart(
        fig_payment,
        use_container_width=True
    )


# ============================================================
# KEY BUSINESS INSIGHTS
# ============================================================

st.markdown(
    '<div class="section-title">💡 Dynamic Business Insights</div>',
    unsafe_allow_html=True
)


best_product = (
    filtered_df
    .groupby("product_name")["quantity"]
    .sum()
    .idxmax()
)

best_category = (
    filtered_df
    .groupby("product_category")["Revenue"]
    .sum()
    .idxmax()
)

best_region = (
    filtered_df
    .groupby("region")["Revenue"]
    .sum()
    .idxmax()
)

best_city = (
    filtered_df
    .groupby("city")["Revenue"]
    .sum()
    .idxmax()
)

avg_satisfaction = (
    filtered_df[
        "customer_satisfaction"
    ].mean()
)


ins1, ins2, ins3 = st.columns(3)

with ins1:
    st.info(
        f"🏆 Best-selling product: **{best_product}**"
    )

with ins2:
    st.info(
        f"📦 Highest-revenue category: **{best_category}**"
    )

with ins3:
    st.info(
        f"🌍 Strongest region: **{best_region}**"
    )


ins4, ins5 = st.columns(2)

with ins4:
    st.info(
        f"🏙️ Highest-revenue city: **{best_city}**"
    )

with ins5:
    st.info(
        f"⭐ Average customer satisfaction: "
        f"**{avg_satisfaction:.2f}/5**"
    )


# ============================================================
# DATA EXPLORER
# ============================================================

st.markdown(
    '<div class="section-title">🔍 Data Explorer</div>',
    unsafe_allow_html=True
)


search_term = st.text_input(
    "Search Product",
    placeholder="Example: Jeans"
)


display_df = filtered_df.copy()


if search_term:

    display_df = display_df[
        display_df[
            "product_name"
        ]
        .astype(str)
        .str.contains(
            search_term,
            case=False,
            na=False
        )
    ]


display_columns = [
    "order_date",
    "customer_name",
    "gender",
    "product_category",
    "product_name",
    "quantity",
    "Revenue",
    "profit",
    "region",
    "city",
    "payment_method",
    "order_status"
]


available_display_columns = [
    col
    for col in display_columns
    if col in display_df.columns
]


st.dataframe(
    display_df[
        available_display_columns
    ],
    use_container_width=True,
    hide_index=True
)


# ============================================================
# DOWNLOAD FILTERED DATA
# ============================================================

csv = display_df.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="⬇️ Download Filtered Data",
    data=csv,
    file_name="filtered_retail_sales.csv",
    mime="text/csv"
)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div class="footer">
    Retail Sales Analytics Dashboard<br>
    Developed by <b>Shubham Maity</b><br>
    Oasis Infobyte — Data Analytics Internship
    </div>
    """,
    unsafe_allow_html=True
)