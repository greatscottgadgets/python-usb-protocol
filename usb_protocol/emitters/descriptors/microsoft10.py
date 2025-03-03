#
# This file is part of usb_protocol.
#
""" Convenience emitters Microsoft OS 1.0 Descriptors. """

import unittest

from contextlib import contextmanager

from ..           import emitter_for_format
from ..descriptor import ComplexDescriptorEmitter

from ...types.descriptors.microsoft10 import (
    ExtendedCompatIDDescriptor,
    ExtendedCompatIDDescriptorFunction,
    ExtendedPropertiesDescriptor,
    ExtendedPropertiesDescriptorSection,
    RegistryTypes
)


# Create our basic emitters...
ExtendedCompatIDDescriptorFunctionEmitter = emitter_for_format(ExtendedCompatIDDescriptorFunction)

# ... and complex emitters.
class ExtendedCompatIDDescriptorEmitter(ComplexDescriptorEmitter):
    """ Emitter that creates a ExtendedCompatIDDescriptor """
    DESCRIPTOR_FORMAT = ExtendedCompatIDDescriptor

    @contextmanager
    def Function(self):
        """ Context manager that allows addition of a function section to the descriptor.

        It can be used with a `with` statement; and yields an ExtendedCompatIDDescriptorFunctionEmitter
        that can be populated:

            with d.Function() as f:
                f.bFirstInterfaceNumber = 0
                f.compatibleID          = 'WINUSB'

        This adds the relevant descriptor, automatically.
        """
        descriptor = ExtendedCompatIDDescriptorFunctionEmitter()
        yield descriptor

        self.add_subordinate_descriptor(descriptor)

    def _pre_emit(self):
        self.bCount = len(self._subordinates)


class ExtendedPropertiesDescriptorEmitter(ComplexDescriptorEmitter):
    """ Emitter that creates a ExtendedPropertiesDescriptor """

    DESCRIPTOR_FORMAT = ExtendedPropertiesDescriptor

    @contextmanager
    def Property(self):
        """ Context manager that allows addition of a property section to the descriptor.

        It can be used with a `with` statement; and yields an ExtendedPropertiesDescriptorSectionEmitter
        that can be populated:

            with d.Property() as p:
                p.dwPropertyDataType = RegistryTypes.REG_EXPAND_SZ
                p.PropertyName       = "Icons"
                p.PropertyData       = "%SystemRoot%\\system32\\shell32.dll,-233"

        This adds the relevant descriptor, automatically.
        """
        descriptor = ExtendedPropertiesDescriptorSectionEmitter()
        yield descriptor
        
        self.add_subordinate_descriptor(descriptor)

    def _pre_emit(self):
        self.wCount   = len(self._subordinates)
        self.dwLength = 10 + sum(len(s) for s in self._subordinates)


class ExtendedPropertiesDescriptorSectionEmitter(ComplexDescriptorEmitter):
    """ Emitter that creates a ExtendedPropertiesDescriptorSection """

    DESCRIPTOR_FORMAT = ExtendedPropertiesDescriptorSection

    def _pre_emit(self):
        if self.dwPropertyDataType in (RegistryTypes.REG_SZ, RegistryTypes.REG_EXPAND_SZ, RegistryTypes.REG_LINK):
            self.PropertyData = self.PropertyData.encode('utf_16_le') + b'\0\0'
        elif self.dwPropertyDataType == RegistryTypes.REG_DWORD_LITTLE_ENDIAN:
            self.PropertyData = self.PropertyData.to_bytes(4, 'little')
        elif self.dwPropertyDataType == RegistryTypes.REG_DWORD_BIG_ENDIAN:
            self.PropertyData = self.PropertyData.to_bytes(4, 'big')
        elif self.dwPropertyDataType == RegistryTypes.REG_MULTI_SZ:
            strings = b''
            for string in self.PropertyData:
                strings += string.encode('utf_16_le') + b'\0\0'
            self.PropertyData = strings


class MicrosoftOS10DescriptorCollection:
    """ Object that builds a full collection of Microsoft OS 1.0 descriptors. """

    def __init__(self):
        self._descriptors = {}

    def add_descriptor(self, descriptor, index=None):
        """ Adds a descriptor to our collection.

        Parameters:
            descriptor      -- The descriptor to be added.
            index           -- The index of the relevant descriptor. Defaults to None.
        """

        # If this is an emitter rather than a descriptor itself, convert it.
        if hasattr(descriptor, 'emit'):
            descriptor = descriptor.emit()

        # Figure out the index for this descriptor...
        if index is None:
            index = (descriptor[7] << 8) | descriptor[6]

        # ... and store it.
        self._descriptors[index] = descriptor

    @contextmanager
    def ExtendedCompatIDDescriptor(self):
        descriptor = ExtendedCompatIDDescriptorEmitter()
        yield descriptor
        self.add_descriptor(descriptor)

    @contextmanager
    def ExtendedPropertiesDescriptor(self):
        descriptor = ExtendedPropertiesDescriptorEmitter()
        yield descriptor
        self.add_descriptor(descriptor)

    def __iter__(self):
        return ((index, descriptor) for index, descriptor in self._descriptors.items())



