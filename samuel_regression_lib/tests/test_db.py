"""
Tests for the database manager.
"""

import unittest
from unittest.mock import patch, MagicMock
import pymongo
from pymongo.errors import ConnectionFailure

from samuel_regression_lib.db import DatabaseManager


class TestDatabaseManager(unittest.TestCase):
    """Test cases for the DatabaseManager class."""

    @patch('pymongo.MongoClient')
    def test_connection_success(self, mock_client):
        """Test successful database connection."""
        # Setup mock
        mock_instance = MagicMock()
        mock_client.return_value = mock_instance

        # Test
        db_manager = DatabaseManager()
        result = db_manager.test_connection()

        # Assert
        self.assertTrue(result)
        mock_client.assert_called_once()

    @patch('pymongo.MongoClient')
    def test_connection_failure(self, mock_client):
        """Test database connection failure."""
        # Setup mock to raise exception
        mock_client.side_effect = ConnectionFailure("Connection error")

        # Test
        db_manager = DatabaseManager()
        result = db_manager.test_connection()

        # Assert
        self.assertFalse(result)
        mock_client.assert_called_once()

    @patch('pymongo.MongoClient')
    def test_get_reference_data_found(self, mock_client):
        """Test retrieving existing reference data."""
        # Setup mock
        mock_instance = MagicMock()
        mock_collection = MagicMock()
        mock_db = {
            "reference_data_lq": mock_collection
        }
        mock_instance.__getitem__.return_value = mock_db
        mock_db.__getitem__.return_value = mock_collection
        mock_client.return_value = mock_instance

        # Setup find_one result
        mock_document = {
            "filename": "test.xml",
            "output_data": {"RESULT": {"VALUE": 123}}
        }
        mock_collection.find_one.return_value = mock_document

        # Test
        db_manager = DatabaseManager()
        result = db_manager.get_reference_data("test.xml", "lq")

        # Assert
        self.assertEqual(result, {"RESULT": {"VALUE": 123}})
        mock_collection.find_one.assert_called_once_with({"filename": "test.xml"})

    @patch('pymongo.MongoClient')
    def test_get_reference_data_not_found(self, mock_client):
        """Test retrieving non-existing reference data."""
        # Setup mock
        mock_instance = MagicMock()
        mock_collection = MagicMock()
        mock_db = {
            "reference_data_lq": mock_collection
        }
        mock_instance.__getitem__.return_value = mock_db
        mock_db.__getitem__.return_value = mock_collection
        mock_client.return_value = mock_instance

        # Setup find_one result
        mock_collection.find_one.return_value = None

        # Test
        db_manager = DatabaseManager()
        result = db_manager.get_reference_data("nonexistent.xml", "lq")

        # Assert
        self.assertIsNone(result)
        mock_collection.find_one.assert_called_once_with({"filename": "nonexistent.xml"})


if __name__ == '__main__':
    unittest.main()