


"""
Main interface for the regression testing library.
"""

from samuel_regression_lib.db import MongoConnector
from samuel_regression_lib.xml_extractor import XMLExtractor
from samuel_regression_lib.case_builder import CaseBuilder
from samuel_regression_lib.cli import main
import samuel_regression_lib.config



class RegressionTest:
    """Main class for regression testing."""

    def __init__(self):
        """Initialize the regression test with MongoDB connection check."""
        self.mongo = MongoConnector()
        self.case_builder = CaseBuilder()

        # Check database connection
        status, message = self.mongo.connect()
        self.case_builder.set_connection_status(status, message)

    def test_file(self, filename, method, actual_output=None):
        """
        Test a file against reference data.

        Args:
            filename (str): Name of the file to test
            method (str): Method name to look under in the database
            actual_output (dict, optional): Actual output data if already available

        Returns:
            str: Test status ("PASS", "FAIL", "WARN", "ERROR")
        """
        # FIX: Check if db is None properly
        if self.mongo.db is None:
            return "ERROR"

        # Find reference data
        reference = self.mongo.find_reference(method, filename)

        if not reference:
            self.case_builder.add_case(filename, method, "WARN", "Reference not found")
            return "WARN"

        # If actual output isn't provided, try to extract it from the reference XML
        if actual_output is None:
            try:
                actual_output = XMLExtractor.extract_output_data(reference["xml_data"])
            except Exception as e:
                self.case_builder.add_case(filename, method, "ERROR", f"Failed to extract output: {str(e)}")
                return "ERROR"

        # Compare outputs
        overall_pass, details = self.case_builder.compare_outputs(
            actual_output, reference["output_data"], config.TOLERANCE_THRESHOLD
        )

        # Add case
        status = "PASS" if overall_pass else "FAIL"
        self.case_builder.add_case(filename, method, status, details)

        return status

    def get_results(self):
        """
        Get the results of all tests.

        Returns:
            str: Formatted test results
        """
        return self.case_builder.get_result()