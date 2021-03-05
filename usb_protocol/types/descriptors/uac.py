#
# This file is part of usb-protocol.
#
""" common USB audio enums and descriptors """

from usb_protocol.types import USBSynchronizationType, USBUsageType
from enum import IntEnum

import construct

from .. import USBTransferType
from ..descriptor import \
    DescriptorField, DescriptorNumber, DescriptorFormat

class AudioInterfaceClassCode(IntEnum):
    AUDIO = 0x01

class AudioFunctionClassCode(IntEnum):
    AUDIO_FUNCTION = AudioInterfaceClassCode.AUDIO

class AudioInterfaceProtocolCodes(IntEnum):
    IP_VERSION_01_00 = 0x00
    IP_VERSION_02_00 = 0x20
    IP_VERSION_03_00 = 0x30

class AudioFunctionProtocolCodes(IntEnum):
    FUNCTION_PROTOCOL_UNDEFINED = 0x00
    AF_VERSION_01_00 = AudioInterfaceProtocolCodes.IP_VERSION_01_00
    AF_VERSION_02_00 = AudioInterfaceProtocolCodes.IP_VERSION_02_00
    AF_VERSION_03_00 = AudioInterfaceProtocolCodes.IP_VERSION_03_00

class AudioFunctionSubclassCodes(IntEnum):
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
    INTERFACE_SUBCLASS_UNDEFINED  = 0x00
    AUDIO_CONTROL                 = 0x01
    AUDIO_STREAMING               = 0x02
    MIDI_STREAMING                = 0x03

class AudioFunctionCategoryCodes(IntEnum):
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


class DescriptorTypes(IntEnum):
    INTERFACE             = 0x04
    ENDPOINT              = 0x05
    INTERFACE_ASSOCIATION = 0x0B

class AudioClassSpecificDescriptorTypes(IntEnum):
    CS_UNDEFINED     = 0x20
    CS_DEVICE        = 0x21
    CS_CONFIGURATION = 0x22
    CS_STRING        = 0x23
    CS_INTERFACE     = 0x24
    CS_ENDPOINT      = 0x25
    CS_CLUSTER       = 0x26

class ClusterDescriptorSubtypes(IntEnum):
    SUBTYPE_UNDEFINED = 0x00

class ClusterDescriptorSegmentTypes(IntEnum):
    SEGMENT_UNDEFINED      = 0x00
    CLUSTER_DESCRIPTION    = 0x01
    CLUSTER_VENDOR_DEFINED = 0x1F
    CHANNEL_INFORMATION    = 0x20
    CHANNEL_AMBISONIC      = 0x21
    CHANNEL_DESCRIPTION    = 0x22
    CHANNEL_VENDOR_DEFINED = 0xFE
    END_SEGMENT            = 0xFF

class  ChannelPurposeDefinitions(IntEnum):
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
    ORD_TYPE_UNDEFINED           = 0x00
    AMBISONIC_CHANNEL_NUMBER_ACN = 0x01
    FURSE_MALHAM                 = 0x02
    SINGLE_INDEX_DESIGNATION_SID = 0x03

class AmbisonicNormalizatioTypes(IntEnum):
    NORM_TYPE_UNDEFINED = 0x00
    MAX_N               = 0x01
    SN3D                = 0x02
    N3D                 = 0x03
    SN2D                = 0x04
    N2D                 = 0x05

class AudioClassSpecificACInterfaceDescriptorSubtypes(IntEnum):
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
 
class AudioClassSpecificStringDescriptorSubtypes(IntEnum):
    SUBTYPE_UNDEFINED = 0x00

class ExtendedTerminalSegmentTypes(IntEnum):
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
    EFFECT_UNDEFINED        = 0x0000
    PARAM_EQ_SECTION_EFFECT = 0x0001
    REVERBERATION_EFFECT    = 0x0002
    MOD_DELAY_EFFECT        = 0x0003
    DYN_RANGE_COMP_EFFECT   = 0x0004

class ProcessingUnitProcessTypes(IntEnum):
    PROCESS_UNDEFINED       = 0x0000
    UP_DOWNMIX_PROCESS      = 0x0001
    STEREO_EXTENDER_PROCESS = 0x0002
    MULTI_FUNCTION_PROCESS  = 0x0003

