"""
XML parsing and data extraction for the regression testing library.
"""

import xml.etree.ElementTree as ET


class XMLExtractor:
    """Handles XML extraction and parsing operations."""

    @staticmethod
    def extract_xml_from_file(filepath):
        """
        Extract XML data as a string from a file.

        Args:
            filepath (str): Path to the XML file

        Returns:
            str: XML content as a string
        """
        with open(filepath, 'r') as file:
            return file.read()

    @staticmethod
    def extract_output_data(xml_string):
        """
        Extract output data from XML string.

        Args:
            xml_string (str): XML content as a string

        Returns:
            dict or None: Dictionary of output data or None if extraction fails
        """
        try:
            root = ET.fromstring(xml_string)
            output = root.find(".//OUTPUT")

            if output is None:
                return None

            # Convert output to a dictionary
            output_dict = {}
            for child in output:
                # Get tag name and value
                tag = child.tag
                value = child.text

                # Try to convert to float if possible for comparison
                try:
                    value = float(value)
                except (ValueError, TypeError):
                    pass

                output_dict[tag] = value

            return output_dict
        except ET.ParseError:
            return None