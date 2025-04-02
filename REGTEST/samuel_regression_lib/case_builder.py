"""
Test case management for the regression testing library.
"""

import samuel_regression_lib.config as config  # Use appropriate import based on your structure


class CaseBuilder:
    """Manages test cases and results."""

    def __init__(self):
        self.cases = []
        self.connection_status = None

    def set_connection_status(self, status, message):
        """
        Set the connection status for the case builder.

        Args:
            status (bool): Connection status
            message (str): Connection message
        """
        self.connection_status = (status, message)
        self.cases.append(message)

    def add_case(self, filename, method, status, details=None):
        """
        Add a case to the case builder.

        Args:
            filename (str): Name of the file being tested
            method (str): Method name
            status (str): Status of the test (e.g., "PASS", "FAIL", "WARN")
            details (dict, optional): Additional details about the test
        """
        # FIX: Check connection status explicitly
        if self.connection_status is None or not self.connection_status[0]:
            # If connection was unsuccessful, don't add more cases
            return

        # Build the case text
        case_text = f"File: {filename}, Method: {method}, Status: {status}"
        if details:
            case_text += f"\nDetails: {details}"

        self.cases.append(case_text)

    def compare_outputs(self, actual, reference, tolerance=None):
        """
        Compare actual output with reference output.

        Args:
            actual (dict): Actual output data
            reference (dict): Reference output data
            tolerance (float, optional): Tolerance threshold (defaults to config value)

        Returns:
            tuple: (overall_pass, details)
        """
        if tolerance is None:
            tolerance = config.TOLERANCE_THRESHOLD

        # FIX: Check dictionaries properly
        if actual is None or reference is None:
            return False, "Missing data for comparison"

        comparison = {}
        percentage_diff = {}
        overall_pass = True

        for key in reference:
            if key in actual:
                comparison[key] = {
                    "reference": reference[key],
                    "actual": actual[key]
                }

                # Calculate percentage difference if values are numeric
                if isinstance(reference[key], (int, float)) and isinstance(actual[key], (int, float)):
                    if reference[key] == 0:
                        # Avoid division by zero
                        if actual[key] == 0:
                            diff = 0
                        else:
                            diff = 1  # 100% different if reference is 0 but actual is not
                    else:
                        diff = abs(reference[key] - actual[key]) / abs(reference[key])

                    percentage_diff[key] = diff * 100

                    # Check if within tolerance
                    if diff > tolerance:
                        overall_pass = False
                else:
                    # For non-numeric values, check equality
                    if reference[key] != actual[key]:
                        overall_pass = False
                        percentage_diff[key] = "N/A (non-numeric comparison)"
                    else:
                        percentage_diff[key] = 0
            else:
                comparison[key] = {
                    "reference": reference[key],
                    "actual": "Missing"
                }
                percentage_diff[key] = "N/A (missing in actual)"
                overall_pass = False

        # Check for keys in actual that aren't in reference
        for key in actual:
            if key not in reference:
                comparison[key] = {
                    "reference": "Missing",
                    "actual": actual[key]
                }
                percentage_diff[key] = "N/A (missing in reference)"
                overall_pass = False

        return overall_pass, {
            "comparison": comparison,
            "percentage_diff": percentage_diff,
            "overall_pass": overall_pass
        }

    def get_result(self):
        """
        Get the complete case builder result.

        Returns:
            str: Formatted result string
        """
        result = "\n".join(self.cases)

        # Add CLI hint if any tests were not found
        if any("not found" in case for case in self.cases):
            result += "\n\nNote: Some files were not found in the database. "
            result += "You can add them using the CLI: python -m regression_test add-reference <filepath> <method>"

        return result