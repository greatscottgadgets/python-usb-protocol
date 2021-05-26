#
# This file is part of usb-protocol.
#
"""
    Descriptors for USB Audio Class Devices (UAC), Release 2

    [Audio20]  refers to "Universal Serial Bus Device Class Definition for Audio Devices", Release 2.0, May 31, 2006
    [Frmts20] refers to "Universal Serial Bus Device Class Definition for Audio Data Formats", Release 2.0, May 31, 2006
    [TermT20] refers to "Universal Serial Bus Device Class Definition for Terminal Types", Release 2.0, May 31, 2006

    NOTE: This is not complete yet and will be extended as needed
"""

import unittest
from usb_protocol.emitters import descriptor
from enum                  import IntEnum

import construct

from .standard import StandardDescriptorNumbers
from ..descriptor import \
    DescriptorField, DescriptorNumber, DescriptorFormat, DescriptorLength


class AudioInterfaceClassCode(IntEnum):
    # As defined in [Audio20], Table A-4
    AUDIO = 0x01


class AudioFunctionClassCode(IntEnum):
    # As defined in [Audio20], Table A-1
    AUDIO_FUNCTION = AudioInterfaceClassCode.AUDIO


class AudioFunctionSubclassCodes(IntEnum):
    # As defined in [Audio20], Table A-2
    FUNCTION_SUBCLASS_UNDEFINED = 0x00


class AudioInterfaceProtocolCodes(IntEnum):
    # As defined in [Audio20], Table A-6
    INTERFACE_PROTOCOL_UNDEFINED = 0x00
    IP_VERSION_02_00             = 0x20


class AudioFunctionProtocolCodes(IntEnum):
    # As defined in [Audio20], Table A-3
    FUNCTION_PROTOCOL_UNDEFINED = 0x00
    AF_VERSION_02_00 = AudioInterfaceProtocolCodes.IP_VERSION_02_00


class AudioInterfaceSubclassCodes(IntEnum):
    # As defined in [Audio20], Table A-5
    INTERFACE_SUBCLASS_UNDEFINED = 0x00
    AUDIO_CONTROL                = 0x01
    AUDIO_STREAMING              = 0x02
    MIDI_STREAMING               = 0x03


class AudioFunctionCategoryCodes(IntEnum):
    # As defined in [Audio20], Table A-7
    FUNCTION_SUBCLASS_UNDEFINED = 0x00
    DESKTOP_SPEAKER             = 0x01
    HOME_THEATER                = 0x02
    MICROPHONE                  = 0x03
    HEADSET                     = 0x04
    TELEPHONE                   = 0x05
    CONVERTER                   = 0x06
    VOICE_SOUND_RECORDER        = 0x07
    IO_BOX                      = 0x08
    MUSICAL_INSTRUMENT          = 0x09
    PRO_AUDIO                   = 0x0A
    AUDIO_VIDEO                 = 0x0B
    CONTROL_PANEL               = 0x0C
    OTHER                       = 0xFF


class AudioClassSpecificStandardDescriptorNumbers(IntEnum):
    # As defined in [Audio20], Table A-8
    CS_UNDEFINED     = 0x20
    CS_DEVICE        = 0x21
    CS_CONFIGURATION = 0x22
    CS_STRING        = 0x23
    CS_INTERFACE     = 0x24
    CS_ENDPOINT      = 0x25


class AudioClassSpecificACInterfaceDescriptorSubtypes(IntEnum):
    # As defined in [Audio20], Table A-9
    AC_DESCRIPTOR_UNDEFINED  = 0x00
    HEADER                   = 0x01
    INPUT_TERMINAL           = 0x02
    OUTPUT_TERMINAL          = 0x03
    MIXER_UNIT               = 0x04
    SELECTOR_UNIT            = 0x05
    FEATURE_UNIT             = 0x06
    EFFECT_UNIT              = 0x07
    PROCESSING_UNIT          = 0x08
    EXTENSION_UNIT           = 0x09
    CLOCK_SOURCE             = 0x0A
    CLOCK_SELECTOR           = 0x0B
    CLOCK_MULTIPLIER         = 0x0C
    SAMPLE_RATE_CONVERTER    = 0x0D


