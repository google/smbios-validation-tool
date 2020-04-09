# Lint as: python3
"""Unit tests for dmiparse."""

import os

import dmiparse

from google3.pyglib import resources
from google3.testing.pybase import googletest

TEST_PATH = 'google3/third_party/py/dmiparse/test_data'


class DmiParserTest(googletest.TestCase):

  def setUp(self):
    super(DmiParserTest, self).setUp()
    data_path = os.path.join(TEST_PATH, 'less_compliant_smbios_records.txt')
    self.data_file = resources.GetResourceFilename(data_path)

  def testDmiParseNoDumpFileRaisesException(self):
    with self.assertRaises(FileNotFoundError):
      dmiparse.DmiParser('').parse()

  def testDmiParseReturnsExpectedRecords(self):
    records, _ = dmiparse.DmiParser(self.data_file).parse()

    self.assertLen(records, 4)
    self.assertIn('0x0002', records)
    self.assertIn('0x0125', records)
    self.assertIn('0x0126', records)

  def testDmiParseReturnsValidBaseBoardRecord(self):
    records, _ = dmiparse.DmiParser(self.data_file).parse()
    self.assertIn('0x0002', records)
    base_board_record = records['0x0002']

    self.assertEqual('0x0002', base_board_record.handle_id)
    self.assertEqual(2, base_board_record.type_id)
    self.assertLen(base_board_record.props, 9)

    self.assertIn('Product Name', base_board_record.props)
    self.assertEqual('Magnesium', base_board_record.props['Product Name'].val)
    self.assertEqual([], base_board_record.props['Product Name'].items)

    self.assertIn('Version', base_board_record.props)
    self.assertEqual('1234567890', base_board_record.props['Version'].val)
    self.assertEqual([], base_board_record.props['Version'].items)

    self.assertIn('UUID', base_board_record.props)
    self.assertEqual('03000200-0400-0500-0006-000700080009',
                     base_board_record.props['UUID'].val)
    self.assertEqual([], base_board_record.props['UUID'].items)

    self.assertIn('Location In Chassis', base_board_record.props)
    self.assertEqual('Riser1',
                     base_board_record.props['Location In Chassis'].val)
    self.assertEqual([], base_board_record.props['Location In Chassis'].items)

    self.assertIn('Chassis Handle', base_board_record.props)
    self.assertEqual('0x0003', base_board_record.props['Chassis Handle'].val)
    self.assertEqual([], base_board_record.props['Chassis Handle'].items)

    self.assertIn('MAC Address', base_board_record.props)
    self.assertEqual('00:1b:83:15:a3:24',
                     base_board_record.props['MAC Address'].val)
    self.assertEqual([], base_board_record.props['MAC Address'].items)

    self.assertIn('Contained Object Handles', base_board_record.props)
    self.assertEqual('5',
                     base_board_record.props['Contained Object Handles'].val)
    self.assertEqual(['0x009A', '0x009B', '0x009C', '0x009D', '0x009E'],
                     base_board_record.props['Contained Object Handles'].items)

    self.assertIn('Characteristics', base_board_record.props)
    self.assertEqual('', base_board_record.props['Characteristics'].val)
    self.assertEqual([
        'PCI is supported', 'BIOS is upgradeable', 'ACPI is supported',
        'UEFI is supported'
    ], base_board_record.props['Characteristics'].items)

  def testDmiParseIndentation(self):
    records, _ = dmiparse.DmiParser(self.data_file).parse()
    self.assertIn('0x0058', records)
    oem_specific_record = records['0x0058']

    self.assertIn('Strings', oem_specific_record.props)
    self.assertEqual([
        'WLYDCRB.86B.WR.64.2019.19.3.03.1837', '0. 0.   0', '4:2.1.21', 'N/A',
        'FRU: Ver 1.21', 'N/A', 'N/A'
    ], oem_specific_record.props['Strings'].items)

  def testDmiParseReturnsValidGroups(self):
    _, groups = dmiparse.DmiParser(self.data_file).parse()
    self.assertIn(2, groups)
    self.assertEqual(['0x0002'], groups[2])

    self.assertIn(14, groups)
    self.assertEqual(['0x0125', '0x0126'], groups[14])


if __name__ == '__main__':
  googletest.main()
