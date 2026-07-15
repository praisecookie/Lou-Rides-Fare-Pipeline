import pandas as pd
import requests
import json
from faker import Faker
import os
import random  # <--- Added this!

print("🚀 Starting Extraction Phase...")
os.makedirs("raw_data", exist_ok=True)

# 1. NYC TLC Taxi Data (Parquet) - Sampling 10,000 rows
try:
    df_taxi = pd.read_parquet('yellow_tripdata_2026-04.parquet')
    df_sampled = df_taxi.sample(n=10000, random_state=42)
    df_sampled.to_csv('raw_data/raw_rides.csv', index=False)
    print("✅ Source 1: 10,000 Taxi rides sampled and saved to CSV.")
except FileNotFoundError:
    print("❌ ERROR: Please download 'yellow_tripdata_2026-04.parquet' into this folder first.")
    exit()

# 2. Open-Meteo Weather API (JSON) - Hourly weather for Apr 2026
url = "https://archive-api.open-meteo.com/v1/archive?latitude=40.71&longitude=-74.01&start_date=2026-04-01&end_date=2026-04-30&hourly=temperature_2m,precipitation&timezone=America%2FNew_York"
response = requests.get(url)
with open('raw_data/raw_weather.json', 'w') as f:
    json.dump(response.json(), f)
print("✅ Source 2: Weather API data fetched and saved to JSON.")

# 3. Internal Driver Database (Faker) - Generating synthetic drivers
fake = Faker()
drivers = []
for _ in range(500):
    drivers.append({
        "Driver_ID": fake.uuid4(),
        "Name": fake.name(),
        "Vehicle_Type": fake.random_element(elements=('Sedan', 'SUV', 'Luxury')),
        "Rating": round(random.uniform(3.0, 5.0), 1),  # <--- Fixed this!
        "Join_Date": fake.date_between(start_date="-3y", end_date="today")
    })
df_drivers = pd.DataFrame(drivers)
df_drivers.to_csv('raw_data/raw_drivers.csv', index=False)
print("✅ Source 3: 500 Synthetic Driver profiles generated.")
