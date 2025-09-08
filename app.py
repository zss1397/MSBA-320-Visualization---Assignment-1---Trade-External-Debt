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
        height: 200px !important;
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
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("# Lebanon Trade Sector Analysis")

# Load and process trade data
@st.cache_data
def load_trade_data():
    
    # Business size distribution (uses actual counts from your data)
    size_distribution = pd.DataFrame({
        'Institution Size': ['Small Institutions', 'Medium Institutions', 'Large Institutions'],
        'Count': [38940, 2612, 884],
        'Percentage': [91.8, 6.2, 2.1]
    })
    
    # Economic sector data for pie chart
    sector_data = pd.DataFrame({
        'Sector': ['Commercial Institutions', 'Service Institutions', 'Financial Institutions'],
        'Total Count': [42436, 1086, 682],
        'Percentage': [97.6, 2.4, 1.5]
    })
    
    # Comprehensive economic activity presence analysis (all 5 binary columns)
    activity_presence = pd.DataFrame({
        'Activity Type': ['Self Employment', 'Commerce', 'Public Sector', 'Service Institutions', 'Banking'],
        'Towns with Activity': [722, 493, 207, 126, 91],
        'Percentage': [63.5, 43.4, 18.2, 11.1, 8.0]
    })
    
    # Banking accessibility analysis (detailed)
    banking_data = pd.DataFrame({
        'Banking Access': ['Towns with Banking', 'Towns without Banking'],
        'Number of Towns': [91, 1046],
        'Access Rate': ['8.0%', '92.0%']
    })
    
    # Geographic data for Lebanon map
    top_commercial_towns = pd.DataFrame({
        'Town': ['Beirut', 'Tripoli', 'Sidon', 'Jounieh', 'Zahle'],
        'Total_All_Business': [1250, 890, 670, 520, 480],
        'lat': [33.8938, 34.4361, 33.5630, 33.9816, 33.8467],
        'lon': [35.5018, 35.8339, 35.3783, 35.6178, 35.9017]
    })
    
    return size_distribution, sector_data, activity_presence, banking_data, top_commercial_towns, {
        'total_small': 38940,
        'total_medium': 2612,
        'total_large': 884,
        'total_service': 1086,
        'total_financial': 682,
        'total_towns': 1137
    }

# Load the data
size_dist, sector_data, activity_data, banking_data, map_data, metrics = load_trade_data()

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

# Visualization 1: Business Size Distribution (Donut Chart) - FIXED
with col1:
    st.markdown("### Commercial Institution Size Distribution")
    fig1 = px.pie(size_dist, values='Count', names='Institution Size', hole=0.5,
                  color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1'])
    
    # Enhanced text formatting for better visibility
    fig1.update_traces(
        textposition='inside', 
        textinfo='label+percent+value',
        textfont_size=12,
        textfont_color='white',
        texttemplate='<b>%{label}</b><br>%{percent}<br>(%{value:,})',
        pull=[0.02, 0.02, 0.02]  # Slightly separate slices
    )
    
    fig1.update_layout(
        height=200,
        template='plotly_white',
        margin=dict(l=10, r=10, t=5, b=10),
        font=dict(size=11),
        annotations=[dict(
            text=f'<b>Total</b><br>{size_dist["Count"].sum():,}', 
            x=0.5, y=0.5, 
            font_size=14, 
            font_color='black',
            showarrow=False
        )]
    )
    st.plotly_chart(fig1, use_container_width=True)

# Visualization 2: Economic Sector Distribution (Pie Chart) - FIXED
with col2:
    st.markdown("### Economic Sector Distribution")
    fig2 = px.pie(sector_data, values='Total Count', names='Sector',
                  color_discrete_sequence=['#FFD700', '#4169E1', '#8A2BE2'])
    
    # Enhanced text formatting for better visibility
    fig2.update_traces(
        textposition='inside', 
        textinfo='label+percent+value',
        textfont_size=12,
        textfont_color='white',
        texttemplate='<b>%{label}</b><br>%{percent}<br>(%{value:,})',
        pull=[0.02, 0.05, 0.05]  # Pull smaller slices out more
    )
    
    fig2.update_layout(
        height=200,
        template='plotly_white',
        margin=dict(l=10, r=10, t=5, b=10),
        font=dict(size=11)
    )
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)

