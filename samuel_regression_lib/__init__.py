"""
Samuel Regression Testing Library

A library for regression testing of XML data processing scripts.
"""

from .db import Database
from .extractors import XMLExtractor
from .comparators import OutputComparator
from .config import TOLERANCE_THRESHOLD
import os


class RegressionTest:
    """
    Main class for regression testing.
    Provides methods for testing, adding reference data, and retrieving results.
    """

    def __init__(self):
        """Initialize the regression testing framework."""
        self.db = Database()
        self.extractor = XMLExtractor()
        self.comparator = OutputComparator()
        self._case_builder = self._CaseBuilder()

        # Test database connection on initialization
        connection_status = self.db.test_connection()
        if connection_status:
            self._case_builder.append_message("Database connection successful")
        else:
            self._case_builder.append_message("Database connection unsuccessful")
            self._case_builder.connection_failed = True

    def test_file(self, filename, method, output_data):
        """
        Test a single file against reference data.

        Args:
            filename: Name of the input file
            method: Method name (e.g., "lq")
            output_data: Output data from the script to compare

        Returns:
            Self (for method chaining)
        """
        # Skip if connection failed
        if self._case_builder.connection_failed:
            return self

        # Check if reference data exists in database
        reference_data = self.db.get_reference_data(filename, method)

        if reference_data is None:
            self._case_builder.append_message(
                f"Warning: No reference data found for file '{filename}' with method '{method}'"
            )
            self._case_builder.missing_references.append((filename, method))
        else:
            # Compare output with reference
            comparison_results = self.comparator.compare(
                output_data, reference_data, TOLERANCE_THRESHOLD
            )
            self._case_builder.append_results(filename, method, comparison_results)

        return self

    # No add_file method - this functionality is only available through the CLI

    def get_results(self):
        """
        Get the complete case builder results as a string.

        Returns:
            String representation of all results
        """
        result = self._case_builder.get_results()

        # Add message about adding missing references if needed
        if self._case_builder.missing_references and not self._case_builder.connection_failed:
            result += "\n\nSome files were not found in the reference database. "
            result += "You can add them using the CLI tool:\n"
            result += "python -m samuel_regression_lib.cli add-reference /path/to/file method_name"

        return result

    def clear_results(self):
        """
        Clear all test results to start fresh.

        Returns:
            Self (for method chaining)
        """
        # Reset case builder but keep connection status
        connection_failed = self._case_builder.connection_failed
        self._case_builder = self._CaseBuilder()
        self._case_builder.connection_failed = connection_failed

        if connection_failed:
            self._case_builder.append_message("Database connection unsuccessful")
        else:
            self._case_builder.append_message("Database connection successful")

        return self

    class _CaseBuilder:
        """
        Inner class to build and maintain test case results.
        """

        def __init__(self):
            """Initialize an empty case builder."""
            self.results = []
            self.connection_failed = False
            self.missing_references = []

        def append_message(self, message):
            """Append a message to the case builder."""
            self.results.append(message)

        def append_results(self, filename, method, comparison_results):
            """Append test results to the case builder."""
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
            """Get the complete case builder results as a string."""
            if not self.results:
                return "No test results available."

            # If connection failed, only return the first message (connection status)
            if self.connection_failed:
                return self.results[0]

            return "\n".join(self.results)


# Expose only the RegressionTest class
__all__ = ['RegressionTest']