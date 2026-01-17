from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
import certifi

load_dotenv()

uri = os.getenv("MONGODB_URI", "mongodb+srv://ines_db:inesines2020@cluster0.vmkdgj0.mongodb.net/?retryWrites=true&w=majority")

# Create client with certifi CA bundle (fixes SSL issues)
try:
    client = MongoClient(
        uri,
        server_api=ServerApi('1'),
        tlsCAFile=certifi.where()  # Use certifi's CA bundle
    )
    
    # Get database
    db = client["dressly_db"]
    
    # Collections
    users_collection = db["users"]
    quiz_responses_collection = db["quiz_responses"]
    
    # Test connection
    client.admin.command('ping')
    print("✅ Connected to MongoDB!")
    
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")