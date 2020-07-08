#
# This file is part of usb-protocol.
#
""" Structures describing Communications Device Class descriptors. """

import unittest
from enum import IntEnum

import construct
from   construct  import this, Default

from .. import LanguageIDs
from ..descriptor import \
    DescriptorField, DescriptorNumber, DescriptorFormat, \
    BCDFieldAdapter, DescriptorLength


class CDCDescriptorNumbers(IntEnum):
    CS_INTERFACE  = 0x24
    CS_ENDPOINT   = 0x25


class CDCDescriptorSubtypes(IntEnum):
    """ Numbers of the Communications Class descriptor subtypes. """

    HEADER                                    = 0x00
    CALL_MANAGEMENT_FUNCTIONAL                = 0x01
    ABSTRACT_CONTROL_MANAGEMENT_FUNCTIONAL    = 0x02
    DIRECT_LINE_MANAGEMENT_FUNCTIONAL         = 0x03
    TELEPHONE_RINGER_FUNCTIONAL               = 0x04
    TELEPHONE_CALL_AND_LINE_STATE_FUNCTIONAL  = 0x05
    UNION_FUNCTIONAL_DESCRIPTOR               = 0x06
    COUNTRY_SELECTION_FUNCTIONAL              = 0x07
    TELEPHONE_OPERATIONAL_MODES_FUNCTIONAL    = 0x08
    USB_TERMINAL_FUNCTIONAL                   = 0x09
    NETWORK_CHANNEL_TERMINAL                  = 0x0a
    PROTOCOL_UNIT_FUNCTIONAL                  = 0x0b
    EXTENSION_UNIT_FUNCTIONAL                 = 0x0c
    MULTI_CHANNEL_MANAGEMENT_FUNCTIONAL       = 0x0d
    CAPI_CONTROL_MANAGEMENT_FUNCTIONAL        = 0x0e
    ETHERNET_NETWORKING_FUNCTIONAL            = 0x0f
    ATM_NETWORKING_FUNCTIONAL                 = 0x10
    WIRELESS_HANDSET_CONTROL_MODEL_FUNCTIONAL = 0x11
    MOBILE_DIRECT_LINE_MODEL_FUNCTIONAL       = 0x12
    MDLM_DETAIL_FUNCTIONAL                    = 0x13
    DEVICE_MANAGEMENT_MODEL_FUNCTIONAL        = 0x14
    OBEX_FUNCTIONAL                           = 0x15
    COMMAND_SET_FUCNTIONAL                    = 0x16
    COMMAND_SET_DETAIL_FUNCTIONAL             = 0x17
    TELEPHONE_CONTROL_MODEL_FUNCTIONAL        = 0x18
    OBEX_SERVICE_IDENTIFIER_FUNCTIONAL        = 0x19
    NCM_FUNCTIONAL                            = 0x1A


HeaderDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(5, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(CDCDescriptorNumbers.CS_INTERFACE),
    "bDescriptorSubtype"  / DescriptorNumber(CDCDescriptorSubtypes.HEADER),
    "bcdCDC"              / DescriptorField(description="CDC Version", default=1.1)
)

ACMFunctionalDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(4, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(CDCDescriptorNumbers.CS_INTERFACE),
    "bDescriptorSubtype"  / DescriptorNumber(CDCDescriptorSubtypes.ABSTRACT_CONTROL_MANAGEMENT_FUNCTIONAL),
    "bmCapabilities"      / DescriptorField(description="ACM Capabilities", default=0b0010)
)

UnionFunctionalDescriptor = DescriptorFormat(
    "bLength"                / construct.Const(5, construct.Int8ul),
    "bDescriptorType"        / DescriptorNumber(CDCDescriptorNumbers.CS_INTERFACE),
    "bDescriptorSubtype"     / DescriptorNumber(CDCDescriptorSubtypes.UNION_FUNCTIONAL_DESCRIPTOR),
    "bControlInterface"      / DescriptorField(description="Control Interface Number"),
    "bSubordinateInterface0" / DescriptorField(description="Subordinate Interface Number")
)

CallManagementFunctionalDescriptor = DescriptorFormat(
    "bLength"                / construct.Const(5, construct.Int8ul),
    "bDescriptorType"        / DescriptorNumber(CDCDescriptorNumbers.CS_INTERFACE),
    "bDescriptorSubtype"     / DescriptorNumber(CDCDescriptorSubtypes.CALL_MANAGEMENT_FUNCTIONAL),
    "bmCapabilities"         / DescriptorField(description="Call Management capabilities", default=0),
    "bDataInterface"         / DescriptorField(description="Data Interface Number")
)
