# Lint as: python3
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Module defines and lists all the rules for validating SMBIOS info.

Usage Example:
Rule(
    matcher.Matcher([matcher.RecordTypeMatcher(constants.RecordType.BIOS_RECORD)]),
    validator.IndividualValidator([validator.FieldPresentChecker('Vendor')]),
    'ERROR: Vendor field is missing in BIOS information record (DMI type 0).',
    'ACTION: Please populate Vendor field with correct vendor name.')

This rule will match SMBIOS records with DMI type 0, and validate if field
'Vendor' is present. If not, the error message and suggested actions will be
printed out.
"""

from smbios_validation_tool import constants
from smbios_validation_tool import matcher
from smbios_validation_tool import validator


class Rule:
  """Class that defines a rule for validating SMBIOS records.

  Attributes:
    matchers: a list of matchers. A record is matched if and only if all the
      matchers are matched.
    validators: a list of validators. A record is valid if and only if all the
      validators are valid.
    err_msg: a string stores the error message if SMBIOS record is invalid.
    action_msg: a string stores suggested actions to correct error if SMBIOS
      record is invalid.
  """

  def __init__(self, matchers, validators, err_msg, action_msg):
    self.matchers = matchers
    self.validators = validators
    self.err_msg = err_msg
    self.action_msg = action_msg

rules = [
    # Rules for Type 0 (BIOS information) record
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.BIOS_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Vendor'),
            validator.FieldValueRegexpChecker('Vendor', r'.*Google.*')
        ]), 'ERROR: Invalid Vendor field in Type 0 (BIOS Information) record.',
        ('ACTION: BIOS Vendor string should contain "Google".\n'
         'Without that our software will ignore the OEM structures.')),
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.BIOS_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Version'),
        ]), 'ERROR: Invalid Version field in Type 0 (BIOS Information) record.',
        ('ACTION: BIOS Version can be any string as long as it follows properly documented procedure.\n'
         'If none available please follow the XX.YY.RR format.')),
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.BIOS_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Release Date'),
            validator.FieldValueRegexpChecker(
                'Release Date', constants.FieldValueRegexps.DATE_REGEXP.value)
        ]),
        'ERROR: Invalid Release Date field in Type 0 (BIOS Information) record.',
        'ACTION: Please populate BIOS Release Date field with correct date (format is MM/DD/YYYY).'
    ),
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.BIOS_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('ROM Size'),
            validator.FieldValueRegexpChecker('ROM Size', r'\d+ [kmgKMG]B')
        ]),
        'ERROR: Invalid ROM Size field in Type 0 (BIOS Information) record.',
        ('ACTION: Please populate BIOS ROM Size field with valid size.\n'
         '*BIOS ROM Size indicates the BIOS size not the flash part size.*')),

    # Rules for Type 2 (Board Information) records
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.BASEBOARD_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Manufacturer'),
        ]),
        'ERROR: Invalid Manufacturer field in Type 2 (Board Information) record.',
        'ACTION: Please populate Manufacturer field with valid string.'),
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.BASEBOARD_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Product Name'),
        ]),
        'ERROR: Invalid Product field in Type 2 (Board Information) record.',
        'ACTION: Please populate Product field with valid string.'),
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.BASEBOARD_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Features'),
        ]),
        'ERROR: Invalid Features field in Type 2 (Board information) record.',
        ('ACTION: Please populate Features field with valid feature flags.\n'
         'Bit0 - 1 for Motherboard, 0 for daughter boards; Bit3 - 1 for replaceable board.'
        )),
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.BASEBOARD_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Location In Chassis'),
            validator.FieldValueRegexpChecker(
                'Location In Chassis',
                constants.FieldValueRegexps.DEVPATH_REGEXP.value)
        ]),
        'ERROR: Invalid Location In Chassis field in Type 2 (Board Information) record.',
        ('ACTION: Please populate Location In Chassis field with valid devpath.\n'
         'This field provides the devpath for the daughter board.')),
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.BASEBOARD_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Chassis Handle'),
            validator.HandleFieldChecker('Chassis Handle', 3)
        ]),
        'ERROR: Invalid Chassis Handle in Type 2 (Board Information) record.',
        'ACTION: Please populate Chassis Handle field with valid handle.'),
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.BASEBOARD_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Contained Object Handles'),
            validator.FieldItemCountChecker('Contained Object Handles')
        ]),
        'ERROR: Invalid Contained Object Handles field in Type 2 (Board Information) record.',
        'ACTION: Please populate Contained Object Handles field with valid handles.\n'
    ),

    # Rules for Type 3 (Chassis) records
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.CHASSIS_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Manufacturer'),
        ]), 'ERROR: Invalid Manufacturer field in Type 3 (Chassis) record.',
        'ACTION: Please populate Manufacturer field with valid string.'),
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.CHASSIS_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Type'),
            validator.FieldValueEnumChecker(
                'Type', constants.FieldValueEnums.CHASSIS_TYPES.value)
        ]), 'ERROR: Invalid Type field in Type 3 (Chassis) record.',
        ('ACTION: Please populate Type field with valid string.\n'
         'Valid Type(s): ' +
         ', '.join(constants.FieldValueEnums.CHASSIS_TYPES.value))),
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.CHASSIS_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Lock'),
            validator.FieldValueEnumChecker(
                'Lock', constants.FieldValueEnums.CHASSIS_LOCK.value),
        ]), 'ERROR: Invalid Lock field in Type 3 (Chassis) record.',
        ('ACTION: Please populate Lock field with valid string.\n'
         'Valid Lock Status: ' +
         ', '.join(constants.FieldValueEnums.CHASSIS_LOCK.value))),
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.CHASSIS_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('OEM Information'),
            validator.FieldValueRegexpChecker(
                'OEM Information',
                constants.FieldValueRegexps.OEM_FOR_GOOGLE_REGEXP.value),
        ]), 'ERROR: Invalid OEM Information field in Type 3 (Chassis) record.',
        ('ACTION: Please populate OEM Information field with valid hex value.\n'
         'OEM Byte 0 must be 0x67, which is the identification for Google OEM Info.'
        )),
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.CHASSIS_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Contained Elements'),
            validator.FieldValueRegexpChecker(
                'Contained Elements',
                constants.FieldValueRegexps.NUMBER_REGEXP.value),
        ]),
        'ERROR: Invalid Contained Elements field in Type 3 (Chassis) record.',
        'ACTION: Please populate Contained Elements field with valid number.'),

    # Rules for Type 4 (Processor Information) records
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.PROCESSOR_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Socket Designation'),
            validator.FieldValueRegexpChecker(
                'Socket Designation',
                constants.FieldValueRegexps.SOCKET_DESIGNATION_REGEXP.value),
        ]),
        'ERROR: Invalid Socket Designation field in Type 4 (Processor Information) record.',
        ('ACTION: Please populate Socket Designation field with valid string.\n'
         'Processor silkscreen tag usually looks like CPU0, CPU1, etc.')),
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.PROCESSOR_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Type'),
            validator.FieldValueEnumChecker(
                'Type', constants.FieldValueEnums.PROCESSOR_TYPE.value),
        ]),
        'ERROR: Invalid Type field in Type 4 (Processor Information) record.',
        ('ACTION: Please populate Type field with valid string.\n'
         'Valid Processor Type(s): ' +
         ', '.join(constants.FieldValueEnums.PROCESSOR_TYPE.value))),
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.PROCESSOR_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Status'),
            validator.FieldValueEnumChecker(
                'Status', constants.FieldValueEnums.PROCESSOR_STATUS.value),
        ]),
        'ERROR: Invalid Status field in Type 4 (Processor Information) record.',
        ('ACTION: Please populate Status field with valid string.\n'
         'Valid Status: ' +
         ', '.join(constants.FieldValueEnums.PROCESSOR_STATUS.value))),
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.PROCESSOR_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('L1 Cache Handle'),
            validator.HandleFieldChecker('L1 Cache Handle',
                                         constants.RecordType.CACHE_RECORD)
        ]),
        'ERROR: Invalid L1 Cache Handle field in Type 4 (Processor Information) record.',
        'ACTION: Please populate L1 Cache Handle field with valid handle'),
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.PROCESSOR_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('L2 Cache Handle'),
            validator.HandleFieldChecker('L2 Cache Handle',
                                         constants.RecordType.CACHE_RECORD)
        ]),
        'ERROR: Invalid L2 Cache Handle field in Type 4 (Processor Information) record.',
        'ACTION: Please populate L2 Cache Handle field with valid handle'),
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.PROCESSOR_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('L3 Cache Handle'),
            validator.HandleFieldChecker('L3 Cache Handle',
                                         constants.RecordType.CACHE_RECORD)
        ]),
        'ERROR: Invalid L3 Cache Handle field in Type 4 (Processor Information) record.',
        'ACTION: Please populate L3 Cache Handle field with valid handle'),
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.PROCESSOR_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Core Count'),
            validator.FieldValueRegexpChecker(
                'Core Count', constants.FieldValueRegexps.NUMBER_REGEXP.value),
        ]),
        'ERROR: Invalid Core Count field in Type 4 (Processor Information) record.',
        'ACTION: Please populate Core Count field with valid number.\n'),
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.PROCESSOR_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Core Enabled'),
            validator.FieldValueRegexpChecker(
                'Core Enabled',
                constants.FieldValueRegexps.NUMBER_REGEXP.value),
        ]),
        'ERROR: Invalid Core Enabled field in Type 4 (Processor Information) record.',
        'ACTION: Please populate Core Enabled field with valid number.\n'),
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.PROCESSOR_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Thread Count'),
            validator.FieldValueRegexpChecker(
                'Thread Count',
                constants.FieldValueRegexps.NUMBER_REGEXP.value),
        ]),
        'ERROR: Invalid Thread Count field in Type 4 (Processor Information) record.',
        'ACTION: Please populate Thread Count field with valid number.\n'),

    # Rules for Type 9 (System Slots) records
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(constants.RecordType.SYSTEM_SLOTS_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Designation'),
        ]), 'ERROR: Invalid Designation field in Type 9 (System Slots) record.',
        ('ACTION: Please populate Designation field with valid Slot silkscreen.\n'
         'e.g. PE0, PE4, etc.')),
    # TODO(xuhha): check there are no 2 slots sharing same designation.
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(constants.RecordType.SYSTEM_SLOTS_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Type'),
        ]), 'ERROR: Invalid Slot Type field in Type 9 (System Slots) record.',
        ('ACTION: Please populate Slot Type field with valid string.\n'
         'e.g. Proprietary, x8 PCI Express 3 x8, etc.')),
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(constants.RecordType.SYSTEM_SLOTS_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Current Usage'),
            validator.FieldValueEnumChecker(
                'Current Usage',
                constants.FieldValueEnums.SYSTEM_SLOTS_CURRENT_USAGE.value)
        ]),
        'ERROR: Invalid Current Usage field in Type 9 (System Slots) record.',
        ('ACTION: Please populate Current Usage field with valid string.\n'
         'Valid Usage: ' + ', '.join(
             constants.FieldValueEnums.SYSTEM_SLOTS_CURRENT_USAGE.value))),
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(constants.RecordType.SYSTEM_SLOTS_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Length'),
            validator.FieldValueEnumChecker(
                'Length', constants.FieldValueEnums.SYSTEM_SLOTS_LENGTH.value)
        ]), 'ERROR: Invalid Slot Length field in Type 9 (System Slots) record.',
        ('ACTION: Please populate Slot Length field with valid string.\n'
         'Valid Length: ' +
         ', '.join(constants.FieldValueEnums.SYSTEM_SLOTS_LENGTH.value))),
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(constants.RecordType.SYSTEM_SLOTS_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Characteristics'),
        ]),
        'ERROR: Invalid Characteristics field in Type 9 (System Slots) record.',
        ('ACTION: Please populate Characteristics field with valid string.\n'
         'e.g. 3.3 V is provided, UNKNOWN, etc.')),
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(constants.RecordType.SYSTEM_SLOTS_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Bus Address'),
            validator.FieldValueRegexpChecker('Bus Address', r'[\d:.]+'),
        ]), 'ERROR: Invalid Bus Address field in Type 9 (System Slots) record.',
        ('ACTION: Please populate Bus Address field with valid string.\n'
         'e.g. 0000:c0:02.0.')),
    # TODO(xuhha): Check for the actual presence of the PCI device from
    # the above address, using 'lspci'.

    # Rules for Type 14 (Group Associations) records
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(
                constants.RecordType.GROUP_ASSOCIATIONS_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Name'),
        ]), 'ERROR: Invalid Name field in Type 14 (Group Associations) record.',
        ('ACTION: Please populate Name field with valid string.\n'
         'e.g. die0, IMC0, Connector, etc.')),
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(
                constants.RecordType.GROUP_ASSOCIATIONS_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Items'),
            validator.FieldItemCountChecker(
                'Items', compare_function=lambda x: x >= 1),
        ]),
        'ERROR: Invalid Items field in Type 14 (Group Associations) record.',
        ('ACTION: Please populate Items field with valid item count and strings.\n'
         'At least one item must be listed in the record.'),
    ),
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(
                constants.RecordType.GROUP_ASSOCIATIONS_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldItemUniquenessChecker('Items'),
        ]),
        'ERROR: Invalid Items field in Type 14 (Group Associations) record.',
        'Please make sure all handles are unique in items of group associations records.'
    ),

    # Rules for Type 16 (Physical Memory Array) records
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(
                constants.RecordType.PHYSICAL_MEMORY_ARRAY_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Location'),
            validator.FieldValueEnumChecker(
                'Location',
                constants.FieldValueEnums.PHYSICAL_MEMORY_ARRAY_LOCATION.value),
        ]),
        'ERROR: Invalid Location field in Type 16 (Physical Memory Array) record.',
        ('ACTION: Please populate Location field with valid string.\n'
         'Usually 0x03 for System Board/Motherboard.')),
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(
                constants.RecordType.PHYSICAL_MEMORY_ARRAY_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Use'),
            validator.FieldValueEnumChecker(
                'Use',
                constants.FieldValueEnums.PHYSICAL_MEMORY_ARRAY_USE.value),
        ]),
        'ERROR: Invalid Use field in Type 16 (Physical Memory Array) record.',
        ('ACTION: Please populate Use field with valid string.\n'
         'Function for which this array is used. Usually 0x03 for System Memory.'
        )),
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(
                constants.RecordType.PHYSICAL_MEMORY_ARRAY_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Error Correction Type'),
        ]),
        'ERROR: Invalid Error Correction Type field in Type 16 (Physical Memory Array) record.',
        ('ACTION: Please populate Error Correction Type field with valid string.\n'
         'e.g. Multi-bit ECC.')),
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(
                constants.RecordType.PHYSICAL_MEMORY_ARRAY_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Maximum Capacity'),
            validator.FieldValueRegexpChecker(
                'Maximum Capacity',
                constants.FieldValueRegexps.SIZE_REGEXP.value),
        ]),
        'ERROR: Invalid Maximum Capacity field in Type 16 (Physical Memory Array) record.',
        'ACTION: Please populate Maximum Capacity field with valid capacity.'),
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(
                constants.RecordType.PHYSICAL_MEMORY_ARRAY_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Number Of Devices'),
            validator.FieldValueRegexpChecker(
                'Number Of Devices',
                constants.FieldValueRegexps.NUMBER_REGEXP.value),
        ]),
        'ERROR: Invalid Number of Devices field in Type 16 (Physical Memory Array) record.',
        'ACTION: Please populate Number of Devices field with valid number'),

    # Rules for Type 17 (Memory Device) records
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(constants.RecordType.MEMORY_DEVICE_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Array Handle'),
            validator.HandleFieldChecker(
                'Array Handle',
                constants.RecordType.PHYSICAL_MEMORY_ARRAY_RECORD)
        ]),
        'ERROR: Invalid Array Handle field in Type 17 (Memory Device) record.',
        ('ACTION: Please populate Array Handle field with valid handle.\n'
         'This field should be the handle associated with the Physical Memory Array to which this device belongs.'
        )),
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(constants.RecordType.MEMORY_DEVICE_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Total Width'),
            validator.FieldValueRegexpChecker(
                'Total Width', constants.FieldValueRegexps.SIZE_REGEXP.value),
        ]),
        'ERROR: Invalid Total Width field in Type 17 (Memory Device) record.',
        'ACTION: Please populate Total Width field with valid number of bits (or Unknown).'
    ),
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(constants.RecordType.MEMORY_DEVICE_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Data Width'),
            validator.FieldValueRegexpChecker(
                'Data Width', constants.FieldValueRegexps.SIZE_REGEXP.value),
        ]),
        'ERROR: Invalid Data Width field in Type 17 (Memory Device) record.',
        'ACTION: Please populate Data Width field with valid number of bits (or Unknown).'
    ),
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(constants.RecordType.MEMORY_DEVICE_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Size'),
            validator.FieldValueRegexpChecker(
                'Size', constants.FieldValueRegexps.SIZE_REGEXP.value),
        ]), 'ERROR: Invalid Size field in Type 17 (Memory Device) record.',
        'ACTION: Please populate Size field with valid capacity (or No Module Installed).'
    ),
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(constants.RecordType.MEMORY_DEVICE_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Form Factor'),
            validator.FieldValueEnumChecker(
                'Form Factor',
                constants.FieldValueEnums.MEMORY_DEVICE_FORM_FACTOR.value),
        ]),
        'ERROR: Invalid Form Factor field in Type 17 (Memory Device) record.',
        ('ACTION: Please populate Form Factor field with valid string.\n'
         'Valid Form Factor(s): ' +
         ', '.join(constants.FieldValueEnums.MEMORY_DEVICE_FORM_FACTOR.value))),
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(constants.RecordType.MEMORY_DEVICE_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Set'),
            validator.FieldValueRegexpChecker('Set', r'Unknown|None|\w+'),
        ]), 'ERROR: Invalid Set field in Type 17 (Memory Device) record.',
        'ACTION: Please populate Set field with valid string (or Unknown/None).'
    ),
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(constants.RecordType.MEMORY_DEVICE_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Locator'),
            validator.FieldValueRegexpChecker(
                'Locator',
                constants.FieldValueRegexps.DEVICE_LOCATOR_REGEXP.value),
        ]), 'ERROR: Invalid Locator field in Type 17 (Memory Device) record.',
        ('ACTION: Please populate Locator field with valid string.\n'
         'This field is silk screen for the DIMM location. e.g. DIMM0')),
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(constants.RecordType.MEMORY_DEVICE_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Bank Locator'),
            validator.FieldValueRegexpChecker(
                'Bank Locator',
                constants.FieldValueRegexps.BANK_LOCATOR_REGEXP.value),
        ]),
        'ERROR: Invalid Bank Locator field in Type 17 (Memory Device) record.',
        ('ACTION: Please populate Bank Locator field with valid string.\n'
         'This is the string that identifies the physically labeled bank '
         'where the memory device is located.'
        )),
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(constants.RecordType.MEMORY_DEVICE_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Type'),
            validator.FieldValueEnumChecker(
                'Type', constants.FieldValueEnums.MEMORY_DEVICE_TYPES.value),
        ]),
        'ERROR: Invalid Memory Type field in Type 17 (Memory Device) record.',
        ('ACTION: Please populate Memory Type field with valid string.\n'
         'Valid Type(s): ' +
         ', '.join(constants.FieldValueEnums.MEMORY_DEVICE_TYPES.value))),
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(constants.RecordType.MEMORY_DEVICE_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Speed'),
            validator.FieldValueRegexpChecker(
                'Speed', constants.FieldValueRegexps.SPEED_REGEXP.value),
        ]), 'ERROR: Invalid Speed field in Type 17 (Memory Device) record.',
        ('ACTION: Please populate Speed field with valid string.\n'
         'e.g. 2400 MT/s')),
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(constants.RecordType.MEMORY_DEVICE_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Manufacturer'),
        ]),
        'ERROR: Invalid Manufacturer field in Type 17 (Memory Device) record.',
        'ACTION: Please populate Manufacturer field with valid string.'),
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(constants.RecordType.MEMORY_DEVICE_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Serial Number'),
        ]),
        'ERROR: Invalid Serial Number field in Type 17 (Memory Device) record.',
        'ACTION: Please populate Serial Number field with valid string.'),
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(constants.RecordType.MEMORY_DEVICE_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Asset Tag'),
        ]), 'ERROR: Invalid Asset Tag field in Type 17 (Memory Device) record.',
        'ACTION: Please populate Asset Tag field with valid string.'),
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(constants.RecordType.MEMORY_DEVICE_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Part Number'),
        ]),
        'ERROR: Invalid Part Number field in Type 17 (Memory Device) record.',
        'ACTION: Please populate Part Number field with valid string.'),
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(constants.RecordType.MEMORY_DEVICE_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Configured Memory Speed'),
            validator.FieldValueRegexpChecker(
                'Configured Memory Speed',
                constants.FieldValueRegexps.SPEED_REGEXP.value),
        ]),
        'ERROR: Invalid Configured Memory Speed field in Type 17 (Memory Device) record.',
        'ACTION: Please populate Configured Memory Speed field with valid speed.'
    ),

    # Rules for Type 19 (Memory Array Mapped Address) records
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(
                constants.RecordType.MEMORY_ARRAY_MAPPED_ADDRESS_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Starting Address'),
            validator.FieldValueRegexpChecker(
                'Starting Address',
                constants.FieldValueRegexps.HEX_REGEXP.value),
        ]),
        'ERROR: Invalid Starting Address field in Type 19 (Memory Array Mapped Address) record.',
        'ACTION: Please populate Starting Address field with valid address.'),
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(
                constants.RecordType.MEMORY_ARRAY_MAPPED_ADDRESS_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Ending Address'),
            validator.FieldValueRegexpChecker(
                'Ending Address', constants.FieldValueRegexps.HEX_REGEXP.value),
        ]),
        'ERROR: Invalid Ending Address field in Type 19 (Memory Array Mapped Address) record.',
        'ACTION: Please populate Ending Address field with valid address.'),
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(
                constants.RecordType.MEMORY_ARRAY_MAPPED_ADDRESS_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Physical Array Handle'),
            validator.HandleFieldChecker(
                'Physical Array Handle',
                constants.RecordType.PHYSICAL_MEMORY_ARRAY_RECORD),
        ]),
        'ERROR: Invalid Physical Array Handle field in Type 19 (Memory Array Mapped Address) record.',
        'ACTION: Please populate Physical Array Handle field with valid handle.'
    ),
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(
                constants.RecordType.MEMORY_ARRAY_MAPPED_ADDRESS_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Partition Width'),
            validator.FieldValueRegexpChecker(
                'Partition Width',
                constants.FieldValueRegexps.NUMBER_REGEXP.value),
        ]),
        'ERROR: Invalid Partition Width field in Type 19 (Memory Array Mapped Address) record.',
        ('ACTION: Please populate Partition Width field with valid number.\n',
         'Partition Width is the number of Memory Devices that form a single row of memory ',
         'for the address partition defined by this structure.')),

    # Rules for Memory Device Mapped Address (Type 20) records
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(
                constants.RecordType.MEMORY_DEVICE_MAPPED_ADDRESS_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Starting Address'),
            validator.FieldValueRegexpChecker(
                'Starting Address',
                constants.FieldValueRegexps.HEX_REGEXP.value),
        ]),
        'ERROR: Invalid Starting Address field in Type 20 (Memory Device Mapped Address) record.',
        'ACTION: Please populate Starting Address field with valid address.'),
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(
                constants.RecordType.MEMORY_DEVICE_MAPPED_ADDRESS_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Ending Address'),
            validator.FieldValueRegexpChecker(
                'Ending Address', constants.FieldValueRegexps.HEX_REGEXP.value),
        ]),
        'ERROR: Invalid Ending Address field in Type 20 (Memory Device Mapped Address) record.',
        'ACTION: Please populate Ending Address field with valid address.'),
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(
                constants.RecordType.MEMORY_DEVICE_MAPPED_ADDRESS_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Physical Device Handle'),
            validator.HandleFieldChecker(
                'Physical Device Handle',
                constants.RecordType.MEMORY_DEVICE_RECORD),
        ]),
        'ERROR: Invalid Physical Device Handle field in Type 20 (Memory Device Mapped Address) record.',
        'ACTION: Please populate Physical Device Handle field with valid handle.'
    ),
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(
                constants.RecordType.MEMORY_DEVICE_MAPPED_ADDRESS_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Memory Array Mapped Address Handle'),
            validator.HandleFieldChecker(
                'Memory Array Mapped Address Handle',
                constants.RecordType.MEMORY_ARRAY_MAPPED_ADDRESS_RECORD),
        ]),
        'ERROR: Invalid Memory Array Mapped Address Handle field in Type 20 (Memory Device Mapped Address) record.',
        'ACTION: Please populate Memory Array Mapped Address Handle field with valid handle.'
    ),
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(
                constants.RecordType.MEMORY_DEVICE_MAPPED_ADDRESS_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Partition Row Position'),
            validator.FieldValueRegexpChecker(
                'Partition Row Position',
                constants.FieldValueRegexps.NUMBER_WITH_UNKNOWN_REGEXP.value),
        ]),
        'ERROR: Invalid Partition Row Position field in Type 20 (Memory Array Mapped Address) record.',
        ('ACTION: Please populate Partition Row Position field with valid number.\n'
         'This is the position of the referenced Memory Device in a row of the address partition.'
        )),
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(
                constants.RecordType.MEMORY_DEVICE_MAPPED_ADDRESS_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Interleave Position'),
            validator.FieldValueRegexpChecker(
                'Interleave Position',
                constants.FieldValueRegexps.NUMBER_WITH_UNKNOWN_REGEXP.value),
        ]),
        'ERROR: Invalid Interleave Position field in Type 20 (Memory Array Mapped Address) record.',
        ('ACTION: Please populate Interleave Position field with valid number.\n'
         'The value 0 indicates non-interleaved, 1 indicates first interleave position,'
         '2 the second interleave position and so on.')),
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(
                constants.RecordType.MEMORY_DEVICE_MAPPED_ADDRESS_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Interleaved Data Depth'),
            validator.FieldValueRegexpChecker(
                'Interleaved Data Depth',
                constants.FieldValueRegexps.NUMBER_WITH_UNKNOWN_REGEXP.value),
        ]),
        'ERROR: Invalid Interleaved Data Depth field in Type 20 (Memory Array Mapped Address) record.',
        ('ACTION: Please populate Interleaved Data Depth field with valid number.\n'
         'Example: If a device transfers two rows each time it is read, its interleaved data depth is 2.'
        )),

    # Rules for Type 38 (IPMI Device Information) records
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(
                constants.RecordType.IPMI_DEVICE_INFO_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Interface Type'),
            validator.FieldValueEnumChecker(
                'Interface Type',
                constants.FieldValueEnums.IPMI_DEVICE_INTERFACE_TYPES.value),
        ]),
        'ERROR: Invalid Interface Type field in Type 38 (IPMI Device Information) record.',
        ('ACTION: Please populate Interface Type field with valid string.\n'
         'Valid Type(s): ' + ', '.join(
             constants.FieldValueEnums.IPMI_DEVICE_INTERFACE_TYPES.value))),
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(
                constants.RecordType.IPMI_DEVICE_INFO_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Specification Version'),
            validator.FieldValueRegexpChecker(
                'Specification Version',
                constants.FieldValueRegexps.VERSION_REGEXP.value),
        ]),
        'ERROR: Invalid Specification Version field in Type 38 (IPMI Device Information) record.',
        'ACTION: Please populate Specification Version field with valid version.'
    ),
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(
                constants.RecordType.IPMI_DEVICE_INFO_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('I2C Slave Address'),
            validator.FieldValueRegexpChecker(
                'I2C Slave Address',
                constants.FieldValueRegexps.HEX_REGEXP.value),
        ]),
        'ERROR: Invalid I2C Slave Address field in Type 38 (IPMI Device Information) record.',
        'ACTION: Please populate I2C Slave Address field with valid address.'),

    # Rules for Type 160 (Google Bridge Device Structure) records
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(
                constants.RecordType.GOOGLE_BRIDGE_DEVICE_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Bridge Name'),
        ]),
        'ERROR: Invalid Bridge Name field in Type 160 (Google Bridge Device Structure) record.',
        'ACTION: Please populate Bridge Name field with valid string.'),
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(
                constants.RecordType.GOOGLE_BRIDGE_DEVICE_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Bridge Address'),
            validator.FieldValueRegexpChecker(
                'Bridge Address', constants.FieldValueRegexps.HEX_REGEXP.value),
        ]),
        'ERROR: Invalid Bridge Address field in Type 160 (Google Bridge Device Structure) record.',
        'ACTION: Please populate Bridge Address field with valid address.'),
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(
                constants.RecordType.GOOGLE_BRIDGE_DEVICE_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Number of links'),
            validator.FieldItemCountChecker('Number of links'),
        ]),
        'ERROR: Invalid Number of links field in Type 160 (Google Bridge Device Structure) record.',
        'ACTION: Please populate Number of links field with valid number and handles.'
    ),

    # Rules for Google Link Device Structure (Type 161) records
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(
                constants.RecordType.GOOGLE_LINK_DEVICE_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Link Name'),
        ]),
        'ERROR: Invalid Link Name field in Type 161 (Google Link Device Structure) record.',
        'ACTION: Please populate Link Name field with valid string.'),
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(
                constants.RecordType.GOOGLE_LINK_DEVICE_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Number of device'),
            validator.FieldItemCountChecker('Number of device', multiplier=2),
        ]),
        'ERROR: Invalid Number of device field in Type 161 (Google Link Device Structure) record.',
        'ACTION: Please populate Number of device field with valid number and info.'
    ),

    # Rules for Type 162 (Google CPU Link Structure) records
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(
                constants.RecordType.GOOGLE_CPU_LINK_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Identifier'),
        ]),
        'ERROR: Invalid Identifier field in Type 162 (Google CPU Link Structure) record.',
        'ACTION: Please populate Identifier field with valid string.'),
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(
                constants.RecordType.GOOGLE_CPU_LINK_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Max speed'),
            validator.FieldValueRegexpChecker(
                'Max speed', constants.FieldValueRegexps.SPEED_REGEXP.value),
        ]),
        'ERROR: Invalid Max Speed field in Type 162 (Google CPU Link Structure) record.',
        'ACTION: Please populate Max Speed field with valid speed.'),
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(
                constants.RecordType.GOOGLE_CPU_LINK_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Current speed'),
            validator.FieldValueRegexpChecker(
                'Current speed',
                constants.FieldValueRegexps.SPEED_REGEXP.value),
        ]),
        'ERROR: Invalid Current Speed field in Type 162 (Google CPU Link Structure) record.',
        'ACTION: Please populate Current Speed field with valid speed.'),
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(
                constants.RecordType.GOOGLE_CPU_LINK_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Source CPU'),
            validator.HandleFieldChecker('Source CPU',
                                         constants.RecordType.PROCESSOR_RECORD),
        ]),
        'ERROR: Invalid Source CPU field in Type 162 (Google CPU Link Structure) record.',
        'ACTION: Please populate Source CPU field with valid handle.'),
    Rule(
        matcher.Matcher([
            matcher.RecordTypeMatcher(
                constants.RecordType.GOOGLE_CPU_LINK_RECORD)
        ]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Destination CPU'),
            validator.HandleFieldChecker('Destination CPU',
                                         constants.RecordType.PROCESSOR_RECORD),
        ]),
        'ERROR: Invalid Destination CPU field in Type 161 (Google CPU Link Structure) record.',
        'ACTION: Please populate Destination CPU field with valid handle.'),
]
