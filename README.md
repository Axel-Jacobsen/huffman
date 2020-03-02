# Huffman Coding

Implementation of [Huffman Coding](https://en.wikipedia.org/wiki/Huffman_coding). 

Tested on the lyrics of [Murder of the Universe](https://www.youtube.com/watch?v=4zUPTPlkqDg) by King Gizzard and the Wizard Lizard.

```txt
Uncompressed File Size (murderoftheuniverse.txt): 2.5K
Compressed File Size (murderoftheuniverse.txt.pine): 1.8K
Compression Ratio: (uncompresed size) / (compressed size) = 1.39
```

i.e. compressed file is 72 % of the size of the uncompressed file. The compression ratio would depend on the number of unique characters in the uncompressed file; the fewer characters, the higher the compression ratio.

A better standard for performance would be the `enwik8` dataset, the first 100M of English Wikipedia:

```txt
Uncompressed File Size (enwik8): 100M
Compressed File Size (enwik8.pine): 61M
Zip Compressed File Size (enwik8.zip): 33M
```

Zip is (of course) better than this solution, both for speed of compression/decompression and for compression ratio. The compression ratio for zip is `100/33 = 3.03`, where the compression ratio for pine  is `100/61 = 1.64`.
