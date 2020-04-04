#
# This file is part of usb-protocol.
#
""" Helpers for creating easy emitters. """

import unittest
import construct

class ConstructEmitter:
    """ Class that creates a simple emitter based on a construct struct.

    For example, if we have a construct format that looks like the following:
        MyStruct = struct(
            "a" / Int8
            "b" / Int8
        )

    We could create emit an object like follows:
        emitter   = ConstructEmitter(MyStruct)
        emitter.a = 0xab
        emitter.b = 0xcd
        my_bytes  = emitter.emit() # "\xab\xcd"
    """

    def __init__(self, struct):
        """
        Parmeters:
            construct_format -- The format for which to create an emitter.
        """
        self.__dict__['format'] = struct
        self.__dict__['fields'] = {}


    def _format_contains_field(self, field_name):
        """ Returns True iff the given format has a field with the provided name.

        Parameters:
            format_object -- The Construct format to work with. This includes e.g. most descriptor types.
            field_name    -- The field name to query.
        """
        return any(f.name == field_name for f in self.format.subcons)


    def __setattr__(self, name, value):
        """ Hook that we used to set our fields. """

        # If the field starts with a '_', don't handle it, as it's an internal field.
        if name.startswith('_'):
            super().__setattr__(name, value)
            return

        if not self._format_contains_field(name):
            raise AttributeError(f"emitter specification contains no field {name}")

        self.fields[name] = value


    def emit(self):
        """ Emits the stream of bytes associated with this object. """

        try:
            return self.format.build(self.fields)
        except KeyError as e:
            raise KeyError(f"missing necessary field: {e}")



class ConstructEmitterTest(unittest.TestCase):

    def test_simple_emitter(self):

        test_struct = construct.Struct(
            "a" / construct.Int8ul,
            "b" / construct.Int8ul
        )

        emitter   = ConstructEmitter(test_struct)
        emitter.a = 0xab
        emitter.b = 0xcd

        self.assertEqual(emitter.emit(), b"\xab\xcd")


def emitter_for_format(construct_format):
    """ Creates a factory method for the relevant construct format. """

    def _factory():
        return ConstructEmitter(construct_format)

    return _factory


if __name__ == "__main__":
    unittest.main()
