#
# This file is part of usb-protocol.
#
""" Structures describing Human Interface Device Class descriptors. """

import unittest
from enum import IntEnum

from ..descriptor import \
    DescriptorField, DescriptorNumber, DescriptorFormat

class HidClassSpecificDescriptorTypes(IntEnum):
    CS_UNDEFINED     = 0x20
    CS_HID           = 0x21
    CS_REPORT        = 0x22
    CS_PHYSICAL      = 0x23


HIDDescriptor = DescriptorFormat(
    "bLength"             / DescriptorField("Descriptor Length"),
    "bDescriptorType"     / DescriptorNumber(HidClassSpecificDescriptorTypes.CS_HID),
    "bcdHID"              / DescriptorField("HID Protocol Version", default=1.11),
    "bCountryCode"        / DescriptorField("Hardware target country", default=0),
    "bNumDescriptors"     / DescriptorField("Number of HID class descriptors to follow", default=0),
)

# This is not reallyy a stand-alone descriptor, but it is part of the HIDDescriptor above.
# That descriptor can contain multiple ReportDescriptors. To support this, a seperate
# descriptor format is used.
HIDReportDescriptor = DescriptorFormat(
    "bDescriptorType"     / DescriptorField("HID Descriptor Type", default=HidClassSpecificDescriptorTypes.CS_REPORT),
    "wDescriptorLength"   / DescriptorField("HID Descriptor Length")
)
