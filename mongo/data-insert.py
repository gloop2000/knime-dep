import pandas as pd
from pymongo import MongoClient
import os

# 1. Setup Connection (Adjust credentials if different)
uri = "mongodb://localhost:27017/"
client = MongoClient(uri)

# 2. Define Database and Collection
db = client['health_data']
collection = db['diabetes']

# 3. Locate the CSV
# Replace 'path' with the actual string from your kagglehub download output
path = "/home/testbed/Downloads/archive/diabetes.csv" 

if os.path.exists(path):
    # Load data with Pandas
    df = pd.read_csv(path)
    
    # Convert DataFrame to a list of dictionaries (JSON-like)
    data_dict = df.to_dict("records")
    
    # 4. Insert into Mongo
    print(f"Inserting {len(data_dict)} records...")
    collection.insert_many(data_dict)
    print("Success! Data indexed in 'health_data.diabetes' collection.")
else:
    print("Error: CSV file not found at the specified path.")

# 5. Verify a sample record
print("Sample record from DB:", collection.find_one())