#
# This file is part of usb-protocol.
#
"""
    Descriptors for USB Audio Class Devices (UAC), Release 1

    [Audio10] refers to "Universal Serial Bus Device Class Definition for Audio Devices", Release 1.0, March 18, 1998
    [Frmts10] refers to "Universal Serial Bus Device Class Definition for Audio Data Formats", Release 1.0, March 18, 1998
    [TermT10] refers to "Universal Serial Bus Device Class Definition for Terminal Types", Release 1.0, March 18, 1998
"""

import construct

from enum import IntEnum

from .standard import StandardDescriptorNumbers

from ..descriptor import (
    DescriptorField,
    DescriptorNumber,
    DescriptorFormat,
)


class AudioInterfaceClassCode(IntEnum):
    # As defined in [Audio10], Table A-1
    AUDIO = 0x01


class AudioInterfaceSubclassCodes(IntEnum):
    # As defined in [Audio10], Table A-2
    INTERFACE_SUBCLASS_UNDEFINED = 0x00
    AUDIO_CONTROL                = 0x01
    AUDIO_STREAMING              = 0x02
    MIDI_STREAMING               = 0x03


class AudioInterfaceProtocolCodes(IntEnum):
    # As defined in [Audio10], Table A-3
    PR_PROTOCOL_UNDEFINED = 0x00


class AudioClassSpecificDescriptorTypes(IntEnum):
    # As defined in [Audio10], Table A-4
    CS_UNDEFINED     = 0x20
    CS_DEVICE        = 0x21
    CS_CONFIGURATION = 0x22
    CS_STRING        = 0x23
    CS_INTERFACE     = 0x24
    CS_ENDPOINT      = 0x25


class AudioClassSpecificACInterfaceDescriptorSubtypes(IntEnum):
    # As defined in [Audio10], Table A-5
    AC_DESCRIPTOR_UNDEFINED  = 0x00
    HEADER                   = 0x01
    INPUT_TERMINAL           = 0x02
    OUTPUT_TERMINAL          = 0x03
    MIXER_UNIT               = 0x04
    SELECTOR_UNIT            = 0x05
    FEATURE_UNIT             = 0x06
    PROCESSING_UNIT          = 0x07
    EXTENSION_UNIT           = 0x08


class AudioClassSpecificASInterfaceDescriptorSubtypes(IntEnum):
    # As defined in [Audio10], Table A-6
    AS_DESCRIPTOR_UNDEFINED = 0x00
    AS_GENERAL              = 0x01
    FORMAT_TYPE             = 0x02
    FORMAT_SPECIFIC         = 0x03


class ProcessingUnitProcessTypes(IntEnum):
    # As defined in [Audio10], Table A-7
    PROCESS_UNDEFINED            = 0x00
    UP_DOWNMIX_PROCESS           = 0x01
    DOLBY_PROLOGIC_PROCESS       = 0x02
    _3D_STEREO_EXTENDER_PROCESS  = 0x03
    REVERBERATION_PROCESS        = 0x04
    CHORUS_PROCESS               = 0x05
    DYN_RANGE_COMP_PROCESS       = 0x06


class AudioClassSpecificEndpointDescriptorSubtypes(IntEnum):
    # As defined in [Audio10], Table A-8
    DESCRIPTOR_UNDEFINED = 0x00
    EP_GENERAL           = 0x01


class AudioClassSpecificRequestCodes(IntEnum):
    # As defined in [Audio10], Table A-9
    REQUEST_CODE_UNDEFINED = 0x00
    SET_CUR                = 0x01
    GET_CUR                = 0x81
    SET_MIN                = 0x02
    GET_MIN                = 0x82
    SET_MAX                = 0x03
    GET_MAX                = 0x83
    SET_RES                = 0x04
    GET_RES                = 0x84
    SET_MEM                = 0x05
    GET_MEM                = 0x85
    GET_STAT               = 0xFF


