import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Set page config
st.set_page_config(
    page_title="MSBA 325 Economic Data Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem;
    }
    .stPlotlyChart {
        height: 400px !important;
    }
    h1 {
        color: #1f77b4;
        text-align: center;
        padding-bottom: 1rem;
    }
    h2 {
        color: #333;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("MSBA 325 Economic Data Dashboard")
st.markdown("**Interactive Plotly Visualizations - Trade & External Debt Analysis**")
st.markdown("---")

# Create sample data that mimics your actual data structure
@st.cache_data
def create_sample_data():
    # Sample trade data
    towns = ['Beirut', 'Tripoli', 'Sidon', 'Tyre', 'Zahle', 'Baalbek', 'Nabatieh', 'Jounieh']
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
    years = list(range(2010, 2024))
    countries = ['Lebanon', 'Jordan', 'Syria', 'Iraq', 'Egypt']
    
    debt_data = []
    for country in countries:
        base_debt = np.random.uniform(10000000000, 80000000000)  # 10B to 80B
        for year in years:
            trend_factor = (year - 2010) * 0.05  # Increasing trend
            noise = np.random.uniform(-0.2, 0.2)
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

# Display success message
st.success("Dashboard loaded successfully! Displaying sample economic data visualizations.")

# Create layout
col1, col2 = st.columns(2)

# VISUALIZATION 1: Stacked Bar Chart
with col1:
    st.subheader("1️⃣ Commercial Institutions by Size")
    
    institution_data = trade_df.groupby('Town').agg({
        'Total number of commercial institutions by size - number of small institutions': 'sum',
        'Total number of commercial institutions by size - number of medium-sized institutions': 'sum',
        'Total number of commercial institutions by size - number of large-sized institutions': 'sum'
    }).reset_index()
    
    institution_data.columns = ['Town', 'Small_Institutions', 'Medium_Institutions', 'Large_Institutions']
    institution_data['Total'] = (institution_data['Small_Institutions'] + 
                                institution_data['Medium_Institutions'] + 
                                institution_data['Large_Institutions'])
    institution_data = institution_data.sort_values('Total', ascending=True).tail(6)
    
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(name='Small', x=institution_data['Town'], y=institution_data['Small_Institutions'], marker_color='lightblue'))
    fig1.add_trace(go.Bar(name='Medium', x=institution_data['Town'], y=institution_data['Medium_Institutions'], marker_color='orange'))
    fig1.add_trace(go.Bar(name='Large', x=institution_data['Town'], y=institution_data['Large_Institutions'], marker_color='darkred'))
    
    fig1.update_layout(
        barmode='stack',
        height=400,
        xaxis_tickangle=-45,
        template='plotly_white',
        margin=dict(l=40, r=40, t=40, b=100),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig1, use_container_width=True)

# VISUALIZATION 2: Line Chart
with col2:
    st.subheader("2️⃣ External Debt Trends Over Time")
    
    debt_trends = debt_df.groupby('refPeriod')['Value'].mean().reset_index()
    
    fig2 = px.line(debt_trends, x='refPeriod', y='Value', 
                  labels={'refPeriod': 'Year', 'Value': 'Average External Debt Value'})
    fig2.update_traces(line=dict(width=3, color='#2E86C1'))
    fig2.update_layout(
        height=400,
        template='plotly_white',
        margin=dict(l=40, r=40, t=40, b=40)
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
        'Service Institutions': trade_df['Existence of commercial and service activities by type - service institutions'].sum(),
        'Commerce': trade_df['Existence of commercial and service activities by type - commerce'].sum()
    }
    
    fig3 = px.pie(values=list(activity_totals.values()), names=list(activity_totals.keys()),
                 color_discrete_sequence=px.colors.qualitative.Set3)
    fig3.update_traces(textposition='inside', textinfo='percent+label')
    fig3.update_layout(
        height=400,
        template='plotly_white',
        margin=dict(l=40, r=40, t=40, b=40)
    )
    st.plotly_chart(fig3, use_container_width=True)

