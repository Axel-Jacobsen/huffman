#! /usr/bin/env python3

from __future__ import annotations

import sys
import time

from collections import Counter
from typing import List, Tuple, Dict, Any, TextIO, Union, Optional

import huffman_coding.pine as pine
from huffman_coding.node import Node


class HuffmanCoding(object):

    HuffmanTree = dict

    def __init__(self):
        self.write_table = {}

    @staticmethod
    def _create_char_freqs(f: TextIO) -> List[Tuple[str, int]]:
        """Returns list of tuples from "char" to it's count"""
        D: Counter = Counter()
        for chunk in pine.read_in_chunks(f):
            D += Counter(chunk)
        return list(D.items())

    @staticmethod
    def _gen_huffman_tree(char_freqs: List[Tuple[Union[str, Node], int]]) -> Node:
        """
        Create the Huffman Tree which will be used for compression

        this could be done better (we are mixing a list of tuples of types (str, int) and (node, int))
        """
        while len(char_freqs) > 1:
            char_freqs.sort(key=lambda v: v[1], reverse=True)
            *char_freqs, bot1, bot2 = char_freqs
            branch = Node(bot1[0], bot2[0])
            char_freqs.append((branch, bot1[1] + bot2[1]))
        peak_node, _ = char_freqs[0]
        assert isinstance(peak_node, Node)
        return peak_node

    def gen_write_table(self, node: Node, b: str = ""):
        """
        Generate write table (which maps the character to its code
        in the Huffman Tree)
        """
        try:
            self.gen_write_table(node.l_child, b + "0")
        except AttributeError:
            self.write_table[node.l_child] = b + "0"
        try:
            self.gen_write_table(node.r_child, b + "1")
        except AttributeError:
            self.write_table[node.r_child] = b + "1"

    def write_to_file(self, write_table, encoded_data: str, fname: str):
        """
        this function does the grunt work of getting the
        write table and encoded data ready and writing it
        to a file
        """
        pine_bytes = pine.bytes_from_write_table(write_table)
        len_pine_bytes = len(pine_bytes).to_bytes(pine.TREE_MAGNITUDE, "big")
        padding = pine.get_padding_size(len(encoded_data))
        padding_byte = padding.to_bytes(1, "big")
        data_as_str = "0" * padding + encoded_data
        assert len(data_as_str) % 8 == 0

        # since file_bytes
        data_as_bytes = int(data_as_str, 2).to_bytes(len(data_as_str) // 8, "big")

        contents = len_pine_bytes + padding_byte + pine_bytes + data_as_bytes

        with open(fname + ".pine", "wb") as g:
            g.write(contents)

    def encode(self, fname: str, out_file: str = None):
        read_file = open(fname, "r")
        char_freqs = HuffmanCoding._create_char_freqs(read_file)
        T = HuffmanCoding._gen_huffman_tree(char_freqs)
        self.gen_write_table(T)

        encoded_data = ""
        read_file.seek(0)
        for chunk in pine.read_in_chunks(read_file):
            for char in chunk:
                encoded_data += self.write_table[char]

        read_file.close()
        self.write_to_file(self.write_table, encoded_data, fname)

    def decode(self, encoded_fname: str, out_file: str = None) -> str:
        """
        Decode the .pine file given by its filename
        """
        s = ""
        write_table_bytes, encoded_data, padding = pine.get_file_chunks(encoded_fname)
        cn = mn = pine.tree_from_bytes(write_table_bytes)
        for byte in encoded_data:
            for b in pine.byte_to_bits(byte, padding):
                if b == "0":
                    cn = cn.l_child
                elif b == "1":
                    cn = cn.r_child
                if isinstance(cn, str):
                    s += cn
                    cn = mn
            padding = 0

        if out_file is not None:
            with open(out_file, "w") as f:
                f.write(s)

        return s


if __name__ == "__main__":
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    else:
        print("Usage: cpsn.py <filename>")
        exit()

    hc = HuffmanCoding()

    # the actual compression
    print(f"compressing {filename}")
    t1 = time.perf_counter()
    hc.encode(filename)
    t2 = time.perf_counter()
    print("Num chars", len(hc.write_table.keys()))

    print(f"time to compress: {t2 - t1:.4f}\n")

    # decompression
    print("decompressing file")
    reconstructed = hc.decode(filename + ".pine")
    original = open(filename, "r").read()
    print(f"time to decompress: {time.perf_counter() - t2:.4f}\n")

    assert reconstructed == original, ""
    print("reconstructed equal to orinal")