class AudioClassSpecificASInterfaceDescriptorSubtypes(IntEnum):
    # As defined in [Audio20], Table A-10
    AS_DESCRIPTOR_UNDEFINED = 0x00
    AS_GENERAL              = 0x01
    FORMAT_TYPE             = 0x02
    ENCODER                 = 0x03
    DECODER                 = 0x04


class EffectUnitEffectTypes(IntEnum):
    # As defined in [Audio20], Table A-11
    EFFECT_UNDEFINED        = 0x00
    PARAM_EQ_SECTION_EFFECT = 0x01
    REVERBERATION_EFFECT    = 0x02
    MOD_DELAY_EFFECT        = 0x03
    DYN_RANGE_COMP_EFFECT   = 0x04


class ProcessingUnitProcessTypes(IntEnum):
    # As defined in [Audio20], Table A-12
    PROCESS_UNDEFINED       = 0x00
    UP_DOWNMIX_PROCESS      = 0x01
    DOLBY_PROLOGIC_PROCESS  = 0x02
    STEREO_EXTENDER_PROCESS = 0x03


class AudioClassSpecificEndpointDescriptorSubtypes(IntEnum):
    # As defined in [Audio20], Table A-13
    DESCRIPTOR_UNDEFINED = 0x00
    EP_GENERAL           = 0x01


class AudioClassSpecificRequestCodes(IntEnum):
    # As defined in [Audio20], Table A-14
    REQUEST_CODE_UNDEFINED = 0x00
    CUR                    = 0x01
    RANGE                  = 0x02
    MEM                    = 0x03


class ClockSourceControlSelectors(IntEnum):
    # As defined in [Audio20], Table A-17
    CS_CONTROL_UNDEFINED   = 0x00
    CS_SAM_FREQ_CONTROL    = 0x01
    CS_CLOCK_VALID_CONTROL = 0x02


class ClockSelectorControlSelectors(IntEnum):
    # As defined in [Audio20], Table A-18
    CX_CONTROL_UNDEFINED      = 0x00
    CX_CLOCK_SELECTOR_CONTROL = 0x01


class ClockMultiplierControlSelectors(IntEnum):
    # As defined in [Audio20], Table A-19
    CM_CONTROL_UNDEFINED   = 0x00
    CM_NUMERATOR_CONTROL   = 0x01
    CM_DENOMINATOR_CONTROL = 0x02


class TerminalControlSelectors(IntEnum):
    # As defined in [Audio20], Table A-20
    TE_CONTROL_UNDEFINED    = 0x00
    TE_COPY_PROTECT_CONTROL = 0x01
    TE_CONNECTOR_CONTROL    = 0x02
    TE_OVERLOAD_CONTROL     = 0x03
    TE_CLUSTER_CONTROL      = 0x04
    TE_UNDERFLOW_CONTROL    = 0x05
    TE_OVERFLOW_CONTROL     = 0x06
    TE_LATENCY_CONTROL      = 0x07


class MixerControlSelectors(IntEnum):
    # As defined in [Audio20], Table A-21
    MU_CONTROL_UNDEFINED = 0x00
    MU_MIXER_CONTROL     = 0x01
    MU_CLUSTER_CONTROL   = 0x02
    MU_UNDERFLOW_CONTROL = 0x03
    MU_OVERFLOW_CONTROL  = 0x04
    MU_LATENCY_CONTROL   = 0x05


class SelectorControlSelectors(IntEnum):
    # As defined in [Audio20], Table A-22
    SU_CONTROL_UNDEFINED = 0x00
    SU_SELECTOR_CONTROL  = 0x01
    SU_LATENCY_CONTROL   = 0x02


class FeatureUnitControlSelectors(IntEnum):
    # As defined in [Audio20], Table A-23
    FU_CONTROL_UNDEFINED         = 0x00
    FU_MUTE_CONTROL              = 0x01
    FU_VOLUME_CONTROL            = 0x02
    FU_BASS_CONTROL              = 0x03
    FU_MID_CONTROL               = 0x04
    FU_TREBLE_CONTROL            = 0x05
    FU_GRAPHIC_EQUALIZER_CONTROL = 0x06
    FU_AUTOMATIC_GAIN_CONTROL    = 0x07
    FU_DELAY_CONTROL             = 0x08
    FU_BASS_BOOST_CONTROL        = 0x09
    FU_LOUDNESS_CONTROL          = 0x0A
    FU_INPUT_GAIN_CONTROL        = 0x0B
    FU_INPUT_GAIN_PAD_CONTROL    = 0x0C
    FU_PHASE_INVERTER_CONTROL    = 0x0D
    FU_UNDERFLOW_CONTROL         = 0x0E
    FU_OVERFLOW_CONTROL          = 0x0F
    FU_LATENCY_CONTROL           = 0x10