# VISUALIZATION 4: Scatter Plot
with col4:
    st.subheader("4️⃣ External Debt by Country & Time")
    
    debt_scatter_data = debt_df.copy()
    debt_scatter_data['Size_Value'] = debt_scatter_data['Value'].abs()
    
    fig4 = px.scatter(debt_scatter_data, x='refPeriod', y='Value', 
                     color='refArea', size='Size_Value',
                     labels={'refPeriod': 'Year', 'Value': 'External Debt Value', 'refArea': 'Country/Region'})
    fig4.update_layout(
        height=400,
        template='plotly_white',
        margin=dict(l=40, r=40, t=40, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig4, use_container_width=True)

# VISUALIZATION 5: Full width grouped bar chart
st.subheader("5️⃣ Business Activity Distribution Across Top Districts")

comparison_data = trade_df.groupby('refArea').agg({
    'Total number of service institutions': 'sum',
    'Total number of non banking financial institutions': 'sum',
    'Existence of commercial and service activities by type - self employment': 'sum',
    'Existence of commercial and service activities by type - commerce': 'sum'
}).reset_index()

comparison_data.columns = ['Region', 'Service_Institutions', 'Financial_Institutions', 
                          'Self_Employment', 'Commerce_Activities']

comparison_data['Total_Activity'] = (comparison_data['Service_Institutions'] + 
                                   comparison_data['Financial_Institutions'] + 
                                   comparison_data['Self_Employment'] + 
                                   comparison_data['Commerce_Activities'])

comparison_data = comparison_data.sort_values('Total_Activity', ascending=False).head(6)

fig5 = go.Figure()
fig5.add_trace(go.Bar(name='Service Institutions', x=comparison_data['Region'], y=comparison_data['Service_Institutions'], marker_color='#1f77b4'))
fig5.add_trace(go.Bar(name='Financial Institutions', x=comparison_data['Region'], y=comparison_data['Financial_Institutions'], marker_color='#ff7f0e'))
fig5.add_trace(go.Bar(name='Self Employment', x=comparison_data['Region'], y=comparison_data['Self_Employment'], marker_color='#2ca02c'))
fig5.add_trace(go.Bar(name='Commerce Activities', x=comparison_data['Region'], y=comparison_data['Commerce_Activities'], marker_color='#d62728'))

fig5.update_layout(
    barmode='group',
    xaxis_tickangle=-30,
    height=500,
    template='plotly_white',
    margin=dict(l=60, r=60, t=60, b=100),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    xaxis_title='District',
    yaxis_title='Number of Activities/Institutions'
)

st.plotly_chart(fig5, use_container_width=True)

# Summary metrics
st.markdown("---")
st.subheader("Dataset Summary")

col_a, col_b, col_c, col_d = st.columns(4)

with col_a:
    st.metric("Total Towns", trade_df['Town'].nunique())
with col_b:
    st.metric("Total Regions", trade_df['refArea'].nunique())
with col_c:
    st.metric("Debt Records", len(debt_df))
with col_d:
    st.metric("Time Range", f"{debt_df['refPeriod'].min()}-{debt_df['refPeriod'].max()}")

# Optional file upload section in sidebar
st.sidebar.title("Upload Your Own Data (Optional)")
st.sidebar.markdown("To replace sample data with your actual CSV files:")

trade_file = st.sidebar.file_uploader("Upload Trade CSV", type=['csv'], key="trade")
debt_file = st.sidebar.file_uploader("Upload External Debt CSV", type=['csv'], key="debt")

if trade_file is not None and debt_file is not None:
    st.sidebar.success("Custom data uploaded! Refresh the page to use your data.")

# Footer
st.markdown("---")
st.markdown("**MSBA 325 Plotly Practice Activity** | Created with Streamlit & Plotly")
st.markdown("Interactive Economic Data Analysis Dashboard")
