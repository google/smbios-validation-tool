// Package dmiparser parses Desktop Management Interface (DMI) SMBIOS records.
//
// An example SMBIOS record output from the dmidecode type 0 structure:
//
// Handle 0x0000, DMI type 0, 24 bytes
// BIOS Information
//
//	Vendor: Hewlett-Packard
//	Version: M60 v02.50
//	Release Date: 11/07/2019
//	Address: 0xF0000
//	Runtime Size: 64 kB
//	ROM Size: 16 MB
//	Characteristics:
//		PCI is supported
//		PNP is supported
//		BIOS is upgradeable
//		BIOS shadowing is allowed
//		Boot from CD is supported
//		Selectable boot is supported
//		EDD is supported
//		Print screen service is supported (int 5h)
//		8042 keyboard services are supported (int 9h)
//		Serial services are supported (int 14h)
//		Printer services are supported (int 17h)
//		ACPI is supported
//		USB legacy is supported
//		BIOS boot specification is supported
//		Function key-initiated network boot is supported
//		Targeted content distribution is supported
//		UEFI is supported
//	BIOS Revision: 2.50
package dmiparser

import (
	"bufio"
	"errors"
	"os"
	"regexp"
	"strings"
)

// Record defines the structure of a table record.
type Record struct {
	Handle string
	Type   string
	Props  map[string]Field
}

// Field is the field-Prop struct of a table.
type Field struct {
	Val  string
	Item []string
}

func newRecord(line string) Record {
	record := Record{}
	pattern := regexp.MustCompile(`Handle (0x[0-9A-F]+), DMI type ([0-9]+).*`)
	match := pattern.FindStringSubmatch(line)
	record.Handle = match[1]
	record.Type = match[2]
	record.Props = map[string]Field{}
	return record
}

func parseRecord(lines []string, record *Record) error {
	field, val, item := "", "", []string{}
	for _, line := range lines {
		switch indentLevel(line) {
		case 1:
			fieldValue := strings.SplitN(line, ":", 2)
			field = strings.TrimSpace(fieldValue[0])
			val = strings.TrimSpace(fieldValue[1])
			item = []string{}
			record.Props[field] = Field{
				Val:  val,
				Item: item,
			}
		case 2:
			line = strings.TrimLeft(line, " \t")
			item = append(item, line)
			// Override the existing prop.
			record.Props[field] = Field{
				Val:  val,
				Item: item,
			}
		default:
			return errors.New("Fail to parse " + line)
		}
	}
	return nil
}

// Parse handles the dmidecode dump file can converts it to a map.
func Parse(filePath string) ([]string, map[string]Record, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return nil, nil, err
	}
	scanner := bufio.NewScanner(file)

	// For keeping the records in order when iterate.
	handles := []string{}
	records := make(map[string]Record)

	var record Record
	// field, val, item := "", "", []string{}
	unparsedLines := []string{}
	for scanner.Scan() {
		line := scanner.Text()
		if strings.HasPrefix(line, "Handle") {
			record = newRecord(line)
		} else if indentLevel(line) != 0 {
			unparsedLines = append(unparsedLines, line)
		} else if line == "" {
			parseRecord(unparsedLines, &record)
			handles = append(handles, record.Handle)
			records[record.Handle] = record
			unparsedLines = []string{}
		}
	}
	// Check for any errors while reading the file
	if err := scanner.Err(); err != nil {
		return nil, nil, err
	}

	// Close the file when done
	file.Close()

	return handles, records, nil
}

func indentLevel(line string) int {
	return (len(line) - len(strings.TrimLeft(line, " \t")))
}
