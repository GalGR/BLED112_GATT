#!/usr/bin/python3

import pygatt
from binascii import hexlify
import threading

import platform
BACKEND = None
if platform.system() == "Linux":
    BACKEND = "GATTTOOL"
elif platform.system() == "Windows":
    BACKEND = "BLED112"

DEVICE_NAME = "Gal_C-TAG__2_____"
SCAN_TIMEOUT = 3

MY_CHAR_UUID = "f0001143-0451-4000-b000-000000000000"
MY_CHAR_CCCD_HND = 0x2a

def handle_my_char_data(handle, value):
    """
    handle -- integer, characteristic read handle the data was received on
    value -- bytearray, the data returned in the notification
    """
    print("Received data: %s" % hexlify(value))

def my_subscribe(device):
    # Subscribe to the wanted characteristic data
    print("Subscribing to the characteristic with UUID %s..." % MY_CHAR_UUID)
    device.subscribe(MY_CHAR_UUID, callback=handle_my_char_data)
    print("Subscribed to the characteristic successfully!\n")

def main():
    # Initialize the adapter according to the backend used
    adapter = None
    if BACKEND == "BLED112":
        adapter = pygatt.BGAPIBackend() # BLED112 backend for Windows
    elif BACKEND == "GATTTOOL":
        adapter = pygatt.GATTToolBackend() # GATTtool backend for Linux

    device = None

    try:
        # Connect to BLED112
        adapter.start()

        # Scan for available BLE devices
        print("Scanning devices for %s seconds..." % str(SCAN_TIMEOUT))
        device_li = adapter.scan(timeout=SCAN_TIMEOUT)
        i = 1
        for d in device_li:
            print("%s. %s -- %s" % (str(i), str(d["address"]), str(d["name"])))
            i += 1

        # Check list size
        if len(device_li) == 0:
            print("No device found!")
            return 0

        # Ask the user which device to connect to
        print("\nSelect which device to connect to (0 to exit):")
        device_ind = None
        while (device_ind == None):
            user_in = input()
            try:
                user_in = int(user_in)
                if (user_in == 0):
                    return
                if (user_in < 0 or user_in > len(device_li)):
                    raise
                device_ind = user_in - 1
            except:
                print("Invalid input")

        # Connect to the device
        print("\nConnecting to the selected device...")
        device = adapter.connect(address=device_li[device_ind]["address"])
        print("Connected successfully!\n")

        # Call the subscribe function as daemon
        sub_d = threading.Thread(target=my_subscribe, args=(device,), daemon=True)
        sub_d.start()

        # Block the function from exiting
        input()
    finally:
        if device != None:
            device.disconnect()
        adapter.stop()

if __name__ == "__main__":
    main()