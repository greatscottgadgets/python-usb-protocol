""" Convenience aliases for versions of descriptor structs that support parsing incomplete binary data. """

from .. import standard

DeviceDescriptor          = standard.DeviceDescriptor.Partial
ConfigurationDescriptor   = standard.ConfigurationDescriptor.Partial
StringDescriptor          = standard.StringDescriptor.Partial
StringLanguageDescriptor  = standard.StringLanguageDescriptor.Partial
InterfaceDescriptor       = standard.InterfaceDescriptor.Partial
EndpointDescriptor        = standard.EndpointDescriptor.Partial
DeviceQualifierDescriptor = standard.DeviceQualifierDescriptor.Partial
