import os
import sys
import tkinter as tk

# Ensure correct import path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.case_builder import CaseBuilder
from core.db import get_db_connection, check_name_exists, get_metadata
from core.comparator import compare_metadata
from core.config import TOLERANCE_LEVEL

# Global instance for library mode
_app_instance = None

class MainApplication:
    def __init__(self):
        self.case_builder = CaseBuilder()
        self.case_builder.append_line("Application started")
        self.db, db_result = get_db_connection()
        self.case_builder.append_line(db_result)
        
        self.root = tk.Tk()
        self.root.title("SAM Registry File Tester")
        self.text_widget = tk.Text(self.root, wrap=tk.WORD, height=20, width=80)
        self.text_widget.pack(padx=10, pady=10)
    
    def test_file(self, filename, method_name, extracted_data):
        try:
            exists, result = check_name_exists(self.db, method_name, filename)
            self.case_builder.append_line(result)
            if not exists:
                self.case_builder.append_line(f"No reference data for '{filename}' in '{method_name}'")
                return False
                
            reference_metadata, result = get_metadata(self.db, method_name, filename)
            self.case_builder.append_line(result)
            comparison, result = compare_metadata(reference_metadata, extracted_data, TOLERANCE_LEVEL * 100)
            self.case_builder.append_line(result)
            
            all_passed = all(v.get("passed", False) for v in comparison.values())
            for key, value in comparison.items():
                status = "PASSED" if value.get("passed", False) else "FAILED"
                percent_diff = value.get('percent_diff')
                if percent_diff is not None:
                    diff = f"{percent_diff:.2f}%"
                else:
                    diff = "N/A"
                self.case_builder.append_line(f"{key}: {status} (Diff: {diff})")
            
            self.case_builder.append_line(f"Overall: {'PASSED' if all_passed else 'FAILED'}")
            return all_passed
            
        except Exception as e:
            self.case_builder.append_line(f"Error: {str(e)}")
            return False
    
    def display_results(self):
        self.case_builder.export_to_tkinter(self.text_widget)
        self.root.mainloop()

# Singleton Instance Handling
def get_app_instance():
    global _app_instance
    if _app_instance is None:
        _app_instance = MainApplication()
    return _app_instance

def test_file(filename, method_name, extracted_data):
    """
    Test a file using the shared application instance.
    
    Args:
        filename (str): Name of the file
        method_name (str): Method name for database lookup
        extracted_data (dict): Extracted metadata from an XML file
        
    Returns:
        bool: True if the test passed, False otherwise
    """
    app = get_app_instance()
    return app.test_file(filename, method_name, extracted_data)

def display_results():
    """Display all accumulated results using the shared application instance."""
    app = get_app_instance()
    app.display_results()

# Make sure these functions are exported
__all__ = ['test_file', 'display_results', 'MainApplication', 'get_app_instance']

# Simple entry point without example implementation
if __name__ == "__main__":
    print("SAM Registry Testing Library")
    print("This module is designed to be imported and used by external scripts.")
