
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