class ParametricEqualizerSectionEffectUnitControlSelectors(IntEnum):
    # As defined in [Audio20], Table A-24
    PE_CONTROL_UNDEFINED  = 0x00
    PE_ENABLE_CONTROL     = 0x01
    PE_CENTERFREQ_CONTROL = 0x02
    PE_QFACTOR_CONTROL    = 0x03
    PE_GAIN_CONTROL       = 0x04
    PE_UNDERFLOW_CONTROL  = 0x05
    PE_OVERFLOW_CONTROL   = 0x06
    PE_LATENCY_CONTROL    = 0x07


class ReverberationEffectUnitControlSelectors(IntEnum):
    # As defined in [Audio20], Table A-25
    RV_CONTROL_UNDEFINED      = 0x00
    RV_ENABLE_CONTROL         = 0x01
    RV_TYPE_CONTROL           = 0x02
    RV_LEVEL_CONTROL          = 0x03
    RV_TIME_CONTROL           = 0x04
    RV_FEEDBACK_CONTROL       = 0x05
    RV_PREDELAY_CONTROL       = 0x06
    RV_DENSITY_CONTROL        = 0x07
    RV_HIFREQ_ROLLOFF_CONTROL = 0x08
    RV_UNDERFLOW_CONTROL      = 0x09
    RV_OVERFLOW_CONTROL       = 0x0A
    RV_LATENCY_CONTROL        = 0x0B


class ModulationDelayEffectUnitControlSelectors(IntEnum):
    # As defined in [Audio20], Table A-26
    MD_CONTROL_UNDEFINED = 0x00
    MD_ENABLE_CONTROL    = 0x01
    MD_BALANCE_CONTROL   = 0x02
    MD_RATE_CONTROL      = 0x03
    MD_DEPTH_CONTROL     = 0x04
    MD_TIME_CONTROL      = 0x05
    MD_FEEDBACK_CONTROL  = 0x06
    MD_UNDERFLOW_CONTROL = 0x07
    MD_OVERFLOW_CONTROL  = 0x08
    MD_LATENCY_CONTROL   = 0x09


class DynamicRangeCompressorEffectUnitControlSelectors(IntEnum):
    # As defined in [Audio20], Table A-27
    DR_CONTROL_UNDEFINED        = 0x00
    DR_ENABLE_CONTROL           = 0x01
    DR_COMPRESSION_RATE_CONTROL = 0x02
    DR_MAXAMPL_CONTROL          = 0x03
    DR_THRESHOLD_CONTROL        = 0x04
    DR_ATTACK_TIME_CONTROL      = 0x05
    DR_RELEASE_TIME_CONTROL     = 0x06
    DR_UNDERFLOW_CONTROL        = 0x07
    DR_OVERFLOW_CONTROL         = 0x08
    DR_LATENCY_CONTROL          = 0x09


class UpDownMixProcessingUnitControlSelectors(IntEnum):
    # As defined in [Audio20], Table A-28
    UD_CONTROL_UNDEFINED   = 0x00
    UD_ENABLE_CONTROL      = 0x01
    UD_MODE_SELECT_CONTROL = 0x02
    UD_CLUSTER_CONTROL     = 0x03
    UD_UNDERFLOW_CONTROL   = 0x04
    UD_OVERFLOW_CONTROL    = 0x05
    UD_LATENCY_CONTROL     = 0x06


class DolbyProLogicProcessingUnitControlSelectors(IntEnum):
    # As defined in [Audio20], Table A-29
    DP_CONTROL_UNDEFINED   = 0x00
    DP_ENABLE_CONTROL      = 0x01
    DP_MODE_SELECT_CONTROL = 0x02
    DP_CLUSTER_CONTROL     = 0x03
    DP_UNDERFLOW_CONTROL   = 0x04
    DP_OVERFLOW_CONTROL    = 0x05
    DP_LATENCY_CONTROL     = 0x06


