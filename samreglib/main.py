import os
import tkinter as tk
from core.case_builder import CaseBuilder
from core.db import get_db_connection, check_name_exists, get_metadata
from core.extractor import extract_metadata_from_xml
from core.comparator import compare_metadata
from core.xml_to_json import xml_to_json
from core.config import TOLERANCE_LEVEL

class MainApplication:
    def __init__(self):
        # Initialize CaseBuilder
        self.case_builder = CaseBuilder()
        self.case_builder.append_line("Application started")
        
        # Initialize database connection and append result to case_builder
        self.db, db_result = get_db_connection()
        self.case_builder.append_line(db_result)
        
        # Initialize Tkinter
        self.root = tk.Tk()
        self.root.title("SAM Registry File Tester")
        self.text_widget = tk.Text(self.root, wrap=tk.WORD, height=20, width=80)
        self.text_widget.pack(padx=10, pady=10)
    
    def test_file(self, filename, method_name, file_path):
        """
        Test a file by extracting its metadata and comparing with reference data.
        
        Args:
            filename (str): Name of the file
            method_name (str): Method name for database lookup
            file_path (str): Path to the file
        """
        # Check if file exists and append result to case_builder
        if not os.path.exists(file_path):
            self.case_builder.append_line(f"File '{filename}' does not exist at path: {file_path}")
            return False
        
        self.case_builder.append_line(f"File '{filename}' found at path: {file_path}")
        
        try:
            # Extract data from file
            if file_path.lower().endswith('.xml'):
                # Extract metadata from XML
                extracted_metadata, extract_result = extract_metadata_from_xml(file_path)
                self.case_builder.append_line(extract_result)
            
            else:
                self.case_builder.append_line(f"Unsupported file format for '{filename}'")
                return False
            
            # Check if reference data exists in database
            exists, exists_result = check_name_exists(self.db, method_name, filename)
            self.case_builder.append_line(exists_result)
            
            if not exists:
                self.case_builder.append_line(f"No reference data found for '{filename}' in method '{method_name}'")
                return False
            
            # Get reference metadata from database
            reference_metadata, metadata_result = get_metadata(self.db, method_name, filename)
        
            
            # Compare metadata using the configured tolerance level
            # TOLERANCE_LEVEL is stored as decimal (e.g., 0.05), convert to percentage for comparator
            comparison, compare_result = compare_metadata(reference_metadata, extracted_metadata, TOLERANCE_LEVEL * 100)
            self.case_builder.append_line(compare_result)
            
            # Append comparison results
            all_passed = True
            for key, value in comparison.items():
                passed = value.get("passed", False)
                if not passed:
                    all_passed = False
                status = "PASSED" if passed else "FAILED"
                percent_diff = value.get("percent_diff")
                if percent_diff is not None:
                    percent_diff_str = f"{percent_diff:.2f}%"
                else:
                    percent_diff_str = "N/A"
                self.case_builder.append_line(f"Comparison for '{key}': {status} (Difference: {percent_diff_str})")
            
            # Overall result
            if all_passed:
                self.case_builder.append_line(f"Overall test for '{filename}': PASSED")
            else:
                self.case_builder.append_line(f"Overall test for '{filename}': FAILED")
            
            return all_passed
            
        except Exception as e:
            self.case_builder.append_line(f"Error processing file '{filename}': {str(e)}")
            return False
    
    def display_results(self):
        """Display results in the Tkinter window."""
        self.case_builder.export_to_tkinter(self.text_widget)
        self.root.mainloop()

def main():
    app = MainApplication()
    
    # Use the correct path to the test data
    test_data_path = r"C:\Users\danis\OneDrive\Desktop\Simons\samreglib\testData"
    
    # Example: Test a file (replace example.xml with your actual XML filename)
    xml_filename = "example.xml"  # Change this to your actual XML file name
    full_path = os.path.join(test_data_path, xml_filename)
    
    app.test_file(xml_filename, "exampleTest", full_path)
    
    # Display results
    app.display_results()

if __name__ == "__main__":
    main()
