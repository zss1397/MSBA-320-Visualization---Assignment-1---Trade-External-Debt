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

# CSS for proper layout
st.markdown("""
<style>
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 100%;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    .stPlotlyChart {
        height: 250px !important;
    }
    h1 {
        color: #1f77b4;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    h2 {
        color: #333;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
        font-weight: bold;
    }
    div[data-testid="stSidebar"] {
        display: none;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Clear title
st.markdown("# MSBA 325 Economic Data Dashboard")
st.markdown("## Interactive Plotly Visualizations - Trade & External Debt Analysis")

# Create simple, clear sample data
@st.cache_data
def create_data():
    # Trade data
    towns = ['Beirut', 'Tripoli', 'Sidon', 'Tyre']
    districts = ['Aley', 'Zahle', 'Matn', 'Baabda']
    
    trade_data = []
    for i, town in enumerate(towns):
        trade_data.append({
            'Town': town,
            'Small_Institutions': np.random.randint(30, 70),
            'Medium_Institutions': np.random.randint(10, 25),
            'Large_Institutions': np.random.randint(2, 8),
            'District': districts[i],
            'Service_Institutions': np.random.randint(15, 45),
            'Financial_Institutions': np.random.randint(8, 25),
            'Self_Employment': np.random.randint(20, 60),
            'Public_Sector': np.random.randint(8, 25),
            'Banking': np.random.randint(3, 15),
            'Commerce': np.random.randint(25, 70)
        })
    
    trade_df = pd.DataFrame(trade_data)
    
    # Debt data
    years = list(range(2018, 2024))
    countries = ['Lebanon', 'Jordan', 'Syria']
    
    debt_data = []
    for country in countries:
        base_debt = {'Lebanon': 50, 'Jordan': 35, 'Syria': 25}[country]
        for year in years:
            trend = (year - 2018) * 3
            noise = np.random.uniform(-2, 2)
            debt_data.append({
                'Country': country,
                'Year': year,
                'Debt_Billions': base_debt + trend + noise
            })
    
    debt_df = pd.DataFrame(debt_data)
    return trade_df, debt_df

trade_df, debt_df = create_data()

# Summary metrics with proper styling
st.markdown("### Dataset Summary")
col_a, col_b, col_c, col_d = st.columns(4)

with col_a:
    st.metric("Towns", len(trade_df), help="Number of towns analyzed")
with col_b:
    st.metric("Districts", trade_df['District'].nunique(), help="Number of districts")
with col_c:
    st.metric("Records", len(debt_df), help="Total debt records")
with col_d:
    st.metric("Years", f"{debt_df['Year'].min()}-{debt_df['Year'].max()}", help="Time period covered")

st.markdown("---")

# Charts in 2x2 layout plus one full width
col1, col2 = st.columns(2)

# Chart 1: Stacked Bar Chart
with col1:
    st.markdown("## 1️⃣ Commercial Institutions by Size")
    
    fig1 = go.Figure()
    
    fig1.add_trace(go.Bar(
        name='Small Institutions',
        x=trade_df['Town'],
        y=trade_df['Small_Institutions'],
        marker_color='lightblue'
    ))
    
    fig1.add_trace(go.Bar(
        name='Medium Institutions',
        x=trade_df['Town'],
        y=trade_df['Medium_Institutions'],
        marker_color='orange'
    ))
    
    fig1.add_trace(go.Bar(
        name='Large Institutions',
        x=trade_df['Town'],
        y=trade_df['Large_Institutions'],
        marker_color='darkred'
    ))
    
    fig1.update_layout(
        barmode='stack',
        height=250,
        template='plotly_white',
        margin=dict(l=60, r=60, t=40, b=80),
        xaxis_title="Towns",
        yaxis_title="Number of Institutions",
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02
        )
    )
    
    st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Line Chart
with col2:
    st.markdown("## 2️⃣ External Debt Trends Over Time")
    
    debt_avg = debt_df.groupby('Year')['Debt_Billions'].mean().reset_index()
    
    fig2 = px.line(
        debt_avg, 
        x='Year', 
        y='Debt_Billions',
        labels={'Year': 'Year', 'Debt_Billions': 'Average Debt (Billions USD)'},
        title=""
    )
    
    fig2.update_traces(line=dict(width=4, color='#2E86C1'))
    fig2.update_layout(
        height=250,
        template='plotly_white',
        margin=dict(l=60, r=60, t=40, b=60),
        xaxis_title="Year",
        yaxis_title="Debt (Billions USD)"
    )
    
    st.plotly_chart(fig2, use_container_width=True)

# Second row
col3, col4 = st.columns(2)

# Chart 3: Pie Chart with clear labels
with col3:
    st.markdown("## 3️⃣ Business Activity Distribution")
    
    # Business activity data
    activity_data = {
        'Self Employment': trade_df['Self_Employment'].sum(),
        'Public Sector': trade_df['Public_Sector'].sum(),
        'Banking': trade_df['Banking'].sum(),
        'Commerce': trade_df['Commerce'].sum()
    }
    
    fig3 = px.pie(
        values=list(activity_data.values()),
        names=list(activity_data.keys()),
        color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    )
    
    fig3.update_traces(
        textposition='inside',
        textinfo='percent+label',
        textfont_size=11
    )
    
    fig3.update_layout(
        height=250,
        template='plotly_white',
        margin=dict(l=20, r=20, t=40, b=20),
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05
        )
    )
    
    st.plotly_chart(fig3, use_container_width=True)

# Chart 4: Scatter Plot
with col4:
    st.markdown("## 4️⃣ External Debt by Country")
    
    fig4 = px.scatter(
        debt_df,
        x='Year',
        y='Debt_Billions',
        color='Country',
        size='Debt_Billions',
        labels={'Year': 'Year', 'Debt_Billions': 'Debt (Billions USD)', 'Country': 'Country'}
    )
    
    fig4.update_layout(
        height=250,
        template='plotly_white',
        margin=dict(l=60, r=60, t=40, b=60),
        xaxis_title="Year",
        yaxis_title="Debt (Billions USD)",
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02
        )
    )
    
    st.plotly_chart(fig4, use_container_width=True)

# Chart 5: Full width grouped bar chart
st.markdown("## 5️⃣ Business Activities by District")

# District comparison data
district_data = trade_df.groupby('District').agg({
    'Service_Institutions': 'sum',
    'Financial_Institutions': 'sum',
    'Self_Employment': 'sum',
    'Commerce': 'sum'
}).reset_index()

fig5 = go.Figure()

fig5.add_trace(go.Bar(
    name='Service Institutions',
    x=district_data['District'],
    y=district_data['Service_Institutions'],
    marker_color='#1f77b4'
))

fig5.add_trace(go.Bar(
    name='Financial Institutions',
    x=district_data['District'],
    y=district_data['Financial_Institutions'],
    marker_color='#ff7f0e'
))

fig5.add_trace(go.Bar(
    name='Self Employment',
    x=district_data['District'],
    y=district_data['Self_Employment'],
    marker_color='#2ca02c'
))

fig5.add_trace(go.Bar(
    name='Commerce Activities',
    x=district_data['District'],
    y=district_data['Commerce'],
    marker_color='#d62728'
))

fig5.update_layout(
    barmode='group',
    height=250,
    template='plotly_white',
    margin=dict(l=80, r=80, t=50, b=80),
    xaxis_title="Districts",
    yaxis_title="Number of Activities/Institutions",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5
    )
)

st.plotly_chart(fig5, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("**MSBA 325 Plotly Practice Activity | Created with Streamlit & Plotly | Interactive Economic Data Analysis**")
