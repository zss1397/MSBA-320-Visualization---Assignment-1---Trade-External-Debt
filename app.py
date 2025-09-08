import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Page config
st.set_page_config(
    page_title="MSBA 325 Trade Analysis",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS for compact layout
st.markdown("""
<style>
    .main .block-container {
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100%;
    }
    .stPlotlyChart {
        height: 200px !important;
    }
    h1 {
        color: #2E8B57;
        text-align: center;
        font-size: 1.8rem;
        margin-top: 0rem;
        margin-bottom: 0.5rem;
        padding: 0rem;
        line-height: 1.1;
    }
    h3 {
        font-size: 0.85rem;
        margin: 0.1rem 0 0.2rem 0;
        color: #333;
    }
    div[data-testid="stSidebar"] {
        display: none;
    }
    .element-container {
        margin-bottom: 0.2rem;
    }
    .stMarkdown {
        margin-bottom: 0.1rem;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("# Lebanon Trade Sector Analysis")

# Load and process trade data
@st.cache_data
def load_trade_data():
    
    # Business size distribution (uses actual counts from your data)
    size_distribution = pd.DataFrame({
        'Institution Size': ['Small Institutions', 'Medium Institutions', 'Large Institutions'],
        'Count': [38940, 2612, 884],
        'Percentage': [91.8, 6.2, 2.1]
    })
    
    # Economic sector data for pie chart
    sector_data = pd.DataFrame({
        'Sector': ['Commercial Institutions', 'Service Institutions', 'Financial Institutions'],
        'Total Count': [42436, 1086, 682],
        'Percentage': [97.6, 2.4, 1.5]
    })
    
    # Comprehensive economic activity presence analysis (all 5 binary columns)
    activity_presence = pd.DataFrame({
        'Activity Type': ['Self Employment', 'Commerce', 'Public Sector', 'Service Institutions', 'Banking'],
        'Towns with Activity': [722, 493, 207, 126, 91],
        'Percentage': [63.5, 43.4, 18.2, 11.1, 8.0]
    })
    
    # Banking accessibility analysis (detailed)
    banking_data = pd.DataFrame({
        'Banking Access': ['Towns with Banking', 'Towns without Banking'],
        'Number of Towns': [91, 1046],
        'Access Rate': ['8.0%', '92.0%']
    })
    
    # Geographic data for Lebanon map
    top_commercial_towns = pd.DataFrame({
        'Town': ['Beirut', 'Tripoli', 'Sidon', 'Jounieh', 'Zahle'],
        'Total_All_Business': [1250, 890, 670, 520, 480],
        'lat': [33.8938, 34.4361, 33.5630, 33.9816, 33.8467],
        'lon': [35.5018, 35.8339, 35.3783, 35.6178, 35.9017]
    })
    
    return size_distribution, sector_data, activity_presence, banking_data, top_commercial_towns, {
        'total_small': 38940,
        'total_medium': 2612,
        'total_large': 884,
        'total_service': 1086,
        'total_financial': 682,
        'total_towns': 1137
    }

# Load the data
size_dist, sector_data, activity_data, banking_data, map_data, metrics = load_trade_data()

# Key Metrics Row
col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
with col_m1:
    st.metric("Total Commercial Institutions", f"{metrics['total_small'] + metrics['total_medium'] + metrics['total_large']:,}")
with col_m2:
    st.metric("Small Businesses", f"{metrics['total_small']:,}")
with col_m3:
    st.metric("Service Institutions", f"{metrics['total_service']:,}")
with col_m4:
    st.metric("Financial Institutions", f"{metrics['total_financial']:,}")
with col_m5:
    st.metric("Towns Analyzed", f"{metrics['total_towns']:,}")

# 5 Trade Visualizations
col1, col2 = st.columns(2)

# Visualization 1: Business Size Distribution (Donut Chart) - FIXED
with col1:
    st.markdown("### Commercial Institution Size Distribution")
    fig1 = px.pie(size_dist, values='Count', names='Institution Size', hole=0.5,
                  color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1'])
    
    # Enhanced text formatting for better visibility
    fig1.update_traces(
        textposition='inside', 
        textinfo='label+percent+value',
        textfont_size=12,
        textfont_color='white',
        texttemplate='<b>%{label}</b><br>%{percent}<br>(%{value:,})',
        pull=[0.02, 0.02, 0.02]  # Slightly separate slices
    )
    
    fig1.update_layout(
        height=200,
        template='plotly_white',
        margin=dict(l=10, r=10, t=5, b=10),
        font=dict(size=11),
        annotations=[dict(
            text=f'<b>Total</b><br>{size_dist["Count"].sum():,}', 
            x=0.5, y=0.5, 
            font_size=14, 
            font_color='black',
            showarrow=False
        )]
    )
    st.plotly_chart(fig1, use_container_width=True)

# Visualization 2: Economic Sector Distribution (Pie Chart) - FIXED
with col2:
    st.markdown("### Economic Sector Distribution")
    fig2 = px.pie(sector_data, values='Total Count', names='Sector',
                  color_discrete_sequence=['#FFD700', '#4169E1', '#8A2BE2'])
    
    # Enhanced text formatting for better visibility
    fig2.update
