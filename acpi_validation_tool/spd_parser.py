from enum import Enum
from acpi_validation_tool import utils
from acpi_validation_tool.ddr4_parser import Ddr4Parser

class SpdType(Enum):
    kTypeUnknown = 0
    kTypeDdr1 = 7
    kTypeDdr2 = 8
    kTypeFbdimm = 9
    kTypeDdr3 = 11
    kTypeDdr4 = 12
    kTypeNvm = 13
    kTypeDdr5 = 18

class SpdParser:
  def __init__(self, data):
    self.data = data

  def spd_parse(self):
    spd_type = self.data[2]
    spd_size = 0
    if spd_type == SpdType.kTypeDdr4.value:
      spd_size = Ddr4Parser(self.data).ddr4_parse()
    else:
      utils.color_print("ERROR: SPD type not supported", utils.ERROR_COLOR)

    return spd_type, spd_size