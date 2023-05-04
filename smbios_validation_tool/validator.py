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
"""Module for validating rules against individual or group of SMBIOS records."""

import re

from smbios_validation_tool import constants
import termcolor

_DIE_REGEX = re.compile(r'die\d+', re.IGNORECASE)
_CONTROLLER_REGEX = re.compile(r'[i|u]mc\d+', re.IGNORECASE)
_CHANNEL_REGEX = re.compile(r'ch\d+', re.IGNORECASE)


class FieldPresentChecker:
  """A checker to validate if a field is present in a SMBIOS record.

  Attributes:
    field: A string representing the name of a SMBIOS record property.
  """

  def __init__(self, field):
    self.field = field

  def validate(self, record, _):
    return record and self.field in record.props and record.props[self.field]


class FieldValueRegexpChecker:
  """A checker to validate if the value of a field matches a specific regexp.

  Attributes:
    field: A string representing the name of an SMBIOS record properties.
    regexp: A regex pattern indicating what the field value is going to match.
  """

  def __init__(self, field, regexp):
    self.field = field
    self.regexp = re.compile(regexp, re.IGNORECASE)

  def validate(self, record, _):
    if not record or self.field not in record.props:
      return False
    prop = record.props[self.field]
    return self.regexp.fullmatch(prop.val)


class FieldValueEnumChecker:
  """A checker to validate if each value of a field matches one of enum members.

  Attributes:
    field: A string representing the name of an SMBIOS record properties.
    enum: A set of enumeration of which each field value should match exact one.
  """

  def __init__(self, field, enum):
    self.field = field
    self.enum = enum

  def validate(self, record, _):
    enum_join = '|'.join(self.enum)
    regexp = r'(' + enum_join + r'){1}(\s+(' + enum_join + r'))*$'
    checker = FieldValueRegexpChecker(self.field, regexp)
    return checker.validate(record, _)


class FieldItemCountChecker:
  """A checker to validate if the count of a field is valid.

  This checker will always validate if the field value equals its item count. To
  further validate if item count is in a specific range, you need to provide a
  compare function (usually a lambda function). For example, the following
  checker will validate if the field 'Items' has at least one item in it.

    FieldItemCountChecker('Items', compare_function=lambda x: x >= 1)

  Sometimes more than one line is needed per item. For example, the following
  record should set multiplier to 2:

    Handle 0x029F, DMI type 161, 72 bytes
    Google Link Devices
      Link Name: smbch0
      Number of device : 6
        Device Address: 0x000000050
        Handle: 0x61
        Device Address: 0x000000051
        Handle: 0x63
        Device Address: 0x000000052
        Handle: 0x65
        Device Address: 0x000000054
        Handle: 0x67
        Device Address: 0x000000055
        Handle: 0x69
        Device Address: 0x000000056
        Handle: 0x6B

  Attributes:
    field: A string representing the name of an SMBIOS record properties.
    compare_function: A function to validate if item count is in a specific
      range.
    multiplier: A number represents how many lines needed per item. Default = 1.
  """

  def __init__(self, field, compare_function=None, multiplier=1):
    self.field = field
    self.compare_function = compare_function
    self.multiplier = multiplier

  def validate(self, record, _):
    if not record or self.field not in record.props:
      return False
    prop = record.props[self.field]
    is_valid = int(prop.val) * self.multiplier == len(prop.items)

    if self.compare_function:
      is_valid &= self.compare_function(int(prop.val))
    return is_valid


class FieldItemUniquenessChecker:
  """A checker to validate all items of a field are unique.

  Attributes:
    field: A string representing the name of an SMBIOS record properties.
  """

  def __init__(self, field):
    self.field = field

  def validate(self, record, _):
    if not record or self.field not in record.props:
      return False
    items = record.props[self.field].items
    return len(set(items)) == len(items)


