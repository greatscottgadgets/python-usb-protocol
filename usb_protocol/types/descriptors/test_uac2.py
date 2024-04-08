#
# This file is part of usb-protocol.
#
"""
    Unit tests for USB Audio Class Devices (UAC), Release 2
"""

import unittest

from .uac2 import *


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
        self.assertEqual(parsed.bDescriptorType, StandardDescriptorNumbers.INTERFACE_ASSOCIATION)
        self.assertEqual(parsed.bFirstInterface, 1)
        self.assertEqual(parsed.bInterfaceCount, 2)
        self.assertEqual(parsed.bFunctionClass, AudioFunctionClassCodes.AUDIO_FUNCTION)
        self.assertEqual(parsed.bFunctionSubClass, AudioFunctionCategoryCodes.FUNCTION_SUBCLASS_UNDEFINED)
        self.assertEqual(parsed.bFunctionProtocol, AudioFunctionProtocolCodes.AF_VERSION_02_00)
        self.assertEqual(parsed.iFunction, 0x42)

    def test_build_interface_association_descriptor(self):
        # Build the relevant descriptor
        data = InterfaceAssociationDescriptor.build({
            'bFirstInterface': 1,
            'bInterfaceCount': 2,
            'iFunction': 0x42,
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
        self.assertEqual(parsed.bDescriptorType, StandardDescriptorNumbers.INTERFACE)
        self.assertEqual(parsed.bInterfaceNumber, 1)
        self.assertEqual(parsed.bAlternateSetting, 2)
        self.assertEqual(parsed.bNumEndpoints, 0)
        self.assertEqual(parsed.bInterfaceClass, AudioInterfaceClassCodes.AUDIO)
        self.assertEqual(parsed.bInterfaceSubClass, AudioInterfaceSubclassCodes.AUDIO_CONTROL)
        self.assertEqual(parsed.bInterfaceProtocol, AudioInterfaceProtocolCodes.IP_VERSION_02_00)
        self.assertEqual(parsed.iInterface, 0x42)

    def test_build_standard_audio_control_interface_descriptor(self):
        # Build the relevant descriptor
        data = StandardAudioControlInterfaceDescriptor.build({
            'bInterfaceNumber': 1,
            'bAlternateSetting': 2,
            'bNumEndpoints': 0,
            'iInterface': 0x42,
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
            0x0A,  # Subtype
            0x01,  # Clock ID
            0x01,  # Attributes
            0x01,  # Controls
            0x01,  # Associate terminal
            0x42   # Clock source name
            ])

        # ... and check the descriptor's fields.
        self.assertEqual(parsed.bLength, 8)
        self.assertEqual(parsed.bDescriptorType, AudioClassSpecificStandardDescriptorNumbers.CS_INTERFACE)
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
                0x0A,  # Subtype
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
                0x23,                    # First channel name
                0x05, 0x00,              # Controls
                0x42                     # Terminal name
            ])

        # ... and check the descriptor's fields.
        self.assertEqual(parsed.bLength, 17)
        self.assertEqual(parsed.bDescriptorType, AudioClassSpecificStandardDescriptorNumbers.CS_INTERFACE)
        self.assertEqual(parsed.bDescriptorSubtype, AudioClassSpecificACInterfaceDescriptorSubtypes.INPUT_TERMINAL)
        self.assertEqual(parsed.bTerminalID, 0x01)
        self.assertEqual(parsed.wTerminalType, USBTerminalTypes.USB_STREAMING)
        self.assertEqual(parsed.bAssocTerminal, 0x00)
        self.assertEqual(parsed.bCSourceID, 0x01)
        self.assertEqual(parsed.bNrChannels, 0x02)
        self.assertEqual(parsed.bmChannelConfig, 0x0003)
        self.assertEqual(parsed.iChannelNames, 0x23)
        self.assertEqual(parsed.bmControls, 5)
        self.assertEqual(parsed.iTerminal, 0x42)

    def test_build_input_terminal_descriptor(self):
        # Build the relevant descriptor
        data = InputTerminalDescriptor.build({
            'bTerminalID': 1,
            'wTerminalType': USBTerminalTypes.USB_STREAMING,
            'bCSourceID': 1,
            'bNrChannels': 2,
            'bmChannelConfig': 3,
            'iChannelNames': 0x23,
            'bmControls': 5,
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
                0x23,                    # First channel name
                0x05, 0x00,              # Controls
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
        self.assertEqual(parsed.bDescriptorType, AudioClassSpecificStandardDescriptorNumbers.CS_INTERFACE)
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

    def test_parse_feature_unit_descriptor(self):
        # Parse the relevant descriptor ...
        parsed = FeatureUnitDescriptor.parse([
                0x12,                    # Length
                0x24,                    # Type
                0x06,                    # Subtype
                0x06,                    # Unit ID
                0x09,                    # Source ID
                0x01, 0x00, 0x00, 0x00,  # Controls 0
                0x02, 0x00, 0x00, 0x00,  # Controls 1
                0x03, 0x00, 0x00, 0x00,  # Controls 2
                0x42                     # Unit name
            ])

        # ... and check the descriptor's fields.
        self.assertEqual(parsed.bLength, 18)
        self.assertEqual(parsed.bDescriptorType, AudioClassSpecificStandardDescriptorNumbers.CS_INTERFACE)
        self.assertEqual(parsed.bDescriptorSubtype, AudioClassSpecificACInterfaceDescriptorSubtypes.FEATURE_UNIT)
        self.assertEqual(parsed.bUnitID, 0x06)
        self.assertEqual(parsed.bSourceID, 0x09)
        self.assertEqual(parsed.bmaControls, [0x0001, 0x0002, 0x0003])
        self.assertEqual(parsed.iFeature, 0x42)

    def test_build_feature_unit_descriptor(self):
        # Build the relevant descriptor
        data = FeatureUnitDescriptor.build({
            'bUnitID': 6,
            'bSourceID': 9,
            'bmaControls': [1, 2, 3],
            'iFeature': 0x42,
        })

        # ... and check the binary output
        self.assertEqual(data, bytes([
                0x12,                    # Length
                0x24,                    # Type
                0x06,                    # Subtype
                0x06,                    # Unit ID
                0x09,                    # Source ID
                0x01, 0x00, 0x00, 0x00,  # Controls 0
                0x02, 0x00, 0x00, 0x00,  # Controls 1
                0x03, 0x00, 0x00, 0x00,  # Controls 2
                0x42                     # Unit name
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
        self.assertEqual(parsed.bDescriptorType, StandardDescriptorNumbers.INTERFACE)
        self.assertEqual(parsed.bInterfaceNumber, 2)
        self.assertEqual(parsed.bAlternateSetting, 3)
        self.assertEqual(parsed.bNumEndpoints, 1)
        self.assertEqual(parsed.bInterfaceClass, AudioInterfaceClassCodes.AUDIO)
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
        self.assertEqual(parsed.bDescriptorType, AudioClassSpecificStandardDescriptorNumbers.CS_INTERFACE)
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
        self.assertEqual(parsed.bDescriptorType, AudioClassSpecificStandardDescriptorNumbers.CS_INTERFACE)
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
        self.assertEqual(parsed.bDescriptorType, AudioClassSpecificStandardDescriptorNumbers.CS_INTERFACE)
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
        self.assertEqual(parsed.bDescriptorType, AudioClassSpecificStandardDescriptorNumbers.CS_INTERFACE)
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
        self.assertEqual(parsed.bDescriptorType, AudioClassSpecificStandardDescriptorNumbers.CS_INTERFACE)
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
        self.assertEqual(parsed.bDescriptorType, AudioClassSpecificStandardDescriptorNumbers.CS_INTERFACE)
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
        self.assertEqual(parsed.bDescriptorType, AudioClassSpecificStandardDescriptorNumbers.CS_INTERFACE)
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
        self.assertEqual(parsed.bDescriptorType, AudioClassSpecificStandardDescriptorNumbers.CS_ENDPOINT)
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
