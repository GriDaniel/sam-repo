import xml.etree.ElementTree as ET

result = ""

def set_result(message):
    global result
    result = message

def get_result():
    return result

def element_to_dict(elem):
    """Convert an ElementTree element to a dictionary."""
    d = dict(elem.attrib) if elem.attrib else {}
    
    children = list(elem)
    if children:
        child_dict = {}
        for child in children:
            tag = child.tag
            child_value = element_to_dict(child)
            
            if tag in child_dict:
                child_dict[tag] = [child_dict[tag], child_value] if not isinstance(child_dict[tag], list) else child_dict[tag] + [child_value]
            else:
                child_dict[tag] = child_value
        
        d.update(child_dict)
    elif elem.text:
        d = elem.text.strip()
    
    return d

def xml_to_json(file_path):
    """Convert XML file to a raw JSON representation."""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        raw_json = {root.tag: element_to_dict(root)}
        
        set_result("XML converted to raw JSON successfully.")
        return raw_json, get_result()
    
    except Exception as e:
        set_result(f"Error parsing XML file: {e}")
        raise ValueError(f"Error parsing XML file: {e}")
