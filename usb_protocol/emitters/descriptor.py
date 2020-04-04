#
# This file is part of usb-protocol.
#


from . import ConstructEmitter
from collections import defaultdict

class ComplexDescriptorEmitter(ConstructEmitter):
    """ Base class for emitting complex descriptors, which contain nested subordinates. """

    # Base classes should override this.
    DESCRIPTOR_FORMAT = None

    def __init__(self):

        # Always create a basic ConstructEmitter from the given format.
        super().__init__(self.DESCRIPTOR_FORMAT)

        # Store a list of subordinate descriptors, and a count of
        # subordinate descriptor types.
        self._subordinates = []
        self._type_counts = {}


    def add_subordinate_descriptor(self, subordinate):
        """ Adds a subordinate descriptor to the relevant descriptor.

        Parameter:
            subordinate -- The subordinate descriptor to add; can be an emitter,
                           or a bytes-like object.
        """

        if hasattr(subordinate, 'emit'):
            subordinate = subordinate.emit()
        else:
            subordinate = bytes(subordinate)

        # The second byte of a given descriptor is always its type number.
        # Count this descriptor type...
        subordinate_type = subordinate[1]

        try:
            self._type_counts[subordinate_type] += 1
        except KeyError:
            self._type_counts[subordinate_type] = 1

        # ... and add the relevant bytes to our list of subordinates.
        self._subordinates.append(subordinate)


    def emit(self, include_subordinates=True):
        """ Emit our descriptor.

        Parameters:
            include_subordinates -- If true or not provided, any subordinate descriptors will be included.
        """

        result = bytearray()

        # Add our basic descriptor...
        result.extend(super().emit())

        # ... and if descired, add our subordinates...
        for sub in self._subordinates:
            result.extend(sub)

        return bytes(result)
