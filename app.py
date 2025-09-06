import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Set page config for wide layout
st.set_page_config(
    page_title="MSBA 325 Economic Data Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for better styling
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
    .metric-row {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("📊 MSBA 325 Economic Data Dashboard")
st.markdown("**Interactive Plotly Visualizations - Trade & External Debt Analysis**")
st.markdown("---")

# File uploader section
st.sidebar.title("📁 Upload Your Data Files")
trade_file = st.sidebar.file_uploader("Upload Trade CSV", type=['csv'], key="trade")
debt_file = st.sidebar.file_uploader("Upload External Debt CSV", type=['csv'], key="debt")

# Load data function
@st.cache_data
def load_data(file):
    if file is not None:
        df = pd.read_csv(file)
        df.columns = df.columns.str.strip()
        return df
    return None

# Load data if uploaded
trade_df = load_data(trade_file)
debt_df = load_data(debt_file)

# Check if data is uploaded
if trade_df is not None and debt_df is not None:
    
    # Success message
    st.success("✅ Data files loaded successfully! Generating visualizations...")
    
    # Create layout with two columns for first 4 charts
    col1, col2 = st.columns(2)
    
    # VISUALIZATION 1: Stacked Bar Chart
    with col1:
        st.subheader("1️⃣ Commercial Institutions by Size")
        
        try:
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
                height=400,
                xaxis_tickangle=-45,
                template='plotly_white',
                margin=dict(l=40, r=40, t=40, b=100),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig1, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error creating chart 1: {str(e)}")

    # VISUALIZATION 2: Line Chart
    with col2:
        st.subheader("2️⃣ External Debt Trends Over Time")
        
        try:
            debt_time_series = debt_df[debt_df['Value'].notna()].copy()
            debt_trends = debt_time_series.groupby('refPeriod')['Value'].mean().reset_index()
            
            fig2 = px.line(debt_trends, x='refPeriod', y='Value', 
                          labels={'refPeriod': 'Year', 'Value': 'Average External Debt Value'})
            fig2.update_traces(line=dict(width=3, color='#2E86C1'))
            fig2.update_layout(
                height=400,
                template='plotly_white',
                margin=dict(l=40, r=40, t=40, b=40)
            )
            st.plotly_chart(fig2, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error creating chart 2: {str(e)}")

    # Second row
    col3, col4 = st.columns(2)
    
    # VISUALIZATION 3: Pie Chart
    with col3:
        st.subheader("3️⃣ Business Activity Distribution")
        
        try:
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
            
        except Exception as e:
            st.error(f"Error creating chart 3: {str(e)}")

    # VISUALIZATION 4: Scatter Plot
    with col4:
        st.subheader("4️⃣ External Debt by Country & Time")
        
        try:
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
                height=400,
                template='plotly_white',
                margin=dict(l=40, r=40, t=40, b=40),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig4, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error creating chart 4: {str(e)}")

    # VISUALIZATION 5: Full width grouped bar chart
    st.subheader("5️⃣ Business Activity Distribution Across Top Districts")
    
    try:
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
            height=500,
            template='plotly_white',
            margin=dict(l=60, r=60, t=60, b=100),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            xaxis_title='District',
            yaxis_title='Number of Activities/Institutions'
        )
        
        st.plotly_chart(fig5, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error creating chart 5: {str(e)}")
    
    # Summary metrics
    st.markdown("---")
    st.subheader("📈 Dataset Summary")
    
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
    # Instructions when no data is uploaded
    st.info("👆 Please upload both CSV files in the sidebar to view all visualizations")
    
    st.markdown("""
    ## 📋 How to Use This Dashboard:
    
    1. **Upload Trade CSV** - Contains commercial and service activities data by town and region
    2. **Upload External Debt CSV** - Contains external debt information over time periods
    3. **View Dashboard** - All 5 interactive visualizations will appear automatically
    
    ## 🎯 What You'll See:
    
    ### Chart Types Included:
    - **📊 Stacked Bar Chart** - Commercial institutions by size across towns
    - **📈 Line Chart** - External debt trends over time periods
    - **🥧 Pie Chart** - Business activity type distribution  
    - **🔸 Scatter Plot** - External debt values by country and time (with bubble sizing)
    - **📊 Grouped Bar Chart** - District-level business activity comparison
    
    ### Features:
    - Interactive zoom, pan, and hover functionality
    - Professional styling and color schemes
    - Responsive layout that works on all devices
    - Clean data processing and error handling
    - Summary statistics and metrics
    """)

# Footer
st.markdown("---")
st.markdown("**MSBA 325 Plotly Practice Activity** | Created with Streamlit & Plotly")
st.markdown("Interactive Economic Data Analysis Dashboard | Deploy on Streamlit Cloud")
