# Lint as: python3
"""Module for parsing BDAT table into structured SPD data."""

from acpi_validation_tool import constants
from acpi_validation_tool import utils
from acpi_validation_tool.spd_parser import SpdParser
import collections
import itertools
import re
import subprocess
import binascii
import uuid
import struct

BYTE_ORDER = 'little'

class SPD_DATA:

  def __init__(self):
    self.datatype = 0           # MEM_SPD_DATA_ENTRY_HEADER.Type
    self.socket = 0             # MEM_SPD_DATA_ENTRY_MEMORY_LOCATION.Socket
    self.channel = 0            # MEM_SPD_DATA_ENTRY_MEMORY_LOCATION.Channel
    self.dimm = 0               # MEM_SPD_DATA_ENTRY_MEMORY_LOCATION.Dimm
    self.no_of_bytes = 0        # MEM_SPD_ENTRY_TYPE0.NumberOfBytes
    self.type = 0               # Type of DIMM
    self.size = 0               # Size of DIMM
    self.data = bytearray()     # expected to be self.no_of_bytes, which is 512 bytes for DDR4.

  def __str__(self):
    return str(self.__dict__)

class BDAT_METADATA:

  def __init__(self):
    self.signature = ''         # BDAT_HEADER_STRUCTURE.BiosDataSignature[8]
    self.data_size = 0          # BDAT_HEADER_STRUCTURE.BiosDataStructSize
    self.crc = 0                # BDAT_HEADER_STRUCTURE.Crc16
    self.schema_count = 0       # BDAT_SCHEMA_LIST_STRUCTURE.SchemaListLength
    self.schema_list = []       # BDAT_SCHEMA_LIST_STRUCTURE.Schemas[SchemaListLength]

  def __str__(self):
    return str(self.__dict__)


class SCHEMA_DATA:

  def __init__(self):
    self.schema_guid = ""       # BDAT_SCHEMA_HEADER_STRUCTURE.SchemaId
    self.data_size = 0          # BDAT_SCHEMA_HEADER_STRUCTURE.DataSize
    self.crc = 0                # BDAT_SCHEMA_HEADER_STRUCTURE.Crc16
    self.spd_data_id_guid = ""  # MEM_SPD_RAW_DATA_HEADER.MemSpdGuid

  def __str__(self):
    return str(self.__dict__)


class BdatParser:
  """Class that parses BDAT raw data to structured data.

  Attributes:
    file: A string represents path to BDAT dump file.
  """

  def __init__(self, file):
    self.file = file

  def load_data(self):
    """Method to load raw data.

    It will read the content of the user assigned file.

    Returns:
      content of the file
    """

    if not self.file:
      return bytearray()

    with open(self.file, 'rb') as fp:
      return fp.read()

  def parse_metadata(self, data):
    """Method to parse metadata of BDAT table.

    It will create a BDAT_METADATA object by parsing the first constants.BDAT_STRUCTURE_SIZE + 4*(# of schemas) bytes of the file.

    Returns:
      BDAT_METADATA object
    """
    metadata = BDAT_METADATA()
    metadata.signature = data[:8].decode("utf-8")
    metadata.data_size = int.from_bytes(data[8:12], byteorder=BYTE_ORDER)
    metadata.crc = int.from_bytes(data[12:14], byteorder=BYTE_ORDER)
    metadata.schema_count = int.from_bytes(data[32:34], byteorder=BYTE_ORDER)

    for i in range(metadata.schema_count):
      start_offset = constants.BDAT_STRUCTURE_SIZE + 4*i
      metadata.schema_list.append(int.from_bytes(data[start_offset:start_offset + 4], byteorder=BYTE_ORDER))

    return metadata

  def parse_schemadata(self, metadata, data):
    """Method to parse schemadata of UEFI standard SPD schema section 5.8

    It will throw an error if the expected SPD schema is not found,
    otherwise it will populate a BDAT_SCHEMADATA object

    Returns:
      BDAT_SCHEMADATA object
    """
    schema_data = SCHEMA_DATA()
    spd_data_list = []
    utils.color_print("No. of schemas expected = " + str(metadata.schema_count), utils.INFO_COLOR)
    for i in range(metadata.schema_count):
      schema_offset = metadata.schema_list[i]
      utils.color_print(str(i+1) + "th Schema ID found = " + str(uuid.UUID(bytes=data[schema_offset:schema_offset + 16])), utils.INFO_COLOR)
      if str(uuid.UUID(bytes=data[schema_offset:schema_offset + 16])) == constants.UEFI_SPD_SCHEMA_GUID:
        utils.color_print('UEFI SPD schema found!!!', utils.VALID_COLOR)
        schema_data.schema_guid = str(uuid.UUID(bytes=data[schema_offset:schema_offset + 16]))
        schema_data.data_size = int.from_bytes(data[schema_offset + 16: schema_offset + 20], byteorder=BYTE_ORDER)
        schema_data.crc = int.from_bytes(data[schema_offset + 20: schema_offset + 22], byteorder=BYTE_ORDER)
        schema_data.spd_data_id_guid = str(uuid.UUID(bytes=data[schema_offset + 22:schema_offset + 38]))

        next_dimm_offset = schema_offset + constants.BDAT_MEM_SPD_STRUCTURE_SIZE
        while(next_dimm_offset < schema_offset + schema_data.data_size):
          spd_buf = data[next_dimm_offset:]
          spd = SPD_DATA()
          spd.datatype = int.from_bytes(spd_buf[: 4], byteorder=BYTE_ORDER)
          spd.socket = int.from_bytes(spd_buf[6: 7], byteorder=BYTE_ORDER)
          spd.channel = int.from_bytes(spd_buf[7: 8], byteorder=BYTE_ORDER)
          spd.dimm = int.from_bytes(spd_buf[8: 9], byteorder=BYTE_ORDER)
          spd.no_of_bytes = int.from_bytes(spd_buf[9: 11], byteorder=BYTE_ORDER)
          spd.data = spd_buf[constants.MEM_SPD_ENTRY_TYPE0_SIZE: constants.MEM_SPD_ENTRY_TYPE0_SIZE + spd.no_of_bytes]

          spd.type, spd.size = SpdParser(spd.data).spd_parse()

          next_dimm_offset = next_dimm_offset + constants.MEM_SPD_ENTRY_TYPE0_SIZE + spd.no_of_bytes
          spd_data_list.append(spd)

    if not schema_data.schema_guid:
      utils.color_print('ERROR: UEFI SPD schema not found!!!', utils.ERROR_COLOR)

    return schema_data, spd_data_list

  def parse(self):
    """Method to parse the BDAT data.

    It will read the input file and parse the byte data into structured objects

    Returns:
      Input file data
      BDAT_METADATA object
      BDAT_SCHEMADATA object
      List of SPD_DATA objects, one entry per DIMM
    """

    data = self.load_data()
    if not data:
      utils.color_print('ERROR: File is empty!', utils.ERROR_COLOR)

    metadata = self.parse_metadata(data)

    schema_data, spd_data_list = self.parse_schemadata(metadata, data)

    return data, metadata, schema_data, spd_data_list
