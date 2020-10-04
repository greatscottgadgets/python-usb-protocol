#
# This file is part of usb-protocol.
#
""" SuperSpeed USB types -- defines enumerations that describe standard USB3 types. """

from enum import IntEnum

class LinkCommand(IntEnum):
    """ Constant values (including both class and type) for link commands. """

    LGOOD = 0   # Header Packet ACK
    LCRD  = 1   # Header Credit
    LRTY  = 2   # Header Packet Retry Sequence
    LBAD  = 3   # Header Packet NAK
    LGO_U = 4   # Request Switching to Power State Ux
    LAU   = 5   # Power State Acceptance
    LXU   = 6   # Power State Rejection
    LPMA  = 7   # Power State Acknowledgement
    LUP   = 8   # Downstream-facing Keep-alive
    LDN   = 11  # Upstream-facing Keep-alive

    def get_class(self):
        return int(self) >> 2

    def get_type(self):
        return int(self) & 0b11


class HeaderPacketType(IntEnum):
    """ Constants representing the Header Packet archetypes. """
    TRANSACTION           = 0b00100
    DATA                  = 0b01000
    ISOCHRONOUS_TIMESTAMP = 0b01100
    LINK_MANAGEMENT       = 0b00000


class TransactionPacketSubtype(IntEnum):
    """ Constants representing the subtypes of Transition Header Packet. """

    ACK           = 1
    NRDY          = 2
    ERDY          = 3
    STATUS        = 4
    STALL         = 5
    NOTIFICATION  = 6
    PING          = 7
    PING_RESPONSE = 8


class LinkManagementPacketSubtype(IntEnum):
    """ Constants represneting the various types of Link Management Packet. """

    SET_LINK_FUNCTION           = 1
    U2_INACTIVITY_TIMEOUT       = 2
    VENDOR_DEVICE_TEST          = 3
    PORT_CAPABILITY             = 4
    PORT_CONFIGURATION          = 5
    PORT_CONFIGURATION_RESPONSE = 6
    PRECISION_TIME_MANAGEMENT   = 7
