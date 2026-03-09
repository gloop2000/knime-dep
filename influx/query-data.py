import influxdb_client_3 as influxdb


# 1. Configuration
DATABASE = "bmw_sales"
TOKEN = "apiv3_2A5PBZxv2vG0HDY5JAmmRkNI8DuLzRKodLDzVhcQeI0i-paCbCukwkwO3VgWBAmB-1egn5HZ5QdfDbc8a8yUVQ"
HOST = "http://127.0.0.1:8181" # Update to your region

# 2. Initialize Client
client = influxdb.InfluxDBClient3(
    host=HOST,
    token=TOKEN,
    database=DATABASE
)

# 3. SQL Query
query = 'SELECT * FROM "bmw_sales" LIMIT 5'

try:
    # Execute query - returns an Arrow Table
    table = client.query(query=query, language="sql")
    
    # Convert the Arrow Table to a Pandas DataFrame
    df = table.to_pandas()
    
    print("--- Head of 'bmw_sales' ---")
    print(df)

except Exception as e:
    print(f"Query failed: {e}")

finally:
    client.close()