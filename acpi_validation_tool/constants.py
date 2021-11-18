"""
#pragma pack(1)
typedef struct {
 UINT8 BiosDataSignature[8]; // "BDATHEAD"
 UINT32 BiosDataStructSize; // sizeof BDAT_STRUCTURE
 UINT16 Crc16; // 16-bit CRC of BDAT_STRUCTURE
 UINT16 Reserved
 UINT16 PrimaryVersion;
 UINT16 SecondaryVersion;
 UINT32 OemOffset;
 UINT32 Reserved1;
 UINT32 Reserved2;
} BDAT_HEADER_STRUCTURE;
#pragma pack()

#pragma pack(push, 1)
typedef struct BdatSchemaList {
 UINT16 SchemaListLength;
 UINT16 Reserved;
 UINT16 Year;
 UINT8 Month;
 UINT8 Day;
 UINT8 Hour;
 UINT8 Minute;
 UINT8 Second;
 UINT8 Reserved;
 UINT32 Schemas[SchemaListLength];
} BDAT_SCHEMA_LIST_STRUCTURE;

typedef struct BdatStruct {
 BDAT_HEADER_STRUCTURE BdatHeader;
 BDAT_SCHEMA_LIST_STRUCTURE BdatSchemas;
} BDAT_STRUCTURE;
#pragma pack(pop)
"""

BDAT_STRUCTURE_SIZE = 44            # This does not include the size of UINT32 Schemas[SchemaListLength];
                                    # SchemaListLength will only be known at runtime.

"""
#pragma pack(push, 1)
typedef struct BdatSchemaHeader {
 EFI_GUID SchemaId;
 UINT32 DataSize;
 UINT16 Crc16;
} BDAT_SCHEMA_HEADER_STRUCTURE;
#pragma pack(pop)

#pragma pack(push, 1)
typedef struct {
 EFI_GUID MemSpdGuid;
 UINT32 Size;
 UINT32 Crc;
 UINT32 Reserved;
} MEM_SPD_RAW_DATA_HEADER;

typedef struct {
 MEM_SPD_RAW_DATA_HEADER Header;

 //
 // This is a dynamic region, where SPD data entries are filled out.
 //
} MEM_SPD_DATA_STRUCTURE

typedef struct {
 BDAT_SCHEMA_HEADER_STRUCTURE SchemaHeader;
 MEM_SPD_DATA_STRUCTURE SpdData;
} BDAT_MEM_SPD_STRUCTURE;

#pragma pack(pop)
"""
# UEFI SPD Schema GUID. EFI_GUID: 1B19F809-1D91-4F00-A3F3-7A676606D3B1
UEFI_SPD_SCHEMA_GUID = "09f8191b-911d-004f-a3f3-7a676606d3b1"
# Memory SPD data identification GUID. EFI_GUID: 46F60B90-9C94-43CA-A77C-09B848999348
MEM_SPD_DATA_ID_GUID = "900bf646-949c-ca43-a77c-09b848999348"
BDAT_MEM_SPD_STRUCTURE_SIZE = 50    # This does not include the dynamic region where the SPD data entries are filled out.

"""
#pragma pack(push, 1)
typedef enum {
 MemSpdDataType0 = 0,
 MemTrainDataTypeMax,
 MemTrainDataTypeDelim = MAX_INT32
} MEM_SPD_DATA_TYPE;

typedef struct {
 MEM_SPD_DATA_TYPE Type;
 UINT16 Size; /// Entries will be packed by byte in contiguous
space. Size of the entry includes the header.
} MEM_SPD_DATA_ENTRY_HEADER;

typedef struct {
 UINT8 Socket;
 UINT8 Channel;
 UINT8 Dimm;
} MEM_SPD_DATA_ENTRY_MEMORY_LOCATION;

typedef struct {
 MEM_SPD_DATA_ENTRY_HEADER Header;
 MEM_SPD_DATA_ENTRY_MEMORY_LOCATION MemmoryLocation;
 UINT16 NumberOfBytes;
 //
 // This is a dynamic region, where SPD data are filled out.
 // The total number of bytes of the SPD data must match NumberOfBytes
 //
} MEM_SPD_ENTRY_TYPE0;
#pragma pack(pop)
"""


MEM_SPD_ENTRY_TYPE0_SIZE = 11       # This is the size of the header fields for each SPD entry
                                    # not including the dynamic region with individual SPD data.

SPD_DDR4_SIZE = 512