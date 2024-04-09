#
# This file is part of usb-protocol.
#
'''
Structures describing Microsoft OS 1.0 Descriptors.
'''

from enum         import IntEnum

import construct
from   construct  import len_, this

from ..descriptor import DescriptorField, DescriptorFormat


class RegistryTypes(IntEnum):
    """ Standard Windows registry data types, used in the extended properties descriptor """
    REG_SZ                  = 1
    REG_EXPAND_SZ           = 2
    REG_BINARY              = 3
    REG_DWORD_LITTLE_ENDIAN = 4
    REG_DWORD_BIG_ENDIAN    = 5
    REG_LINK                = 6
    REG_MULTI_SZ            = 7


# Extended Compat ID descriptor
ExtendedCompatIDDescriptor = DescriptorFormat(
    'dwLength'              / construct.Rebuild(construct.Int32ul, 16 + this.bCount * 24),
    'bcdVersion'            / construct.Const(0x0100, construct.Int16ul),
    'wIndex'                / construct.Const(0x0004, construct.Int16ul),
    'bCount'                / DescriptorField("Number of function sections"),
    'reserved'              / construct.Padding(7),
)

ExtendedCompatIDDescriptorFunction = DescriptorFormat(
    'bFirstInterfaceNumber' / DescriptorField("Interface number"),
    'bReserved'             / construct.Const(0x01, construct.Int8ul),
    'compatibleID'          / construct.Default(construct.PaddedString(8, 'ascii'), ""),
    'subCompatibleID'       / construct.Default(construct.PaddedString(8, 'ascii'), ""),
    'reserved'              / construct.Padding(6),
)


# Extended properties descriptor
ExtendedPropertiesDescriptor = DescriptorFormat(
    'dwLength'              / DescriptorField("Length of the complete extended properties descriptor", length=4),
    'bcdVersion'            / construct.Const(0x0100, construct.Int16ul),
    'wIndex'                / construct.Const(0x0005, construct.Int16ul),
    'wCount'                / DescriptorField("Number of custom property sections"),
)

ExtendedPropertiesDescriptorSection = DescriptorFormat(
    'dwSize'                / construct.Rebuild(construct.Int32ul, 14 + 2 * len_(this.PropertyName) + 2 + len_(this.PropertyData)),
    'dwPropertyDataType'    / DescriptorField('Data type of the registry property', length=4),
    'wPropertyNameLength'   / construct.Rebuild(construct.Int16ul, 2 * len_(this.PropertyName) + 2),
    'PropertyName'          / construct.CString('utf_16_le'),
    'dwPropertyDataLength'  / construct.Rebuild(construct.Int32ul, len_(this.PropertyData)),
    'PropertyData'          / construct.GreedyBytes,
)
