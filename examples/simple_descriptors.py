#!/usr/bin/env python3
#
# This file is part of usb-protocol.
#
""" Examples for using the simple descriptor data structures. """

from usb_protocol.types.descriptors    import StringDescriptor
from usb_protocol.emitters.descriptors import DeviceDescriptorEmitter

string_descriptor = bytes([
        40, # Length
        3,  # Type
        ord('G'), 0x00,
        ord('r'), 0x00,
        ord('e'), 0x00,
        ord('a'), 0x00,
        ord('t'), 0x00,
        ord(' '), 0x00,
        ord('S'), 0x00,
        ord('c'), 0x00,
        ord('o'), 0x00,
        ord('t'), 0x00,
        ord('t'), 0x00,
        ord(' '), 0x00,
        ord('G'), 0x00,
        ord('a'), 0x00,
        ord('d'), 0x00,
        ord('g'), 0x00,
        ord('e'), 0x00,
        ord('t'), 0x00,
        ord('s'), 0x00,
    ])

# Use our simple StringDescriptor object to parse a binary blob string descriptor.
print(f"Parsing: {string_descriptor}")
parsed = StringDescriptor.parse(string_descriptor)
print(parsed)

# Create a simple Device Descriptor via an emitter object.
# Our object has sane defaults, so we can skip some fields if we want.
builder = DeviceDescriptorEmitter()
builder.idVendor  = 0x1234
builder.idProduct = 0xabcd
builder.bNumConfigurations = 3
print(f"Generated device descriptor: {builder.emit()}")
