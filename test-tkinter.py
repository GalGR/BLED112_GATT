#!/usr/bin/python3

import tkinter as tk
from tkinter import ttk

progressbar_styles = list()
progressbars = list()
outer_isopen = None
inner_isopen = None
inner_clicker = None
red_handle = None
reset_check = None
counter = None

PROGRESS_BAR_LEN = 300

def my_channel_row(frame, row, label, style):
    ttk.Label(
        frame,
        text=label
    ).grid(
        row=row,
        sticky=tk.W
    )

    row += 1

    ttk.Label(
        frame,
        text="Is Open"
    ).grid(
        row=row,
        column=0,
        sticky=tk.W
    )
    ttk.Label(
        frame,
        text="Channel 1"
    ).grid(
        row=row,
        column=1
    )
    ttk.Label(
        frame,
        text="Channel 2"
    ).grid(
        row=row,
        column=2
    )

    row += 1

    ttk.Checkbutton(
        frame,
        state=tk.DISABLED
    ).grid(
        row=row,
        column=0
    )
    w = ttk.Progressbar(
        frame,
        orient=tk.HORIZONTAL,
        length=PROGRESS_BAR_LEN,
        style=("%sChannel1" % style)
    )
    progressbars.append(w)
    w.grid(
        row=row,
        column=1
    )
    w = ttk.Progressbar(
        frame,
        orient=tk.HORIZONTAL,
        length=PROGRESS_BAR_LEN,
        style=("%sChannel2" % style)
    )
    progressbars.append(w)
    w.grid(
        row=row,
        column=2
    )

    return row + 1

def my_seperator(frame, row):
    ttk.Separator(
        frame,
        orient=tk.HORIZONTAL
    ).grid(
        pady=10,
        row=row,
        columnspan=3,
        sticky=(tk.W + tk.E)
    )
    return row + 1

def my_widgets(frame):
    # Add style for labeled progress bar
    for name in ["OuterHandleChannel1", "OuterHandleChannel2", "InnerHandleChannel1", "InnerHandleChannel2", "Clicker"]:
        style = ttk.Style(
            frame
        )
        progressbar_styles.append(style)
        style.layout(
            name,
            [
                (
                    "%s.trough" % name,
                    {
                        "children":
                        [
                            (
                                "%s.pbar" % name,
                                {"side": "left", "sticky": "ns"}
                            ),
                            (
                                "%s.label" % name,
                                {"sticky": ""}
                            )
                        ],
                        "sticky": "nswe"
                    }
                )
            ]
        )


    # Outer Handle
    row = 0
    row = my_channel_row(
        frame=frame,
        row=row,
        label="Outer Handle",
        style="OuterHandle"
    )

    # Seperator
    row = my_seperator(frame, row)

    # Inner Handle
    row = my_channel_row(
        frame=frame,
        row=row,
        label="Inner Handle",
        style="InnerHandle"
    )

    # Seperator
    row = my_seperator(frame, row)

    # Clicker labels
    ttk.Label(
        frame,
        text="Inner Clicker"
    ).grid(
        row=row,
        column=0,
        sticky=tk.W
    )
    ttk.Label(
        frame,
        text="Clicker"
    ).grid(
        row=row,
        column=1
    )

    row += 1

    # Clicker data
    inner_clicker = ttk.Checkbutton(
        frame,
        state=tk.DISABLED
    )
    inner_clicker.grid(
        row=row,
        column=0
    )
    w = ttk.Progressbar(
        frame,
        orient=tk.HORIZONTAL,
        length=PROGRESS_BAR_LEN,
        style="Clicker"
    )
    progressbars.append(w)
    w.grid(
        row=row,
        column=1
    )

    row += 1

    # Seperator
    row = my_seperator(frame, row)

    # Red handle and reset button labels
    ttk.Label(
        frame,
        text="Red Handle"
    ).grid(
        row=row,
        column=0,
        sticky=tk.W
    )
    ttk.Label(
        frame,
        text="Reset Button"
    ).grid(
        row=row,
        column=1
    )

    row += 1

    # Red handle and reset button data
    red_handle = ttk.Checkbutton(
        frame,
        state=tk.DISABLED
    )
    red_handle.grid(
        row=row,
        column=0
    )
    reset_check = ttk.Checkbutton(
        frame,
        state=tk.DISABLED
    )
    reset_check.grid(
        row=row,
        column=1
    )

    row += 1

    # Seperator
    row = my_seperator(frame, row)

    # Counter
    ttk.Label(
        frame,
        text="Counter"
    ).grid(
        row=row,
        column=0,
        sticky=tk.E,
    )
    counter = ttk.Entry(
        frame,
        width=20,
        state=tk.DISABLED
    ).grid(
        padx=10,
        pady=5,
        row=row,
        column=1,
        columnspan=2,
        sticky=tk.W,
    )

def main():
    # Initialize GUI variable
    root = tk.Tk()
    root.title("Test")

    my_widgets(root)

    # Start the GUI main loop
    root.mainloop()

if __name__ == "__main__":
    main()