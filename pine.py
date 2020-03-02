#! /usr/bin/env python3

from node import Node


def tree_as_bytes(write_table):
    byte_arr = bytes()
    for char, code in write_table.items():
        byte_arr += bytes(code, 'utf-8')
        byte_arr += bytes(char, 'utf-8')
        byte_arr += bytes([0xff])
    return byte_arr


def _build_write_table_from_bytes(write_table_bytes):
    write_table = {}
    write_arr = write_table_bytes.split(bytes([0xff]))[:-1]
    for v in write_arr:
        code_char_str = v.decode('utf-8')
        write_table[code_char_str[-1]] = code_char_str[:-1]
    return write_table


def bytes_as_tree(write_table_bytes):
    write_table = _build_write_table_from_bytes(write_table_bytes)
    T = Node()
    for char, code in write_table.items():
        _add_char_code(T, char, code)
    return T


def _add_char_code(tree, char, code):
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

    if code[-1] == '0':
        cnode.l_child = char
    else:
        cnode.r_child = char

