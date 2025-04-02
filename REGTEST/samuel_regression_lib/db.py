"""
MongoDB connection and operations for the regression testing library.
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import samuel_regression_lib.config as config  # Use appropriate import based on your structure


class MongoConnector:
    """Handles all MongoDB operations for the regression testing library."""

    def __init__(self):
        self.client = None
        self.db = None

    def connect(self):
        """
        Establish connection to MongoDB.

        Returns:
            tuple: (success_status, message)
        """
        try:
            self.client = MongoClient(config.MONGO_URI)
            # The ismaster command is cheap and does not require auth
            self.client.admin.command('ismaster')
            self.db = self.client[config.DATABASE_NAME]
            return True, "Connection successful"
        except ConnectionFailure:
            return False, "Connection unsuccessful"

    def find_reference(self, method, filename):
        """
        Find reference data for a given method and filename.

        Args:
            method (str): Method name (collection name in MongoDB)
            filename (str): File name to look for

        Returns:
            dict or None: Reference data if found, None otherwise
        """
        # FIX: Check if db is None properly
        if self.db is None:
            return None

        collection = self.db[method]
        result = collection.find_one({"filename": filename})
        return result

    def add_reference(self, method, filename, xml_data, output_data):
        """
        Add a new reference to the database.

        Args:
            method (str): Method name (collection name in MongoDB)
            filename (str): File name to store
            xml_data (str): XML data as a string
            output_data (dict): Extracted output data

        Returns:
            tuple: (success_status, message)
        """
        # FIX: Check if db is None properly
        if self.db is None:
            return False, "Database connection not established"

        collection = self.db[method]

        # Check if reference already exists
        existing = collection.find_one({"filename": filename})
        if existing:
            return False, f"Reference for {filename} under method {method} already exists"

        # Insert new reference
        collection.insert_one({
            "filename": filename,
            "xml_data": xml_data,
            "output_data": output_data
        })

        return True, f"Reference for {filename} under method {method} added successfully"