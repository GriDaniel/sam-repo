import xml.etree.ElementTree as ET

# Global result variable for extractor messages
result = ""

def set_result(message):
    global result
    result = message

def get_result():
    return result

def extract_metadata_from_xml(file_path):
    """
    Extract metadata from an XML file by dynamically searching for <SLOPE> and <RESULT> tags.
    """
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
    except Exception as e:
        raise ValueError(f"Error parsing XML file: {e}")

    # Search for all SLOPE elements anywhere in the XML
    slopes = []
    for slope in root.findall(".//SLOPE"):
        pos_elem = slope.find("Pos")
        sensor_elem = slope.find("Sensor")
        if pos_elem is None or sensor_elem is None:
            raise ValueError("A <SLOPE> element is missing a <Pos> or <Sensor> tag.")
        try:
            pos = float(pos_elem.text)
            sensor = float(sensor_elem.text)
        except Exception as e:
            raise ValueError(f"Invalid numerical value in <SLOPE>: {e}")
        slopes.append({"Pos": pos, "Sensor": sensor})

    # Search for the first RESULT element anywhere in the XML
    result_elem = root.find(".//RESULT")
    if result_elem is None:
        raise ValueError("Missing <RESULT> element in the XML file.")

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
