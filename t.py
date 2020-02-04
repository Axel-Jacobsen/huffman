#! /usr/bin/env python3

import numpy as np
import cpsn


class WriteTest(object):

    def ws(s):
        with open('out', 'wb') as g:
            bb = int(s, 2).to_bytes(len(s) // 8, 'big')
            g.write(bb)

    def rout():
        s = ''
        with open('out', 'rb') as f:
            byte = f.read(1)
            while byte:
                for b in WriteTest._htb(byte):
                    s += b
                byte = f.read(1)
        return s

    def _gen_s(i=10, j=4):
        s = ''
        for i in range(np.random.randint(0, high=i)):
            s += np.random.randint(0, high=j) * '0' \
               + np.random.randint(0, high=j) * '1' \
               + np.random.randint(0, high=j) * '01' \
               + np.random.randint(0, high=j) * '10'
        s += '0' * (8 * (len(s) // 8 + 1) - len(s))
        return s

    def _htb(b):
        for i in range(8):
            yield str((int.from_bytes(b, 'big') >> (7 - i)) & 1)

    def test():
        s = WriteTest._gen_s()
        print(s)
        WriteTest.ws(s)
        rs = WriteTest.rout()
        assert s == rs
        print('s == rs asserted')




if __name__ == '__main__':
    WriteTest.test()

