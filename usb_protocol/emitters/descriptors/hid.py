import unittest

from contextlib import contextmanager

from ..           import emitter_for_format
from ..descriptor import ComplexDescriptorEmitter
from ...types.descriptors.hid import *

class HIDDescriptorEmitter(ComplexDescriptorEmitter):

    DESCRIPTOR_FORMAT = HIDDescriptor
    
    @contextmanager
    def DescriptorReference(self):
        """ Context manager that allows addition of a subordinate report descriptor.

        It can be used with a `with` statement; and yields an HIDDescriptorReferenceEmitter
        that can be populated:

            with hiddescriptor.DescriptorReference() as r:
                r.wDescriptorLength = 0x10

        This adds the relevant descriptor, automatically.
        """

        descriptor = HIDDescriptorReferenceEmitter()
        yield descriptor

        self.add_subordinate_descriptor(descriptor)

    def _pre_emit(self):
        # Figure out the total length of our descriptor, including subordinates.
        subordinate_length = sum(len(sub) for sub in self._subordinates)
        self.bLength = subordinate_length + self.DESCRIPTOR_FORMAT.sizeof()
        self.bNumDescriptors = len(self._subordinates)
        pass


HIDDescriptorReferenceEmitter = emitter_for_format(HIDDescriptorReference)
