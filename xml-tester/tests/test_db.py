# my_xml_tester/db.py
from pymongo import MongoClient

def get_db_connection(method_name: str):
    """
    Returns a MongoDB collection for the given method name.
    This uses a database named 'xml_tester' and a collection per method.
    """
    client = MongoClient("mongodb://localhost:27017/")
    db = client['xml_tester']
    return db[method_name]
