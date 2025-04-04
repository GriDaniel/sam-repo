class CaseBuilder:
    def __init__(self):
        self.case_lines = []
    
    def append_line(self, message):
        """Append a new line to the case builder."""
        message = str(message) if message is not None else "No result message"
        self.case_lines.append(message)
    
    def get_all_lines(self):
        """Return all lines as a single string, separated by newlines."""
        return "\n\n".join(self.case_lines)  # Added extra newline for spacing
    
    def clear(self):
        """Clear all stored case lines."""
        self.case_lines = []
    
    def export_to_tkinter(self, tkinter_instance):
        """Export the case lines to a Tkinter widget."""
        tkinter_instance.delete('1.0', tk.END)  # Clear existing content
        tkinter_instance.insert('1.0', self.get_all_lines())
        tkinter_instance.yview_moveto(1)  # Scroll to the bottom
