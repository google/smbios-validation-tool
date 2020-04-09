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
"""Tests for smbios_validation_tool.matcher."""

import os

import dmiparse
from smbios_validation_tool import constants
from smbios_validation_tool import matcher

from google3.pyglib import resources
from google3.testing.pybase import googletest

TEST_PATH = 'google3/third_party/py/smbios_validation_tool/test_data'


class MatcherTest(googletest.TestCase):

  def setUp(self):
    super(MatcherTest, self).setUp()
    data_path = os.path.join(TEST_PATH, 'less_compliant_smbios_records.txt')
    data_file = resources.GetResourceFilename(data_path)
    self.records, _ = dmiparse.DmiParser(data_file).parse()
    self.assertLen(self.records, 382)

  def testRecordTypeMatcherMatchesSingleRecord(self):
    matchers = matcher.Matcher(
        [matcher.RecordTypeMatcher(constants.RecordType.BIOS_RECORD)])
    matched_records = []
    for _, record in self.records.items():
      if matchers.is_matched_record(record):
        matched_records.append(record)
    self.assertLen(matched_records, 1)

  def testRecordTypeMatcherMatchesMultipleRecords(self):
    matchers = matcher.Matcher([
        matcher.RecordTypeMatcher(
            constants.RecordType.GROUP_ASSOCIATIONS_RECORD)
    ])
    matched_records = []
    for _, record in self.records.items():
      if matchers.is_matched_record(record):
        matched_records.append(record)
    self.assertLen(matched_records, 53)


if __name__ == '__main__':
  googletest.main()
