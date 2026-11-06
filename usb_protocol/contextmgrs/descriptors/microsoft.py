#
# This file is part of usb-protocol.
#

from ...emitters.descriptors.microsoft import (
	PlatformDescriptorCollection, PlatformDescriptorEmitter
)
from ...emitters.descriptors.standard  import BinaryObjectStoreDescriptorEmitter
from ..manager                         import DescriptorContextManager

class PlatformDescriptor(DescriptorContextManager):
	ParentDescriptor = BinaryObjectStoreDescriptorEmitter

	def DescriptorEmitter(self) -> PlatformDescriptorEmitter:
		return PlatformDescriptorEmitter(platform_collection = self._platform_collection)

	def __init__(
		self, parentDesc: ParentDescriptor, platform_collection: PlatformDescriptorCollection
	) -> None:
		self._platform_collection = platform_collection
		super().__init__(parentDesc)
