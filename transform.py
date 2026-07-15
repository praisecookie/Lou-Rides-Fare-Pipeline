import pandas as pd
import json
import random
import os

print("🚀 Starting Transformation Phase...")

# Load raw data
df_rides = pd.read_csv('raw_data/raw_rides.csv')
df_drivers = pd.read_csv('raw_data/raw_drivers.csv')
with open('raw_data/raw_weather.json', 'r') as f:
    weather_data = json.load(f)

# 1. Clean Ride Data (Handle Anomalies)
initial_count = len(df_rides)
df_rides = df_rides[(df_rides['passenger_count'] > 0) &
                    (df_rides['trip_distance'] > 0.0) &
                    (df_rides['fare_amount'] >= 2.50)]
print(
    f"🧹 Cleaned anomalies: Dropped {initial_count - len(df_rides)} invalid ride records.")

# Convert timestamps to datetime and floor to nearest hour for the weather join
df_rides['tpep_pickup_datetime'] = pd.to_datetime(
    df_rides['tpep_pickup_datetime'])
df_rides['pickup_hour'] = df_rides['tpep_pickup_datetime'].dt.floor('H')

# 2. Process Weather Data into a DataFrame
weather_df = pd.DataFrame({
    'time': pd.to_datetime(weather_data['hourly']['time']),
    'temperature_2m': weather_data['hourly']['temperature_2m'],
    'precipitation': weather_data['hourly']['precipitation']
})

# 3. The Big Join
# Merge rides with weather on the specific hour
df_merged = pd.merge(df_rides, weather_df,
                     left_on='pickup_hour', right_on='time', how='inner')

# Assign a random Driver_ID to each ride
driver_ids = df_drivers['Driver_ID'].tolist()
df_merged['Driver_ID'] = [random.choice(
    driver_ids) for _ in range(len(df_merged))]

# Select only the features the Data Science team needs
final_columns = [
    'Driver_ID', 'tpep_pickup_datetime', 'trip_distance', 'passenger_count',
    'temperature_2m', 'precipitation', 'fare_amount'
]
df_clean = df_merged[final_columns].dropna()

# Save transformed data
os.makedirs("clean_data", exist_ok=True)
df_clean.to_csv('clean_data/clean_model_features.csv', index=False)
print(
    f"✅ Data transformed and joined successfully! Final Dataset Shape: {df_clean.shape}")
