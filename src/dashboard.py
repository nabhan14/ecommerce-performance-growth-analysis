import pandas as pd
import streamlit as st
import plotly.express as px

# Load Data
df = pd.read_csv("data/processed/retail_clean.csv")
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Dashboard Title
st.set_page_config(page_title="E-commerce Sales Analysis", layout="wide")
st.title("📊 E-commerce Performance & Growth Analysis Dashboard")

st.markdown(
    """
    <h3 style='font-size:20px;'>This dashboard provides a quick overview of e-commerce performance:</h3>
    <ul>
        <li><b>Top Selling Products</b> → what customers buy most</li>
        <li><b>Top Customers</b> → who drives the most revenue</li>
        <li><b>Monthly Sales Trend</b> → how sales evolve over time</li>
    </ul>
    """,
    unsafe_allow_html=True
)

# Key Metrics (KPIs)
col1, col2, col3 = st.columns(3)

total_revenue = df["TotalPrice"].sum()
unique_customers = df["CustomerID"].nunique()
total_orders = df["InvoiceNo"].nunique()

col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Unique Customers", unique_customers)
col3.metric("Total Orders", total_orders)

st.markdown("---")

# Top Selling Products
st.subheader("Top Selling Products")
top_products = (
    df.groupby("Description")["Quantity"]
    .sum()
    .reset_index()
    .sort_values(by="Quantity", ascending=False)
    .head(10)
)
fig1 = px.bar(
    top_products,
    x="Description",
    y="Quantity",
    title="Top 10 Products by Quantity Sold",
    text="Quantity",
)
fig1.update_layout(title=dict(font=dict(size=20)))
fig1.update_layout(xaxis_tickangle=-45, height=500)
st.plotly_chart(fig1, use_container_width=True)

# Top Customers
st.subheader("Top Customers by Revenue")
top_customers = (
    df.groupby("CustomerID")["TotalPrice"]
    .sum()
    .reset_index()
    .sort_values(by="TotalPrice", ascending=False)
    .head(10)
)
fig2 = px.bar(
    top_customers,
    x="CustomerID",
    y="TotalPrice",
    title="Top 10 Customers by Spending",
    text="TotalPrice",
)
fig2.update_layout(title=dict(font=dict(size=20)))
fig2.update_traces(texttemplate="%{text:.2s}", textposition="outside")
fig2.update_layout(height=500)
st.plotly_chart(fig2, use_container_width=True)

# Monthly Sales Trend
st.subheader("Monthly Sales Trend")
monthly_sales = (
    df.groupby(df["InvoiceDate"].dt.to_period("M"))["TotalPrice"]
    .sum()
    .reset_index()
)
monthly_sales["InvoiceDate"] = monthly_sales["InvoiceDate"].astype(str)

fig3 = px.line(
    monthly_sales,
    x="InvoiceDate",
    y="TotalPrice",
    title="Sales Trend Over Time",
    markers=True,
)
fig3.update_layout(title=dict(font=dict(size=20)))
fig3.update_layout(height=500)
st.plotly_chart(fig3, use_container_width=True)

fig1.write_image("reports/figures/top_10_products.png")
fig2.write_image("reports/figures/top_10_customers.png")
fig3.write_image("reports/figures/monthly_sales_trend.png")