class AudioClassSpecificEndpointDescriptorSubtypes(IntEnum):
    DESCRIPTOR_UNDEFINED = 0x00
    EP_GENERAL           = 0x01

class AudioClassSpecificRequestCodes(IntEnum):
    REQUEST_CODE_UNDEFINED     = 0x00
    CUR                        = 0x01
    RANGE                      = 0x02
    MEM                        = 0x03
    INTEN                      = 0x04
    STRING                     = 0x05
    HIGH_CAPABILITY_DESCRIPTOR = 0x06

class AudioControlInterfaceControlSelectors(IntEnum):
    AC_CONTROL_UNDEFINED        = 0x00
    AC_ACTIVE_INTERFACE_CONTROL = 0x01
    AC_POWER_DOMAIN_CONTROL     = 0x02

class ClockSourceControlSelectors(IntEnum):
    CS_CONTROL_UNDEFINED   = 0x00
    CS_SAM_FREQ_CONTROL    = 0x01
    CS_CLOCK_VALID_CONTROL = 0x02

class ClockSelectorControlSelectors(IntEnum):
    CX_CONTROL_UNDEFINED      = 0x00
    CX_CLOCK_SELECTOR_CONTROL = 0x01

class ClockMultiplierControlSelectors(IntEnum):
    CM_CONTROL_UNDEFINED   = 0x00
    CM_NUMERATOR_CONTROL   = 0x01
    CM_DENOMINATOR_CONTROL = 0x02

class TerminalControlSelectors(IntEnum):
    TE_CONTROL_UNDEFINED = 0x00
    TE_INSERTION_CONTROL = 0x01
    TE_OVERLOAD_CONTROL  = 0x02
    TE_UNDERFLOW_CONTROL = 0x03
    TE_OVERFLOW_CONTROL  = 0x04
    TE_LATENCY_CONTROL   = 0x05

class MixerControlSelectors(IntEnum):
    MU_CONTROL_UNDEFINED = 0x00
    MU_MIXER_CONTROL     = 0x01
    MU_UNDERFLOW_CONTROL = 0x02
    MU_OVERFLOW_CONTROL  = 0x03
    MU_LATENCY_CONTROL   = 0x04

class SelectorControlSelectors(IntEnum):
    SU_CONTROL_UNDEFINED = 0x00
    SU_SELECTOR_CONTROL  = 0x01
    SU_LATENCY_CONTROL   = 0x02

class FeatureUnitControlSelectors(IntEnum):
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
    PE_CONTROL_UNDEFINED  = 0x00
    PE_ENABLE_CONTROL     = 0x01
    PE_CENTERFREQ_CONTROL = 0x02
    PE_QFACTOR_CONTROL    = 0x03
    PE_GAIN_CONTROL       = 0x04
    PE_UNDERFLOW_CONTROL  = 0x05
    PE_OVERFLOW_CONTROL   = 0x06
    PE_LATENCY_CONTROL    = 0x07

class ReverberationEffectUnitControlSelectors(IntEnum):
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
    UD_CONTROL_UNDEFINED   = 0x00
    UD_MODE_SELECT_CONTROL = 0x01
    UD_UNDERFLOW_CONTROL   = 0x02
    UD_OVERFLOW_CONTROL    = 0x03
    UD_LATENCY_CONTROL     = 0x04

class StereoExtenderProcessingUnitControlSelectors(IntEnum):
    ST_EXT_CONTROL_UNDEFINED = 0x00
    ST_EXT_WIDTH_CONTROL     = 0x01
    ST_EXT_UNDERFLOW_CONTROL = 0x02
    ST_EXT_OVERFLOW_CONTROL  = 0x03
    ST_EXT_LATENCY_CONTROL   = 0x04

class ExtensionUnitControlSelectors(IntEnum):
    XU_CONTROL_UNDEFINED = 0x00
    XU_UNDERFLOW_CONTROL = 0x01
    XU_OVERFLOW_CONTROL  = 0x02
    XU_LATENCY_CONTROL   = 0x03

