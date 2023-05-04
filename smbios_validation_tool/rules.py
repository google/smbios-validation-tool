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
    'Vendor,
    None,
    'ACTION: Please populate Vendor field with correct vendor name.')

This rule will validate if field 'Vendor' is present. If not, the error message
and suggested actions will be printed out.
"""

from smbios_validation_tool import constants
from smbios_validation_tool import validator


class Rules:

  def __init__(self, rules):
    self.rules = rules

  def all_rules_validate(self, record, records, error_bucket):
    is_less_compliant = True
    for rule in self.rules:
      if rule.validators.validate_rule(record, records):
        continue
      is_less_compliant = False
      error_bucket.add_error(record.handle_id, (rule.err_msg, rule.action_msg))
    return is_less_compliant


class Rule:
  """Class that defines a rule for validating SMBIOS records.

  Attributes:
    validators: a list of validators with by default at least a
      FieldPresenceChecker. A record is valid if and only if all the validators
      are valid.
    err_msg: a string stores the error message if SMBIOS record is invalid.
    action_msg: a string stores suggested actions to correct error if SMBIOS
      record is invalid.
  """

  def __init__(
      self,
      field,
      field_validator,
      action_msg,
  ):
    self.validators = validator.IndividualValidator(
        [validator.FieldPresentChecker(field)]
    )
    if field_validator:
      self.validators = validator.IndividualValidator(
          [validator.FieldPresentChecker(field), field_validator]
      )
    self.err_msg = 'FIELD ERROR: ' + field
    self.action_msg = action_msg


# Rules for Type 0 (BIOS Information) structures
RULES_0 = Rules([
    Rule(
        'Vendor',
        validator.FieldValueRegexpChecker('Vendor', r'.*Google.*'),
        (
            'ACTION: BIOS Vendor string should contain "Google".\n'
            'Without that our software will ignore the OEM structures.'
        ),
    ),
    Rule(
        'Version',
        None,
        (
            'ACTION: BIOS Version can be any string as long as it follows'
            ' properly documented procedure.\nIf none available please follow'
            ' the XX.YY.RR format.'
        ),
    ),
    Rule(
        'Release Date',
        validator.FieldValueRegexpChecker(
            'Release Date', constants.FieldValueRegexps.DATE_REGEXP.value
        ),
        (
            'ACTION: Please populate BIOS Release Date field with correct date'
            ' (format is MM/DD/YYYY).'
        ),
    ),
    Rule(
        'ROM Size',
        validator.FieldValueRegexpChecker('ROM Size', r'\d+ [kmgKMG]B'),
        (
            'ACTION: Please populate BIOS ROM Size field with valid size.\n'
            '*BIOS ROM Size indicates the BIOS size not the flash part size.*'
        ),
    ),
])

# Rules for Type 1 (System Information) structures
RULES_1 = Rules([])

# Rules for Type 2 (Board Information) structures
RULES_2 = Rules([
    Rule(
        'Manufacturer',
        None,
        'ACTION: Please populate Manufacturer field with valid string.',
    ),
    Rule(
        'Product Name',
        None,
        'ACTION: Please populate Product field with valid string.',
    ),
    Rule(
        'Features',
        None,
        (
            'ACTION: Please populate Features field with valid feature'
            ' flags.\nBit0 - 1 for Motherboard, 0 for daughter boards; Bit3 - 1'
            ' for replaceable board.'
        ),
    ),
    Rule(
        'Location In Chassis',
        validator.FieldValueRegexpChecker(
            'Location In Chassis',
            constants.FieldValueRegexps.DEVPATH_REGEXP.value,
        ),
        (
            'ACTION: Please populate Location In Chassis field with valid'
            ' devpath.\nThis field provides the devpath for the daughter board.'
        ),
    ),
    Rule(
        'Chassis Handle',
        validator.HandleFieldChecker('Chassis Handle', 3),
        'ACTION: Please populate Chassis Handle field with valid handle.',
    ),
    Rule(
        'Contained Object Handles',
        validator.FieldItemCountChecker('Contained Object Handles'),
        (
            'ACTION: Please populate Contained Object Handles field with valid'
            ' handles.\n'
        ),
    ),
])

# Rules for Type 3 (Chassis and Tray Information) structures
RULES_3 = Rules([
    Rule(
        'Manufacturer',
        None,
        'ACTION: Please populate Manufacturer field with valid string.',
    ),
    Rule(
        'Type',
        validator.FieldValueEnumChecker(
            'Type', constants.FieldValueEnums.CHASSIS_TYPES.value
        ),
        (
            'ACTION: Please populate Type field with valid string.\n'
            'Valid Type(s): '
            + ', '.join(constants.FieldValueEnums.CHASSIS_TYPES.value)
        ),
    ),
    Rule(
        'Lock',
        validator.FieldValueEnumChecker(
            'Lock', constants.FieldValueEnums.CHASSIS_LOCK.value
        ),
        (
            'ACTION: Please populate Lock field with valid string.\n'
            'Valid Lock Status: '
            + ', '.join(constants.FieldValueEnums.CHASSIS_LOCK.value)
        ),
    ),
    Rule(
        'OEM Information',
        validator.FieldValueRegexpChecker(
            'OEM Information',
            constants.FieldValueRegexps.OEM_FOR_GOOGLE_REGEXP.value,
        ),
        (
            'ACTION: Please populate OEM Information field with valid hex'
            ' value.\nOEM Byte 0 must be 0x67, which is the identification for'
            ' Google OEM Info.'
        ),
    ),
    Rule(
        'Contained Elements',
        validator.FieldValueRegexpChecker(
            'Contained Elements',
            constants.FieldValueRegexps.NUMBER_REGEXP.value,
        ),
        'ACTION: Please populate Contained Elements field with valid number.',
    ),
])

# Rules for Type 4 (Processor Information) structures
RULES_4 = Rules([
    Rule(
        'Socket Designation',
        validator.FieldValueRegexpChecker(
            'Socket Designation',
            constants.FieldValueRegexps.SOCKET_DESIGNATION_REGEXP.value,
        ),
        (
            'ACTION: Please populate Socket Designation field with valid'
            ' string.\nProcessor silkscreen tag usually looks like CPU0, CPU1,'
            ' etc.'
        ),
    ),
    Rule(
        'Type',
        validator.FieldValueEnumChecker(
            'Type', constants.FieldValueEnums.PROCESSOR_TYPE.value
        ),
        (
            'ACTION: Please populate Type field with valid string.\n'
            'Valid Processor Type(s): '
            + ', '.join(constants.FieldValueEnums.PROCESSOR_TYPE.value)
        ),
    ),
    Rule(
        'Status',
        validator.FieldValueRegexpChecker(
            'Status', constants.FieldValueRegexps.PROCESSOR_STATUS_REGEXP.value
        ),
        'ACTION: Please populate Status field with valid string.\n',
    ),
    Rule(
        'L1 Cache Handle',
        validator.HandleFieldChecker(
            'L1 Cache Handle', constants.StructureType.CACHE_INFORMATION
        ),
        'ACTION: Please populate L1 Cache Handle field with valid handle',
    ),
    Rule(
        'L2 Cache Handle',
        validator.HandleFieldChecker(
            'L2 Cache Handle', constants.StructureType.CACHE_INFORMATION
        ),
        'ACTION: Please populate L2 Cache Handle field with valid handle',
    ),
    Rule(
        'L3 Cache Handle',
        validator.HandleFieldChecker(
            'L3 Cache Handle', constants.StructureType.CACHE_INFORMATION
        ),
        'ACTION: Please populate L3 Cache Handle field with valid handle',
    ),
    Rule(
        'Core Count',
        validator.FieldValueRegexpChecker(
            'Core Count', constants.FieldValueRegexps.NUMBER_REGEXP.value
        ),
        'ACTION: Please populate Core Count field with valid number.\n',
    ),
    Rule(
        'Core Enabled',
        validator.FieldValueRegexpChecker(
            'Core Enabled', constants.FieldValueRegexps.NUMBER_REGEXP.value
        ),
        'ACTION: Please populate Core Enabled field with valid number.\n',
    ),
    Rule(
        'Thread Count',
        validator.FieldValueRegexpChecker(
            'Thread Count', constants.FieldValueRegexps.NUMBER_REGEXP.value
        ),
        'ACTION: Please populate Thread Count field with valid number.\n',
    ),
])

# Rules for Type 8 (Port Connector Information) structures
RULES_8 = Rules([])

# Rules for Type 9 (System Slots) structures
RULES_9 = Rules(
    [
        Rule(
            'Designation',
            None,
            (
                'ACTION: Please populate Designation field with valid Slot'
                ' silkscreen.\ne.g. PE0, PE4, etc.'
            ),
        ),
        # TODO(xuhha): check there are no 2 slots sharing same designation.
        Rule(
            'Type',
            None,
            (
                'ACTION: Please populate Slot Type field with valid string.\n'
                'e.g. Proprietary, x8 PCI Express 3 x8, etc.'
            ),
        ),
        Rule(
            'Current Usage',
            validator.FieldValueEnumChecker(
                'Current Usage',
                constants.FieldValueEnums.SYSTEM_SLOTS_CURRENT_USAGE.value,
            ),
            (
                'ACTION: Please populate Current Usage field with valid'
                ' string.\nValid Usage: '
                + ', '.join(
                    constants.FieldValueEnums.SYSTEM_SLOTS_CURRENT_USAGE.value
                )
            ),
        ),
        Rule(
            'Length',
            validator.FieldValueEnumChecker(
                'Length', constants.FieldValueEnums.SYSTEM_SLOTS_LENGTH.value
            ),
            (
                'ACTION: Please populate Slot Length field with valid string.\n'
                'Valid Length: '
                + ', '.join(constants.FieldValueEnums.SYSTEM_SLOTS_LENGTH.value)
            ),
        ),
        Rule(
            'Characteristics',
            None,
            (
                'ACTION: Please populate Characteristics field with valid'
                ' string.\ne.g. 3.3 V is provided, UNKNOWN, etc.'
            ),
        ),
        Rule(
            'Bus Address',
            validator.FieldValueRegexpChecker(
                'Bus Address', r'[0-9a-f]{4}:[0-9a-f]{2}:[0-9a-f]{2}\.[0-9a-f]'
            ),
            (
                'ACTION: Please populate Bus Address field with valid string.\n'
                'e.g. 0000:c0:02.0.'
            ),
        ),
        # TODO(xuhha): Check for the actual presence of the PCI device from
        # the above address, using 'lspci'.
    ]
)

# Rules for Type 14 (Group Associations) structures
RULES_14 = Rules([
    Rule(
        'Name',
        None,
        (
            'ACTION: Please populate Name field with valid string.\n'
            'e.g. die0, IMC0, Connector, etc.'
        ),
    ),
    Rule(
        'Items',
        validator.FieldItemCountChecker(
            'Items', compare_function=lambda x: x >= 1
        ),
        (
            'ACTION: Please populate Items field with valid item count and'
            ' strings.\nAt least one item must be listed in the record.'
        ),
    ),
    Rule(
        'Items',
        validator.FieldItemUniquenessChecker('Items'),
        (
            'Please make sure all handles are unique in items of group'
            ' associations records.'
        ),
    ),
])

# Rules for Type 16 (Physical Memory Array) structures
RULES_16 = Rules([
    Rule(
        'Location',
        validator.FieldValueEnumChecker(
            'Location',
            constants.FieldValueEnums.PHYSICAL_MEMORY_ARRAY_LOCATION.value,
        ),
        (
            'ACTION: Please populate Location field with valid string.\n'
            'Usually 0x03 for System Board/Motherboard.'
        ),
    ),
    Rule(
        'Use',
        validator.FieldValueEnumChecker(
            'Use', constants.FieldValueEnums.PHYSICAL_MEMORY_ARRAY_USE.value
        ),
        (
            'ACTION: Please populate Use field with valid string.\nFunction for'
            ' which this array is used. Usually 0x03 for System Memory.'
        ),
    ),
    Rule(
        'Error Correction Type',
        None,
        (
            'ACTION: Please populate Error Correction Type field with valid'
            ' string.\ne.g. Multi-bit ECC.'
        ),
    ),
    Rule(
        'Maximum Capacity',
        validator.FieldValueRegexpChecker(
            'Maximum Capacity', constants.FieldValueRegexps.SIZE_REGEXP.value
        ),
        'ACTION: Please populate Maximum Capacity field with valid capacity.',
    ),
    Rule(
        'Number Of Devices',
        validator.FieldValueRegexpChecker(
            'Number Of Devices', constants.FieldValueRegexps.NUMBER_REGEXP.value
        ),
        'ACTION: Please populate Number of Devices field with valid number',
    ),
])

# Rules for Type 17 (Memory Device) structures
RULES_17 = Rules([
    Rule(
        'Array Handle',
        validator.HandleFieldChecker(
            'Array Handle', constants.StructureType.PHYSICAL_MEMORY_ARRAY
        ),
        (
            'ACTION: Please populate Array Handle field with valid'
            ' handle.\nThis field should be the handle associated with the'
            ' Physical Memory Array to which this device belongs.'
        ),
    ),
    Rule(
        'Error Information Handle',
        validator.FieldValueRegexpChecker(
            'Error Information Handle',
            r'(Not provided)|(No Error)|(0x[0-9a-f]{4})',
        ),
        (
            'ACTION: Please populate Error Information Handle field with valid'
            ' value'
        ),
    ),
    Rule(
        'Total Width',
        validator.FieldValueRegexpChecker('Total Width', r'(Unknown)|\d+ bits'),
        (
            'ACTION: Please populate Total Width field with valid number of'
            ' bits (or Unknown).'
        ),
    ),
    Rule(
        'Data Width',
        validator.FieldValueRegexpChecker('Data Width', r'(Unknown)|\d+ bits'),
        (
            'ACTION: Please populate Data Width field with valid number of bits'
            ' (or Unknown).'
        ),
    ),
    Rule(
        'Size',
        validator.FieldValueRegexpChecker(
            'Size', r'(Unknown)|(No Module Installed)|(\d+ (MB|GB|TB))'
        ),
        (
            'ACTION: Please populate Size field with valid capacity (or No'
            ' Module Installed).'
        ),
    ),
    Rule(
        'Form Factor',
        validator.FieldValueEnumChecker(
            'Form Factor',
            constants.FieldValueEnums.MEMORY_DEVICE_FORM_FACTOR.value,
        ),
        (
            'ACTION: Please populate Form Factor field with valid string.\n'
            'Valid Form Factor(s): '
            + ', '.join(
                constants.FieldValueEnums.MEMORY_DEVICE_FORM_FACTOR.value
            )
        ),
    ),
    Rule(
        'Set',
        validator.FieldValueRegexpChecker('Set', r'Unknown|None|\w+'),
        (
            'ACTION: Please populate Set field with valid string (or'
            ' Unknown/None).'
        ),
    ),
    Rule(
        'Locator',
        validator.FieldValueRegexpChecker('Locator', r'(?:[^\d]*)\d+'),
        (
            'ACTION: Please populate Locator field with valid string.\n'
            'This field is silk screen for the DIMM location. e.g. DIMM0'
        ),
    ),
    Rule(
        'Bank Locator',
        validator.FieldValueRegexpChecker(
            'Bank Locator',
            r'.*(Node|Channel).*',
        ),
        (
            'ACTION: Please populate Bank Locator field with valid string.\n'
            'This is the string that identifies the physically labeled bank '
            'where the memory device is located.'
        ),
    ),
    Rule(
        'Type',
        validator.FieldValueEnumChecker(
            'Type', constants.FieldValueEnums.MEMORY_DEVICE_TYPES.value
        ),
        (
            'ACTION: Please populate Memory Type field with valid string.\n'
            'Valid Type(s): '
            + ', '.join(constants.FieldValueEnums.MEMORY_DEVICE_TYPES.value)
        ),
    ),
    Rule(
        'Type Detail',
        None,
        'ACTION: Please populate Memory Type field with valid string.\n',
    ),
])

# Rules for Type 19 (Memory Array Mapped Address) structures
RULES_19 = Rules([
    Rule(
        'Starting Address',
        None,
        'ACTION: Please populate Starting Address field with valid address.',
    ),
    Rule(
        'Ending Address',
        None,
        'ACTION: Please populate Ending Address field with valid address.',
    ),
    Rule(
        'Physical Array Handle',
        validator.HandleFieldChecker(
            'Physical Array Handle',
            constants.StructureType.PHYSICAL_MEMORY_ARRAY,
        ),
        (
            'ACTION: Please populate Physical Array Handle field with valid'
            ' handle.'
        ),
    ),
    Rule(
        'Partition Width',
        validator.FieldValueRegexpChecker(
            'Partition Width', constants.FieldValueRegexps.NUMBER_REGEXP.value
        ),
        (
            (
                'ACTION: Please populate Partition Width field with valid'
                ' number.\n'
            ),
            (
                'Partition Width is the number of Memory Devices that form a'
                ' single row of memory '
            ),
            'for the address partition defined by this structure.',
        ),
    ),
])

# Rules for Type 20 (Memory Device Mapped Address) structures
RULES_20 = Rules([
    Rule(
        'Starting Address',
        None,
        'ACTION: Please populate Starting Address field with valid address.',
    ),
    Rule(
        'Ending Address',
        None,
        'ACTION: Please populate Ending Address field with valid address.',
    ),
    Rule(
        'Physical Device Handle',
        validator.HandleFieldChecker(
            'Physical Device Handle', constants.StructureType.MEMORY_DEVICE
        ),
        (
            'ACTION: Please populate Physical Device Handle field with valid'
            ' handle.'
        ),
    ),
    Rule(
        'Memory Array Mapped Address Handle',
        validator.HandleFieldChecker(
            'Memory Array Mapped Address Handle',
            constants.StructureType.MEMORY_ARRAY_MAPPED_ADDRESS,
        ),
        (
            'ACTION: Please populate Memory Array Mapped Address Handle field'
            ' with valid handle.'
        ),
    ),
    Rule(
        'Partition Row Position',
        validator.FieldValueRegexpChecker(
            'Partition Row Position',
            constants.FieldValueRegexps.NUMBER_WITH_UNKNOWN_REGEXP.value,
        ),
        (
            'ACTION: Please populate Partition Row Position field with valid'
            ' number.\nThis is the position of the referenced Memory Device in'
            ' a row of the address partition.'
        ),
    ),
    Rule(
        'Interleave Position',
        validator.FieldValueRegexpChecker(
            'Interleave Position',
            constants.FieldValueRegexps.NUMBER_WITH_UNKNOWN_REGEXP.value,
        ),
        (
            'ACTION: Please populate Interleave Position field with valid'
            ' number.\nThe value 0 indicates non-interleaved, 1 indicates first'
            ' interleave position,2 the second interleave position and so on.'
        ),
    ),
    Rule(
        'Interleaved Data Depth',
        validator.FieldValueRegexpChecker(
            'Interleaved Data Depth',
            constants.FieldValueRegexps.NUMBER_WITH_UNKNOWN_REGEXP.value,
        ),
        (
            'ACTION: Please populate Interleaved Data Depth field with valid'
            ' number.\nExample: If a device transfers two rows each time it is'
            ' read, its interleaved data depth is 2.'
        ),
    ),
])

# Rules for Type 32 (System Root Information) structures
RULES_32 = Rules([])

# Rules for Type 38 (IPMI Device Information) structures
RULES_38 = Rules([
    Rule(
        'Interface Type',
        validator.FieldValueEnumChecker(
            'Interface Type',
            constants.FieldValueEnums.IPMI_DEVICE_INTERFACE_TYPES.value,
        ),
        (
            'ACTION: Please populate Interface Type field with valid string.\n'
            'Valid Type(s): '
            + ', '.join(
                constants.FieldValueEnums.IPMI_DEVICE_INTERFACE_TYPES.value
            )
        ),
    ),
    Rule(
        'Specification Version',
        validator.FieldValueRegexpChecker(
            'Specification Version',
            constants.FieldValueRegexps.VERSION_REGEXP.value,
        ),
        (
            'ACTION: Please populate Specification Version field with valid'
            ' version.'
        ),
    ),
    Rule(
        'I2C Address',
        validator.FieldValueRegexpChecker(
            'I2C Address', constants.FieldValueRegexps.HEX_REGEXP.value
        ),
        'ACTION: Please populate I2C Address field with valid address.',
    ),
])

# Rules for Type 39 (System Power Supply Structure) structures
RULES_39 = Rules([])

# Rules for Type 41 (Onboard Devices Extended Information) structures
RULES_41 = Rules([])

# Rules for Type 160 (Google Bridge Device Structure) structures
RULES_160 = Rules([
    Rule(
        'Bridge Name',
        None,
        'ACTION: Please populate Bridge Name field with valid string.',
    ),
    Rule(
        'Bridge Address',
        validator.FieldValueRegexpChecker(
            'Bridge Address', constants.FieldValueRegexps.HEX_REGEXP.value
        ),
        'ACTION: Please populate Bridge Address field with valid address.',
    ),
    Rule(
        'Number of links',
        validator.FieldItemCountChecker('Number of links'),
        (
            'ACTION: Please populate Number of links field with valid number'
            ' and handles.'
        ),
    ),
])

# Rules for Type 161 (Google Link Device Structure) structures
RULES_161 = Rules([
    Rule(
        'Link Name',
        None,
        'ACTION: Please populate Link Name field with valid string.',
    ),
    Rule(
        'Number of device',
        validator.FieldItemCountChecker('Number of device', multiplier=2),
        (
            'ACTION: Please populate Number of device field with valid number'
            ' and info.'
        ),
    ),
])

# Rules for Type 162 (Google CPU Link Structure) structures
RULES_162 = Rules([
    Rule(
        'Identifier',
        None,
        'ACTION: Please populate Identifier field with valid string.',
    ),
    Rule(
        'Max speed',
        validator.FieldValueRegexpChecker(
            'Max speed', constants.FieldValueRegexps.SPEED_REGEXP.value
        ),
        'ACTION: Please populate Max Speed field with valid speed.',
    ),
    Rule(
        'Current speed',
        validator.FieldValueRegexpChecker(
            'Current speed', constants.FieldValueRegexps.SPEED_REGEXP.value
        ),
        'ACTION: Please populate Current Speed field with valid speed.',
    ),
    Rule(
        'Source CPU',
        validator.HandleFieldChecker(
            'Source CPU', constants.StructureType.PROCESSOR_INFORMATION
        ),
        'ACTION: Please populate Source CPU field with valid handle.',
    ),
    Rule(
        'Destination CPU',
        validator.HandleFieldChecker(
            'Destination CPU', constants.StructureType.PROCESSOR_INFORMATION
        ),
        'ACTION: Please populate Destination CPU field with valid handle.',
    ),
])

default_rules = {
    constants.StructureType.BIOS_INFORMATION: RULES_0,
    constants.StructureType.SYSTEM_INFORMATION: RULES_1,
    constants.StructureType.BOARD_INFORMATION: RULES_2,
    constants.StructureType.CHASSIS_AND_TRAY_INFORMATION: RULES_3,
    constants.StructureType.PROCESSOR_INFORMATION: RULES_4,
    constants.StructureType.PORT_CONNECTOR_INFORMATION: RULES_8,
    constants.StructureType.SYSTEM_SLOTS: RULES_9,
    constants.StructureType.GROUP_ASSOCIATIONS: RULES_14,
    constants.StructureType.PHYSICAL_MEMORY_ARRAY: RULES_16,
    constants.StructureType.MEMORY_DEVICE: RULES_17,
    constants.StructureType.MEMORY_ARRAY_MAPPED_ADDRESS: RULES_19,
    constants.StructureType.MEMORY_DEVICE_MAPPED_ADDRESS: RULES_20,
    constants.StructureType.SYSTEM_BOOT_INFORMATION: RULES_32,
    constants.StructureType.IPMI_DEVICE_INFORMATION: RULES_38,
    constants.StructureType.SYSTEM_POWER_SUPPLY_STRUCTURE: RULES_39,
    constants.StructureType.ONBOARD_DEVICES_EXTENDED_INFORMATION: RULES_41,
    constants.StructureType.GOOGLE_BRIDGE_DEVICE_STRUCTURE: RULES_160,
    constants.StructureType.GOOGLE_LINK_DEVICE_STRUCTURE: RULES_161,
    constants.StructureType.GOOGLE_CPU_LINK_STRUCTURE: RULES_162,
}

CONIDTION_RULES_17 = Rules([
    Rule(
        'Speed',
        validator.FieldValueRegexpChecker('Speed', r'(Unknown)|\d+ MT/s'),
        (
            'ACTION: Please populate Speed field with valid string.\n'
            'e.g. 2400 MT/s'
        ),
    ),
    Rule(
        'Manufacturer',
        None,
        'ACTION: Please populate Manufacturer field with valid string.',
    ),
    Rule(
        'Serial Number',
        None,
        'ACTION: Please populate Serial Number field with valid string.',
    ),
    Rule(
        'Asset Tag',
        None,
        'ACTION: Please populate Asset Tag field with valid string.',
    ),
    Rule(
        'Part Number',
        None,
        'ACTION: Please populate Part Number field with valid string.',
    ),
    Rule(
        'Rank',
        None,
        'ACTION: Please populate Rank field with valid string.',
    ),
    Rule(
        'Configured Memory Speed',
        validator.FieldValueRegexpChecker(
            'Configured Memory Speed',
            r'(Unknown)|\d+ MT/s',
        ),
        (
            'ACTION: Please populate Configured Memory Speed field with valid'
            ' speed.'
        ),
    ),
    Rule(
        'Minimum Voltage',
        validator.FieldValueRegexpChecker(
            'Minimum Voltage', r'(Unknown)|(\d.\d+ V)'
        ),
        'ACTION: Please populate Minimum Voltage field with valid voltage.',
    ),
    Rule(
        'Maximum Voltage',
        validator.FieldValueRegexpChecker(
            'Maximum Voltage', r'(Unknown)|(\d.\d+ V)'
        ),
        'ACTION: Please populate Maximum Voltage field with valid voltage.',
    ),
    Rule(
        'Configured Voltage',
        validator.FieldValueRegexpChecker(
            'Configured Voltage',
            r'(Unknown)|(\d.\d+ V)',
        ),
        'ACTION: Please populate Configured Voltage field with valid voltage.',
    ),
])