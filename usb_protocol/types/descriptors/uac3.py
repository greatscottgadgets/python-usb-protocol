#
# This file is part of usb-protocol.
#
"""
    Descriptors for USB Audio Class Devices (UAC), Release 3

    [Audio30] refers to "Universal Serial Bus Device Class Definition for Audio Devices", Release 3.0, September 22, 2016
    [Frmts30] refers to "Universal Serial Bus Device Class Definition for Audio Data Formats", Release 3.0, September 22, 2016
    [TermT30] refers to "Universal Serial Bus Device Class Definition for Terminal Types", Release 3.0, May 31, 2006

    NOTE: This is not complete yet and will be extended as needed
"""

from build.lib.usb_protocol.emitters import descriptor
import unittest
from enum import IntEnum

import construct
from   construct  import this, Default

from .. import LanguageIDs
from .standard import StandardDescriptorNumbers
from ..descriptor import \
    DescriptorField, DescriptorNumber, DescriptorFormat, \
    BCDFieldAdapter, DescriptorLength


class AudioInterfaceClassCode(IntEnum):
    # As defined in [Audio30], Table A-4
    AUDIO = 0x01


class AudioFunctionClassCode(IntEnum):
    # As defined in [Audio30], Table A-1
    AUDIO_FUNCTION = AudioInterfaceClassCode.AUDIO


class AudioFunctionSubclassCodes(IntEnum):
    # As defined in [Audio30], Table A-2
    FUNCTION_SUBCLASS_UNDEFINED = 0x00
    FULL_ADC_3_0                = 0x01
    GENERIC_IO                  = 0x20
    HEADPHONE                   = 0x21
    SPEAKER                     = 0x22
    MICROPHONE                  = 0x23
    HEADSET                     = 0x24
    HEADSET_ADAPTER             = 0x25
    SPEAKERPHONE                = 0x26


class AudioInterfaceSubclassCodes(IntEnum):
    # As defined in [Audio30], Table A-5
    INTERFACE_SUBCLASS_UNDEFINED = 0x00
    AUDIO_CONTROL                = 0x01
    AUDIO_STREAMING              = 0x02
    MIDI_STREAMING               = 0x03


class AudioInterfaceProtocolCodes(IntEnum):
    # As defined in [Audio30], Table A-6
    IP_VERSION_01_00 = 0x00
    IP_VERSION_02_00 = 0x20
    IP_VERSION_03_00 = 0x30


class AudioFunctionProtocolCodes(IntEnum):
    # As defined in [Audio30], Table A-3
    FUNCTION_PROTOCOL_UNDEFINED = 0x00
    AF_VERSION_01_00 = AudioInterfaceProtocolCodes.IP_VERSION_01_00
    AF_VERSION_02_00 = AudioInterfaceProtocolCodes.IP_VERSION_02_00
    AF_VERSION_03_00 = AudioInterfaceProtocolCodes.IP_VERSION_03_00


class AudioFunctionCategoryCodes(IntEnum):
    # As defined in [Audio30], Table A-7
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
    HEADPHONE                   = 0x0D
    GENERIC_SPEAKER             = 0x0E
    HEADSET_ADAPTER             = 0x0F
    SPEAKERPHONE                = 0x10
    OTHER                       = 0xFF


class AudioClassSpecificStandardDescriptorTypes(IntEnum):
    # As defined in [Audio30], Table A-8
    CS_UNDEFINED     = 0x20
    CS_DEVICE        = 0x21
    CS_CONFIGURATION = 0x22
    CS_STRING        = 0x23
    CS_INTERFACE     = 0x24
    CS_ENDPOINT      = 0x25
    CS_CLUSTER       = 0x26


class ClusterDescriptorSubtypes(IntEnum):
    # As defined in [Audio30], Table A-9
    SUBTYPE_UNDEFINED = 0x00


class ClusterDescriptorSegmentTypes(IntEnum):
    # As defined in [Audio30], Table A-10
    SEGMENT_UNDEFINED      = 0x00
    CLUSTER_DESCRIPTION    = 0x01
    CLUSTER_VENDOR_DEFINED = 0x1F
    CHANNEL_INFORMATION    = 0x20
    CHANNEL_AMBISONIC      = 0x21
    CHANNEL_DESCRIPTION    = 0x22
    CHANNEL_VENDOR_DEFINED = 0xFE
    END_SEGMENT            = 0xFF


class  ChannelPurposeDefinitions(IntEnum):
    # As defined in [Audio30], Table A-11
    PURPOSE_UNDEFINED = 0x00
    GENERIC_AUDIO     = 0x01
    VOICE             = 0x02
    SPEECH            = 0x03
    AMBIENT           = 0x04
    REFERENCE         = 0x05
    ULTRASONIC        = 0x06
    VIBROKINETIC      = 0x07
    NON_AUDIO         = 0xFF


