import pymongo
import pprint
from bson.json_util import dumps
import json

# MongoDB connection parameters
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "religious_places_db"

# Collections to check
COLLECTIONS = [
    "places",
    "buddhism",
    "christianities",
    "islam",
    "jainism",
    "sikhism",
    "temples",
    "howtoreaches",
    "transportation",
    "wheretostays"
]

def check_database():
    """Check if the database and collections exist and contain data"""
    
    # Connect to MongoDB
    try:
        client = pymongo.MongoClient(MONGO_URI)
        db = client[DB_NAME]
        print(f"✓ Connected to MongoDB at {MONGO_URI}")
    except Exception as e:
        print(f"✗ Failed to connect to MongoDB: {e}")
        return
    
    # Check if database exists
    all_dbs = client.list_database_names()
    if DB_NAME in all_dbs:
        print(f"✓ Database '{DB_NAME}' exists")
    else:
        print(f"✗ Database '{DB_NAME}' does not exist")
        return
    
    # Check collections
    print("\nCollections Summary:")
    print("===================")
    
    for collection_name in COLLECTIONS:
        if collection_name in db.list_collection_names():
            count = db[collection_name].count_documents({})
            print(f"✓ Collection '{collection_name}' exists with {count} documents")
        else:
            print(f"✗ Collection '{collection_name}' does not exist")
    
    # Detailed inspection of each collection
    print("\nDetailed Collection Contents:")
    print("===========================")
    
    for collection_name in COLLECTIONS:
        if collection_name in db.list_collection_names():
            collection = db[collection_name]
            docs = list(collection.find().limit(3))  # Get first 3 documents for sample
            
            print(f"\n{collection_name.upper()} COLLECTION:")
            print("-" * 40)
            
            if not docs:
                print("Collection is empty")
                continue
            
            # Print sample document structure (first document)
            print("Document Structure:")
            document_fields = list(docs[0].keys())
            print(", ".join(document_fields))
            
            # Print sample documents
            print("\nSample Documents:")
            for i, doc in enumerate(docs):
                print(f"Document {i+1}:")
                # Convert ObjectId to string for better readability
                print(json.loads(dumps(doc)))
                print("-" * 30)
    
    # Check for place names across collections
    print("\nPlace Name Coverage:")
    print("===================")
    
    # Get all place names from the main places collection
    all_places = set()
    if "places" in db.list_collection_names():
        places = list(db["places"].find({}, {"name": 1}))
        all_places = {place.get("name") for place in places if "name" in place}
        print(f"✓ Found {len(all_places)} place names in 'places' collection")
    
    # Check each collection for these places
    for collection_name in COLLECTIONS:
        if collection_name == "places" or collection_name not in db.list_collection_names():
            continue
        
        collection = db[collection_name]
        place_coverage = {}
        
        for place in all_places:
            count = collection.count_documents({"name": place})
            if count > 0:
                place_coverage[place] = count
        
        coverage_percent = (len(place_coverage) / len(all_places)) * 100 if all_places else 0
        print(f"Collection '{collection_name}' covers {len(place_coverage)}/{len(all_places)} places ({coverage_percent:.1f}%)")
        
        # Show sample of covered places
        if place_coverage:
            sample_places = list(place_coverage.items())[:3]
            sample_str = ", ".join([f"{place} ({count} docs)" for place, count in sample_places])
            print(f"  Sample: {sample_str}...")

if __name__ == "__main__":
    check_database() 