#
# This file is part of usb-protocol.
#
""" Structures describing standard USB descriptors. """

import unittest

import construct
from   construct  import this

from ..descriptor import DescriptorField, DescriptorNumber, DescriptorFormat

DeviceDescriptor = DescriptorFormat(
    "bLength"             / DescriptorField("Length"),
    "bDescriptorType"     / DescriptorNumber(1),
    "bcdUSB"              / DescriptorField("USB Version"),
    "bDeviceClass"        / DescriptorField("Class"),
    "bDeviceSubclass"     / DescriptorField("Subclass"),
    "bDeviceProtocol"     / DescriptorField("Protocol"),
    "bMaxPacketSize0"     / DescriptorField("EP0 Max Pkt Size"),
    "idVendor"            / DescriptorField("Vendor ID"),
    "idProduct"           / DescriptorField("Product ID"),
    "bcdDevice"           / DescriptorField("Device Version"),
    "iManufacturer"       / DescriptorField("Manufacturer Str"),
    "iProduct"            / DescriptorField("Product Str"),
    "iSerialNumber"       / DescriptorField("Serial Number"),
    "bNumConfigurations"  / DescriptorField("Configuration Count"),
)


ConfigurationDescriptor = DescriptorFormat(
    "bLength"             / DescriptorField("Length"),
    "bDescriptorType"     / DescriptorNumber(2),
    "wTotalLength"        / DescriptorField("Length including subordinates"),
    "bNumInterfaces"      / DescriptorField("Interface count"),
    "bConfigurationValue" / DescriptorField("Configuration number"),
    "iConfiguration"      / DescriptorField("Description string"),
    "bmAttributes"        / DescriptorField("Attributes"),
    "bMaxPower"           / DescriptorField("Max power consumption"),
)


StringDescriptor = DescriptorFormat(
    "bLength"             / DescriptorField("Length"),
    "bDescriptorType"     / DescriptorNumber(3),
    "bString"             / construct.PaddedString(this.bLength - 2, "utf_16_le")
)


InterfaceDescriptor = DescriptorFormat(
    "bLength"             / DescriptorField("Length"),
    "bDescriptorType"     / DescriptorNumber(4),
    "bInterfaceNumber"    / DescriptorField("Interface number"),
    "bAlternateSetting"   / DescriptorField("Alternate setting"),
    "bNumEndpoints"       / DescriptorField("Endpoints included"),
    "bInterfaceClass"     / DescriptorField("Class"),
    "bInterfaceSubclass"  / DescriptorField("Subclass"),
    "bInterfaceProtocol"  / DescriptorField("Protocol"),
    "iInterface"          / DescriptorField("String index"),
)


EndpointDescriptor = DescriptorFormat(
    "bLength"             / DescriptorField("Length"),
    "bDescriptorType"     / DescriptorNumber(5),
    "bEndpointAddress"    / DescriptorField("Endpoint Address"),
    "bmAttributes"        / DescriptorField("Attributes"),
    "wMaxPacketSize"      / DescriptorField("Maximum Packet Size"),
    "bInterval"           / DescriptorField("Polling interval"),
)


DeviceQualifierDescriptor = DescriptorFormat(
    "bLength"             / DescriptorField("Length"),
    "bDescriptorType"     / DescriptorNumber(6),
    "bcdUSB"              / DescriptorField("USB Version"),
    "bDeviceClass"        / DescriptorField("Class"),
    "bDeviceSubclass"     / DescriptorField("Subclass"),
    "bDeviceProtocol"     / DescriptorField("Protocol"),
    "bMaxPacketSize0"     / DescriptorField("EP0 Max Pkt Size"),
    "bNumConfigurations"  / DescriptorField("Configuration Count"),
    "_bReserved"          / construct.Optional(construct.Const(b"\0"))
)


class DescriptorParserCases(unittest.TestCase):

    def test_string_descriptor(self):

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

        # Parse the relevant string...
        parsed = StringDescriptor.parse(string_descriptor)

        # ... and check the desriptor's fields.
        self.assertEqual(parsed.bLength,                    40)
        self.assertEqual(parsed.bDescriptorType,             3)
        self.assertEqual(parsed.bString, "Great Scott Gadgets")


    def test_device_descriptor(self):

        device_descriptor = [
            0x12,         # Length
            0x01,         # Type
            0x00, 0x02,   # USB version
            0xFF,         # class
            0xFF,         # subclass
            0xFF,         # protocol
            64,           # ep0 max packet size
            0xd0, 0x16,   # VID
            0x3b, 0x0f,   # PID
            0x00, 0x00,   # device rev
            0x01,         # manufacturer string
            0x02,         # product string
            0x03,         # serial number
            0x01          # number of configurations
        ]

        # Parse the relevant string...
        parsed = DeviceDescriptor.parse(device_descriptor)

        # ... and check the desriptor's fields.
        self.assertEqual(parsed.bLength,             18)
        self.assertEqual(parsed.bDescriptorType,      1)
        self.assertEqual(parsed.bcdUSB,          0x0200)
        self.assertEqual(parsed.bDeviceClass,      0xFF)
        self.assertEqual(parsed.bDeviceSubclass,   0xFF)
        self.assertEqual(parsed.bDeviceProtocol,   0xFF)
        self.assertEqual(parsed.bMaxPacketSize0,     64)
        self.assertEqual(parsed.idVendor,        0x16d0)
        self.assertEqual(parsed.idProduct,       0x0f3b)
        self.assertEqual(parsed.bcdDevice,       0x0000)
        self.assertEqual(parsed.iManufacturer,        1)
        self.assertEqual(parsed.iProduct,             2)
        self.assertEqual(parsed.iSerialNumber,        3)
        self.assertEqual(parsed.bNumConfigurations,   1)


if __name__ == "__main__":
    unittest.main()
