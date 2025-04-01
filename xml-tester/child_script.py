# child_script.py
import os
import random
import xml.etree.ElementTree as ET
from my_xml_tester.extractor import extract_filename
from my_xml_tester.storage import check_file_exists, compare_output_with_reference

TEST_DATA_DIR = 'testData'
OUTPUT_DATA_DIR = 'outputData'
METHOD_NAME = 'squareTube'

# List to track files not found in the DB
files_not_in_db = []

def process_single_file(filename: str):
    input_path = os.path.join(TEST_DATA_DIR, filename)
    with open(input_path, 'r') as file:
        xml_content = file.read()
    
    # Check if the file exists in the DB via the library
    if not check_file_exists(input_path, METHOD_NAME):
        files_not_in_db.append(filename)
        # You may decide to continue processing even if not in DB, or skip it.
        # For demo purposes, we continue processing.
    
    # Randomly decide to modify the output XML or not (50/50 chance)
    modify_output = random.choice([True, False])
    
    # Parse the XML
    root = ET.fromstring(xml_content)
    analyzer_elem = root.find('.//AnalyzerResult')
    
    if analyzer_elem is None:
        print(f"No AnalyzerResult found in {filename}")
        return
    
    # Optionally modify the AnalyzerResult snippet
    if modify_output:
        height_elem = analyzer_elem.find('Height')
        if height_elem is not None:
            try:
                new_value = float(height_elem.text) * 1.1  # slight modification
                height_elem.text = str(new_value)
            except (TypeError, ValueError):
                print("Error converting Height value.")
    
    # Save the modified AnalyzerResult as the output XML
    output_path = os.path.join(OUTPUT_DATA_DIR, filename)
    tree = ET.ElementTree(analyzer_elem)
    tree.write(output_path)
    
    # If the file exists in the DB, compare the generated output with the stored reference.
    if check_file_exists(input_path, METHOD_NAME):
        base_filename = extract_filename(filename)
        result = compare_output_with_reference(base_filename, METHOD_NAME, output_path)
        print(f"File: {filename} comparison result: {result}")
    else:
        print(f"File: {filename} not found in DB; skipping comparison.")

def process_xml_files():
    print("Starting XML file processing...")
    if not os.path.exists(TEST_DATA_DIR):
        print(f"Test data directory '{TEST_DATA_DIR}' does not exist.")
        return
    if not os.path.exists(OUTPUT_DATA_DIR):
        os.makedirs(OUTPUT_DATA_DIR)
        print(f"Created output directory: {OUTPUT_DATA_DIR}")

    xml_files = [f for f in os.listdir(TEST_DATA_DIR) if f.endswith('.xml')]
    if not xml_files:
        print("No .xml files found in testData folder.")
        return

    for filename in xml_files:
        process_single_file(filename)

    if files_not_in_db:
        print("Files not found in database:")
        for f in files_not_in_db:
            print(f" - {f}")

if __name__ == '__main__':
    process_xml_files()
