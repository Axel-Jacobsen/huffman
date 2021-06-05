#! /usr/bin/env python3

from huffman_coding.node import Node

from typing import Generator, Tuple, TextIO, Dict


""" .pine File Description

This file provides the framework to write and read to .pine
files. Using notation <number of bytes:name of block>, the
.pine file consists of the following structure:

    <TREE_MAGNITUDE:write_table_size>
    <1:prepadding_size>
    <write_table_size:write_table>
    <prepadding_size:padding>
    <r:encoded_data>

where `r` denotes the 'rest' of the file
"""

TREE_MAGNITUDE = 2


def read_in_chunks(f: TextIO, chunk_size=1024) -> Generator[str, None, None]:
    while True:
        data = f.read(chunk_size)
        if not data:
            break
        yield data


def get_file_chunks(
    fname: str, tree_magnitude: int = TREE_MAGNITUDE
) -> Tuple[bytes, bytes, int]:
    """
    following the file description above, this function pulls
    chunks of bytes from `fname` and returns them
    """
    f = open(fname, "rb")
    tree_size = int.from_bytes(f.read(tree_magnitude), "big")
    padding = int.from_bytes(f.read(1), "big")
    tree = f.read(tree_size)
    rest = f.read()
    f.close()

    return tree, rest, padding


def tree_from_bytes(write_table_bytes: bytes) -> Node:
    """
    decode a chunk of bytes, encoded as a write table,
    to a tree representing the same
    """
    write_table = write_table_from_bytes(write_table_bytes)
    T = Node()
    for char, code in write_table.items():
        _add_char_code(T, char, code)
    return T


def bytes_from_write_table(write_table: dict) -> bytes:
    """
    encode the write table in a chunk of bytes,
    for eventual writing in a .pine file
    """
    byte_arr = bytes()
    for char, code in write_table.items():
        code_padding_len = get_padding_size(len(code))
        code = "0" * code_padding_len + code
        byte_arr += code_padding_len.to_bytes(1, "big")
        byte_arr += int(code, 2).to_bytes(len(code) // 8, "big")
        byte_arr += bytes(char, "utf-8")
        byte_arr += bytes([0xFF])
    return byte_arr


def write_table_from_bytes(write_table_bytes: bytes) -> Dict[str, str]:
    """
    build and return the write table from a chunk of bytes
    representing a write table - e.g. this function is
    the inverse of bytes_from_write_table
    """
    write_table = {}
    write_arr = write_table_bytes.split(bytes([0xFF]))[:-1]
    for v in write_arr:
        padding = v[0]  # byte 0 is padding size
        code = bytes_to_str(v[1:-1], padding)  # middle bytes is the code
        char = chr(v[-1])  # last byte is the char
        write_table[char] = code
    return write_table


def _add_char_code(tree: Node, char: str, code: str):
    """
    write `char` into `tree` in the position that `code` gives
    creates nodes in the tree if they dont exist yet
    """
    # Find the parent that will hold `char`
    cnode = tree
    traverse_path, insert_position = code[:-1], code[-1]

    for v in traverse_path:
        if v == "0":
            if cnode.l_child is None:
                cnode.l_child = Node()
                cnode = cnode.l_child
            else:
                cnode = cnode.l_child
        elif v == "1":
            if cnode.r_child is None:
                cnode.r_child = Node()
                cnode = cnode.r_child
            else:
                cnode = cnode.r_child

    # set the parent's child with `char` as desired
    if insert_position == "0":
        cnode.l_child = char
    else:
        cnode.r_child = char


def get_padding_size(bits_str_len: int):
    """
    return the size of padding required so the length of `bits_str`
    is divisible by 8 - i.e. bits_str represents individual bits,
    which we want to convert to bytes (which we can't do if bits_str % 8 != 0)
    """
    return (8 - bits_str_len % 8) % 8


def byte_to_bits(byte: int, discard: int = 0) -> Generator[str, None, None]:
    """
    yield bit by bit from byte, ignoring the first `discard` bits
    `discard` is used to ignore the zero padding before the encoded file
    """
    for i in range(discard, 8):
        yield str((byte >> (7 - i)) & 1)


def bytes_to_str(code_bytes: bytes, discard: int = 0) -> str:
    """
    turns byte into a string of bits
    byte_to_str(0xff) == '11111111'
    byte_to_str(0x09) == '00001001'
    """
    s = ""
    for byte in code_bytes:
        for b in byte_to_bits(byte, discard):
            s += b
            discard = 0
    return s
