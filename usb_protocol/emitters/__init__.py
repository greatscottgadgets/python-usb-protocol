#
# This file is part of usb-protocol.
#
""" USB-related emitters. """

from .construct_interop    import emitter_for_format, ConstructEmitter
from .descriptors.standard import DeviceDescriptorCollection, SuperSpeedDeviceDescriptorCollection