class AmbisonicComponentOrderingConventionTypes(IntEnum):
    # As defined in [Audio30], Table A-13
    ORD_TYPE_UNDEFINED           = 0x00
    AMBISONIC_CHANNEL_NUMBER_ACN = 0x01
    FURSE_MALHAM                 = 0x02
    SINGLE_INDEX_DESIGNATION_SID = 0x03


class AmbisonicNormalizationTypes(IntEnum):
    # As defined in [Audio30], Table A-14
    NORM_TYPE_UNDEFINED = 0x00
    MAX_N               = 0x01
    SN3D                = 0x02
    N3D                 = 0x03
    SN2D                = 0x04
    N2D                 = 0x05


class AudioClassSpecificACInterfaceDescriptorSubtypes(IntEnum):
    # As defined in [Audio30], Table A-15
    AC_DESCRIPTOR_UNDEFINED  = 0x00
    HEADER                   = 0x01
    INPUT_TERMINAL           = 0x02
    OUTPUT_TERMINAL          = 0x03
    EXTENDED_TERMINAL        = 0x04
    MIXER_UNIT               = 0x05
    SELECTOR_UNIT            = 0x06
    FEATURE_UNIT             = 0x07
    EFFECT_UNIT              = 0x08
    PROCESSING_UNIT          = 0x09
    EXTENSION_UNIT           = 0x0A
    CLOCK_SOURCE             = 0x0B
    CLOCK_SELECTOR           = 0x0C
    CLOCK_MULTIPLIER         = 0x0D
    SAMPLE_RATE_CONVERTER    = 0x0E
    CONNECTORS               = 0x0F
    POWER_DOMAIN             = 0x10


class AudioClassSpecificASInterfaceDescriptorSubtypes(IntEnum):
    # As defined in [Audio30], Table A-16
    AS_DESCRIPTOR_UNDEFINED = 0x00
    AS_GENERAL              = 0x01
    AS_VALID_FREQ_RANGE     = 0x02


class AudioClassSpecificStringDescriptorSubtypes(IntEnum):
    # As defined in [Audio30], Table A-17
    SUBTYPE_UNDEFINED = 0x00


class ExtendedTerminalSegmentTypes(IntEnum):
    # As defined in [Audio30], Table A-18
    SEGMENT_UNDEFINED                = 0x00
    TERMINAL_VENDOR_DEFINED          = 0x1F
    CHANNEL_BANDWIDTH                = 0x20
    CHANNEL_MAGNITUDE_RESPONSE       = 0x21
    CHANNEL_MAGNITUDE_PHASE_RESPONSE = 0x22
    CHANNEL_POSITION_XYZ             = 0x23
    CHANNEL_POSITION_R_THETA_PHI     = 0x24
    CHANNEL_VENDOR_DEFINED           = 0xFE
    END_SEGMENT                      = 0xFF


class EffectUnitEffectTypes(IntEnum):
    # As defined in [Audio30], Table A-19
    EFFECT_UNDEFINED        = 0x00
    PARAM_EQ_SECTION_EFFECT = 0x01
    REVERBERATION_EFFECT    = 0x02
    MOD_DELAY_EFFECT        = 0x03
    DYN_RANGE_COMP_EFFECT   = 0x04


class ProcessingUnitProcessTypes(IntEnum):
    # As defined in [Audio30], Table A20
    PROCESS_UNDEFINED       = 0x0000
    UP_DOWNMIX_PROCESS      = 0x0001
    STEREO_EXTENDER_PROCESS = 0x0002
    MULTI_FUNCTION_PROCESS  = 0x0003


class AudioClassSpecificEndpointDescriptorSubtypes(IntEnum):
    # As defined in [Audio30], Table A-21
    DESCRIPTOR_UNDEFINED = 0x00
    EP_GENERAL           = 0x01


class AudioClassSpecificRequestCodes(IntEnum):
    # As defined in [Audio30], Table A-22
    REQUEST_CODE_UNDEFINED     = 0x00
    CUR                        = 0x01
    RANGE                      = 0x02
    MEM                        = 0x03
    INTEN                      = 0x04
    STRING                     = 0x05
    HIGH_CAPABILITY_DESCRIPTOR = 0x06


class AudioControlInterfaceControlSelectors(IntEnum):
    # As defined in [Audio30], Table A-23
    AC_CONTROL_UNDEFINED        = 0x00
    AC_ACTIVE_INTERFACE_CONTROL = 0x01
    AC_POWER_DOMAIN_CONTROL     = 0x02


class ClockSourceControlSelectors(IntEnum):
    # As defined in [Audio30], Table A-24
    CS_CONTROL_UNDEFINED   = 0x00
    CS_SAM_FREQ_CONTROL    = 0x01
    CS_CLOCK_VALID_CONTROL = 0x02


