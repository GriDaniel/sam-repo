import re

result = ""

def set_result(message):
    global result
    result = message

def get_result():
    return result

def compare_metadata(reference, extracted, tolerance):
    """Compare reference metadata with extracted data."""
    comparison = {}
    ref_result = reference.get("result", {})
    
    for key in ref_result:
        ref_val = ref_result.get(key)
        ext_val = None
        
        # Extract value from different input types
        if isinstance(extracted, str):
            match = re.search(f"<{key}>(.*?)</{key}>", extracted)
            ext_val = float(match.group(1).strip()) if match else None
        elif isinstance(extracted, dict):
            ext_val = extracted.get("result", {}).get(key) or extracted.get(key)
        
        # Skip comparison if values are missing
        if ref_val is None or ext_val is None:
            comparison[key] = {"percent_diff": None, "passed": False, "message": "Missing value"}
            continue
        
        # Calculate percentage difference
        percent_diff = 0.0 if ref_val == 0 else abs(ref_val - ext_val) / abs(ref_val) * 100
        passed = percent_diff <= tolerance
        
        comparison[key] = {"percent_diff": percent_diff, "passed": passed}
    
    set_result("Comparison completed successfully.")
    return comparison, get_result()
