import duckdb

print("🚀 Starting Load Phase...")

# Connect to DuckDB (This creates a local database file called lourides_warehouse.db)
con = duckdb.connect('lourides_warehouse.db')

# Create a table and load the clean CSV directly into it
con.execute("""
    CREATE OR REPLACE TABLE ds_fare_prediction_features AS 
    SELECT * FROM read_csv_auto('clean_data/clean_model_features.csv')
""")

# Verify the load
result = con.execute(
    "SELECT COUNT(*) FROM ds_fare_prediction_features").fetchone()
print(f"✅ Successfully loaded {result[0]} rows into DuckDB Data Warehouse.")

# Print a preview of the warehouse data
print("\n--- Data Warehouse Preview ---")
print(con.execute("SELECT trip_distance, temperature_2m, fare_amount FROM ds_fare_prediction_features LIMIT 5").fetchdf())

con.close()
