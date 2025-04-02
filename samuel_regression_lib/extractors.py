"""
XML data extraction functionality for embedded XML-like text.
"""

import xml.etree.ElementTree as ET
import re

class XMLExtractor:
    """
    Extracts data from XML files with embedded XML-like text.
    """
    
    def extract_output(self, xml_data):
        """
        Extract output data from XML string where the actual data
        is embedded as text content inside a <Data> tag.
        
        Args:
            xml_data: XML data as string
            
        Returns:
            Dictionary containing extracted output data
        """
        try:
            # Parse the main XML
            root = ET.fromstring(xml_data)
            
            # Find Data section
            data_section = root.find(".//Data")
            if data_section is None:
                raise ValueError("No Data section found in XML data")
            
            # Get the text content - this contains our XML-like structure
            embedded_xml_text = data_section.text
            if not embedded_xml_text or embedded_xml_text.strip() == "":
                raise ValueError("Data section is empty")
            
            # Now we need to parse the text content using regex since it's not well-formed XML
            return self._parse_embedded_xml(embedded_xml_text)
            
        except Exception as e:
            print(f"Error extracting XML data: {e}")
            raise
    
    def _parse_embedded_xml(self, text):
        """
        Parse XML-like text content using regex to extract structured data.
        
        Args:
            text: XML-like text from the Data section
            
        Returns:
            Dictionary containing the extracted data
        """
        # Extract the content between <OUTPUT> and </OUTPUT>
        output_match = re.search(r'<OUTPUT>\s*(.*?)\s*</OUTPUT>', text, re.DOTALL)
        if not output_match:
            raise ValueError("No OUTPUT section found in Data content")
        
        output_content = output_match.group(1)
        
        # Extract SLOPE data - there might be multiple SLOPE sections
        slopes = []
        slope_matches = re.finditer(r'<SLOPE>\s*(.*?)\s*</SLOPE>', output_content, re.DOTALL)
        
        for slope_match in slope_matches:
            slope_content = slope_match.group(1)
            
            # Extract Pos and Sensor values
            pos_match = re.search(r'<Pos>\s*(.*?)\s*</Pos>', slope_content, re.DOTALL)
            sensor_match = re.search(r'<Sensor>\s*(.*?)\s*</Sensor>', slope_content, re.DOTALL)
            
            slope_data = {
                "Pos": self._convert_value(pos_match.group(1) if pos_match else ""),
                "Sensor": self._convert_value(sensor_match.group(1) if sensor_match else "")
            }
            slopes.append(slope_data)
        
        # Extract RESULT data
        result_match = re.search(r'<RESULT>\s*(.*?)\s*</RESULT>', output_content, re.DOTALL)
        if not result_match:
            raise ValueError("No RESULT section found in OUTPUT content")
        
        result_content = result_match.group(1)
        
        # Extract all the result values
        result_data = {
            "START": self._extract_value(result_content, "START"),
            "END": self._extract_value(result_content, "END"),
            "WIDTH": self._extract_value(result_content, "WIDTH"),
            "HEIGHT_MIN": self._extract_value(result_content, "HEIGHT_MIN"),
            "HEIGHT_MAX": self._extract_value(result_content, "HEIGHT_MAX"),
            "HEIGHT_MEAN": self._extract_value(result_content, "HEIGHT_MEAN"),
            "ANGLE": self._extract_value(result_content, "ANGLE")
        }
        
        # Combine data
        extracted_data = {
            "SLOPES": slopes,
            "RESULT": result_data
        }
        
        return extracted_data
    
    def _extract_value(self, content, tag_name):
        """
        Extract a value for a specific tag from text content.
        
        Args:
            content: Text content to search in
            tag_name: Name of the tag to extract
            
        Returns:
            Extracted and converted value
        """
        pattern = r'<' + tag_name + r'>\s*(.*?)\s*</' + tag_name + r'>'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            return self._convert_value(match.group(1))
        return None
    
    def _convert_value(self, value_str):
        """
        Convert a string value to the appropriate type.
        
        Args:
            value_str: String value to convert
            
        Returns:
            Converted value with appropriate type
        """
        if not value_str or value_str.strip() == "":
            return ""
        
        # Try to convert to numeric if it looks like a number
        try:
            # Check if it's a float with decimal point
            if "." in value_str:
                return float(value_str)
            # Otherwise, try as int
            return int(value_str)
        except ValueError:
            # If conversion fails, return as string
            return value_str
