import pandas as pd


def clean_data():
    print("⏳ Starting data pre-processing...")

    # --- PART 1: PREPARE CITIES (df4.csv) ---
    # We need to link City Name -> Department Code
    print("   ... Processing Cities (df4.csv)")
    df_cities = pd.read_csv('data/df4.csv', dtype={'dep_code': str})

    # Select only useful columns and rename them for clarity
    cities_db = df_cities[['nom_standard', 'dep_code', 'dep_nom', 'latitude_centre', 'longitude_centre']].copy()
    cities_db.rename(columns={
        'nom_standard': 'city_name',
        'latitude_centre': 'lat',
        'longitude_centre': 'lon'
    }, inplace=True)

    # Ensure department codes are 2 digits (e.g., "1" becomes "01") to match weather data
    cities_db['dep_code'] = cities_db['dep_code'].str.pad(width=2, side='left', fillchar='0')

    # Save optimized cities file
    cities_db.to_csv('data/cities_db.csv', index=False)

    # --- PART 2: PREPARE CLIMATE HISTORY (df0.csv) ---
    # We calculate the "Percentage of Frost" for every day of the year for each department
    print("   ... Processing Weather History (df0.csv)")
    df_weather = pd.read_csv('data/df0.csv', dtype={'Code INSEE département': str})

    # Rename and clean
    df_weather.rename(columns={
        'Date': 'date',
        'Code INSEE département': 'dep_code',
        'TMin (°C)': 'min_temp'
    }, inplace=True)

    # Ensure department codes are 2 digits
    df_weather['dep_code'] = df_weather['dep_code'].str.pad(width=2, side='left', fillchar='0')

    # Convert dates
    df_weather['date'] = pd.to_datetime(df_weather['date'])

    # Filter years (Exclude 2025 if it's forecast, keep valid history 2018-2024)
    # This creates our "Typical Year" dataset
    df_weather = df_weather[df_weather['date'].dt.year < 2025]

    # Extract Month and Day to group data across years
    df_weather['month'] = df_weather['date'].dt.month
    df_weather['day'] = df_weather['date'].dt.day

    # Define Frost: True (1) if Min Temp < 0, else False (0)
    df_weather['is_frost'] = (df_weather['min_temp'] < 0).astype(int)

    # --- AGGREGATION ---
    # We calculate the PROBABILITY of frost for each specific day (e.g. Jan 1st) in each department
    # Mean of 'is_frost' (0s and 1s) gives us the percentage (e.g., 0.40 = 40% chance)
    climate_stats = df_weather.groupby(['dep_code', 'month', 'day']).agg({
        'is_frost': 'mean',  # Frost Probability
        'min_temp': 'mean'  # Average Min Temp
    }).reset_index()

    # Create a dummy date for plotting (using year 2020 as it's a leap year, covers Feb 29)
    # This helps the chart display "Jan 1" to "Dec 31" nicely
    climate_stats['plot_date'] = pd.to_datetime(
        dict(year=2020, month=climate_stats['month'], day=climate_stats['day'])
    )

    # Save optimized climate file
    climate_stats.to_csv('data/frost_climate_db.csv', index=False)

    print("✅ Done! Created 'cities_db.csv' and 'frost_climate_db.csv'.")


if __name__ == "__main__":
    clean_data()