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
"""Module for defining constants used in the tool."""

import enum


class RecordType(enum.IntEnum):
  """Define SMBIOS record types."""
  BIOS_RECORD = 0
  SYSTEM_RECORD = 1
  BASEBOARD_RECORD = 2
  CHASSIS_RECORD = 3
  PROCESSOR_RECORD = 4
  CACHE_RECORD = 7
  PORT_CONNECTOR_RECORD = 8
  SYSTEM_SLOTS_RECORD = 9
  GROUP_ASSOCIATIONS_RECORD = 14
  PHYSICAL_MEMORY_ARRAY_RECORD = 16
  MEMORY_DEVICE_RECORD = 17
  MEMORY_ARRAY_MAPPED_ADDRESS_RECORD = 19
  MEMORY_DEVICE_MAPPED_ADDRESS_RECORD = 20
  SYSTEM_BOOT_INFO_RECORD = 32
  IPMI_DEVICE_INFO_RECORD = 38
  SYSTEM_POWER_SUPPLY_RECORD = 39
  GOOGLE_BRIDGE_DEVICE_RECORD = 160
  GOOGLE_LINK_DEVICE_RECORD = 161
  GOOGLE_CPU_LINK_RECORD = 162


class FieldValueEnums(enum.Enum):
  """List all enums used to verify field value of records."""
  CHASSIS_TYPES = ['Main Server Chassis', 'Rack Mount Chassis']
  CHASSIS_LOCK = ['Present', 'Not Present']
  PROCESSOR_TYPE = ['Central Processor']
  PROCESSOR_STATUS = ['Populated', 'Unpopulated', 'Enabled', 'Disabled']
  SYSTEM_SLOTS_CURRENT_USAGE = ['In Use', 'Available']
  SYSTEM_SLOTS_LENGTH = ['Short', 'Long']
  PHYSICAL_MEMORY_ARRAY_LOCATION = ['System Board Or Motherboard']
  PHYSICAL_MEMORY_ARRAY_USE = ['System Memory']
  MEMORY_DEVICE_FORM_FACTOR = ['Unknown', 'DIMM']
  MEMORY_DEVICE_TYPES = ['Unknown', 'DDR4', 'LPDDR4']
  IPMI_DEVICE_INTERFACE_TYPES = [
      'BT (Block Transfer)', 'KCS (Keyboard Control Style)'
  ]


class FieldValueRegexps(enum.Enum):
  """List all regex patterns used to verify field value of records."""
  NUMBER_REGEXP = r'\d+'
  HEX_REGEXP = r'0x[0-9A-Fa-f]+'
  SPEED_REGEXP = r'(Unknown)|(\d+ [KMG]T/s)'
  SIZE_REGEXP = r'(Unknown)|(No Module Installed)|(\d+ ([kmgtKMGT]B|bits))'
  VERSION_REGEXP = r'[\d.]+'
  DATE_REGEXP = r'\d{2}/\d{2}/\d{4}'
  DEVPATH_REGEXP = r'[\w/]*'
  OEM_FOR_GOOGLE_REGEXP = r'0x[0-9A-Fa-f]*67'
  VENDOR_FOR_GOOGLE_REGEXP = r'.*Google.*'
  CPU_REGEXP = r'CPU\d+'