# Visualization 3: Comprehensive Economic Activity Presence (Horizontal Bar) - FIXED
with col3:
    st.markdown("### Economic Activity Presence Across Towns")
    fig3 = px.bar(activity_data, y='Activity Type', x='Towns with Activity', orientation='h',
                  color='Towns with Activity', color_continuous_scale='RdYlGn',
                  text='Towns with Activity')
    
    # Add value labels and percentages on bars
    fig3.update_traces(
        texttemplate='<b>%{x}</b> towns<br>(%{customdata:.1f}%)',
        textposition='middle right',
        textfont_size=11,
        textfont_color='black',
        customdata=activity_data['Percentage']
    )
    
    fig3.update_layout(
        height=200,
        template='plotly_white',
        margin=dict(l=120, r=80, t=5, b=25),
        coloraxis_showscale=False,
        font=dict(size=11),
        xaxis_title='Number of Towns',
        yaxis_title=None
    )
    st.plotly_chart(fig3, use_container_width=True)

# Visualization 4: Banking Accessibility (Vertical Bar) - FIXED
with col4:
    st.markdown("### Banking Institution Accessibility")
    fig4 = px.bar(banking_data, x='Banking Access', y='Number of Towns',
                  color='Banking Access', color_discrete_sequence=['#1f77b4', '#ff7f0e'],
                  text='Number of Towns')
    
    # Enhanced bar labels with both count and percentage - simplified approach
    fig4.update_traces(
        texttemplate='<b>%{y:,}</b> towns',
        textposition='outside',
        textfont_size=12,
        textfont_color='black'
    )
    
    # Add percentage labels manually
    fig4.add_annotation(x=0, y=91 + 50, text='(8.0%)', showarrow=False, 
                       font=dict(size=11, color='darkblue'))
    fig4.add_annotation(x=1, y=1046 + 50, text='(92.0%)', showarrow=False, 
                       font=dict(size=11, color='darkorange'))
    
    fig4.update_layout(
        height=200,
        template='plotly_white',
        margin=dict(l=30, r=10, t=40, b=60),
        font=dict(size=11),
        showlegend=False,
        yaxis_title='Number of Towns',
        xaxis_title=None
    )
    
    st.plotly_chart(fig4, use_container_width=True)

# Visualization 5: Geographic Map of Commercial Centers in Lebanon (Scatter Mapbox) - ENHANCED
st.markdown("### Commercial Centers Distribution Across Lebanon")

# Create custom hover text
map_data['hover_text'] = map_data.apply(
    lambda row: f"<b>{row['Town']}</b><br>Businesses: {row['Total_All_Business']:,}", 
    axis=1
)

fig5 = px.scatter_mapbox(map_data, 
                        lat='lat', lon='lon', 
                        size='Total_All_Business',
                        color='Total_All_Business',
                        hover_name='Town',
                        hover_data={'Total_All_Business': ':,', 'lat': False, 'lon': False},
                        color_continuous_scale='Viridis',
                        size_max=25,
                        zoom=7,
                        center=dict(lat=33.8547, lon=35.8623))

# Add text labels for major cities
fig5.add_trace(go.Scattermapbox(
    lat=map_data['lat'],
    lon=map_data['lon'],
    mode='text',
    text=[f'<b>{town}</b><br>{count:,}' for town, count in zip(map_data['Town'], map_data['Total_All_Business'])],
    textfont=dict(size=10, color='black'),
    textposition='top center',
    showlegend=False,
    hoverinfo='skip'
))

fig5.update_layout(
    mapbox_style="open-street-map",
    height=300,
    margin=dict(l=0, r=0, t=0, b=0),
    coloraxis_showscale=True,
    coloraxis_colorbar=dict(
        title="Business Count",
        titlefont_size=12,
        tickfont_size=10
    )
)
st.plotly_chart(fig5, use_container_width=True)

# Footer
st.markdown("**MSBA 325 Trade Analysis | Commercial Institutions • Service Activities • Economic Distribution**")

# Trade insights
with st.expander("📈 Key Trade Insights"):
    col_i1, col_i2 = st.columns(2)
    with col_i1:
        st.markdown("""
        **Economic Structure:**
        - Small enterprises: 38,940 institutions (91.8% by volume)
        - Commercial sector dominates: 42,436 vs 1,768 service/financial
        - Limited large enterprise presence across Lebanon
        """)
    with col_i2:
        st.markdown("""
        **Economic Activity Distribution:**
        - Self employment most widespread: 722 towns (63.5%)
        - Commerce activity: 493 towns (43.4%)
        - Banking severely limited: only 91 towns (8.0%)
        """)