class HandleFieldChecker:
  """A checker to validate fields for storing handle ID of another record.

  Typical usage example:
    HandleFieldChecker("Chassis Handle", 3)

    This will create a checker that verifies "Chassis Handle" field is a record
    handle and the corresponding record type is 3

  Attributes:
    field: A string representing the name of an SMBIOS record properties.
    type_id: A number representing the DMI type of the record.
  """

  def __init__(self, field, type_id):
    self.field = field
    self.type_id = type_id

  def validate(self, record, records):
    """Make sure the handle id matches the required type."""
    if not record or self.field not in record.props:
      return False
    handle_id = record.props[self.field].val
    if handle_id not in records:
      return False
    # Make sure the format of handle id is equivalent to all other handles
    # e.g. '0x123' will become '0x0123'.
    handle_id = '0x{:04X}'.format(int(handle_id, 16))
    if handle_id not in records:
      return False
    if records[handle_id].type_id != self.type_id:
      return False
    return True


class IndividualValidator:
  """Class for validating checkers against an individual SMBIOS record.

  Attributes:
    checkers: A list of checkers. Each checker is an instance of a Checker class
      defined to validate individual SMBIOS record.
  """

  def __init__(self, checkers):
    self.checkers = checkers

  # A rule is valid if and only if all the checkers are valid.
  def validate_rule(self, record, records):
    for checker in self.checkers:
      if not checker.validate(record, records):
        return False
    return True


class RecordsPresenceChecker:
  """A checker to validate presence of all mandatory SMBIOS records.

  Attributes:
    records: dict that maps handle id to the record instance.
    groups: dict that maps type id to set of handle ids that has same type.
    err_msgs: a dict that maps error messages to corresponding action messages.
  """

  def __init__(self, records, groups):
    self.records = records
    self.groups = groups
    self.err_msgs = {}

  def validate(self):
    """A series of rules to validate existance of mandatory SMBIOS records."""

    # Check if motherboard record exists
    motherboard_record_exists = False
    board_info_records = self.groups[constants.StructureType.BOARD_INFORMATION]
    for handle_id in board_info_records:
      record = self.records[handle_id]
      if 'Type' in record.props and record.props['Type'].val == 'Motherboard':
        motherboard_record_exists = True
        break
    if not motherboard_record_exists:
      self.err_msgs['Motherboard SMBIOS record is missing.'] = (
          'There should be at least one structure defining the motherboard '
          '(Board Type: 0xA).')

    return self.err_msgs