class StereoExtenderProcessingUnitControlSelectors(IntEnum):
    # As defined in [Audio20], Table A-30
    ST_EXT_CONTROL_UNDEFINED = 0x00
    ST_EXT_ENABLE_CONTROL    = 0x01
    ST_EXT_UNDERFLOW_CONTROL = 0x03
    ST_EXT_OVERFLOW_CONTROL  = 0x04
    ST_EXT_LATENCY_CONTROL   = 0x05


class ExtensionUnitControlSelectors(IntEnum):
    # As defined in [Audio20], Table A-31
    XU_CONTROL_UNDEFINED = 0x00
    XU_ENABLE_CONTROL    = 0x01
    XU_CLUSTER_CONTROL   = 0x02
    XU_UNDERFLOW_CONTROL = 0x03
    XU_OVERFLOW_CONTROL  = 0x04
    XU_LATENCY_CONTROL   = 0x05


class AudioStreamingInterfaceControlSelectors(IntEnum):
    # As defined in [Audio20], Table A-32
    AS_CONTROL_UNDEFINED         = 0x00
    AS_ACT_ALT_SETTING_CONTROL   = 0x01
    AS_VAL_ALT_SETTINGS_CONTROL  = 0x02
    AS_AUDIO_DATA_FORMAT_CONTROL = 0x03


class EndpointControlSelectors(IntEnum):
    # As defined in [Audio20], Table A-33
    EP_CONTROL_UNDEFINED     = 0x00
    EN_BIT_RATE_CONTROL      = 0x01
    EN_QUALITY_CONTROL       = 0x02
    EN_VBR_CONTROL           = 0x03
    EN_TYPE_CONTROL          = 0x04
    EN_UNDERFLOW_CONTROL     = 0x05
    EN_OVERFLOW_CONTROL      = 0x06
    EN_ENCODER_ERROR_CONTROL = 0x07
    EN_PARAM1_CONTROL        = 0x08
    EN_PARAM2_CONTROL        = 0x09
    EN_PARAM3_CONTROL        = 0x0A
    EN_PARAM4_CONTROL        = 0x0B
    EN_PARAM5_CONTROL        = 0x0C
    EN_PARAM6_CONTROL        = 0x0D
    EN_PARAM7_CONTROL        = 0x0E
    EN_PARAM8_CONTROL        = 0x0F


class USBTerminalTypes(IntEnum):
    # As defined in [TermT20], Table 2-1
    USB_UNDEFINED       = 0x0100
    USB_STREAMING       = 0x0101
    USB_VENDOR_SPECIFIC = 0x01FF


class InputTerminalTypes(IntEnum):
    # As defined in [TermT20], Table 2-2
    INPUT_UNDEFINED             = 0x0200
    MICROPHONE                  = 0x0201
    DESKTOP_MICROPHONE          = 0x0202
    PERSONAL_MICROPHONE         = 0x0203
    OMNI_DIRECTIONAL_MICROPHONE = 0x0204
    MICROPHONE_ARRAY            = 0x0205
    PROCESSING_MICROPHONE_ARRAY = 0x0206


class OutputTerminalTypes(IntEnum):
    # As defined in [TermT20], Table 2-3
    OUTPUT_UNDEFINED              = 0x0300
    SPEAKER                       = 0x0301
    HEADPHONES                    = 0x0302
    DESKTOP_SPEAKER               = 0x0304
    ROOM_SPEAKER                  = 0x0305
    COMMUNICATION_SPEAKER         = 0x0306
    LOW_FREQUENCY_EFFECTS_SPEAKER = 0x0307


class BidirectionalTerminalTypes(IntEnum):
    # As defined in [TermT20], Table 2-4
    BIDIRECTIONAL_UNDEFINED       = 0x0400
    HANDSET                       = 0x0401
    HEADSET                       = 0x0402
    ECHO_SUPPRESSING_SPEAKERPHONE = 0x0404
    ECHO_CANCELING_SPEAKERPHONE   = 0x0405


class TelephonyTerminalTypes(IntEnum):
    # As defined in [TermT20], Table 2-5
    TELEPHONY_UNDEFINED = 0x0500
    PHONE_LINE          = 0x0501
    TELEPHONE           = 0x0502
    DOWN_LINE_PHONE     = 0x0503


