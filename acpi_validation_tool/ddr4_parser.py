'''
// Layout of fields in a DDR4 SPD.
  // Individual field descriptions are taken directly from the JEDEC spec.
  struct Ddr4Fields {
    // Number of Serial PD Bytes Written / SPD Device Size / CRC Coverage
    uint8_t bytes_used_bytes_total_crc_coverage;
    // SPD Revision
    uint8_t spd_revision;
    // Key Byte / DRAM Device Type
    uint8_t dram_device_type;
    // Key Byte / Module Type
    uint8_t module_type;
    // SDRAM Density and Banks
    uint8_t sdram_density_and_banks;
    // SDRAM Addressing
    uint8_t sdram_addressing;
    // SDRAM Package Type
    uint8_t sdram_package_type;
    // SDRAM Optional Features
    uint8_t sdram_optional;
    // SDRAM Thermal and Refresh Options
    uint8_t sdram_thermal_and_refresh;
    // Other SDRam Optional Features
    uint8_t other_sdram_optional;
    // Reserved
    uint8_t reserved_0;
    // Module Nominal Voltage, VDD
    uint8_t vdd;
    // Module Organization
    uint8_t ranks_width;
    // Module Memory Bus Width
    uint8_t memory_bus_width;
    // Module Thermal Sensor
    uint8_t thermal_sensor;
    // Extended Module Type
    uint8_t extended_module_type;
    // Reserved
    uint8_t reserved_1;
    // Timebases
    uint8_t timebases;
    // SDRAM Minimum Cycle Time (tCKAVGmin)
    uint8_t t_ckavg_min;
    // SDRAM Maximum Cycle Time (tCKAVGmax)
    uint8_t t_ckavg_max;
    // CAS Latencies Supported, First Byte
    uint8_t cas_first;
    // CAS Latencies Supported, Second Byte
    uint8_t cas_second;
    // CAS Latencies Supported, Third Byte
    uint8_t cas_third;
    // CAS Latencies Supported, Fourth Byte
    uint8_t cas_fourth;
    // Minimum CAS Latency Time (tAAmin)
    uint8_t t_aa_min;
    // Minimum RAS to CAS Delay Time (tRCDmin)
    uint8_t t_rcd_min;
    // Minimum Row Precharge Delay Time (tRPmin)
    uint8_t t_rp_min;
    // Upper Nibbles for tRASmin and tRCmin
    uint8_t t_rasmin_t_rcmin_upper_nibbles;
    // Minimum Active to Precharge Delay Time (tRASmin), Least Significant Byte
    uint8_t t_ras_min_lsb;
    // Minimum Active to Active/Refresh Delay Time (tRCmin), Least
    // Significant Byte
    uint8_t t_rc_min_lsb;
    // Minimum Refresh Recovery Delay Time (tRFC1min), Least Significant Byte
    uint8_t t_rfc1_min_lsb;
    // Minimum Refresh Recovery Delay Time (tRFC1min), Most Significant Byte
    uint8_t t_rfc1_min_msb;
    // Minimum Refresh Recovery Delay Time (tRFC2min), Least Significant Byte
    uint8_t t_rfc2_min_lsb;
    // Minimum Refresh Recovery Delay Time (tRFC2min), Most Significant Byte
    uint8_t t_rfc2_min_msb;
    // Minimum Refresh Recovery Delay Time (tRFC4min), Least Significant Byte
    uint8_t t_rfc4_min_lsb;
    // Minimum Refresh Recovery Delay Time (tRFC4min), Most Significant Byte
    uint8_t t_rfc4_min_msb;
    // Minimum Four Activate Window Time (tFAWmin), Most Significant Nibble
    uint8_t t_faw_min_ms_nibble;
    // Minimum Four Activate Window Time (tFAWmin), Least Significant Byte
    uint8_t t_faw_min_lsb;
    // Minimum Activate to Activate Delay Time (tRRD_Smin), different bank group
    uint8_t t_rrd_smin_diff_bank;
    // Minimum Activate to Activate Delay Time (tRRD_Lmin), same bank group
    uint8_t t_rrd_smin_same_bank;
    // Minimum CAS to CAS Delay Time (tCCD_Lmin), same bank group
    uint8_t t_ccd_lmin_same_bank;
    // Reserved
    uint8_t reserved_2[19];
    // Connector to SDRAM Bit Mapping
    uint8_t connector_to_sdram[18];
    // Reserved
    uint8_t reserved_3[39];
    // Fine Offset for Minimum CAS to CAS Delay Time (tCCD_Lmin), same bank
    // group
    uint8_t fine_t_ccd_lmin_same_bank;
    // Fine Offset for Minimum Activate to Activate Delay Time (tRRD_Lmin), same
    // bank group
    uint8_t fine_t_rrd_lmin_same_bank;
    // Fine Offset for Minimum Activate to Activate Delay Time (tRRD_Smin),
    // different bank group
    uint8_t fine_t_rrd_smin_diff_bank;
    // Fine Offset for Minimum Activate to Activate/Refresh Delay Time (tRCmin)
    uint8_t fine_t_rc_min;
    // Fine Offset for Minimum Row Precharge Delay Time (tRPmin)
    uint8_t fine_t_rp_min;
    // Fine Offset for Minimum RAS to CAS Delay Time (tRCDmin)
    uint8_t fine_t_rcd_min;
    // Fine Offset for Minimum CAS Latency Time (tAAmin)
    uint8_t fine_t_aa_min;
    // Fine Offset for SDRAM Maximum Cycle Time (tCKAVGmax)
    uint8_t fine_t_ckavg_max;
    // Fine Offset for SDRAM Minimum Cycle Time (tCKAVGmin)
    uint8_t fine_t_ckavg_min;
    // CRC for Base Configuration Section, Least Significant Byte
    uint8_t crc_base_config_lsb;
    // CRC for Base Configuration Section, Most Significant Byte
    uint8_t crc_base_config_msb;
    // Module-Specific Section: Bytes 60-116
    uint8_t module_specific_section[128];
    // Reserved
    uint8_t reserved_4[64];
    // Module Manufacturer ID Code, Least Significant Byte
    uint8_t module_manufacturer_id_cont_bytes;
    // Module Manufacturer ID Code, Most Significant Byte
    uint8_t module_manufacturer_id_index;
    // Module Manufacturing Location
    uint8_t manufacturing_location;
    // Module Manufacturing Date
    uint8_t manufacturing_year;  // BCD
    uint8_t manufacturing_week;  // BCD
    // Module Serial Number
    uint8_t serial_number[4];
    // Module Part Number
    uint8_t part_number[20];
    // Module Revision Code
    uint8_t revision_code;
    // DRAM Manufacturer ID Code, Least Significant Byte
    uint8_t dram_manufacturer_id_cont_bytes;
    // DRAM Manufacturer ID Code, Most Significant Byte
    uint8_t dram_manufacturer_id_index;
    // DRAM Stepping
    uint8_t dram_stepping;
    // Manufacturer's Specific Data
    uint8_t manufacturer_data[29];
    // Reserved
    uint8_t reserved_5[2];
    // Open for Customer Use
    uint8_t customer_data[128];
  }
'''

