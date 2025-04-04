import pymongo
from pymongo import MongoClient
from core.config import DB_URI, DB_NAME

result = ""

def set_result(message):
    global result
    result = message

def get_result():
    return result

def get_db_connection():
    """Establish MongoDB database connection."""
    try:
        client = MongoClient(DB_URI)
        db = client[DB_NAME]
        set_result("Connected to MongoDB successfully.")
        return db, result
    except Exception as e:
        set_result(f"Connection failed: {str(e)}")
        return None, result

def store_document(db, collection_name, document_name, document_data, metadata):
    """Store a document with its metadata."""
    try:
        collection = db[collection_name]
        document = {
            "name": document_name,
            "data": document_data,
            "metadata": metadata
        }
        collection.insert_one(document)
        set_result(f"Document '{document_name}' stored successfully.")
        return result
    except Exception as e:
        set_result(f"Error storing document: {str(e)}")
        return result

def check_name_exists(db, collection_name, document_name):
    """Check if a document exists in the collection."""
    try:
        collection = db[collection_name]
        query_result = collection.find_one({"name": document_name})
        if query_result:
            set_result(f"Document '{document_name}' exists.")
            return True, result
        else:
            set_result(f"Document '{document_name}' does not exist.")
            return False, result
    except Exception as e:
        set_result(f"Error checking document: {str(e)}")
        return False, result

def get_metadata(db, collection_name, document_name):
    """Retrieve metadata for a document."""
    try:
        collection = db[collection_name]
        query_result = collection.find_one({"name": document_name})
        if query_result:
            set_result(f"Metadata for '{document_name}' retrieved.")
            return query_result.get("metadata", {}), result
        else:
            set_result(f"Document '{document_name}' not found.")
            return None, result
    except Exception as e:
        set_result(f"Error retrieving metadata: {str(e)}")
        return None, result
