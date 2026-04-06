import requests
import json
import time
from tqdm import tqdm

headers = {'accept': 'application/json'}

print('Searching DNAse-seq experiments...')
url = 'https://www.encodeproject.org/search/?type=Experiment&biosample_ontology.classification=cell+line&assay_term_name=DNase-seq&limit=all&format=json'
response = requests.get(url, headers=headers)
search_results = response.json()

dnase_seq_counts = dict()
for elem in search_results['@graph']:
    cell_line = elem['biosample_ontology']['term_name']
    if cell_line not in dnase_seq_counts:
        dnase_seq_counts[cell_line] = 1
    else:
        dnase_seq_counts[cell_line] += 1

print('Searching CHIP-seq experiments...')
for cell_line in sorted(dnase_seq_counts, key=lambda k: dnase_seq_counts[k], reverse=True):
    url = f'https://www.encodeproject.org/search/?type=Experiment&biosample_ontology.classification=cell+line&biosample_ontology.term_name={cell_line}&assay_term_name=ChIP-seq&limit=all&format=json'
    response = requests.get(url, headers=headers)
    search_results = response.json()
    if len(search_results['@graph']) > 0:
        break

target_data = []
for elem in search_results['facets']:
    if elem['field'] == 'target.label':
        target_data = elem['terms']
        break

gene_names = [elem['key'] for elem in target_data]

results = dict()

print('Searching proteins corresponding our genes...')
# For some reason the following did not work through Wi-Fi with or without VPN
for i in tqdm(range(len(gene_names))):
    gene = gene_names[i]
    # 9606 - Homo sapiens
    query = f"gene:{gene} AND taxonomy_id:9606"

    # API endpoint
    url = "https://rest.uniprot.org/uniprotkb/search"

    # Parameters
    params = {
        "query": query,
        "format": "json",
        "fields": "accession"
    }

    for i in range(5):
        try:
            response = requests.get(requests.Request('GET', url, params=params).prepare().url)
            response.raise_for_status()

            data = response.json()
            results[gene] = []

            if data["results"]:
                for result in data["results"]:
                    results[gene].append(result["primaryAccession"])
            break
        except:
            continue
    time.sleep(1)


# OMFG it finally worked!!!

gene2domain = dict()
retries = 5

print('Looking up Pfam domains...')
for gene, ids in tqdm(results.items(), position=0, leave=True):
    gene2domain[gene] = []
    pfam_ids = set()
    for up_id in ids:
        managed = False
        for i in range(retries):
            try:
                url = f'https://www.ebi.ac.uk/interpro/api/protein/uniprot/{up_id}/entry/pfam'
                response = requests.get(url)
                response.raise_for_status()
                managed = True
                break
            except:
                time.sleep(0.5)
            print(f"Couldn't connect to {url}, tried {i+1} times")
        if response.status_code == 204:
            continue   # No entries found matching this request
        if managed:
            data = response.json()
            time.sleep(0.5)
            for i in range(retries):
                try:
                    response = requests.get(data['entries_url'])
                    response.raise_for_status()
                    data = response.json()['results']
                    for res in data:
                        pfam_ids.add(res['metadata']['accession'])
                    break
                except:
                    time.sleep(0.5)
                print(f"Couldn't connect to {url}, tried {i + 1} times")
            time.sleep(0.5)
        domain_ids = set()
        for pfam_id in pfam_ids:
            for i in range(retries):
                try:
                    url = f'https://www.ebi.ac.uk/interpro/api/entry/pfam/{pfam_id}?ida'
                    response = requests.get(url)
                    response.raise_for_status()
                    break
                except:
                    time.sleep(0.5)
                print(f"Couldn't connect to {url}, tried {i+1} times")
            data = response.json()
            for res in data['results']:
                if 'representative' in res.keys():
                    for repr in res['representative']['domains']:
                        domain_ids.add(repr['accession'])
            time.sleep(0.5)
    gene2domain[gene] = domain_ids

data2write = {key: list(sorted(gene2domain[key])) for key in gene2domain}

with open('domains.json', 'w') as outfile:
    json.dump(data2write, outfile, indent=4)