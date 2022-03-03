#!/usr/bin/env python3

"""
Prepares the required file hierarchy based on the ISIN and sets environment
variables that can be used in later stages.
"""

import sys
import os
import json

from scripts.web_api import *

def setup(api_key, isin):
    """
    Prepares the files and sets the necessary environment variables. If there
    exists no entry for an ISIN, it will trigger the search API based on the
    given ISIN.
    """
    stocksFile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stocks.json")

    if not os.path.exists(stocksFile):
        sys.exit("File {} does not exist.".format(stocksFile))

    with open(stocksFile, "r") as f:
        data = json.load(f)

        if not isin in data:
            print("No data for company with ISIN {}.\n".format(isin))
            print("Search API:\n")
            searchData = searchAPI_getData(api_key, isin)
            print("{: <20} {: <20} {: <20}".format("Country" ,"Code", "Exchange"))
            for entry in searchData:
                print("{: <20} {: <20} {: <20}".format(entry["Country"], entry["Code"], entry["Exchange"]))
            print("\n")
            sys.exit("Add entry for {} in {} before continuing...".format(isin, stocksFile))

        symbol = data[isin]["Symbol"]
        exchangeID = data[isin]["ExchangeID"]

    os.environ['SYMBOL'] = symbol
    os.environ['EXCHANGE_ID'] = exchangeID

    stockDir = os.path.dirname(os.path.abspath(__file__))
    stockDir = os.path.join(stockDir, "stocks", isin)
    latexDir = os.path.join(stockDir, "latex")
    jsonFile = os.path.join(stockDir, "data.json")

    os.environ['STOCK_DIR'] = stockDir
    os.environ['LATEX_DIR'] = latexDir
    os.environ['JSON_FILE'] = jsonFile

    if not os.path.exists(stockDir):
        os.makedirs(stockDir)
