#
# This file is part of usb-protocol.
#
""" Structures describing Communications Device Class descriptors. """

import unittest
from enum import IntEnum, unique

import construct
from   construct  import this, Default

from .. import LanguageIDs
from ..descriptor import \
    DescriptorField, DescriptorNumber, DescriptorFormat, \
    BCDFieldAdapter, DescriptorLength

@unique
class HIDPrefix(IntEnum):
    # Main items
    INPUT          = 0b1000_00
    OUTPUT         = 0b1001_00
    FEATURE        = 0b1011_00
    COLLECTION     = 0b1010_00
    END_COLLECTION = 0b1100_00
    # Global items
    USAGE_PAGE     = 0b0000_01
    LOGICAL_MIN    = 0b0001_01
    LOGICAL_MAX    = 0b0010_01
    PHYSICAL_MIN   = 0b0011_01
    PHYSICAL_MAX   = 0b0100_01
    UNIT_EXPONENT  = 0b0101_01
    UNIT           = 0b0110_01
    REPORT_SIZE    = 0b0111_01
    REPORT_ID      = 0b1000_01
    REPORT_COUNT   = 0b1001_01
    PUSH           = 0b1010_01
    POP            = 0b1011_01
    # Local Items
    USAGE          = 0b0000_10
    USAGE_MIN      = 0b0001_10
    USAGE_MAX      = 0b0010_10
    DESIGNATOR_IDX = 0b0011_10
    DESIGNATOR_MIN = 0b0100_10
    DESIGNATOR_MAX = 0b0101_10
    STRING_IDX     = 0b0111_10
    STRING_MIN     = 0b1000_10
    STRING_MAX     = 0b1001_10
    DELIMITER      = 0b1010_10

HIDDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(0x09, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(33),
    "bcdHID"              / DescriptorField("HID Protocol Version", default=1.11),
    "bCountryCode"        / DescriptorField("HID Device Language", default=0),
    "bNumDescriptors"     / DescriptorField("Number of HID Descriptors", default=1),
    "bDescriptorType"     / DescriptorField("HID Descriptor Type", default=34),
    "wDescriptorLength"   / DescriptorField("HID Descriptor Length")
    # bDescriptorType and wDescriptorLength repeat bNumDescriptors times
)

_hid_item_length = [ 0, 1, 2, 4 ]
ReportDescriptor = DescriptorFormat(
    "bHeader" / construct.BitStruct(
        # prefix technically consists of a 4 byte tag and a 2 byte type,
        # however, they're all listed together in the HID spec
        "prefix"  / construct.Enum(construct.BitsInteger(6), HIDPrefix),
        "bSize"   / construct.BitsInteger(2),
    ),
    "data"    / construct.Byte[lambda ctx: _hid_item_length[ctx.bHeader.bSize]]
)

# Flags for INPUT/OUTPUT/FEATURE items. Named under one of the following conventions:
# valA_valB: valA when 0, valB when 1
# flag:      Flag disabled when 0, flag enabled when 1
# nFlag:     Flag enabled when 0, flag disabled when 1
ItemFlags = construct.BitStruct(
    "volatile"          / construct.Flag,
    "null"              / construct.Flag,
    "nPreferred"        / construct.Flag,
    "linear"            / construct.Flag,
    "wrap"              / construct.Flag,
    "absolute_relative" / construct.Flag,
    "array_variable"    / construct.Flag,
    "data_constant"     / construct.Flag,
)