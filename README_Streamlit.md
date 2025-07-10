# 🗺️ European Commuting Zones Explorer - Streamlit App

An interactive web application for exploring commuting zones across Europe, with a focus on the UK. This app allows you to visualize and analyze commuting zones data from Meta's Data for Good initiative.

## 🌟 Features

### 📊 **Overview Dashboard**
- Total statistics across all European countries
- Top countries by number of commuting zones
- Summary tables with key metrics

### 🏛️ **Country Analysis**
- Interactive country selection (UK-focused by default)
- Commuting zones maps with population data
- Population vs Area comparison charts
- Top zones by population rankings

### 📍 **Zone Details**
- Detailed information for individual commuting zones
- Population, area, and infrastructure data
- Complete zone listings for each country

## 🚀 Quick Start

### Prerequisites

1. **R and R packages** (for data processing):
   ```r
   install.packages("remotes")
   remotes::install_github("facebookincubator/CommutingZones")
   install.packages(c("dplyr", "jsonlite"))
   ```

2. **Python and pip** (for the web app):
   ```bash
   python --version  # Should be 3.8 or higher
   pip --version
   ```

### Installation

1. **Clone or download the files** to your local machine

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** and go to the URL shown in the terminal (usually `http://localhost:8501`)

## 📱 How to Use

### Navigation
The app has four main sections accessible from the sidebar:

1. **Overview** - See summary statistics for all European countries
2. **Country Analysis** - Explore specific countries (UK is selected by default)
3. **Zone Details** - Get detailed information about individual zones
4. **About** - Learn more about commuting zones and the data source

### UK Analysis (Default Focus)
When you open the app:
- The UK is automatically selected in the Country Analysis section
- You can see all 67 UK commuting zones
- Interactive maps show population distribution
- Charts compare population vs area across zones

### Exploring Other Countries
- Use the country dropdown to select any European country
- Each country shows its unique commuting zones data
- Maps and charts update automatically

## 📊 Data Insights

### UK Commuting Zones Highlights:
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

## 🔧 Technical Details

### Architecture
- **Frontend**: Streamlit web interface
- **Data Processing**: R scripts using CommutingZones package
- **Visualization**: Plotly interactive charts
- **Data Format**: JSON export from R to Python

### Key Files
- `app.py` - Main Streamlit application
- `requirements.txt` - Python dependencies
- `extract_data.R` - R script for data extraction (auto-generated)
- `commuting_zones_data.json` - Exported data (auto-generated)
- `summary_data.json` - Summary statistics (auto-generated)

### Data Flow
1. R script loads CommutingZones data
2. Data is exported to JSON format
3. Python reads JSON and creates interactive visualizations
4. Streamlit serves the web interface

## 🛠️ Troubleshooting

### Common Issues

**"Failed to load data" error:**
- Ensure R is installed and accessible from command line
- Check that CommutingZones package is installed: `R -e "library(CommutingZones)"`
- Verify all R dependencies are installed

**"No module named 'streamlit'" error:**
- Install requirements: `pip install -r requirements.txt`
- Or install manually: `pip install streamlit pandas plotly numpy`

**App runs but no data appears:**
- Check that the R script executed successfully
- Look for generated JSON files in the directory
- Check R console output for errors

### Performance Tips
- The app caches data loading for faster subsequent runs
- Large datasets may take a few seconds to load initially
- Use the sidebar to navigate between sections efficiently

## 📈 Future Enhancements

Potential improvements for the application:
- **Geographic maps** with actual zone boundaries
- **City search** functionality
- **Time series analysis** of zone changes
- **Export capabilities** for reports and data
- **Comparison tools** between countries
- **Mobile-responsive design** improvements

## 📚 Data Source & Citation

### Data Source
- **Meta Data for Good**: https://dataforgood.facebook.com/dfg/tools/commuting-zones
- **Dataset**: Commuting Zones March 2023
- **Coverage**: Global commuting zones based on Facebook location data

### Citation
If you use this data in your research, please cite:
- Data for Good at Meta
- Include a link to: https://dataforgood.facebook.com/dfg/tools/commuting-zones

## 🤝 Contributing

Feel free to contribute to this project by:
- Reporting bugs or issues
- Suggesting new features
- Improving documentation
- Adding new visualizations

## 📄 License

This project is MIT licensed, as found in the LICENSE file.

---

**Enjoy exploring European commuting zones!** 🗺️✨ 