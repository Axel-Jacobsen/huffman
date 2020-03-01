#! /usr/bin/env python3

from cpsn import HuffmanCoding
from node import Node


def _get_twos_below(num):
    if num == 0 or num == 1:
        return [1]
    twos = []
    j = 0
    while 2 ** j <= num:
        twos.append(2 ** j)
        j += 1
    return twos


def _get_twos_sum(num):
    twos = _get_twos_below(num)
    twos_sum = []
    csum = 0
    for v in twos:
        csum += v
        twos_sum.append(csum - 1)
    return twos_sum


def _get_num_level_offset(num):
    ts = _get_twos_sum(num)
    return min(
        filter(lambda v: v >= 0, [num - v for v in ts])
    )


def _get_tree_level(val):
    twos_sum = _get_twos_sum(val + 2)
    i = 0
    while val >= twos_sum[i]:
        i += 1
    return i


def code_to_val(code):
    bval = int(code, 2)
    preset = sum([2 ** i for i in range(len(code))])
    return bval + preset - 1


def val_to_code(val):
    level = _get_tree_level(val)
    code_bin_val = '{0:b}'.format(_get_num_level_offset(val))
    return '0' * (level - len(code_bin_val)) + code_bin_val


def write_tree(write_table, fname='.pine'):
    with open(fname, 'wb') as f:
        for char, code in write_table.items():
            f.write(bytes(code, 'utf-8'))
            f.write(bytes(char, 'utf-8'))
            f.write(bytes([0xff]))


def _build_write_table_from_file(fname):
    write_table = {}
    with open(fname, 'rb') as f:
        write_arr = f.read().split(bytes([0xff]))[:-1]
        for v in write_arr:
            code_char_str = v.decode('utf-8')
            write_table[code_char_str[-1]] = code_char_str[:-1]
    return write_table


def read_tree(fname):
    write_table = _build_write_table_from_file(fname)
    T = Node()
    for char, code in write_table.items():
        add_char_code(T, char, code)
    return T


def add_char_code(tree, char, code):
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
            raise AssertionError(f'invalid position code in .pine file: {code}, {v}')

    if code[-1] == '0':
        cnode.l_child = char
    else:
        cnode.r_child = char


if __name__ == '__main__':
    hc = HuffmanCoding()
    T = hc.encode('murderoftheuniverse.txt')

    write_tree(hc.write_table)
    read_tree('.pine')
