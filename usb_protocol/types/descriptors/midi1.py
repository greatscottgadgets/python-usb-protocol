#
# This file is part of usb-protocol.
#
"""
    Descriptors for USB MIDI Class Devices

    [Midi10] refers to "Universal Serial Bus Device Class Definition for MIDI Devices", Release 1.0, November 1, 1999
"""

from enum import IntEnum

from .standard import StandardDescriptorNumbers


class MidiStreamingInterfaceDescriptorSubtypes(IntEnum):
    # As defined in [Midi10], A.1
    MS_DESCRIPTOR_UNDEFINED = 0x00
    MS_HEADER               = 0x01
    MIDI_IN_JACK            = 0x02
    MIDI_OUT_JACK           = 0x03
    ELEMENT                 = 0x04


class MidiStreamingEndpointDescriptorSubtypes(IntEnum):
    # As defined in [Midi10], A.2
    DESCRIPTOR_UNDEFINED = 0x00
    MS_GENERAL           = 0x01


class MidiStreamingJackTypes(IntEnum):
    # As defined in [Midi10], A.3
    JACK_TYPE_UNDEFINED = 0x00
    EMBEDDED            = 0x01
    EXTERNAL            = 0x02


# As defined in [Midi10], Table 6-1
StandardMidiStreamingInterfaceDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(9, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(DescriptorTypes.INTERFACE),
    "bInterfaceNumber"    / DescriptorField(description="ID of the streaming interface"),
    "bAlternateSetting"   / DescriptorField(description="alternate setting number for the interface", default=0),
    "bNumEndpoints"       / DescriptorField(description="Number of data endpoints used (excluding endpoint 0). Can be: 0 (no data endpoint); 1 (data endpoint); 2 (data + explicit feedback endpoint)", default=0),
    "bInterfaceClass"     / DescriptorNumber(AudioInterfaceClassCode.AUDIO),
    "bInterfaceSubClass"  / DescriptorNumber(AudioInterfaceSubclassCodes.MIDI_STREAMING),
    "bInterfaceProtocol"  / DescriptorNumber(0),
    "iInterface"          / DescriptorField(description="index of a string descriptor describing this interface (0 = unused)", default=0)
)

# As defined in [Midi10], Table 6-2
ClassSpecificMidiStreamingInterfaceHeaderDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(7, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificDescriptorTypes.CS_INTERFACE),
    "bDescriptorSubtype"  / DescriptorNumber(AudioClassSpecificACInterfaceDescriptorSubtypes.HEADER),
    "bcdADC"              / DescriptorField(description="Midi Streaming Class specification release version", default=1.0),
    "wTotalLength"        / DescriptorField(description="Total number of bytes of the class-specific MIDIStreaming interface descriptor. Includes the combined length of this descriptor header and all Jack and Element descriptors."),
)

# As defined in [Midi10], Table 6-3
MidiInJackDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(6, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificDescriptorTypes.CS_INTERFACE),
    "bDescriptorSubtype"  / DescriptorNumber(MidiStreamingInterfaceDescriptorSubtypes.MIDI_IN_JACK),
    "bJackType"           / DescriptorField(description="see MidiStreamingJackTypes"),
    "bJackID"             / DescriptorField(description="Constant uniquely identifying the MIDI IN Jack within the USB-MIDI function"),
    "iJack"               / DescriptorField(description="index of a string descriptor describing this jack (0 = unused)", default=0)
)

# As defined in [Midi10], Table 6-4
MidiOutJackDescriptorHead = DescriptorFormat(
    "bLength"             / DescriptorField(description="Size of this descriptor, in bytes: 6+2*p"),
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificDescriptorTypes.CS_INTERFACE),
    "bDescriptorSubtype"  / DescriptorNumber(MidiStreamingInterfaceDescriptorSubtypes.MIDI_OUT_JACK),
    "bJackType"           / DescriptorField(description="see MidiStreamingJackTypes"),
    "bJackID"             / DescriptorField(description="Constant uniquely identifying the MIDI IN Jack within the USB-MIDI function"),
    "bNrInputPins"        / DescriptorField(description="Number of Input Pins of this MIDI OUT Jack: p", default=1)
)

MidiOutJackDescriptorElement = DescriptorFormat(
    "baSourceID"          / construct.Int8ul, # ID of the Entity to which the first Input Pin of this MIDI OUT Jack is connected
    "BaSourcePin"         / construct.Int8ul, #Output Pin number of the Entity to which the first Input Pin of this MIDI OUT Jack is connected
)

MidiOutJackDescriptorFoot = DescriptorFormat(
    "iJack"               / DescriptorField(description="index of a string descriptor describing this jack (0 = unused)", default=0)
)

# As defined in [Midi10], Table 6-6
StandardMidiStreamingBulkDataEndpointDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(9, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(DescriptorTypes.ENDPOINT),
    "bEndpointAddress"    / DescriptorField(description="The address of the endpoint, use USBDirection.*.from_endpoint_address()"),
    "bmAttributes"        / DescriptorField(description="D1..0: transfer type (10=bulk), D3..2: synchronization type (00=no sync);", default=USBTransferType.BULK | USBSynchronizationType.NONE | USBUsageType.DATA),
    "wMaxPacketSize"      / DescriptorField(description="Maximum packet size this endpoint is capable of", default=512),
    "bInterval"           / DescriptorField(description="Interval for polling endpoint for data transfers expressed in milliseconds. This field is ignored for bulk endpoints. Must be set to 0", default=0),
    "bRefresh"            / DescriptorField(description="must be set to 0", default=0),
    "bSynchAddress"       / DescriptorField(description="The address of the endpoint used to communicate synchronization information if required by this endpoint. Must be set to 0", default=0)
)

# As defined in [Midi10], Table 6-7
ClassSpecificMidiStreamingBulkDataEndpointDescriptorHead = DescriptorFormat(
    "bLength"             / DescriptorField(description="Size of this descriptor, in bytes: 4+n"),
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificDescriptorTypes.CS_ENDPOINT),
    "bDescriptorSubtype"  / DescriptorField(description="see MidiStreamingEndpointDescriptorSubtypes", default=MidiStreamingEndpointDescriptorSubtypes.MS_GENERAL),
    "bNumEmbMIDIJack"     / DescriptorField(description="Number of Embedded MIDI Jacks: n", default=1)
)

ClassSpecificMidiStreamingBulkDataEndpointDescriptorElement = DescriptorFormat(
    "baAssocJackID"       / construct.Int8ul # ID of the embedded eack that is associated with this endpoint
)
