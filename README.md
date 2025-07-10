# 🗺️ European Commuting Zones Explorer

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://commuting-zones-explorer.streamlit.app)

An interactive web application for exploring commuting zones across Europe, with a focus on the UK. This app visualizes commuting zones data from Meta's Data for Good initiative on actual geographic maps.

## 🌟 Live Demo

**🚀 [View the Live App](https://commuting-zones-explorer.streamlit.app)**

## 📊 What are Commuting Zones?

Commuting zones are geographic areas where people live and work, providing insights into local economies and social connectivity. They represent areas where people spend the majority of their time, based on actual commuting patterns rather than political boundaries.

### Key Benefits:
- **Economic integration** across regions
- **Commute patterns** and travel behavior
- **Local labor markets** and economic communities
- **Infrastructure connectivity** and development

## 🗺️ Features

### 📊 **Overview Dashboard**
- Total statistics across all European countries
- Top countries by number of commuting zones
- Summary tables with key metrics

### 🗺️ **Geographic Maps** (NEW!)
- **Real geographic boundaries** using WKT geometry data
- **Interactive maps** with OpenStreetMap base layer
- **Population and Area visualization** with color coding
- **Clickable zones** with detailed information popups
- **Zoom and pan** functionality

### 🏛️ **Country Analysis**
- Interactive country selection (UK-focused by default)
- Geographic maps with real zone boundaries
- Population vs Area comparison charts
- Top zones by population rankings

### 📍 **Zone Details**
- Detailed information for individual commuting zones
- Population, area, and infrastructure data
- Geographic location visualization
- Complete zone listings for each country

## 🚀 Quick Start

### Option 1: Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/european-commuting-zones.git
   cd european-commuting-zones
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install R and required packages:**
   ```r
   install.packages("remotes")
   remotes::install_github("facebookincubator/CommutingZones")
   install.packages(c("dplyr", "jsonlite", "sf"))
   ```

4. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** and go to `http://localhost:8501`

### Option 2: Deploy to Streamlit Cloud

1. **Fork this repository** to your GitHub account

2. **Go to [Streamlit Cloud](https://streamlit.io/cloud)**

3. **Connect your GitHub account** and select this repository

4. **Deploy** - Streamlit Cloud will automatically detect the app and deploy it

5. **Share the URL** with others!

## 📊 UK Commuting Zones Highlights

- **67 total zones** across the United Kingdom
- **63.6 million people** total population
- **245,565 km²** total area
- **Average zone size**: 3,665 km²
- **Average population per zone**: 949,010 people

### Top UK Zones by Population:
1. **Europe457** - 4.4M people (London area)
2. **Europe400** - 4.4M people (Greater London)
3. **Europe394** - 4.4M people (South East)
4. **Europe459** - 4.4M people (Midlands)
5. **Europe389** - 2.9M people (South West)

## 🛠️ Technical Architecture

### Frontend
- **Streamlit** - Web application framework
- **Plotly** - Interactive charts and visualizations
- **Folium** - Geographic mapping with OpenStreetMap

### Backend
- **Python** - Main application logic
- **R** - Data processing with CommutingZones package
- **GeoPandas** - Geographic data manipulation
- **Shapely** - Geometry operations

### Data Flow
1. R script loads CommutingZones data
2. Data is exported to JSON format with WKT geometry
3. Python reads JSON and creates interactive visualizations
4. Streamlit serves the web interface

## 📁 Project Structure

```
european-commuting-zones/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── .streamlit/
│   └── config.toml                # Streamlit configuration
├── data/                          # Data files (auto-generated)
├── R/                             # R scripts (auto-generated)
└── docs/                          # Documentation
```

## 🔧 Configuration

### Streamlit Configuration
The app uses a custom theme and configuration in `.streamlit/config.toml`:
- Custom color scheme
- Server settings for deployment
- Performance optimizations

### Data Sources
- **Meta Data for Good**: https://dataforgood.facebook.com/dfg/tools/commuting-zones
- **Dataset**: Commuting Zones March 2023
- **Coverage**: Global commuting zones based on Facebook location data

## 🚀 Deployment Options

### 1. Streamlit Cloud (Recommended)
- Free hosting for public repositories
- Automatic deployment from GitHub
- Built-in analytics and monitoring

### 2. Heroku
- Create a `Procfile` with: `web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
- Add buildpacks for Python and R

### 3. Docker
- Create a Dockerfile for containerized deployment
- Deploy to any cloud platform

### 4. Local Server
- Run on your own server with proper R and Python installations
- Configure reverse proxy for production use

## 📈 Future Enhancements

- [ ] **City search** functionality
- [ ] **Time series analysis** of zone changes
- [ ] **Export capabilities** for reports and data
- [ ] **Comparison tools** between countries
- [ ] **Mobile-responsive design** improvements
- [ ] **Additional map layers** (satellite, terrain)
- [ ] **Zone boundary downloads** in various formats

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt
pip install black flake8 pytest

# Run tests
pytest

# Format code
black app.py
```

## 📚 Data Source & Citation

### Data Source
- **Meta Data for Good**: https://dataforgood.facebook.com/dfg/tools/commuting-zones
- **Dataset**: Commuting Zones March 2023
- **Coverage**: Global commuting zones based on Facebook location data

### Citation
If you use this data in your research, please cite:
- Data for Good at Meta
- Include a link to: https://dataforgood.facebook.com/dfg/tools/commuting-zones

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Meta Data for Good** for providing the commuting zones data
- **Streamlit** for the amazing web app framework
- **OpenStreetMap** for the base map tiles
- **GeoPandas and Folium** for geographic visualization

## 📞 Support

If you encounter any issues or have questions:

1. **Check the [Issues](https://github.com/yourusername/european-commuting-zones/issues)** page
2. **Create a new issue** with detailed information
3. **Contact the maintainers** for direct support

---

**Enjoy exploring European commuting zones!** 🗺️✨

[![GitHub stars](https://img.shields.io/github/stars/yourusername/european-commuting-zones?style=social)](https://github.com/yourusername/european-commuting-zones)
[![GitHub forks](https://img.shields.io/github/forks/yourusername/european-commuting-zones?style=social)](https://github.com/yourusername/european-commuting-zones)
[![GitHub issues](https://img.shields.io/github/issues/yourusername/european-commuting-zones)](https://github.com/yourusername/european-commuting-zones/issues)
