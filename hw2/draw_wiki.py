#!/usr/bin/env python3
import networkx as nx
import matplotlib.pyplot as plt
import argparse
import json

parser = argparse.ArgumentParser(
                    prog='Visualiser of url connections graph',
                    description='''This program helps in visualising connections
                    graph that is produced by Wikipedia web crawler.''',)
parser.add_argument('url', help='URL for which crawling has been done')
parser.add_argument('--output', help='Output file', default='output.png')

args = parser.parse_args()

with open(args.url + '.json') as file:
    edges = json.load(file)

G = nx.Graph()
G.add_edges_from(edges)
color_map = ['tab:green' if node == args.url else 'tab:blue' for node in G.nodes()]
nx.draw(G, with_labels=False, node_color=color_map, node_size = 50)
plt.savefig(args.output, format="PNG")