from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pymongo import MongoClient
import re
import os
import traceback
import json
from bson import ObjectId

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# MongoDB Atlas connection string
MONGO_URI = "mongodb+srv://jpatil2670:6260162831@cluster0.bi5q8.mongodb.net/teerth-saarthi?retryWrites=true&w=majority"
PORT = 5000

# Global variables for collections
db = None
places_collection = None
buddhism_collection = None
christianities_collection = None
islam_collection = None
jainism_collection = None
sikhism_collection = None
temples_collection = None
howtoreaches_collection = None
transportation_collection = None
wheretostays_collection = None

# Connect to MongoDB
try:
    client = MongoClient(MONGO_URI)
    db = client['teerth-saarthi']
    
    # Initialize all collections
    places_collection = db['places']
    buddhism_collection = db['buddhism']
    christianities_collection = db['christianities']
    islam_collection = db['islam']
    jainism_collection = db['jainism']
    sikhism_collection = db['sikhism']
    temples_collection = db['temples']
    howtoreaches_collection = db['howtoreaches']
    transportation_collection = db['transportation']
    wheretostays_collection = db['wheretostays']
    
    print("Connected to MongoDB Atlas successfully!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

# Helper class to handle MongoDB ObjectId serialization
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/api/status')
def api_status():
    return jsonify({"status": "API is running"})

@app.route('/styles.css')
def styles():
    return send_file('styles.css')

@app.route('/script.js')
def script():
    return send_file('script.js')

@app.route('/api/message', methods=['POST'])
def handle_message():
    try:
        data = request.json
        user_message = data.get('message', '').lower()
        
        # Process the user message and get a response
        response = get_response(user_message)
        
        return jsonify({"response": response})
    except Exception as e:
        print(f"Error in handle_message: {e}")
        traceback.print_exc()
        return jsonify({"response": f"Sorry, I encountered an error: {str(e)}. Please try again later."}), 500

def get_response(message):
    # Check if MongoDB is connected
    if db is None:
        return "Sorry, I'm having trouble connecting to the database. Please try again later."
    
    # Log the incoming message for debugging
    print(f"Processing message: '{message}'")
    
    # Check for specific query types
    if any(word in message.lower() for word in ['hello', 'hi', 'hey']):
        return "Hello! I'm your Teerth Saarthi assistant. How can I help you with information about religious places, transportation, or accommodations today?"
    
    # Extract info about query type and place name
    query_type, place_name, religion_type = extract_query_info(message)
    print(f"Extracted place name: '{place_name}', Query type: '{query_type}', Religion: '{religion_type}'")
    
    # If we have a religion type but no specific place, list places for that religion
    if religion_type and not place_name:
        return get_places_by_religion(religion_type)
    
    # If we have a place name, find it in the database
    if place_name:
        try:
            # Try to find the place across all collections
            place = find_place_in_collections(place_name)
            
            if place:
                print(f"Found place in database: {place.get('name', place_name)}")
                
                # Handle different query types
                if query_type == "history":
                    return get_history_response(place)
                elif query_type == "transport":
                    return get_transport_response(place)
                elif query_type == "accommodation":
                    return get_accommodation_response(place)
                elif query_type == "attraction":
                    return get_attraction_response(place)
                elif query_type == "location":
                    return get_location_response(place)
                else:
                    # No specific query type detected, provide a general response
                    print(f"Returning general info for {place.get('name', place_name)}")
                    return f"I have information about {place.get('name', place_name)}. You can ask about its history, nearby tourist attractions, transportation options, accommodations, or location."
            else:
                return f"I don't have specific information about {place_name}. Could you ask about another religious place or be more specific?"
        except Exception as e:
            print(f"Database lookup error: {e}")
            traceback.print_exc()
            return f"I'm having trouble retrieving information about {place_name} right now. Please try again later."
    
    # If we have a query type but no place name
    if query_type and not place_name:
        if query_type == "history":
            return "I can provide historical information about various religious places. Could you specify which place you're interested in?"
        elif query_type == "transport":
            return "I can help with transportation options to religious sites. Please specify which place you want to visit."
        elif query_type == "accommodation":
            return "I can recommend accommodations near religious places. Please specify the location you're interested in."
        elif query_type == "attraction":
            return "There are many attractions near religious sites. Could you specify which place you're interested in?"
        elif query_type == "location":
            return "I can help you find the location of religious places. Please specify which place you're looking for."
    
    # Default response if we couldn't extract any specific info
    return "I'm here to help with information about religious places, their history, transportation options, accommodations, and nearby attractions. Could you please ask about a specific religious place or religion?"

def extract_query_info(message):
    """
    Extract query type, place name, and religion type from the message
    """
    message_lower = message.lower()
    
    # Determine query type
    query_type = None
    
    # Check for accommodation queries first (higher priority)
    if any(word in message_lower for word in ["accommodation", "hotel", "stay", "lodging", "dharamshala"]) or "near" in message_lower and any(word in message_lower for word in ["hotel", "stay", "accommodation"]):
        query_type = "accommodation"
    # Then check for transport queries
    elif any(phrase in message_lower for phrase in ["how to reach", "how do i reach", "how to get", "transport", "travel"]) or "how do i get to" in message_lower:
        query_type = "transport"
    # Then attractions
    elif any(word in message_lower for word in ["attraction", "tourist", "visit", "places to visit", "nearby"]):
        query_type = "attraction"
    # Then location
    elif any(word in message_lower for word in ["location", "address", "where is", "situated"]):
        query_type = "location"
    # Default to history for general inquiries
    elif any(word in message_lower for word in ["history", "about", "tell me about", "what is", "what's the history"]):
        query_type = "history"
    
    # Extract place name
    place_name = extract_place_name(message)
    
    # Extract religion type
    religion_type = None
    religion_keywords = {
        "hindu": "Hinduism",
        "temple": "Hinduism",
        "mandir": "Hinduism",
        "buddhist": "Buddhism",
        "buddha": "Buddhism",
        "stupa": "Buddhism",
        "christian": "Christianity",
        "church": "Christianity",
        "basilica": "Christianity",
        "cathedral": "Christianity",
        "islam": "Islam",
        "muslim": "Islam",
        "mosque": "Islam",
        "dargah": "Islam",
        "jain": "Jainism",
        "jainism": "Jainism",
        "sikh": "Sikhism",
        "gurdwara": "Sikhism"
    }
    
    for keyword, religion in religion_keywords.items():
        if keyword in message_lower:
            religion_type = religion
            break
    
    print(f"Extracted query type: '{query_type}' for message: '{message}'")
    return query_type, place_name, religion_type

def extract_place_name(message):
    try:
        # Log the input message for debugging
        print(f"Extracting place name from: '{message}'")
        
        # Special direct handling for known problematic queries
        message_lower = message.lower()
        if "khatu shyam temple history" in message_lower or "khatu shyam history" in message_lower:
            print("Special direct match for 'Khatu Shyam Temple history'")
            return "Shree Khatu Shyam Mandir"
        
        if "ranakpur jain temple" in message_lower or "what's the history of ranakpur" in message_lower:
            print("Special direct match for Ranakpur Jain Temple")
            return "Ranakpur Jain Temple"
            
        if "dilwara temples" in message_lower or "reach dilwara" in message_lower:
            print("Special direct match for Dilwara Temples")
            return "Dilwara Temples"
            
        # Handle specific history queries for known places
        if "history of vatican city" in message_lower:
            print("Special direct match for Vatican City")
            return "Vatican City"
            
        if "history of varanasi" in message_lower:
            print("Special direct match for Varanasi")
            return "Varanasi"
            
        if "history of somnath temple" in message_lower or "what is the history of somnath temple" in message_lower:
            print("Special direct match for Somnath Temple")
            return "Somnath Temple"
            
        if "history of khwaja gharib nawaz dargah sharif" in message_lower or "tell me about the history of khwaja gharib nawaz dargah sharif" in message_lower:
            print("Special direct match for Khwaja Gharib Nawaz Dargah Sharif")
            return "Khwaja Gharib Nawaz Dargah Sharif"
        
        # More comprehensive temple name lookup
        common_temple_names = {
            "khatu shyam temple": "Shree Khatu Shyam Mandir",
            "khatu shyam": "Shree Khatu Shyam Mandir",
            "khatu": "Shree Khatu Shyam Mandir",
            "shyam temple": "Shree Khatu Shyam Mandir",
            "shyam mandir": "Shree Khatu Shyam Mandir",
            "mahakaleshwar": "Mahakaleshwar Temple",
            "mahakal": "Mahakaleshwar Temple",
            "somnath": "Somnath Temple",
            "venkateshwara": "Venkateshwara Temple",
            "tirupati": "Venkateshwara Temple",
            "balaji": "Venkateshwara Temple",
            "mehandipur": "Mehandipur Balaji Temple",
            "amarnath": "Amarnath Temple",
            "kamakhya": "Kamakhya Temple",
            "mallikarjuna": "Mallikarjuna Temple",
            "omkareshwar": "Omkareshwar Temple",
            "bhimashankar": "Bhimashankar Temple",
            "trimbakeshwar": "Trimbakeshwar Temple",
            "baidyanath": "Baidyanath Temple",
            "nageshwar": "Nageshwar Temple",
            "grishneshwar": "Grishneshwar Temple",
            "golden temple": "Golden Temple",
            "kashi vishwanath": "Kashi Vishwanath Temple",
            "varanasi": "Varanasi",
            "bodhgaya": "Bodhgaya",
            "ajmer sharif": "Khwaja Gharib Nawaz Dargah Sharif",
            "vatican": "Vatican City",
            "vatican city": "Vatican City",
            "basilica": "Basilica of Bom Jesus",
            "bom jesus": "Basilica of Bom Jesus",
            "palitana": "Palitana Jain Temples",
            "sammed shikharji": "Shri Sammed Shikharji",
            "parasnath": "Shri Sammed Shikharji",
            "ranakpur": "Ranakpur Jain Temple",
            "dilwara": "Dilwara Temples",
            "mount abu": "Dilwara Temples",
            "kulpakji": "Kulpakji Jain Temple",
            "kolanupaka": "Kulpakji Jain Temple",
            "khwaja gharib nawaz": "Khwaja Gharib Nawaz Dargah Sharif",
            "ajmer dargah": "Khwaja Gharib Nawaz Dargah Sharif",
            "dargah sharif": "Khwaja Gharib Nawaz Dargah Sharif"
        }
        
        # First check for direct matches in our lookup table
        for key, value in common_temple_names.items():
            if key in message_lower:
                print(f"Found direct match: '{key}' -> '{value}'")
                return value
        
        # Get all place names from various collections
        all_places = []
        
        # Check places collection
        if places_collection is not None:
            places_cursor = places_collection.find({}, {"name": 1, "_id": 0})
            all_places.extend([place["name"] for place in places_cursor])
            
        # Check other religion-specific collections
        for collection in [buddhism_collection, christianities_collection, islam_collection, 
                          jainism_collection, sikhism_collection, temples_collection]:
            if collection is not None:
                places_cursor = collection.find({}, {"name": 1, "_id": 0})
                all_places.extend([place["name"] for place in places_cursor])
        
        # Check for substring matches in database names
        for place in all_places:
            if place.lower() in message_lower:
                print(f"Found database match: '{place}'")
                return place
        
        # Try to extract the place name from common patterns in questions
        location_patterns = [
            r"about (.+?)(?:\s+history|\s+information|\s*$)",
            r"history of (.+?)(?:\s+is|\s*$)",
            r"tell me about (.+?)(?:\s+history|\s*$)",
            r"what is the history of (.+?)(?:\s*\?*$)",
            r"tell me about the history of (.+?)(?:\s*\?*$)",
            r"(.+?)(?:\s+temple|\s+mandir|\s+history|\s+information)"
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, message_lower)
            if match:
                potential_place = match.group(1).strip()
                print(f"Extracted potential place from pattern: '{potential_place}'")
                
                # Check if this potential place might be a known temple
                for place in all_places:
                    place_lower = place.lower()
                    # Check if the extracted text is part of any temple name
                    if (potential_place in place_lower or 
                        any(word in place_lower for word in potential_place.split() if len(word) > 3)):
                        print(f"Found pattern match: '{potential_place}' -> '{place}'")
                        return place
                
                # If no match in database, check our common names dictionary
                for key, value in common_temple_names.items():
                    if (potential_place in key or 
                        any(word in key for word in potential_place.split() if len(word) > 3)):
                        print(f"Found pattern match in common names: '{potential_place}' -> '{value}'")
                        return value
        
        print("No place name found")
        return None
    except Exception as e:
        print(f"Error in place name extraction: {e}")
        traceback.print_exc()
        return None

def find_place_in_collections(place_name):
    """
    Find place information across all collections
    """
    place = None
    
    # Define all collections to search
    collections = [
        places_collection,
        buddhism_collection, 
        christianities_collection, 
        islam_collection,
        jainism_collection, 
        sikhism_collection, 
        temples_collection
    ]
    
    # Search each collection for the place
    for collection in collections:
        if collection is None:
            continue
            
        # Try exact match
        place = collection.find_one({"name": place_name})
        if place:
            break
            
        # Try case-insensitive match
        place = collection.find_one({"name": {"$regex": f"^{re.escape(place_name)}$", "$options": "i"}})
        if place:
            break
            
        # Try partial match
        place = collection.find_one({"name": {"$regex": f"{re.escape(place_name)}", "$options": "i"}})
        if place:
            break
    
    # If not found, try more flexible matching
    if not place:
        for collection in collections:
            if collection is None:
                continue
                
            all_places = list(collection.find())
            for p in all_places:
                if place_name.lower() in p["name"].lower() or p["name"].lower() in place_name.lower():
                    place = p
                    break
            if place:
                break
    
    return place

def get_places_by_religion(religion):
    """
    Get a list of places for a specific religion
    """
    places = []
    collection = None
    
    # Determine which collection to use based on religion
    if religion == "Hinduism":
        collection = temples_collection
    elif religion == "Buddhism":
        collection = buddhism_collection
    elif religion == "Christianity":
        collection = christianities_collection
    elif religion == "Islam":
        collection = islam_collection
    elif religion == "Jainism":
        collection = jainism_collection
    elif religion == "Sikhism":
        collection = sikhism_collection
    
    # Get places from the collection
    if collection is not None:
        places_cursor = collection.find({}, {"name": 1, "address": 1, "_id": 0})
        places = list(places_cursor)
    
    # If no places found, try the general places collection
    if not places and places_collection is not None:
        places_cursor = places_collection.find({"religion": religion}, {"name": 1, "address": 1, "_id": 0})
        places = list(places_cursor)
    
    # Format the response
    if places:
        response = f"Here are some {religion} places you can explore:\n"
        for place in places:
            response += f"- {place['name']}"
            if 'address' in place:
                response += f" ({place['address']})"
            response += "\n"
        response += "\nYou can ask me about any of these places for more details."
        return response
    else:
        return f"I don't have information about {religion} places at the moment. Please try asking about a specific place instead."

def get_history_response(place):
    """
    Get historical information about a place
    """
    print(f"Returning history for {place.get('name', 'this place')}")
    
    # Try different fields that might contain historical information
    if 'history' in place and place['history']:
        return place['history']
    elif 'description' in place and place['description']:
        return place['description']
    else:
        return f"I have information about {place.get('name', 'this place')}, but no specific history details. Would you like to know something else about it?"

def get_transport_response(place):
    """
    Get transportation information for a place
    """
    print(f"Returning transportation info for {place.get('name', 'this place')}")
    place_name = place.get('name', 'this place')
    
    # Check if we have a place_id to query howtoreaches collection
    place_id = place.get('_id')
    
    # Try to get transport info from howtoreaches collection
    transport_info = []
    if place_id is not None and howtoreaches_collection is not None:
        transport_options = list(howtoreaches_collection.find({"temple_id": place_id}))
        if not transport_options:  # Try by name if id doesn't match
            transport_options = list(howtoreaches_collection.find({"temple_name": place_name}))
        
        if transport_options:
            for option in transport_options:
                transport_info.append(f"- {option.get('transport_type')}: {option.get('station_name')} ({option.get('distance_km')} km away), Fare: Rs. {option.get('fare')}, Travel time: {option.get('travel_time')}")
    
    # If not found in howtoreaches, try transportation collection
    if not transport_info and transportation_collection is not None:
        transport_options = list(transportation_collection.find({"temple_name": place_name}))
        if transport_options:
            for option in transport_options:
                transport_info.append(f"- {option.get('transport_type')}: {option.get('station_name')} ({option.get('distance_km')} km away), Fare: Rs. {option.get('fare')}, Travel time: {option.get('travel_time')}")
    
    # If not found in specific collections, try the transport field in the place document
    if not transport_info and 'transportation' in place:
        transport = place['transportation']
        for mode, details in transport.items():
            transport_info.append(f"- {mode.capitalize()}: {details}")
    
    # Format the response
    if transport_info:
        response = f"Transportation options to {place_name}:\n" + "\n".join(transport_info)
        return response
    else:
        return f"I don't have specific transportation information for {place_name} at the moment."

def get_accommodation_response(place):
    """
    Generate a response with accommodation information for a given place
    """
    print(f"Getting accommodation response for {place.get('name')}")
    place_id = place.get("_id")
    place_name = place.get("name")
    
    # Check wheretostays collection first
    accommodation_info = None
    if wheretostays_collection is not None:
        print(f"Checking wheretostays_collection by place_id")
        accommodation_info = wheretostays_collection.find_one({"place_id": place_id})
        
        # If not found by ID, try by name
        if not accommodation_info:
            print(f"Checking wheretostays_collection by place_name")
            accommodation_info = wheretostays_collection.find_one({"place_name": place_name})
            
            # Try case-insensitive name
            if not accommodation_info:
                print(f"Trying case-insensitive place_name search")
                accommodation_info = wheretostays_collection.find_one(
                    {"place_name": {"$regex": f"^{re.escape(place_name)}$", "$options": "i"}}
                )
    
    # If found in wheretostays collection
    if accommodation_info:
        print(f"Found accommodation info in wheretostays collection")
        accommodations = accommodation_info.get("accommodations", [])
        if accommodations:
            response = f"Here are some accommodation options near {place_name}:\n\n"
            for acc in accommodations:
                name = acc.get("name", "")
                description = acc.get("description", "")
                if name:
                    response += f"• {name}"
                    if description:
                        response += f": {description}"
                    response += "\n"
            return response
    
    # Check if place document has accommodations field
    print(f"Checking if place document has accommodations field")
    accommodations = []
    if not accommodation_info and 'accommodations' in place:
        print(f"Using accommodations field from place document for {place_name}")
        accommodations = place['accommodations']
    
    # Format response
    if accommodations:
        print(f"Found {len(accommodations)} accommodations")
        response = f"Here are some accommodation options near {place_name}:\n\n"
        if isinstance(accommodations, list):
            for acc in accommodations:
                if isinstance(acc, dict):
                    name = acc.get("name", "")
                    description = acc.get("description", "")
                    if name:
                        response += f"• {name}"
                        if description:
                            response += f": {description}"
                        response += "\n"
                else:
                    response += f"• {acc}\n"
        else:
            response = f"Accommodation information for {place_name}: {accommodations}"
        return response
    
    print(f"No accommodation information found for {place_name}")
    return f"I'm having trouble retrieving accommodation information for {place_name}. Please try again later or check with local tourism offices for accommodation options."

def get_attraction_response(place):
    """
    Get nearby attractions information for a place
    """
    print(f"Returning attraction info for {place.get('name', 'this place')}")
    
    # Try to get attractions from the nearby_places field
    if 'nearby_places' in place:
        tourist_places = place['nearby_places']
        if tourist_places:
            response = f"Here are some tourist attractions near {place.get('name', 'this place')}:\n"
            for spot in tourist_places:
                if isinstance(spot, dict):
                    response += f"- {spot.get('name')}"
                    if 'distance_km' in spot:
                        response += f" ({spot.get('distance_km')} km away)"
                    if 'description' in spot:
                        response += f": {spot.get('description')}"
                    response += "\n"
                else:
                    response += f"- {spot}\n"
            return response
    
    # Try to get attractions from the nearby_attractions field
    if 'nearby_attractions' in place:
        tourist_places = place['nearby_attractions']
        if tourist_places:
            return f"Here are some tourist attractions near {place.get('name', 'this place')}: {', '.join(tourist_places)}"
    
    return f"I don't have information about tourist attractions near {place.get('name', 'this place')} at the moment."

def get_location_response(place):
    """
    Get location information for a place
    """
    print(f"Returning location info for {place.get('name', 'this place')}")
    
    # Try to get location from the location field
    if 'location' in place:
        location = place['location']
        if isinstance(location, dict):
            address = location.get('address', 'Address not available')
            description = location.get('description', '')
            
            # Check if we have coordinates
            coords = ""
            if 'latitude' in location and 'longitude' in location:
                coords = f" (Coordinates: {location['latitude']}, {location['longitude']})"
            
            return f"{place.get('name', 'This place')} is located at: {address}{coords}. {description}"
    
    # Try to get address directly
    if 'address' in place:
        address = place['address']
        state = place.get('state', '')
        return f"{place.get('name', 'This place')} is located at: {address}, {state}."
    
    return f"I don't have the exact location details for {place.get('name', 'this place')} at the moment."

@app.route('/api/places', methods=['GET'])
def get_places():
    """Get a list of all places for autocomplete"""
    try:
        if db is None:
            return jsonify({"error": "Database connection not available"}), 500

        # Collect places from all collections
        all_places = []
        
        # From places collection
        if places_collection is not None:
            places = list(places_collection.find({}, {"name": 1, "_id": 0}))
            all_places.extend([place["name"] for place in places])
        
        # From other collections
        for collection in [buddhism_collection, christianities_collection, islam_collection, 
                          jainism_collection, sikhism_collection, temples_collection]:
            if collection is not None:
                places = list(collection.find({}, {"name": 1, "_id": 0}))
                all_places.extend([place["name"] for place in places])
        
        # Remove duplicates and sort
        all_places = sorted(list(set(all_places)))
        
        return jsonify({"places": all_places})
    except Exception as e:
        print(f"Error getting places list: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e), "places": []}), 500

if __name__ == '__main__':
    app.run(debug=True, port=PORT) 