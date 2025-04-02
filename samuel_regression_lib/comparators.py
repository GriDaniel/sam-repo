"""
Output comparison logic.
"""


class OutputComparator:
    """
    Compares output data with reference data.
    """

    def compare(self, actual_data, reference_data, tolerance_threshold):
        """
        Compare actual output data with reference data.

        Args:
            actual_data: Output data from script
            reference_data: Reference data from database
            tolerance_threshold: Maximum allowed percentage difference

        Returns:
            Dictionary containing comparison results
        """
        result = {
            "attributes": {},
            "overall_passed": True,
            "average_diff": 0.0
        }

        # Compare RESULT section attributes
        result_actual = actual_data.get("RESULT", {})
        result_reference = reference_data.get("RESULT", {})

        total_diff = 0.0
        count = 0

        for key in result_reference:
            expected = result_reference.get(key)
            actual = result_actual.get(key)

            # Skip if either value is missing
            if expected is None or actual is None:
                result["attributes"][key] = {
                    "expected": str(expected),
                    "actual": str(actual),
                    "diff_percentage": 0.0,
                    "passed": False
                }
                result["overall_passed"] = False
                continue

            # Calculate difference based on type
            if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
                # For numeric values, calculate percentage difference
                if expected == 0:
                    # Avoid division by zero
                    diff_pct = 100.0 if actual != 0 else 0.0
                else:
                    diff_pct = abs((actual - expected) / expected * 100.0)

                passed = diff_pct <= tolerance_threshold * 100.0

                result["attributes"][key] = {
                    "expected": expected,
                    "actual": actual,
                    "diff_percentage": diff_pct,
                    "passed": passed
                }

                total_diff += diff_pct
                count += 1

                if not passed:
                    result["overall_passed"] = False
            else:
                # For string values, check exact match
                passed = expected == actual

                result["attributes"][key] = {
                    "expected": str(expected),
                    "actual": str(actual),
                    "diff_percentage": 0.0 if passed else 100.0,
                    "passed": passed
                }

                if not passed:
                    result["overall_passed"] = False
                    total_diff += 100.0

                count += 1

        # Calculate average difference
        result["average_diff"] = total_diff / count if count > 0 else 0.0

        # Also check SLOPES section if available
        if "SLOPES" in reference_data and "SLOPES" in actual_data:
            # For simplicity, we just check if the number of SLOPE elements matches
            # A more detailed comparison would be needed for production use
            if len(reference_data["SLOPES"]) != len(actual_data["SLOPES"]):
                result["attributes"]["SLOPES_COUNT"] = {
                    "expected": len(reference_data["SLOPES"]),
                    "actual": len(actual_data["SLOPES"]),
                    "diff_percentage": 100.0,
                    "passed": False
                }
                result["overall_passed"] = False
            else:
                result["attributes"]["SLOPES_COUNT"] = {
                    "expected": len(reference_data["SLOPES"]),
                    "actual": len(actual_data["SLOPES"]),
                    "diff_percentage": 0.0,
                    "passed": True
                }

        return result