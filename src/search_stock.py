#!/usr/bin/env python3

"""
Searchs stock information based on the ISIN by using the Web Search API.
"""

import os
import argparse
import json

from scripts.web_api import *

parser = argparse.ArgumentParser()

# -k APIKEY -i ISIN
parser.add_argument("-k", "--apikey", required=True, help="API key")
parser.add_argument("-i", "--isin", required=True, help="ISIN")

args = parser.parse_args()

data = searchAPI_getData(args.apikey, args.isin)

#print("{: <20} {: <20} {: <20}".format("Country","Code","Exchange"))
#for entry in data:
#    print("{: <20} {: <20} {: <20}".format(entry["Country"],entry["Code"],entry["Exchange"]))

print(json.dumps(data[0], indent=4, sort_keys=True))
