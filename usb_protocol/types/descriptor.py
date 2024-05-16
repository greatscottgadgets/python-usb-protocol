#
# This file is part of usb-protocol.
#
""" Type elements for defining USB descriptors. """

import unittest
import construct

class DescriptorFormat(construct.Struct):
    """
    Creates a Construct structure for a USB descriptor, and a corresponding version that
    supports parsing incomplete binary as `DescriptorType.Partial`, e.g. `DeviceDescriptor.Partial`.
    """

    def __init__(self, *subcons, _create_partial=True, **subconskw):

        if _create_partial:
            self.Partial = self._create_partial(*subcons, **subconskw) # pylint: disable=invalid-name

        super().__init__(*subcons, **subconskw)


    @classmethod
    def _get_subcon_field_type(cls, subcon):
        """ Gets the actual field type for a Subconstruct behind arbitrary levels of `Renamed`s."""

        # DescriptorFields are usually `<Renamed <Renamed <FormatField>>>`.
        # The type behind the `Renamed`s is the one we're interested in, so let's recursively examine
        # the child Subconstruct until we get to it.

        if not isinstance(subcon, construct.Renamed):
            return subcon
        else:
            return cls._get_subcon_field_type(subcon.subcon)


    @classmethod
    def _create_partial(cls, *subcons, **subconskw):
        """ Creates a version of the descriptor format for parsing incomplete binary data as a descriptor.

        This essentially wraps every field after bLength and bDescriptorType in a `construct.Optional`.
        """

        def _apply_optional(subcon):

            subcon_type = cls._get_subcon_field_type(subcon)

            #
            # If it's already Optional then we don't need to apply it again.
            #
            if isinstance(subcon_type, construct.Select):
                # construct uses a weird singleton to define Pass. `construct.core.Pass` would normally be
                # the type's name, but then they create a singleton of that same name, replacing that name and
                # making the type technically unnamable and only accessable via `type()`.
                if isinstance(subcon_type.subcons[1], type(construct.Pass)):
                    return subcon

            return (subcon.name / construct.Optional(subcon_type)) * subcon.docs

        # First store the Subconstructs we don't want to modify: bLength and bDescriptorType,
        # as these are never optional.
        new_subcons = list(subcons[0:2])

        # Then apply Optional to all of the rest of the Subconstructs.
        new_subcons.extend([_apply_optional(subcon) for subcon in subcons[2:]])

        return DescriptorFormat(*new_subcons, _create_partial=False, **subconskw)


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

        # Break the object down into its component parts...
        integer = int(obj) % 100
        percent = int(round(obj * 100)) % 100

        # ... make sure nothing is lost during conversion...
        if float(f"{integer:02}.{percent:02}") != obj:
            raise AssertionError("BCD fields must be in the format XX.YY")

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
        'dw'  : construct.Int32ul,
    }


    LENGTH_TYPES = {
        1: construct.Int8ul,
        2: construct.Int16ul,
        3: construct.Int24ul,
        4: construct.Int32ul,
        8: construct.Int64ul
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


    def __init__(self, description="", default=None, *, length=None):
        self.description = description
        self.default = default
        self.length = length


    def __rtruediv__(self, field_name):
        # If we have a length, use it to figure out the type.
        # Otherwise, extract the type from the prefix. (Using a length
        # is useful for e.g. USB3 bitfields; which can span several bytes.)
        if self.length is not None:
            field_type = self.LENGTH_TYPES[self.length]
        else:
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
