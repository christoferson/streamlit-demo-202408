import pandas as pd
import streamlit as st
import numpy as np
from datetime import datetime, timedelta
import random

# Custom CSS for this page
st.markdown("""
<style>
    .chart-container {
        background: linear-gradient(145deg, #f8f9fa, #ffffff);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .data-header {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Page header
st.markdown("""
<div class="data-header">
    <h1>📊 Charts & Data Visualization</h1>
    <p>Interactive dashboards with real-time data insights</p>
</div>
""", unsafe_allow_html=True)

# Sidebar controls
st.sidebar.markdown("# 📊 Chart Controls")
st.sidebar.markdown("Customize your data visualization experience")

# Data generation controls
data_points = st.sidebar.slider("Number of data points", 10, 100, 50)
chart_type = st.sidebar.selectbox(
    "Select chart type",
    ["Line Chart", "Bar Chart", "Area Chart", "Scatter Plot", "All Charts"]
)

# Generate sample data
@st.cache_data
def generate_sample_data(n_points):
    dates = [datetime.now() - timedelta(days=x) for x in range(n_points, 0, -1)]
    
    # Sales data
    sales_data = {
        'Date': dates,
        'Sales': [random.randint(1000, 5000) + i*10 for i in range(n_points)],
        'Profit': [random.randint(200, 1000) + i*5 for i in range(n_points)],
        'Customers': [random.randint(50, 200) + i*2 for i in range(n_points)],
        'Region': [random.choice(['North', 'South', 'East', 'West']) for _ in range(n_points)]
    }
    
    return pd.DataFrame(sales_data)

# Generate data
df = generate_sample_data(data_points)

# Key metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="💰 Total Sales",
        value=f"${df['Sales'].sum():,}",
        delta=f"{df['Sales'].iloc[-1] - df['Sales'].iloc[-2]:,}"
    )

with col2:
    st.metric(
        label="📈 Avg Profit",
        value=f"${df['Profit'].mean():.0f}",
        delta=f"{((df['Profit'].iloc[-5:].mean() - df['Profit'].iloc[-10:-5].mean()) / df['Profit'].iloc[-10:-5].mean() * 100):.1f}%"
    )

with col3:
    st.metric(
        label="👥 Total Customers",
        value=f"{df['Customers'].sum():,}",
        delta=f"{df['Customers'].iloc[-1] - df['Customers'].iloc[-2]}"
    )

with col4:
    st.metric(
        label="📊 Data Points",
        value=len(df),
        delta="Live Data"
    )

st.markdown("---")

# Chart display based on selection
if chart_type == "Line Chart" or chart_type == "All Charts":
    st.markdown("### 📈 Sales Trend Over Time")
    
    # Prepare data for line chart
    chart_data = df.set_index('Date')[['Sales', 'Profit']]
    st.line_chart(chart_data, height=400)
    
    # Additional insights
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"📈 Sales Growth: {((df['Sales'].iloc[-1] - df['Sales'].iloc[0]) / df['Sales'].iloc[0] * 100):.1f}%")
    with col2:
        st.info(f"💰 Profit Growth: {((df['Profit'].iloc[-1] - df['Profit'].iloc[0]) / df['Profit'].iloc[0] * 100):.1f}%")

if chart_type == "Bar Chart" or chart_type == "All Charts":
    st.markdown("### 📊 Regional Performance")
    
    regional_data = df.groupby('Region').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Customers': 'sum'
    }).reset_index()
    
    # Display regional data as bar chart
    st.bar_chart(regional_data.set_index('Region')['Sales'], height=400)
    
    # Show regional breakdown
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Top Region by Sales:**")
        top_region = regional_data.loc[regional_data['Sales'].idxmax()]
        st.success(f"{top_region['Region']}: ${top_region['Sales']:,}")
    
    with col2:
        st.markdown("**Most Profitable Region:**")
        profit_region = regional_data.loc[regional_data['Profit'].idxmax()]
        st.success(f"{profit_region['Region']}: ${profit_region['Profit']:,}")

if chart_type == "Area Chart" or chart_type == "All Charts":
    st.markdown("### 🌊 Cumulative Growth")
    
    df_cumulative = df.copy()
    df_cumulative['Cumulative_Sales'] = df_cumulative['Sales'].cumsum()
    df_cumulative['Cumulative_Profit'] = df_cumulative['Profit'].cumsum()
    
    # Area chart using Streamlit's built-in functionality
    area_data = df_cumulative.set_index('Date')[['Cumulative_Sales', 'Cumulative_Profit']]
    st.area_chart(area_data, height=400)
    
    # Growth insights
    total_growth = df_cumulative['Cumulative_Sales'].iloc[-1]
    st.info(f"🚀 Total Cumulative Sales: ${total_growth:,}")

if chart_type == "Scatter Plot" or chart_type == "All Charts":
    st.markdown("### 🎯 Sales vs Profit Analysis")
    
    # Create scatter plot data
    scatter_data = df[['Sales', 'Profit']].copy()
    st.scatter_chart(scatter_data, x='Sales', y='Profit', height=400)
    
    # Correlation analysis
    correlation = df['Sales'].corr(df['Profit'])
    if correlation > 0.7:
        st.success(f"📈 Strong positive correlation: {correlation:.2f}")
    elif correlation > 0.3:
        st.info(f"📊 Moderate correlation: {correlation:.2f}")
    else:
        st.warning(f"📉 Weak correlation: {correlation:.2f}")
    
    # Additional scatter insights
    col1, col2, col3 = st.columns(3)
    with col1:
        avg_sales = df['Sales'].mean()
        st.metric("Avg Sales", f"${avg_sales:.0f}")
    with col2:
        avg_profit = df['Profit'].mean()
        st.metric("Avg Profit", f"${avg_profit:.0f}")
    with col3:
        profit_margin = (df['Profit'].sum() / df['Sales'].sum()) * 100
        st.metric("Profit Margin", f"{profit_margin:.1f}%")

# Interactive data table
st.markdown("---")
st.markdown("### 📋 Interactive Data Table")

# Add filters
col1, col2 = st.columns(2)
with col1:
    region_filter = st.multiselect(
        "Filter by Region",
        options=df['Region'].unique(),
        default=df['Region'].unique()
    )

with col2:
    sales_range = st.slider(
        "Sales Range",
        min_value=int(df['Sales'].min()),
        max_value=int(df['Sales'].max()),
        value=(int(df['Sales'].min()), int(df['Sales'].max()))
    )

# Apply filters
filtered_df = df[
    (df['Region'].isin(region_filter)) &
    (df['Sales'] >= sales_range[0]) &
    (df['Sales'] <= sales_range[1])
]

# Display filtered data
st.dataframe(
    filtered_df,
    column_config={
        "Date": st.column_config.DateColumn("Date", format="DD/MM/YYYY"),
        "Sales": st.column_config.NumberColumn("Sales ($)", format="$%d"),
        "Profit": st.column_config.NumberColumn("Profit ($)", format="$%d"),
        "Customers": st.column_config.NumberColumn("Customers", format="%d"),
        "Region": st.column_config.TextColumn("Region")
    },
    use_container_width=True,
    hide_index=True
)

# Download data option
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Data as CSV",
        data=csv,
        file_name=f'sales_data_{datetime.now().strftime("%Y%m%d")}.csv',
        mime='text/csv',
        type="primary"
    )

# Real-time simulation
if st.sidebar.button("🔄 Refresh Data", type="primary"):
    st.cache_data.clear()
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip**: Use the controls above to customize your charts and explore different visualizations!")