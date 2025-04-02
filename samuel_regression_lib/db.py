"""
Database operations for Samuel Regression Testing Library.
"""

import time
import pymongo
from pymongo.errors import ConnectionFailure, OperationFailure
from .config import MONGO_URI, MONGO_DB_NAME, MONGO_COLLECTION_PREFIX


class Database:
    """
    Handles all database operations.
    """

    def __init__(self):
        """Initialize the database manager."""
        self.client = None
        self.db = None

    def _connect(self):
        """
        Connect to MongoDB.

        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Create a client with connection timeout
            self.client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            self.db = self.client[MONGO_DB_NAME]
            return True
        except (ConnectionFailure, OperationFailure) as e:
            print(f"Database connection error: {e}")
            return False

    def test_connection(self):
        """
        Test the database connection.

        Returns:
            True if connection successful, False otherwise
        """
        start_time = time.time()
        success = self._connect()
        end_time = time.time()

        if success:
            print(f"Database connection successful (took {end_time - start_time:.2f}s)")
        else:
            print(f"Database connection failed (after {end_time - start_time:.2f}s)")

        return success

    def get_reference_data(self, filename, method):
        """
        Get reference data for a specific file and method.

        Args:
            filename: Name of the file to look up
            method: Method name (e.g., "lq")

        Returns:
            Reference output data if found, None otherwise
        """
        if not self._connect():
            return None

        collection_name = f"{MONGO_COLLECTION_PREFIX}{method}"

        try:
            collection = self.db[collection_name]
            result = collection.find_one({"filename": filename})

            if result:
                return result.get("output_data")
            return None
        except Exception as e:
            print(f"Error retrieving reference data: {e}")
            return None
        finally:
            if self.client:
                self.client.close()

    def store_reference_data(self, filename, method, xml_data, output_data):
        """
        Store reference data for a specific file and method.
        This method is only used by the CLI tool.

        Args:
            filename: Name of the file
            method: Method name (e.g., "lq")
            xml_data: Full XML data as string
            output_data: Extracted output data

        Returns:
            True if storage successful, False otherwise
        """
        if not self._connect():
            return False

        collection_name = f"{MONGO_COLLECTION_PREFIX}{method}"

        try:
            collection = self.db[collection_name]

            # Check if entry already exists
            existing = collection.find_one({"filename": filename})

            if existing:
                # Update existing entry
                collection.update_one(
                    {"filename": filename},
                    {"$set": {
                        "xml_data": xml_data,
                        "output_data": output_data,
                        "updated_at": time.time()
                    }}
                )
            else:
                # Create new entry
                collection.insert_one({
                    "filename": filename,
                    "method": method,  # Store method name for easier querying
                    "xml_data": xml_data,
                    "output_data": output_data,
                    "created_at": time.time(),
                    "updated_at": time.time()
                })

            return True
        except Exception as e:
            print(f"Error storing reference data: {e}")
            return False
        finally:
            if self.client:
                self.client.close()

    def list_reference_data(self, method=None):
        """
        List all reference data in the database, optionally filtered by method.
        This method is only used by the CLI tool.

        Args:
            method: Optional method name to filter by

        Returns:
            List of reference data entries with basic metadata
        """
        if not self._connect():
            return []

        results = []

        try:
            if method:
                # Query a specific collection
                collection_name = f"{MONGO_COLLECTION_PREFIX}{method}"
                if collection_name in self.db.list_collection_names():
                    collection = self.db[collection_name]
                    for doc in collection.find({}, {"filename": 1, "created_at": 1, "updated_at": 1}):
                        doc["method"] = method
                        results.append(doc)
            else:
                # Query all collections
                for collection_name in self.db.list_collection_names():
                    if collection_name.startswith(MONGO_COLLECTION_PREFIX):
                        method = collection_name[len(MONGO_COLLECTION_PREFIX):]
                        collection = self.db[collection_name]
                        for doc in collection.find({}, {"filename": 1, "created_at": 1, "updated_at": 1}):
                            doc["method"] = method
                            results.append(doc)

            return results
        except Exception as e:
            print(f"Error listing reference data: {e}")
            return []
        finally:
            if self.client:
                self.client.close()