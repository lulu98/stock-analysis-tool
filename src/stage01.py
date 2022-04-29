#!/usr/bin/env python3

"""
Pipeline - Stage 1

Pulls financial data from the Web API (i.e. EOD historical data) and stores it
in a JSON file.
"""

import os
import sys
import argparse

from scripts.web_api import *

def setEnvironmentVariables():
    rootDir = os.path.abspath(os.getcwd())
    dataDir = os.path.join(rootDir, "data")

    os.environ['ROOT_DIR'] = rootDir
    os.environ['DATA_DIR'] = dataDir

def getConfig(api_key, isin):
    jsonFile = "./stocks.json"

    with open(jsonFile, "r") as f:
        data = json.load(f)

    config = {}
    if isin != None:
        config[isin] = data[isin] # only get config for specific ISIN
    else:
        config = data # get config for all ISIN

    return config

def pullStockData(api_key, isin, symbol, exchangeID):
    dataDir = os.getenv('DATA_DIR')
    stockDir = os.path.join(dataDir, isin)
    stockFile = os.path.join(stockDir, "data.json")

    if not os.path.exists(stockDir):
        os.makedirs(stockDir)

    if os.path.exists(stockFile):
        print("File {} does already exist.".format(stockFile))
        return
   
    print("Pull financial data for company {}".format(isin))
    fundamentalsAPI_downloadData(api_key, symbol, exchangeID, stockFile)

def stage01(api_key, isin):
    config = getConfig(api_key, isin)

    for isin in config:
        symbol = config[isin]['Symbol']
        exchangeID = config[isin]['ExchangeID']
        pullStockData(api_key, isin, symbol, exchangeID)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # -k APIKEY -i ISIN
    parser.add_argument("-k", "--apikey", required=True, help="API key")
    parser.add_argument("-i", "--isin", required=False, help="ISIN")

    args = parser.parse_args()

    setEnvironmentVariables()

    print("Stage 1: started...")
    stage01(args.apikey, args.isin)
    print("Stage 1: done...\n")
