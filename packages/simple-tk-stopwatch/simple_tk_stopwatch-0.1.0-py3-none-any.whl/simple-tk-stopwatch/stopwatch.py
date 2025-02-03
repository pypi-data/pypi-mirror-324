import tkinter as tk
from tkinter import StringVar
 
 
class StopwatchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stopwatch")
        self.root.geometry("200x120")
        self.root.attributes('-topmost', True)  # Keep window on top

        self.running = False
        self.counter = 0
 
        # Configure grid to center the widgets
        self.root.rowconfigure(0, weight=1)  # Space above the timer
        self.root.rowconfigure(1, weight=1)  # Space above the buttons
        self.root.rowconfigure(2, weight=1)  # Space below the buttons
        self.root.columnconfigure(0, weight=1)  # Space left and right of content
 
        # Display for the timer
        self.time_var = StringVar()
        self.time_var.set("00:00:00")
        self.label = tk.Label(root, textvariable=self.time_var, font=("Helvetica", 18))
        self.label.grid(row=0, column=0, pady=8, sticky="n")
 
        # Start/Pause button
        self.start_pause_button = tk.Button(root, text="Start", command=self.start_pause, width=15, height=2)
        self.start_pause_button.grid(row=1, column=0, pady=3)
 
        # Reset button
        self.reset_button = tk.Button(root, text="Reset", command=self.reset, width=15, height=2)
        self.reset_button.grid(row=2, column=0, pady=3)
 
        # Ensure update_timer starts running
        self.update_timer()
 
    def start_pause(self):
        if self.running:
            self.running = False
            self.start_pause_button.config(text="Start")
        else:
            self.running = True
            self.start_pause_button.config(text="Pause")
 
    def reset(self):
        self.running = False
        self.counter = 0
        self.time_var.set("00:00:00")
        self.start_pause_button.config(text="Start")
 
    def update_timer(self):
        # Increment the counter if running
        if self.running:
            self.counter += 1
            self.time_var.set(self.format_time(self.counter))
 
        # Call update_timer again after 1000ms (1 second)
        self.root.after(1000, self.update_timer)
 
    def format_time(self, total_seconds):
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"
 
 
if __name__ == "__main__":
    root = tk.Tk()
    app = StopwatchApp(root)
    root.mainloop()
