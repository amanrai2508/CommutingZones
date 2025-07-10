#!/usr/bin/env python3
"""
Test script for geographic mapping functionality
"""

import pandas as pd
import json
import subprocess
import sys
from shapely.wkt import loads
import geopandas as gpd
import folium
from streamlit_folium import folium_static

def test_data_extraction():
    """Test if we can extract data with geometry from R"""
    print("Testing data extraction from R...")
    
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
    writeLines(json_data, "test_commuting_zones_data.json")
    
    cat("Data exported successfully\\n")
    '''
    
    # Write R script to file
    with open("test_extract_data.R", "w") as f:
        f.write(r_script)
    
    # Run R script
    result = subprocess.run(["Rscript", "test_extract_data.R"], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ R script executed successfully")
        return True
    else:
        print(f"❌ R script failed: {result.stderr}")
        return False

def test_data_loading():
    """Test if we can load the JSON data"""
    print("\nTesting data loading...")
    
    try:
        with open("test_commuting_zones_data.json", "r") as f:
            data = json.load(f)
        
        df = pd.DataFrame(data)
        print(f"✅ Data loaded successfully: {len(df)} rows")
        print(f"   Columns: {list(df.columns)}")
        
        # Check if geometry column exists
        if 'geography_wkt' in df.columns:
            print("✅ Geometry column found")
            return df
        else:
            print("❌ Geometry column not found")
            return None
            
    except Exception as e:
        print(f"❌ Error loading data: {str(e)}")
        return None

def test_geometry_parsing(df):
    """Test if we can parse WKT geometry"""
    print("\nTesting geometry parsing...")
    
    try:
        # Test with a few rows
        test_df = df.head(5).copy()
        test_df['geometry'] = test_df['geography_wkt'].apply(loads)
        
        print(f"✅ Geometry parsed successfully for {len(test_df)} rows")
        
        # Create GeoDataFrame
        gdf = gpd.GeoDataFrame(test_df, crs="EPSG:4326")
        print("✅ GeoDataFrame created successfully")
        
        return gdf
        
    except Exception as e:
        print(f"❌ Error parsing geometry: {str(e)}")
        return None

def test_map_creation(gdf):
    """Test if we can create a folium map"""
    print("\nTesting map creation...")
    
    try:
        # Calculate center
        center_lat = gdf.geometry.centroid.y.mean()
        center_lon = gdf.geometry.centroid.x.mean()
        
        # Create map
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=6,
            tiles='OpenStreetMap'
        )
        
        # Add a simple polygon
        for idx, row in gdf.iterrows():
            folium.GeoJson(
                row.geometry,
                style_function=lambda x: {
                    'fillColor': 'blue',
                    'color': 'black',
                    'weight': 1,
                    'fillOpacity': 0.7
                },
                popup=f"Zone: {row['fbcz_id']}"
            ).add_to(m)
        
        print("✅ Map created successfully")
        print(f"   Center: {center_lat:.4f}, {center_lon:.4f}")
        print(f"   Zones added: {len(gdf)}")
        
        return m
        
    except Exception as e:
        print(f"❌ Error creating map: {str(e)}")
        return None

def test_uk_data(df):
    """Test UK-specific data"""
    print("\nTesting UK data...")
    
    uk_data = df[df['country'] == 'United Kingdom']
    
    if len(uk_data) > 0:
        print(f"✅ UK data found: {len(uk_data)} zones")
        print(f"   Total population: {uk_data['win_population'].sum():,.0f}")
        print(f"   Total area: {uk_data['area'].sum():,.0f} km²")
        
        # Show some zone IDs
        zone_ids = uk_data['fbcz_id'].head(5).tolist()
        print(f"   Sample zones: {zone_ids}")
        
        return uk_data
    else:
        print("❌ No UK data found")
        return None

def main():
    """Run all tests"""
    print("🧪 Testing Geographic Mapping Functionality")
    print("=" * 50)
    
    # Test 1: Data extraction
    if not test_data_extraction():
        print("❌ Data extraction failed. Stopping tests.")
        return
    
    # Test 2: Data loading
    df = test_data_loading()
    if df is None:
        print("❌ Data loading failed. Stopping tests.")
        return
    
    # Test 3: UK data
    uk_data = test_uk_data(df)
    if uk_data is None:
        print("❌ UK data not found. Stopping tests.")
        return
    
    # Test 4: Geometry parsing
    gdf = test_geometry_parsing(uk_data.head(3))
    if gdf is None:
        print("❌ Geometry parsing failed. Stopping tests.")
        return
    
    # Test 5: Map creation
    map_obj = test_map_creation(gdf)
    if map_obj is None:
        print("❌ Map creation failed. Stopping tests.")
        return
    
    print("\n" + "=" * 50)
    print("🎉 All tests passed! Geographic mapping is working correctly.")
    print("\nYou can now run the Streamlit app with:")
    print("streamlit run app.py")
    
    # Save test map
    map_obj.save("test_map.html")
    print("\nTest map saved as: test_map.html")

if __name__ == "__main__":
    main() 