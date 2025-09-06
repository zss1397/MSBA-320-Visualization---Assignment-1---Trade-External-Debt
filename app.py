import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Page config
st.set_page_config(
    page_title="MSBA 325 Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ultra-compact CSS
st.markdown("""
<style>
    .main .block-container {
        padding-top: 0.2rem;
        padding-bottom: 0.2rem;
        max-width: 100%;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    .stPlotlyChart {
        height: 160px !important;
    }
    h1 {
        color: #1f77b4;
        text-align: center;
        font-size: 1.8rem;
        margin: 0.2rem 0;
        font-weight: bold;
    }
    h2 {
        color: #333;
        font-size: 0.9rem;
        margin: 0.1rem 0;
        font-weight: bold;
    }
    h3 {
        color: #333;
        font-size: 0.8rem;
        margin: 0.1rem 0;
    }
    div[data-testid="stSidebar"] {
        display: none;
    }
    .stMetric {
        background-color: #f8f9fa;
        padding: 0.3rem;
        border-radius: 0.3rem;
        text-align: center;
        height: 50px;
    }
    .element-container {
        margin-bottom: 0.2rem;
    }
    .stMarkdown {
        margin-bottom: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

# Compact title
st.markdown("# MSBA 325 Economic Dashboard")

# Create simple data
@st.cache_data
def create_data():
    towns = ['Beirut', 'Tripoli', 'Sidon', 'Tyre']
    districts = ['Aley', 'Zahle', 'Matn', 'Baabda']
    
    trade_data = []
    for i, town in enumerate(towns):
        trade_data.append({
            'Town': town,
            'Small': np.random.randint(30, 60),
            'Medium': np.random.randint(8, 20),
            'Large': np.random.randint(2, 6),
            'District': districts[i],
            'Service': np.random.randint(15, 35),
            'Financial': np.random.randint(8, 20),
            'Self_Employment': np.random.randint(20, 50),
            'Public_Sector': np.random.randint(8, 20),
            'Banking': np.random.randint(3, 12),
            'Commerce': np.random.randint(25, 60)
        })
    
    trade_df = pd.DataFrame(trade_data)
    
    debt_data = []
    years = list(range(2019, 2024))
    countries = ['Lebanon', 'Jordan', 'Syria']
    
    for country in countries:
        base_debt = {'Lebanon': 45, 'Jordan': 30, 'Syria': 20}[country]
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

# Compact metrics
col_a, col_b, col_c, col_d = st.columns(4)
with col_a:
    st.metric("Towns", len(trade_df))
with col_b:
    st.metric("Districts", trade_df['District'].nunique())
with col_c:
    st.metric("Records", len(debt_df))
with col_d:
    st.metric("Years", f"{debt_df['Year'].min()}-{debt_df['Year'].max()}")

# Charts in 2x3 layout
col1, col2, col3 = st.columns(3)

# Chart 1
with col1:
    st.markdown("## 1️⃣ Institutions by Size")
    
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(name='S', x=trade_df['Town'], y=trade_df['Small'], marker_color='lightblue'))
    fig1.add_trace(go.Bar(name='M', x=trade_df['Town'], y=trade_df['Medium'], marker_color='orange'))
    fig1.add_trace(go.Bar(name='L', x=trade_df['Town'], y=trade_df['Large'], marker_color='darkred'))
    
    fig1.update_layout(
        barmode='stack',
        height=160,
        template='plotly_white',
        margin=dict(l=30, r=10, t=10, b=40),
        legend=dict(x=0, y=1, orientation="h"),
        showlegend=True,
        xaxis_tickangle=-45
    )
    
    st.plotly_chart(fig1, use_container_width=True)

# Chart 2
with col2:
    st.markdown("## 2️⃣ Debt Trends")
    
    debt_avg = debt_df.groupby('Year')['Debt'].mean().reset_index()
    
    fig2 = px.line(debt_avg, x='Year', y='Debt')
    fig2.update_traces(line=dict(width=3, color='#2E86C1'))
    fig2.update_layout(
        height=160,
        template='plotly_white',
        margin=dict(l=30, r=10, t=10, b=30),
        showlegend=False
    )
    
    st.plotly_chart(fig2, use_container_width=True)

# Chart 3
with col3:
    st.markdown("## 3️⃣ Business Activities")
    
    activities = ['Self Emp', 'Public', 'Banking', 'Commerce']
    values = [trade_df['Self_Employment'].sum(), trade_df['Public_Sector'].sum(), 
             trade_df['Banking'].sum(), trade_df['Commerce'].sum()]
    
    fig3 = px.pie(values=values, names=activities)
    fig3.update_traces(textposition='inside', textinfo='percent', textfont_size=10)
    fig3.update_layout(
        height=160,
        template='plotly_white',
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=True,
        legend=dict(x=0, y=0, orientation="v", font=dict(size=8))
    )
    
    st.plotly_chart(fig3, use_container_width=True)

# Second row
col4, col5 = st.columns(2)

# Chart 4
with col4:
    st.markdown("## 4️⃣ Debt by Country")
    
    fig4 = px.scatter(debt_df, x='Year', y='Debt', color='Country', size='Debt')
    fig4.update_layout(
        height=160,
        template='plotly_white',
        margin=dict(l=40, r=10, t=10, b=40),
        legend=dict(x=0, y=1, orientation="h", font=dict(size=8))
    )
    
    st.plotly_chart(fig4, use_container_width=True)

# Chart 5
with col5:
    st.markdown("## 5️⃣ District Activities")
    
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
        height=160,
        template='plotly_white',
        margin=dict(l=40, r=10, t=10, b=40),
        legend=dict(x=0, y=1, orientation="h", font=dict(size=8)),
        xaxis_tickangle=-30
    )
    
    st.plotly_chart(fig5, use_container_width=True)

# Minimal footer
st.markdown("**MSBA 325 Plotly Practice | Streamlit Dashboard**")
