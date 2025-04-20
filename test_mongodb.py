import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from urllib.parse import urlparse

def test_mongodb_connection():
    # Load environment variables
    load_dotenv()
    
    # Get MongoDB connection string
    mongodb_uri = os.getenv('MONGODB_URI')
    
    if not mongodb_uri:
        print("Error: MONGODB_URI not found in .env file")
        return False
    
    try:
        # Parse the connection string to check if database name is included
        parsed_uri = urlparse(mongodb_uri)
        if not parsed_uri.path or parsed_uri.path == '/':
            print("Error: No database name specified in connection string")
            print("Please add the database name to your connection string")
            print("Example: mongodb+srv://<username>:<password>@<cluster>.mongodb.net/ollama_chat")
            return False
        
        # Create a MongoDB client
        client = MongoClient(mongodb_uri)
        
        # Test the connection
        client.admin.command('ping')
        
        # Get database name from connection string
        db_name = parsed_uri.path.lstrip('/')
        db = client[db_name]
        collection = db.chats
        
        # Insert a test document
        test_doc = {
            "title": "Test Chat",
            "messages": [
                {"role": "user", "content": "Hello, this is a test message."},
                {"role": "assistant", "content": "This is a test response."}
            ]
        }
        
        result = collection.insert_one(test_doc)
        
        # Retrieve the test document
        retrieved_doc = collection.find_one({"_id": result.inserted_id})
        
        # Delete the test document
        collection.delete_one({"_id": result.inserted_id})
        
        print("MongoDB connection successful!")
        print("Test document inserted and retrieved successfully.")
        print("Database name:", db_name)
        print("Collection name: chats")
        print("Number of documents in collection:", collection.count_documents({}))
        
        return True
        
    except ConnectionFailure as e:
        print("Error: Could not connect to MongoDB")
        print("Error details:", str(e))
        print("\nPlease check:")
        print("1. Your connection string is correct")
        print("2. Your IP address is whitelisted in MongoDB Atlas")
        print("3. Your username and password are correct")
        return False
    except Exception as e:
        print("Error: An unexpected error occurred")
        print("Error details:", str(e))
        return False
    finally:
        # Close the connection
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    test_mongodb_connection() 