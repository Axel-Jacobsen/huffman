#! /usr/bin/env python3

from collections import defaultdict


class Node(object):

    def __init__(self, l_child=None, r_child=None):
        self.l_child = l_child
        self.r_child = r_child
        self.name = 'node'

    def __repr__(self):
        return self.name


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

    def write(self, node, file_h, node_num=0):
        if isinstance(node.l_child, Node):
            lnode = node_num + 1
            self.write(node.l_child, file_h, lnode)
        else:
            lnode = node.l_child

        if isinstance(node.r_child, Node):
            rnode = node_num + 2
            self.write(node.r_child, file_h, rnode)
        else:
            rnode = node.r_child

        file_h.write(f'{node_num}|{lnode}|{rnode} ')

    # def build_tree_from_file(self, filename):
    #     if self.huff_tree is None:
    #         raise RuntimeError(
    #             'There is no tree file associated with this HuffmanTree object - must encode a file'
    #         )

    def encode(self, f):
        print('Getting Char Frequency')
        char_freqs = HuffmanCoding._create_char_freqs(f)

        print('Generating Huffman Tree')
        T = HuffmanCoding._gen_huffman(char_freqs)

        print('Generating Writing Table')

        self._gen_write_table(T)
        print(self.write_table)

        print('Writing byte file')
        total_bits = ''
        for char in f:
            total_bits += self.write_table[char]

        # pad the last digits to make bytes out of bits
        len_bits = len(total_bits)
        total_bits += '0' * (8 * (len_bits // 8 + 1) - len_bits)

        with open('out', 'wb') as g:
            bb = int(total_bits, 2).to_bytes(len(total_bits) // 8, 'big')
            g.write(bb)

        self.huff_tree = T
        return T

    def decode(self, encoded_file, tree_file=None):
        cn = mn = self.huff_tree
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
                    cn = mn
            byte = encoded_file.read(1)
        return s[:-1]


if __name__ == '__main__':
    enw = open('murderoftheuniverse.txt', 'r').read()
    hc = HuffmanCoding()
    T = hc.encode(enw)
    with open('treefile', 'w') as f:
        hc.write(T, f)

    encoded_f = open('out', 'rb')
    reconstructed = hc.decode(encoded_f, T)
    encoded_f.close()

    print('\nReconstructed')
    print(reconstructed)

