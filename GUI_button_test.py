#!/usr/bin/python3

import pygatt
from binascii import hexlify
import sys
import argparse

import tkinter as tk
from tkinter import ttk

import platform
BACKEND = None
if platform.system() == "Linux":
    BACKEND = "GATTTOOL"
elif platform.system() == "Windows":
    BACKEND = "BLED112"

SCAN_TIMEOUT = 3
print_cntr = 0
prev_int_outer_handle_channel1 = 0
red_handle_ignore_val = 0

MY_CHAR_UUID = "f0001143-0451-4000-b000-000000000000"

OUTER_HANDLE_CHANNEL1_STYLE = "OuterHandleChannel1"
OUTER_HANDLE_CHANNEL2_STYLE = "OuterHandleChannel2"
INNER_HANDLE_CHANNEL1_STYLE = "InnerHandleChannel1"
INNER_HANDLE_CHANNEL2_STYLE = "InnerHandleChannel2"
CLICKER_STYLE = "Clicker"

style_names = [
    OUTER_HANDLE_CHANNEL1_STYLE,
    OUTER_HANDLE_CHANNEL2_STYLE,
    INNER_HANDLE_CHANNEL1_STYLE,
    INNER_HANDLE_CHANNEL2_STYLE,
    CLICKER_STYLE
]

progressbar_styles = list()
progressbars = list()
isopen = list()
inner_clicker = list()
red_handle = list()
reset_check = list()
counter_entry = list()
clicker_counter_entry = list()
ignore_red = list()

root = None

def update_checkbox(checkbox, bool_value):
    if (bool_value):
        checkbox.select()
    else:
        checkbox.deselect()

def toggle_val(value):
    if (value):
        value = 0
    else:
        value = 1
    return value

def ignoreCallBack():
   global red_handle_ignore_val
   print( "ignoreCallBack:", "ignore red handle")
   print( "red_handle_ignore:", str(red_handle_ignore_val))
   red_handle_ignore_val = toggle_val(red_handle_ignore_val)
   checkbox_ignore_red = ignore_red
   update_checkbox(checkbox_ignore_red, red_handle_ignore_val)

   