class TerminalControlSelectors(IntEnum):
    # As defined in [Audio10], Table A-10
    TE_CONTROL_UNDEFINED = 0x00
    COPY_PROTECT_CONTROL = 0x01


class FeatureUnitControlSelectors(IntEnum):
    # As defined in [Audio10], Table A-11
    FU_CONTROL_UNDEFINED      = 0x00
    MUTE_CONTROL              = 0x01
    VOLUME_CONTROL            = 0x02
    BASS_CONTROL              = 0x03
    MID_CONTROL               = 0x04
    TREBLE_CONTROL            = 0x05
    GRAPHIC_EQUALIZER_CONTROL = 0x06
    AUTOMATIC_GAIN_CONTROL    = 0x07
    DELAY_CONTROL             = 0x08
    BASS_BOOST_CONTROL        = 0x09
    LOUDNESS_CONTROL          = 0x0A


class UpDownMixProcessingUnitControlSelectors(IntEnum):
    # As defined in [Audio10], Table A-12
    UD_CONTROL_UNDEFINED   = 0x00
    UD_ENABLE_CONTROL      = 0x01
    UD_MODE_SELECT_CONTROL = 0x02


class DolbyProLogicProcessingUnitControlSelectors(IntEnum):
    # As defined in [Audio10], Table A-13
    DP_CONTROL_UNDEFINED   = 0x00
    DP_ENABLE_CONTROL      = 0x01
    DP_MODE_SELECT_CONTROL = 0x02


class _3DStereoExtenderProcessingUnitControlSelectors(IntEnum):
    # As defined in [Audio10], Table A-14
    _3D_CONTROL_UNDEFINED = 0x00
    _3D_ENABLE_CONTROL    = 0x01
    SPACIOUSNESS_CONTROL  = 0x02


class ReverberationProcessingUnitControlSelectors(IntEnum):
    # As defined in [Audio10], Table A-15
    RV_CONTROL_UNDEFINED    = 0x00
    RV_ENABLE_CONTROL       = 0x01
    REVERB_LEVEL_CONTROL    = 0x02
    REVERB_TIME_CONTROL     = 0x03
    REVERB_FEEDBACK_CONTROL = 0x04


class ChorusProcessingUnitControlSelectors(IntEnum):
    # As defined in [Audio10], Table A-16
    CH_CONTROL_UNDEFINED = 0x00
    CH_ENABLE_CONTROL    = 0x01
    CHORUS_LEVEL_CONTROL = 0x02
    CHORUS_RATE_CONTROL  = 0x03
    CHORUS_DEPTH_CONTROL = 0x04


class DynamicRangeCompressorProcessingUnitControlSelectors(IntEnum):
    # As defined in [Audio10], Table A-17
    DR_CONTROL_UNDEFINED     = 0x00
    DR_ENABLE_CONTROL        = 0x01
    COMPRESSION_RATE_CONTROL = 0x02
    MAXAMPL_CONTROL          = 0x03
    THRESHOLD_CONTROL        = 0x04
    ATTACK_TIME              = 0x05
    RELEASE_TIME             = 0x06


class ExtensionUnitControlSelectors(IntEnum):
    # As defined in [Audio10], Table A-18
    XU_CONTROL_UNDEFINED     = 0x00
    XU_ENABLE_CONTROL        = 0x01


class EndpointsControlSelectors(IntEnum):
    # As defined in [Audio10], Table A-19
    EP_CONTROL_UNDEFINED  = 0x00
    SAMPLING_FREQ_CONTROL = 0x01
    PITCH_CONTROL         = 0x02


class USBTerminalTypes(IntEnum):
    # As defined in [TermT10], Table 2-1
    USB_UNDEFINED       = 0x0100
    USB_STREAMING       = 0x0101
    USB_VENDOR_SPECIFIC = 0x01FF


