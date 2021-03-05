#
# This file is part of usb-protocol.
#
""" descriptors specific to USB version 2
    NOTE: This is not complete yet and will be extended as needed
"""

from usb_protocol.emitters import descriptor
from enum                  import IntEnum

import construct

from ..descriptor import \
    DescriptorField, DescriptorNumber, DescriptorFormat

from .uac import *

class ClockAttributes(IntEnum):
    EXTERNAL_CLOCK              = 0b00
    INTERNAL_FIXED_CLOCK        = 0b01
    INTERNAL_VARIABLE_CLOCK     = 0b10
    INTERNAL_PROGRAMMABLE_CLOCK = 0b11

class ClockFrequencyControl(IntEnum):
    NOT_PRESENT       = 0b00
    HOST_READ_ONLY    = 0b01
    HOST_PROGRAMMABLE = 0b11

class CopyProtectControl(IntEnum):
    NOT_PRESENT       = 0b00
    HOST_READ_ONLY    = 0b10
    HOST_PROGRAMMABLE = 0b11

class ConnectorControl(IntEnum):
    NOT_PRESENT       = (0b00) << 2
    HOST_READ_ONLY    = (0b10) << 2
    HOST_PROGRAMMABLE = (0b11) << 2

class OverloadControl(IntEnum):
    NOT_PRESENT       = (0b00) << 4
    HOST_READ_ONLY    = (0b10) << 4
    HOST_PROGRAMMABLE = (0b11) << 4

class ClusterControl(IntEnum):
    NOT_PRESENT       = (0b00) << 6
    HOST_READ_ONLY    = (0b10) << 6
    HOST_PROGRAMMABLE = (0b11) << 6

class UnderflowControl(IntEnum):
    NOT_PRESENT       = (0b00) << 8
    HOST_READ_ONLY    = (0b10) << 8
    HOST_PROGRAMMABLE = (0b11) << 8

class OverflowControl(IntEnum):
    NOT_PRESENT       = (0b00) << 10
    HOST_READ_ONLY    = (0b10) << 10
    HOST_PROGRAMMABLE = (0b11) << 10


class FormatTypes(IntEnum):
    FORMAT_TYPE_UNDEFINED = 0x00
    FORMAT_TYPE_I         = 0x01
    FORMAT_TYPE_II        = 0x02
    FORMAT_TYPE_III       = 0x03
    FORMAT_TYPE_IV        = 0x04
    EXT_FORMAT_TYPE_I     = 0x81
    EXT_FORMAT_TYPE_II    = 0x82
    EXT_FORMAT_TYPE_III   = 0x83

class TypeIFormats(IntEnum):
    PCM             = (1 << 0)
    PCM8            = (1 << 1)
    IEEE_FLOAT      = (1 << 2)
    ALAW            = (1 << 3)
    MULAW           = (1 << 4)
    TYPE_I_RAW_DATA = (1 << 31)

class TypeIIFormats(IntEnum):
    MPEG             = (1 << 0)
    AC_3             = (1 << 1)
    WMA              = (1 << 2)
    DTS              = (1 << 3)
    TYPE_II_RAW_DATA = (1 << 31)

class TypeIIIFormats(IntEnum):
    IEC61937_AC_3               = (1 << 0)
    IEC61937_MPEG_1_Layer1      = (1 << 1)
    IEC61937_MPEG_1_Layer2_3    = (1 << 2) # same bit!
    IEC61937_MPEG_2_NOEXT       = (1 << 2) # same bit!
    IEC61937_MPEG_2_EXT         = (1 << 3)
    IEC61937_MPEG_2_AAC_ADTS    = (1 << 4)
    IEC61937_MPEG_2_Layer1_LS   = (1 << 5)
    IEC61937_MPEG_2_Layer2_3_LS = (1 << 6)
    IEC61937_DTS_I              = (1 << 7)
    IEC61937_DTS_II             = (1 << 8)
    IEC61937_DTS_III            = (1 << 9)
    IEC61937_ATRAC              = (1 << 10)
    IEC61937_ATRAC2_3           = (1 << 11)
    TYPE_III_WMA                = (1 << 12)

