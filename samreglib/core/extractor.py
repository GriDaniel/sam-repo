import xml.etree.ElementTree as ET

_result_message = ""

def set_result(message):
    global _result_message
    _result_message = message

def get_result():
    return _result_message

def extract_metadata_from_xml(file_path):
    """Extract metadata from an XML file."""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        data_elem = root.find(".//Data")
        
        if data_elem is None or data_elem.text is None:
            raise ValueError("Missing or empty <Data> element")
        
        data_tree = ET.fromstring(data_elem.text.strip())
        
        # Extract slopes
        slopes = []
        for slope in data_tree.findall(".//SLOPE"):
            pos_elem = slope.find("PosY")
            sensor_elem = slope.find("Sensor")
            
            if pos_elem is None or sensor_elem is None:
                raise ValueError("Missing <PosY> or <Sensor> tag")
            
            pos = float(pos_elem.text)
            sensor = float(sensor_elem.text)
            slopes.append({"PosY": pos, "Sensor": sensor})
        
        # Extract result data
        result_elem = data_tree.find(".//RESULT")
        if result_elem is None:
            raise ValueError("Missing <RESULT> element")
        
        expected_tags = ["START", "END", "WIDTH", "HEIGHT_MIN", "HEIGHT_MAX", "HEIGHT_MEAN", "ANGLE"]
        result_data = {}
        for tag in expected_tags:
            tag_elem = result_elem.find(tag)
            if tag_elem is None or tag_elem.text is None:
                raise ValueError(f"Missing or empty <{tag}> element")
            result_data[tag] = float(tag_elem.text)
        
        set_result("Extraction completed successfully.")
        return {"slopes": slopes, "result": result_data}, get_result()
    
    except Exception as e:
        set_result(f"Extraction failed: {e}")
        raise
