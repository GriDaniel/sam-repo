# test_storage.py
import os
import shutil
import unittest
from my_xml_tester.storage import check_file_exists_and_log, compare_output_with_reference_and_log

TEST_DB_DIR = "test_dbStorage"
TEST_METHOD_NAME = "testMethod"

class TestStorageFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up a temporary test database directory."""
        cls.method_dir = os.path.join(TEST_DB_DIR, TEST_METHOD_NAME)
        os.makedirs(cls.method_dir, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        """Clean up after tests."""
        shutil.rmtree(TEST_DB_DIR)

    def test_check_file_exists_and_log(self):
        """Check if the function properly detects existing and missing files."""
        test_filename = "existing_file.xml"
        test_filepath = os.path.join(self.method_dir, test_filename)

        # Create a file to simulate an existing entry
        with open(test_filepath, "w") as f:
            f.write("<root><AnalyzerResult><Height>100</Height></AnalyzerResult></root>")

        # Check if the file exists
        self.assertTrue(check_file_exists_and_log(test_filepath, TEST_METHOD_NAME))

        # Check a non-existent file
        missing_filepath = os.path.join(self.method_dir, "missing_file.xml")
        self.assertFalse(check_file_exists_and_log(missing_filepath, TEST_METHOD_NAME))

    def test_compare_output_with_reference_and_log(self):
        """Ensure correct behavior when comparing XML output to reference."""
        test_filename = "test_compare.xml"
        reference_filepath = os.path.join(self.method_dir, test_filename)
        output_filepath = os.path.join(self.method_dir, "output_test.xml")

        # Create a reference XML file
        reference_xml = "<root><AnalyzerResult><Height>100</Height></AnalyzerResult></root>"
        with open(reference_filepath, "w") as f:
            f.write(reference_xml)

        # Case 1: Matching XML (should pass)
        with open(output_filepath, "w") as f:
            f.write(reference_xml)

        compare_output_with_reference_and_log(test_filename, TEST_METHOD_NAME, output_filepath)

        # Case 2: Different XML (should fail)
        with open(output_filepath, "w") as f:
            f.write("<root><AnalyzerResult><Height>110</Height></AnalyzerResult></root>")

        compare_output_with_reference_and_log(test_filename, TEST_METHOD_NAME, output_filepath)

if __name__ == "__main__":
    unittest.main()
