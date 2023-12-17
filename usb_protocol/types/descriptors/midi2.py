#
# This file is part of usb-protocol.
#
"""
    Descriptors for USB MIDI Class Devices

    [Midi20] refers to "Universal Serial Bus Device Class Definition for MIDI Devices", Release 2.0, May 5, 2020
"""

from enum import IntEnum

from .standard import StandardDescriptorNumbers


class MidiStreamingInterfaceDescriptorTypes(IntEnum):
    # As defined in [Midi20], A.1
    CS_UNDEFINED     = 0x20
    CS_DEVICE        = 0x21
    CS_CONFIGURATION = 0x22
    CS_STRING        = 0x23
    CS_INTERFACE     = 0x24
    CS_ENDPOINT      = 0x25
    CS_GR_TRM_BLOCK  = 0x26


class MidiStreamingInterfaceDescriptorSubtypes(IntEnum):
    # As defined in [Midi20], A.1
    MS_DESCRIPTOR_UNDEFINED = 0x00
    MS_HEADER               = 0x01
    MIDI_IN_JACK            = 0x02
    MIDI_OUT_JACK           = 0x03
    ELEMENT                 = 0x04


class MidiStreamingEndpointDescriptorSubtypes(IntEnum):
    # As defined in [Midi20], A.2
    DESCRIPTOR_UNDEFINED = 0x00
    MS_GENERAL           = 0x01
    MS_GENERAL_2_0       = 0x02


class MidiStreamingInterfaceHeaderClassRevision(IntEnum):
    # As defined in [Midi20], A.4
    MS_MIDI_1_0 = 0x0100
    MS_MIDI_2_0 = 0x0200


class MidiStreamingJackTypes(IntEnum):
    # As defined in [Midi20], A.5
    JACK_TYPE_UNDEFINED = 0x00
    EMBEDDED            = 0x01
    EXTERNAL            = 0x02


# As defined in [Midi20], Table B-5
StandardMidiStreamingInterfaceDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(9, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(DescriptorTypes.INTERFACE),
    "bInterfaceNumber"    / DescriptorField(description="ID of the streaming interface"),
    "bAlternateSetting"   / DescriptorField(description="alternate setting number for the interface", default=0),
    "bNumEndpoints"       / DescriptorField(description="Number of data endpoints used (excluding endpoint 0). Can be: 0 (no data endpoint); 1 (data endpoint); 2 (data + explicit feedback endpoint)", default=0),
    "bInterfaceClass"     / DescriptorNumber(AudioInterfaceClassCodes.AUDIO),
    "bInterfaceSubClass"  / DescriptorNumber(AudioInterfaceSubclassCodes.MIDI_STREAMING),
    "bInterfaceProtocol"  / DescriptorNumber(0),
    "iInterface"          / DescriptorField(description="index of a string descriptor describing this interface (0 = unused)", default=0)
)

# As defined in [Midi20], Table B-6
ClassSpecificMidiStreamingInterfaceHeaderDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(7, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificDescriptorTypes.CS_INTERFACE),
    "bDescriptorSubtype"  / DescriptorNumber(AudioClassSpecificACInterfaceDescriptorSubtypes.HEADER),
    "bcdADC"              / DescriptorField(description="Midi Streaming Class specification release version", default=1.0),
    "wTotalLength"        / DescriptorField(description="Total number of bytes of the class-specific MIDIStreaming interface descriptor. Includes the combined length of this descriptor header and all Jack and Element descriptors."),
)

# As defined in [Midi20], Table 5-3
StandardMidiStreamingDataEndpointDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(7, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificDescriptorTypes.CS_ENDPOINT),
    "bEndpointAddress"    / DescriptorField(description="endpoint address, use USBDirection.*.from_endpoint_address()"),
    "bmAttributes"        / DescriptorField(description="endpoint type, see USBTransferType (only NONE, BULK or INTERRUPT allowed)", default=USBTransferType.BULK),
    "wMaxPacketSize"      / DescriptorField(description="Maximum packet size this endpoint is capable of sending or receiving"),
    "bInterval"           / DescriptorField(description="Interval for polling endpoint for Interrupt data transfers. For bulk endpoints this field is ignored and must be reset to 0", default=0)
)



