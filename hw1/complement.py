#!/usr/bin/env python3
import argparse

parser = argparse.ArgumentParser(
                    prog='complement',
                    description='Finds reverse-complement of given sequence and calculates GC-content.')

parser.add_argument('--seq', help='Input sequence', required=True)

args = parser.parse_args()
seq = args.seq.upper()

def rev_compl(seq):
    dct = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
    out = ''
    for c in seq[::-1]:
        out += dct[c]
    return out

def gc(seq):
    return (seq.count('G') + seq.count('C'))/ len(seq)

print(rev_compl(seq))
print(f'{gc(seq):.03f}')