

# database.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
from bson.objectid import ObjectId

load_dotenv()

# Connect to MongoDB
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.mediguide_db

# Define collections
users_collection = db.users
conversations_collection = db.conversations

# --- Helpers ---
def serialize_doc(doc):
    """Convert MongoDB document (_id as ObjectId) into JSON serializable dict."""
    if not doc:
        return None
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc

# --- User Functions ---
def get_user(username: str):
    """Fetches a user by their username."""
    return users_collection.find_one({"username": username})

def create_user(username: str, hashed_password: str):
    """Inserts a new user into the database."""
    return users_collection.insert_one({
        "username": username,
        "hashed_password": hashed_password,
        "created_at": datetime.utcnow()
    })

# --- Conversation Functions ---
def get_user_conversations(username: str):
    """Fetches all conversation metadata for a user."""
    convos = list(conversations_collection.find(
        {"username": username},
        {"messages": 0}  # Exclude messages for performance
    ).sort("created_at", -1))
    return [serialize_doc(c) for c in convos]

def get_conversation_by_id(conversation_id: str, username: str):
    """Fetches a single, complete conversation, ensuring the user owns it."""
    convo = conversations_collection.find_one({
        "_id": ObjectId(conversation_id),
        "username": username
    })
    return serialize_doc(convo)

def create_conversation(username: str, first_message: dict):
    """Creates a new conversation document."""
    result = conversations_collection.insert_one({
        "username": username,
        "title": first_message['content'][:50] + "...",
        "messages": [first_message],
        "created_at": datetime.utcnow()
    })
    return result.inserted_id

def add_message_to_conversation(conversation_id: str, message: dict):
    """Adds a message to an existing conversation's 'messages' array."""
    conversations_collection.update_one(
        {"_id": ObjectId(conversation_id)},
        {"$push": {"messages": message}}
    )
