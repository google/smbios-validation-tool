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
"""Module for defining matching conditions of a rule against a DMI table."""


class RecordTypeMatcher:
  """A matcher that matches DMI records with a specific type id.

  Attributes:
    type_id: an integer representing type of a table.
  """

  def __init__(self, type_id):
    self.type_id = type_id

  def match(self, record):
    return record.type_id == self.type_id


class Matcher:
  """Class for matching all the matchers against a DMI table.

  Attributes:
    matchers: A list of matchers. Each matcher is an instance of a xxMatcher
      class defined in this file.
  """

  def __init__(self, matchers):
    self.matchers = matchers

  def is_matched_record(self, record):
    for matcher in self.matchers:
      if not matcher.match(record):
        return False
    return True
