"""
XML data extraction functionality.
"""

import xml.etree.ElementTree as ET


class XMLExtractor:
    """
    Extracts data from XML files.
    """

    def extract_output(self, xml_data):
        """
        Extract output data from XML string.

        Args:
            xml_data: XML data as string

        Returns:
            Dictionary containing extracted output data
        """
        try:
            # Parse XML
            root = ET.fromstring(xml_data)

            # Find OUTPUT section
            output_section = root.find(".//OUTPUT")
            if output_section is None:
                raise ValueError("No OUTPUT section found in XML data")

            # Extract SLOPE data
            slopes = []
            for slope in output_section.findall("./SLOPE"):
                slope_data = {
                    "Pos": self._extract_value(slope.find("Pos")),
                    "Sensor": self._extract_value(slope.find("Sensor"))
                }
                slopes.append(slope_data)

            # Extract RESULT data
            result_section = output_section.find("./RESULT")
            if result_section is None:
                raise ValueError("No RESULT section found in OUTPUT")

            result_data = {
                "START": self._extract_value(result_section.find("START")),
                "END": self._extract_value(result_section.find("END")),
                "WIDTH": self._extract_value(result_section.find("WIDTH")),
                "HEIGHT_MIN": self._extract_value(result_section.find("HEIGHT_MIN")),
                "HEIGHT_MAX": self._extract_value(result_section.find("HEIGHT_MAX")),
                "HEIGHT_MEAN": self._extract_value(result_section.find("HEIGHT_MEAN")),
                "ANGLE": self._extract_value(result_section.find("ANGLE"))
            }

            # Combine data
            extracted_data = {
                "SLOPES": slopes,
                "RESULT": result_data
            }

            return extracted_data
        except Exception as e:
            print(f"Error extracting XML data: {e}")
            raise

    def _extract_value(self, element):
        """
        Extract value from XML element, preserving type.

        Args:
            element: XML element to extract value from

        Returns:
            Extracted value with appropriate type
        """
        if element is None:
            return None

        value = element.text.strip() if element.text else ""

        # Try to convert to numeric if it looks like a number
        if not value:
            return ""

        try:
            # Check if it's a float with decimal point
            if "." in value:
                return float(value)
            # Otherwise, try as int
            return int(value)
        except ValueError:
            # If conversion fails, return as string
            return value