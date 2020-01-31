#! /usr/bin/env python3


def ws(s):
    assert len(s) % 8 == 0
    with open('out', 'wb') as g:
        bb = int(s, 2).to_bytes(len(s) // 8, 'big')
        g.write(bb)

def htb(b):
    for i in range(8):
        yield str((int.from_bytes(b, 'big') >> (7 - i)) & 1)

def rout():
    s = ''
    with open('out', 'rb') as f:
        byte = f.read(1)
        while byte:
            for b in htb(byte):
                s += b
            byte = f.read(1)
    return s

if __name__ == '__main__':
    s = '1' * 8 + '01' * 4
    s += s[::-1]
    ws(s)
    rs = rout()
    print('ws', s)
    print('rs', rs)
    assert s == rs

