# Global result variable for comparator messages
result = ""

def set_result(message):
    global result
    result = message

def get_result():
    return result

def compare_metadata(reference, extracted, tolerance):
    """
    Compare two metadata dictionaries (specifically, their "result" sections)
    and compute the percentage differences for each key.
    """
    comparison = {}
    ref_result = reference.get("result", {})
    ext_result = extracted.get("result", {})

    for key in ref_result:
        ref_val = ref_result.get(key)
        ext_val = ext_result.get(key)
        if ref_val is None or ext_val is None:
            comparison[key] = {"percent_diff": None, "passed": False, "message": "Missing value"}
            continue
        if ref_val == 0:
            # If reference value is zero, define diff as 0 only if extracted is also zero.
            percent_diff = 0.0 if ext_val == 0 else float('inf')
        else:
            percent_diff = abs(ref_val - ext_val) / abs(ref_val) * 100
        passed = percent_diff <= tolerance
        comparison[key] = {"percent_diff": percent_diff, "passed": passed}
    
    set_result("Comparison completed successfully.")
    return comparison, get_result()
