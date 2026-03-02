#!/usr/bin/env python3
import argparse
import json

default_k = 4

parser = argparse.ArgumentParser(
                    prog='count_kmers',
                    description='Takes a FASTA file and writes kmers counts to .json file.')

parser.add_argument('--fa', help='Input file in FASTA format', required=True)
parser.add_argument('-out', help='Output file name', default='cnts.json')
parser.add_argument('-k', help=f'Value of k, default is {default_k}', default=default_k)

args = parser.parse_args()
out = dict()

def count_kmers(seq, k):
    ans = dict()
    for i in range(len(seq) - k + 1):
        kmer = seq[i:i + k]
        if kmer not in ans.keys():
            ans[kmer] = 1
        else:
            ans[kmer] += 1
    return ans

with open(args.fa) as file:
    seq = ''
    for line in file:
        line = line.rstrip()
        if line.startswith('>'):
            if seq:
                out[name] = count_kmers(seq, int(args.k))
            name = line[1:]
            seq = ''
        else:
            seq += line
    if seq:
        out[name] = count_kmers(seq, int(args.k))

with open(args.out, 'w') as file:
    json.dump(out, file, indent=4)
