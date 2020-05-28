#!/usr/bin/python3

import tkinter as tk
from tkinter import ttk

PROGRESS_BAR_LEN = 500

def my_widgets(frame):
    # Add widgets to the GUI
    progress_bar = ttk.Progressbar(
        frame,
        orient=tk.HORIZONTAL,
        length=PROGRESS_BAR_LEN,
        mode='determinate'
    )

    # Update the progress bar value
    def bar():
        import time
        progress_bar["value"] = 50
        frame.update_idletasks()
        time.sleep(1)
        progress_bar["value"] = 10
        frame.update_idletasks()

    progress_bar.pack(pady=10)

    button = ttk.Button(
        frame,
        text="Start",
        command=bar
    )
    button.pack(pady=10)

def main():
    # Initialize GUI variable
    top = tk.Tk()

    # Add widgets to the GUI
    my_widgets(top)

    # Start the GUI main loop
    top.mainloop()

if __name__ == "__main__":
    main()