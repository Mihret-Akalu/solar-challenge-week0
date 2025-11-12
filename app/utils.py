"""
Utility functions for the Solar Data Discovery Dashboard
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import os

def load_data():
    """
    Load all cleaned country datasets and combine them
    """
    try:
        data_dir = Path(__file__).parent.parent / "data"
        
        # Define file paths
        file_paths = {
            'Benin': data_dir / 'benin_clean.csv',
            'Sierra Leone': data_dir / 'sierraleone_clean.csv',
            'Togo': data_dir / 'togo_clean.csv'
        }
        
        dataframes = []
        
        for country, file_path in file_paths.items():
            if file_path.exists():
                df = pd.read_csv(file_path)
                df['Country'] = country
                dataframes.append(df)
            else:
                print(f"Warning: {file_path} not found")
        
        if not dataframes:
            return None
            
        # Combine all data
        df_all = pd.concat(dataframes, ignore_index=True)
        return df_all
        
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def create_comparison_plot(df, metric, plot_type="Box Plot"):
    """
    Create comparison plots using Plotly
    """
    if plot_type == "Box Plot":
        fig = px.box(df, x='Country', y=metric, color='Country',
                     title=f'{metric} Distribution by Country',
                     labels={metric: f'{metric} (W/m²)', 'Country': ''})
        
    elif plot_type == "Violin Plot":
        fig = px.violin(df, x='Country', y=metric, color='Country',
                        title=f'{metric} Distribution by Country',
                        labels={metric: f'{metric} (W/m²)', 'Country': ''})
        
    elif plot_type == "Bar Chart":
        avg_data = df.groupby('Country')[metric].mean().reset_index()
        fig = px.bar(avg_data, x='Country', y=metric, color='Country',
                     title=f'Average {metric} by Country',
                     labels={metric: f'Average {metric} (W/m²)', 'Country': ''})
    
    # Update layout
    fig.update_layout(
        showlegend=False,
        plot_bgcolor='white',
        font=dict(size=12)
    )
    
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text=f'{metric} (W/m²)')
    
    return fig

def calculate_metrics(df, metric):
    """
    Calculate summary metrics for a given metric
    """
    return {
        'mean': df[metric].mean(),
        'median': df[metric].median(),
        'std': df[metric].std(),
        'count': len(df)
    }

def get_country_summary(df, country):
    """
    Get summary statistics for a specific country
    """
    country_data = df[df['Country'] == country]
    
    summary = {
        'country': country,
        'records': len(country_data),
        'metrics': {}
    }
    
    solar_metrics = ['GHI', 'DNI', 'DHI']
    for metric in solar_metrics:
        if metric in country_data.columns:
            summary['metrics'][metric] = calculate_metrics(country_data, metric)
    
    return summary