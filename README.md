# SMBIOS Validation Tool

## What is it?

SMBIOS Validation Tool is an open source tool that will validate SMBIOS records
in vendor's firmware (BIOS) conformance to the SMBIOS requirements to Google
Server Firmware Specification.

Note: This is not an officially supported Google product.

## Terminology

*   **SMBIOS** - System Management BIOS. The SMBIOS Specification addresses how
    motherboard and system vendors present management information about their
    products in a standard format by extending the BIOS interface on x86
    architecture systems. The information is intended to allow generic
    instrumentation to deliver this information to management applications that
    use DMI, CIM or direct access, eliminating the need for error prone
    operations like probing system hardware for presence detection.

*   **SMBIOS Record** - One specific SMBIOS Structure. Each record has a type, a
    unique handle id, and required fields with corresponding info. See below
    graph for more intuitive understanding.

![SMBIOS Table](https://docs.google.com/drawings/d/e/2PACX-1vSa-CpaATNXhP-FZg9gV1dVQ_C8eRHE4TJRRB4lEQwCEXulKPcdeUOZn8obdWuwEKg2pLHr-8SKBFgZ/pub?w=562&h=434)

## Quick start

### Prepare the Environment

#### Install dmidecode

*   Make sure dmidecode is installed, or dmidecode binary is in the same folder
    when executing the tool.

#### Install termcolor

```shell
pip install termcolor
```

### Execute the Tool

Copy the binary to the machine. Then execute it simply as other executable
files:

```shell
./smbios_validation.par
```

The tool can also analyze a dmi dump file, although this is a rare use case:

```shell
./smbios_validation.par --file=path_to_your_dump_file.txt
```

## Output

The tool is designed to provide the error and suggested action messages as
clearly as possible, to help users correct errors in SMBIOS much easier.

Whenever the tool finds a rule is not valid on the host, an error message in a
fixed format will be printed out, followed by the suggested action. The tool
uses termcolor to highlight the output to make it more readable. Please install
termcolor as stated in 'Quick Start' section.

### Error Messages

Error message will have fixed format for individual records, and is displayed as
red color:

```
ERROR: Invalid <field_name> field in Type <type_id> (<type_name>) record.
Handle ID: <handle_id>
```

Error messages for validating groups of records do not have a fixed format, but
will also contain all necessary information for debugging.

### Action Messages

Action messages will provide users with the suggestion of how to fix the error.
Action messages will also have fixed format for individual records, and are
displayed right below the corresponding error messages as orange color and with
underline:

```
ACTION: Please populate <field_name> field with valid string/number/handle/etc.
<Optional extra messages>
```

Again, action messages for validating groups of records do not have a fixed
format. Our goal is to provide useful information for users to correct the
error, so usually the action message will clearly state what the rule is and/or
which part of the rule is not valid.
