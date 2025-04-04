import xml.etree.ElementTree as ET

# Global result variable for this module
result = ""

def set_result(message):
    global result
    result = message

def get_result():
    return result

def element_to_dict(elem):
    """
    Recursively converts an ElementTree element into a dictionary.
    If an element has attributes and text, the text is used if there are no children.
    If there are children, attributes (if any) are merged with child data.
    """
    # Start with attributes, if any.
    d = {}
    if elem.attrib:
        d.update(elem.attrib)
    
    # Process children.
    children = list(elem)
    if children:
        child_dict = {}
        for child in children:
            child_value = element_to_dict(child)
            tag = child.tag
            # If the tag already exists, ensure its value is a list.
            if tag in child_dict:
                if not isinstance(child_dict[tag], list):
                    child_dict[tag] = [child_dict[tag]]
                child_dict[tag].append(child_value)
            else:
                child_dict[tag] = child_value
        d.update(child_dict)
    else:
        # If no children, use text (even if attributes exist, text takes precedence).
        d = elem.text.strip() if elem.text is not None else ""
    return d

def xml_to_json(file_path):
    """
    Reads an entire XML file and converts it into a raw JSON (Python dictionary) representation.
    """
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
    except Exception as e:
        set_result(f"Error parsing XML file: {e}")
        raise ValueError(f"Error parsing XML file: {e}")
    
    raw_json = {root.tag: element_to_dict(root)}
    set_result("XML converted to raw JSON successfully.")
    return raw_json, get_result()