class ClockSelectorControlSelectors(IntEnum):
    # As defined in [Audio30], Table A-24
    CX_CONTROL_UNDEFINED      = 0x00
    CX_CLOCK_SELECTOR_CONTROL = 0x01


class ClockMultiplierControlSelectors(IntEnum):
    # As defined in [Audio30], Table A-26
    CM_CONTROL_UNDEFINED   = 0x00
    CM_NUMERATOR_CONTROL   = 0x01
    CM_DENOMINATOR_CONTROL = 0x02


class TerminalControlSelectors(IntEnum):
    # As defined in [Audio30], Table A-27
    TE_CONTROL_UNDEFINED = 0x00
    TE_INSERTION_CONTROL = 0x01
    TE_OVERLOAD_CONTROL  = 0x02
    TE_UNDERFLOW_CONTROL = 0x03
    TE_OVERFLOW_CONTROL  = 0x04
    TE_LATENCY_CONTROL   = 0x05


class MixerControlSelectors(IntEnum):
    # As defined in [Audio30], Table A-28
    MU_CONTROL_UNDEFINED = 0x00
    MU_MIXER_CONTROL     = 0x01
    MU_UNDERFLOW_CONTROL = 0x02
    MU_OVERFLOW_CONTROL  = 0x03
    MU_LATENCY_CONTROL   = 0x04


class SelectorControlSelectors(IntEnum):
    # As defined in [Audio30], Table A-29
    SU_CONTROL_UNDEFINED = 0x00
    SU_SELECTOR_CONTROL  = 0x01
    SU_LATENCY_CONTROL   = 0x02


class FeatureUnitControlSelectors(IntEnum):
    # As defined in [Audio30], Table A-30
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
    # As defined in [Audio30], Table A-31
    PE_CONTROL_UNDEFINED  = 0x00
    PE_ENABLE_CONTROL     = 0x01
    PE_CENTERFREQ_CONTROL = 0x02
    PE_QFACTOR_CONTROL    = 0x03
    PE_GAIN_CONTROL       = 0x04
    PE_UNDERFLOW_CONTROL  = 0x05
    PE_OVERFLOW_CONTROL   = 0x06
    PE_LATENCY_CONTROL    = 0x07


class ReverberationEffectUnitControlSelectors(IntEnum):
    # As defined in [Audio30], Table A-32
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
    # As defined in [Audio30], Table A-33
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
    # As defined in [Audio30], Table A-34
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
    # As defined in [Audio30], Table A-35
    UD_CONTROL_UNDEFINED   = 0x00
    UD_MODE_SELECT_CONTROL = 0x01
    UD_UNDERFLOW_CONTROL   = 0x02
    UD_OVERFLOW_CONTROL    = 0x03
    UD_LATENCY_CONTROL     = 0x04


class StereoExtenderProcessingUnitControlSelectors(IntEnum):
    # As defined in [Audio30], Table A-36
    ST_EXT_CONTROL_UNDEFINED = 0x00
    ST_EXT_WIDTH_CONTROL     = 0x01
    ST_EXT_UNDERFLOW_CONTROL = 0x02
    ST_EXT_OVERFLOW_CONTROL  = 0x03
    ST_EXT_LATENCY_CONTROL   = 0x04


class ExtensionUnitControlSelectors(IntEnum):
    # As defined in [Audio30], Table A-37
    XU_CONTROL_UNDEFINED = 0x00
    XU_UNDERFLOW_CONTROL = 0x01
    XU_OVERFLOW_CONTROL  = 0x02
    XU_LATENCY_CONTROL   = 0x03


class AudioStreamingInterfaceControlSelectors(IntEnum):
    # As defined in [Audio30], Table A-38
    AS_CONTROL_UNDEFINED         = 0x00
    AS_ACT_ALT_SETTING_CONTROL   = 0x01
    AS_VAL_ALT_SETTINGS_CONTROL  = 0x02
    AS_AUDIO_DATA_FORMAT_CONTROL = 0x03


class EndpointControlSelectors(IntEnum):
    # As defined in [Audio30], Table A-39
    EP_CONTROL_UNDEFINED     = 0x00
    EP_PITCH_CONTROL         = 0x01
    EP_DATA_OVERRUN_CONTROL  = 0x02
    EP_DATA_UNDERRUN_CONTROL = 0x03


class USBTerminalTypes(IntEnum):
    # As defined in [TermT30], Table 2-1
    USB_UNDEFINED       = 0x0100
    USB_STREAMING       = 0x0101
    USB_VENDOR_SPECIFIC = 0x01FF