class ExternalTerminalTypes(IntEnum):
    # As defined in [TermT20], Table 2-6
    EXTERNAL_UNDEFINED             = 0x0600
    ANALOG_CONNECTOR               = 0x0601
    DIGITAL_AUDIO_INTERFACE        = 0x0602
    LINE_CONNECTOR                 = 0x0603
    SPDIF_INTERFACE                = 0x0605
    IEEE_1394_DA_STREAM            = 0x0606
    IEEE_1394_DV_STREAM_SOUNDTRACK = 0x0607
    ADAT_LIGHTPIPE                 = 0x0608
    TDIF                           = 0x0609
    MADI                           = 0x060A


class EmbeddedFunctionTerminalTypes(IntEnum):
    # As defined in [TermT20], Table 2-7
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
    PIANO                    = 0x0714
    GUITAR                   = 0x0715
    DRUMS_RHYTHM             = 0x0716
    OTHER_MUSICAL_INSTRUMENT = 0x0717


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


# As defined in [Audio20], Table 4-25
AudioControlInterruptEndpointDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(7, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificStandardDescriptorNumbers.CS_ENDPOINT),
    "bEndpointAddress"    / DescriptorField(description="The address of the endpoint, use USBDirection.*.from_endpoint_address()"),
    "bmAttributes"        / DescriptorField(description="D1..0: Transfer type (0b11 = Interrupt)", default=0b11),
    "wMaxPacketSize"      / DescriptorField(description="Maximum packet size this endpoint is capable of. Used here to pass 6-byte interrupt information.", default=6),
    "bInterval"           / DescriptorField(description="Interval for polling the Interrupt endpoint")
)

# As defined in [Audio30], Table 4-33
AudioStreamingIsochronousEndpointDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(7, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(StandardDescriptorNumbers.ENDPOINT),
    "bEndpointAddress"    / DescriptorField(description="The address of the endpoint, use USBDirection.*.from_endpoint_address()"),
    "bmAttributes"        / DescriptorField(description="D1..0: transfer type (01=isochronous); D3..2: synchronization type (01=asynchronous/10=adaptive/11=synchronous); D5..4: usage (00=data/10=feedback)", default=0b000101),
    "wMaxPacketSize"      / DescriptorField(description="Maximum packet size this endpoint is capable of. Used here to pass 6-byte interrupt information.", default=6),
    "bInterval"           / DescriptorField(description="Interval for polling the Interrupt endpoint")
)

# As defined in [Audio30], Table 4-35
AudioStreamingIsochronousFeedbackEndpointDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(7, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(StandardDescriptorNumbers.ENDPOINT),
    "bEndpointAddress"    / DescriptorField(description="The address of the endpoint, use USBDirection.*.from_endpoint_address()"),
    "bmAttributes"        / DescriptorField(description="D1..0: transfer type (01=isochronous); D3..2: synchronization type (00=no sync); D5..4: usage (10=feedback)", default=0b00100001),
    "wMaxPacketSize"      / DescriptorField(description="Maximum packet size this endpoint is capable of. Used here to pass 6-byte interrupt information.", default=6),
    "bInterval"           / DescriptorField(description="Interval for polling the Interrupt endpoint")
)

InterfaceAssociationDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(8, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(StandardDescriptorNumbers.INTERFACE_ASSOCIATION),
    "bFirstInterface"     / DescriptorField(description="Interface number of the first interface that is associated with this function.", default=0),
    "bInterfaceCount"     / DescriptorField(description="Number of contiguous interfaces that are associated with this function"),
    "bFunctionClass"      / DescriptorNumber(AudioFunctionClassCode.AUDIO_FUNCTION),
    "bFunctionSubClass"   / DescriptorField(description="function subclass code (currently not used in uac2)", default=AudioFunctionCategoryCodes.FUNCTION_SUBCLASS_UNDEFINED), 
    "bFunctionProtocol"   / DescriptorNumber(AudioFunctionProtocolCodes.AF_VERSION_02_00),
    "iFunction"           / DescriptorField(description="Index of a string descriptor that describes this interface", default=0),
)

StandardAudioControlInterfaceDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(9, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(StandardDescriptorNumbers.INTERFACE),
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
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificStandardDescriptorNumbers.CS_INTERFACE),
    "bDescriptorSubtype"  / DescriptorNumber(AudioClassSpecificACInterfaceDescriptorSubtypes.HEADER),
    "bcdADC"              / DescriptorField(description="Audio Device Class specification release version", default=2.0),
    "bCategory"           / DescriptorField(description="primary use of this audio function (see AudioFunctionCategoryCodes)", default=AudioFunctionCategoryCodes.IO_BOX),
    "wTotalLength"        / DescriptorField(description="total number of bytes for the class specific audio control interface descriptor; Includes the combined length of this descriptor header and all Clock Source, Unit and Terminal descriptors"),
    "bmControls"          / DescriptorField(description="D1..0: latency control", default=0),
)

ClockSourceDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(8, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificStandardDescriptorNumbers.CS_INTERFACE),
    "bDescriptorSubtype"  / DescriptorNumber(AudioClassSpecificACInterfaceDescriptorSubtypes.CLOCK_SOURCE),
    "bClockID"            / DescriptorField(description="ID of the clock source entity within the audio function (used in requests)"),
    "bmAttributes"        / DescriptorField(description="D1..0: clock type (see ClockAttributs)"),
    "bmControls"          / DescriptorField(description="D1..0: clock frequency control (D0..1: See ClockFrequencyControl, D3..2: clock validity control (0))", default=ClockFrequencyControl.NOT_PRESENT),
    "bAssocTerminal"      / DescriptorField(description="ID of the terminal which is associated with this clock", default=0),
    "iClockSource"        / DescriptorField(description="index of the string description of this clock source", default=0),
)

InputTerminalDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(17, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificStandardDescriptorNumbers.CS_INTERFACE),
    "bDescriptorSubtype"  / DescriptorNumber(AudioClassSpecificACInterfaceDescriptorSubtypes.INPUT_TERMINAL),
    "bTerminalID"         / DescriptorField(description="unique identifier for the terminal within the audio function (used in requests)"),
    "wTerminalType"       / DescriptorField(description="a value of one of the terminal types Enums (eg InputTerminaTypes, ExternalTerminalTypes)"),
    "bAssocTerminal"      / DescriptorField(description="ID of the associated output terminal", default=0),
    "bCSourceID"          / DescriptorField(description="ID of the clock which is connected to this terminal"),
    "bNrChannels"         / DescriptorField(description="number of logical output channels in the terminal’s output channel cluster"),
    "bmChannelConfig"     / DescriptorField(description="describes the spatial location of the logical channels", default=0, length=4),
    "iChannelNames"       / DescriptorField(description="string descriptor index of the first logical channel name", default=0),
    "bmControls"          / DescriptorField(description="OR combination of  ClockFrequencyControl, CopyProtectControl, ConnectorControl, ClusterControl, UnderflowControl and OverflowControl", default=0, length=2),
    "iTerminal"           / DescriptorField(description="ID of the input terminal string descriptor", default=0)
)

OutputTerminalDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(12, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificStandardDescriptorNumbers.CS_INTERFACE),
    "bDescriptorSubtype"  / DescriptorNumber(AudioClassSpecificACInterfaceDescriptorSubtypes.OUTPUT_TERMINAL),
    "bTerminalID"         / DescriptorField(description="unique identifier for the terminal within the audio function."),
    "wTerminalType"       / DescriptorField(description="a value of one of the terminal types Enums (eg OutputTerminaTypes, ExternalTerminalTypes)"),
    "bAssocTerminal"      / DescriptorField(description="ID of the associated input terminal", default=0),
    "bSourceID"           / DescriptorField(description="ID of the unit or terminal which is connected to this terminal"),
    "bCSourceID"          / DescriptorField(description="ID of the clock which is connected to this terminal"),
    "bmControls"          / DescriptorField(description="OR combination of  ClockFrequencyControl, CopyProtectControl, ConnectorControl, UnderflowControl>>2 and OverflowControl>>2", default=0, length=2),
    "iTerminal"           / DescriptorField(description="ID of the input terminal string descriptor", default=0)
)

FeatureUnitDescriptorLength = construct.Rebuild(construct.Int8ul, construct.len_(construct.this.bmaControls) * 4 + 6)

FeatureUnitDescriptor = DescriptorFormat(
    "bLength"             / FeatureUnitDescriptorLength,
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificStandardDescriptorNumbers.CS_INTERFACE),
    "bDescriptorSubtype"  / DescriptorNumber(AudioClassSpecificACInterfaceDescriptorSubtypes.FEATURE_UNIT),
    "bUnitID"             / DescriptorField(description="unique identifier for the unit within the audio function."),
    "bSourceID"           / DescriptorField(description="ID of the unit or terminal which is connected to this terminal"),
    "bmaControls"         / construct.Array((construct.this.bLength - 6)//4, construct.Int32ul) * "The control bitmap for all channels",
    "iFeature"            / DescriptorField(description="ID of the feature unit string descriptor", default=0)
)

AudioStreamingInterfaceDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(9, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(StandardDescriptorNumbers.INTERFACE),
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
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificStandardDescriptorNumbers.CS_INTERFACE),
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
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificStandardDescriptorNumbers.CS_INTERFACE),
    "bDescriptorSubtype"  / DescriptorNumber(AudioClassSpecificASInterfaceDescriptorSubtypes.FORMAT_TYPE),
    "bFormatType"         / DescriptorNumber(FormatTypes.FORMAT_TYPE_I),
    "bSubslotSize"        / DescriptorField(description="number of bytes occupied by one audio subslot (1, 2, 3 or 4)"),
    "bBitResolution"      / DescriptorField(description="number of effectively used bits out of the available bits in an audio subslot")
)

ExtendedTypeIFormatTypeDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(9, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificStandardDescriptorNumbers.CS_INTERFACE),
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
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificStandardDescriptorNumbers.CS_INTERFACE),
    "bDescriptorSubtype"  / DescriptorNumber(AudioClassSpecificASInterfaceDescriptorSubtypes.FORMAT_TYPE),
    "bFormatType"         / DescriptorNumber(FormatTypes.FORMAT_TYPE_II),
    "wMaxBitRate"         / DescriptorField(description="maximum bitrate of this interface in kbits/s"),
    "wSlotsPerFrame"      / DescriptorField(description="number of PCM audio slots in one audio frame")
)

ExtendedTypeIIFormatTypeDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(10, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificStandardDescriptorNumbers.CS_INTERFACE),
    "bDescriptorSubtype"  / DescriptorNumber(AudioClassSpecificASInterfaceDescriptorSubtypes.FORMAT_TYPE),
    "bFormatType"         / DescriptorNumber(FormatTypes.EXT_FORMAT_TYPE_II),
    "wMaxBitRate"         / DescriptorField(description="maximum bitrate of this interface in kbits/s"),
    "wSamplesPerFrame"    / DescriptorField(description="number of PCM audio samples in one audio frame"),
    "bHeaderLength"       / DescriptorField(description="size of the packet header in bytes"),
    "bSideBandProtocol"   / DescriptorField(description="side band protocol, see SidebandProtocols", default=SidebandProtocols.PROTOCOL_UNDEFINED)
)

TypeIIIFormatTypeDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(6, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificStandardDescriptorNumbers.CS_INTERFACE),
    "bDescriptorSubtype"  / DescriptorNumber(AudioClassSpecificASInterfaceDescriptorSubtypes.FORMAT_TYPE),
    "bFormatType"         / DescriptorNumber(FormatTypes.FORMAT_TYPE_III),
    "bSubslotSize"        / DescriptorField(description="number of bytes occupied by one audio subslot (must be 2)", default=2),
    "bBitResolution"      / DescriptorField(description="number of effectively used bits out of the available bits in an audio subslot"),
)

ExtendedTypeIIIFormatTypeDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(8, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificStandardDescriptorNumbers.CS_INTERFACE),
    "bDescriptorSubtype"  / DescriptorNumber(AudioClassSpecificASInterfaceDescriptorSubtypes.FORMAT_TYPE),
    "bFormatType"         / DescriptorNumber(FormatTypes.EXT_FORMAT_TYPE_III),
    "bSubslotSize"        / DescriptorField(description="number of bytes occupied by one audio subslot (must be 2)", default=2),
    "bBitResolution"      / DescriptorField(description="number of effectively used bits out of the available bits in an audio subslot"),
    "bHeaderLength"       / DescriptorField(description="size of the packet header in bytes"),
    "bSideBandProtocol"   / DescriptorField(description="side band protocol, see SidebandProtocols", default=SidebandProtocols.PROTOCOL_UNDEFINED)
)

ClassSpecificAudioStreamingIsochronousAudioDataEndpointDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(8, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificStandardDescriptorNumbers.CS_ENDPOINT),
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
        self.assertEqual(parsed.bDescriptorType, StandardDescriptorNumbers.INTERFACE_ASSOCIATION)
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
        self.assertEqual(parsed.bDescriptorType, StandardDescriptorNumbers.INTERFACE)
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
