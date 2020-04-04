#
# This file is part of usb_protocol.
#
""" Convenience emitters for simple, standard descriptors. """

import unittest

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


    def _pre_emit(self):

        # Count our endpoints, and update our internal count.
        self.bNumEndpoints = self._type_counts[StandardDescriptorNumbers.ENDPOINT]

        # Ensure that our interface string is an index, if we can.
        if self._collection and hasattr(self, 'iInterface'):
            self.iInterface = self._collection.ensure_string_field_is_index(self.iInterface)



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
        descriptor = InterfaceDescriptorEmitter(collection=self._collection)
        yield descriptor

        self.add_subordinate_descriptor(descriptor)


    def _pre_emit(self):

        # Count our interfaces.
        self.bNumInterfaces = self._type_counts[StandardDescriptorNumbers.INTERFACE]

        # Figure out our total length.
        subordinate_length = sum(len(sub) for sub in self._subordinates)
        self.wTotalLength = subordinate_length + self.DESCRIPTOR_FORMAT.sizeof()

        # Ensure that our configuration string is an index, if we can.
        if self._collection and hasattr(self, 'iConfiguration'):
            self.iConfiguration = self._collection.ensure_string_field_is_index(self.iConfiguration)



class DeviceDescriptorCollection:
    """ Object that builds a full collection of descriptors related to a given USB device. """

    def __init__(self):

        # Create our internal descriptor tracker.
        # Keys are a tuple of (type, index).
        self._descriptors = {}

        # Track string descriptors as they're created.
        self._next_string_index = 1
        self._index_for_string = {}


    def ensure_string_field_is_index(self, field_value):
        """ Processes the given field value; if it's not an string index, converts it to one.

        Non-index-fields are converted to indices using `get_index_for_string`, which automatically
        adds the relevant fields to our string descriptor collection.
        """

        if isinstance(field_value, str):
            return self.get_index_for_string(field_value)
        else:
            return field_value


    def get_index_for_string(self, string):
        """ Returns an string descriptor index for the given string.

        If a string descriptor already exists for the given string, its index is
        returned. Otherwise, a string descriptor is created.
        """

        # If we already have a descriptor for this string, return it.
        if string in self._index_for_string:
            return self._index_for_string[string]


        # Otherwise, create one:

        # Allocate an index...
        index = self._next_string_index
        self._index_for_string[string] = index
        self._next_string_index += 1

        # ... store our string descriptor with it ...
        identifier = StandardDescriptorNumbers.STRING, index
        self._descriptors[identifier] = get_string_descriptor(string)

        # ... and return our index.
        return index


    def add_descriptor(self, descriptor, index=0):
        """ Adds a descriptor to our collection.

        Parameters:
            descriptor -- The descriptor to be added.
            index      -- The index of the relevant descriptor. Defaults to 0.
        """

        # If this is an emitter rather than a descriptor itself, convert it.
        if hasattr(descriptor, 'emit'):
            descriptor = descriptor.emit()

        # Figure out the identifier (type + index) for this descriptor...
        descriptor_type = descriptor[1]
        identifier = descriptor_type, index

        # ... and store it.
        self._descriptors[identifier] = descriptor


    @contextmanager
    def DeviceDescriptor(self):
        """ Context manager that allows addition of a device descriptor.

        It can be used with a `with` statement; and yields an DeviceDescriptorEmitter
        that can be populated:

            with collection.DeviceDescriptor() as d:
                d.idVendor  = 0xabcd
                d.idProduct = 0x1234
                [snip]

        This adds the relevant descriptor, automatically.
        """
        descriptor = DeviceDescriptorEmitter()
        yield descriptor

        # If we have any string fields, ensure that they're indices before continuing.
        for field in ('iManufacturer', 'iProduct', 'iSerialNumber'):
            if hasattr(descriptor, field):
                value = getattr(descriptor, field)
                index = self.ensure_string_field_is_index(value)
                setattr(descriptor, field, index)

        self.add_descriptor(descriptor)


    @contextmanager
    def ConfigurationDescriptor(self):
        """ Context manager that allows addition of a configuration descriptor.

        It can be used with a `with` statement; and yields an ConfigurationDescriptorEmitter
        that can be populated:

            with collection.ConfigurationDescriptor() as d:
                d.bConfigurationValue = 1
                [snip]

        This adds the relevant descriptor, automatically. Note that populating derived
        fields such as bNumInterfaces aren't necessary; they'll be populated automatically.
        """
        descriptor = ConfigurationDescriptorEmitter()
        yield descriptor

        self.add_descriptor(descriptor)


    def __iter__(self):
        """ Allow iterating over each of our descriptors; yields (index, value, descriptor). """
        return ((number, index, desc) for ((number, index), desc) in self._descriptors.items())


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


    def test_descriptor_collection(self):
        collection = DeviceDescriptorCollection()

        with collection.DeviceDescriptor() as d:
            d.idVendor           = 0xdead
            d.idProduct          = 0xbeef
            d.bNumConfigurations = 1

            d.iManufacturer      = "Test Company"
            d.iProduct           = "Test Product"


        with collection.ConfigurationDescriptor() as c:
            c.bConfigurationValue = 1

            with c.InterfaceDescriptor() as i:
                i.bInterfaceNumber = 1

                with i.EndpointDescriptor() as e:
                    e.bEndpointAddress = 0x81

                with i.EndpointDescriptor() as e:
                    e.bEndpointAddress = 0x01


        results = list(collection)

        # We should wind up with four descriptor entries, as our endpoint/interface descriptors are
        # included in our configuration descriptor.
        self.assertEqual(len(results), 4)

        # Manufacturer / product string.
        self.assertIn((3, 1, b'\x1a\x03T\x00e\x00s\x00t\x00 \x00C\x00o\x00m\x00p\x00a\x00n\x00y\x00'), results)
        self.assertIn((3, 2, b'\x1a\x03T\x00e\x00s\x00t\x00 \x00P\x00r\x00o\x00d\x00u\x00c\x00t\x00'), results)

        # Device descriptor.
        self.assertIn((1, 0, b'\x0f\x01\x00\x02\x00\x00\x00@\xad\xde\xef\xbe\x00\x00\x01\x02\x00\x01'), results)

        # Configuration descriptor, with subordinates.
        self.assertIn((2, 0, b'\r\x02 \x00\x01\x01\x00\x80\xfa\t\x04\x01\x00\x02\xff\xff\xff\x00\x07\x05\x81\x02@\x00\xff\x07\x05\x01\x02@\x00\xff'), results)

if __name__ == "__main__":
    unittest.main()