class InputTerminalTypes(IntEnum):
    # As defined in [TermT30], Table 2-2
    INPUT_UNDEFINED             = 0x0200
    MICROPHONE                  = 0x0201
    DESKTOP_MICROPHONE          = 0x0202
    PERSONAL_MICROPHONE         = 0x0203
    OMNI_DIRECTIONAL_MICROPHONE = 0x0204
    MICROPHONE_ARRAY            = 0x0205
    PROCESSING_MICROPHONE_ARRAY = 0x0206


class OutputTerminalTypes(IntEnum):
    # As defined in [TermT30], Table 2-3
    OUTPUT_UNDEFINED              = 0x0300
    SPEAKER                       = 0x0301
    HEADPHONES                    = 0x0302
    DESKTOP_SPEAKER               = 0x0304
    ROOM_SPEAKER                  = 0x0305
    COMMUNICATION_SPEAKER         = 0x0306
    LOW_FREQUENCY_EFFECTS_SPEAKER = 0x0307


class BidirectionalTerminalTypes(IntEnum):
    # As defined in [TermT30], Table 2-4
    BIDIRECTIONAL_UNDEFINED       = 0x0400
    HANDSET                       = 0x0401
    HEADSET                       = 0x0402
    ECHO_SUPPRESSING_SPEAKERPHONE = 0x0404
    ECHO_CANCELING_SPEAKERPHONE   = 0x0405


class TelephonyTerminalTypes(IntEnum):
    # As defined in [TermT30], Table 2-5
    TELEPHONY_UNDEFINED = 0x0500
    PHONE_LINE          = 0x0501
    TELEPHONE           = 0x0502
    DOWN_LINE_PHONE     = 0x0503


class ExternalTerminalTypes(IntEnum):
    # As defined in [TermT30], Table 2-6
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
    # As defined in [TermT30], Table 2-7
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


class ConnectorTypes(IntEnum):
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


# As defined in [Audio30], Table 4-47
AudioControlInterruptEndpointDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(7, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificStandardDescriptorTypes.CS_ENDPOINT),
    "bEndpointAddress"    / DescriptorField(description="The address of the endpoint, use USBDirection.*.from_endpoint_address()"),
    "bmAttributes"        / DescriptorField(description="D1..0: Transfer type (0b11 = Interrupt)", default=0b11),
    "wMaxPacketSize"      / DescriptorField(description="Maximum packet size this endpoint is capable of. Used here to pass 6-byte interrupt information.", default=6),
    "bInterval"           / DescriptorField(description="Interval for polling the Interrupt endpoint")
)

# As defined in [Audio30], Table 4-51
AudioStreamingIsochronousEndpointDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(7, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(StandardDescriptorNumbers.ENDPOINT),
    "bEndpointAddress"    / DescriptorField(description="The address of the endpoint, use USBDirection.*.from_endpoint_address()"),
    "bmAttributes"        / DescriptorField(description="D1..0: transfer type (01=isochronous); D3..2: synchronization type (01=asynchronous/10=adaptive/11=synchronous); D5..4: usage (00=data/10=feedback)", default=0b000101),
    "wMaxPacketSize"      / DescriptorField(description="Maximum packet size this endpoint is capable of. Used here to pass 6-byte interrupt information.", default=6),
    "bInterval"           / DescriptorField(description="Interval for polling the Interrupt endpoint")
)

# As defined in [Audio30], Table 4-53
AudioStreamingIsochronousFeedbackEndpointDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(7, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(StandardDescriptorNumbers.ENDPOINT),
    "bEndpointAddress"    / DescriptorField(description="The address of the endpoint, use USBDirection.*.from_endpoint_address()"),
    "bmAttributes"        / DescriptorField(description="D1..0: transfer type (01=isochronous); D3..2: synchronization type (00=no sync); D5..4: usage (10=feedback)", default=0b00100001),
    "wMaxPacketSize"      / DescriptorField(description="Maximum packet size this endpoint is capable of. Used here to pass 6-byte interrupt information.", default=6),
    "bInterval"           / DescriptorField(description="Interval for polling the Interrupt endpoint")
)

HeaderDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(10, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificStandardDescriptorTypes.CS_INTERFACE),
    "bDescriptorSubtype"  / DescriptorNumber(AudioClassSpecificACInterfaceDescriptorSubtypes.HEADER),
    "bCategory"           / DescriptorField(description="Audio Function Category, see AudioFunctionCategoryCodes"),
    "wTotalLength"        / DescriptorField("Length including subordinates"),
    "bmControls"          / DescriptorField("D1..0: Latency Control; D31..2: Reserved.", length=4, default=0)
)

AudioStreamingInterfaceDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(9, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(StandardDescriptorNumbers.INTERFACE),
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
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificStandardDescriptorTypes.CS_INTERFACE),
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
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificStandardDescriptorTypes.CS_INTERFACE),
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
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificStandardDescriptorTypes.CS_INTERFACE),
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
