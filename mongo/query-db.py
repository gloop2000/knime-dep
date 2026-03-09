from pymongo import MongoClient

# 1. Connection Details
uri = "mongodb://localhost:27017/"
client = MongoClient(uri)

# 2. Access the database and collection
db = client['health_data']
collection = db['diabetes']

def get_head(limit=5):
    print(f"--- Fetching the first {limit} records ---\n")
    
    # .find({}) returns all docs, .limit(n) restricts the count
    results = collection.find({}).limit(limit)
    
    for i, doc in enumerate(results, 1):
        # We remove the MongoDB internal _id for a cleaner print
        doc.pop('_id', None) 
        print(f"Record {i}: {doc}")

if __name__ == "__main__":
    try:
        # Check if the collection actually has data first
        count = collection.count_documents({})
        if count == 0:
            print("The collection is empty. Did you run the import script?")
        else:
            get_head(5)
    except Exception as e:
        print(f"Connection Error: {e}")