class TypeIVFormats(IntEnum):
    PCM                           = (1 << 0)
    PCM8                          = (1 << 1)
    IEEE_FLOAT                    = (1 << 2)
    ALAW                          = (1 << 3)
    MULAW                         = (1 << 4)
    MPEG                          = (1 << 5)
    AC_3                          = (1 << 6)
    WMA                           = (1 << 7)
    IEC61937_AC_3                 = (1 << 8)
    IEC61937_MPEG_1_Layer1        = (1 << 9)
    IEC61937_MPEG_1_Layer2_3      = (1 << 10) # same bit!
    IEC61937_MPEG_2_NOEXT         = (1 << 10) # same bit!
    IEC61937_MPEG_2_EXT           = (1 << 11)
    IEC61937_MPEG_2_AAC_ADTS      = (1 << 12)
    IEC61937_MPEG_2_Layer1_LS     = (1 << 13)
    IEC61937_MPEG_2_Layer2_3_LS   = (1 << 14)
    IEC61937_DTS_I                = (1 << 15)
    IEC61937_DTS_II               = (1 << 16)
    IEC61937_DTS_III              = (1 << 17)
    IEC61937_ATRAC                = (1 << 18)
    IEC61937_ATRAC2_3             = (1 << 19)
    TYPE_III_WMA                  = (1 << 20)
    IEC60958_PCM                  = (1 << 21)

class SidebandProtocols(IntEnum):
    PROTOCOL_UNDEFINED      = 0x00
    PRES_TIMESTAMP_PROTOCOL = 0x02

class AudioClassSpecificASInterfaceDescriptorSubtypes(IntEnum):
    AS_DESCRIPTOR_UNDEFINED = 0x00
    AS_GENERAL              = 0x01
    FORMAT_TYPE             = 0x02
    ENCODER                 = 0x03
    DECODER                 = 0x04

InterfaceAssociationDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(8, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(DescriptorTypes.INTERFACE_ASSOCIATION),
    "bFirstInterface"     / DescriptorField(description="Interface number of the first interface that is associated with this function.", default=0),
    "bInterfaceCount"     / DescriptorField(description="Number of contiguous interfaces that are associated with this function"),
    "bFunctionClass"      / DescriptorNumber(AudioFunctionClassCode.AUDIO_FUNCTION),
    "bFunctionSubClass"   / DescriptorField(description="function subclass code (currently not used in uac2)", default=AudioFunctionCategoryCodes.FUNCTION_SUBCLASS_UNDEFINED), 
    "bFunctionProtocol"   / DescriptorNumber(AudioFunctionProtocolCodes.AF_VERSION_02_00),
    "iFunction"           / DescriptorField(description="Index of a string descriptor that describes this interface", default=0),
)

StandardAudioControlInterfaceDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(9, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(DescriptorTypes.INTERFACE),
    "bAlternateSetting"   / DescriptorField(description="alternate setting for the interface (must be 0)", default=0),
    "bNumEndpoints"       / DescriptorField(description="number of endpoints used by this interface (excluding endpoint 0). This number is either 0 or 1 if the optional interrupt endpoint is present", default=0),
    "bInterfaceClass"     / DescriptorNumber(AudioInterfaceClassCode.AUDIO),
    "bInterfaceSubClass"  / DescriptorNumber(AudioInterfaceSubclassCodes.AUDIO_CONTROL),
    "bInterfaceProtocol"  / DescriptorNumber(AudioInterfaceProtocolCodes.IP_VERSION_02_00),
    "iInterface"          / DescriptorField(description="index of string descriptor describing this interface", default=0),
)

ClassSpecificAudioControlInterfaceDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(9, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificDescriptorTypes.CS_INTERFACE),
    "bDescriptorSubtype"  / DescriptorNumber(AudioClassSpecificACInterfaceDescriptorSubtypes.HEADER),
    "bcdADC"              / DescriptorField(description="Audio Device Class specification release version", default=2.0),
    "bCategory"           / DescriptorField(description="primary use of this audio function (see AudioFunctionCategoryCodes)", default=AudioFunctionCategoryCodes.IO_BOX),
    "wTotalLength"        / DescriptorField(description="total number of bytes for the class specific audio control interface descriptor; Includes the combined length of this descriptor header and all Clock Source, Unit and Terminal descriptors"),
    "bmControls"          / DescriptorField(description="D1..0: latency control", default=0),
)

ClockSourceDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(9, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificDescriptorTypes.CS_INTERFACE),
    "bDescriptorSubtype"  / DescriptorNumber(AudioClassSpecificACInterfaceDescriptorSubtypes.CLOCK_SOURCE),
    "bClockID"            / DescriptorField(description="ID of the clock source entity within the audio function (used in requests)"),
    "bmAttributes"        / DescriptorField(description="D1..0: clock type (see ClockAttributs)"),
    "bmControls"          / DescriptorField(description="D1..0: clock frequency control (D0..1: See ClockFrequencyControl, D3..2: clock validity control (0))", default=ClockFrequencyControl.NOT_PRESENT),
    "bAssocTerminal"      / DescriptorField(description="ID of the terminal which is associated with this clock", default=0),
    "iClockSource"        / DescriptorField(description="index of the string description of this clock source", default=0),
)

InputTerminalDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(17, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificDescriptorTypes.CS_INTERFACE),
    "bDescriptorSubtype"  / DescriptorNumber(AudioClassSpecificACInterfaceDescriptorSubtypes.INPUT_TERMINAL),
    "bTerminalID"         / DescriptorField(description="unique identifier for the terminal within the audio function (used in requests)"),
    "wTerminalType"       / DescriptorField(description="a value of one of the terminal types Enums (eg InputTerminaTypes, ExternalTerminalTypes)"),
    "bAssocTerminal"      / DescriptorField(description="ID of the associated output terminal", default=0),
    "bCSourceID"          / DescriptorField(description="ID of the clock which is connected to this terminal"),
    "bNrChannels"         / DescriptorField(description="number of logical output channels in the terminal’s output channel cluster"),
    "bmChannelConfig"     / DescriptorField(description="describes the spatial location of the logical channels", default=0),
    "bmControls"          / DescriptorField(description="OR combination of  ClockFrequencyControl, CopyProtectControl, ConnectorControl, ClusterControl, UnderflowControl and OverflowControl", default=0),
    "iChannelNames"       / DescriptorField(description="string descriptor index of the first logical channel name", default=0),
    "iTerminal"           / DescriptorField(description="ID of the input terminal string description", default=0)
)

OutputTerminalDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(12, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificDescriptorTypes.CS_INTERFACE),
    "bDescriptorSubtype"  / DescriptorNumber(AudioClassSpecificACInterfaceDescriptorSubtypes.OUTPUT_TERMINAL),
    "bTerminalID"         / DescriptorField(description="unique identifier for the terminal within the audio function."),
    "wTerminalType"       / DescriptorField(description="a value of one of the terminal types Enums (eg OutputTerminaTypes, ExternalTerminalTypes)"),
    "bAssocTerminal"      / DescriptorField(description="ID of the associated input terminal", default=0),
    "bSourceID"           / DescriptorField(description="ID of the unit or terminal which is connected to this terminal"),
    "bCSourceID"          / DescriptorField(description="ID of the clock which is connected to this terminal"),
    "bmControls"          / DescriptorField(description="OR combination of  ClockFrequencyControl, CopyProtectControl, ConnectorControl, UnderflowControl>>2 and OverflowControl>>2", default=0),
    "iTerminal"           / DescriptorField(description="ID of the input terminal string description", default=0)
)

AudioStreamingInterfaceDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(9, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(DescriptorTypes.INTERFACE),
    "bInterfaceNumber"    / DescriptorField(description="ID of the streaming interface"),
    "bAlternateSetting"   / DescriptorField(description="alternate setting number for the interface", default=0),
    "bNumEndpoints"       / DescriptorField(description="Number of data endpoints used (excluding endpoint 0). Can be: 0 (no data endpoint); 1 (data endpoint); 2 (data + explicit feedback endpoint)", default=0),
    "bInterfaceClass"     / DescriptorNumber(AudioInterfaceClassCode.AUDIO),
    "bInterfaceSubClass"  / DescriptorNumber(AudioInterfaceSubclassCodes.AUDIO_STREAMING),
    "bInterfaceProtocol"  / DescriptorNumber(AudioInterfaceProtocolCodes.IP_VERSION_02_00),
    "iInterface"          / DescriptorField(description="index of a string descriptor describing this interface (0 = unused)", default=0)
)

ClassSpecificAudioStreamingInterfaceDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(16, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificDescriptorTypes.CS_INTERFACE),
    "bDescriptorSubtype"  / DescriptorNumber(AudioClassSpecificASInterfaceDescriptorSubtypes.AS_GENERAL),
    "bTerminalLink"       / DescriptorField(description="the ID of the terminal to which this interface is connected"),
    "bmControls"          / DescriptorField(description="D1..0: active alternate setting control; D3..2: valid alternate settings control; D7..4: reserved, must be 0", default=0),
    "bFormatType"         / DescriptorField(description="see FormatTypes"),
    "bmFormats"           / DescriptorField(description="audio data formats which can be used with this interface", length=4),
    "bNrChannels"         / DescriptorField(description="Number of physical channels in the AS Interface audio channel cluster"),
    "bmChannelConfig"     / DescriptorField(description="spatial location of the physical channels", default=0),
    "iChannelNames"       / DescriptorField(description="ndex of a string descriptor, describing the name of the first physical channel.", default=0)
)

TypeIFormatTypeDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(6, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificDescriptorTypes.CS_INTERFACE),
    "bDescriptorSubtype"  / DescriptorNumber(AudioClassSpecificASInterfaceDescriptorSubtypes.FORMAT_TYPE),
    "bFormatType"         / DescriptorNumber(FormatTypes.FORMAT_TYPE_I),
    "bSubslotSize"        / DescriptorField(description="number of bytes occupied by one audio subslot (1, 2, 3 or 4)"),
    "bBitResolution"      / DescriptorField(description="number of effectively used bits out of the available bits in an audio subslot")
)

ExtendedTypeIFormatTypeDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(9, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificDescriptorTypes.CS_INTERFACE),
    "bDescriptorSubtype"  / DescriptorNumber(AudioClassSpecificASInterfaceDescriptorSubtypes.FORMAT_TYPE),
    "bFormatType"         / DescriptorNumber(FormatTypes.EXT_FORMAT_TYPE_I),
    "bSubslotSize"        / DescriptorField(description="number of bytes occupied by one audio subslot (1, 2, 3 or 4)"),
    "bBitResolution"      / DescriptorField(description="number of effectively used bits out of the available bits in an audio subslot"),
    "bHeaderLength"       / DescriptorField(description="size of the packet header in bytes"),
    "bControlSize"        / DescriptorField(description="size of the control channel words in bytes"),
    "bSideBandProtocol"   / DescriptorField(description="side band protocol, see SidebandProtocols", default=SidebandProtocols.PROTOCOL_UNDEFINED)
)

TypeIIFormatTypeDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(8, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificDescriptorTypes.CS_INTERFACE),
    "bDescriptorSubtype"  / DescriptorNumber(AudioClassSpecificASInterfaceDescriptorSubtypes.FORMAT_TYPE),
    "bFormatType"         / DescriptorNumber(FormatTypes.FORMAT_TYPE_II),
    "wMaxBitRate"         / DescriptorField(description="maximum bitrate of this interface in kbits/s"),
    "wSlotsPerFrame"      / DescriptorField(description="number of PCM audio slots in one audio frame")
)

ExtendedTypeIIFormatTypeDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(10, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificDescriptorTypes.CS_INTERFACE),
    "bDescriptorSubtype"  / DescriptorNumber(AudioClassSpecificASInterfaceDescriptorSubtypes.FORMAT_TYPE),
    "bFormatType"         / DescriptorNumber(FormatTypes.EXT_FORMAT_TYPE_II),
    "wMaxBitRate"         / DescriptorField(description="maximum bitrate of this interface in kbits/s"),
    "wSamplesPerFrame"    / DescriptorField(description="number of PCM audio samples in one audio frame"),
    "bHeaderLength"       / DescriptorField(description="size of the packet header in bytes"),
    "bSideBandProtocol"   / DescriptorField(description="side band protocol, see SidebandProtocols", default=SidebandProtocols.PROTOCOL_UNDEFINED)
)

TypeIIIFormatTypeDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(9, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificDescriptorTypes.CS_INTERFACE),
    "bDescriptorSubtype"  / DescriptorNumber(AudioClassSpecificASInterfaceDescriptorSubtypes.FORMAT_TYPE),
    "bFormatType"         / DescriptorNumber(FormatTypes.FORMAT_TYPE_III),
    "bSubslotSize"        / DescriptorField(description="number of bytes occupied by one audio subslot (must be 2)", default=2),
    "bBitResolution"      / DescriptorField(description="number of effectively used bits out of the available bits in an audio subslot"),
)

ExtendedTypeIIIFormatTypeDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(8, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificDescriptorTypes.CS_INTERFACE),
    "bDescriptorSubtype"  / DescriptorNumber(AudioClassSpecificASInterfaceDescriptorSubtypes.FORMAT_TYPE),
    "bFormatType"         / DescriptorNumber(FormatTypes.EXT_FORMAT_TYPE_III),
    "bSubslotSize"        / DescriptorField(description="number of bytes occupied by one audio subslot (must be 2)", default=2),
    "bBitResolution"      / DescriptorField(description="number of effectively used bits out of the available bits in an audio subslot"),
    "bHeaderLength"       / DescriptorField(description="size of the packet header in bytes"),
    "bSideBandProtocol"   / DescriptorField(description="side band protocol, see SidebandProtocols", default=SidebandProtocols.PROTOCOL_UNDEFINED)
)

ClassSpecificAudioStreamingIsochronousAudioDataEndpointDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(8, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificDescriptorTypes.CS_ENDPOINT),
    "bDescriptorSubtype"  / DescriptorNumber(AudioClassSpecificEndpointDescriptorSubtypes.EP_GENERAL),
    "bmAttributes"        / DescriptorField(description="bit D7 = 1: only packets with size wMaxPacketSize allowed", default=0),
    "bmControls"          / DescriptorField(description="D1..0: pitch control D3..2: data overrun control; D5..4: data underrun control;", default=0),
    "bLockDelayUnits"     / DescriptorField(description="wLockDelay unit: 0: undefined; 1: milliseconds; 2: decoded PCM samples;", default=0),
    "wLockDelay"          / DescriptorField(description="the time it takes this endpoint to reliably lock its internal clock recovery circuitry. Units see bLockDelayUnits", default=0)
)

###################### MIDI #########################

class MidiStreamingGroupTerminalBlockDescriptorSubtypes(IntEnum):
    GR_TRM_BLOCK_UNDEFINED = 0x00
    GR_TRM_BLOCK_HEADER    = 0x01
    GR_TRM_BLOCK           = 0x02

class GroupTerminalBlockType(IntEnum):
    BIDIRECTIONAL = 0x00
    INPUT_ONLY    = 0x01
    OUTPUT_ONLY   = 0x02

class GroupTerminalDefaultMidiProtocol(IntEnum):
    USE_MIDI_CI                      = 0x00
    MIDI_1_0_UP_TO_64_BITS           = 0x01
    MIDI_1_0_UP_TO_64_BITS_AND_JRTS  = 0x02
    MIDI_1_0_UP_TO_128_BITS          = 0x03
    MIDI_1_0_UP_TO_128_BITS_AND_JRTS = 0x04
    MIDI_2_0                         = 0x11
    MIDI_2_0_AND_JRTS                = 0x12

class GroupTerminalNumber(IntEnum):
    GROUP_1  = 0x00
    GROUP_2  = 0x01
    GROUP_3  = 0x02
    GROUP_4  = 0x03
    GROUP_5  = 0x04
    GROUP_6  = 0x05
    GROUP_7  = 0x06
    GROUP_8  = 0x07
    GROUP_9  = 0x08
    GROUP_10 = 0x09
    GROUP_11 = 0x0A
    GROUP_12 = 0x0B
    GROUP_13 = 0x0C
    GROUP_14 = 0x0D
    GROUP_15 = 0x0E
    GROUP_16 = 0x0F