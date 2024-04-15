#
# This file is part of usb_protocol.
#
""" Convenience emitters for USB MIDI Class 1 descriptors. """

from ..                         import emitter_for_format
from ...emitters.descriptor     import ComplexDescriptorEmitter
from ...types.descriptors.midi1 import *

class ClassSpecificMidiStreamingInterfaceDescriptorEmitter(ComplexDescriptorEmitter):
    DESCRIPTOR_FORMAT = ClassSpecificMidiStreamingInterfaceHeaderDescriptor

    def _pre_emit(self):
        # Figure out the total length of our descriptor, including subordinates.
        subordinate_length = sum(len(sub) for sub in self._subordinates)
        self.wTotalLength = subordinate_length + self.DESCRIPTOR_FORMAT.sizeof()

class MidiOutJackDescriptorEmitter(ComplexDescriptorEmitter):
    DESCRIPTOR_FORMAT = MidiOutJackDescriptorHead

    def add_subordinate_descriptor(self, subordinate):
        subordinate = subordinate.emit()
        self._subordinates.append(subordinate)

    def add_source(self, sourceId, sourcePin=1):
        sourceDescriptor = MidiOutJackDescriptorElementEmitter()
        sourceDescriptor.baSourceID = sourceId
        sourceDescriptor.BaSourcePin = sourcePin
        self.add_subordinate_descriptor(sourceDescriptor)

    def _pre_emit(self):
        self.add_subordinate_descriptor(MidiOutJackDescriptorFootEmitter())
        # Figure out the total length of our descriptor, including subordinates.
        subordinate_length = sum(len(sub) for sub in self._subordinates)
        self.bLength = subordinate_length + self.DESCRIPTOR_FORMAT.sizeof()

class ClassSpecificMidiStreamingBulkDataEndpointDescriptorEmitter(ComplexDescriptorEmitter):
    DESCRIPTOR_FORMAT = ClassSpecificMidiStreamingBulkDataEndpointDescriptorHead

    def add_subordinate_descriptor(self, subordinate):
        subordinate = subordinate.emit()
        self._subordinates.append(subordinate)

    def add_associated_jack(self, jackID):
        jackDescriptor = ClassSpecificMidiStreamingBulkDataEndpointDescriptorElementEmitter()
        jackDescriptor.baAssocJackID = jackID
        self.add_subordinate_descriptor(jackDescriptor)

    def _pre_emit(self):
        # Figure out the total length of our descriptor, including subordinates.
        subordinate_length = sum(len(sub) for sub in self._subordinates)
        self.bLength = subordinate_length + self.DESCRIPTOR_FORMAT.sizeof()

StandardMidiStreamingInterfaceDescriptorEmitter                    = emitter_for_format(StandardMidiStreamingInterfaceDescriptor)
ClassSpecificMidiStreamingInterfaceHeaderDescriptorEmitter         = emitter_for_format(ClassSpecificMidiStreamingInterfaceHeaderDescriptor)
MidiInJackDescriptorEmitter                                        = emitter_for_format(MidiInJackDescriptor)
MidiOutJackDescriptorHeadEmitter                                   = emitter_for_format(MidiOutJackDescriptorHead)
MidiOutJackDescriptorElementEmitter                                = emitter_for_format(MidiOutJackDescriptorElement)
MidiOutJackDescriptorFootEmitter                                   = emitter_for_format(MidiOutJackDescriptorFoot)
StandardMidiStreamingBulkDataEndpointDescriptorEmitter             = emitter_for_format(StandardMidiStreamingBulkDataEndpointDescriptor)
ClassSpecificMidiStreamingBulkDataEndpointDescriptorHeadEmitter    = emitter_for_format(ClassSpecificMidiStreamingBulkDataEndpointDescriptorHead)
ClassSpecificMidiStreamingBulkDataEndpointDescriptorElementEmitter = emitter_for_format(ClassSpecificMidiStreamingBulkDataEndpointDescriptorElement)
