import unittest

from contextlib import contextmanager

from ..           import emitter_for_format
from ..descriptor import ComplexDescriptorEmitter
from ...types.descriptors.hid import \
    HIDDescriptor as HIDDescriptorType
from ...types.descriptors.hid import *

ReportDescriptorEmitter = emitter_for_format(ReportDescriptor)

_hid_item_length = [ 0, 1, 2, 4 ]

class HIDDescriptor(ComplexDescriptorEmitter):
    DESCRIPTOR_FORMAT = HIDDescriptorType

    def add_report_raw(self, report_data):
        """Append raw report item or bytes to HID report

        Arguments:
        report_data -- bytes-like or ReportDescriptor to be appended to
                       the HID report.
        """
        self._reports.append(hid_data)

    def add_report_item(self, report_prefix, *report_data):
        """Convenience function to add formatted HID report item

        Arguments:
        report_prefix -- HIDPrefix enum representing report item type
        *report_data  -- Additional bytes-like report item data.
                         Valid lengths are 1, 2, or 4 bytes.
        """
        hid_report = ReportDescriptorEmitter()
        report_len = _hid_item_length.index(len(report_data))
        hid_report.bHeader = {
            "prefix": report_prefix,
            "bSize":  report_len
        }
        hid_report.data = report_data
        self._reports.append(hid_report)

    def add_input_item(self,
                  data_constant = False,
                  array_variable = True,
                  absolute_relative = False,
                  wrap = False,
                  linear = False,
                  preferred = True,
                  null = False,
                  volatile = False):
        """Convenience function to add HID input item with preformatted flags.
           See HID 1.11 section 6.2.2.5 for flag meanings.
        """
        item_flags = ItemFlags.build({
            "data_constant": data_constant,
            "array_variable": array_variable,
            "absolute_relative": absolute_relative,
            "wrap": wrap,
            "linear": linear,
            "nPreferred": ~preferred,
            "null": null,
            "volatile": volatile,
        })
        self.add_report(HIDPrefix.INPUT, ord(item_flags))

    def add_output_item(self,
                  data_constant = False,
                  array_variable = True,
                  absolute_relative = False,
                  wrap = False,
                  linear = False,
                  preferred = True,
                  null = False,
                  volatile = False):
        """Convenience function to add HID output item with preformatted flags.
           See HID 1.11 section 6.2.2.5 for flag meanings.
        """
        item_flags = ItemFlags.build({
            "data_constant": data_constant,
            "array_variable": array_variable,
            "absolute_relative": absolute_relative,
            "wrap": wrap,
            "linear": linear,
            "nPreferred": ~preferred,
            "null": null,
            "volatile": volatile,
        })
        self.add_report(HIDPrefix.OUTPUT, ord(item_flags))

    def __init__(self, parent_descriptor):
        super().__init__()
        # The HID Report Descriptor sits under a different USB Descriptor,
        # we need access to the descriptor root to create this.
        self._parent_descriptor = parent_descriptor
        self._reports = []

    def _pre_emit(self):
        report_descriptor = []
        for report in self._reports:
            if hasattr(report, "emit"):
                report_descriptor.append(report.emit()) 
            else:
                report_descriptor.append(report)
        report_descriptor = b"".join(report_descriptor)
        descriptor_len = len(report_descriptor)
        self.wDescriptorLength = descriptor_len
        self._parent_descriptor.add_descriptor(report_descriptor, 0x22)