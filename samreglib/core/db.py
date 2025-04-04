import pymongo
from pymongo import MongoClient
from core.config import DB_URI, DB_NAME
import json

# Global result variable for storing messages
result = ""

def set_result(message):
    """Set the global result message."""
    global result
    result = message

def get_result():
    """Return the global result message."""
    return result

def get_db_connection():
    """Establish and return the MongoDB database connection."""
    try:
        client = MongoClient(DB_URI)
        db = client[DB_NAME]
        set_result("Connected to MongoDB successfully.")
        return db, result
    except Exception as e:
        set_result(f"Connection failed: {str(e)}")
        return None, result

def store_document(db, collection_name, document_name, document_data, metadata):
    """Store a decoded JSON document along with its metadata."""
    try:
        collection = db[collection_name]
        document = {
            "name": document_name,
            "data": document_data,
            "metadata": metadata
        }
        collection.insert_one(document)
        set_result(f"Document '{document_name}' stored successfully in '{collection_name}' collection.")
        return result
    except Exception as e:
        set_result(f"Error storing document: {str(e)}")
        return result

def check_name_exists(db, collection_name, document_name):
    """Check if a document with the specified name exists in the collection."""
    try:
        collection = db[collection_name]
        query_result = collection.find_one({"name": document_name})
        if query_result:
            set_result(f"Document '{document_name}' exists in '{collection_name}' collection.")
            return True, get_result()  # Return the message, not the document
        else:
            set_result(f"Document '{document_name}' does not exist in '{collection_name}' collection.")
            return False, get_result()
    except Exception as e:
        set_result(f"Error checking document existence: {str(e)}")
        return False, get_result()

def get_metadata(db, collection_name, document_name):
    """Retrieve metadata for a document with the specified name."""
    try:
        collection = db[collection_name]
        query_result = collection.find_one({"name": document_name})
        if query_result:
            set_result(f"Metadata for '{document_name}' retrieved successfully.")
            return query_result.get("metadata", {}), get_result()  # Return metadata and message
        else:
            set_result(f"Document '{document_name}' not found in '{collection_name}' collection.")
            return None, get_result()
    except Exception as e:
        set_result(f"Error retrieving metadata: {str(e)}")
        return None, get_result()

