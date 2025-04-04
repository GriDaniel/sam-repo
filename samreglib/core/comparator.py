import re

# Global result variable for comparator messages
result = ""

def set_result(message):
    global result
    result = message

def get_result():
    return result

def compare_metadata(reference, extracted, tolerance):
    """
    Compare reference metadata with extracted data that might be an XML string.
    
    Args:
        reference (dict): Dictionary with metadata from database
        extracted (str or dict): String with XML tags or a dictionary
        tolerance (float): Percentage tolerance for differences
    """
    comparison = {}
    
    # Get result section from reference
    ref_result = reference.get("result", {})
    
    # Process each key in the reference data
    for key in ref_result:
        ref_val = ref_result.get(key)
        
        # Try to find this key's value in the extracted data
        ext_val = None
        
        # CASE 1: If extracted is a string (with XML)
        if isinstance(extracted, str):
            # Use regex to find patterns like <START>10.5</START>
            pattern = f"<{key}>(.*?)</{key}>"
            match = re.search(pattern, extracted)
            if match:
                # Try to convert to float
                try:
                    ext_val = float(match.group(1).strip())
                except ValueError:
                    ext_val = match.group(1).strip()
        
        # CASE 2: If extracted has a result dictionary
        elif isinstance(extracted, dict) and "result" in extracted:
            ext_val = extracted["result"].get(key)
            
        # CASE 3: If extracted is itself a dictionary
        elif isinstance(extracted, dict):
            ext_val = extracted.get(key)
        
        # Skip comparison if values are missing
        if ref_val is None or ext_val is None:
            comparison[key] = {"percent_diff": None, "passed": False, "message": "Missing value"}
            continue
        
        # Calculate percentage difference
        if ref_val == 0:
            # If reference value is zero, define diff as 0 only if extracted is also zero
            percent_diff = 0.0 if ext_val == 0 else float('inf')
        else:
            percent_diff = abs(ref_val - ext_val) / abs(ref_val) * 100
            
        # Check if within tolerance
        passed = percent_diff <= tolerance
        comparison[key] = {"percent_diff": percent_diff, "passed": passed}
    
    set_result("Comparison completed successfully.")
    return comparison, get_result()