class AudioStreamingInterfaceControlSelectors(IntEnum):
    AS_CONTROL_UNDEFINED         = 0x00
    AS_ACT_ALT_SETTING_CONTROL   = 0x01
    AS_VAL_ALT_SETTINGS_CONTROL  = 0x02
    AS_AUDIO_DATA_FORMAT_CONTROL = 0x03

class EndpointControlSelectors(IntEnum):
    EP_CONTROL_UNDEFINED     = 0x00
    EP_PITCH_CONTROL         = 0x01
    EP_DATA_OVERRUN_CONTROL  = 0x02
    EP_DATA_UNDERRUN_CONTROL = 0x03

###################### Terminal Types #########################

class USBTerminalTypes(IntEnum):
    USB_UNDEFINED       = 0x0100
    USB_STREAMING       = 0x0101
    USB_VENDOR_SPECIFIC = 0x01FF

class InputTerminalTypes(IntEnum):
    INPUT_UNDEFINED             = 0x0200
    MICROPHONE                  = 0x0201
    DESKTOP_MICROPHONE          = 0x0202
    PERSONAL_MICROPHONE         = 0x0203
    OMNI_DIRECTIONAL_MICROPHONE = 0x0204
    MICROPHONE_ARRAY            = 0x0205
    PROCESSING_MICROPHONE_ARRAY = 0x0206

class OutputTerminalTypes(IntEnum):
    OUTPUT_UNDEFINED              = 0x0300
    SPEAKER                       = 0x0301
    HEADPHONES                    = 0x0302
    DESKTOP_SPEAKER               = 0x0304
    ROOM_SPEAKER                  = 0x0305
    COMMUNICATION_SPEAKER         = 0x0306
    LOW_FREQUENCY_EFFECTS_SPEAKER = 0x0307

class BidirectionalTerminalTypes(IntEnum):
    BIDIRECTIONAL_UNDEFINED       = 0x0400
    HANDSET                       = 0x0401
    HEADSET                       = 0x0402
    ECHO_SUPPRESSING_SPEAKERPHONE = 0x0404
    ECHO_CANCELING_SPEAKERPHONE   = 0x0405

class TelephonyTerminalTypes(IntEnum):
    TELEPHONY_UNDEFINED = 0x0500
    PHONE_LINE          = 0x0501
    TELEPHONE           = 0x0502
    DOWN_LINE_PHONE     = 0x0503

class ExternalTerminalTypes(IntEnum):
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

AudioControlInterruptEndpointDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(7, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificDescriptorTypes.CS_ENDPOINT),
    "bEndpointAddress"    / DescriptorField(description="The address of the endpoint, use USBDirection.*.from_endpoint_address()"),
    "bmAttributes"        / DescriptorField(description="D1..0: Transfer type (0b11 = Interrupt)", default=0b11),
    "wMaxPacketSize"      / DescriptorField(description="Maximum packet size this endpoint is capable of. Used here to pass 6-byte interrupt information.", default=6),
    "bInterval"           / DescriptorField(description="Interval for polling the Interrupt endpoint")
)

AudioStreamingIsochronousEndpointDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(7, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(DescriptorTypes.ENDPOINT),
    "bEndpointAddress"    / DescriptorField(description="The address of the endpoint, use USBDirection.*.from_endpoint_address()"),
    "bmAttributes"        / DescriptorField(description="D1..0: transfer type (01=isochronous); D3..2: synchronization type (01=asynchronous/10=adaptive/11=synchronous); D5..4: usage (00=data/10=feedback)", default=0b000101),
    "wMaxPacketSize"      / DescriptorField(description="Maximum packet size this endpoint is capable of. Used here to pass 6-byte interrupt information.", default=6),
    "bInterval"           / DescriptorField(description="Interval for polling the Interrupt endpoint")
)

AudioStreamingIsochronousFeedbackEndpointDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(7, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(DescriptorTypes.ENDPOINT),
    "bEndpointAddress"    / DescriptorField(description="The address of the endpoint, use USBDirection.*.from_endpoint_address()"),
    "bmAttributes"        / DescriptorField(description="D1..0: transfer type (01=isochronous); D3..2: synchronization type (00=no sync); D5..4: usage (10=feedback)", default=0b00100001),
    "wMaxPacketSize"      / DescriptorField(description="Maximum packet size this endpoint is capable of. Used here to pass 6-byte interrupt information.", default=6),
    "bInterval"           / DescriptorField(description="Interval for polling the Interrupt endpoint")
)

