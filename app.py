import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Customer Segmentation Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load Data
df = pd.read_csv("data/customer_segments.csv")

# Header
st.title("🛍 Customer Segmentation Dashboard")
st.markdown("### Customer Analytics using K-Means Clustering")

# ==========================
# KPI CARDS
# ==========================
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Customers", len(df))

with col2:
    st.metric("Number of Clusters", df['Cluster'].nunique())

with col3:
    st.metric(
        "Average Spending Score",
        round(df['Spending Score (1-100)'].mean(), 2)
    )

# ==========================
# Dataset Preview
# ==========================
st.header("📄 Dataset Preview")
st.dataframe(df.head())

# ==========================
# Cluster Summary
# ==========================
st.header("📊 Cluster Summary")

summary = df.groupby('Cluster').agg({
    'Age':'mean',
    'Annual Income (k$)':'mean',
    'Spending Score (1-100)':'mean'
}).round(2)

st.dataframe(summary)

# ==========================
# Cluster Visualization
# ==========================
st.header("🎯 Customer Segments")

fig, ax = plt.subplots(figsize=(10,6))

sns.scatterplot(
    data=df,
    x='Annual Income (k$)',
    y='Spending Score (1-100)',
    hue='Cluster',
    palette='Set1',
    s=100,
    ax=ax
)

st.pyplot(fig)

# ==========================
# Cluster Distribution
# ==========================
st.header("📈 Cluster Distribution")

cluster_counts = df['Cluster'].value_counts()

fig2, ax2 = plt.subplots(figsize=(8,5))

ax2.bar(
    cluster_counts.index.astype(str),
    cluster_counts.values
)

ax2.set_xlabel("Cluster")
ax2.set_ylabel("Customers")
ax2.set_title("Customers per Cluster")

st.pyplot(fig2)

# ==========================
# Download Button
# ==========================
st.header("⬇ Download Segmented Dataset")

csv = df.to_csv(index=False)

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="customer_segments.csv",
    mime="text/csv"
)

# ==========================
# Business Insights
# ==========================
st.header("💡 Business Insights")

st.success("""
Cluster 0 → Regular Customers

Cluster 1 → Premium Customers

Cluster 2 → Loyal Shoppers

Cluster 3 → Potential Customers

Cluster 4 → Budget Customers
""")
