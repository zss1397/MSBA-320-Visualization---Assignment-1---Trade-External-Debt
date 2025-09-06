import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page config for wide layout
st.set_page_config(
    page_title="MSBA 325 Economic Data Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS to make it more compact
st.markdown("""
<style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
    .stPlotlyChart {
        height: 350px !important;
    }
    h1 {
        padding-bottom: 0.5rem;
    }
    h3 {
        padding-top: 0rem;
        padding-bottom: 0.3rem;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("📊 MSBA 325 Economic Data Dashboard")
st.markdown("**Interactive Plotly Visualizations - Trade & External Debt Analysis**")

# File upload section
st.sidebar.title("📁 Upload Data Files")
trade_file = st.sidebar.file_uploader("Upload Trade CSV", type=['csv'], key="trade")
debt_file = st.sidebar.file_uploader("Upload External Debt CSV", type=['csv'], key="debt")

# Load data
@st.cache_data
def load_data(file):
    if file is not None:
        df = pd.read_csv(file)
        df.columns = df.columns.str.strip()
        return df
    return None

trade_df = load_data(trade_file)
debt_df = load_data(debt_file)

if trade_df is not None and debt_df is not None:
    # Create a 2x3 grid layout
    col1, col2 = st.columns(2)
    
    with col1:
        # VISUALIZATION 1: Stacked Bar Chart
        st.subheader("1️⃣ Commercial Institutions by Size")
        
        institution_data = trade_df.groupby('Town').agg({
            'Total number of commercial institutions by size - number of small institutions': 'sum',
            'Total number of commercial institutions by size - number of medium-sized institutions': 'sum',
            'Total number of commercial institutions by size - number of large-sized institutions': 'sum'
        }).reset_index()
        
        institution_data.columns = ['Town', 'Small_Institutions', 'Medium_Institutions', 'Large_Institutions']
        institution_data = institution_data[
            (institution_data['Small_Institutions'] > 0) | 
            (institution_data['Medium_Institutions'] > 0) | 
            (institution_data['Large_Institutions'] > 0)
        ]
        
        institution_data['Total'] = (institution_data['Small_Institutions'] + 
                                    institution_data['Medium_Institutions'] + 
                                    institution_data['Large_Institutions'])
        institution_data = institution_data.sort_values('Total', ascending=True).tail(8)
        
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(name='Small', x=institution_data['Town'], y=institution_data['Small_Institutions'], marker_color='lightblue'))
        fig1.add_trace(go.Bar(name='Medium', x=institution_data['Town'], y=institution_data['Medium_Institutions'], marker_color='orange'))
        fig1.add_trace(go.Bar(name='Large', x=institution_data['Town'], y=institution_data['Large_Institutions'], marker_color='darkred'))
        
        fig1.update_layout(
            barmode='stack',
            height=300,
            xaxis_tickangle=-45,
            template='plotly_white',
            margin=dict(l=40, r=40, t=40, b=80),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        # VISUALIZATION 2: Line Chart
        st.subheader("2️⃣ External Debt Trends Over Time")
        
        debt_time_series = debt_df[debt_df['Value'].notna()].copy()
        debt_trends = debt_time_series.groupby('refPeriod')['Value'].mean().reset_index()
        
        fig2 = px.line(debt_trends, x='refPeriod', y='Value', 
                      labels={'refPeriod': 'Year', 'Value': 'Average External Debt Value'})
        fig2.update_traces(line=dict(width=3, color='#2E86C1'))
        fig2.update_layout(
            height=300,
            template='plotly_white',
            margin=dict(l=40, r=40, t=40, b=40)
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Second row
    col3, col4 = st.columns(2)
    
    with col3:
        # VISUALIZATION 3: Pie Chart
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
            height=300,
            template='plotly_white',
            margin=dict(l=40, r=40, t=40, b=40)
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        # VISUALIZATION 4: Scatter Plot
        st.subheader("4️⃣ External Debt by Country & Time")
        
        top_countries = debt_df['refArea'].value_counts().head(5).index
        debt_scatter_data = debt_df[
            (debt_df['refArea'].isin(top_countries)) & 
            (debt_df['Value'].notna())
        ].copy()
        debt_scatter_data['Size_Value'] = debt_scatter_data['Value'].abs()
        debt_scatter_data = debt_scatter_data[debt_scatter_data['Size_Value'] > 0]
        
        fig4 = px.scatter(debt_scatter_data, x='refPeriod', y='Value', 
                         color='refArea', size='Size_Value',
                         labels={'refPeriod': 'Year', 'Value': 'External Debt Value', 'refArea': 'Country/Region'})
        fig4.update_layout(
            height=300,
            template='plotly_white',
            margin=dict(l=40, r=40, t=40, b=40),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig4, use_container_width=True)

    # Third row - Full width for the grouped bar chart
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
    
    comparison_data = comparison_data[comparison_data['Total_Activity'] > 0]
    comparison_data = comparison_data.sort_values('Total_Activity', ascending=False).head(6)
    
    def clean_region_name(name):
        if pd.isna(name):
            return "Unknown"
        name = str(name)
        if 'http' in name:
            if '/' in name:
                name = name.split('/')[-1]
        name = name.replace('_', ' ').replace('%2C', ' ').replace('%20', ' ')
        if name.lower().startswith('aley'):
            return "Aley District"
        elif name.lower().startswith('zahl'):
            return "Zahle District"  
        elif name.lower().startswith('matn'):
            return "Matn District"
        elif name.lower().startswith('baab'):
            return "Baabda District"
        elif name.lower().startswith('akkar'):
            return "Akkar District"
        elif 'hermel' in name.lower():
            return "Baalbek-Hermel District"
        else:
            first_word = name.split(' ')[0]
            if len(first_word) > 2:
                return first_word.title() + " District"
            else:
                return "Region " + first_word.upper()
    
    comparison_data['Clean_Region'] = comparison_data['Region'].apply(clean_region_name)
    
    fig5 = go.Figure()
    fig5.add_trace(go.Bar(name='Service Institutions', x=comparison_data['Clean_Region'], y=comparison_data['Service_Institutions'], marker_color='#1f77b4'))
    fig5.add_trace(go.Bar(name='Financial Institutions', x=comparison_data['Clean_Region'], y=comparison_data['Financial_Institutions'], marker_color='#ff7f0e'))
    fig5.add_trace(go.Bar(name='Self Employment', x=comparison_data['Clean_Region'], y=comparison_data['Self_Employment'], marker_color='#2ca02c'))
    fig5.add_trace(go.Bar(name='Commerce Activities', x=comparison_data['Clean_Region'], y=comparison_data['Commerce_Activities'], marker_color='#d62728'))
    
    fig5.update_layout(
        barmode='group',
        xaxis_tickangle=-30,
        height=400,
        template='plotly_white',
        margin=dict(l=60, r=60, t=60, b=100),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        xaxis_title='District',
        yaxis_title='Number of Activities/Institutions'
    )
    
    st.plotly_chart(fig5, use_container_width=True)
    
    # Summary metrics
    st.markdown("---")
    col_a, col_b, col_c, col_d = st.columns(4)
    
    with col_a:
        st.metric("Total Towns", trade_df['Town'].nunique())
    with col_b:
        st.metric("Total Regions", trade_df['refArea'].nunique())
    with col_c:
        st.metric("Debt Records", len(debt_df))
    with col_d:
        st.metric("Time Range", f"{debt_df['refPeriod'].min()}-{debt_df['refPeriod'].max()}")

else:
    st.info("👆 Please upload both CSV files in the sidebar to view the dashboard")
    st.markdown("""
    ### 📋 Instructions:
    1. **Upload Trade CSV** - Contains commercial and service activities data
    2. **Upload External Debt CSV** - Contains external debt information
    3. **View Dashboard** - All 5 visualizations will appear on one page
    
    ### 🎯 What You'll See:
    - **Stacked Bar Chart** - Commercial institutions by size
    - **Line Chart** - External debt trends over time
    - **Pie Chart** - Business activity distribution  
    - **Scatter Plot** - External debt by country and time
    - **Grouped Bar Chart** - District business activities
    """)

# Footer
st.markdown("---")
st.markdown("**MSBA 325 Plotly Practice Activity** | Created with Streamlit & Plotly | 📊 Interactive Economic Data Analysis")
