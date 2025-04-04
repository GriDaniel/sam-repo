class CaseBuilder:
    def __init__(self):
        # Initialize an empty list to hold the case lines (strings)
        self.case_lines = []
    
    def append_line(self, message):
        """
        Append a new line to the case builder.
        Converts None values to a string representation.
        """
        if message is None:
            message = "No result message"  # Convert None to a default message
        
        # Ensure message is a string
        message = str(message)
        self.case_lines.append(message)
    
    def get_all_lines(self):
        """Return all lines as a single string, separated by newlines."""
        return "\n".join(self.case_lines)
    
    def clear(self):
        """Clear all stored case lines."""
        self.case_lines = []
    
    def export_to_tkinter(self, tkinter_instance):
        """Export the case lines to a Tkinter platform for display."""
        # Assuming tkinter_instance is a Text widget or something similar
        tkinter_instance.insert('1.0', self.get_all_lines())
        tkinter_instance.yview_moveto(1)  # Scroll to the bottom if needed
