#! /usr/bin/env python3


import sys
import time
from collections import defaultdict

import pine
from node import Node


class HuffmanCoding(object):

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

    def _byte_to_bits(byte, discard=0):
        """
        yield bit by bit from byte, ignoring the first `discard` bits
        `discard` is used to ignore the zero padding before the encoded file
        """
        for i in range(discard, 8):
            yield str((byte >> (7 - i)) & 1)

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

        contents = pine.create_file_contents(self.write_table, encoded_data)

        with open(fname + '.pine', 'wb') as g:
            g.write(contents)

        return T

    def decode(self, encoded_fname: str) -> str:
        """
        Decode the .pine file given by its filename
        """
        s = ''
        write_table_bytes, encoded_data, padding = pine.get_file_chunks(encoded_fname)
        cn = mn = pine.tree_from_bytes(write_table_bytes)
        for byte in encoded_data:
            for b in HuffmanCoding._byte_to_bits(byte, padding):
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
    filename = 'murderoftheuniverse.txt'
    if len(sys.argv) == 2:
        filename = sys.argv[1]

    t1 = time.time()
    hc = HuffmanCoding()
    T = hc.encode(filename)
    t2 = time.time()

    print('------------------')
    print(f'Time to compress: {t2 - t1}\n')

    print('Uncompressing file')
    reconstructed = hc.decode(filename + '.pine')
    original = open(filename, 'r').read()
    print('------------------')
    print(f'Time to decompress: {time.time() - t2}\n')

    try:
        assert reconstructed == original
    except AssertionError:
        print("DECOMPRESSION ERROR")
        print(reconstructed)
        print(original)
    print('Reconstructed equal to original')
    # print(reconstructed)

