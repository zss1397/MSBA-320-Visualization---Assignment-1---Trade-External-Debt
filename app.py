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
        height: 180px !important;
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
    .metric-container {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        border-radius: 8px;
        padding: 0.5rem;
        margin-bottom: 0.5rem;
        border: 1px solid #e0e0e0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("# MSBA 325 Trade Data Deep Dive")

# Load and process trade data
@st.cache_data
def load_trade_data():
    try:
        # Load trade dataset from GitHub
        trade_df = pd.read_csv("https://raw.githubusercontent.com/zss1397/MSBA-320-Visualization---Assignment-1---Trade-External-Debt/main/6e85b4bb294649046214badfdfed7b4d_20240905_151545%20%20trade.csv")
        trade_df.columns = trade_df.columns.str.strip()
        
        # Calculate key metrics
        total_small = trade_df['Total number of commercial institutions by size - number of small institutions'].sum()
        total_medium = trade_df['Total number of commercial institutions by size - number of medium-sized institutions'].sum()
        total_large = trade_df['Total number of commercial institutions by size - number of large-sized institutions'].sum()
        total_service = trade_df['Total number of service institutions '].sum()
        total_financial = trade_df['Total number of non banking financial institutions '].sum()
        
        # Business size distribution
        size_distribution = pd.DataFrame({
            'Institution Size': ['Small Institutions', 'Medium Institutions', 'Large Institutions'],
            'Count': [total_small, total_medium, total_large],
            'Percentage': [
                (total_small / (total_small + total_medium + total_large)) * 100,
                (total_medium / (total_small + total_medium + total_large)) * 100,
                (total_large / (total_small + total_medium + total_large)) * 100
            ]
        })
        
        # Activity type distribution by town count
        activity_distribution = pd.DataFrame({
            'Activity Type': ['Self Employment', 'Commerce', 'Service Institutions', 'Banking', 'Public Sector'],
            'Towns Count': [
                trade_df['Existence of commercial and service activities by type - self employment'].sum(),
                trade_df['Existence of commercial and service activities by type - commerce'].sum(),
                trade_df['Existence of commercial and service activities by type - service institutions'].sum(),
                trade_df['Existence of commercial and service activities by type - banking institutions'].sum(),
                trade_df['Existence of commercial and service activities by type - public sector'].sum()
            ]
        })
        
        # Small vs Medium Enterprise percentage analysis
        trade_df['SME_Percentage'] = trade_df['Percentage of small and medium sized commercial institutions'].fillna(0)
        sme_ranges = pd.DataFrame({
            'SME Range': ['0-25%', '26-50%', '51-75%', '76-100%'],
            'Towns Count': [
                ((trade_df['SME_Percentage'] >= 0) & (trade_df['SME_Percentage'] <= 25)).sum(),
                ((trade_df['SME_Percentage'] > 25) & (trade_df['SME_Percentage'] <= 50)).sum(),
                ((trade_df['SME_Percentage'] > 50) & (trade_df['SME_Percentage'] <= 75)).sum(),
                ((trade_df['SME_Percentage'] > 75) & (trade_df['SME_Percentage'] <= 100)).sum()
            ]
        })
        
        # Institution density by governorate
        trade_df['Governorate'] = trade_df['refArea'].str.extract(r'/([^/]+)_Governorate')
        gov_analysis = trade_df.groupby('Governorate').agg({
            'Total number of commercial institutions by size - number of small institutions': 'sum',
            'Total number of commercial institutions by size - number of medium-sized institutions': 'sum',
            'Total number of commercial institutions by size - number of large-sized institutions': 'sum',
            'Total number of service institutions ': 'sum',
            'Total number of non banking financial institutions ': 'sum'
        }).fillna(0)
        
        gov_analysis['Total_Commercial'] = (
            gov_analysis['Total number of commercial institutions by size - number of small institutions'] +
            gov_analysis['Total number of commercial institutions by size - number of medium-sized institutions'] +
            gov_analysis['Total number of commercial institutions by size - number of large-sized institutions']
        )
        
        gov_analysis = gov_analysis.reset_index()
        gov_analysis = gov_analysis[gov_analysis['Governorate'].notna()]
        
        # Service vs Financial institutions comparison
        service_financial = pd.DataFrame({
            'Institution Type': ['Service Institutions', 'Non-Banking Financial'],
            'Total Count': [total_service, total_financial],
            'Average per Town': [
                total_service / len(trade_df) if len(trade_df) > 0 else 0,
                total_financial / len(trade_df) if len(trade_df) > 0 else 0
            ]
        })
        
        st.success("Trade data loaded successfully from GitHub!")
        return size_distribution, activity_distribution, sme_ranges, gov_analysis, service_financial, {
            'total_small': total_small,
            'total_medium': total_medium, 
            'total_large': total_large,
            'total_service': total_service,
            'total_financial': total_financial,
            'total_towns': len(trade_df)
        }
        
    except Exception as e:
        st.error(f"Error loading trade data: {str(e)}")
        st.info("Using sample trade data for demonstration...")
        
        # Fallback sample data
        size_distribution = pd.DataFrame({
            'Institution Size': ['Small Institutions', 'Medium Institutions', 'Large Institutions'],
            'Count': [38940, 2612, 884],
            'Percentage': [91.7, 6.2, 2.1]
        })
        
        activity_distribution = pd.DataFrame({
            'Activity Type': ['Self Employment', 'Commerce', 'Service Institutions', 'Banking', 'Public Sector'],
            'Towns Count': [722, 493, 126, 91, 207]
        })
        
        sme_ranges = pd.DataFrame({
            'SME Range': ['0-25%', '26-50%', '51-75%', '76-100%'],
            'Towns Count': [85, 156, 289, 607]
        })
        
        gov_analysis = pd.DataFrame({
            'Governorate': ['Mount_Lebanon', 'North', 'South', 'Bekaa', 'Nabatieh'],
            'Total_Commercial': [15420, 8930, 7650, 6890, 3546]
        })
        
        service_financial = pd.DataFrame({
            'Institution Type': ['Service Institutions', 'Non-Banking Financial'],
            'Total Count': [1086, 682],
            'Average per Town': [0.96, 0.60]
        })
        
        return size_distribution, activity_distribution, sme_ranges, gov_analysis, service_financial, {
            'total_small': 38940,
            'total_medium': 2612,
            'total_large': 884,
            'total_service': 1086,
            'total_financial': 682,
            'total_towns': 1137
        }

# Load the data
size_dist, activity_dist, sme_ranges, gov_data, service_fin, metrics = load_trade_data()

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

# Visualization 1: Business Size Distribution (Donut Chart)
with col1:
    st.markdown("### Commercial Institution Size Distribution")
    fig1 = px.pie(size_dist, values='Count', names='Institution Size', hole=0.5,
                  color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1'])
    fig1.update_traces(textposition='inside', textinfo='percent+label', textfont_size=10)
    fig1.update_layout(
        height=180,
        template='plotly_white',
        margin=dict(l=10, r=10, t=5, b=10),
        annotations=[dict(text=f'Total<br>{size_dist["Count"].sum():,}', x=0.5, y=0.5, font_size=12, showarrow=False)]
    )
    st.plotly_chart(fig1, use_container_width=True)

# Visualization 2: Activity Type Distribution (Horizontal Bar)
with col2:
    st.markdown("### Business Activity Types Across Towns")
    fig2 = px.bar(activity_dist, y='Activity Type', x='Towns Count', orientation='h',
                  color='Towns Count', color_continuous_scale='Viridis')
    fig2.update_layout(
        height=180,
        template='plotly_white',
        margin=dict(l=80, r=10, t=5, b=25),
        coloraxis_showscale=False,
        font=dict(size=10)
    )
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)

# Visualization 3: SME Percentage Distribution (Bar Chart)
with col3:
    st.markdown("### Small & Medium Enterprise Concentration")
    fig3 = px.bar(sme_ranges, x='SME Range', y='Towns Count',
                  color='Towns Count', color_continuous_scale='RdYlBu_r')
    fig3.update_layout(
        height=180,
        template='plotly_white',
        margin=dict(l=30, r=10, t=5, b=40),
        coloraxis_showscale=False,
        font=dict(size=10),
        xaxis_title='SME Percentage Range',
        yaxis_title='Number of Towns'
    )
    st.plotly_chart(fig3, use_container_width=True)

# Visualization 4: Service vs Financial Institutions (Grouped Bar)
with col4:
    st.markdown("### Service vs Financial Institution Comparison")
    fig4 = go.Figure()
    fig4.add_trace(go.Bar(name='Total Count', x=service_fin['Institution Type'], 
                         y=service_fin['Total Count'], yaxis='y', marker_color='#E67E22'))
    fig4.add_trace(go.Bar(name='Avg per Town', x=service_fin['Institution Type'], 
                         y=service_fin['Average per Town'], yaxis='y2', marker_color='#3498DB'))
    
    fig4.update_layout(
        height=180,
        template='plotly_white',
        margin=dict(l=30, r=30, t=5, b=40),
        yaxis=dict(title='Total Count', side='left'),
        yaxis2=dict(title='Average per Town', side='right', overlaying='y'),
        legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center", font=dict(size=9)),
        font=dict(size=10)
    )
    st.plotly_chart(fig4, use_container_width=True)

# Visualization 5: Commercial Institutions by Governorate (Bubble Chart)
st.markdown("### Commercial Institution Distribution by Governorate")
if not gov_data.empty and 'Total_Commercial' in gov_data.columns:
    fig5 = px.scatter(gov_data, x='Governorate', y='Total_Commercial', 
                     size='Total_Commercial', color='Total_Commercial',
                     color_continuous_scale='plasma', size_max=60)
    fig5.update_traces(marker=dict(opacity=0.7, line=dict(width=2, color='white')))
    fig5.update_layout(
        height=200,
        template='plotly_white',
        margin=dict(l=40, r=10, t=5, b=50),
        font=dict(size=10),
        yaxis_title='Total Commercial Institutions',
        xaxis_tickangle=-30,
        coloraxis_showscale=False
    )
    st.plotly_chart(fig5, use_container_width=True)
else:
    st.info("Governorate data processing - showing overall summary")
    summary_data = pd.DataFrame({
        'Metric': ['Small Institutions', 'Medium Institutions', 'Large Institutions', 'Service Institutions', 'Financial Institutions'],
        'Count': [metrics['total_small'], metrics['total_medium'], metrics['total_large'], metrics['total_service'], metrics['total_financial']]
    })
    fig5 = px.bar(summary_data, x='Metric', y='Count', color='Count', color_continuous_scale='plasma')
    fig5.update_layout(
        height=200,
        template='plotly_white',
        margin=dict(l=40, r=10, t=5, b=50),
        font=dict(size=10),
        xaxis_tickangle=-30,
        coloraxis_showscale=False
    )
    st.plotly_chart(fig5, use_container_width=True)

# Footer with insights
st.markdown("**MSBA 325 Trade Analysis | Commercial Institutions • Service Activities • SME Distribution**")

# Trade insights
with st.expander("📈 Key Trade Insights"):
    col_i1, col_i2 = st.columns(2)
    with col_i1:
        st.markdown("""
        **Business Structure:**
        - Small enterprises dominate (91.7% of all commercial institutions)
        - Self-employment is the most common activity type
        - Service sector shows strong presence across Lebanon
        """)
    with col_i2:
        st.markdown("""
        **Distribution Patterns:**
        - Most towns have high SME concentration (76-100%)
        - Banking institutions present in fewer towns (selective distribution)
        - Public sector activities span multiple regions
        """)
