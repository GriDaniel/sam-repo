# Global result variable for comparator messages
result = ""

def set_result(message):
    global result
    result = message

def get_result():
    return result

def compare_metadata(reference, extracted, tolerance):
    """
    Compare two metadata dictionaries with debug output.
    """
    comparison = {}
    
    # Debug output for input types
    print("\n==== DEBUG: COMPARISON INPUT ====")
    print(f"Reference type: {type(reference)}")
    print(f"Extracted type: {type(extracted)}")
    
    # Get result section from reference
    ref_result = reference.get("result", {})
    
    # Get result section from extracted data
    if isinstance(extracted, dict) and "result" in extracted:
        ext_result = extracted["result"]
    else:
        ext_result = extracted  # Use directly if it doesn't have a result key
    
    # Debug output for result sections
    print("\n==== DEBUG: RESULT SECTIONS ====")
    print(f"Reference result type: {type(ref_result)}")
    print(f"Reference result keys: {list(ref_result.keys()) if isinstance(ref_result, dict) else 'NOT A DICT'}")
    print(f"Extracted result type: {type(ext_result)}")
    print(f"Extracted result keys: {list(ext_result.keys()) if isinstance(ext_result, dict) else 'NOT A DICT'}")
    
    # Compare values for each key in reference
    print("\n==== DEBUG: KEY COMPARISONS ====")
    for key in ref_result:
        ref_val = ref_result.get(key)
        ext_val = ext_result.get(key) if isinstance(ext_result, dict) else None
        
        print(f"\nComparing key: {key}")
        print(f"  Reference value: {ref_val} (type: {type(ref_val)})")
        print(f"  Extracted value: {ext_val} (type: {type(ext_val)})")
        
        if ref_val is None:
            print("  ISSUE: Reference value is None")
            comparison[key] = {"percent_diff": None, "passed": False, "message": "Reference value is None"}
            continue
            
        if ext_val is None:
            print("  ISSUE: Extracted value is None (missing key or null)")
            comparison[key] = {"percent_diff": None, "passed": False, "message": "Extracted value is None"}
            continue
            
        # Try to convert to float if they're strings
        try:
            if isinstance(ref_val, str):
                ref_val = float(ref_val)
                print(f"  Converted reference string to float: {ref_val}")
            if isinstance(ext_val, str):
                ext_val = float(ext_val)
                print(f"  Converted extracted string to float: {ext_val}")
        except ValueError as e:
            print(f"  ISSUE: Value conversion error: {e}")
            comparison[key] = {"percent_diff": None, "passed": False, "message": f"Value conversion error: {e}"}
            continue
            
        # Calculate percentage difference
        try:
            if ref_val == 0:
                if ext_val == 0:
                    percent_diff = 0.0
                    print("  Both values are zero, setting diff to 0")
                else:
                    percent_diff = float('inf')
                    print("  Reference is zero but extracted is not, setting diff to infinity")
            else:
                percent_diff = abs(ref_val - ext_val) / abs(ref_val) * 100
                print(f"  Calculated percent diff: {percent_diff:.2f}%")
                
            # Check if within tolerance
            passed = percent_diff <= tolerance
            print(f"  Within tolerance ({tolerance}%)? {passed}")
            comparison[key] = {"percent_diff": percent_diff, "passed": passed}
            
        except Exception as e:
            print(f"  ISSUE: Error calculating difference: {e}")
            comparison[key] = {"percent_diff": None, "passed": False, "message": f"Calculation error: {e}"}
    
    set_result("Comparison completed with debug info.")
    return comparison, get_result()
