from pymongo import MongoClient
import json

# MongoDB Atlas connection string
MONGO_URI = "mongodb+srv://jpatil2670:6260162831@cluster0.bi5q8.mongodb.net/teerth-saarthi?retryWrites=true&w=majority"

# Connect to MongoDB
try:
    client = MongoClient(MONGO_URI)
    db = client['teerth-saarthi']
    print("Connected to MongoDB Atlas successfully!")
    
    # List of collections to examine
    collections_to_examine = [
        "buddhism",
        "christianities",
        "howtoreaches",
        "islam",
        "jainism",
        "sikhism",
        "temples",
        "transportation",
        "wheretostays"
    ]
    
    # Examine each collection
    for collection_name in collections_to_examine:
        try:
            collection = db[collection_name]
            count = collection.count_documents({})
            print(f"\n=== {collection_name.upper()} Collection ===")
            print(f"Contains {count} documents")
            
            # Get a sample document to examine structure
            if count > 0:
                sample_doc = collection.find_one()
                print(f"Sample document structure:")
                # Remove _id from output for cleaner display
                if "_id" in sample_doc:
                    del sample_doc["_id"]
                # Print sample document in pretty format
                print(json.dumps(sample_doc, indent=2, default=str))
            else:
                print("No documents to examine")
        except Exception as e:
            print(f"Error examining {collection_name}: {e}")
    
except Exception as e:
    print(f"Error connecting to MongoDB: {e}") 