import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import json
from io import StringIO
import subprocess
import sys
import os
import folium
from streamlit_folium import folium_static
import geopandas as gpd
from shapely.wkt import loads
import branca.colormap as cm

# Page configuration
st.set_page_config(
    page_title="European Commuting Zones Explorer",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .zone-info {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .map-container {
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_commuting_zones_data():
    """Load commuting zones data using R script"""
    try:
        # Create R script to extract data with geometry
        r_script = '''
        library(CommutingZones)
        library(dplyr)
        library(jsonlite)
        library(sf)
        
        # Load data
        data(cz_data)
        
        # Convert to data frame and handle geometry
        cz_df <- as.data.frame(cz_data)
        
        # Keep geometry for mapping
        cz_df$geography_wkt <- as.character(cz_data$geography)
        
        # Convert to JSON
        json_data <- toJSON(cz_df, pretty = TRUE)
        
        # Write to file
        writeLines(json_data, "commuting_zones_data.json")
        
        # Also create a summary
        summary_data <- cz_df %>%
          group_by(country) %>%
          summarise(
            total_zones = n(),
            total_population = sum(win_population, na.rm = TRUE),
            total_area = sum(area, na.rm = TRUE),
            avg_population = mean(win_population, na.rm = TRUE),
            avg_area = mean(area, na.rm = TRUE)
          )
        
        summary_json <- toJSON(summary_data, pretty = TRUE)
        writeLines(summary_json, "summary_data.json")
        
        cat("Data exported successfully\\n")
        '''
        
        # Write R script to file
        with open("extract_data.R", "w") as f:
            f.write(r_script)
        
        # Run R script
        result = subprocess.run(["Rscript", "extract_data.R"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            # Load the JSON data
            with open("commuting_zones_data.json", "r") as f:
                data = json.load(f)
            
            with open("summary_data.json", "r") as f:
                summary = json.load(f)
            
            return pd.DataFrame(data), pd.DataFrame(summary)
        else:
            st.error(f"Error running R script: {result.stderr}")
            return None, None
            
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None

@st.cache_data
def get_available_countries(data):
    """Get list of available countries"""
    if data is not None:
        return sorted(data['country'].unique())
    return []

def create_geographic_map(data, selected_country, map_type="population"):
    """Create a geographic map of commuting zones using folium"""
    if data is None or selected_country is None:
        return None
    
    # Filter data for selected country
    country_data = data[data['country'] == selected_country].copy()
    
    if len(country_data) == 0:
        return None
    
    try:
        # Convert WKT to GeoDataFrame
        country_data['geometry'] = country_data['geography_wkt'].apply(loads)
        gdf = gpd.GeoDataFrame(country_data, crs="EPSG:4326")
        
        # Calculate center of the map
        center_lat = gdf.geometry.centroid.y.mean()
        center_lon = gdf.geometry.centroid.x.mean()
        
        # Create base map
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=6,
            tiles='OpenStreetMap'
        )
        
        # Choose color column based on map type
        if map_type == "population":
            color_column = 'win_population'
            color_map = cm.LinearColormap(
                colors=['lightblue', 'darkblue'],
                vmin=gdf[color_column].min(),
                vmax=gdf[color_column].max(),
                caption='Population'
            )
        else:  # area
            color_column = 'area'
            color_map = cm.LinearColormap(
                colors=['lightgreen', 'darkgreen'],
                vmin=gdf[color_column].min(),
                vmax=gdf[color_column].max(),
                caption='Area (km²)'
            )
        
        # Add zones to map
        for idx, row in gdf.iterrows():
            # Get color for this zone
            color = color_map(row[color_column])
            
            # Create popup content
            popup_content = f"""
            <b>Zone: {row['fbcz_id']}</b><br>
            Population: {row['win_population']:,.0f}<br>
            Area: {row['area']:,.1f} km²<br>
            Roads: {row['win_roads_km']:,.1f} km
            """
            
            # Add polygon to map
            folium.GeoJson(
                row.geometry,
                style_function=lambda x, color=color: {
                    'fillColor': color,
                    'color': 'black',
                    'weight': 1,
                    'fillOpacity': 0.7
                },
                popup=folium.Popup(popup_content, max_width=300),
                tooltip=f"Zone: {row['fbcz_id']}"
            ).add_to(m)
        
        # Add color map to map
        color_map.add_to(m)
        
        return m
        
    except Exception as e:
        st.error(f"Error creating map: {str(e)}")
        return None

def create_commuting_zones_map(data, selected_country):
    """Create an interactive map of commuting zones for selected country"""
    if data is None or selected_country is None:
        return None
    
    # Filter data for selected country
    country_data = data[data['country'] == selected_country].copy()
    
    if len(country_data) == 0:
        return None
    
    # Create choropleth map
    fig = px.choropleth(
        country_data,
        locations='fbcz_id',
        color='win_population',
        hover_data=['fbcz_id', 'win_population', 'area', 'win_roads_km'],
        title=f"Commuting Zones - {selected_country}",
        color_continuous_scale='plasma',
        labels={'win_population': 'Population', 'fbcz_id': 'Zone ID'}
    )
    
    fig.update_layout(
        height=600,
        title_x=0.5,
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    return fig

def create_population_area_comparison(data, selected_country):
    """Create comparison charts for population and area"""
    if data is None or selected_country is None:
        return None
    
    country_data = data[data['country'] == selected_country].copy()
    
    if len(country_data) == 0:
        return None
    
    # Create subplots
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Population by Zone', 'Area by Zone'),
        specs=[[{"type": "bar"}, {"type": "bar"}]]
    )
    
    # Population chart
    fig.add_trace(
        go.Bar(
            x=country_data['fbcz_id'],
            y=country_data['win_population'],
            name='Population',
            marker_color='lightblue'
        ),
        row=1, col=1
    )
    
    # Area chart
    fig.add_trace(
        go.Bar(
            x=country_data['fbcz_id'],
            y=country_data['area'],
            name='Area (km²)',
            marker_color='lightgreen'
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        height=500,
        title_text=f"Zone Comparison - {selected_country}",
        title_x=0.5,
        showlegend=False
    )
    
    fig.update_xaxes(tickangle=45)
    
    return fig

def create_zone_details_table(data, selected_country):
    """Create detailed table of zones"""
    if data is None or selected_country is None:
        return None
    
    country_data = data[data['country'] == selected_country].copy()
    
    if len(country_data) == 0:
        return None
    
    # Select relevant columns and format
    display_data = country_data[['fbcz_id', 'win_population', 'area', 'win_roads_km']].copy()
    display_data['win_population'] = display_data['win_population'].apply(lambda x: f"{x:,.0f}")
    display_data['area'] = display_data['area'].apply(lambda x: f"{x:,.1f}")
    display_data['win_roads_km'] = display_data['win_roads_km'].apply(lambda x: f"{x:,.1f}" if pd.notna(x) else "N/A")
    
    display_data.columns = ['Zone ID', 'Population', 'Area (km²)', 'Roads (km)']
    
    return display_data

def main():
    # Header
    st.markdown('<h1 class="main-header">🗺️ European Commuting Zones Explorer</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["Overview", "Geographic Maps", "Country Analysis", "Zone Details", "About"]
    )
    
    # Load data
    with st.spinner("Loading commuting zones data..."):
        data, summary = load_commuting_zones_data()
    
    if data is None:
        st.error("Failed to load data. Please check if the CommutingZones R package is installed.")
        st.stop()
    
    # Main content based on selected page
    if page == "Overview":
        show_overview(data, summary)
    elif page == "Geographic Maps":
        show_geographic_maps(data)
    elif page == "Country Analysis":
        show_country_analysis(data)
    elif page == "Zone Details":
        show_zone_details(data)
    elif page == "About":
        show_about()

def show_overview(data, summary):
    """Show overview page"""
    st.header("🌍 European Commuting Zones Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Countries", len(summary))
    
    with col2:
        total_zones = summary['total_zones'].sum()
        st.metric("Total Zones", f"{total_zones:,}")
    
    with col3:
        total_pop = summary['total_population'].sum()
        st.metric("Total Population", f"{total_pop:,.0f}")
    
    with col4:
        total_area = summary['total_area'].sum()
        st.metric("Total Area", f"{total_area:,.0f} km²")
    
    # Top countries by zones
    st.subheader("Top Countries by Number of Commuting Zones")
    top_countries = summary.nlargest(10, 'total_zones')
    
    fig = px.bar(
        top_countries,
        x='country',
        y='total_zones',
        title="Top 10 Countries by Number of Commuting Zones",
        labels={'total_zones': 'Number of Zones', 'country': 'Country'}
    )
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)
    
    # Summary table
    st.subheader("Country Summary")
    st.dataframe(summary, use_container_width=True)

def show_geographic_maps(data):
    """Show geographic maps page"""
    st.header("🗺️ Geographic Maps")
    st.markdown("Explore commuting zones on actual geographic maps with real boundaries.")
    
    # Country selection
    countries = get_available_countries(data)
    selected_country = st.selectbox("Select a country:", countries, index=countries.index("United Kingdom") if "United Kingdom" in countries else 0)
    
    if selected_country:
        # Map type selection
        map_type = st.radio("Choose map type:", ["Population", "Area"], horizontal=True)
        
        # Create geographic map
        st.subheader(f"Geographic Map - {selected_country} ({map_type})")
        
        with st.spinner("Creating geographic map..."):
            map_obj = create_geographic_map(data, selected_country, map_type.lower())
        
        if map_obj:
            # Display the map
            st.markdown('<div class="map-container">', unsafe_allow_html=True)
            folium_static(map_obj, width=800, height=600)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Map controls
            col1, col2 = st.columns(2)
            with col1:
                st.info("💡 **Map Tips:**")
                st.markdown("""
                - Click on zones to see detailed information
                - Hover over zones for zone IDs
                - Use the color legend to understand the scale
                - Zoom and pan to explore different areas
                """)
            
            with col2:
                st.info("🗺️ **Map Features:**")
                st.markdown("""
                - Real geographic boundaries
                - Population/Area color coding
                - Interactive popups with zone details
                - OpenStreetMap base layer
                """)
        else:
            st.warning("Could not create geographic map. Check if geometry data is available.")
        
        # Zone statistics
        country_data = data[data['country'] == selected_country]
        if len(country_data) > 0:
            st.subheader("Zone Statistics")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Zones", len(country_data))
            
            with col2:
                total_pop = country_data['win_population'].sum()
                st.metric("Total Population", f"{total_pop:,.0f}")
            
            with col3:
                total_area = country_data['area'].sum()
                st.metric("Total Area", f"{total_area:,.0f} km²")
            
            with col4:
                avg_pop = country_data['win_population'].mean()
                st.metric("Avg Population/Zone", f"{avg_pop:,.0f}")

def show_country_analysis(data):
    """Show country analysis page"""
    st.header("🏛️ Country Analysis")
    
    # Country selection
    countries = get_available_countries(data)
    selected_country = st.selectbox("Select a country:", countries, index=countries.index("United Kingdom") if "United Kingdom" in countries else 0)
    
    if selected_country:
        # Filter data for selected country
        country_data = data[data['country'] == selected_country]
        
        # Key metrics for selected country
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Zones", len(country_data))
        
        with col2:
            total_pop = country_data['win_population'].sum()
            st.metric("Total Population", f"{total_pop:,.0f}")
        
        with col3:
            total_area = country_data['area'].sum()
            st.metric("Total Area", f"{total_area:,.0f} km²")
        
        with col4:
            avg_pop = country_data['win_population'].mean()
            st.metric("Avg Population/Zone", f"{avg_pop:,.0f}")
        
        # Geographic map
        st.subheader("Geographic Map")
        map_type = st.radio("Map type:", ["Population", "Area"], horizontal=True, key="analysis_map")
        
        with st.spinner("Creating map..."):
            map_obj = create_geographic_map(data, selected_country, map_type.lower())
        
        if map_obj:
            folium_static(map_obj, width=800, height=500)
        else:
            st.warning("No map data available for this country.")
        
        # Population and Area comparison
        st.subheader("Zone Comparison")
        comp_fig = create_population_area_comparison(data, selected_country)
        if comp_fig:
            st.plotly_chart(comp_fig, use_container_width=True)
        
        # Top zones
        st.subheader("Top 10 Zones by Population")
        top_zones = country_data.nlargest(10, 'win_population')[['fbcz_id', 'win_population', 'area']]
        top_zones['win_population'] = top_zones['win_population'].apply(lambda x: f"{x:,.0f}")
        top_zones['area'] = top_zones['area'].apply(lambda x: f"{x:,.1f}")
        st.dataframe(top_zones, use_container_width=True)

def show_zone_details(data):
    """Show detailed zone information"""
    st.header("📍 Zone Details")
    
    # Country selection
    countries = get_available_countries(data)
    selected_country = st.selectbox("Select a country:", countries, key="zone_country", index=countries.index("United Kingdom") if "United Kingdom" in countries else 0)
    
    if selected_country:
        # Zone selection
        country_data = data[data['country'] == selected_country]
        zone_ids = sorted(country_data['fbcz_id'].unique())
        selected_zone = st.selectbox("Select a zone:", zone_ids)
        
        if selected_zone:
            zone_data = country_data[country_data['fbcz_id'] == selected_zone].iloc[0]
            
            # Zone details
            st.subheader(f"Zone: {selected_zone}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="zone-info">
                    <h4>Population</h4>
                    <p>{zone_data['win_population']:,.0f} people</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="zone-info">
                    <h4>Area</h4>
                    <p>{zone_data['area']:,.1f} km²</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="zone-info">
                    <h4>Roads</h4>
                    <p>{zone_data['win_roads_km']:,.1f} km</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="zone-info">
                    <h4>Region</h4>
                    <p>{zone_data['region']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Zone map
            st.subheader("Zone Location")
            zone_map = create_geographic_map(data, selected_country, "population")
            if zone_map:
                folium_static(zone_map, width=600, height=400)
            
            # All zones table
            st.subheader("All Zones in Selected Country")
            zones_table = create_zone_details_table(data, selected_country)
            if zones_table is not None:
                st.dataframe(zones_table, use_container_width=True)

def show_about():
    """Show about page"""
    st.header("ℹ️ About")
    
    st.markdown("""
    ## European Commuting Zones Explorer
    
    This application allows you to explore commuting zones across Europe on actual geographic maps. Commuting zones are geographic areas where people live and work, providing insights into local economies and social connectivity.
    
    ### What are Commuting Zones?
    
    Commuting zones represent areas where people spend the majority of their time, based on actual commuting patterns rather than political boundaries. They help understand:
    
    - **Economic integration** across regions
    - **Commute patterns** and travel behavior
    - **Local labor markets** and economic communities
    - **Infrastructure connectivity** and development
    
    ### Geographic Maps
    
    The application now features real geographic maps showing:
    - **Actual zone boundaries** based on WKT geometry data
    - **Interactive popups** with detailed zone information
    - **Color-coded visualization** by population or area
    - **OpenStreetMap base layer** for geographic context
    
    ### Data Source
    
    The data comes from Meta's Data for Good initiative and includes:
    - Population estimates for each zone
    - Geographic area measurements
    - Road infrastructure data
    - Zone boundaries and identifiers
    - WKT geometry for mapping
    
    ### How to Use
    
    1. **Overview**: See summary statistics across all European countries
    2. **Geographic Maps**: Explore zones on real geographic maps
    3. **Country Analysis**: Interactive analysis with maps and charts
    4. **Zone Details**: Get detailed information about individual zones
    
    ### Citation
    
    If you use this data in your research, please cite:
    - Data for Good at Meta
    - Include a link to: https://dataforgood.facebook.com/dfg/tools/commuting-zones
    """)

if __name__ == "__main__":
    main() 