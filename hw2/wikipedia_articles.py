#!/usr/bin/env python3
import argparse
import re
from bs4 import BeautifulSoup
import requests
import json

parser = argparse.ArgumentParser(
                    prog='Wikipedia web crawler',
                    description='''This program starts off with the specified article and 
                    visits all the articles linked to it and so on until specified depth
                    is  reached.''',
                    epilog='Pssst... Your back is all white!')

parser.add_argument('--url', help='URL to start with')
parser.add_argument('--depth', type=int, help='Crawling depth')
parser.add_argument('-max_output',
                    help='''Maximum number of articles to output, because I do not want to crash Wikipedia :D
                    Default value is 1000''',
                    default=1000)

args = parser.parse_args()

headers = {'User-Agent': 'MyEducationalScraper/1.0 (contact: Alexandra Suvorova)'}
base_url = 'https://en.wikipedia.org/wiki/'

pat = re.compile(r'^(/wiki/)((?!:).)*$') #  so-called negative lookaround

def get_articles(article):
    url = base_url + article
    r = requests.get(url, headers=headers, timeout=5)
    r.raise_for_status()

    bs = BeautifulSoup(r.content, 'html.parser')
    content = bs.find('div', id='bodyContent')

    if content:
        return content.find_all('a', href=pat)
    return []

unique_links = set()
unique_links.add(args.url.split('/')[-1])
links2visit = [args.url]
is_enough = False
edges = []

for _ in range(args.depth):
    links_new = []
    for link in links2visit:
        articles = get_articles(link)
        for article in articles:
            article_link = article['href'].split('/')[-1]
            edges.append((link.replace('_', ' '), article_link.replace('_', ' ')))
            if article_link not in unique_links:
                unique_links.add(article_link)
                links_new.append(article_link)
                edges.append((link, article_link))
                if len(unique_links) == args.max_output:
                    is_enough = True
                    print(f'Reached maximum number of articles specified in -max_output parameter: {args.max_output}')
                    break
        if is_enough:
            break
    if is_enough:
        break
    links2visit = links_new

for i, name in enumerate(sorted(unique_links)):
    name = name.replace('_', ' ')
    print(f'{i + 1}. {name}')

with open(args.url + '.json', 'w') as out:
    json.dump(edges, out)