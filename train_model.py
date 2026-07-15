import duckdb
import warnings
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

# Suppress sklearn warnings for cleaner terminal output
warnings.filterwarnings("ignore")

print("🧪 Starting Data Science Handoff...")

# 1. Connect to the Data Engineer's Warehouse
con = duckdb.connect('lourides_warehouse.db')
df = con.execute(
    "SELECT trip_distance, temperature_2m, precipitation, fare_amount FROM ds_fare_prediction_features").fetchdf()

# 2. Define Features (X) and Target Fare (y)
X = df[['trip_distance', 'temperature_2m', 'precipitation']]
y = df['fare_amount']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# 3. Train the Predictive Model
model = LinearRegression()
model.fit(X_train, y_train)

# 4. Evaluate the Model
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)

print(f"✅ Machine Learning Model Trained Successfully!")
print(
    f"📉 Mean Absolute Error: ${mae:.2f} (The model's prediction is off by this much on average)")

# 5. Simulate a live user requesting a ride in the Lou Rides App
# Example inputs: 5.2 miles distance, 15.0 degrees Celsius, 0.0mm precipitation
sample_ride = [[5.2, 15.0, 0.0]]
est_fare = model.predict(sample_ride)[0]

print(f"\n📱 APP DISPLAY:")
print(
    f"🚕 A 5.2 mile ride in 15.0°C weather is estimated to cost: ${est_fare:.2f}")

con.close()
