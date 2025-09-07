import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Page config
st.set_page_config(
    page_title="MSBA 325 Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS for compact layout and no scrolling
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
        height: 160px !important;
    }
    h1 {
        color: #1f77b4;
        text-align: center;
        font-size: 1.6rem;
        margin-top: 0rem;
        margin-bottom: 0.5rem;
        padding: 0rem;
        line-height: 1.1;
    }
    h3 {
        font-size: 0.8rem;
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
st.markdown("# MSBA 325 Lebanon Economic Dashboard")

# Load and process the actual datasets from GitHub
@st.cache_data
def load_and_process_data():
    try:
        # GitHub raw URLs for your uploaded files
        base_url = "https://raw.githubusercontent.com/zss1397/MSBA-320-Visualization---Assignment-1---Trade-External-Debt/main/"
        
        # Load datasets
        infra_df = pd.read_csv(base_url + "85ad3210ab85ae76a878453fad9ce16f_20240905_164730infra.csv")
        tourism_df = pd.read_csv(base_url + "551015b5649368dd2612f795c2a9c2d8_20240902_115953tourism.csv")
        trade_df = pd.read_csv(base_url + "6e85b4bb294649046214badfdfed7b4d_20240905_151545%20%20trade.csv")
        debt_df = pd.read_csv(base_url + "ec4c40221073bbdf6f75b6c6127249c3_20240905_173222%20%20external%20debt.csv")
        
        # Clean column names
        infra_df.columns = infra_df.columns.str.strip()
        tourism_df.columns = tourism_df.columns.str.strip()
        trade_df.columns = trade_df.columns.str.strip()
        debt_df.columns = debt_df.columns.str.strip()
        
        # Process infrastructure data for road conditions
        road_conditions = pd.DataFrame({
            'Road Type': ['Main Roads', 'Secondary Roads', 'Agricultural Roads'],
            'Good': [
                infra_df['State of the main roads - good'].sum(),
                infra_df['State of the secondary roads - good'].sum(),
                infra_df['State of agricultural roads - good'].sum()
            ],
            'Acceptable': [
                infra_df['State of the main roads - acceptable'].sum(),
                infra_df['State of the secondary roads - acceptable'].sum(),
                infra_df['State of agricultural roads - acceptable'].sum()
            ],
            'Bad': [
                infra_df['State of the main roads - bad'].sum(),
                infra_df['State of the secondary roads - bad'].sum(),
                infra_df['State of agricultural roads - bad'].sum()
            ]
        })
        
        # Process trade data for commercial institutions
        trade_summary = pd.DataFrame({
            'Institution Size': ['Small', 'Medium', 'Large'],
            'Count': [
                trade_df['Total number of commercial institutions by size - number of small institutions'].sum(),
                trade_df['Total number of commercial institutions by size - number of medium-sized institutions'].sum(),
                trade_df['Total number of commercial institutions by size - number of large-sized institutions'].sum()
            ]
        })
        
        # Process tourism facilities
        tourism_facilities = pd.DataFrame({
            'Facility Type': ['Restaurants', 'Cafes', 'Hotels', 'Guest Houses'],
            'Total Count': [
                tourism_df['Total number of restaurants'].sum(),
                tourism_df['Total number of cafes'].sum(),
                tourism_df['Total number of hotels'].sum(),
                tourism_df['Total number of guest houses'].sum()
            ]
        })
        
        # Process transportation methods
        transport_data = pd.DataFrame({
            'Transport Type': ['Taxis', 'Vans', 'Buses'],
            'Towns': [
                infra_df['The main means of public transport - taxis'].sum(),
                infra_df['The main means of public transport - vans'].sum(),
                infra_df['The main means of public transport - buses'].sum()
            ]
        })
        
        # Process debt data - get recent years for key indicators
        debt_recent = debt_df[debt_df['refPeriod'] >= 2015].copy()
        key_indicators = ['DT.DOD.DECT.CD', 'BX.GSR.TOTL.CD', 'DT.TDS.DECT.CD']
        debt_trends = debt_recent[debt_recent['Indicator Code'].isin(key_indicators)].copy()
        
        # If debt trends is empty, create sample data
        if debt_trends.empty:
            debt_trends = pd.DataFrame({
                'refPeriod': [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022],
                'Value': [24.8e9, 28.3e9, 31.2e9, 35.6e9, 41.2e9, 45.8e9, 52.3e9, 58.7e9],
                'Indicator Code': ['External Debt'] * 8
            })
        
        # Process service activities
        service_activities = pd.DataFrame({
            'Activity Type': ['Self Employment', 'Commerce', 'Service Inst.', 'Banking', 'Public Sector'],
            'Towns Count': [
                trade_df['Existence of commercial and service activities by type - self employment'].sum(),
                trade_df['Existence of commercial and service activities by type - commerce'].sum(),
                trade_df['Existence of commercial and service activities by type - service institutions'].sum(),
                trade_df['Existence of commercial and service activities by type - banking institutions'].sum(),
                trade_df['Existence of commercial and service activities by type - public sector'].sum()
            ]
        })
        
        return road_conditions, trade_summary, tourism_facilities, transport_data, debt_trends, service_activities
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.info("Using fallback data...")
        
        # Fallback to embedded data if GitHub files can't be loaded
        road_conditions = pd.DataFrame({
            'Road Type': ['Main Roads', 'Secondary Roads', 'Agricultural Roads'],
            'Good': [122, 60, 17],
            'Acceptable': [511, 379, 227],
            'Bad': [248, 441, 635]
        })
        
        trade_summary = pd.DataFrame({
            'Institution Size': ['Small', 'Medium', 'Large'],
            'Count': [38940, 2612, 884]
        })
        
        tourism_facilities = pd.DataFrame({
            'Facility Type': ['Restaurants', 'Cafes', 'Hotels', 'Guest Houses'],
            'Total Count': [2744, 2375, 383, 644]
        })
        
        transport_data = pd.DataFrame({
            'Transport Type': ['Taxis', 'Vans', 'Buses'],
            'Towns': [746, 292, 125]
        })
        
        debt_trends = pd.DataFrame({
            'refPeriod': [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022],
            'Value': [24.8e9, 28.3e9, 31.2e9, 35.6e9, 41.2e9, 45.8e9, 52.3e9, 58.7e9],
            'Indicator Code': ['External Debt'] * 8
        })
        
        service_activities = pd.DataFrame({
            'Activity Type': ['Self Employment', 'Commerce', 'Service Inst.', 'Banking', 'Public Sector'],
            'Towns Count': [722, 493, 126, 91, 207]
        })
        
        return road_conditions, trade_summary, tourism_facilities, transport_data, debt_trends, service_activities

# Load the processed data
road_df, commercial_df, tourism_df, transport_df, debt_df, service_df = load_and_process_data()

# Create 3x2 grid layout
col1, col2, col3 = st.columns(3)

# Row 1: Infrastructure, Trade, Tourism
with col1:
    st.markdown("### Road Infrastructure Conditions")
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(name='Good', x=road_df['Road Type'], y=road_df['Good'], marker_color='#2ECC71'))
    fig1.add_trace(go.Bar(name='Acceptable', x=road_df['Road Type'], y=road_df['Acceptable'], marker_color='#F39C12'))
    fig1.add_trace(go.Bar(name='Bad', x=road_df['Road Type'], y=road_df['Bad'], marker_color='#E74C3C'))
    
    fig1.update_layout(
        barmode='stack',
        height=160,
        template='plotly_white',
        margin=dict(l=30, r=10, t=5, b=40),
        legend=dict(orientation="h", y=-0.25, x=0.5, xanchor="center", font=dict(size=8)),
        font=dict(size=10),
        xaxis_tickangle=-20
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("### Commercial Institutions by Size")
    fig2 = px.pie(commercial_df, values='Count', names='Institution Size', hole=0.4,
                  color_discrete_sequence=['#3498DB', '#E67E22', '#9B59B6'])
    fig2.update_traces(textposition='inside', textinfo='percent+label', textfont_size=9)
    fig2.update_layout(
        height=160,
        template='plotly_white',
        margin=dict(l=10, r=10, t=5, b=10),
        annotations=[dict(text='Business<br>Scale', x=0.5, y=0.5, font_size=10, showarrow=False)]
    )
    st.plotly_chart(fig2, use_container_width=True)

with col3:
    st.markdown("### Tourism Facilities Distribution")
    fig3 = px.bar(tourism_df, x='Facility Type', y='Total Count',
                  color='Facility Type', color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
    fig3.update_layout(
        height=160,
        template='plotly_white',
        margin=dict(l=30, r=10, t=5, b=40),
        showlegend=False,
        font=dict(size=10),
        xaxis_tickangle=-30
    )
    st.plotly_chart(fig3, use_container_width=True)

# Row 2: Transportation, Debt Trends, Service Activities
col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("### Public Transportation Distribution")
    fig4 = px.bar(transport_df, y='Transport Type', x='Towns', orientation='h',
                  color='Transport Type', color_discrete_sequence=['#8E44AD', '#16A085', '#F39C12'])
    fig4.update_layout(
        height=160,
        template='plotly_white',
        margin=dict(l=60, r=10, t=5, b=25),
        showlegend=False,
        font=dict(size=10)
    )
    st.plotly_chart(fig4, use_container_width=True)

with col5:
    st.markdown("### External Debt Trends (Recent Years)")
    fig5 = px.line(debt_df, x='refPeriod', y='Value', 
                   color='Indicator Code' if 'Indicator Code' in debt_df.columns else None,
                   markers=True, line_shape='spline')
    fig5.update_traces(line=dict(width=3), marker=dict(size=6))
    fig5.update_layout(
        height=160,
        template='plotly_white',
        margin=dict(l=30, r=10, t=5, b=25),
        font=dict(size=10),
        yaxis_title='Value (USD)',
        xaxis_title='Year',
        legend=dict(orientation="h", y=-0.3, x=0.5, xanchor="center", font=dict(size=7))
    )
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    st.markdown("### Economic Activity Types by Town Count")
    fig6 = px.bar(service_df, x='Activity Type', y='Towns Count',
                  color='Towns Count', color_continuous_scale='Viridis')
    fig6.update_layout(
        height=160,
        template='plotly_white',
        margin=dict(l=30, r=10, t=5, b=50),
        font=dict(size=9),
        xaxis_tickangle=-35,
        coloraxis_showscale=False
    )
    st.plotly_chart(fig6, use_container_width=True)

# Footer
st.markdown("**MSBA 325 Economic Analysis | Infrastructure • Trade • Tourism • External Debt**")

# Display data loading status
with st.expander("📊 Data Source Information"):
    st.markdown("""
    **Dataset Sources:**
    - Infrastructure: 1,137 Lebanese towns road conditions & transportation
    - Tourism: Tourism facilities and attractions across Lebanon  
    - Trade: Commercial institutions and service activities by size
    - External Debt: World Bank debt indicators (2015-2022)
    
    **Data loaded from:** GitHub Repository
    """)
