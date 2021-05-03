#
# This file is part of usb_protocol.
#
""" Convenience emitters for USB Audio Class 3 descriptors. """

from .. import emitter_for_format
from ...types.descriptors.uac3 import *

InputTerminalDescriptorEmitter                                           = emitter_for_format(InputTerminalDescriptor)
OutputTerminalDescriptorEmitter                                          = emitter_for_format(OutputTerminalDescriptor)
AudioStreamingInterfaceDescriptorEmitter                                 = emitter_for_format(AudioStreamingInterfaceDescriptor)
ClassSpecificAudioStreamingInterfaceDescriptorEmitter                    = emitter_for_format(ClassSpecificAudioStreamingInterfaceDescriptor)
AudioControlInterruptEndpointDescriptorEmitter                           = emitter_for_format(AudioControlInterruptEndpointDescriptor)
AudioStreamingIsochronousEndpointDescriptorEmitter                       = emitter_for_format(AudioStreamingIsochronousEndpointDescriptor)
AudioStreamingIsochronousFeedbackEndpointDescriptorEmitter               = emitter_for_format(AudioStreamingIsochronousFeedbackEndpointDescriptor)