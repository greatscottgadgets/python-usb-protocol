#
# This file is part of usb-protocol.
#
""" Type elements for defining USB descriptors. """

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
        'b'   : construct.Optional(construct.Int8ul),
        'bcd' : construct.Optional(construct.Int16ul),  # TODO: Create a BCD parser for this
        'i'   : construct.Optional(construct.Int8ul),
        'id'  : construct.Optional(construct.Int16ul),
        'bm'  : construct.Optional(construct.Int8ul),
        'w'   : construct.Optional(construct.Int16ul),
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


    def __init__(self, description=""):
        self.description = description


    def __rtruediv__(self, field_name):
        field_type = self._get_type_for_name(field_name)

        # wew does construct make this look weird
        return (field_name / field_type) * self.description
