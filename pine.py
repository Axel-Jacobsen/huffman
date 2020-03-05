#! /usr/bin/env python3

from node import Node


""" .pine File Description

This file provides the framework to write and read to .pine
files. Using notation <number of bytes:name of block>, the
.pine file consists of the following structure:

    <2:write_table_size>
    <1:prepadding_size>
    <write_table_size:write_table>
    <prepadding_size:padding>
    <r:encoded_data>

where `r` denotes the 'rest' of the file
"""

TREE_MAGNITUDE = 2


def get_file_chunks(fname: str, tree_magnitude=TREE_MAGNITUDE):
    """
    following the file description above, this function pulls
    chunks of bytes from `fname` and returns them
    """
    f = open(fname, 'rb')
    tree_size = int.from_bytes(f.read(tree_magnitude), 'big')
    padding = int.from_bytes(f.read(1), 'big')
    tree = f.read(tree_size)
    rest = f.read()
    f.close()

    return tree, rest, padding


def tree_from_bytes(write_table_bytes):
    """
    decode a chunk of bytes, encoded as a write table,
    to a tree representing the same
    """
    write_table = write_table_from_bytes(write_table_bytes)
    T = Node()
    for char, code in write_table.items():
        print(char, code)
        _add_char_code(T, char, code)
    return T


def bytes_from_write_table(write_table):
    """
    encode the write table in a chunk of bytes,
    for eventual writing in a .pine file
    """
    byte_arr = bytes()
    for char, code in write_table.items():
        code_padding_len = get_padding_size(len(code))
        code = '0' * code_padding_len + code 
        byte_arr += code_padding_len.to_bytes(1, 'big')
        byte_arr += int(code, 2).to_bytes(len(code) // 8, 'big')
        byte_arr += bytes(char, 'utf-8')
        byte_arr += bytes([0xff])
    return byte_arr


def write_table_from_bytes(write_table_bytes):
    """
    build and return the write table from a chunk of bytes
    representing a write table - e.g. this function is
    the inverse of bytes_from_write_table
    """
    write_table = {}
    write_arr = write_table_bytes.split(bytes([0xff]))[:-1]
    for v in write_arr:
        padding = v[0]
        code = int.from_bytes(v[1:-1], 'big')
        code = byte_to_str(code, padding)
        char = chr(v[-1])
        write_table[char] = code
    return write_table

def _add_char_code(tree, char, code):
    """
    write `char` into `tree` in the position that `code` gives
    creates nodes in the tree if they dont exist yet
    """
    # Find the parent that will hold `char`
    cnode = tree
    for v in code[:-1]:
        if v == '0':
            if cnode.l_child is None:
                cnode.l_child = Node()
                cnode = cnode.l_child
            else:
                cnode = cnode.l_child
        elif v == '1':
            if cnode.r_child is None:
                cnode.r_child = Node()
                cnode = cnode.r_child
            else:
                cnode = cnode.r_child
        else:
            raise AssertionError(f'invalid code in .pine file: {code}, {v}')

    # set the parent's child with `char` as desired
    if code[-1] == '0':
        cnode.l_child = char
    else:
        cnode.r_child = char


def get_padding_size(bits_str_len):
    """
    return the size of padding required so the length of `bits_str`
    is divisible by 8 - i.e. bits_str represents individual bits,
    which we want to convert to bytes (which we can't do if bits_str % 8 != 0)
    """
    return 8 * (bits_str_len // 8 + 1) - bits_str_len


def byte_to_bits(byte, discard=0):
    """
    yield bit by bit from byte, ignoring the first `discard` bits
    `discard` is used to ignore the zero padding before the encoded file
    """
    for i in range(discard, 8):
        yield str((byte >> (7 - i)) & 1)

def byte_to_str(byte, discard=0):
    """
    turns byte into a string of bits
    byte_to_str(0xff) == '11111111'
    byte_to_str(0x09) == '00001001'
    """
    s = ''
    for b in byte_to_bits(byte, discard):
        s += b
    return s

