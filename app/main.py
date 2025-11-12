"""
Solar Data Discovery Dashboard
Streamlit app for comparing solar potential across Benin, Sierra Leone, and Togo
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import sys
import os

# Add project root to path to import utils
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from app.utils import load_data, create_comparison_plot, calculate_metrics, get_country_summary

# Page configuration
st.set_page_config(
    page_title="Solar Data Discovery",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
    }
    .country-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">☀️ Solar Data Discovery Dashboard</h1>', 
                unsafe_allow_html=True)
    st.markdown("Compare solar potential across Benin, Sierra Leone, and Togo")
    
    # Sidebar
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.selectbox(
        "Choose Dashboard View",
        ["📊 Country Comparison", "📈 Time Series Analysis", "🌡️ Weather Correlations", "🏆 Regional Rankings"]
    )
    
    # Load data
    with st.spinner("Loading solar data..."):
        df_all = load_data()
    
    if df_all is None:
        st.error("❌ Could not load data. Please make sure the cleaned CSV files exist in the data directory.")
        return
    
    # Main content based on selection
    if app_mode == "📊 Country Comparison":
        show_country_comparison(df_all)
    elif app_mode == "📈 Time Series Analysis":
        show_time_series(df_all)
    elif app_mode == "🌡️ Weather Correlations":
        show_weather_correlations(df_all)
    elif app_mode == "🏆 Regional Rankings":
        show_regional_rankings(df_all)
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.info(
        "This dashboard analyzes solar irradiance data from three West African countries "
        "to identify optimal locations for solar farm development."
    )

def show_country_comparison(df_all):
    st.header("📊 Country Comparison")
    
    # Controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        metric = st.selectbox(
            "Select Solar Metric",
            ["GHI", "DNI", "DHI"],
            index=0,
            help="GHI: Global Horizontal Irradiance, DNI: Direct Normal Irradiance, DHI: Diffuse Horizontal Irradiance"
        )
    
    with col2:
        plot_type = st.selectbox(
            "Plot Type",
            ["Box Plot", "Violin Plot", "Bar Chart"],
            index=0
        )
    
    with col3:
        selected_countries = st.multiselect(
            "Select Countries",
            options=df_all['Country'].unique(),
            default=df_all['Country'].unique()
        )
    
    if not selected_countries:
        st.warning("Please select at least one country")
        return
    
    # Filter data
    df_filtered = df_all[df_all['Country'].isin(selected_countries)]
    
    # Create plot
    fig = create_comparison_plot(df_filtered, metric, plot_type)
    st.plotly_chart(fig, use_container_width=True)
    
    # Metrics cards
    st.subheader("📈 Summary Statistics")
    cols = st.columns(len(selected_countries))
    
    for idx, country in enumerate(selected_countries):
        country_data = df_filtered[df_filtered['Country'] == country]
        with cols[idx]:
            st.markdown(f'<div class="country-card">', unsafe_allow_html=True)
            st.metric(
                label=f"**{country}** - Average {metric}",
                value=f"{country_data[metric].mean():.1f} W/m²",
                delta=f"Median: {country_data[metric].median():.1f} W/m²"
            )
            st.caption(f"Records: {len(country_data):,}")
            st.caption(f"Std Dev: {country_data[metric].std():.1f}")
            st.markdown('</div>', unsafe_allow_html=True)

def show_time_series(df_all):
    st.header("📈 Time Series Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        country_ts = st.selectbox(
            "Select Country",
            df_all['Country'].unique(),
            key="ts_country"
        )
    
    with col2:
        metric_ts = st.selectbox(
            "Select Metric",
            ["GHI", "DNI", "DHI", "Tamb", "WS"],
            key="ts_metric"
        )
    
    if 'Timestamp' not in df_all.columns:
        st.warning("Timestamp data not available for time series analysis")
        return
    
    # Filter and prepare time series data
    df_country = df_all[df_all['Country'] == country_ts].copy()
    df_country['Timestamp'] = pd.to_datetime(df_country['Timestamp'])
    df_country = df_country.sort_values('Timestamp')
    
    # Resample for different time scales
    resample_period = st.select_slider(
        "Time Aggregation",
        options=["Raw", "Hourly", "Daily", "Monthly"],
        value="Daily"
    )
    
    if resample_period == "Hourly":
        df_ts = df_country.set_index('Timestamp').resample('H').mean().reset_index()
    elif resample_period == "Daily":
        df_ts = df_country.set_index('Timestamp').resample('D').mean().reset_index()
    elif resample_period == "Monthly":
        df_ts = df_country.set_index('Timestamp').resample('M').mean().reset_index()
    else:
        df_ts = df_country
    
    # Plot time series
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df_ts['Timestamp'], df_ts[metric_ts], alpha=0.7, linewidth=1)
    ax.set_title(f'{metric_ts} Over Time - {country_ts}', fontsize=14, fontweight='bold')
    ax.set_ylabel(f'{metric_ts} ({get_metric_unit(metric_ts)})')
    ax.set_xlabel('Date')
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    st.pyplot(fig)

def show_weather_correlations(df_all):
    st.header("🌡️ Weather Correlations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        x_metric = st.selectbox(
            "X-Axis Metric",
            ["Tamb", "WS", "RH", "GHI"],
            index=0
        )
    
    with col2:
        y_metric = st.selectbox(
            "Y-Axis Metric", 
            ["GHI", "DNI", "DHI", "Tamb", "WS"],
            index=0
        )
    
    # Create scatter plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    colors = {'Benin': 'red', 'Sierra Leone': 'blue', 'Togo': 'green'}
    
    for country in df_all['Country'].unique():
        country_data = df_all[df_all['Country'] == country]
        ax.scatter(
            country_data[x_metric], 
            country_data[y_metric],
            alpha=0.5, 
            label=country,
            color=colors.get(country, 'gray'),
            s=10
        )
    
    ax.set_xlabel(f'{x_metric} ({get_metric_unit(x_metric)})')
    ax.set_ylabel(f'{y_metric} ({get_metric_unit(y_metric)})')
    ax.set_title(f'{y_metric} vs {x_metric} by Country', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    st.pyplot(fig)
    
    # Correlation matrix
    st.subheader("Correlation Matrix")
    numeric_cols = df_all.select_dtypes(include=[np.number]).columns
    corr_matrix = df_all[numeric_cols].corr()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, ax=ax)
    st.pyplot(fig)

def show_regional_rankings(df_all):
    st.header("🏆 Regional Rankings")
    
    ranking_metric = st.selectbox(
        "Ranking Metric",
        ["GHI", "DNI", "DHI", "Tamb", "WS"],
        index=0
    )
    
    # Calculate rankings
    rankings = df_all.groupby('Country')[ranking_metric].agg([
        ('Average', 'mean'),
        ('Median', 'median'),
        ('Stability', lambda x: 1/x.std()),  # Inverse of std for stability score
        ('Records', 'count')
    ]).round(2)
    
    rankings['Stability Rank'] = rankings['Stability'].rank(ascending=False)
    rankings['Potential Rank'] = rankings['Average'].rank(ascending=False)
    rankings['Overall Score'] = (rankings['Potential Rank'] + rankings['Stability Rank']) / 2
    
    # Display rankings
    st.subheader("Solar Potential Rankings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "🏆 Best Solar Potential",
            rankings.loc[rankings['Potential Rank'].idxmin()].name,
            f"Avg {ranking_metric}: {rankings['Average'].max():.1f} {get_metric_unit(ranking_metric)}"
        )
    
    with col2:
        st.metric(
            "📊 Most Stable",
            rankings.loc[rankings['Stability Rank'].idxmin()].name,
            f"Stability Score: {rankings['Stability'].max():.2f}"
        )
    
    # Rankings table
    st.subheader("Detailed Rankings")
    display_rankings = rankings[['Average', 'Median', 'Stability', 'Records', 'Overall Score']]
    display_rankings['Overall Score'] = display_rankings['Overall Score'].round(2)
    st.dataframe(display_rankings.style.background_gradient(cmap='Blues'))
    
    # Recommendation
    best_country = rankings.loc[rankings['Overall Score'].idxmin()].name
    st.success(
        f"💡 **Recommendation**: Based on {ranking_metric} data, **{best_country}** shows the best "
        f"combination of high solar potential and stability for solar farm development."
    )

def get_metric_unit(metric):
    """Get unit for metric display"""
    units = {
        'GHI': 'W/m²', 'DNI': 'W/m²', 'DHI': 'W/m²',
        'Tamb': '°C', 'WS': 'm/s', 'RH': '%'
    }
    return units.get(metric, '')

if __name__ == "__main__":
    main()