class MemoryGroupAssociationsChecker:
  """A checker to validate memory hierarchy group associations records.

  A typical memory hierarchy is Die -> controller -> Channel -> DIMMs.

  Attributes:
    records: dict that maps handle id to the record instance.
    groups: dict that maps type id to set of handle ids that has same type.
    err_msgs: a dict that maps error messages to corresponding action messages.
    dies: a list of handles for dies.
    controllers: a list of handles for memory controllers. (IMC, UMC, etc.)
    channels: a list of handles for channels.
  """

  def __init__(self, records, groups):
    self.records = records
    self.groups = groups
    self.err_msgs = {}

    # Collect all handles for die, controller and channel records.
    group_records = self.groups[constants.StructureType.GROUP_ASSOCIATIONS]
    self.dies = []
    self.controllers = []
    self.channels = []

    for handle_id in group_records:
      record = self.records[handle_id]
      if 'Name' not in record.props:
        continue
      if _DIE_REGEX.match(record.props['Name'].val):
        self.dies.append(handle_id)
      if _CONTROLLER_REGEX.match(record.props['Name'].val):
        self.controllers.append(handle_id)
      if _CHANNEL_REGEX.match(record.props['Name'].val):
        self.channels.append(handle_id)

  def _get_group_handles(self, items):
    """Extracts handles for group associations from SMBIOS record items.

    A typical group associations record looks like this:

      Handle 0x02CA, DMI type 14, 35 bytes
      Group Associations
      Name: die0
      Items: 4
          0x0299 (Group Associations)
          0x029A (Group Associations)
          0x02C0 (OEM-specific)
          0x0126 (Processor)

    This function will extract the handles for group associations only.
    i.e., it will return ['0x0299', '0x029A']

    Args:
      items: a list of items for an SMBIOS record

    Returns:
      handles: a list of group associations handle ids extracted from the items
    """
    handles = []
    for item in items:
      matched = re.match(r'(0x[0-9a-fA-F]+) (?:\(Group Associations\))', item)
      if matched:
        handles.append(matched.group(1))
    return handles

  def _validate_dies(self):
    """Validates all group associations records for dies."""
    # Keep track of memory controller handles that are listed in items of all
    # dies in a dictionary.
    # Key: memory controller handle
    # Value: die handle that the memory controller handle belongs to
    visited_controllers = {}
    for die_handle in self.dies:
      die_record = self.records[die_handle]
      die_items = die_record.props.get('Items')
      die_name = die_record.props.get('Name').val
      group_handles = self._get_group_handles(die_items.items)

      # Make sure a memory controller handle does not belong to multiple
      # die records.
      for handle_id in set(visited_controllers).intersection(group_handles):
        err_msg = (
            'In items of Die Handle {} ({}), memory controller handle {} was'
            ' belong to another die record ({}).').format(
                die_handle, die_name, handle_id, visited_controllers[handle_id])
        self.err_msgs[err_msg] = (
            'Please make sure a memory controller handle does not belong to '
            'multiple die records.')

      # Make sure at least one handle is pointing to a memory controller record.
      new_visited = {
          handle_id: die_handle
          for handle_id in group_handles
          if handle_id in self.controllers
      }
      if not new_visited:
        err_msg = (
            'There is no memory controller handle in items of Die Handle {}'
            ' ({}).').format(die_handle, die_name)
        self.err_msgs[err_msg] = (
            'At least one item of a die record should be a memory controller '
            'handle.')
      else:
        visited_controllers.update(new_visited)

    return visited_controllers

  def _validate_controllers(self, controllers_in_die):
    """Validates all group associations records for controllers.

    Args:
      controllers_in_die: a list of memory controller handles that are in a die
        grouping.
    """
    for controller_handle in self.controllers:
      controller_record = self.records[controller_handle]
      controller_items = controller_record.props.get('Items')
      controller_name = controller_record.props.get('Name').val

      # Validate that the memory controller handle is listed in a die record.
      if controller_handle not in controllers_in_die:
        err_msg = (
            'Memory Controller Handle {} ({}) is not listed in any die record.'
        ).format(controller_handle, controller_name)
        self.err_msgs[err_msg] = (
            'Please make sure every memory controller handle is listed in one '
            'and only one die record.')

      # Validate that all items are group associations handles
      handles = self._get_group_handles(controller_items.items)
      if len(handles) < len(controller_items.items):
        err_msg = ('Some items in Handle {} ({}) are not Type 14 handles (Group'
                   ' Associations).').format(controller_handle, controller_name)
        self.err_msgs[err_msg] = (
            'All items in controller records must be Type 14 (Group '
            'Associations) handles.')

  def validate(self):
    """Validates all memory hierarchy group associations records.

    Returns:
      err_msgs: a dictionary with error messages and suggested action found
      during the validation.
    """
    visited_controllers = self._validate_dies()
    self._validate_controllers(visited_controllers)
    return self.err_msgs


class GroupValidator:
  """Class for validating checkers against groups of SMBIOS records.

  Attributes:
    checkers: A list of checkers. Each checker is an instance of a Checker class
      defined to validate groups of SMBIOS records.
  """

  def __init__(self, records, groups):
    self.checkers = []
    self.checkers.append(RecordsPresenceChecker(records, groups))
    self.checkers.append(MemoryGroupAssociationsChecker(records, groups))

  def _print_msg(self, err_msgs):
    for err_msg, action_msg in err_msgs.items():
      print(termcolor.colored('ERROR: ' + err_msg, color='red', attrs=['bold']))
      print(
          termcolor.colored(
              'ACTION: ' + action_msg, color='yellow', attrs=['underline']))
      print('\n')

  def validate(self):
    is_valid = True
    for checker in self.checkers:
      err_msgs = checker.validate()
      if err_msgs:
        is_valid = False
        self._print_msg(err_msgs)
    return is_valid