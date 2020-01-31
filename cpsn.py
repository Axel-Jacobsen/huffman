#! /usr/bin/env python3

# 36548940  gzipped enwik8
# 100000000         enwik8

import struct
from collections import defaultdict


class Node(object):

    def __init__(self, l=None, r=None):
        self.l = l
        self.r = r

    def print_leaves(self):
        try:
            print(self.l.print_leaves())
        except AttributeError:
            print(self.l)
        try:
            print(self.r.print_leaves())
        except AttributeError:
            print(self.r)


def create_char_freqs(bts):
    D = defaultdict(int)
    for byte in bts:
        D[byte] += 1
    return sorted(D.items(), key=lambda v: v[1], reverse=True)

def gen_huffman(char_freqs):
    while len(char_freqs) > 1:
        last_2 = char_freqs[-2:]
        del char_freqs[-2:]

        branch = Node(last_2[0][0], last_2[1][0])
        freq_sum = last_2[0][1] + last_2[1][1] 
        char_freqs.append((branch, freq_sum))
        char_freqs.sort(key=lambda v: v[1], reverse=True)
    return char_freqs[0][0]

def gen_write_table(huffman_tree, write_table, b=''):
    try:
        gen_write_table(huffman_tree.l, write_table, b + '0')
    except AttributeError:
        write_table[huffman_tree.l] = b + '0'
    try:
        gen_write_table(huffman_tree.r, write_table, b + '1')
    except AttributeError:
        write_table[huffman_tree.r] = b + '1'

def encode(f):
    print('Getting Char Frequency')
    char_freqs = create_char_freqs(f)
    print('Generating Huffman tree')
    T = gen_huffman(char_freqs)
    wt = {}
    print('Generating Writing Table')
    gen_write_table(T, wt)
    print(f'Number of chars: {len(wt)}')

    print('Writing byte file')
    total_bits = ''
    print(wt)
    for char in f:
        total_bits += wt[char]
    
    # pad the last digits to make bytes out of bits
    l = len(total_bits)
    total_bits += '0' * (8 * (l // 8 + 1) - l)

    with open('out', 'wb') as g:
        bb = int(total_bits, 2).to_bytes(len(total_bits) // 8, 'big')
        g.write(bb)
    return T

def hex_to_bin(byte):
    # return '{0:b}'.format(ord(byte))
    for i in range(8):
        yield str((int.from_bytes(byte, 'big') >> (7 - i)) & 1)

def decode(bs, N):
    cn = N
    s = ''
    byte = bs.read(1)
    while byte:
        for b in hex_to_bin(byte):
            try:
                if b == '0':
                    cn = cn.l
                elif b == '1':
                    cn = cn.r
            except AttributeError:
                s += cn
                cn = N

        byte = bs.read(1)
    return s


if __name__ == '__main__':
    enw = open("murderoftheuniverse.txt", "r").read()
    T = encode(enw)
    encoded_f = open('out', 'rb')
    reconstructed = decode(encoded_f, T)
    encoded_f.close()

    print('\nReconstructed')
    print(reconstructed)

