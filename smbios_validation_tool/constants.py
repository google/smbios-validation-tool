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
"""Module for defining constants used in the tool."""

import enum


class StructureType(enum.IntEnum):
  """Define SMBIOS structure types."""

  BIOS_INFORMATION = 0
  SYSTEM_INFORMATION = 1
  BOARD_INFORMATION = 2
  CHASSIS_AND_TRAY_INFORMATION = 3
  PROCESSOR_INFORMATION = 4
  CACHE_INFORMATION = 7
  PORT_CONNECTOR_INFORMATION = 8
  SYSTEM_SLOTS = 9
  GROUP_ASSOCIATIONS = 14
  PHYSICAL_MEMORY_ARRAY = 16
  MEMORY_DEVICE = 17
  MEMORY_ARRAY_MAPPED_ADDRESS = 19
  MEMORY_DEVICE_MAPPED_ADDRESS = 20
  SYSTEM_BOOT_INFORMATION = 32
  IPMI_DEVICE_INFORMATION = 38
  SYSTEM_POWER_SUPPLY_STRUCTURE = 39
  ONBOARD_DEVICES_EXTENDED_INFORMATION = 41
  GOOGLE_BRIDGE_DEVICE_STRUCTURE = 160
  GOOGLE_LINK_DEVICE_STRUCTURE = 161
  GOOGLE_CPU_LINK_STRUCTURE = 162

StructureName = {
    StructureType.BIOS_INFORMATION: 'BIOS Information',
    StructureType.SYSTEM_INFORMATION: 'System Information',
    StructureType.BOARD_INFORMATION: 'Board Information',
    StructureType.CHASSIS_AND_TRAY_INFORMATION: 'Chassis and Tray Information',
    StructureType.PROCESSOR_INFORMATION: 'Processor Information',
    StructureType.CACHE_INFORMATION: 'Cache Information',
    StructureType.PORT_CONNECTOR_INFORMATION: 'Port Connector Information',
    StructureType.SYSTEM_SLOTS: 'System Slots',
    StructureType.GROUP_ASSOCIATIONS: 'Group Associations',
    StructureType.PHYSICAL_MEMORY_ARRAY: 'Physical Memory Array',
    StructureType.MEMORY_DEVICE: 'Memory Device',
    StructureType.MEMORY_ARRAY_MAPPED_ADDRESS: 'Memory Array Mapped Address',
    StructureType.MEMORY_DEVICE_MAPPED_ADDRESS: 'Memory Device Mapped Address',
    StructureType.SYSTEM_BOOT_INFORMATION: 'System Root Information',
    StructureType.IPMI_DEVICE_INFORMATION: 'IPMI Device Information',
    StructureType.SYSTEM_POWER_SUPPLY_STRUCTURE: (
        'System Power Supply Structure'
    ),
    StructureType.ONBOARD_DEVICES_EXTENDED_INFORMATION: (
        'Onboard Devices Extended Information'
    ),
    StructureType.GOOGLE_BRIDGE_DEVICE_STRUCTURE: (
        'Google Bridge Device Structure'
    ),
    StructureType.GOOGLE_LINK_DEVICE_STRUCTURE: 'Google Link Device Structure',
    StructureType.GOOGLE_CPU_LINK_STRUCTURE: 'Google CPU Link Structure',
}

class FieldValueEnums(enum.Enum):
  """List all enums used to verify field value of records."""
  CHASSIS_TYPES = ['Main Server Chassis', 'Rack Mount Chassis']
  CHASSIS_LOCK = ['Present', 'Not Present']
  PROCESSOR_TYPE = ['Central Processor']
  SYSTEM_SLOTS_CURRENT_USAGE = ['In Use', 'Available', 'Unknown']
  SYSTEM_SLOTS_LENGTH = ['Short', 'Long']
  PHYSICAL_MEMORY_ARRAY_LOCATION = ['System Board Or Motherboard']
  PHYSICAL_MEMORY_ARRAY_USE = ['System Memory']
  # Type 17
  MEMORY_DEVICE_FORM_FACTOR = ['Unknown', 'DIMM']
  MEMORY_DEVICE_TYPES = ['Unknown', 'DDR4', 'LPDDR4', 'DDR5']
  IPMI_DEVICE_INTERFACE_TYPES = [
      r'BT \(Block Transfer\)',
      r'KCS \(Keyboard Control Style\)',
  ]


class FieldValueRegexps(enum.Enum):
  """List all regex patterns used to verify field value of records."""
  NUMBER_REGEXP = r'\d+'
  NUMBER_WITH_UNKNOWN_REGEXP = r'\d+|unknown'
  HEX_REGEXP = r'0x[0-9A-Fa-f]+'
  SPEED_REGEXP = r'(Unknown)|(\d+ [KMG]T/s)'
  SIZE_REGEXP = r'(Unknown)|(No Module Installed)|(\d+ ([kmgtKMGT]B|bits))'
  VERSION_REGEXP = r'[\d.]+'
  DATE_REGEXP = r'\d{2}/\d{2}/\d{4}'
  DEVPATH_REGEXP = r'[\w/]*'
  OEM_FOR_GOOGLE_REGEXP = r'0x[0-9A-Fa-f]*67'
  VENDOR_FOR_GOOGLE_REGEXP = r'.*Google.*'
  SOCKET_DESIGNATION_REGEXP = r'(CPU|P)\d+'
  PROCESSOR_STATUS_REGEXP = (
      r'(Unpopulated)|(Populated,\s(Unknown|Enabled|Disabled By User|Disabled'
      r' By BIOS|Idle<OUT OF SPEC>|Other))'
  )