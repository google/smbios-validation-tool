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
"""Tests for smbios_validation_tool.rules."""

import os

import dmiparse
from smbios_validation_tool import constants
from smbios_validation_tool import rules

from google3.pyglib import resources
from google3.testing.pybase import googletest

TEST_PATH = 'google3/third_party/py/smbios_validation_tool/test_data'


class RulesTest(googletest.TestCase):

  def setUp(self):
    super(RulesTest, self).setUp()
    good_data_path = os.path.join(TEST_PATH,
                                  'less_compliant_smbios_records.txt')
    good_data_file = resources.GetResourceFilename(good_data_path)
    bad_data_path = os.path.join(TEST_PATH,
                                 'not_less_compliant_smbios_records.txt')
    bad_data_file = resources.GetResourceFilename(bad_data_path)
    self.good_records, self.good_groups = dmiparse.DmiParser(
        good_data_file).parse()
    self.bad_records, self.bad_groups = dmiparse.DmiParser(
        bad_data_file).parse()

  def _get_err_and_action_msgs(self, record_type):
    err_action_msgs = {}
    for handle in self.bad_groups[record_type]:
      record = self.bad_records[handle]
      for rule in rules.rules:
        if rule.matchers.is_matched_record(
            record) and not rule.validators.validate_rule(
                record, self.bad_records):
          err_msg = rule.err_msg + '\nHandle ID: ' + record.handle_id
          err_action_msgs[err_msg] = rule.action_msg
    return err_action_msgs

  def testGoodDataPassesAllRulesForIndividualRecords(self):
    err_msgs = []
    for record in self.good_records.values():
      for rule in rules.rules:
        if rule.matchers.is_matched_record(
            record) and not rule.validators.validate_rule(
                record, self.good_records):
          err_msgs.append(rule.err_msg + '\nHandle ID: ' + record.handle_id)
    self.assertEmpty(err_msgs)

  def testBadDataPromptsExpectedErrorMessagesForBiosInformationRecords(self):
    err_action_msgs = self._get_err_and_action_msgs(
        constants.RecordType.BIOS_RECORD)

    self.assertEqual(
        err_action_msgs, {
            'ERROR: Invalid Vendor field in Type 0 (BIOS Information) record.\nHandle ID: 0x0000':
                'ACTION: BIOS Vendor string should contain "Google".\nWithout that our software will ignore the OEM structures.',
        })

  def testBadDataPromptsExpectedErrorMessagesForChassisRecords(self):
    err_action_msgs = self._get_err_and_action_msgs(
        constants.RecordType.CHASSIS_RECORD)

    self.assertEqual(
        err_action_msgs, {
            'ERROR: Invalid Type field in Type 3 (Chassis) record.\nHandle ID: 0x0003':
                ('ACTION: Please populate Type field with valid string.\n'
                 'Valid Type(s): Main Server Chassis, Rack Mount Chassis'),
            'ERROR: Invalid Lock field in Type 3 (Chassis) record.\nHandle ID: 0x0003':
                ('ACTION: Please populate Lock field with valid string.\n'
                 'Valid Lock Status: Present, Not Present'),
            'ERROR: Invalid OEM Information field in Type 3 (Chassis) record.\nHandle ID: 0x0003':
                ('ACTION: Please populate OEM Information field with valid hex value.\n'
                 'OEM Byte 0 must be 0x67, which is the identification for Google OEM Info.'
                )
        })

  def testBadDataPromptsExpectedErrorMessagesForProcessorRecords(self):
    err_action_msgs = self._get_err_and_action_msgs(
        constants.RecordType.PROCESSOR_RECORD)

    self.assertEqual(
        err_action_msgs, {
            'ERROR: Invalid Type field in Type 4 (Processor Information) record.\nHandle ID: 0x0122':
                ('ACTION: Please populate Type field with valid string.\n'
                 'Valid Processor Type(s): Central Processor')
        })

  def testBadDataPromptsExpectedErrorMessagesForGroupAssociationsRecords(self):
    err_action_msgs = self._get_err_and_action_msgs(
        constants.RecordType.GROUP_ASSOCIATIONS_RECORD)

    self.assertEqual(
        err_action_msgs, {
            'ERROR: Invalid Items field in Type 14 (Group Associations) record.\nHandle ID: 0x0297':
                ('ACTION: Please populate Items field with valid item count and strings.\n'
                 'At least one item must be listed in the record.'),
            'ERROR: Invalid Items field in Type 14 (Group Associations) record.\nHandle ID: 0x02C9':
                ('ACTION: Please populate Items field with valid item count and strings.\n'
                 'At least one item must be listed in the record.'),
            'ERROR: Invalid Items field in Type 14 (Group Associations) record.\nHandle ID: 0x02CB':
                ('ACTION: Please populate Items field with valid item count and strings.\n'
                 'At least one item must be listed in the record.'),
            'ERROR: Invalid Items field in Type 14 (Group Associations) record.\nHandle ID: 0x02CC':
                'Please make sure all handles are unique in items of group associations records.'
        })


if __name__ == '__main__':
  googletest.main()
