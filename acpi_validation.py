#!/usr/bin/env python3
#
# Lint as: python3
# Copyright 2021 Google LLC
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
"""Main function to run ACPI validation."""

from absl import app
from absl import flags
from acpi_validation_tool import BdatParser
from acpi_validation_tool import constants
from acpi_validation_tool import utils

FLAGS = flags.FLAGS

flags.DEFINE_string('file', '', 'bdat data file path')


def print_source_code_header():
  """Print header when running the binary."""
  print('*********************************************************************')
  print('ACPI BDAT Validation Tool\n')
  print('Copyright 2021 Google LLC')
  print('Licensed under the Apache License, Version 2.0 (the "License")')
  print('you may not use this file except in compliance with the License.')
  print('You may obtain a copy of the License at\n')
  print('https://www.apache.org/licenses/LICENSE-2.0\n')
  print('Unless required by applicable law or agreed to in writing, software')
  print('distributed under the License is distributed on an "AS IS" BASIS,')
  print(
      'WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.'
  )
  print('See the License for the specific language governing permissions and')
  print('limitations under the License.')
  print(
      '*********************************************************************\n')

def validate_spd_data(spd_data_list):
  utils.color_print("Number of DIMMs found = " + str(len(spd_data_list)), utils.INFO_COLOR)
  utils.color_print("Printing SPD INFO ----------- \n", utils.INFO_COLOR)
  for spd in spd_data_list:
    if spd.no_of_bytes != constants.SPD_DDR4_SIZE:
      utils.color_print("Unexpected size of spd info," + str(spd.no_of_bytes), utils.ERROR_COLOR)
    utils.color_print("  Node:{},Channel:{},dimm:{} => Size:{}MB".format(
                               spd.socket, spd.channel, spd.dimm, spd.size), utils.INFO_COLOR)

def validate_schemadata(schema_data):
  if schema_data.spd_data_id_guid == constants.MEM_SPD_DATA_ID_GUID:
    utils.color_print("Memory SPD data identification GUID matched!", utils.VALID_COLOR)
  else:
    utils.color_print("Memory SPD data identification GUID did not match!" +
    "Expected:{} , Actual:{}".format(constants.MEM_SPD_DATA_ID_GUID, schema_data.spd_data_id_guid),
    utils.ERROR_COLOR)

def validate_metadata(metadata, file_data):
  if metadata.signature == 'BDATHEAD':
    utils.color_print("**BDAT Table signature matched**\n", utils.VALID_COLOR)
  else:
    utils.color_print("**BDAT Table signature NOT matched!!!!**\n", utils.ERROR_COLOR)

  utils.color_print("Size of data file = " + str(len(file_data)) + "B, Size of BDAT table = " + str(metadata.data_size) + "B", utils.INFO_COLOR)
  if len(file_data) == metadata.data_size:
    utils.color_print("Size of data file matches expected size of the BDAT table", utils.VALID_COLOR)
  else:
    utils.color_print("Size of data file does not match expected size of the BDAT table", utils.ERROR_COLOR)

def main(argv):
  if len(argv) > 1:
    raise app.UsageError('Too many command-line arguments.')

  print_source_code_header()
  file_data, metadata, schema_data, spd_data = BdatParser(FLAGS.file).parse()

  # Validate BDAT metadata
  validate_metadata(metadata, file_data)

  # Validate Schema Header data
  validate_schemadata(schema_data)

  # Validate SPD data
  validate_spd_data(spd_data)

if __name__ == '__main__':
  app.run(main)
