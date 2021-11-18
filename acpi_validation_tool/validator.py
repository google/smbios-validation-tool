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
from . import BdatParser
import termcolor

FLAGS = flags.FLAGS

flags.DEFINE_string('file', '', 'dmidecode dump file path')


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


def main(argv):
  if len(argv) > 1:
    raise app.UsageError('Too many command-line arguments.')

  print_source_code_header()
  meta_data, spd_data = BdatParser(FLAGS.file).parse()
  print(spd_data)

  is_less_compliant = True

  # Validate rules for BDAT record


  if is_less_compliant:
    print(
        termcolor.colored(
            '**The SMBIOS implementation in this host is LESS compliant.**\n',
            color='green',
            attrs=['bold']))
  else:
    print(
        termcolor.colored(
            '**The SMBIOS implementation in this host lacks LESS compliance.**\n',
            color='red',
            attrs=['bold']))


if __name__ == '__main__':
  app.run(main)
