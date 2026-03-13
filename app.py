# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration

st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Title

st.title("📊 Sales Data Dashboard")
st.markdown("""
Welcome! This interactive dashboard helps you explore your sales data.
Use the sidebar filters to customize your view.
""")


# Load Dataset

try:
    df = pd.read_csv("dataset/sales.csv")
    df.columns = df.columns.str.strip()  # remove spaces
except FileNotFoundError:
    st.error("❌ Dataset not found! Please make sure 'dataset/sales.csv' exists.")
    st.stop()


# Sidebar Filters

st.sidebar.header("Filter Options")
regions = st.sidebar.multiselect(
    "Select Region", options=df["Region"].unique(), default=df["Region"].unique()
)
categories = st.sidebar.multiselect(
    "Select Category", options=df["Category"].unique(), default=df["Category"].unique()
)

filtered_df = df[(df["Region"].isin(regions)) & (df["Category"].isin(categories))]


# Key Metrics

st.subheader("🏆 Key Metrics")
col1, col2, col3 = st.columns(3)

with col1:
    total_sales = filtered_df["Sales"].sum()
    st.metric("💰 Total Sales", f"${total_sales:,.2f}")

with col2:
    total_orders = filtered_df.shape[0]
    st.metric("🛒 Total Orders", f"{total_orders}")

with col3:
    if "Profit" in filtered_df.columns:
        total_profit = filtered_df["Profit"].sum()
        st.metric("📈 Total Profit", f"${total_profit:,.2f}")
    else:
        st.metric("📈 Total Profit", "N/A")

st.markdown("---")


# Charts

st.subheader("Sales by Category")
fig_category = px.bar(
    filtered_df,
    x="Category",
    y="Sales",
    color="Category",
    text="Sales",
    title="💡 Sales by Category",
    template="plotly_white",
    color_discrete_sequence=px.colors.qualitative.Pastel
)
fig_category.update_traces(texttemplate="$%{text:,.2f}", textposition="outside")
st.plotly_chart(fig_category, use_container_width=True)

st.subheader("Sales by Region")
fig_region = px.pie(
    filtered_df,
    names="Region",
    values="Sales",
    title="💡 Sales Distribution by Region",
    template="plotly_white",
    color_discrete_sequence=px.colors.qualitative.Vivid
)
st.plotly_chart(fig_region, use_container_width=True)

st.subheader("Sales Trend Over Time")
if "Order Date" in df.columns:
    df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True, errors='coerce')
    sales_trend = df.groupby("Order Date")["Sales"].sum().reset_index()
    fig_trend = px.line(
        sales_trend,
        x="Order Date",
        y="Sales",
        title="📈 Sales Trend Over Time",
        template="plotly_white",
        markers=True
    )
    st.plotly_chart(fig_trend, use_container_width=True)


# Raw Data Table

st.subheader("📋 Raw Dataset Preview")
st.dataframe(filtered_df, use_container_width=True)

# Download Button

st.download_button(
    label="⬇ Download Filtered Data as CSV",
    data=filtered_df.to_csv(index=False),
    file_name='filtered_sales.csv',
    mime='text/csv.'
)

