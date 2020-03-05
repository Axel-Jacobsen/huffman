# Huffman Coding

Implementation of [Huffman Coding](https://en.wikipedia.org/wiki/Huffman_coding).

The first 100M of English Wikipedia:

```txt
Uncompressed File Size (enwik8): 100M
Compressed File Size (enwik8.pine): 61M
Zip Compressed File Size (enwik8.zip): 33M
```

Zip is (of course) better than my code, both for speed of compression/decompression and for compression ratio. The compression ratio for zip is `100/33 = 3.03`, where the compression ratio for pine  is `100/61 = 1.64`.
Tested on the lyrics of [Murder of the Universe](https://www.youtube.com/watch?v=4zUPTPlkqDg) by King Gizzard and the Wizard Lizard.

```txt
Uncompressed File Size (murderoftheuniverse.txt): 2.5K
Compressed File Size (murderoftheuniverse.txt.pine): 1.8K
Compression Ratio: (uncompresed size) / (compressed size) = 1.39
```

i.e. compressed file is 72 % of the size of the uncompressed file. The compression ratio would depend on the number of unique characters in the uncompressed file; the fewer characters, the higher the compression ratio.


The time to compress and decompress are both much too long (on my 2015 Macbook Pro, ~60s to compress enwik8, ~600s to decompress!). Look for optimizations in the decompress method first.

## Improvements

- The write table is not being compressed as much as it should be. It is currently saving the zeros and ones in the write table as their utf-8 codes (e.g. 0x30, 0x31) instead of as bytes of zeros and ones.
- Decompression is much slower than compression; most likely because we have to go through the compressed file bit by bit to find characters in the tree. Must think of ways to get around this.

