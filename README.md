# Huffman Coding

Implementation of [Huffman Coding](https://en.wikipedia.org/wiki/Huffman_coding).

Tested on the lyrics of [Murder of the Universe](https://www.youtube.com/watch?v=4zUPTPlkqDg) by King Gizzard and the Wizard Lizard.

```txt
Uncompressed File Size (murderoftheuniverse.txt): 2.5K
Compressed File Size (murderoftheuniverse.txt.pine): 1.8K
Compression Ratio: (uncompresed size) / (compressed size) = 1.39
```

i.e. compressed file is 72% of the size of the uncompressed file. The compression ratio would depend on the number of unique characters in the uncompressed file; the fewer characters, the higher the compression ratio.

Note: this only works on ASCII files - i.e., each character is 1 byte. Also, the time to compress and decompress are both much too long (on my 2015 Macbook Pro, ~60s to compress enwik8, ~600s to decompress!). Look for optimizations in the decompress method first.

## .pine file description

.pine File Description

This file provides the framework to write and read to .pine
files. Using notation `<number of bytes:name of block>`, the
.pine file consists of the following structure:

```
<TREE_MAGNITUDE:write_table_size>
<1:prepadding_size>
<write_table_size:write_table>
<prepadding_size:padding>
<r:encoded_data>
```

where `r` denotes the 'rest' of the file

## Improvements

- The write table is not being compressed as much as it should be. It is currently saving the zeros and ones in the write table as their utf-8 codes (e.g. 0x30, 0x31) instead of as bytes of zeros and ones.
- Decompression is much slower than compression; most likely because we have to go through the compressed file bit by bit to find characters in the tree. Must think of ways to get around this.
- Read in the file in chunks, for when there are large files

