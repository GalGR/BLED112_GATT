#!/usr/bin/python3

import asyncio
from bleak import discover
from bleak import BleakClient

MODEL_NBR_UUID = "00002a24-0000-1000-8000-00805f9b34fb"
DESCRIPTOR_HND = 0x2a
DESCRIPTOR_HND_STR = hex(DESCRIPTOR_HND)

DEVICE_NAME = "Gal_C-TAG________"

async def my_discover():
    devices = await discover()
    li_devices = []
    for d in devices:
        li_devices.append(d)
        print(d)
    return li_devices

async def my_connect_get_model_number(address, loop):
    model_number = None
    model_number_str = "N/A"
    async with BleakClient(address, loop=loop) as client:
        model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        model_number_str = "".join(map(chr, model_number))
        print("Model Number: {0}".format(model_number_str))
    return model_number_str

async def my_get_descriptor(address, loop):
    descriptor_val = None
    async with BleakClient(address, loop=loop) as client:
        descriptor_val = await client.read_gatt_descriptor(DESCRIPTOR_HND)
        descriptor_val_str = str(descriptor_val)
        print("Descriptor {0}: {1}".format(DESCRIPTOR_HND_STR, descriptor_val_str))
    return descriptor_val

def main():
    loop = asyncio.get_event_loop()
    li_devices = loop.run_until_complete(my_discover())
    device_address = None
    device_name = None
    for d in li_devices:
        if d.name == DEVICE_NAME:
            device_address = d.address
            device_name = d.name
    model_number_str = loop.run_until_complete(my_connect_get_model_number(device_address, loop=loop))
    descriptor_val = loop.run_until_complete(my_get_descriptor(device_address, loop=loop))

if __name__ == "__main__":
    main()