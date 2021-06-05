#! /usr/bin/env python3

import argparse

from huffman_coding.cpsn import HuffmanCoding


def main():
    parser = argparse.ArgumentParser("Huffman Coding")
    parser.add_argument(
        "file",
        metavar="file",
        type=str,
        help="file to compress or decompress",
    )
    parser.add_argument(
        "-d",
        "--decompress",
        action="store_true",
        help="decompress file",
    )
    parser.add_argument(
        "-o", "--output", help="filename for output - defaults to adding/removing .pine"
    )
    args = parser.parse_args()

    H = HuffmanCoding()

    if args.decompress:
        if args.output:
            out_file = args.output
        else:
            out_file = args.file.replace(".pine", "")
        decoded = H.decode(in_file, out_file=out_file)
    else:
        if args.output:
            out_file = args.output
        else:
            out_file = args.file + ".pine"
        H.encode(in_file, out_file=out_file)
