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

# Title positioned at very top
st.markdown("# MSBA 325 Economic Data Dashboard")

# Create sample data
@st.cache_data
def create_data():
    towns = ['Beirut', 'Tripoli', 'Sidon', 'Tyre']
    districts = ['Aley', 'Zahle', 'Matn', 'Baabda']
    
    trade_data = []
    for i, town in enumerate(towns):
        trade_data.append({
            'Town': town,
            'Small': np.random.randint(25, 55),
            'Medium': np.random.randint(8, 18),
            'Large': np.random.randint(2, 8),
            'District': districts[i],
            'Service': np.random.randint(12, 32),
            'Financial': np.random.randint(6, 18),
            'Self_Employment': np.random.randint(18, 45),
            'Commerce': np.random.randint(22, 55)
        })
    
    trade_df = pd.DataFrame(trade_data)
    
    debt_data = []
    years = list(range(2019, 2024))
    countries = ['Lebanon', 'Jordan', 'Syria']
    
    for country in countries:
        base_debt = {'Lebanon': 42, 'Jordan': 28, 'Syria': 18}[country]
        for year in years:
            trend = (year - 2019) * 2.5
            debt_data.append({
                'Country': country,
                'Year': year,
                'Debt': base_debt + trend + np.random.uniform(-1.5, 1.5)
            })
    
    debt_df = pd.DataFrame(debt_data)
    return trade_df, debt_df

trade_df, debt_df = create_data()

# Charts in 3x2 grid layout - minimized heights
col1, col2, col3 = st.columns(3)

# Row 1: Charts 1, 2, 3
with col1:
    st.markdown("### Commercial Institutions by Size")
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(name='Small', x=trade_df['Town'], y=trade_df['Small'], marker_color='lightblue'))
    fig1.add_trace(go.Bar(name='Medium', x=trade_df['Town'], y=trade_df['Medium'], marker_color='orange'))
    fig1.add_trace(go.Bar(name='Large', x=trade_df['Town'], y=trade_df['Large'], marker_color='darkred'))
    
    fig1.update_layout(
        barmode='stack',
        height=160,
        template='plotly_white',
        margin=dict(l=20, r=10, t=5, b=40),
        legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center", font=dict(size=8)),
        xaxis_tickangle=-30,
        font=dict(size=10)
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("### External Debt Trends Over Time")
    debt_avg = debt_df.groupby('Year')['Debt'].mean().reset_index()
    
    fig2 = px.line(debt_avg, x='Year', y='Debt', 
                   labels={'Debt': 'Debt (Billions)'})
    fig2.update_traces(line=dict(width=3, color='#2E86C1'))
    fig2.update_layout(
        height=160,
        template='plotly_white',
        margin=dict(l=20, r=10, t=5, b=25),
        font=dict(size=10)
    )
    st.plotly_chart(fig2, use_container_width=True)

with col3:
    st.markdown("### Business Activity Distribution")
    activities = ['Self Employment', 'Commerce', 'Service', 'Financial']
    values = [trade_df['Self_Employment'].sum(), trade_df['Commerce'].sum(), 
             trade_df['Service'].sum(), trade_df['Financial'].sum()]
    
    fig3 = px.pie(values=values, names=activities,
                  color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
    fig3.update_traces(textposition='inside', textinfo='percent', textfont_size=8)
    fig3.update_layout(
        height=160,
        template='plotly_white',
        margin=dict(l=10, r=10, t=5, b=10),
        legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center", font=dict(size=7))
    )
    st.plotly_chart(fig3, use_container_width=True)

# Row 2: Charts 4 and 5
col4, col5 = st.columns(2)

with col4:
    st.markdown("### External Debt by Country")
    fig4 = px.scatter(debt_df, x='Year', y='Debt', color='Country', size='Debt',
                     labels={'Debt': 'Debt (Billions)'})
    fig4.update_layout(
        height=160,
        template='plotly_white',
        margin=dict(l=30, r=10, t=5, b=35),
        legend=dict(orientation="h", y=-0.25, x=0.5, xanchor="center", font=dict(size=8)),
        font=dict(size=10)
    )
    st.plotly_chart(fig4, use_container_width=True)

with col5:
    st.markdown("### Business Activities by District")
    district_data = trade_df.groupby('District').agg({
        'Service': 'sum',
        'Financial': 'sum',
        'Self_Employment': 'sum',
        'Commerce': 'sum'
    }).reset_index()
    
    fig5 = go.Figure()
    fig5.add_trace(go.Bar(name='Service', x=district_data['District'], y=district_data['Service'], marker_color='#1f77b4'))
    fig5.add_trace(go.Bar(name='Financial', x=district_data['District'], y=district_data['Financial'], marker_color='#ff7f0e'))
    fig5.add_trace(go.Bar(name='Self Emp', x=district_data['District'], y=district_data['Self_Employment'], marker_color='#2ca02c'))
    fig5.add_trace(go.Bar(name='Commerce', x=district_data['District'], y=district_data['Commerce'], marker_color='#d62728'))
    
    fig5.update_layout(
        barmode='group',
        height=160,
        template='plotly_white',
        margin=dict(l=30, r=10, t=5, b=35),
        legend=dict(orientation="h", y=-0.25, x=0.5, xanchor="center", font=dict(size=8)),
        xaxis_tickangle=-20,
        font=dict(size=10)
    )
    st.plotly_chart(fig5, use_container_width=True)

# Footer
st.markdown("**MSBA 325 Plotly Practice | Interactive Economic Data Analysis**")
