"""
Core case builder functionality.
"""


class CaseBuilder:
    """
    Builds and maintains the test case results.
    """

    def __init__(self):
        """Initialize an empty case builder."""
        self.results = []
        self.connection_failed = False
        self.missing_references = []

    def append_message(self, message):
        """
        Append a message to the case builder.

        Args:
            message: String message to append
        """
        self.results.append(message)

    def append_results(self, filename, method, comparison_results):
        """
        Append test results to the case builder.

        Args:
            filename: Name of the tested file
            method: Method used for testing
            comparison_results: Dictionary containing comparison results
        """
        result_str = f"\n--- Test Results for '{filename}' with method '{method}' ---\n"

        # Add attribute-by-attribute comparison
        for attr, values in comparison_results['attributes'].items():
            expected = values['expected']
            actual = values['actual']
            diff_pct = values['diff_percentage']
            passed = values['passed']

            status = "PASS" if passed else "FAIL"
            result_str += f"{attr:15} | Expected: {expected:10} | Actual: {actual:10} | Diff: {diff_pct:.2f}% | {status}\n"

        # Add overall result
        overall_status = "PASS" if comparison_results['overall_passed'] else "FAIL"
        result_str += f"\nOverall Result: {overall_status}\n"
        result_str += f"Average Difference: {comparison_results['average_diff']:.2f}%\n"

        self.results.append(result_str)

    def get_results(self):
        """
        Get the complete case builder results as a string.

        Returns:
            String representation of all results
        """
        if not self.results:
            return "No test results available."

        # If connection failed, only return the first message (connection status)
        if self.connection_failed:
            return self.results[0]

        return "\n".join(self.results)