import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Set page config
st.set_page_config(
    page_title="MSBA 325 Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ultra-compact CSS
st.markdown("""
<style>
    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        max-width: 100%;
    }
    .stPlotlyChart {
        height: 110px !important;
    }
    h1 {
        color: #1f77b4;
        text-align: center;
        font-size: 1.3rem;
        margin: 0rem;
        padding: 0rem;
    }
    h4 {
        font-size: 0.7rem;
        margin: 0rem;
        padding: 0rem;
    }
    .element-container {
        margin: 0rem;
    }
    div[data-testid="stSidebar"] {
        display: none;
    }
    .stMarkdown {
        margin: 0rem;
    }
    .stMetric {
        height: 40px;
    }
    .stColumns {
        gap: 0.3rem;
    }
</style>
""", unsafe_allow_html=True)

# Minimal title
st.title("MSBA 325 Economic Data Dashboard")

# Create sample data
@st.cache_data
def create_sample_data():
    towns = ['Beirut', 'Tripoli', 'Sidon', 'Tyre']
    regions = ['Aley District', 'Zahle District', 'Matn District', 'Baabda District']
    
    trade_data = []
    for town in towns:
        trade_data.append({
            'Town': town,
            'Total number of commercial institutions by size - number of small institutions': np.random.randint(20, 80),
            'Total number of commercial institutions by size - number of medium-sized institutions': np.random.randint(5, 25),
            'Total number of commercial institutions by size - number of large-sized institutions': np.random.randint(1, 8),
            'refArea': np.random.choice(regions),
            'Total number of service institutions': np.random.randint(10, 40),
            'Total number of non banking financial institutions': np.random.randint(5, 20),
            'Existence of commercial and service activities by type - self employment': np.random.randint(15, 50),
            'Existence of commercial and service activities by type - public sector': np.random.randint(5, 20),
            'Existence of commercial and service activities by type - banking institutions': np.random.randint(2, 12),
            'Existence of commercial and service activities by type - service institutions': np.random.randint(10, 35),
            'Existence of commercial and service activities by type - commerce': np.random.randint(20, 60)
        })
    
    trade_df = pd.DataFrame(trade_data)
    
    debt_data = []
    years = list(range(2018, 2024))
    countries = ['Lebanon', 'Jordan', 'Syria']
    
    for country in countries:
        base_debt = np.random.uniform(30000000000, 70000000000)
        for year in years:
            trend_factor = (year - 2018) * 0.1
            debt_value = base_debt * (1 + trend_factor + np.random.uniform(-0.1, 0.1))
            debt_data.append({
                'refArea': country,
                'refPeriod': year,
                'Value': debt_value
            })
    
    debt_df = pd.DataFrame(debt_data)
    return trade_df, debt_df

trade_df, debt_df = create_sample_data()

# Ultra-compact metrics
col_a, col_b, col_c, col_d = st.columns(4)
with col_a:
    st.metric("Towns", len(trade_df))
with col_b:
    st.metric("Regions", trade_df['refArea'].nunique())
with col_c:
    st.metric("Records", len(debt_df))
with col_d:
    st.metric("Years", f"{debt_df['refPeriod'].min()}-{debt_df['refPeriod'].max()}")

# Row 1: Charts 1 & 2
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 1️⃣ Commercial Institutions")
    
    inst_data = trade_df.groupby('Town').agg({
        'Total number of commercial institutions by size - number of small institutions': 'sum',
        'Total number of commercial institutions by size - number of medium-sized institutions': 'sum',
        'Total number of commercial institutions by size - number of large-sized institutions': 'sum'
    }).reset_index()
    inst_data.columns = ['Town', 'Small', 'Medium', 'Large']
    
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(name='Small', x=inst_data['Town'], y=inst_data['Small'], marker_color='lightblue'))
    fig1.add_trace(go.Bar(name='Medium', x=inst_data['Town'], y=inst_data['Medium'], marker_color='orange'))
    fig1.add_trace(go.Bar(name='Large', x=inst_data['Town'], y=inst_data['Large'], marker_color='darkred'))
    
    fig1.update_layout(
        barmode='stack', height=110, template='plotly_white',
        margin=dict(l=0, r=0, t=0, b=20), showlegend=False, xaxis_tickangle=-45
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("#### 2️⃣ External Debt Trends")
    
    debt_trends = debt_df.groupby('refPeriod')['Value'].mean().reset_index()
    
    fig2 = px.line(debt_trends, x='refPeriod', y='Value')
    fig2.update_traces(line=dict(width=3, color='#2E86C1'))
    fig2.update_layout(
        height=110, template='plotly_white',
        margin=dict(l=0, r=0, t=0, b=0), showlegend=False
    )
    st.plotly_chart(fig2, use_container_width=True)

# Row 2: Charts 3 & 4
col3, col4 = st.columns(2)

with col3:
    st.markdown("#### 3️⃣ Business Activity")
    
    activity_totals = {
        'Self Employment': trade_df['Existence of commercial and service activities by type - self employment'].sum(),
        'Public': trade_df['Existence of commercial and service activities by type - public sector'].sum(),
        'Banking': trade_df['Existence of commercial and service activities by type - banking institutions'].sum(),
        'Service': trade_df['Existence of commercial and service activities by type - service institutions'].sum(),
        'Commerce': trade_df['Existence of commercial and service activities by type - commerce'].sum()
    }
    
    fig3 = px.pie(values=list(activity_totals.values()), names=list(activity_totals.keys()))
    fig3.update_traces(textposition='inside', textinfo='percent')
    fig3.update_layout(
        height=110, template='plotly_white',
        margin=dict(l=0, r=0, t=0, b=0), showlegend=False
    )
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.markdown("#### 4️⃣ Debt by Country")
    
    debt_scatter = debt_df.copy()
    debt_scatter['Size_Value'] = debt_scatter['Value'].abs()
    
    fig4 = px.scatter(debt_scatter, x='refPeriod', y='Value', color='refArea', size='Size_Value')
    fig4.update_layout(
        height=110, template='plotly_white',
        margin=dict(l=0, r=0, t=0, b=0), showlegend=False
    )
    st.plotly_chart(fig4, use_container_width=True)

# Row 3: Chart 5 (full width)
st.markdown("#### 5️⃣ District Business Activities")

comp_data = trade_df.groupby('refArea').agg({
    'Total number of service institutions': 'sum',
    'Total number of non banking financial institutions': 'sum',
    'Existence of commercial and service activities by type - self employment': 'sum',
    'Existence of commercial and service activities by type - commerce': 'sum'
}).reset_index()

comp_data.columns = ['Region', 'Service', 'Financial', 'Self Employment', 'Commerce']

fig5 = go.Figure()
fig5.add_trace(go.Bar(name='Service', x=comp_data['Region'], y=comp_data['Service'], marker_color='#1f77b4'))
fig5.add_trace(go.Bar(name='Financial', x=comp_data['Region'], y=comp_data['Financial'], marker_color='#ff7f0e'))
fig5.add_trace(go.Bar(name='Self Employment', x=comp_data['Region'], y=comp_data['Self Employment'], marker_color='#2ca02c'))
fig5.add_trace(go.Bar(name='Commerce', x=comp_data['Region'], y=comp_data['Commerce'], marker_color='#d62728'))

fig5.update_layout(
    barmode='group', height=110, template='plotly_white',
    margin=dict(l=0, r=0, t=0, b=20), showlegend=False, xaxis_tickangle=-30
)

st.plotly_chart(fig5, use_container_width=True)

# Minimal footer
st.markdown("**MSBA 325 Plotly Practice | Streamlit Dashboard**")
