#!/usr/bin/env python3
#
# This file is part of usb-protocol.
#
""" Example that builds a device-worth of descriptors using a collection object. """

from usb_protocol.emitters.descriptors import DeviceDescriptorCollection

collection = DeviceDescriptorCollection()

# Create our device descriptor, and populate it with some fields.
# Many fields have sane/common defaults; and thus can be omitted.
with collection.DeviceDescriptor() as d:
    d.idVendor           = 0xc001
    d.idProduct          = 0xc0de
    d.bNumConfigurations = 1

    d.iManufacturer      = "usb-tools"
    d.iProduct           = "Illegitimate USB Device"
    d.iSerialNumber      = "123456"


# Create our configuration descriptor, and its subordinates.
with collection.ConfigurationDescriptor() as c:
    # Here, this is our first configuration, and is automatically assigned number '1'.

    # We'll create a simple interface with a couple of endpoints.
    with c.InterfaceDescriptor() as i:
        i.bInterfaceNumber = 0

        # Our endpoints default to bulk; with mostly-sane defaults.
        with i.EndpointDescriptor() as e:
            e.bEndpointAddress = 0x01
            e.wMaxPacketSize   = 512

        with i.EndpointDescriptor() as e:
            e.bEndpointAddress = 0x81
            e.wMaxPacketSize   = 512


print("This device's descriptors would look like:")

# Iterate over all of our descriptors.
for value, index, raw in collection:
    print(f"    type {value} (index {index}) = {raw}")