class MicrosoftOS10EmitterTests(unittest.TestCase):

    def test_compat_id_descriptor(self):

        # From Extended Compat ID OS Feature Descriptor Specification, Annex 1
        descriptor = bytes([
            0x58, 0x00, 0x00, 0x00,                         # Descriptor length
            0x00, 0x01,                                     # Version 1.00
            0x04, 0x00,                                     # Extended compat ID descriptor
            0x03,                                           # Number of function sections
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,       # Reserved / padding

            # Function Section 1
            0x00,                                           # First interface number
            0x01,                                           # Reserved
            0x52, 0x4e, 0x44, 0x49, 0x53, 0x00, 0x00, 0x00, # compatibleID
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, # subCompatibleID
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00,             # Reserved / padding
            
            # Function Section 2
            0x02,                                           # First interface number
            0x01,                                           # Reserved
            0x4d, 0x54, 0x50, 0x00, 0x00, 0x00, 0x00, 0x00, # compatibleID
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, # subCompatibleID
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00,             # Reserved / padding
            
            # Function section 3
            0x03,                                           # First interface number
            0x01,                                           # Reserved
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, # compatibleID
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, # subCompatibleID
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00              # Reserved / padding
        ])

        # Create a trivial configuration descriptor...
        collection = MicrosoftOS10DescriptorCollection()

        with collection.ExtendedCompatIDDescriptor() as d:
            with d.Function() as i:
                i.bFirstInterfaceNumber = 0
                i.compatibleID          = 'RNDIS'
            with d.Function() as i:
                i.bFirstInterfaceNumber = 2
                i.compatibleID          = 'MTP'
            with d.Function() as i:
                i.bFirstInterfaceNumber = 3

        # ... and validate that it maches our reference descriptor.
        results = list(collection)
        self.assertEqual(results[0], (4, descriptor))


    def test_extended_properties_descriptor(self):

        # Based on the Appendix from Extended Properties OS Feature Descriptor Specification
        descriptor = bytes([
            # Header
            0xa2, 0x00, 0x00, 0x00,  # total descriptor length
            0x00, 0x01,              # bcdVersion
            0x05, 0x00,              # wIndex
            0x02, 0x00,              # Number of custom properties

            # Custom property 1
            0x68, 0x00, 0x00, 0x00,                                                  # Size of this custom property section
            0x02, 0x00, 0x00, 0x00,                                                  # Property data format
            0x0c, 0x00,                                                              # Property name length
            0x49, 0x00, 0x63, 0x00, 0x6f, 0x00, 0x6e, 0x00, 0x73, 0x00, 0x00, 0x00,  # Property name
            0x4e, 0x00, 0x00, 0x00,                                                  # Length of the property data
            0x25, 0x00, 0x53, 0x00, 0x79, 0x00, 0x73, 0x00, 0x74, 0x00, 0x65, 0x00,  # Property data
            0x6d, 0x00, 0x52, 0x00, 0x6f, 0x00, 0x6f, 0x00, 0x74, 0x00, 0x25, 0x00, 
            0x5c, 0x00, 0x73, 0x00, 0x79, 0x00, 0x73, 0x00, 0x74, 0x00, 0x65, 0x00, 
            0x6d, 0x00, 0x33, 0x00, 0x32, 0x00, 0x5c, 0x00, 0x73, 0x00, 0x68, 0x00, 
            0x65, 0x00, 0x6c, 0x00, 0x6c, 0x00, 0x33, 0x00, 0x32, 0x00, 0x2e, 0x00, 
            0x64, 0x00, 0x6c, 0x00, 0x6c, 0x00, 0x2c, 0x00, 0x2d, 0x00, 0x32, 0x00,
            0x33, 0x00, 0x33, 0x00, 0x00, 0x00,
            
            # Custom property 2
            0x30, 0x00, 0x00, 0x00,                                                  # Size of this custom property section
            0x01, 0x00, 0x00, 0x00,                                                  # Property data format
            0x0c, 0x00,                                                              # Property name length
            0x4c, 0x00, 0x61, 0x00, 0x62, 0x00, 0x65, 0x00, 0x6c, 0x00, 0x00, 0x00,  # Property name
            0x16, 0x00, 0x00, 0x00,                                                  # Length of the property data
            0x58, 0x00, 0x59, 0x00, 0x5a, 0x00, 0x20, 0x00, 0x44, 0x00, 0x65, 0x00,  # Property data
            0x76, 0x00, 0x69, 0x00, 0x63, 0x00, 0x65, 0x00, 0x00, 0x00,
        ])

        # Create a trivial configuration descriptor...
        collection = MicrosoftOS10DescriptorCollection()

        with collection.ExtendedPropertiesDescriptor() as d:
            with d.Property() as p:
                p.dwPropertyDataType = RegistryTypes.REG_EXPAND_SZ
                p.PropertyName       = "Icons"
                p.PropertyData       = "%SystemRoot%\\system32\\shell32.dll,-233"
            with d.Property() as p:
                p.dwPropertyDataType = RegistryTypes.REG_SZ
                p.PropertyName       = "Label"
                p.PropertyData       = "XYZ Device"

        # ... and validate that it maches our reference descriptor.
        results = list(collection)
        self.assertEqual(results[0], (5, descriptor))


if __name__ == "__main__":
    unittest.main()
