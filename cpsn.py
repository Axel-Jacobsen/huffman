#! /usr/bin/env python3

from collections import defaultdict


class HuffmanCoding(object):

    def __init__(self, filename):
        self.filename = filename
        self.huff_tree = None

    class Node(object):

        def __init__(self, l_child=None, r_child=None):
            self.l_child = l_child
            self.r_child = r_child

        def __repr__(self):
            return self.name

    def _create_char_freqs(bts):
        D = defaultdict(int)
        for byte in bts:
            D[byte] += 1
        return sorted(D.items(), key=lambda v: v[1], reverse=True)

    def _gen_huffman(char_freqs):
        i = 0
        while len(char_freqs) > 1:
            last_2 = char_freqs[-2:]
            del char_freqs[-2:]

            i += 1
            branch = HuffmanCoding.Node(last_2[0][0], last_2[1][0])
            freq_sum = last_2[0][1] + last_2[1][1]
            char_freqs.append((branch, freq_sum))
            char_freqs.sort(key=lambda v: v[1], reverse=True)
        return char_freqs[0][0]

    def _gen_write_table(huffman_tree, write_table, b=''):
        try:
            HuffmanCoding._gen_write_table(
                huffman_tree.l_child, write_table, b + '0')
        except AttributeError:
            write_table[huffman_tree.l] = b + '0'
        try:
            HuffmanCoding._gen_write_table(
                huffman_tree.r_child, write_table, b + '1')
        except AttributeError:
            write_table[huffman_tree.r] = b + '1'

    def _hex_to_bin(byte):
        for i in range(8):
            yield str((int.from_bytes(byte, 'big') >> (7 - i)) & 1)

    def write_tree_file(self):
        if self.huff_tree is None:
            raise RuntimeError(
                'There is no tree file associated with this HuffmanTree object - must encode a file'
            )
        

    def build_tree_from_file(self, filename):
        pass

    def encode(self, f):
        print('Getting Char Frequency')
        char_freqs = HuffmanCoding._create_char_freqs(f)

        print('Generating Huffman tree')
        T = HuffmanCoding.gen_huffman(char_freqs)
        wt = {}

        print('Generating Writing Table')
        HuffmanCoding._gen_write_table(T, wt)

        print('Writing byte file')
        total_bits = ''
        for char in f:
            total_bits += wt[char]

        # pad the last digits to make bytes out of bits
        len_bits = len(total_bits)
        total_bits += '0' * (8 * (len_bits // 8 + 1) - l)

        with open('out', 'wb') as g:
            bb = int(total_bits, 2).to_bytes(len(total_bits) // 8, 'big')
            g.write(bb)

        self.huff_tree = T
        return T

    def decode(self, encoded_file, tree_file=None):
        if tree_file is None:
            if self.huff_tree is None:
                raise RuntimeError(
                    'Huffman Tree has not been created - must supply the tree file')
            cn = self.huff_tree
        else:
            cn = HuffmanCoding.build_tree_from_file(tree_file)

        s = ''
        byte = encoded_file.read(1)
        while byte:
            for b in HuffmanCoding._hex_to_bin(byte):
                if b == '0':
                    cn = cn.l_child
                elif b == '1':
                    cn = cn.r_child
                if isinstance(cn, str):
                    s += cn
                    cn = N
            byte = encoded_file.read(1)
        return s[:-1]


if __name__ == '__main__':
    enw = open('murderoftheuniverse.txt', 'r').read()
    hc = HuffmanCoding()
    T = hc.encode(enw)
    encoded_f = open('out', 'rb')
    reconstructed = hc.decode(encoded_f, T)
    encoded_f.close()

    print('\nReconstructed')
    print(reconstructed)
