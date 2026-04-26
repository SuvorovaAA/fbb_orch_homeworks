#!/usr/bin/env python3
import argparse
import subprocess
import re
import requests
import json

parser = argparse.ArgumentParser(
                    prog='Parser of traffic route',
                    description='''Using traceroute tool and ipwho.is API
                    finds how the packages travel to reach the host from 
                    the specified url. 
                    Outputs to <url>.json.''',)
parser.add_argument('url', help='URL to reach out to')

args = parser.parse_args()

protocol, url = args.url.split('//', maxsplit=1)
host = url.split('/')[0].split('?')[0]

if ':' in host:
    host, port = host.split(':')
    print(f'Host: {host}, port: {port}')
    line2run = f"traceroute {host} -p {port} -n"
else:
    print(f'Host: {host}')
    line2run = f"traceroute {host} -n"

result = subprocess.run(line2run, shell=True, capture_output=True, text=True)

# Matches any 1-3 digit numbers separated by dots
pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"

hops = []
silent_hops = 0
for line in result.stdout.split('\n'):
    # Matches any 1-3 digit numbers separated by dots
    ips = re.findall(pattern, line)
    if not ips:
        silent_hops += 1
    else:
        hops.append(ips)

traceroute_steps = []

for ips in hops:
    hop_data = []
    for ip in ips:
        response = requests.get(f"https://ipwho.is/{ip}")
        data = response.json()
        if data['success']:
            hop_data.append((data['country'], data['city'], data['ip']))
    if hop_data:
        traceroute_steps.append(hop_data)

data2dump = {
    'traceroute_steps': traceroute_steps,
    'silent_hops': silent_hops
    }

with open(host + '.json', 'w') as out:
    json.dump(data2dump, out, indent=4)