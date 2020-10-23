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
"""Class to group and print smbios validation errors.

Multiple errors might happen in one smbios record. This class will collect
corresponding error messages and create a dictionary, then print human-readable
debug messagee.
"""

import collections
import termcolor


class ErrorBucket:
  """Class to group and print smbios validation errors."""

  def __init__(self):
    self.bucket = collections.defaultdict(list)

  def add_error(self, handle_id, error_action_msg_pair):
    self.bucket[handle_id].append(error_action_msg_pair)

  def print_buckets(self):
    for handle_id in sorted(self.bucket):
      handle_msg = 'Handle ID: ' + handle_id
      print(termcolor.colored(handle_msg, attrs=['bold']))
      for err_msg, action_msg in self.bucket[handle_id]:
        print(termcolor.colored(err_msg, color='red', attrs=['bold']))
        print(
            termcolor.colored(action_msg, color='yellow', attrs=['underline']))
      print('\n')
