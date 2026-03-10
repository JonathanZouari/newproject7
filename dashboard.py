import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Dashboard", layout="wide")

# Title
st.title("Eyal Dashboard")

# Sidebar
st.sidebar.header("Filters")
selected_metric = st.sidebar.selectbox(
    "Select Metric",
    ["Sales", "Revenue", "Users", "Engagement"]
)

# Create sample data
data = {
    'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    'Sales': [120, 150, 180, 160, 200, 220],
    'Revenue': [12000, 15000, 18000, 16000, 20000, 22000],
    'Users': [500, 650, 800, 750, 900, 1000],
    'Engagement': [65, 70, 75, 72, 80, 85]
}
df = pd.DataFrame(data)

# Metrics row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Sales", f"{df['Sales'].sum()}", "+12%")
with col2:
    st.metric("Total Revenue", f"${df['Revenue'].sum():,}", "+15%")
with col3:
    st.metric("Total Users", f"{df['Users'].sum():,}", "+18%")
with col4:
    st.metric("Avg Engagement", f"{df['Engagement'].mean():.1f}%", "+8%")

# Charts
st.subheader(f"{selected_metric} Over Time")
fig = px.line(df, x='Month', y=selected_metric, markers=True)
st.plotly_chart(fig, use_container_width=True)

# Data table
st.subheader("Data Table")
st.dataframe(df, use_container_width=True)