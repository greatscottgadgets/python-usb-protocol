#
# This file is part of usb_protocol.
#
""" Convenience emitters for USB Audio Class 1 descriptors. """

from contextlib import contextmanager

from ...types.descriptors.uac1 import *

AudioControlInterruptEndpointDescriptorEmitter  = emitter_for_format(AudioControlInterruptEndpointDescriptor)
