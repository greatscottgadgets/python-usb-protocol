#
# This file is part of usb_protocol.
#
""" Convenience emitters for simple, standard descriptors. """

import unittest
import functools

from contextlib import contextmanager

from ..           import emitter_for_format
from ..descriptor import ComplexDescriptorEmitter

from ...types.descriptors.standard import \
    DeviceDescriptor, StringDescriptor, EndpointDescriptor, DeviceQualifierDescriptor, \
    ConfigurationDescriptor, InterfaceDescriptor, StandardDescriptorNumbers


# Create our basic emitters...
DeviceDescriptorEmitter    = emitter_for_format(DeviceDescriptor)
StringDescriptorEmitter    = emitter_for_format(StringDescriptor)
EndpointDescriptorEmitter  = emitter_for_format(EndpointDescriptor)
DeviceQualifierDescriptor  = emitter_for_format(DeviceQualifierDescriptor)

# ... convenience functions ...
def get_string_descriptor(string):
    """ Generates a string descriptor for the relevant string. """

    emitter = StringDescriptorEmitter()
    emitter.bString = string
    return emitter.emit()

# ... and complex emitters.

class InterfaceDescriptorEmitter(ComplexDescriptorEmitter):
    """ Emitter that creates an InterfaceDescriptor. """

    DESCRIPTOR_FORMAT = InterfaceDescriptor

    @contextmanager
    def EndpointDescriptor(self):
        """ Context manager that allows addition of a subordinate endpoint descriptor.

        It can be used with a `with` statement; and yields an EndpointDesriptorEmitter
        that can be populated:

            with interface.EndpointDescriptor() as d:
                d.bEndpointAddress = 0x01
                d.bmAttributes     = 0x80
                d.wMaxPacketSize   = 64
                d.bInterval        = 0

        This adds the relevant descriptor, automatically.
        """

        descriptor = EndpointDescriptorEmitter()
        yield descriptor

        self.add_subordinate_descriptor(descriptor)


    def emit(self, include_subordinates=True):

        # Count our endpoints, and then call our parent emitter.
        self.bNumEndpoints = self._type_counts[StandardDescriptorNumbers.ENDPOINT]
        return super().emit(include_subordinates=include_subordinates)



class ConfigurationDescriptorEmitter(ComplexDescriptorEmitter):
    """ Emitter that creates a configuration descriptor. """

    DESCRIPTOR_FORMAT = ConfigurationDescriptor

    @contextmanager
    def InterfaceDescriptor(self):
        """ Context manager that allows addition of a subordinate interface descriptor.

        It can be used with a `with` statement; and yields an InterfaceDescriptorEmitter
        that can be populated:

            with interface.InterfaceDescriptor() as d:
                d.bInterfaceNumber = 0x01
                [snip]

        This adds the relevant descriptor, automatically. Note that populating derived
        fields such as bNumEndpoints aren't necessary; they'll be populated automatically.
        """
        descriptor = InterfaceDescriptorEmitter()
        yield descriptor

        self.add_subordinate_descriptor(descriptor)


    def emit(self, include_subordinates=True):

        # Count our interfaces...
        self.bNumInterfaces = self._type_counts[StandardDescriptorNumbers.INTERFACE]

        # ... and figure out our total length.
        subordinate_length = sum(len(sub) for sub in self._subordinates)
        self.wTotalLength = subordinate_length + self.DESCRIPTOR_FORMAT.sizeof()

        # Finally, emit our whole descriptor.
        return super().emit(include_subordinates=include_subordinates)


class EmitterTests(unittest.TestCase):

    def test_string_emitter(self):
        emitter = StringDescriptorEmitter()
        emitter.bString = "Hello"

        self.assertEqual(emitter.emit(), b"\x0C\x03H\0e\0l\0l\0o\0")


    def test_string_emitter_function(self):
        self.assertEqual(get_string_descriptor("Hello"), b"\x0C\x03H\0e\0l\0l\0o\0")


    def test_configuration_emitter(self):
        descriptor = bytes([

            # config descriptor
            12,     # length
            2,      # type
            25, 00, # total length
            1,      # num interfaces
            1,      # configuration number
            0,      # config string
            0x80,   # attributes
            250,    # max power

            # interface descriptor
            9,    # length
            4,    # type
            0,    # number
            0,    # alternate
            1,    # num endpoints
            0xff, # class
            0xff, # subclass
            0xff, # protocol
            0,    # string

            # endpoint descriptor
            7,       # length
            5,       # type
            0x01,    # address
            2,       # attributes
            64, 0,   # max packet size
            255,     # interval
        ])


        # Create a trivial configuration descriptor...
        emitter = ConfigurationDescriptorEmitter()

        with emitter.InterfaceDescriptor() as interface:
            interface.bInterfaceNumber = 0

            with interface.EndpointDescriptor() as endpoint:
                endpoint.bEndpointAddress = 1


        # ... and validate that it maches our reference descriptor.
        binary = emitter.emit()
        self.assertEqual(len(binary), len(descriptor))


if __name__ == "__main__":
    unittest.main()
