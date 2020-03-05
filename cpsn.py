#! /usr/bin/env python3


import sys
import time
from collections import defaultdict

import pine
from node import Node


class HuffmanCoding(object):

    TREE_MAGNITUDE = 2

    def __init__(self):
        self.write_table = {}

    def _create_char_freqs(bts):
        D = defaultdict(int)
        for byte in bts:
            D[byte] += 1
        return sorted(D.items(), key=lambda v: v[1], reverse=True)

    def _pop_last_two(char_freqs):
        last_2 = char_freqs[-2:]
        del char_freqs[-2:]
        return last_2

    def _gen_huffman_tree(char_freqs):
        """
        Create the Huffman Tree which will be used for compression
        """
        while len(char_freqs) > 1:
            bot1, bot2 = HuffmanCoding._pop_last_two(char_freqs)
            branch = Node(bot1[0], bot2[0])
            char_freqs.append((branch, bot1[1] + bot2[1]))
            char_freqs.sort(key=lambda v: v[1], reverse=True)
        return char_freqs[0][0]

    def gen_write_table(self, node, b=''):
        """
        Generate write table (which maps the character to its code
        in the Huffman Tree)
        """
        try:
            self.gen_write_table(node.l_child, b + '0')
        except AttributeError:
            self.write_table[node.l_child] = b + '0'
        try:
            self.gen_write_table(node.r_child, b + '1')
        except AttributeError:
            self.write_table[node.r_child] = b + '1'

    def encode(self, fname):
        print('Getting Char Frequency')
        with open(fname, 'r') as read_file:
            f = read_file.read()
            char_freqs = HuffmanCoding._create_char_freqs(f)

        print('Generating Huffman Tree')
        T = HuffmanCoding._gen_huffman_tree(char_freqs)

        print('Generating Writing Table')
        self.gen_write_table(T)

        print('Writing byte file')
        encoded_data = ''
        for char in f:
            encoded_data += self.write_table[char]

        HuffmanCoding.write_to_file(self.write_table, encoded_data, fname)

        return T

    def write_to_file(write_table, encoded_data, fname):
        """
        this function does the grunt work of getting the
        write table and encoded data ready and writing it
        to a file
        """
        pine_bytes = pine.bytes_from_write_table(write_table)
        len_pine_bytes = len(pine_bytes).to_bytes(HuffmanCoding.TREE_MAGNITUDE, 'big')
        padding = pine.get_padding_size(len(encoded_data))
        padding_byte = padding.to_bytes(1, 'big')
        file_bytes = '0' * padding + encoded_data
        file_bytes = int(file_bytes, 2).to_bytes(len(file_bytes) // 8, 'big')

        contents =  len_pine_bytes + padding_byte + pine_bytes + file_bytes

        with open(fname + '.pine', 'wb') as g:
            g.write(contents)


    def decode(self, encoded_fname: str) -> str:
        """
        Decode the .pine file given by its filename
        """
        s = ''
        write_table_bytes, encoded_data, padding = pine.get_file_chunks(encoded_fname)
        cn = mn = pine.tree_from_bytes(write_table_bytes)
        for byte in encoded_data:
            for b in pine.byte_to_bits(byte, padding):
                if b == '0':
                    cn = cn.l_child
                elif b == '1':
                    cn = cn.r_child
                if isinstance(cn, str):
                    s += cn
                    cn = mn
            padding = 0
        return s


if __name__ == '__main__':
    filename = 'README.md'
    if len(sys.argv) == 2:
        filename = sys.argv[1]

    t1 = time.time()
    hc = HuffmanCoding()
    T = hc.encode(filename)
    t2 = time.time()
    print(hc.write_table)

    print('------------------')
    print(f'Time to compress: {t2 - t1}\n')

    print('Uncompressing file')
    reconstructed = hc.decode(filename + '.pine')
    original = open(filename, 'r').read()
    print('------------------')
    print(f'Time to decompress: {time.time() - t2}\n')

    assert reconstructed == original
    print('Reconstructed equal to original')
    # print(reconstructed)

