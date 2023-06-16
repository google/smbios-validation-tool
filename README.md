## How to build

Access to the root directory of the tool and run the following command.
```
go build -o smbios_validator
```

## How to run

```
./smbios_validator --table=path/dmidecode.dat --rule=./rules/textproto/less.textproto
```

- --table: Specifies the path to a dmidecode dump file.
- --rule: Specifies the path to the rule that applies. The rule file should be located in the `rules/prototext` folder.

Make sure to provide the correct paths for both --table and --rule options when running the tool.