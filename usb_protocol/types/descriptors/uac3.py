#
# This file is part of usb-protocol.
#
"""
    descriptors specific to USB version 2 
    NOTE: This is not complete yet and will be extended as needed
"""

from build.lib.usb_protocol.emitters import descriptor
import unittest
from enum import IntEnum

import construct
from   construct  import this, Default

from .. import LanguageIDs
from ..descriptor import \
    DescriptorField, DescriptorNumber, DescriptorFormat, \
    BCDFieldAdapter, DescriptorLength

from .uac import *

class AudioClassSpecificASInterfaceDescriptorSubtypes(IntEnum):
    AS_DESCRIPTOR_UNDEFINED = 0x00
    AS_GENERAL              = 0x01
    AS_VALID_FREQ_RANGE     = 0x02

class ConnectorTypess(IntEnum):
    UNDEFINED                     = 0x00
    PHONE_CONNECTOR_2_5_MM        = 0x01
    PHONE_CONNECTOR_3_5_MM        = 0x02
    PHONE_CONNECTOR_6_35_MM       = 0x03
    XLR_6_35MM_COMBO_CONNECTOR    = 0x04
    XLR                           = 0x05
    OPTICAL_3_5MM_COMBO_CONNECTOR = 0x06
    RCA                           = 0x07
    BNC                           = 0x08
    BANANA                        = 0x09
    BINDING_POST                  = 0x0A
    SPEAKON                       = 0x0B
    SPRING_CLIP                   = 0x0C
    SCREW_TYPE                    = 0x0D
    DIN                           = 0x0E
    MINI_DIN                      = 0x0F
    EUROBLOCK                     = 0x10
    USB_TYPE_C                    = 0x11
    RJ_11                         = 0x12
    RJ_45                         = 0x13
    TOSLINK                       = 0x14
    HDMI                          = 0x15
    Mini_HDMI                     = 0x16
    Micro_HDMI                    = 0x17
    DP                            = 0x18
    MINI_DP                       = 0x19
    D_SUB                         = 0x1A
    THUNDERBOLT                   = 0x1B
    LIGHTNING                     = 0x1C
    WIRELESS                      = 0x1D
    USB_STANDARD_A                = 0x1E
    USB_STANDARD_B                = 0x1F
    USB_MINI_B                    = 0x20
    USB_MICRO_B                   = 0x21
    USB_MICRO_AB                  = 0x22
    USB_3_0_MICRO_B               = 0x23

class AudioDataFormats(IntEnum):
    PCM                             = (1 << 0)
    PCM8                            = (1 << 1)
    IEEE_FLOAT                      = (1 << 2)
    ALAW                            = (1 << 3)
    MULAW                           = (1 << 4)
    DSD                             = (1 << 5)
    RAW_DATA                        = (1 << 6)
    PCM_IEC60958                    = (1 << 7)
    AC_3                            = (1 << 8)
    MPEG_1_Layer1                   = (1 << 9)
    MPEG_1_Layer2_3                 = (1 << 10) # These share the same bit
    MPEG_2_NOEXT                    = (1 << 10) # These share the same bit
    MPEG_2_EXT                      = (1 << 11)
    MPEG_2_AAC_ADTS                 = (1 << 12)
    MPEG_2_Layer1_LS                = (1 << 13)
    MPEG_2_Layer2_3_LS              = (1 << 14)
    DTS_I                           = (1 << 15)
    DTS_II                          = (1 << 16)
    DTS_III                         = (1 << 17)
    ATRAC                           = (1 << 18)
    ATRAC2_3                        = (1 << 19)
    WMA                             = (1 << 20)
    E_AC_3                          = (1 << 21)
    MAT                             = (1 << 22)
    DTS_IV                          = (1 << 23)
    MPEG_4_HE_AAC                   = (1 << 24)
    MPEG_4_HE_AAC_V2                = (1 << 25)
    MPEG_4_AAC_LC                   = (1 << 26)
    DRA                             = (1 << 27)
    MPEG_4_HE_AAC_SURROUND          = (1 << 28)
    MPEG_4_AAC_LC_SURROUND          = (1 << 29)
    MPEG_H_3D_AUDIO                 = (1 << 30)
    AC4                             = (1 << 31)
    MPEG_4_AAC_ELD                  = (1 << 32)


HeaderDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(10, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificDescriptorTypes.CS_INTERFACE),
    "bDescriptorSubtype"  / DescriptorNumber(AudioClassSpecificACInterfaceDescriptorSubtypes.HEADER),
    "bCategory"           / DescriptorField(description="Audio Function Category, see AudioFunctionCategoryCodes"),
    "wTotalLength"        / DescriptorField("Length including subordinates"),
    "bmControls"          / DescriptorField("D1..0: Latency Control; D31..2: Reserved.", length=4, default=0)
)

AudioStreamingInterfaceDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(9, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(DescriptorTypes.INTERFACE),
    "bInterfaceNumber"    / DescriptorField(description="ID of the streaming interface"),
    "bAlternateSetting"   / DescriptorField(description="alternate setting number for the interface", default=0),
    "bNumEndpoints"       / DescriptorField(description="Number of data endpoints used (excluding endpoint 0). Can be: 0 (no data endpoint); 1 (data endpoint); 2 (data + explicit feedback endpoint)", default=0),
    "bInterfaceClass"     / DescriptorNumber(AudioInterfaceClassCode.AUDIO),
    "bInterfaceSubClass"  / DescriptorNumber(AudioInterfaceSubclassCodes.AUDIO_STREAMING),
    "bInterfaceProtocol"  / DescriptorNumber(AudioInterfaceProtocolCodes.IP_VERSION_03_00),
    "iInterface"          / DescriptorField(description="index of a string descriptor describing this interface (0 = unused)")
)

ClassSpecificAudioStreamingInterfaceDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(23, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificDescriptorTypes.CS_INTERFACE),
    "bDescriptorSubtype"  / DescriptorNumber(AudioClassSpecificASInterfaceDescriptorSubtypes.AS_GENERAL),
    "bTerminalLink"       / DescriptorField(description="the ID of the terminal to which this interface is connected"),
    "bmControls"          / DescriptorField(description="D1..0: active alternate setting control; D3..2: valid alternate settings control; D5..4: audio data format control; D31..6: reserved"),
    "wClusterDescrID"     / DescriptorField(description="ID of the cluster descriptor of the audio streamin interface"),
    "bmFormats"           / DescriptorField(description="audio data formats which can be used with this interface", length=8, default=AudioDataFormats.PCM),
    "bSubslotSize"        / DescriptorField(description="number of bytes occupied by one audio subslot"),
    "bBitResolution"      / DescriptorField(description="number of effectively used bits in the audio subslot"),
    "bmAuxProtocols"      / DescriptorField(description="which auxiliary protocols are required", default=0),
    "bControlSize"        / DescriptorField(description="size of the control channel words in bytes")
)

InputTerminalDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(20, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificDescriptorTypes.CS_INTERFACE),
    "bDescriptorSubtype"  / DescriptorNumber(AudioClassSpecificACInterfaceDescriptorSubtypes.INPUT_TERMINAL),
    "bTerminalID"         / DescriptorField(description="unique identifier for the terminal within the audio function."),
    "wTerminalType"       / DescriptorField(description="a value of one of the terminal types Enums (eg InputTerminaTypes, ExternalTerminalTypes)"),
    "bAssocTerminal"      / DescriptorField(description="ID of the associated output terminal"),
    "bCSourceID"          / DescriptorField(description="ID of the clock which is connected to this terminal"),
    "bmControls"          / DescriptorField(description="D1..0: Insertion Control; D3..2: Overload Control; D5..4: Underflow Control; D7..6: Overflow Control; D31..8: Reserved"),
    "wClusterDescrID"     / DescriptorField(description="ID of the cluster descriptor for this input terminal."),
    "wExTerminalDescrID"  / DescriptorField(description="ID of the extended terminal descriptor for this input terminal. Zero if no extended terminal descriptor is present."),
    "wConnectorsDescrID"  / DescriptorField(description="ID of the Connectors descriptor for this Input Terminal. Zero if no connectors descriptor is present."),
    "wTerminalDescrStr"   / DescriptorField(description="ID of a class-specific string descriptor, describing the input terminal.")
)

OutputTerminalDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(19, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificDescriptorTypes.CS_INTERFACE),
    "bDescriptorSubtype"  / DescriptorNumber(AudioClassSpecificACInterfaceDescriptorSubtypes.OUTPUT_TERMINAL),
    "bTerminalID"         / DescriptorField(description="unique identifier for the terminal within the audio function."),
    "wTerminalType"       / DescriptorField(description="a value of one of the terminal types Enums (eg OutputTerminaTypes, ExternalTerminalTypes)"),
    "bAssocTerminal"      / DescriptorField(description="ID of the associated input terminal"),
    "bSourceID"           / DescriptorField(description="ID of the unit or terminal which is connected to this terminal"),
    "bCSourceID"          / DescriptorField(description="ID of the clock which is connected to this terminal"),
    "bmControls"          / DescriptorField(description="D1..0: Insertion Control; D3..2: Overload Control; D5..4: Underflow Control; D7..6: Overflow Control; D31..8: Reserved"),
    "wClusterDescrID"     / DescriptorField(description="ID of the cluster descriptor for this input terminal."),
    "wExTerminalDescrID"  / DescriptorField(description="ID of the extended terminal descriptor for this output terminal. Zero if no extended terminal descriptor is present.", default=0),
    "wConnectorsDescrID"  / DescriptorField(description="ID of the connectors descriptor for this input terminal. Zero if no connectors descriptor is present.", default=0),
    "wTerminalDescrStr"   / DescriptorField(description="ID of a class-specific string descriptor, describing the output terminal.")
)