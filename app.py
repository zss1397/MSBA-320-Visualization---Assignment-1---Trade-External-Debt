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

# Ultra-minimal CSS for single row layout
st.markdown("""
<style>
    .main .block-container {
        padding: 0.1rem 0.5rem;
        max-width: 100%;
    }
    .stPlotlyChart {
        height: 300px !important;
    }
    h1 {
        color: #1f77b4;
        text-align: center;
        font-size: 1.2rem;
        margin: 0;
        padding: 0;
    }
    h3 {
        font-size: 0.7rem;
        margin: 0.1rem 0;
        color: #333;
    }
    div[data-testid="stSidebar"] {
        display: none;
    }
    .stMetric {
        text-align: center;
        padding: 0;
        margin: 0;
    }
    .stMetric > div {
        padding: 0.1rem;
    }
    .stMetric > div > div {
        font-size: 0.6rem !important;
    }
    .stMetric > div > div > div {
        font-size: 0.9rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Minimal title
st.markdown("# MSBA 325 Economic Dashboard")

# Create data
@st.cache_data
def create_data():
    towns = ['Beirut', 'Tripoli', 'Sidon', 'Tyre']
    districts = ['Aley', 'Zahle', 'Matn', 'Baabda']
    
    trade_data = []
    for i, town in enumerate(towns):
        trade_data.append({
            'Town': town,
            'Small': np.random.randint(25, 50),
            'Medium': np.random.randint(8, 15),
            'Large': np.random.randint(2, 6),
            'District': districts[i],
            'Service': np.random.randint(12, 28),
            'Financial': np.random.randint(6, 15),
            'Self_Employment': np.random.randint(18, 40),
            'Commerce': np.random.randint(22, 50)
        })
    
    trade_df = pd.DataFrame(trade_data)
    
    debt_data = []
    years = list(range(2019, 2024))
    countries = ['Lebanon', 'Jordan', 'Syria']
    
    for country in countries:
        base_debt = {'Lebanon': 40, 'Jordan': 26, 'Syria': 16}[country]
        for year in years:
            trend = (year - 2019) * 2
            debt_data.append({
                'Country': country,
                'Year': year,
                'Debt': base_debt + trend + np.random.uniform(-1, 1)
            })
    
    debt_df = pd.DataFrame(debt_data)
    return trade_df, debt_df

trade_df, debt_df = create_data()

# Ultra-compact metrics in one line
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.metric("Towns", len(trade_df))
with col_m2:
    st.metric("Districts", trade_df['District'].nunique())
with col_m3:
    st.metric("Records", len(debt_df))
with col_m4:
    st.metric("Years", f"{debt_df['Year'].min()}-{debt_df['Year'].max()}")

# ALL 5 CHARTS IN ONE SINGLE ROW
col1, col2, col3, col4, col5 = st.columns(5)

# Chart 1: Stacked Bar
with col1:
    st.markdown("### Institutions")
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(name='S', x=trade_df['Town'], y=trade_df['Small'], marker_color='lightblue'))
    fig1.add_trace(go.Bar(name='M', x=trade_df['Town'], y=trade_df['Medium'], marker_color='orange'))
    fig1.add_trace(go.Bar(name='L', x=trade_df['Town'], y=trade_df['Large'], marker_color='darkred'))
    
    fig1.update_layout(
        barmode='stack',
        height=300,
        template='plotly_white',
        margin=dict(l=20, r=5, t=10, b=40),
        legend=dict(x=0, y=1, font=dict(size=8)),
        xaxis_tickangle=-45,
        xaxis=dict(tickfont=dict(size=8)),
        yaxis=dict(tickfont=dict(size=8))
    )
    st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Line Chart
with col2:
    st.markdown("### Debt Trends")
    debt_avg = debt_df.groupby('Year')['Debt'].mean().reset_index()
    
    fig2 = px.line(debt_avg, x='Year', y='Debt')
    fig2.update_traces(line=dict(width=3, color='#2E86C1'))
    fig2.update_layout(
        height=300,
        template='plotly_white',
        margin=dict(l=20, r=5, t=10, b=20),
        xaxis=dict(tickfont=dict(size=8)),
        yaxis=dict(tickfont=dict(size=8))
    )
    st.plotly_chart(fig2, use_container_width=True)

# Chart 3: Pie Chart
with col3:
    st.markdown("### Activities")
    activities = ['Self Emp', 'Commerce', 'Service', 'Financial']
    values = [trade_df['Self_Employment'].sum(), trade_df['Commerce'].sum(), 
             trade_df['Service'].sum(), trade_df['Financial'].sum()]
    
    fig3 = px.pie(values=values, names=activities)
    fig3.update_traces(textposition='inside', textinfo='percent', textfont_size=8)
    fig3.update_layout(
        height=300,
        template='plotly_white',
        margin=dict(l=5, r=5, t=10, b=10),
        showlegend=False
    )
    st.plotly_chart(fig3, use_container_width=True)

# Chart 4: Scatter Plot
with col4:
    st.markdown("### Debt by Country")
    fig4 = px.scatter(debt_df, x='Year', y='Debt', color='Country', size='Debt')
    fig4.update_layout(
        height=300,
        template='plotly_white',
        margin=dict(l=20, r=5, t=10, b=20),
        legend=dict(x=0, y=1, font=dict(size=8)),
        xaxis=dict(tickfont=dict(size=8)),
        yaxis=dict(tickfont=dict(size=8))
    )
    st.plotly_chart(fig4, use_container_width=True)

# Chart 5: Grouped Bar
with col5:
    st.markdown("### Districts")
    district_data = trade_df.groupby('District').agg({
        'Service': 'sum',
        'Financial': 'sum',
        'Self_Employment': 'sum',
        'Commerce': 'sum'
    }).reset_index()
    
    fig5 = go.Figure()
    fig5.add_trace(go.Bar(name='Svc', x=district_data['District'], y=district_data['Service'], marker_color='#1f77b4'))
    fig5.add_trace(go.Bar(name='Fin', x=district_data['District'], y=district_data['Financial'], marker_color='#ff7f0e'))
    fig5.add_trace(go.Bar(name='Self', x=district_data['District'], y=district_data['Self_Employment'], marker_color='#2ca02c'))
    fig5.add_trace(go.Bar(name='Com', x=district_data['District'], y=district_data['Commerce'], marker_color='#d62728'))
    
    fig5.update_layout(
        barmode='group',
        height=300,
        template='plotly_white',
        margin=dict(l=20, r=5, t=10, b=40),
        legend=dict(x=0, y=1, font=dict(size=8)),
        xaxis_tickangle=-30,
        xaxis=dict(tickfont=dict(size=8)),
        yaxis=dict(tickfont=dict(size=8))
    )
    st.plotly_chart(fig5, use_container_width=True)

# Minimal footer
st.markdown("**MSBA 325 Plotly Practice**")
