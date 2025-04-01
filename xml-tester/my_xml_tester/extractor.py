# my_xml_tester/extractor.py
import os
import xml.etree.ElementTree as ET

def extract_filename(file_path: str) -> str:
    """Extracts the filename without extension from the provided file path."""
    return os.path.splitext(os.path.basename(file_path))[0]

def extract_analyzer_result(xml_content: str) -> ET.Element:
    """
    Parses the XML content and returns the <AnalyzerResult> element.
    Assumes that <AnalyzerResult> exists somewhere in the XML.
    """
    root = ET.fromstring(xml_content)
    return root.find('.//AnalyzerResult')

def extract_raw_xml(xml_path: str) -> str:
    """Reads the XML file as a raw string."""
    with open(xml_path, 'r') as file:
        return file.read()