class InputTerminalTypes(IntEnum):
    # As defined in [TermT10], Table 2-2
    INPUT_UNDEFINED             = 0x0200
    MICROPHONE                  = 0x0201
    DESKTOP_MICROPHONE          = 0x0202
    PERSONAL_MICROPHONE         = 0x0203
    OMNI_DIRECTIONAL_MICROPHONE = 0x0204
    MICROPHONE_ARRAY            = 0x0205
    PROCESSING_MICROPHONE_ARRAY = 0x0206


class OutputTerminalTypes(IntEnum):
    # As defined in [TermT10], Table 2-3
    OUTPUT_UNDEFINED              = 0x0300
    SPEAKER                       = 0x0301
    HEADPHONES                    = 0x0302
    DESKTOP_SPEAKER               = 0x0304
    ROOM_SPEAKER                  = 0x0305
    COMMUNICATION_SPEAKER         = 0x0306
    LOW_FREQUENCY_EFFECTS_SPEAKER = 0x0307


class BidirectionalTerminalTypes(IntEnum):
    # As defined in [TermT10], Table 2-4
    BIDIRECTIONAL_UNDEFINED       = 0x0400
    HANDSET                       = 0x0401
    HEADSET                       = 0x0402
    ECHO_SUPPRESSING_SPEAKERPHONE = 0x0404
    ECHO_CANCELING_SPEAKERPHONE   = 0x0405


class TelephonyTerminalTypes(IntEnum):
    # As defined in [TermT10], Table 2-5
    TELEPHONY_UNDEFINED = 0x0500
    PHONE_LINE          = 0x0501
    TELEPHONE           = 0x0502
    DOWN_LINE_PHONE     = 0x0503


class ExternalTerminalTypes(IntEnum):
    # As defined in [TermT10], Table 2-6
    EXTERNAL_UNDEFINED             = 0x0600
    ANALOG_CONNECTOR               = 0x0601
    DIGITAL_AUDIO_INTERFACE        = 0x0602
    LINE_CONNECTOR                 = 0x0603
    SPDIF_INTERFACE                = 0x0605
    IEEE_1394_DA_STREAM            = 0x0606
    IEEE_1394_DV_STREAM_SOUNDTRACK = 0x0607


class EmbeddedFunctionTerminalTypes(IntEnum):
    # As defined in [TermT10], Table 2-7
    EMBEDDED_UNDEFINED       = 0x0700
    EQUALIZATION_NOISE       = 0x0702
    CD_PLAYER                = 0x0703
    DAT                      = 0x0704
    DCC                      = 0x0705
    ANALOG_TAPE              = 0x0707
    PHONOGRAPH               = 0x0708
    VCR_AUDIO                = 0x0709
    VIDEO_DISC_AUDIO         = 0x070A
    DVD_AUDIO                = 0x070B
    TV_TUNER_AUDIO           = 0x070C
    SATELLITE_RECEIVER_AUDIO = 0x070D
    CABLE_TUNER_AUDIO        = 0x070E
    DSS_AUDIO                = 0x070F
    RADIO_RECEIVER           = 0x0710
    RADIO_TRANSMITTER        = 0x0711
    MULTI_TRACK_RECORDER     = 0x0712
    SYNTHESIZER              = 0x0713


# As defined in [Audio10], Table 4-17
AudioControlInterruptEndpointDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(9, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificDescriptorTypes.CS_ENDPOINT),
    "bEndpointAddress"    / DescriptorField(description="The address of the endpoint, use USBDirection.*.from_endpoint_address()"),
    "bmAttributes"        / DescriptorField(description="D1..0: Transfer type (0b11 = Interrupt)", default=0b11),
    "wMaxPacketSize"      / DescriptorField(description="Maximum packet size this endpoint is capable of. Used here to pass 6-byte interrupt information.", default=6),
    "bInterval"           / DescriptorField(description="Interval for polling the Interrupt endpoint"),
    "bRefresh"            / DescriptorField(description="Reset to 0"),
    "bSynchAddress"       / DescriptorField(description="Reset to 0"),
)

