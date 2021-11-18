# ACPI BDAT Validation Tool

## What is it?

ACPI BDAT Validation Tool is an open source tool that will validate the ACPI BDAT table in vendor's firmware (BIOS) conformance to the [UEFI standard SPD schema](https://uefi.org/sites/default/files/resources/BDAT%20Specification%20v4.0%20Draft5_0.pdf) section 5.8 - DIMM SPD RAW Data Schema 7.

## Terminology

*   **ACPI** - Advanced Configuration and Power Interface. ACPI provides an open standard that operating systems can use to discover and configure computer hardware components, to perform power management e.g. putting unused hardware components to sleep, to perform auto configuration e.g. Plug and Play and hot swapping, and to perform status monitoring.

*   **BDAT** - BIOS Data ACPI Table. ACPI table that, in our case, points to a structure with the SPD info as defined by the UEFI standard.

*   **SPD** - Serial Presence Detect (SPD) is information stored in an electrically erasable programmable read-only memory (EEPROM) chip on a synchronous dynamic random access memory (SDRAM) memory module that tells the basic input/output system (BIOS) the module's size, data width, speed, and voltage.

## Execution

Access to the root directory of the tool and simply run:

```shell
python3 acpi_validation.py --file=path/to/your/bdat_dump_file
```

## Extract BDAT table from the system

### Find address of BDAT
The ACPI table header for BDAT can be found by running the following command. The last 64 bits in the header correspond to the address at which the BDAT table is located in memory.

NOTE: The system uses little endian format in this example so values need to be converted accordingly.

```shell
$ xxd /sys/firmware/acpi/tables/BDAT
00000000: 4244 4154 3000 0000 0122 416d 7065 7265  BDAT0...."Ampere
00000010: 416c 7472 6120 2020 0200 0000 414d 502e  Altra   ....AMP.
00000020: 1300 0001 0008 0000 1800 5efd 3f08 0000  ..........^.?...
```

### Find size of BDAT table

The address of the table in this example is 0x0000083ffd5e0018, after conversion from 1800 5efd 3f08 0000. We can read the first 16 bytes from this address to verify if it is indeed the address for the BDAT table.

```shell
$ /usr/local/iotools/mem_dump 0x0000083ffd5e0018 16 -b | xxd
00000000: 4244 4154 4845 4144 f620 0000 c651 0000  BDATHEAD. ...Q..
```

We see that the first 8 bytes correspond to the signature <em>BDATHEAD</em>. The next 4 bytes represent the <em>size</em> of the table.

```shell
$ echo $(( 16#000020f6 ))
8438
```

The <em>size</em> of this table is 8,438 bytes.

### Write BDAT data to a file

We need to write <em>size</em> number of bytes from the beginning of the table to a file. Due to alignment issues we round up the size to a multiple of 16 and read the data to a temporary file. From the temp file, we read the first <em>size</em> bytes into our final BDAT data file.

```shell
$ /usr/local/iotools/mem_dump 0x083ffd5e0018 8448 -b > bdat_data_tmp
$ head -c 8438 bdat_data_tmp > bdat_data
```

## Example Output
![Success](images/success_example)

The above is an example output for a well formatted BDAT table in accordance with the UEFI SPD Schema.

![Fail](images/fail_example)

The above is an example output for a BDAT table that does not contain the UEFI SPD Schema.

## Future Work

Add capability to parse more BDAT schemas as well as other ACPI tables.