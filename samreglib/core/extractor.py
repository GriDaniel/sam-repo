import xml.etree.ElementTree as ET

# Global result variable for extractor messages
_result_message = ""

def set_result(message):
    global _result_message
    _result_message = message

def get_result():
    return _result_message

def extract_metadata_from_xml(file_path):
    """
    Extract metadata from an XML file by searching for the <Data> tag,
    parsing its plain text content as XML, and then extracting SLOPE and RESULT info.
    
    Args:
        file_path (str): Path to the XML file.
    
    Returns:
        tuple: A tuple containing a dictionary with keys 'slopes' and 'result' and a result message.
    
    Raises:
        ValueError: If any required element is missing or if parsing fails.
    """
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
    except Exception as e:
        raise ValueError(f"Error parsing XML file: {e}")
    
    # Search for the central <Data> element
    data_elem = root.find(".//Data")
    if data_elem is None or data_elem.text is None:
        raise ValueError("Missing or empty <Data> element in the XML file.")
    
    # Parse the plain text inside <Data> as XML
    try:
        data_tree = ET.fromstring(data_elem.text.strip())
    except Exception as e:
        raise ValueError(f"Error parsing plain text in <Data> as XML: {e}")
    
    # Extract slopes from the parsed content (using <PosY> instead of <Pos>)
    slopes = []
    for slope in data_tree.findall(".//SLOPE"):
        pos_elem = slope.find("PosY")  # Changed from "Pos" to "PosY"
        sensor_elem = slope.find("Sensor")
        if pos_elem is None or sensor_elem is None:
            raise ValueError("A <SLOPE> element is missing a <PosY> or <Sensor> tag.")
        try:
            pos = float(pos_elem.text)
            sensor = float(sensor_elem.text)
        except Exception as e:
            raise ValueError(f"Invalid numerical value in <SLOPE>: {e}")
        slopes.append({"PosY": pos, "Sensor": sensor})
    
    # Extract the first RESULT element from the parsed content
    result_elem = data_tree.find(".//RESULT")
    if result_elem is None:
        raise ValueError("Missing <RESULT> element in the parsed <Data> content.")
    
    expected_tags = ["START", "END", "WIDTH", "HEIGHT_MIN", "HEIGHT_MAX", "HEIGHT_MEAN", "ANGLE"]
    result_data = {}
    for tag in expected_tags:
        tag_elem = result_elem.find(tag)
        if tag_elem is None or tag_elem.text is None:
            raise ValueError(f"Missing or empty <{tag}> element in <RESULT>.")
        try:
            result_data[tag] = float(tag_elem.text)
        except Exception as e:
            raise ValueError(f"Invalid numerical value for <{tag}>: {e}")
    
    set_result("Extraction completed successfully.")
    return {"slopes": slopes, "result": result_data}, get_result()
