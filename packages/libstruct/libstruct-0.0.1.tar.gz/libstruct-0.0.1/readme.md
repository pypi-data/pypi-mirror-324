# StructLib

`StructLib` is a Python class that offers a more human-friendly interface to the `struct` module,
allowing packing and unpacking of C-like struct data.  StructLib is a thin wrapper on top of
the `struct` module.  This module provides for human readable packet definitions using intuitive
strings rather than single character types that allow:

`little_endian ubyte byte uint16 int16 uint32 int32 uint64 int64`

instead of

`<BbHhIiQq`

Some useful binary viewing tools are also provided.

## Features

Packs and unpacks bytes by mapping human-readable format strings to equivalent `struct` format symbols.
Provides format symbols for a variety of data types, including integer types, floating-point types,
characters, strings, Pascal strings and padding.
Supports specification of endianness in format strings using terms like `little_endian` and `big_endian`.

## Basic Usage

```python 
from libstruct import LibStruct

# Initialize with a format string
sl = LibStruct("bool int32 str")
# Pack data into bytes
packed_data = sl.pack(True, 123, b"Hello")
# Unpack bytes into data
unpacked_data = sl.unpack(packed_data) 
```

## Format Strings

The format strings used to initialize `LibStruct` are made up of space-separated parts.
Each part represents a type to be packed/unpacked.
Supported types include:

| Description            | Available Types                                   |
| ---------------------- | ------------------------------------------------- |
| Integer Types          | `int8`, `uint8`, `int16`, `uint16`, `int32`, `uint32`, `int64`, `uint64` |
| Floating Point Types   | `float`, `double`                                 |
| Byte and Character     | `byte`, `ubyte`, `char`                           |
| Strings                | `str`, `string`                                   |
| Pascal Strings         | `p`, `pascal`                                     |
| Padding                | `pad`, `padding`                                  |
| Endianness             | `little_endian`, `big_endian`, `network`, `native`|



To repeat a type, use `*` operator followed by number, e.g. `10*int32` to specify that you want to
handle 10 integers.

Endianness can be specified at the beginning of the format string. Supported options are `little_endian`, `
big_endian`, `network`, and `native`.

## Support for hex output.

Since we often need to look at binary data a way to print data in hex I've provided a simple
library that converts binary data "packets" into a formatted hex output.  When displaying data as
bytes you can optionally show the data as text in a 'standard' hex dump.


### Examples:

Regular hex data as a list of 32 bit hex values.

```text
>>>bdata = list(range(0,256))
>>>ho = HexOut(columns=8,bytes_per_column=4,hex_format='0x{:08X}',addr_format='0x{:02X}: ',show_address=True)
>>>print(ho.as_hex(bdata))
0x00: 0x00010203 0x04050607 0x08090A0B 0x0C0D0E0F 0x10111213 0x14151617 0x18191A1B 0x1C1D1E1F
0x20: 0x20212223 0x24252627 0x28292A2B 0x2C2D2E2F 0x30313233 0x34353637 0x38393A3B 0x3C3D3E3F
0x40: 0x40414243 0x44454647 0x48494A4B 0x4C4D4E4F 0x50515253 0x54555657 0x58595A5B 0x5C5D5E5F
0x60: 0x60616263 0x64656667 0x68696A6B 0x6C6D6E6F 0x70717273 0x74757677 0x78797A7B 0x7C7D7E7F
0x80: 0x80818283 0x84858687 0x88898A8B 0x8C8D8E8F 0x90919293 0x94959697 0x98999A9B 0x9C9D9E9F
0xA0: 0xA0A1A2A3 0xA4A5A6A7 0xA8A9AAAB 0xACADAEAF 0xB0B1B2B3 0xB4B5B6B7 0xB8B9BABB 0xBCBDBEBF
0xC0: 0xC0C1C2C3 0xC4C5C6C7 0xC8C9CACB 0xCCCDCECF 0xD0D1D2D3 0xD4D5D6D7 0xD8D9DADB 0xDCDDDEDF
0xE0: 0xE0E1E2E3 0xE4E5E6E7 0xE8E9EAEB 0xECEDEEEF 0xF0F1F2F3 0xF4F5F6F7 0xF8F9FAFB 0xFCFDFEFF
```
or a list of 8bit hex values
```text
>>>bdata = list(range(0,256))
>>>print(HexOut(bytes_per_column=1, columns=16,hex_format='{:02X}').as_hex(bdata))
00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F
10 11 12 13 14 15 16 17 18 19 1A 1B 1C 1D 1E 1F
20 21 22 23 24 25 26 27 28 29 2A 2B 2C 2D 2E 2F
30 31 32 33 34 35 36 37 38 39 3A 3B 3C 3D 3E 3F
40 41 42 43 44 45 46 47 48 49 4A 4B 4C 4D 4E 4F
50 51 52 53 54 55 56 57 58 59 5A 5B 5C 5D 5E 5F
60 61 62 63 64 65 66 67 68 69 6A 6B 6C 6D 6E 6F
70 71 72 73 74 75 76 77 78 79 7A 7B 7C 7D 7E 7F
80 81 82 83 84 85 86 87 88 89 8A 8B 8C 8D 8E 8F
90 91 92 93 94 95 96 97 98 99 9A 9B 9C 9D 9E 9F
A0 A1 A2 A3 A4 A5 A6 A7 A8 A9 AA AB AC AD AE AF
B0 B1 B2 B3 B4 B5 B6 B7 B8 B9 BA BB BC BD BE BF
C0 C1 C2 C3 C4 C5 C6 C7 C8 C9 CA CB CC CD CE CF
D0 D1 D2 D3 D4 D5 D6 D7 D8 D9 DA DB DC DD DE DF
E0 E1 E2 E3 E4 E5 E6 E7 E8 E9 EA EB EC ED EE EF
F0 F1 F2 F3 F4 F5 F6 F7 F8 F9 FA FB FC FD FE FF
```
or

