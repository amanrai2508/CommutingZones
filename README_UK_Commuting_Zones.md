# UK Commuting Zones Visualization

This repository contains scripts to help you plot and analyze commuting zones for the United Kingdom using the CommutingZones R package.

## What are Commuting Zones?

Commuting zones are geographic areas where people live and work, useful for understanding local economies and how they differ from traditional political boundaries. These zones are built using aggregated estimates of home and work locations.

## Files Included

1. **`simple_uk_commuting_zones.R`** - A simple, easy-to-use script for plotting UK commuting zones
2. **`plot_uk_commuting_zones.R`** - A comprehensive script with advanced features and analysis
3. **`README_UK_Commuting_Zones.md`** - This documentation file

## Prerequisites

Before running the scripts, you need to install the required R packages:

```r
# Install the CommutingZones package
install.packages("remotes")
remotes::install_github("facebookincubator/CommutingZones")

# Install additional required packages
install.packages(c("ggplot2", "sf", "dplyr", "maps", "mapdata"))

# Optional: For interactive plots
install.packages("plotly")
```

## Quick Start

### Option 1: Simple Script (Recommended for beginners)

```r
# Load the simple script
source("simple_uk_commuting_zones.R")

# The script will automatically run and show you:
# 1. What UK data is available
# 2. Summary statistics
# 3. Population-based map
# 4. Area-based map
```

### Option 2: Comprehensive Script

```r
# Load the comprehensive script
source("plot_uk_commuting_zones.R")

# This script provides more advanced features including:
# - Interactive maps
# - Detailed analysis
# - Multiple visualization options
```

## Manual Usage

If you prefer to use the functions manually:

```r
# Check what UK data is available
uk_countries <- check_uk_data()

# Get summary statistics
summary_data <- get_uk_summary("United Kingdom")

# Create population-based plot
population_plot <- plot_uk_zones("United Kingdom")
print(population_plot)

# Create area-based plot
area_plot <- plot_uk_zones_area("United Kingdom")
print(area_plot)
```

## Working with Specific UK Locations

If the package doesn't include UK commuting zones data, you can work with specific UK locations:

```r
library(CommutingZones)

# Create a dataset with UK locations
uk_locations <- data.frame(
  location = c("London", "Manchester", "Birmingham", "Liverpool", "Leeds", 
               "Sheffield", "Bristol", "Glasgow", "Edinburgh", "Cardiff"),
  country = c("United Kingdom", "United Kingdom", "United Kingdom", "United Kingdom", "United Kingdom",
              "United Kingdom", "United Kingdom", "United Kingdom", "United Kingdom", "United Kingdom")
)

# Get commuting zones for these locations
uk_zones <- commuting_zones(
  data = uk_locations,
  location_col_name = "location",
  country_col_name = "country",
  gmaps_key = "YOUR_GOOGLE_MAPS_API_KEY"  # You'll need to get this from Google
)

# Plot the results
plot(uk_zones)
```

## Getting a Google Maps API Key

To use the `commuting_zones()` function with specific locations, you need a Google Maps API key:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Geocoding API
4. Create credentials (API key)
5. Replace `"YOUR_GOOGLE_MAPS_API_KEY"` with your actual API key

## Available Functions

### Simple Script Functions

- `check_uk_data()` - Check what UK-related countries are available in the dataset
- `get_uk_summary(country_name)` - Get summary statistics for a country
- `plot_uk_zones(country_name)` - Create a population-based map
- `plot_uk_zones_area(country_name)` - Create an area-based map
- `example_uk_plot()` - Run a complete example

### Comprehensive Script Functions

- `check_uk_availability()` - Detailed availability check
- `plot_uk_commuting_zones()` - Advanced plotting with multiple options
- `analyze_uk_commuting_zones()` - Detailed statistical analysis
- `create_interactive_uk_map()` - Create interactive maps (requires plotly)

## Troubleshooting

### No UK Data Found

If you get a message saying no UK data is found:

1. Check what countries are available: `check_uk_data()`
2. The UK might be listed under a different name (e.g., "Great Britain", "England")
3. The dataset might not include UK data - in this case, use the specific locations approach

### Package Installation Issues

If you have trouble installing the CommutingZones package:

```r
# Try installing from CRAN first
install.packages("CommutingZones")

# If that doesn't work, try the GitHub version
install.packages("remotes")
remotes::install_github("facebookincubator/CommutingZones")
```

### Google Maps API Issues

If you get errors with the Google Maps API:

1. Make sure your API key is valid
2. Ensure the Geocoding API is enabled
3. Check if you have billing set up (required for Google Maps API)

## Output Examples

The scripts will generate:

1. **Population-based maps** - Shows commuting zones colored by population density
2. **Area-based maps** - Shows commuting zones colored by geographic area
3. **Summary statistics** - Total zones, population, area, and averages
4. **Interactive maps** - Zoomable and clickable maps (if plotly is installed)

## Data Source

The commuting zones data comes from Meta's Data for Good initiative and is available at: https://dataforgood.facebook.com/dfg/tools/commuting-zones

## Citation

If you use this data in your research, please cite:
- Data for Good at Meta
- Include a link to the Commuting Zones page: https://dataforgood.facebook.com/dfg/tools/commuting-zones

## License

This project is MIT licensed, as found in the LICENSE file. 