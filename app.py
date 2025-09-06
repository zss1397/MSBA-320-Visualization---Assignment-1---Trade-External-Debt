import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Set page config
st.set_page_config(
    page_title="MSBA 325 Economic Data Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for compact layout
st.markdown("""
<style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        max-width: 100%;
    }
    .stPlotlyChart {
        height: 250px !important;
    }
    h1 {
        color: #1f77b4;
        text-align: center;
        padding-bottom: 0.5rem;
        font-size: 2rem;
    }
    h2 {
        color: #333;
        font-size: 1.2rem;
        margin-bottom: 0.3rem;
    }
    .element-container {
        margin-bottom: 0.5rem;
    }
    div[data-testid="stSidebar"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("MSBA 325 Economic Data Dashboard")
st.markdown("**Interactive Plotly Visualizations - Trade & External Debt Analysis**")

# Create sample data
@st.cache_data
def create_sample_data():
    # Sample trade data
    towns = ['Beirut', 'Tripoli', 'Sidon', 'Tyre', 'Zahle', 'Baalbek']
    regions = ['Aley District', 'Zahle District', 'Matn District', 'Baabda District', 'Akkar District', 'Baalbek-Hermel District']
    
    trade_data = []
    for i, town in enumerate(towns):
        trade_data.append({
            'Town': town,
            'Total number of commercial institutions by size - number of small institutions': np.random.randint(20, 100),
            'Total number of commercial institutions by size - number of medium-sized institutions': np.random.randint(5, 30),
            'Total number of commercial institutions by size - number of large-sized institutions': np.random.randint(1, 10),
            'refArea': np.random.choice(regions),
            'Total number of service institutions': np.random.randint(10, 50),
            'Total number of non banking financial institutions': np.random.randint(5, 25),
            'Existence of commercial and service activities by type - self employment': np.random.randint(15, 60),
            'Existence of commercial and service activities by type - public sector': np.random.randint(5, 25),
            'Existence of commercial and service activities by type - banking institutions': np.random.randint(2, 15),
            'Existence of commercial and service activities by type - service institutions': np.random.randint(10, 40),
            'Existence of commercial and service activities by type - commerce': np.random.randint(20, 70)
        })
    
    trade_df = pd.DataFrame(trade_data)
    
    # Sample debt data
    years = list(range(2015, 2024))
    countries = ['Lebanon', 'Jordan', 'Syria', 'Iraq']
    
    debt_data = []
    for country in countries:
        base_debt = np.random.uniform(20000000000, 80000000000)
        for year in years:
            trend_factor = (year - 2015) * 0.08
            noise = np.random.uniform(-0.1, 0.1)
            debt_value = base_debt * (1 + trend_factor + noise)
            
            debt_data.append({
                'refArea': country,
                'refPeriod': year,
                'Value': debt_value,
                'Indicator Code': 'DT.DOD.DECT.CD'
            })
    
    debt_df = pd.DataFrame(debt_data)
    return trade_df, debt_df

# Load sample data
trade_df, debt_df = create_sample_data()

# Create compact layout - 2x2 grid for first 4 charts
col1, col2 = st.columns(2)

# VISUALIZATION 1: Stacked Bar Chart
with col1:
    st.subheader("1️⃣ Commercial Institutions by Size")
    
    institution_data = trade_df.groupby('Town').agg({
        'Total number of commercial institutions by size - number of small institutions': 'sum',
        'Total number of commercial institutions by size - number of medium-sized institutions': 'sum',
        'Total number of commercial institutions by size - number of large-sized institutions': 'sum'
    }).reset_index()
    
    institution_data.columns = ['Town', 'Small', 'Medium', 'Large']
    institution_data['Total'] = institution_data['Small'] + institution_data['Medium'] + institution_data['Large']
    institution_data = institution_data.sort_values('Total', ascending=True).tail(5)
    
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(name='Small', x=institution_data['Town'], y=institution_data['Small'], marker_color='lightblue'))
    fig1.add_trace(go.Bar(name='Medium', x=institution_data['Town'], y=institution_data['Medium'], marker_color='orange'))
    fig1.add_trace(go.Bar(name='Large', x=institution_data['Town'], y=institution_data['Large'], marker_color='darkred'))
    
    fig1.update_layout(
        barmode='stack',
        height=250,
        template='plotly_white',
        margin=dict(l=20, r=20, t=20, b=60),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig1, use_container_width=True)

# VISUALIZATION 2: Line Chart
with col2:
    st.subheader("2️⃣ External Debt Trends Over Time")
    
    debt_trends = debt_df.groupby('refPeriod')['Value'].mean().reset_index()
    
    fig2 = px.line(debt_trends, x='refPeriod', y='Value', 
                  labels={'refPeriod': 'Year', 'Value': 'Avg External Debt'})
    fig2.update_traces(line=dict(width=3, color='#2E86C1'))
    fig2.update_layout(
        height=250,
        template='plotly_white',
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig2, use_container_width=True)

# Second row
col3, col4 = st.columns(2)

# VISUALIZATION 3: Pie Chart
with col3:
    st.subheader("3️⃣ Business Activity Distribution")
    
    activity_totals = {
        'Self Employment': trade_df['Existence of commercial and service activities by type - self employment'].sum(),
        'Public Sector': trade_df['Existence of commercial and service activities by type - public sector'].sum(),
        'Banking': trade_df['Existence of commercial and service activities by type - banking institutions'].sum(),
        'Service': trade_df['Existence of commercial and service activities by type - service institutions'].sum(),
        'Commerce': trade_df['Existence of commercial and service activities by type - commerce'].sum()
    }
    
    fig3 = px.pie(values=list(activity_totals.values()), names=list(activity_totals.keys()),
                 color_discrete_sequence=px.colors.qualitative.Set3)
    fig3.update_traces(textposition='inside', textinfo='percent+label')
    fig3.update_layout(
        height=250,
        template='plotly_white',
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig3, use_container_width=True)

# VISUALIZATION 4: Scatter Plot
with col4:
    st.subheader("4️⃣ External Debt by Country & Time")
    
    debt_scatter_data = debt_df.copy()
    debt_scatter_data['Size_Value'] = debt_scatter_data['Value'].abs()
    
    fig4 = px.scatter(debt_scatter_data, x='refPeriod', y='Value', 
                     color='refArea', size='Size_Value',
                     labels={'refPeriod': 'Year', 'Value': 'External Debt', 'refArea': 'Country'})
    fig4.update_layout(
        height=250,
        template='plotly_white',
        margin=dict(l=20, r=20, t=20, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig4, use_container_width=True)

# VISUALIZATION 5: Compact grouped bar chart
st.subheader("5️⃣ Business Activity Distribution Across Districts")

comparison_data = trade_df.groupby('refArea').agg({
    'Total number of service institutions': 'sum',
    'Total number of non banking financial institutions': 'sum',
    'Existence of commercial and service activities by type - self employment': 'sum',
    'Existence of commercial and service activities by type - commerce': 'sum'
}).reset_index()

comparison_data.columns = ['Region', 'Service', 'Financial', 'Self Employment', 'Commerce']
comparison_data['Total'] = comparison_data['Service'] + comparison_data['Financial'] + comparison_data['Self Employment'] + comparison_data['Commerce']
comparison_data = comparison_data.sort_values('Total', ascending=False).head(5)

fig5 = go.Figure()
fig5.add_trace(go.Bar(name='Service', x=comparison_data['Region'], y=comparison_data['Service'], marker_color='#1f77b4'))
fig5.add_trace(go.Bar(name='Financial', x=comparison_data['Region'], y=comparison_data['Financial'], marker_color='#ff7f0e'))
fig5.add_trace(go.Bar(name='Self Employment', x=comparison_data['Region'], y=comparison_data['Self Employment'], marker_color='#2ca02c'))
fig5.add_trace(go.Bar(name='Commerce', x=comparison_data['Region'], y=comparison_data['Commerce'], marker_color='#d62728'))

fig5.update_layout(
    barmode='group',
    height=280,
    template='plotly_white',
    margin=dict(l=40, r=40, t=40, b=80),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    xaxis_tickangle=-30,
    xaxis_title='District',
    yaxis_title='Count'
)

st.plotly_chart(fig5, use_container_width=True)

# Compact footer
st.markdown("**MSBA 325 Plotly Practice** | Streamlit & Plotly Dashboard")

# Footer
st.markdown("---")
st.markdown("**MSBA 325 Plotly Practice Activity** | Created with Streamlit & Plotly")
st.markdown("Interactive Economic Data Analysis Dashboard")