from enum import Enum
from acpi_validation_tool import utils

class PackageType(Enum):
  PACKAGE_TYPE_UNSPECIFIED = 0
  PACKAGE_TYPE_DDP_QDP = 1
  PACKAGE_TYPE_3DS =2

class Ddr4Parser:
  def __init__(self, data):
    self.data = data    # 512 bytes

  def density(self, sdram_density_and_banks):
    # Density stored in bits 3:0 as 256 megabits * 2^(stored value).
    density = 256 << (sdram_density_and_banks & 0x0f)
    if (density < 256 or density > 32768):
      # Values other than 256, 512, 1024, 2048, 4096, 8192, 16384, 32768 are invalid.
      utils.color_print("ERROR: Invalid SPD Density", utils.ERROR_COLOR)
    density >>= 3  # Convert megabits to megabytes.
    return density

  def ranks(self, sdram_package_type, ranks_width):
    # Returns logical ranks
    # SDRAM package type is bits 6:4
    package_type = (sdram_package_type & 0x03)
    if (package_type < 0 or package_type > 2):
      # Values outside the interval [0,2] are invalid.
      utils.color_print("ERROR: Invalid SPD Package Type", utils.ERROR_COLOR)
    # Package Ranks is (bits 5:3 with offset 1)
    package_ranks = (1 + ((ranks_width >> 3) & 0x07))
    if (package_ranks < 1 or package_type > 4):
      # Values outside the interval [1,4] are invalid.
      utils.color_print("ERROR: Invalid SPD Package ranks", utils.ERROR_COLOR)
    if (package_type == PackageType.PACKAGE_TYPE_3DS.value):
      # 3DS - Logical Ranks is package ranks * die count
      die_count = (1 + ((sdram_package_type >> 4) & 0x07))
      if (die_count < 1 or die_count > 8):
        # Values outside the interval [1,8] are invalid.
        utils.color_print("ERROR: Invalid SPD Die Count", utils.ERROR_COLOR)
      logical_ranks = package_ranks * die_count
    else:
      # SDP, DDP, QDP - Logical Ranks is package ranks * 1.
      logical_ranks = package_ranks
    if (logical_ranks < 1 or logical_ranks > 32):
      # Values outside the interval [1,32] are invalid.
      utils.color_print("ERROR: Invalid SPD Logical Ranks", utils.ERROR_COLOR)
    return logical_ranks

  def device_width(self, ranks_width):
    # Width stored in bits 2:0 as 4 bits * 2^(stored value).
    device_width = 4 * (1 << (ranks_width & 0x07))
    if (device_width < 4 or device_width > 32):
      # Values other than 4, 8, 16, 32 are invalid.
      utils.color_print("ERROR: Invalid SPD Device Width", utils.ERROR_COLOR)
    return device_width

  def bus_width(self, memory_bus_width):
    # Primary bus width in bits 2:0 as 8 bits * 2^(stored value).
    bus_width = 8 << (memory_bus_width & 0x07)
    if (bus_width < 8 or bus_width > 64):
      # Values other than 8, 16, 32, 64 are invalid.
      utils.color_print("ERROR: Invalid SPD Memory Bus Width", utils.ERROR_COLOR)
    return bus_width

  def ddr4_parse(self):

    density = self.density(self.data[4])
    ranks = self.ranks(self.data[6], self.data[12])
    device_width = self.device_width(self.data[12])
    bus_width = self.bus_width(self.data[13])
    spd_size = (density * ranks * bus_width) // device_width

    return spd_size