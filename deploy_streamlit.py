#!/usr/bin/env python3
"""
Streamlit Cloud Deployment Helper

This script helps prepare the app for Streamlit Cloud deployment by:
1. Creating a fallback data mechanism when R is not available
2. Setting up proper configuration
3. Providing deployment instructions
"""

import os
import json
import subprocess
import sys

def create_streamlit_config():
    """Create Streamlit configuration for cloud deployment"""
    config_content = """
[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
"""
    
    with open(".streamlit/config.toml", "w") as f:
        f.write(config_content)
    
    print("✅ Created Streamlit configuration")

def create_packages_file():
    """Create packages.txt for system dependencies"""
    packages_content = """
# System packages needed for geographic data processing
libgeos-dev
libproj-dev
proj-data
proj-bin
libgdal-dev
gdal-bin
"""
    
    with open("packages.txt", "w") as f:
        f.write(packages_content)
    
    print("✅ Created packages.txt for system dependencies")

def create_deployment_readme():
    """Create deployment instructions"""
    readme_content = """
# Streamlit Cloud Deployment

## Quick Deploy

1. **Fork this repository** to your GitHub account
2. **Go to [Streamlit Cloud](https://share.streamlit.io/)**
3. **Connect your GitHub account**
4. **Deploy the app**:
   - Repository: `your-username/CommutingZones`
   - Main file path: `app.py`
   - Python version: 3.9+

## What This App Does

This Streamlit app explores European commuting zones with:

- **Geographic Maps**: Real WKT geometry boundaries on OpenStreetMap
- **Interactive Visualizations**: Population and area analysis
- **Country Comparison**: Multi-country data exploration
- **Zone Details**: Individual zone information and statistics

## Demo Mode

When deployed on Streamlit Cloud (where R is not available), the app automatically switches to **Demo Mode** using sample data that demonstrates:

- 67 UK commuting zones with realistic population/area data
- Geographic boundaries for mapping
- All interactive features working

## Local Development

For full functionality with real data:

```bash
# Install R and required packages
R -e "install.packages(c('CommutingZones', 'dplyr', 'jsonlite', 'sf'))"

# Install Python dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## Features

✅ **Geographic Maps**: Real boundaries on OpenStreetMap  
✅ **Interactive Popups**: Zone details on click  
✅ **Color Coding**: Population/area visualization  
✅ **Multi-page Navigation**: Overview, Maps, Analysis, Details  
✅ **Responsive Design**: Works on desktop and mobile  
✅ **Demo Mode**: Works without R dependencies  

## Data Source

- **Meta Data for Good**: Commuting Zones dataset
- **Geographic Data**: WKT geometry boundaries
- **Population Data**: Facebook population estimates
- **Infrastructure**: Road network data

## Support

For issues or questions:
- Check the app's "About" page for more information
- Review the deployment logs in Streamlit Cloud
- Ensure all dependencies are properly installed
"""
    
    with open("STREAMLIT_DEPLOYMENT.md", "w") as f:
        f.write(readme_content)
    
    print("✅ Created deployment instructions")

def test_app():
    """Test if the app can run without R"""
    try:
        # Test importing the main modules
        import streamlit as st
        import pandas as pd
        import plotly.express as px
        import folium
        from streamlit_folium import folium_static
        import geopandas as gpd
        from shapely.wkt import loads
        
        print("✅ All Python dependencies available")
        
        # Test sample data creation
        from app import create_sample_data
        data, summary = create_sample_data()
        print(f"✅ Sample data created: {len(data)} zones")
        
        return True
        
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing app: {e}")
        return False

def main():
    """Main deployment preparation"""
    print("🚀 Preparing Streamlit Cloud Deployment...")
    
    # Create necessary directories
    os.makedirs(".streamlit", exist_ok=True)
    
    # Create configuration files
    create_streamlit_config()
    create_packages_file()
    create_deployment_readme()
    
    # Test the app
    if test_app():
        print("\n🎉 Deployment preparation complete!")
        print("\n📋 Next steps:")
        print("1. Commit and push these changes to GitHub")
        print("2. Go to https://share.streamlit.io/")
        print("3. Connect your repository")
        print("4. Deploy with main file: app.py")
        print("\n📖 See STREAMLIT_DEPLOYMENT.md for detailed instructions")
    else:
        print("\n❌ App testing failed. Please check dependencies.")
        sys.exit(1)

if __name__ == "__main__":
    main() 