#! /usr/bin/env python3

from collections import defaultdict

from node import Node


class HuffmanCoding(object):

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

    def _gen_write_table(self, node, b=''):
        try:
            self._gen_write_table(node.l_child, b + '0')
        except AttributeError:
            self.write_table[node.l_child] = b + '0'
        try:
            self._gen_write_table(node.r_child, b + '1')
        except AttributeError:
            self.write_table[node.r_child] = b + '1'

    def _hex_to_bin(byte):
        for i in range(8):
            yield str((int.from_bytes(byte, 'big') >> (7 - i)) & 1)

    def encode(self, fname):
        print('Getting Char Frequency')
        with open(fname, 'r') as read_file:
            f = read_file.read()
            char_freqs = HuffmanCoding._create_char_freqs(f)

        print('Generating Huffman Tree')
        T = HuffmanCoding._gen_huffman(char_freqs)

        print('Generating Writing Table')
        self._gen_write_table(T)

        print('Writing byte file')
        total_bits = ''
        for char in f:
            total_bits += self.write_table[char]

        # pad the last digits to make bytes out of the leftover bits
        len_bits = len(total_bits)
        total_bits += '0' * (8 * (len_bits // 8 + 1) - len_bits)

        # format compressed file name
        with open(fname + '.pine', 'wb') as g:
            bb = int(total_bits, 2).to_bytes(len(total_bits) // 8, 'big')
            g.write(bb)

        self.huff_tree = T
        return T

    def decode(self, encoded_fname, tree_file=None):
        cn = mn = self.huff_tree
        s = ''
        encoded_file = open(encoded_fname)
        byte = encoded_file.read(1)
        while byte:
            for b in HuffmanCoding._hex_to_bin(byte):
                if b == '0':
                    cn = cn.l_child
                elif b == '1':
                    cn = cn.r_child
                if isinstance(cn, str):
                    s += cn
                    cn = mn
            byte = encoded_file.read(1)
        return s[:-1]


if __name__ == '__main__':
    hc = HuffmanCoding()
    T = hc.encode('murderoftheuniverse.txt')

    print(hc.write_table)

    with open('treefile', 'wb') as f:
        hc.write(T, f)

    with open('treefile', 'rb') as g:
        hc.build_tree_from_file(g)

    encoded_f = open('out', 'rb')
    reconstructed = hc.decode(encoded_f, T)
    encoded_f.close()

    print('\nReconstructed')
    print(reconstructed)
