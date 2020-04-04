#
# This file is part of usb-protocol.
#
""" Type elements for defining USB descriptors. """

import unittest
import construct

class DescriptorFormat(construct.Struct):

    @staticmethod
    def _to_detail_dictionary(descriptor, use_pretty_names=True):
        result = {}

        # Loop over every entry in our descriptor context, and try to get a
        # fancy name for it.
        for key, value in descriptor.items():

            # Don't include any underscore-prefixed private members.
            if key.startswith('_'):
                continue

            # If there's no definition for the given key in our format, # skip it.
            if not hasattr(descriptor._format, key):
                continue

            # Try to apply any documentation on the given field rather than it's internal name.
            format_element = getattr(descriptor._format, key)
            detail_key = format_element.docs if (format_element.docs and use_pretty_names) else key

            # Finally, add the entry to our dict.
            result[detail_key] = value

        return result


    def parse(self, data, **context_keywords):
        """ Hook on the parent parse() method which attaches a few methods. """

        # Use construct to run the parse itself...
        result = super().parse(bytes(data), **context_keywords)

        # ... and then bind our static to_detail_dictionary to it.
        result._format = self
        result._to_detail_dictionary = self._to_detail_dictionary.__get__(result, type(result))

        return result


class DescriptorNumber(construct.Const):
    """ Trivial wrapper class that denotes a particular Const as the descriptor number. """

    def __init__(self, const):

        # If our descriptor number is an integer, instead of "raw",
        # convert it to a byte, first.
        if not isinstance(const, bytes):
            const = const.to_bytes(1, byteorder='little')

        # Grab the inner descriptor number represented by the constant.
        self.number = int.from_bytes(const, byteorder='little')

        # And pass this to the core constant class.
        super().__init__(const)

        # Finally, add a documentation string for the type.
        self.docs = "Descriptor type"


    def _parse(self, stream, context, path):
        const_bytes = super()._parse(stream, context, path)
        return const_bytes[0]


    def get_descriptor_number(self):
        """ Returns this constant's associated descriptor number."""
        return self.number


class BCDFieldAdapter(construct.Adapter):
    """ Construct adapter that dynamically parses BCD fields. """

    def _decode(self, obj, context, path):
        hex_string = f"{obj:04x}"
        return float(f"{hex_string[0:2]}.{hex_string[2:]}")


    def _encode(self, obj, context, path):

        # Ensure the data is parseable.
        if (obj * 100) % 1:
            raise AssertionError("BCD fields must be in the format XX.YY")

        # Break the object down into its component parts...
        integer = int(obj)
        percent = int((obj * 100) % 100)

        # ... and squish them into an integer.
        return int(f"{integer:02}{percent:02}", 16)



class DescriptorField(construct.Subconstruct):
    """
    Construct field definition that automatically adds fields of the proper
    size to Descriptor definitions.
    """

    #
    # The C++-wonk operator overloading is Construct, not me, I swear.
    #

    # FIXME: these are really primitive views of these types;
    # we should extend these to get implicit parsing wherever possible
    USB_TYPES = {
        'b'   : construct.Int8ul,
        'bcd' : BCDFieldAdapter(construct.Int16ul),  # TODO: Create a BCD parser for this
        'i'   : construct.Int8ul,
        'id'  : construct.Int16ul,
        'bm'  : construct.Int8ul,
        'w'   : construct.Int16ul,
    }

    @staticmethod
    def _get_prefix(name):
        """ Returns the lower-case prefix on a USB descriptor name. """
        prefix = []

        # Silly loop that continues until we find an uppercase letter.
        # You'd be aghast at how the 'pythonic' answers look.
        for c in name:

            # Ignore leading underscores.
            if c == '_':
                continue

            if c.isupper():
                break
            prefix.append(c)

        return ''.join(prefix)


    @classmethod
    def _get_type_for_name(cls, name):
        """ Returns the type that's appropriate for a given descriptor field name. """

        try:
            return cls.USB_TYPES[cls._get_prefix(name)]
        except KeyError:
            raise ValueError("field names must be formatted per the USB standard!")


    def __init__(self, description="", default=None):
        self.description = description
        self.default = default


    def __rtruediv__(self, field_name):
        field_type = self._get_type_for_name(field_name)

        if self.default is not None:
            field_type = construct.Default(field_type, self.default)

        # Build our subconstruct. Construct makes this look super weird,
        # but this is actually "we have a field with <field_name> of type <field_type>".
        # In long form, we'll call it "description".
        return (field_name / field_type) * self.description


# Convenience type that gets a descriptor's own length.
DescriptorLength = \
     construct.Rebuild(construct.Int8ul, construct.len_(construct.this)) \
     * "Descriptor Length"