def handle_my_char_data(handle, value):
    """
    handle -- integer, characteristic read handle the data was received on
    value -- bytearray, the data returned in the notification
    """
    global print_cntr
    global prev_int_outer_handle_channel1
    global red_handle_ignore_val
    
    # print("Received data: %s %s" % hexlify(value) str(print_cntr))
    if (print_cntr % 10 ) == 0:
        s = "Received data: " + str(hexlify(value)) + "  " + str(print_cntr)
        print(s)
    print_cntr += 1 

    # 
    digital = (int(value[1]) << 8) + int(value[0])
    analog = [(int(value[i + 1]) << 8) + int(value[i]) for i in range(2, 5 * 2 + 1, 2)]
    # counter = (int(value[12]) << 8) + int(value[13]) # This value is big endian
    # use only 8 bits from the MSP counter value 
    # ( leave hi nibble for something else: clicker_counter... )
    counter = int(value[13]) # use only 8 bits
    clicker_counter = int(value[12]) # use only 8 bits
    
    # print the "MSP Version" out of special info packet
    if (digital == 0x3101):
        if (analog[0] == 0x1965):
            s = 'MSP Version: ' + repr(analog[2]) + '.' + repr(analog[3]) + '.' + repr(analog[4])
            print(s)

    encoder1 = analog[3]
    encoder2 = analog[0]
    encoder3 = analog[1]
    encoder4 = analog[2]
    clicker_analog = analog[4]

    bool_inner_isopen = bool((digital >> 0) & 0x0001)
    bool_outer_isopen = bool((digital >> 1) & 0x0001)
    bool_clicker = bool((digital >> 2) & 0x0001)
    bool_reset = bool((digital >> 4) & 0x0001)
    bool_red_handle = bool((digital >> 7) & 0x0001)
    int_outer_handle_channel1 = analog[1]
    int_outer_handle_channel2 = analog[2]
    int_inner_handle_channel1 = analog[0]
    int_inner_handle_channel2 = analog[3]
    int_clicker = clicker_analog
    int_counter = counter
    int_clicker_counter = clicker_counter
    precentage_outer_handle_channel1 = int((int_outer_handle_channel1 / 4096) * 100)
    precentage_outer_handle_channel2 = int((int_outer_handle_channel2 / 4096) * 100)
    precentage_inner_handle_channel1 = int((int_inner_handle_channel1 / 4096) * 100)
    precentage_inner_handle_channel2 = int((int_inner_handle_channel2 / 4096) * 100)
    precentage_clicker = int((int_clicker / 4096) * 100)
    
    # calc delta once every second 
    if (print_cntr % 5 ) == 0:
        Delta = -(prev_int_outer_handle_channel1 - int_outer_handle_channel1)
        if( Delta > 2 or Delta < -2 ):
            s = 'Delta: ' + repr(Delta) 
            print( s )
        prev_int_outer_handle_channel1 = int_outer_handle_channel1

    progressbar_style_outer_handle_channel1 = progressbar_styles[0]
    progressbar_style_outer_handle_channel2 = progressbar_styles[1]
    progressbar_style_inner_handle_channel1 = progressbar_styles[2]
    progressbar_style_inner_handle_channel2 = progressbar_styles[3]
    progressbar_style_clicker = progressbar_styles[4]
    progressbar_outer_handle_channel1 = progressbars[0]
    progressbar_outer_handle_channel2 = progressbars[1]
    progressbar_inner_handle_channel1 = progressbars[2]
    progressbar_inner_handle_channel2 = progressbars[3]
    progressbar_clicker = progressbars[4]
    checkbox_outer_handle_isopen = isopen[0]
    checkbox_inner_handle_isopen = isopen[1]
    checkbox_inner_clicker = inner_clicker
    checkbox_red_handle = red_handle
    checkbox_reset_check = reset_check
    checkbox_red_handle_ignore_val = red_handle_ignore_val
    entry_counter = counter_entry
    entry_clicker_counter = clicker_counter_entry

    progressbar_style_outer_handle_channel1.configure(
        OUTER_HANDLE_CHANNEL1_STYLE,
        text=("%d" % int_outer_handle_channel1)
    )
    progressbar_style_outer_handle_channel2.configure(
        OUTER_HANDLE_CHANNEL2_STYLE,
        text=("%d" % int_outer_handle_channel2)
    )
    progressbar_style_inner_handle_channel1.configure(
        INNER_HANDLE_CHANNEL1_STYLE,
        text=("%d" % int_inner_handle_channel1)
    )
    progressbar_style_inner_handle_channel2.configure(
        INNER_HANDLE_CHANNEL2_STYLE,
        text=("%d" % int_inner_handle_channel2)
    )
    progressbar_style_clicker.configure(
        CLICKER_STYLE,
        text=("%d" % int_clicker)
    )

    progressbar_outer_handle_channel1["value"] = precentage_outer_handle_channel1
    progressbar_outer_handle_channel2["value"] = precentage_outer_handle_channel2
    progressbar_inner_handle_channel1["value"] = precentage_inner_handle_channel1
    progressbar_inner_handle_channel2["value"] = precentage_inner_handle_channel2
    progressbar_clicker["value"] = precentage_clicker

    update_checkbox(checkbox_outer_handle_isopen, bool_outer_isopen)
    update_checkbox(checkbox_inner_handle_isopen, bool_inner_isopen)
    update_checkbox(checkbox_inner_clicker, bool_clicker)
    update_checkbox(checkbox_red_handle, bool_red_handle)
    update_checkbox(checkbox_reset_check, bool_reset)
    update_checkbox(checkbox_red_handle_ignore_val, red_handle_ignore_val)

    entry_counter.delete(0, tk.END)
    entry_counter.insert(tk.END, "%d" % int_counter)

    entry_clicker_counter.delete(0, tk.END)
    entry_clicker_counter.insert(tk.END, "%d" % int_clicker_counter)

    root.update()

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

    w = tk.Checkbutton(
        frame,
        state=tk.DISABLED
    )
    isopen.append(w)
    w.grid(
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
    for name in style_names:
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
        style.configure(name, background="lime")


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
    ttk.Label(
        frame,
        text="Clicker Counter"
    ).grid(
        row=row,
        column=2
    )

    row += 1

    # Clicker data
    w = tk.Checkbutton(
        frame,
        state=tk.DISABLED
    )
    global inner_clicker
    inner_clicker = w
    w.grid(
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
    # yg: adding clicker counter display
    w = ttk.Entry(
        frame,
        width=20,
    )
    global clicker_counter_entry
    clicker_counter_entry = w
    w.grid(
        # padx=10,
        # pady=5,
        row=row,
        column=2,
        # sticky=tk.W,
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

    ttk.Label(
        frame,
        text="Ignore RedHandle fault"
    ).grid(
        row=row,
        column=2
    )

    row += 1

    # Red handle and reset button data
    w = tk.Checkbutton(
        frame,
        state=tk.DISABLED
    )
    global red_handle
    red_handle = w
    w.grid(
        row=row,
        column=0
    )
    w = tk.Checkbutton(
        frame,
        state=tk.DISABLED
    )
    global reset_check
    reset_check = w
    w.grid(
        row=row,
        column=1
    )
# B = tkinter.Button(top, text ="Hello", command = ignoreCallBack)
    
    w = tk.Button(
        frame,
        text ="send ignore",
        command = ignoreCallBack
    )
    global red_handle_ignore
    red_handle_ignore = w
    w.grid(
        row=row,
        column=3
    )
    
    # checkbox for the ignore red handle 
    w = tk.Checkbutton(
        frame,
        state=tk.DISABLED
    )
    global ignore_red
    ignore_red = w
    w.grid(
        row=row,
        column=2
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
    w = ttk.Entry(
        frame,
        width=20,
        # state=tk.DISABLED
    )
    global counter_entry
    counter_entry = w
    w.grid(
        padx=10,
        pady=5,
        row=row,
        column=1,
        columnspan=2,
        sticky=tk.W,
    )

def init_parser():
    parser = argparse.ArgumentParser(
        description="Read the GATT data characteristic from C-TAG over BLE.\nIf no argument is given, the program scans for devices and prompts the user to select which device to connect to."
    )
    parser.add_argument(
        "-n", "--name",
        dest="name",
        metavar="DEVICE_NAME",
        type=str,
        nargs=1,
        required=False,
        help="connects to the device with the given name"
    )
    parser.add_argument(
        "-a", "--address",
        dest="address",
        metavar="MAC_ADDRESS",
        type=str,
        nargs=1,
        required=False,
        help="connects to the device with the MAC address"
    )
    return parser

def main():
    # Parse the command line arguments
    parser = init_parser()
    args = parser.parse_args(sys.argv[1:])

    # Initialize the flags according from the command line arguments
    avail_address = args.address != None
    avail_name = args.name != None
    do_scan = (not avail_address) or avail_name
    manual_mode = (not avail_address) and (not avail_name)
    verify_mode = avail_address and avail_name

    # Initialize the adapter according to the backend used
    adapter = None
    if BACKEND == "BLED112":
        adapter = pygatt.BGAPIBackend() # BLED112 backend for Windows
    elif BACKEND == "GATTTOOL":
        adapter = pygatt.GATTToolBackend() # GATTtool backend for Linux

    device = None

    gui_only = 1
    
    if (gui_only == 0):
        pass

    # try:
        # # Connect to BLED112
        # adapter.start()

        # # Scan for available BLE devices
        # if (do_scan):
            # print("Scanning devices for %s seconds..." % str(SCAN_TIMEOUT))
            # device_li = adapter.scan(timeout=SCAN_TIMEOUT)
            # i = 1
            # for d in device_li:
                # print("%s. %s -- %s" % (str(i), str(d["address"]), str(d["name"])))
                # i += 1

            # # Check list size
            # if len(device_li) == 0:
                # print("No device found!")
                # return

        # device_address = None
        

        # # Ask the user which device to connect to
        # if (manual_mode):
            # print("\nSelect which device to connect to (0 to exit):")
            # device_ind = None
            # while (device_ind == None):
                # user_in = input()
                # try:
                    # user_in = int(user_in)
                    # if (user_in == 0):
                        # return
                    # if (user_in < 0 or user_in > len(device_li)):
                        # raise
                    # device_ind = user_in - 1
                # except:
                    # print("Invalid input")
            # device_address = device_li[device_ind]["address"]

        # else:
            # if (avail_name):
                # found = False
                # error_name = False
                # error_address = False
                # for d in device_li:
                    # if (verify_mode):
                        # if (d["address"] == args.address[0] and d["name"] != args.name[0]):
                            # error_name = True
                            # break
                        # if (d["address"] != args.address[0] and d["name"] == args.name[0]):
                            # error_address = True
                            # break
                    # if (d["name"] == args.name[0] and ((not verify_mode) or (verify_mode and d["address"] == args.address[0]))):
                        # device_address = d["address"]
                        # found = True
                        # break
                # if (not found):
                    # print("Couldn't find the device")
                    # if (error_address):
                        # print("Warning: Found a device with that name but with a different address")
                    # if (error_name):
                        # print("Warning: Found a device with that address but with a different name")
                    # return
            # else:
                # device_address = args.address[0]
    
    else:        
        # Initialize the main window
        global root
        root = tk.Tk()
        root.title("C-TAG BLE")

        # Initialize the GUI widgets
        my_widgets(root)

        # Connect to the device
        # print("\nConnecting to the selected device...")
        # device = adapter.connect(address=device_address)
        # print("Connected successfully!\n")

        # # Subscribe to the wanted characteristic data
        # print("Subscribing to the characteristic with UUID %s..." % MY_CHAR_UUID)
        # device.subscribe(MY_CHAR_UUID, callback=handle_my_char_data)
        # print("Subscribed to the characteristic successfully!\n")

        # Run the GUI main loop
        root.mainloop()
    # finally:
        # if device != None:
            # device.disconnect()
        # adapter.stop()

if __name__ == "__main__":
    main()