###################### MIDI #########################
class MidiStreamingInterfaceDescriptorTypes(IntEnum):
    CS_UNDEFINED     = 0x20
    CS_DEVICE        = 0x21
    CS_CONFIGURATION = 0x22
    CS_STRING        = 0x23
    CS_INTERFACE     = 0x24
    CS_ENDPOINT      = 0x25
    CS_GR_TRM_BLOCK  = 0x26

class MidiStreamingInterfaceDescriptorSubtypes(IntEnum):
    MS_DESCRIPTOR_UNDEFINED = 0x00
    MS_HEADER               = 0x01
    MIDI_IN_JACK            = 0x02
    MIDI_OUT_JACK           = 0x03
    ELEMENT                 = 0x04

class MidiStreamingEndpointDescriptorSubtypes(IntEnum):
    DESCRIPTOR_UNDEFINED = 0x00
    MS_GENERAL           = 0x01
    MS_GENERAL_2_0       = 0x02

class MidiStreamingInterfaceHeaderClassRevision(IntEnum):
    MS_MIDI_1_0 = 0x0100
    MS_MIDI_2_0 = 0x0200

class MidiStreamingJackTypes(IntEnum):
    JACK_TYPE_UNDEFINED = 0x00
    EMBEDDED            = 0x01
    EXTERNAL            = 0x02

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

ClassSpecificMidiStreamingInterfaceHeaderDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(7, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificDescriptorTypes.CS_INTERFACE),
    "bDescriptorSubtype"  / DescriptorNumber(AudioClassSpecificACInterfaceDescriptorSubtypes.HEADER),
    "bcdADC"              / DescriptorField(description="Midi Streaming Class specification release version", default=1.0),
    "wTotalLength"        / DescriptorField(description="Total number of bytes of the class-specific MIDIStreaming interface descriptor. Includes the combined length of this descriptor header and all Jack and Element descriptors."),
)

StandardMidiStreamingDataEndpointDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(7, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificDescriptorTypes.CS_ENDPOINT),
    "bEndpointAddress"    / DescriptorField(description="endpoint address, use USBDirection.*.from_endpoint_address()"),
    "bmAttributes"        / DescriptorField(description="endpoint type, see USBTransferType (only NONE, BULK or INTERRUPT allowed)", default=USBTransferType.BULK),
    "wMaxPacketSize"      / DescriptorField(description="Maximum packet size this endpoint is capable of sending or receiving"),
    "bInterval"           / DescriptorField(description="Interval for polling endpoint for Interrupt data transfers. For bulk endpoints this field is ignored and must be reset to 0", default=0)
)

MidiInJackDescriptor = DescriptorFormat(
    "bLength"             / construct.Const(6, construct.Int8ul),
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificDescriptorTypes.CS_INTERFACE),
    "bDescriptorSubtype"  / DescriptorNumber(MidiStreamingInterfaceDescriptorSubtypes.MIDI_IN_JACK),
    "bJackType"           / DescriptorField(description="see MidiStreamingJackTypes"),
    "bJackID"             / DescriptorField(description="Constant uniquely identifying the MIDI IN Jack within the USB-MIDI function"),
    "iJack"               / DescriptorField(description="index of a string descriptor describing this jack (0 = unused)", default=0)
)

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

ClassSpecificMidiStreamingBulkDataEndpointDescriptorHead = DescriptorFormat(
    "bLength"             / DescriptorField(description="Size of this descriptor, in bytes: 4+n"),
    "bDescriptorType"     / DescriptorNumber(AudioClassSpecificDescriptorTypes.CS_ENDPOINT),
    "bDescriptorSubtype"  / DescriptorField(description="see MidiStreamingEndpointDescriptorSubtypes", default=MidiStreamingEndpointDescriptorSubtypes.MS_GENERAL),
    "bNumEmbMIDIJack"     / DescriptorField(description="Number of Embedded MIDI Jacks: n", default=1)
)

ClassSpecificMidiStreamingBulkDataEndpointDescriptorElement = DescriptorFormat(
    "baAssocJackID"       / construct.Int8ul # ID of the embedded eack that is associated with this endpoint
)