```text
>>>bdata = list(range(0,32))
>>>print(HexOut(bytes_per_column=4, columns=4,hex_format='{:08X}').as_hex(bdata))
00010203 04050607 08090A0B 0C0D0E0F
10111213 14151617 18191A1B 1C1D1E1F
```

or even:

```text
>>>print(HexOut(show_ascii=True,columns=32).as_hex(range(0,256)))
00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F 10 11 12 13 14 15 16 17 18 19 1A 1B 1C 1D 1E 1F ................................
20 21 22 23 24 25 26 27 28 29 2A 2B 2C 2D 2E 2F 30 31 32 33 34 35 36 37 38 39 3A 3B 3C 3D 3E 3F  !"#$%&'()*+,-./0123456789:;<=>?
40 41 42 43 44 45 46 47 48 49 4A 4B 4C 4D 4E 4F 50 51 52 53 54 55 56 57 58 59 5A 5B 5C 5D 5E 5F @ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_
60 61 62 63 64 65 66 67 68 69 6A 6B 6C 6D 6E 6F 70 71 72 73 74 75 76 77 78 79 7A 7B 7C 7D 7E 7F `abcdefghijklmnopqrstuvwxyz{|}~.
80 81 82 83 84 85 86 87 88 89 8A 8B 8C 8D 8E 8F 90 91 92 93 94 95 96 97 98 99 9A 9B 9C 9D 9E 9F ................................
A0 A1 A2 A3 A4 A5 A6 A7 A8 A9 AA AB AC AD AE AF B0 B1 B2 B3 B4 B5 B6 B7 B8 B9 BA BB BC BD BE BF ................................
C0 C1 C2 C3 C4 C5 C6 C7 C8 C9 CA CB CC CD CE CF D0 D1 D2 D3 D4 D5 D6 D7 D8 D9 DA DB DC DD DE DF ................................
E0 E1 E2 E3 E4 E5 E6 E7 E8 E9 EA EB EC ED EE EF F0 F1 F2 F3 F4 F5 F6 F7 F8 F9 FA FB FC FD FE FF ................................
```

If data is provided that is out of range for bytes (0-255) a `ValueError` exception is thrown.

## Note

This class raises exceptions consistent with Python's `struct` module. So, when you are using `StructLib`,
you might need to handle the same exceptions that you would when using `struct`.
Keep in mind that `str`/`string` type in `StructLib` corresponds to the `struct` `s` format
(fixed-size string), and `p`/`pascal` corresponds to the `struct` `p` format (Pascal string). For the
difference between `s` and `p` in `struct`, you might need to refer to Python's `struct` module documentation.
Please note that this class provides a simple and limited interface to Python's `struct` module. For complex
struct packing/unpacking needs, it is recommended to directly use the `struct` module.



