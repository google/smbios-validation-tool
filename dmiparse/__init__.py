# Lint as: python3
"""Module for parsing DMI dump raw data into structured data."""

import collections
import itertools
import re
import subprocess

STATE_RECORD_NAME, STATE_READ_KV, STATE_LIST_PROPERTY = range(3)


class Record:
  """Class that represents a single SMBIOS record.

  Attributes:
    handle_id: a string representing a unique hex value for an SMBIOS record
    type_id: an integer representing the type of an SMBIOS record.
    props: a dictionary maps property name to an instance of Property class that
      stores all properties of the record.
  """

  def __init__(self):
    self.handle_id = ''
    self.type_id = None
    self.props = {}

  def __str__(self):
    return str(self.__dict__)


class Property:
  """Class that represents properties of an SMBIOS table.

  Attributes:
    val: a string stores value of a property (if exists).
    items: a list stores items of a property (if exists).
  """

  def __init__(self, val):
    self.val = val
    self.items = []

  def add_item(self, item):
    self.items.append(item)

  def __str__(self):
    return str(self.__dict__)


class DmiParser:
  """Class that parses DMI dump raw data to structured data.

  Attributes:
    file: A string represents path to DMI dump file, possibly empty.
  """

  def __init__(self, file):
    self.file = file

  def dmidecode_output(self):
    """Method that returns the output of running dmidecode binary."""
    return subprocess.run(['dmidecode'],
                          stdout=subprocess.PIPE).stdout.decode('utf-8')

  def load_dmidump(self):
    """Method to get DMI dump raw data.

    If user assigned a file, it will read the content of the file.
    Otherwise, it will try to run dmidecode binary and get the output.

    Returns:
      content of the file, or output of dmidecode binary
    """

    if not self.file:
      return self.dmidecode_output()

    with open(self.file, 'r') as fp:
      return fp.read()

  def parse(self):
    """Parses DMI dump raw data into structured data.

    Returns:
     records: a dictionary, record handle id => record instance
     groups: a dictionary, record type id => set of record's handle ids
    """

    dmi_dump = self.load_dmidump()
    if not dmi_dump:
      print('WARNING: DMI raw data is empty!')
    lines = dmi_dump.splitlines()
    records = collections.OrderedDict()  # handle_id => record
    groups = collections.defaultdict(list)  # table_type => list of handle ids
    state = None
    record = None
    prop = None

    def get_indent_level(line):
      return len(list(itertools.takewhile(lambda c: c.isspace(), line)))

    for line_num, line in enumerate(lines):
      # Parse the first line of each table, which is in the format of:
      # Handle 0xXX, DMI type X, X bytes
      if line.startswith('Handle'):
        record = Record()
        pattern = re.compile('Handle (0x[0-9A-F]+), DMI type ([0-9]+).*')
        record_info = pattern.match(line)
        record.handle_id = record_info.group(1)
        record.type_id = int(record_info.group(2))
        state = STATE_RECORD_NAME
        continue

      if not line:  # can be just new line before reading any sections.
        if record is not None:
          records[record.handle_id] = record
          groups[record.type_id].append(record.handle_id)
        continue

      if state == STATE_RECORD_NAME:
        state = STATE_READ_KV
      elif state == STATE_READ_KV:
        prop_name, prop_value = [x.strip() for x in line.split(':', 1)]
        prop = Property(prop_value)
        if line_num < len(lines) and get_indent_level(line) < get_indent_level(
            lines[line_num + 1]):
          state = STATE_LIST_PROPERTY
        else:
          record.props[prop_name] = prop
      elif state == STATE_LIST_PROPERTY:
        prop.add_item(line.strip())
        if get_indent_level(line) > get_indent_level(
            lines[line_num + 1]) and get_indent_level(line) <= 2:
          state = STATE_READ_KV
          record.props[prop_name] = prop

    return records, groups
