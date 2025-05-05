import requests
import json
import time

# Define the API endpoint
BASE_URL = "http://127.0.0.1:5000"

def test_api():
    """Test various aspects of the enhanced chatbot API"""
    
    print("Testing Teerth Saarthi Enhanced Chatbot API")
    print("===========================================")
    
    # Test 1: API Status
    print("\nTest 1: Checking API Status...")
    try:
        response = requests.get(f"{BASE_URL}/api/status")
        if response.status_code == 200:
            print("✓ API is running")
        else:
            print(f"✗ API returned status code {response.status_code}")
    except Exception as e:
        print(f"✗ Error connecting to API: {e}")
        return
    
    # Test 2: Get Places List
    print("\nTest 2: Retrieving places list for autocomplete...")
    try:
        response = requests.get(f"{BASE_URL}/api/places")
        if response.status_code == 200:
            places = response.json().get("places", [])
            print(f"✓ Retrieved {len(places)} places")
            if places:
                print(f"Sample places: {', '.join(places[:5])}...")
        else:
            print(f"✗ Failed to retrieve places. Status code: {response.status_code}")
    except Exception as e:
        print(f"✗ Error retrieving places: {e}")
    
    # Test 3: Basic Query Processing
    print("\nTest 3: Testing basic greeting query...")
    test_query("hello", "Expected: Greeting response")
    
    # Test religion-specific queries
    print("\nTest 4: Testing religion-specific queries...")
    test_query("tell me about hindu temples", "Expected: List of Hindu temples")
    test_query("buddhist places in india", "Expected: List of Buddhist places")
    
    # Test place-specific queries with different query types
    print("\nTest 5: Testing place-specific queries with different query types...")
    test_query("history of Golden Temple", "Expected: History information about Golden Temple")
    test_query("how to reach Khwaja Gharib Nawaz Dargah Sharif", "Expected: Transport information")
    test_query("accommodations near Vatican City", "Expected: Accommodation information")
    test_query("tourist attractions near Palitana Jain Temples", "Expected: Attraction information")
    test_query("location of Somnath Temple", "Expected: Location information")
    
    # Test special case handling
    print("\nTest 6: Testing special case handling...")
    test_query("khatu shyam temple history", "Expected: History of Shree Khatu Shyam Mandir")
    test_query("what's the history of ranakpur jain temple?", "Expected: History of Ranakpur Jain Temple")
    test_query("how do i reach dilwara temples?", "Expected: Transport info for Dilwara Temples")
    
    print("\nTest complete!")

def test_query(query, expected_result):
    """Test a specific query and print the response"""
    try:
        response = requests.post(
            f"{BASE_URL}/api/message",
            json={"message": query},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json().get("response", "No response")
            print(f"Query: '{query}'")
            print(f"{expected_result}")
            print(f"Response: {result[:100]}..." if len(result) > 100 else f"Response: {result}")
            print("-" * 50)
        else:
            print(f"Query: '{query}' - Failed with status code {response.status_code}")
    except Exception as e:
        print(f"Error testing query '{query}': {e}")
    
    # Add a small delay to prevent overwhelming the server
    time.sleep(0.5)

if __name__ == "__main__":
    test_api() 