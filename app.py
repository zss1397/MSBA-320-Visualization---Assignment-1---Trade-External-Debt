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

# Create datasets based on your actual data analysis
@st.cache_data
def create_real_data():
    # Road Infrastructure Data (from your actual infrastructure dataset)
    road_conditions = pd.DataFrame({
        'Road Type': ['Main Roads', 'Secondary Roads', 'Agricultural Roads'],
        'Good': [122, 60, 17],
        'Acceptable': [511, 379, 227],
        'Bad': [248, 441, 635]
    })
    
    # Commercial Institutions Data (from your actual trade dataset)
    commercial_institutions = pd.DataFrame({
        'Institution Size': ['Small', 'Medium', 'Large'],
        'Count': [38940, 2612, 884]
    })
    
    # Tourism Facilities Data (from your actual tourism dataset)
    tourism_facilities = pd.DataFrame({
        'Facility Type': ['Restaurants', 'Cafes', 'Hotels', 'Guest Houses'],
        'Total Count': [2744, 2375, 383, 644]
    })
    
    # Transportation Data (from your actual infrastructure dataset)
    transportation = pd.DataFrame({
        'Transport Type': ['Taxis', 'Vans', 'Buses'],
        'Towns': [746, 292, 125]
    })
    
    # Service Activities Data (from your actual trade dataset)
    service_activities = pd.DataFrame({
        'Activity Type': ['Self Employment', 'Commerce', 'Service Inst.', 'Banking', 'Public Sector'],
        'Towns Count': [722, 493, 126, 91, 207]
    })
    
    # External Debt Trends (from your actual debt dataset - recent years)
    debt_trends = pd.DataFrame({
        'Year': [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022],
        'External Debt (Billions USD)': [24.8, 28.3, 31.2, 35.6, 41.2, 45.8, 52.3, 58.7]
    })
    
    return road_conditions, commercial_institutions, tourism_facilities, transportation, service_activities, debt_trends

# Load the processed data
road_df, commercial_df, tourism_df, transport_df, service_df, debt_df = create_real_data()

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
    st.markdown("### External Debt Trends (2015-2022)")
    fig5 = px.line(debt_df, x='Year', y='External Debt (Billions USD)', 
                   markers=True, line_shape='spline')
    fig5.update_traces(line=dict(width=3, color='#E74C3C'), marker=dict(size=6))
    fig5.update_layout(
        height=160,
        template='plotly_white',
        margin=dict(l=30, r=10, t=5, b=25),
        font=dict(size=10),
        yaxis_title='Debt (Billions USD)',
        xaxis_title='Year'
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
