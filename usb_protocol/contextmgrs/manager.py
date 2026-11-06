#
# This file is part of usb-protocol.
#

from ..emitters.descriptor import ComplexDescriptorEmitter


class DescriptorContextManager:
	ParentDescriptor = ComplexDescriptorEmitter
	DescriptorEmitter = None

	def __init__(self, parentDesc: ParentDescriptor) -> None:
		self._parent = parentDesc
		self._descriptor = self.DescriptorEmitter()

	def __enter__(self):
		return self._descriptor

	def __exit__(self, exc_type, exc_value, traceback):
		# If an exception was raised, fast exit
		if not (exc_type is None and exc_value is None and traceback is None):
			return
		self._parent.add_subordinate_descriptor(self._descriptor)
