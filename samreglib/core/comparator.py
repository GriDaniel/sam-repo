# Global result variable for comparator messages
result = ""

def set_result(message):
    global result
    result = message

def get_result():
    return result

def compare_metadata(reference, extracted, tolerance):
    """
    Compare two metadata dictionaries and compute the percentage differences.
    """
    comparison = {}
    
    # Get result section from reference
    ref_result = reference.get("result", {})
    
    # Get result section from extracted data (or use directly if it's already the result)
    if isinstance(extracted, dict) and "result" in extracted:
        ext_result = extracted["result"]
    else:
        ext_result = extracted  # Use directly if it doesn't have a result key
    
    # Compare values for each key in reference
    for key in ref_result:
        ref_val = ref_result.get(key)
        ext_val = ext_result.get(key) if isinstance(ext_result, dict) else None
        
        if ref_val is None or ext_val is None:
            comparison[key] = {"percent_diff": None, "passed": False, "message": "Missing value"}
            continue
            
        # Calculate percentage difference
        if ref_val == 0:
            percent_diff = 0.0 if ext_val == 0 else float('inf')
        else:
            percent_diff = abs(ref_val - ext_val) / abs(ref_val) * 100
            
        # Check if within tolerance
        passed = percent_diff <= tolerance
        comparison[key] = {"percent_diff": percent_diff, "passed": passed}
    
    set_result("Comparison completed successfully.")
    return comparison, get_result()
