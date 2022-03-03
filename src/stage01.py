#!/usr/bin/env python3

"""
Pipeline - Stage 1

Pulls financial data from the Web API (i.e. EOD historical data) and stores it
in a JSON file.
"""

import os
import sys
import argparse

import preparation
from scripts.web_api import *

parser = argparse.ArgumentParser()

# -k APIKEY -i ISIN
parser.add_argument("-k", "--apikey", required=True, help="API key")
parser.add_argument("-i", "--isin", required=True, help="ISIN")

args = parser.parse_args()

def stage01(api_key, symbol, exchangeID):
    jsonFile = os.getenv('JSON_FILE')

    if jsonFile == None:
        print("Please set environment variable JSON_FILE.")
        return

    if os.path.exists(jsonFile):
        print("File {} already exists.".format(jsonFile))
        return

    print("Pull financial data for company {}".format(symbol))
    fundamentalsAPI_downloadData(api_key, symbol, exchangeID, jsonFile)

preparation.setup(args.apikey, args.isin)

symbol = os.getenv('SYMBOL')
exchangeID = os.getenv('EXCHANGE_ID')

print("Stage 1: started...")
stage01(args.apikey, symbol, exchangeID)
print("Stage 1: done...\n")
