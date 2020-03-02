#! /usr/bin/env python3

from collections import defaultdict
import pine
from node import Node


class HuffmanCoding(object):

    TREE_MAGNITUDE = 4

    def __init__(self):
        self.huff_tree = None
        self.write_table = {}

    def _create_char_freqs(bts):
        D = defaultdict(int)
        for byte in bts:
            D[byte] += 1
        return sorted(D.items(), key=lambda v: v[1], reverse=True)

    def _gen_huffman(char_freqs):
        while len(char_freqs) > 1:
            last_2 = char_freqs[-2:]
            del char_freqs[-2:]
            branch = Node(last_2[0][0], last_2[1][0])
            freq_sum = last_2[0][1] + last_2[1][1]
            char_freqs.append((branch, freq_sum))
            char_freqs.sort(key=lambda v: v[1], reverse=True)
        return char_freqs[0][0]

    def gen_write_table(self, node, b=''):
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
        yield bit by bit from byte
        """
        for i in range(discard, 8):
            yield str((byte >> (7 - i)) & 1)

    def encode(self, fname):
        print('Getting Char Frequency')
        with open(fname, 'r') as read_file:
            f = read_file.read()
            char_freqs = HuffmanCoding._create_char_freqs(f)

        print('Generating Huffman Tree')
        T = HuffmanCoding._gen_huffman(char_freqs)

        print('Generating Writing Table')
        self.gen_write_table(T)

        print('Writing byte file')
        total_bits = ''
        for char in f:
            total_bits += self.write_table[char]

        pine_bytes = pine.tree_as_bytes(self.write_table)
        len_pine_b = len(pine_bytes).to_bytes(HuffmanCoding.TREE_MAGNITUDE, 'big')
        padding    = HuffmanCoding.get_tail_padding(total_bits)
        padd_byte  = padding.to_bytes(1, 'big')
        file_bytes = '0' * padding + total_bits
        file_bytes = int(file_bytes, 2).to_bytes(len(file_bytes) // 8, 'big')

        with open(fname + '.pine', 'wb') as g:
            # <4:write_table_size><1:tail_bytes><write_table_size:write_table><r:encoded_file>
            g.write(len_pine_b + padd_byte + pine_bytes + file_bytes)

        self.huff_tree = T
        return T

    def decode(self, encoded_fname: str) -> str:
        s = ''
        write_table_bytes, encoded_file, padding = HuffmanCoding.pull_file_chunks(encoded_fname)
        cn = mn = pine.bytes_as_tree(write_table_bytes)
        for byte in encoded_file:
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

    def get_tail_padding(bits_str: str):
        # pad the last digits to make bytes out of the leftover bits
        len_bits = len(bits_str)
        return 8 * (len_bits // 8 + 1) - len_bits

    def pull_file_chunks(fname: str):
        """
        <size:name of chunk>
        <r:*> -> rest of the bytes in the file belong to chunk *

        <4:write_table_size>
        <1:prepadding>
        <write_table_size:write_table>
        <prepadding:padding>
        <r:encoded_file>
        """
        f = open(fname, 'rb')
        tree_size = int.from_bytes(f.read(HuffmanCoding.TREE_MAGNITUDE), 'big')
        padding = int.from_bytes(f.read(1), 'big')
        tree = f.read(tree_size)
        rest = f.read()
        f.close()

        return tree, rest, padding


if __name__ == '__main__':
    hc = HuffmanCoding()
    T = hc.encode('murderoftheuniverse.txt')
    reconstructed = hc.decode('murderoftheuniverse.txt.pine')

    print('\nReconstructed')
    print(reconstructed)

