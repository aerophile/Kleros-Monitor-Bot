#!/usr/bin/python3

import sys
import os
from kleros import Kleros, KlerosDispute, KlerosVote
from collections import Counter, defaultdict
import pprint
import requests

node_url = os.environ["ETH_NODE_URL"]

pp = pprint.PrettyPrinter(indent=2)
case_Number = 1
juror_accounts = []

def get_dispute_max():
    url = "https://api.etherscan.io/api?" \
    "module=logs&action=getLogs" \
    "&fromBlock=379224&toBlock=latest" \
    "&address=0x988b3A538b618C7A603e1c11Ab82Cd16dbE28069" \
    "&topic0=0x141dfc18aa6a56fc816f44f0e9e2f1ebc92b15ab167770e17db5b084c10ed995" \
    "&apikey=YourApiKeyToken"
    response = requests.get(url = url)
    dict_json_response = response.json()
    dispute_num_hex = dict_json_response["result"][-1]['topics'][1]
    dispute_num_decimal = int(dispute_num_hex, 16)
    return dispute_num_decimal

total_dispute = get_dispute_max()

while case_Number < total_dispute:
    dispute = KlerosDispute(case_Number, node_url=node_url)
    appeal = len(dispute.rounds) - 1
    jurors = dispute.rounds[-1]

    for i in range(jurors):
    	Votingdata = KlerosVote(case_Number, node_url=node_url, appeal = appeal, vote_id = i)
    	dude_to_add = Votingdata.account
    	juror_accounts.append(dude_to_add)        
    case_Number = case_Number + 1

unique_jurors = dict(Counter(juror_accounts))
new_unique_jurors = defaultdict(list)
{new_unique_jurors[v].append(k) for k, v in unique_jurors.items()}

dispute_number = case_Number - 1
print("A total of %s unique jurors have been picked on Kleros" % len(unique_jurors))
print("A total of %s disputes have been arbitraged on Kleros" % dispute_number)
pp.pprint(new_unique_jurors)
