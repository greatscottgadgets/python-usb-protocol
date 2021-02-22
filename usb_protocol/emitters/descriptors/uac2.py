#
# This file is part of usb_protocol.
#
""" Convenience emitters for USB Audio Class 2 descriptors. """

from contextlib import contextmanager

from .. import emitter_for_format
from ...types.descriptors.uac  import *
from ...types.descriptors.uac2 import *
from ...emitters.descriptor    import ComplexDescriptorEmitter

# Create our emitters.
InterfaceAssociationDescriptorEmitter          = emitter_for_format(InterfaceAssociationDescriptor)
StandardAudioControlInterfaceDescriptorEmitter = emitter_for_format(StandardAudioControlInterfaceDescriptor)

class ClassSpecificAudioControlInterfaceDescriptorEmitter(ComplexDescriptorEmitter):
    DESCRIPTOR_FORMAT = ClassSpecificAudioControlInterfaceDescriptor

    def _pre_emit(self):
        # Figure out the total length of our descriptor, including subordinates.
        subordinate_length = sum(len(sub) for sub in self._subordinates)
        self.wTotalLength = subordinate_length + self.DESCRIPTOR_FORMAT.sizeof()

ClockSourceDescriptorEmitter                                             = emitter_for_format(ClockSourceDescriptor)
InputTerminalDescriptorEmitter                                           = emitter_for_format(InputTerminalDescriptor)
OutputTerminalDescriptorEmitter                                          = emitter_for_format(OutputTerminalDescriptor)
AudioStreamingInterfaceDescriptorEmitter                                 = emitter_for_format(AudioStreamingInterfaceDescriptor)
ClassSpecificAudioStreamingInterfaceDescriptorEmitter                    = emitter_for_format(ClassSpecificAudioStreamingInterfaceDescriptor)
TypeIFormatTypeDescriptorEmitter                                         = emitter_for_format(TypeIFormatTypeDescriptor)
ExtendedTypeIFormatTypeDescriptorEmitter                                 = emitter_for_format(ExtendedTypeIFormatTypeDescriptor)
TypeIIFormatTypeDescriptorEmitter                                        = emitter_for_format(TypeIIFormatTypeDescriptor)
ExtendedTypeIIFormatTypeDescriptorEmitter                                = emitter_for_format(ExtendedTypeIIFormatTypeDescriptor)
TypeIIIFormatTypeDescriptorEmitter                                       = emitter_for_format(TypeIIIFormatTypeDescriptor)
ExtendedTypeIIIFormatTypeDescriptorEmitter                               = emitter_for_format(ExtendedTypeIIIFormatTypeDescriptor)
ClassSpecificAudioStreamingIsochronousAudioDataEndpointDescriptorEmitter = emitter_for_format(ClassSpecificAudioStreamingIsochronousAudioDataEndpointDescriptor)
AudioControlInterruptEndpointDescriptorEmitter                           = emitter_for_format(AudioControlInterruptEndpointDescriptor)
AudioStreamingIsochronousEndpointDescriptorEmitter                       = emitter_for_format(AudioStreamingIsochronousEndpointDescriptor)
AudioStreamingIsochronousFeedbackEndpointDescriptorEmitter               = emitter_for_format(AudioStreamingIsochronousFeedbackEndpointDescriptor)
