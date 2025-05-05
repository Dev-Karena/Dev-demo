from pymongo import MongoClient

# MongoDB Atlas connection string
MONGO_URI = "mongodb+srv://jpatil2670:6260162831@cluster0.bi5q8.mongodb.net/teerth-saarthi?retryWrites=true&w=majority"

# Connect to MongoDB
try:
    client = MongoClient(MONGO_URI)
    db = client['teerth-saarthi']
    print("Connected to MongoDB Atlas successfully!")
    
    # Get list of all collections in the database
    collections = db.list_collection_names()
    print(f"Found {len(collections)} collections in the database:")
    for collection in collections:
        print(f"- {collection}")
    
    # Check for the specific collections mentioned
    required_collections = [
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
    
    print("\nChecking for required collections:")
    for collection in required_collections:
        if collection in collections:
            print(f"✓ {collection} exists")
            # Count documents in the collection
            count = db[collection].count_documents({})
            print(f"  Contains {count} documents")
        else:
            print(f"✗ {collection} does not exist")
    
except Exception as e:
    print(f"Error connecting to MongoDB: {e}") 