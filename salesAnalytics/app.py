import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
from scipy import stats
import streamlit as st

# Configure page
st.set_page_config(page_title="Retail Sales Analytics", layout="wide")

# Title
st.title("🛍️ Retail Sales Analytics Dashboard")

# Load data
DATA_PATH = r"D:\retail-sales-analytics\salesAnalytics\Sample - Superstore.csv"  # Update if needed

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH, encoding="ISO-8859-1")

data = load_data()
data.columns = data.columns.str.strip()

# Data Cleaning
data.dropna(inplace=True)
data['Order Date'] = pd.to_datetime(data['Order Date'])
data['month'] = data['Order Date'].dt.month
data['year'] = data['Order Date'].dt.year

# Show raw data
if st.checkbox("🔍 Show Raw Data"):
    st.dataframe(data.head())

# Summary info
with st.expander("ℹ️ Dataset Info"):
    buffer = []
    data.info(buf=buffer)
    s = "\n".join(buffer)
    st.text(s)

# Descriptive Stats
st.subheader("📊 Descriptive Statistics")
st.write(data.describe())

# Correlation Heatmap
st.subheader("🔁 Correlation Matrix (Numeric Columns Only)")
num_data = data.select_dtypes(include='number')
corr_matrix = num_data.corr()

fig1, ax1 = plt.subplots(figsize=(7, 7))
sb.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax1)
st.pyplot(fig1)

# Monthly Sales Lineplot
st.subheader("📈 Monthly Sales Trend")
monthly_sales = data.groupby(['year', 'month'])['Sales'].sum().reset_index()
fig2, ax2 = plt.subplots(figsize=(14, 7))
sb.lineplot(data=monthly_sales, x='month', y='Sales', hue='year', ax=ax2)
plt.title("Monthly Sales Report")
st.pyplot(fig2)

# Category-wise Sales by Region (Bar)
st.subheader("📦 Category-wise Sales by Region")
fig3, ax3 = plt.subplots(figsize=(12, 6))
sb.barplot(data=data, x='Category', y='Sales', hue='Region', ax=ax3)
st.pyplot(fig3)

# Sales Distribution by Region (Pie)
st.subheader("🌍 Sales Distribution by Region")
region_sales = data.groupby('Region')['Sales'].sum()
fig4, ax4 = plt.subplots()
ax4.pie(region_sales, labels=region_sales.index, autopct='%1.1f%%')
plt.title("Sales by Region")
st.pyplot(fig4)

# Scatterplot: Sales vs Profit
st.subheader("💰 Sales vs Profit by Segment")
fig5, ax5 = plt.subplots(figsize=(8, 6))
sb.scatterplot(data=data, x='Sales', y='Profit', hue='Segment', ax=ax5)
st.pyplot(fig5)

# Product Performance Heatmap
st.subheader("🧾 Product Performance (Pivot Heatmap)")
try:
    product_perf = data.pivot_table(values='Sales', index='Category', columns='Sub-Category', aggfunc='sum')
    fig6, ax6 = plt.subplots(figsize=(12, 8))
    sb.heatmap(product_perf, cmap='YlGnBu', ax=ax6)
    st.pyplot(fig6)
except KeyError as e:
    st.warning(f"Missing column: {e}")

# Hypothesis Test
st.subheader("📊 Region-wise Sales Comparison (T-Test)")

region1 = st.selectbox("Select Region 1", data["Region"].unique())
region2 = st.selectbox("Select Region 2", data["Region"].unique())
threshold = 0.05

r1_sales = data[data["Region"] == region1]["Sales"]
r2_sales = data[data["Region"] == region2]["Sales"]

t_stat, p_val = stats.ttest_ind(r1_sales, r2_sales)
st.write(f"**T-test Result for {region1} vs {region2}:**")
st.write(f"p-value = `{p_val:.4f}`")

if p_val < threshold:
    st.success("✅ Significant difference between the two regions (Reject H₀)")
else:
    st.info("❕ No significant difference (Fail to Reject H₀)")

# Discount Distribution
st.subheader("🧮 Discount Distribution")
fig7, ax7 = plt.subplots()
sb.histplot(data=data, x='Discount', bins=20, kde=True, ax=ax7)
st.pyplot(fig7)

