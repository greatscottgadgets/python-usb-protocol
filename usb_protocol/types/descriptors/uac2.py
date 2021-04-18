#
# This file is part of usb-protocol.
#
""" descriptors specific to USB version 2
    NOTE: This is not complete yet and will be extended as needed
"""

import unittest
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
    "bInterfaceNumber"    / DescriptorField(description="ID of the control interface"),
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
    "bLength"             / construct.Const(8, construct.Int8ul),
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
    "bmChannelConfig"     / DescriptorField(description="describes the spatial location of the logical channels", default=0, length=4),
    "bmControls"          / DescriptorField(description="OR combination of  ClockFrequencyControl, CopyProtectControl, ConnectorControl, ClusterControl, UnderflowControl and OverflowControl", default=0, length=2),
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
    "bmControls"          / DescriptorField(description="OR combination of  ClockFrequencyControl, CopyProtectControl, ConnectorControl, UnderflowControl>>2 and OverflowControl>>2", default=0, length=2),
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
    "bmChannelConfig"     / DescriptorField(description="spatial location of the physical channels", default=0, length=4),
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
    "bLength"             / construct.Const(6, construct.Int8ul),
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


class UAC2Cases(unittest.TestCase):

    def test_parse_interface_association_descriptor(self):
        # Parse the relevant descriptor ...
        parsed = InterfaceAssociationDescriptor.parse([
                0x08,  # Length
                0x0B,  # Type
                0x01,  # First interface
                0x02,  # Interface count
                0x01,  # Function class
                0x00,  # Function subclass
                0x20,  # Function protocol
                0x42   # Function name
            ])

        # ... and check the descriptor's fields.
        self.assertEqual(parsed.bLength, 8)
        self.assertEqual(parsed.bDescriptorType, DescriptorTypes.INTERFACE_ASSOCIATION)
        self.assertEqual(parsed.bFirstInterface, 1)
        self.assertEqual(parsed.bInterfaceCount, 2)
        self.assertEqual(parsed.bFunctionClass, AudioFunctionClassCode.AUDIO_FUNCTION)
        self.assertEqual(parsed.bFunctionSubClass, AudioFunctionCategoryCodes.FUNCTION_SUBCLASS_UNDEFINED)
        self.assertEqual(parsed.bFunctionProtocol, AudioFunctionProtocolCodes.AF_VERSION_02_00)
        self.assertEqual(parsed.iFunction, 0x42)

    def test_build_interface_association_descriptor(self):
        # Build the relevant descriptor
        data = InterfaceAssociationDescriptor.build({
            'bFirstInterface': 1,
            'bInterfaceCount': 2,
            'iFunction': 0x42
        })

        # ... and check the binary output
        self.assertEqual(data, bytes([
                0x08,  # Length
                0x0B,  # Type
                0x01,  # First interface
                0x02,  # Interface count
                0x01,  # Function class
                0x00,  # Function subclass
                0x20,  # Function protocol
                0x42   # Function name
            ]))

    def test_parse_standard_audio_control_interface_descriptor(self):
        # Parse the relevant descriptor ...
        parsed = StandardAudioControlInterfaceDescriptor.parse([
                0x09,  # Length
                0x04,  # Type
                0x01,  # Interface number
                0x02,  # Alternate settings
                0x00,  # Number of endpoints
                0x01,  # Interface class
                0x01,  # Interface subclass
                0x20,  # Interface protocol
                0x42   # Interface name
            ])

        # ... and check the descriptor's fields.
        self.assertEqual(parsed.bLength, 9)
        self.assertEqual(parsed.bDescriptorType, DescriptorTypes.INTERFACE)
        self.assertEqual(parsed.bInterfaceNumber, 1)
        self.assertEqual(parsed.bAlternateSetting, 2)
        self.assertEqual(parsed.bNumEndpoints, 0)
        self.assertEqual(parsed.bInterfaceClass, AudioInterfaceClassCode.AUDIO)
        self.assertEqual(parsed.bInterfaceSubClass, AudioInterfaceSubclassCodes.AUDIO_CONTROL)
        self.assertEqual(parsed.bInterfaceProtocol, AudioInterfaceProtocolCodes.IP_VERSION_02_00)
        self.assertEqual(parsed.iInterface, 0x42)

    def test_build_standard_audio_control_interface_descriptor(self):
        # Build the relevant descriptor
        data = StandardAudioControlInterfaceDescriptor.build({
            'bInterfaceNumber': 1,
            'bAlternateSetting': 2,
            'bNumEndpoints': 0,
            'iInterface': 0x42
        })

        # ... and check the binary output
        self.assertEqual(data, bytes([
                0x09,  # Length
                0x04,  # Type
                0x01,  # Interface number
                0x02,  # Alternate settings
                0x00,  # Number of endpoints
                0x01,  # Interface class
                0x01,  # Interface subclass
                0x20,  # Interface protocol
                0x42   # Interface Name
            ]))

    def test_parse_clock_source_descriptor(self):
        # Parse the relevant descriptor ...
        parsed = ClockSourceDescriptor.parse([
            0x08,  # Length
            0x24,  # Type
            0x0B,  # Subtype
            0x01,  # Clock ID
            0x01,  # Attributes
            0x01,  # Controls
            0x01,  # Associate terminal
            0x42   # Clock source name
            ])

        # ... and check the descriptor's fields.
        self.assertEqual(parsed.bLength, 8)
        self.assertEqual(parsed.bDescriptorType, AudioClassSpecificDescriptorTypes.CS_INTERFACE)
        self.assertEqual(parsed.bDescriptorSubtype, AudioClassSpecificACInterfaceDescriptorSubtypes.CLOCK_SOURCE)
        self.assertEqual(parsed.bClockID, 0x01)
        self.assertEqual(parsed.bmAttributes, ClockAttributes.INTERNAL_FIXED_CLOCK)
        self.assertEqual(parsed.bmControls, ClockFrequencyControl.HOST_READ_ONLY)
        self.assertEqual(parsed.bAssocTerminal, 0x01)
        self.assertEqual(parsed.iClockSource, 0x42)

    def test_build_clock_source_descriptor(self):
        # Build the relevant descriptor
        data = ClockSourceDescriptor.build({
            'bClockID': 1,
            'bmAttributes': ClockAttributes.INTERNAL_FIXED_CLOCK,
            'bmControls': ClockFrequencyControl.HOST_READ_ONLY,
            'bAssocTerminal': 0x01,
            'iClockSource': 0x42,
        })

        # ... and check the binary output
        self.assertEqual(data, bytes([
                0x08,  # Length
                0x24,  # Type
                0x0B,  # Subtype
                0x01,  # Clock ID
                0x01,  # Attributes
                0x01,  # Controls
                0x01,  # Associate terminal
                0x42   # Clock source name
            ]))

    def test_parse_input_terminal_descriptor(self):
        # Parse the relevant descriptor ...
        parsed = InputTerminalDescriptor.parse([
                0x11,                    # Length
                0x24,                    # Type
                0x02,                    # Subtype
                0x01,                    # Terminal ID
                0x01, 0x01,              # Terminal type
                0x00,                    # Associated terminal
                0x01,                    # Clock ID
                0x02,                    # Number of channels
                0x03, 0x00, 0x00, 0x00,  # Channel configuration
                0x00,                    # First channel name
                0x00, 0x00,              # Controls
                0x42                     # Terminal name
            ])

        # ... and check the descriptor's fields.
        self.assertEqual(parsed.bLength, 17)
        self.assertEqual(parsed.bDescriptorType, AudioClassSpecificDescriptorTypes.CS_INTERFACE)
        self.assertEqual(parsed.bDescriptorSubtype, AudioClassSpecificACInterfaceDescriptorSubtypes.INPUT_TERMINAL)
        self.assertEqual(parsed.bTerminalID, 0x01)
        self.assertEqual(parsed.wTerminalType, USBTerminalTypes.USB_STREAMING)
        self.assertEqual(parsed.bAssocTerminal, 0x00)
        self.assertEqual(parsed.bCSourceID, 0x01)
        self.assertEqual(parsed.bNrChannels, 0x02)
        self.assertEqual(parsed.bmChannelConfig, 0x0003)
        self.assertEqual(parsed.iChannelNames, 0x00)
        self.assertEqual(parsed.iTerminal, 0x42)

    def test_build_input_terminal_descriptor(self):
        # Build the relevant descriptor
        data = InputTerminalDescriptor.build({
            'bTerminalID': 1,
            'wTerminalType': USBTerminalTypes.USB_STREAMING,
            'bCSourceID': 1,
            'bNrChannels': 2,
            'bmChannelConfig': 3,
            'iTerminal': 0x42,
        })

        # ... and check the binary output
        self.assertEqual(data, bytes([
                0x11,                    # Length
                0x24,                    # Type
                0x02,                    # Subtype
                0x01,                    # Terminal ID
                0x01, 0x01,              # Terminal type
                0x00,                    # Associated terminal
                0x01,                    # Clock ID
                0x02,                    # Number of channels
                0x03, 0x00, 0x00, 0x00,  # Channel configuration
                0x00,                    # First channel name
                0x00, 0x00,              # Controls
                0x42                     # Terminal name
            ]))

    def test_parse_output_terminal_descriptor(self):
        # Parse the relevant descriptor ...
        parsed = OutputTerminalDescriptor.parse([
                0x0C,        # Length
                0x24,        # Type
                0x03,        # Subtype
                0x06,        # Terminal ID
                0x01, 0x03,  # Terminal type
                0x00,        # Associated terminal
                0x09,        # Source ID
                0x01,        # Clock ID
                0x00, 0x00,  # Controls
                0x42         # Terminal name
            ])

        # ... and check the descriptor's fields.
        self.assertEqual(parsed.bLength, 12)
        self.assertEqual(parsed.bDescriptorType, AudioClassSpecificDescriptorTypes.CS_INTERFACE)
        self.assertEqual(parsed.bDescriptorSubtype, AudioClassSpecificACInterfaceDescriptorSubtypes.OUTPUT_TERMINAL)
        self.assertEqual(parsed.bTerminalID, 0x06)
        self.assertEqual(parsed.wTerminalType, OutputTerminalTypes.SPEAKER)
        self.assertEqual(parsed.bAssocTerminal, 0x00)
        self.assertEqual(parsed.bSourceID, 0x09)
        self.assertEqual(parsed.bCSourceID, 0x01)
        self.assertEqual(parsed.bmControls, 0x0000)
        self.assertEqual(parsed.iTerminal, 0x42)

    def test_build_output_terminal_descriptor(self):
        # Build the relevant descriptor
        data = OutputTerminalDescriptor.build({
            'bTerminalID': 6,
            'wTerminalType': OutputTerminalTypes.SPEAKER,
            'bSourceID': 9,
            'bCSourceID': 1,
            'iTerminal': 0x42,
        })

        # ... and check the binary output
        self.assertEqual(data, bytes([
                0x0C,        # Length
                0x24,        # Type
                0x03,        # Subtype
                0x06,        # Terminal ID
                0x01, 0x03,  # Terminal type
                0x00,        # Associated terminal
                0x09,        # Source ID
                0x01,        # Clock ID
                0x00, 0x00,  # Controls
                0x42         # Terminal name
            ]))

    def test_parse_audio_streaming_interface_descriptor(self):
        # Parse the relevant descriptor ...
        parsed = AudioStreamingInterfaceDescriptor.parse([
                0x09,  # Length
                0x04,  # Type
                0x02,  # Interface number
                0x03,  # Alternate setting
                0x01,  # Number of endpoints
                0x01,  # Interface class
                0x02,  # Interface subclass
                0x20,  # Interface protocol
                0x42   # Interface name
            ])

        # ... and check the descriptor's fields.
        self.assertEqual(parsed.bLength, 9)
        self.assertEqual(parsed.bDescriptorType, DescriptorTypes.INTERFACE)
        self.assertEqual(parsed.bInterfaceNumber, 2)
        self.assertEqual(parsed.bAlternateSetting, 3)
        self.assertEqual(parsed.bNumEndpoints, 1)
        self.assertEqual(parsed.bInterfaceClass, AudioInterfaceClassCode.AUDIO)
        self.assertEqual(parsed.bInterfaceSubClass, AudioInterfaceSubclassCodes.AUDIO_STREAMING)
        self.assertEqual(parsed.bInterfaceProtocol, AudioInterfaceProtocolCodes.IP_VERSION_02_00)
        self.assertEqual(parsed.iInterface, 0x42)

    def test_build_audio_streaming_interface_descriptor(self):
        # Build the relevant descriptor
        data = AudioStreamingInterfaceDescriptor.build({
            'bInterfaceNumber': 2,
            'bAlternateSetting': 3,
            'bNumEndpoints': 1,
            'iInterface': 0x42,
        })

        # ... and check the binary output
        self.assertEqual(data, bytes([
                0x09,  # Length
                0x04,  # Type
                0x02,  # Interface number
                0x03,  # Alternate setting
                0x01,  # Number of endpoints
                0x01,  # Interface class
                0x02,  # Interface subclass
                0x20,  # Interface protocol
                0x42   # Interface name
            ]))

    def test_parse_class_specific_audio_streaming_interface_descriptor(self):
        # Parse the relevant descriptor ...
        parsed = ClassSpecificAudioStreamingInterfaceDescriptor.parse([
                0x10,                    # Length
                0x24,                    # Type
                0x01,                    # Subtype
                0x03,                    # Terminal ID
                0x00,                    # Controls
                0x01,                    # Format type
                0x01, 0x00, 0x00, 0x00,  # Formats
                0x02,                    # Number of channels
                0x00, 0x00, 0x00, 0x00,  # Channel config
                0x42                     # First channel name
            ])

        # ... and check the descriptor's fields.
        self.assertEqual(parsed.bLength, 16)
        self.assertEqual(parsed.bDescriptorType, AudioClassSpecificDescriptorTypes.CS_INTERFACE)
        self.assertEqual(parsed.bDescriptorSubtype, AudioClassSpecificASInterfaceDescriptorSubtypes.AS_GENERAL)
        self.assertEqual(parsed.bTerminalLink, 3)
        self.assertEqual(parsed.bmControls, 0)
        self.assertEqual(parsed.bFormatType, FormatTypes.FORMAT_TYPE_I)
        self.assertEqual(parsed.bmFormats, TypeIFormats.PCM)
        self.assertEqual(parsed.bNrChannels, 2)
        self.assertEqual(parsed.bmChannelConfig, 0x0)
        self.assertEqual(parsed.iChannelNames, 0x42)

    def test_build_class_specific_audio_streaming_interface_descriptor(self):
        # Build the relevant descriptor
        data = ClassSpecificAudioStreamingInterfaceDescriptor.build({
            'bTerminalLink': 3,
            'bmControls': 0,
            'bFormatType': FormatTypes.FORMAT_TYPE_I,
            'bmFormats': TypeIFormats.PCM,
            'bNrChannels': 2,
            'bmChannelConfig': 0,
            'iChannelNames': 0x42,
        })

        # ... and check the binary output
        self.assertEqual(data, bytes([
                0x10,                    # Length
                0x24,                    # Type
                0x01,                    # Subtype
                0x03,                    # Terminal ID
                0x00,                    # Controls
                0x01,                    # Format type
                0x01, 0x00, 0x00, 0x00,  # Formats
                0x02,                    # Number of channels
                0x00, 0x00, 0x00, 0x00,  # Channel config
                0x42                     # First channel name
            ]))

    def test_parse_type_i_format_type_descriptor(self):
        # Parse the relevant descriptor ...
        parsed = TypeIFormatTypeDescriptor.parse([
                0x06,  # Length
                0x24,  # Type
                0x02,  # Subtype
                0x01,  # Format type
                0x02,  # Subslot size
                0x10,  # Bit resolution
            ])

        # ... and check the descriptor's fields.
        self.assertEqual(parsed.bLength, 6)
        self.assertEqual(parsed.bDescriptorType, AudioClassSpecificDescriptorTypes.CS_INTERFACE)
        self.assertEqual(parsed.bDescriptorSubtype, AudioClassSpecificASInterfaceDescriptorSubtypes.FORMAT_TYPE)
        self.assertEqual(parsed.bFormatType, FormatTypes.FORMAT_TYPE_I)
        self.assertEqual(parsed.bSubslotSize, 2)
        self.assertEqual(parsed.bBitResolution, 16)

    def test_build_type_i_format_type_descriptor(self):
        # Build the relevant descriptor
        data = TypeIFormatTypeDescriptor.build({
            'bSubslotSize': 2,
            'bBitResolution': 16,
        })

        # ... and check the binary output
        self.assertEqual(data, bytes([
                0x06,  # Length
                0x24,  # Type
                0x02,  # Subtype
                0x01,  # Format type
                0x02,  # Subslot size
                0x10,  # Bit resolution
            ]))

    def test_parse_extended_type_i_format_type_descriptor(self):
        # Parse the relevant descriptor ...
        parsed = ExtendedTypeIFormatTypeDescriptor.parse([
                0x09,  # Length
                0x24,  # Type
                0x02,  # Subtype
                0x81,  # Format type
                0x02,  # Subslot size
                0x10,  # Bit resolution
                0x0A,  # Header length
                0x04,  # Control size
                0x00,  # Side band protocol
            ])

        # ... and check the descriptor's fields.
        self.assertEqual(parsed.bLength, 9)
        self.assertEqual(parsed.bDescriptorType, AudioClassSpecificDescriptorTypes.CS_INTERFACE)
        self.assertEqual(parsed.bDescriptorSubtype, AudioClassSpecificASInterfaceDescriptorSubtypes.FORMAT_TYPE)
        self.assertEqual(parsed.bFormatType, FormatTypes.EXT_FORMAT_TYPE_I)
        self.assertEqual(parsed.bSubslotSize, 2)
        self.assertEqual(parsed.bBitResolution, 16)
        self.assertEqual(parsed.bHeaderLength, 10)
        self.assertEqual(parsed.bControlSize, 4)
        self.assertEqual(parsed.bSideBandProtocol, 0)

    def test_build_extended_type_i_format_type_descriptor(self):
        # Build the relevant descriptor
        data = ExtendedTypeIFormatTypeDescriptor.build({
            'bSubslotSize': 2,
            'bBitResolution': 16,
            'bHeaderLength': 10,
            'bControlSize': 4,
            'bSideBandProtocol': 0,
        })

        # ... and check the binary output
        self.assertEqual(data, bytes([
                0x09,  # Length
                0x24,  # Type
                0x02,  # Subtype
                0x81,  # Format type
                0x02,  # Subslot size
                0x10,  # Bit resolution
                0x0A,  # Header length
                0x04,  # Control size
                0x00,  # Side band protocol
            ]))

    def test_parse_type_ii_format_type_descriptor(self):
        # Parse the relevant descriptor ...
        parsed = TypeIIFormatTypeDescriptor.parse([
                0x08,        # Length
                0x24,        # Type
                0x02,        # Subtype
                0x02,        # Format type
                0x40, 0x00,  # Maximum bit rate
                0x20, 0x00,  # Slots per frame
            ])

        # ... and check the descriptor's fields.
        self.assertEqual(parsed.bLength, 8)
        self.assertEqual(parsed.bDescriptorType, AudioClassSpecificDescriptorTypes.CS_INTERFACE)
        self.assertEqual(parsed.bDescriptorSubtype, AudioClassSpecificASInterfaceDescriptorSubtypes.FORMAT_TYPE)
        self.assertEqual(parsed.bFormatType, FormatTypes.FORMAT_TYPE_II)
        self.assertEqual(parsed.wMaxBitRate, 64)
        self.assertEqual(parsed.wSlotsPerFrame, 32)

    def test_build_type_ii_format_type_descriptor(self):
        # Build the relevant descriptor
        data = TypeIIFormatTypeDescriptor.build({
            'wMaxBitRate': 64,
            'wSlotsPerFrame': 32,
        })

        # ... and check the binary output
        self.assertEqual(data, bytes([
                0x08,        # Length
                0x24,        # Type
                0x02,        # Subtype
                0x02,        # Format type
                0x40, 0x00,  # Maximum bit rate
                0x20, 0x00,  # Slots per frame
            ]))

    def test_parse_extended_type_ii_format_type_descriptor(self):
        # Parse the relevant descriptor ...
        parsed = ExtendedTypeIIFormatTypeDescriptor.parse([
                0x0A,        # Length
                0x24,        # Type
                0x02,        # Subtype
                0x82,        # Format type
                0x40, 0x00,  # Maximum bit rate
                0x20, 0x00,  # Samples per frame
                0x0A,        # Header length
                0x00,        # Side band protocol
            ])

        # ... and check the descriptor's fields.
        self.assertEqual(parsed.bLength, 10)
        self.assertEqual(parsed.bDescriptorType, AudioClassSpecificDescriptorTypes.CS_INTERFACE)
        self.assertEqual(parsed.bDescriptorSubtype, AudioClassSpecificASInterfaceDescriptorSubtypes.FORMAT_TYPE)
        self.assertEqual(parsed.bFormatType, FormatTypes.EXT_FORMAT_TYPE_II)
        self.assertEqual(parsed.wMaxBitRate, 64)
        self.assertEqual(parsed.wSamplesPerFrame, 32)
        self.assertEqual(parsed.bHeaderLength, 10)
        self.assertEqual(parsed.bSideBandProtocol, 0)

    def test_build_extended_type_ii_format_type_descriptor(self):
        # Build the relevant descriptor
        data = ExtendedTypeIIFormatTypeDescriptor.build({
            'wMaxBitRate': 64,
            'wSamplesPerFrame': 32,
            'bHeaderLength': 10,
            'bSideBandProtocol': 0,
        })

        # ... and check the binary output
        self.assertEqual(data, bytes([
                0x0A,        # Length
                0x24,        # Type
                0x02,        # Subtype
                0x82,        # Format type
                0x40, 0x00,  # Maximum bit rate
                0x20, 0x00,  # Samples per frame
                0x0A,        # Header length
                0x00,        # Side band protocol
            ]))

    def test_parse_type_iii_format_type_descriptor(self):
        # Parse the relevant descriptor ...
        parsed = TypeIIIFormatTypeDescriptor.parse([
                0x06,  # Length
                0x24,  # Type
                0x02,  # Subtype
                0x03,  # Format type
                0x02,  # Subslot size
                0x10,  # Bit resolution
            ])

        # ... and check the descriptor's fields.
        self.assertEqual(parsed.bLength, 6)
        self.assertEqual(parsed.bDescriptorType, AudioClassSpecificDescriptorTypes.CS_INTERFACE)
        self.assertEqual(parsed.bDescriptorSubtype, AudioClassSpecificASInterfaceDescriptorSubtypes.FORMAT_TYPE)
        self.assertEqual(parsed.bFormatType, FormatTypes.FORMAT_TYPE_III)
        self.assertEqual(parsed.bSubslotSize, 2)
        self.assertEqual(parsed.bBitResolution, 16)

    def test_build_type_iii_format_type_descriptor(self):
        # Build the relevant descriptor
        data = TypeIIIFormatTypeDescriptor.build({
            'bBitResolution': 16,
        })

        # ... and check the binary output
        self.assertEqual(data, bytes([
                0x06,  # Length
                0x24,  # Type
                0x02,  # Subtype
                0x03,  # Format type
                0x02,  # Subslot size
                0x10,  # Bit resolution
            ]))

    def test_parse_extended_type_iii_format_type_descriptor(self):
        # Parse the relevant descriptor ...
        parsed = ExtendedTypeIIIFormatTypeDescriptor.parse([
                0x08,  # Length
                0x24,  # Type
                0x02,  # Subtype
                0x83,  # Format type
                0x02,  # Subslot size
                0x10,  # Bit resolution
                0x0A,  # Header length
                0x00,  # Side band protocol
            ])

        # ... and check the descriptor's fields.
        self.assertEqual(parsed.bLength, 8)
        self.assertEqual(parsed.bDescriptorType, AudioClassSpecificDescriptorTypes.CS_INTERFACE)
        self.assertEqual(parsed.bDescriptorSubtype, AudioClassSpecificASInterfaceDescriptorSubtypes.FORMAT_TYPE)
        self.assertEqual(parsed.bFormatType, FormatTypes.EXT_FORMAT_TYPE_III)
        self.assertEqual(parsed.bSubslotSize, 2)
        self.assertEqual(parsed.bBitResolution, 16)
        self.assertEqual(parsed.bHeaderLength, 10)
        self.assertEqual(parsed.bSideBandProtocol, 0)

    def test_build_extended_type_iii_format_type_descriptor(self):
        # Build the relevant descriptor
        data = ExtendedTypeIIIFormatTypeDescriptor.build({
            'bBitResolution': 16,
            'bHeaderLength': 10,
            'bSideBandProtocol': 0,
        })

        # ... and check the binary output
        self.assertEqual(data, bytes([
                0x08,  # Length
                0x24,  # Type
                0x02,  # Subtype
                0x83,  # Format type
                0x02,  # Subslot size
                0x10,  # Bit resolution
                0x0A,  # Header length
                0x00,  # Side band protocol
            ]))

    def test_parse_class_specific_audio_streaming_isochronous_audio_data_endpoint_descriptor(self):
        # Parse the relevant descriptor ...
        parsed = ClassSpecificAudioStreamingIsochronousAudioDataEndpointDescriptor.parse([
                0x08,       # Length
                0x25,       # Type
                0x01,       # Subtype
                0x00,       # Attributes
                0x00,       # Controls
                0x01,       # Lock Delay Units
                0x00, 0x00  # Lock delay
            ])

        # ... and check the descriptor's fields.
        self.assertEqual(parsed.bLength, 8)
        self.assertEqual(parsed.bDescriptorType, AudioClassSpecificDescriptorTypes.CS_ENDPOINT)
        self.assertEqual(parsed.bDescriptorSubtype, AudioClassSpecificEndpointDescriptorSubtypes.EP_GENERAL)
        self.assertEqual(parsed.bmAttributes, 0)
        self.assertEqual(parsed.bmControls, 0)
        self.assertEqual(parsed.bLockDelayUnits, 1)
        self.assertEqual(parsed.wLockDelay, 0)

    def test_build_class_specific_audio_streaming_isochronous_audio_data_endpoint_descriptor(self):
        # Build the relevant descriptor
        data = ClassSpecificAudioStreamingIsochronousAudioDataEndpointDescriptor.build({
            'bmAttributes': 0,
            'bmControls': 0,
            'bLockDelayUnits': 1,
            'wLockDelay': 0,
        })

        # ... and check the binary output
        self.assertEqual(data, bytes([
                0x08,       # Length
                0x25,       # Type
                0x01,       # Subtype
                0x00,       # Attributes
                0x00,       # Controls
                0x01,       # Lock Delay Units
                0x00, 0x00  # Lock delay
            ]))
