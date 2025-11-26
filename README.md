# Frost App - Frost Risk Assessment Tool

## Project Overview
Frost App is a data visualization tool built with Streamlit, designed to assist winemakers and agricultural professionals in assessing frost risks in France.

By analyzing historical weather data (2018-2024), the application calculates the probability of frost events (temperatures dropping below 0 C) for specific geographical locations. It generates a "Typical Year" model, allowing users to visualize temperature evolution and frost frequency over a user-defined period (e.g., the critical budburst phase in spring).

## Features
- **City-Level Granularity:** Users can select specific communes in France to analyze local climate risks.
- **Historical Analysis:** Data is aggregated from departmental weather records spanning 2018 to 2024 to create robust probability models.
- **Interactive Risk Chart:** Displays a dual-axis graph showing:
  - Daily probability of frost (percentage chance based on history).
  - Average minimum daily temperature.
- **Geospatial Visualization:** Interactive map locating the selected commune.
- **Customizable Date Ranges:** Users can filter the analysis for specific observation windows (e.g., January 1st to April 30th).


## Data Sources & Methodology
The application utilizes a combination of administrative and meteorological datasets:

1. **Administrative Data (df4.csv):** Provides the mapping between French communes (cities) and their respective departments and coordinates.
2. **Meteorological History (df0.csv):** Contains daily minimum temperatures for French departments.

**Calculation Logic:**
The application does not rely on a single year's weather. Instead, it computes a probabilistic model:
- **Frost Definition:** Any day where the minimum temperature is strictly less than 0°C.
- **Probability Calculation:** For every day of the year (e.g., April 15th), the system calculates the frequency of frost events over the available historical years. A probability of 20% implies that frost occurred on that specific day in 20% of the recorded years.

## Installation and Setup

### 1. Clone the Repository
Clone the project to your local machine:
git clone https://github.com/your-username/frost-app.git
cd frost-app

### 2. Set Up a Virtual Environment (Recommended)
It is best practice to run Python projects in a virtual environment.

**Windows:**
python -m venv .venv
.venv\Scripts\activate

**macOS/Linux:**
python3 -m venv .venv
source .venv/bin/activate

### 3. Install Dependencies
Install the required Python libraries.
pip install streamlit pandas plotly

## Usage

### Step 1: Data Pre-processing
Before running the application for the first time, you must process the raw data files in the data/ folder. This script generates the optimized files (cities_db.csv and frost_climate_db.csv) used by the app for performance.

Run the following command in your terminal:
python preprocess.py

*Wait for the script to confirm that the database files have been created.*

### Step 2: Running the Application
Launch the Streamlit interface:
streamlit run app.py

The application will open automatically in your default web browser at http://localhost:8501.

### Output Example

<img src="Capture d'écran 2025-11-26 093207.png" alt="Frost App Screenshot" width="1814"/>

## Future Improvements
- Integration of 2025 forecast data to compare historical averages against current predictions.
- Expansion of the dataset to include station-specific data (from df.csv) for higher precision in micro-climates.
- Alerting system implementation for upcoming frost risks.