import tkinter as tk
from core.case_builder import CaseBuilder

# Initialize Tkinter window and Text widget
root = tk.Tk()
text_widget = tk.Text(root, wrap=tk.WORD, height=15, width=50)
text_widget.pack()

# Initialize CaseBuilder
case_builder = CaseBuilder()

# Simulate appending lines (messages)
case_builder.append_line("Case Started")
case_builder.append_line("Step 1 completed")
case_builder.append_line("Step 2 completed")
case_builder.append_line("Case Finished")

# Export the result to Tkinter widget
case_builder.export_to_tkinter(text_widget)

# Run the Tkinter main loop
root.mainloop()
