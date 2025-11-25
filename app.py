import streamlit as st
import pandas as pd
import plotly.express as px

# --- SETUP & CONFIG ---
st.set_page_config(page_title="Frost App", layout="wide")


# Load Data (Cached for performance)
@st.cache_data
def load_data():
    cities = pd.read_csv('data/cities_db.csv', dtype={'dep_code': str})
    climate = pd.read_csv('data/frost_climate_db.csv', dtype={'dep_code': str})
    # Convert 'plot_date' back to datetime for the chart
    climate['plot_date'] = pd.to_datetime(climate['plot_date'])
    return cities, climate


try:
    df_cities, df_climate = load_data()
except FileNotFoundError:
    st.error("⚠️ Data files not found. Please run the 'preprocess.py' script first!")
    st.stop()

# --- SIDEBAR: USER INPUTS ---
st.sidebar.title("🍇 Frost App Parameters")

# 1. Select City
selected_city = st.sidebar.selectbox(
    "Select a City (Commune):",
    options=df_cities['city_name'].sort_values().unique(),
    index=int(df_cities[df_cities['city_name'] == 'Ambérieu-en-Bugey'].index[0]) if 'Ambérieu-en-Bugey' in df_cities[
        'city_name'].values else 0
)

# 2. Select Date Range
st.sidebar.subheader("Observation Period")
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2023-04-30"))

# Retrieve Info for Selected City
city_info = df_cities[df_cities['city_name'] == selected_city].iloc[0]
dep_code = city_info['dep_code']
dep_name = city_info['dep_nom']

# --- MAIN LOGIC ---
# Filter climate data for this department
dept_data = df_climate[df_climate['dep_code'] == dep_code].copy()

# Sort by date
dept_data.sort_values('plot_date', inplace=True)

# Filter by user selected Day/Month range
# We map the user's selected dates to our "Typical Year" (2020) dates for comparison
mask_start = pd.Timestamp(year=2020, month=start_date.month, day=start_date.day)
mask_end = pd.Timestamp(year=2020, month=end_date.month, day=end_date.day)

if mask_start <= mask_end:
    period_data = dept_data[(dept_data['plot_date'] >= mask_start) & (dept_data['plot_date'] <= mask_end)]
else:
    # Handle wrap-around year (e.g. Dec to Jan)
    period_data = dept_data[(dept_data['plot_date'] >= mask_start) | (dept_data['plot_date'] <= mask_end)]

# Calculate Statistics
# Sum of probabilities = Expected number of frost days
expected_frost_days = period_data['is_frost'].sum()
avg_min_temp_period = period_data['min_temp'].mean()

# --- DASHBOARD UI ---
st.title(f"❄️ Frost Risk: {selected_city}")
st.markdown(
    f"**Department:** {dep_name} ({dep_code}) | **Analysis Period:** {start_date.strftime('%d %b')} - {end_date.strftime('%d %b')}")

# Top KPI Columns
col1, col2, col3 = st.columns(3)
col1.metric("Avg Frost Days", f"{expected_frost_days:.1f} days",
            help="Statistical expectation based on historical data")
col2.metric("Avg Min Temp", f"{avg_min_temp_period:.1f} °C")
col3.metric("Latitude", f"{city_info['lat']:.2f}")

# Two Columns: Chart and Map
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("📉 Temperature & Frost Evolution")

    # Create the Percentage Chart
    # X-Axis: Date, Y-Axis: Probability of Frost (0-100%)

    fig = px.line(
        period_data,
        x='plot_date',
        y=period_data['is_frost'] * 100,  # Convert to percentage
        title="Probability of Frost per Day (%)",
        labels={'plot_date': 'Date (Typical Year)', 'y': 'Frost Probability (%)'},
        markers=True
    )

    # Add a smooth line for average temperature on secondary axis (optional, but useful)
    fig.add_scatter(
        x=period_data['plot_date'],
        y=period_data['min_temp'],
        mode='lines',
        name='Avg Min Temp (°C)',
        yaxis='y2',
        line=dict(color='orange', dash='dot')
    )

    # Update layout for dual axis
    fig.update_layout(
        yaxis=dict(title="Frost Probability (%)", range=[0, 100]),
        yaxis2=dict(title="Temperature (°C)", overlaying='y', side='right'),
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("📍 Location")
    # Simple Map
    map_data = pd.DataFrame({'lat': [city_info['lat']], 'lon': [city_info['lon']]})
    st.map(map_data, zoom=8)

st.info(
    "ℹ️ Data based on Météo-France departmental averages (2018-2024). 'Probability' represents the frequency of frost observed on this specific day over the past years.")