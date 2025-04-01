# my_xml_tester/storage.py
import xml.etree.ElementTree as ET
from my_xml_tester.db import get_db_connection
from my_xml_tester.extractor import extract_filename, extract_analyzer_result, extract_raw_xml

def check_file_exists(file_path: str, method_name: str) -> bool:
    """
    Check if the given XML file (by its base name) exists in the database for the given method.
    """
    filename = extract_filename(file_path)
    db_collection = get_db_connection(method_name)
    return db_collection.find_one({"filename": filename}) is not None

def store_xml(file_path: str, method_name: str):
    """
    Stores the XML data in MongoDB if it doesn't already exist.
    Raises a ValueError if the file (by name) already exists under the given method.
    """
    filename = extract_filename(file_path)
    db_collection = get_db_connection(method_name)
    if db_collection.find_one({"filename": filename}):
        raise ValueError(f"File {filename} already exists under method {method_name}.")

    raw_data = extract_raw_xml(file_path)
    analyzer_elem = extract_analyzer_result(raw_data)
    analyzer_data = ET.tostring(analyzer_elem, encoding='unicode') if analyzer_elem is not None else ""

    record = {
        "filename": filename,
        "raw_data": raw_data,
        "analyzer_data": analyzer_data
    }
    db_collection.insert_one(record)
    return record

def compare_output_with_reference(filename: str, method_name: str, output_xml_path: str) -> str:
    """
    Compares the modified output XML against the stored reference in MongoDB.
    For demonstration, we compare the <AnalyzerResult> XML string.
    """
    db_collection = get_db_connection(method_name)
    stored_record = db_collection.find_one({"filename": filename})
    if not stored_record:
        return f"No stored reference for file {filename} under method {method_name}."
    
    output_raw = extract_raw_xml(output_xml_path)
    output_analyzer_elem = extract_analyzer_result(output_raw)
    output_analyzer_data = ET.tostring(output_analyzer_elem, encoding='unicode') if output_analyzer_elem is not None else ""
    
    return "Match" if stored_record["analyzer_data"] == output_analyzer_data else "Mismatch"
