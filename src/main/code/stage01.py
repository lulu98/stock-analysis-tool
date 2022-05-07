#!/usr/bin/env python3

"""
Pipeline - Stage 1

Pulls financial data from the Web API (i.e. EOD historical data) and stores it
in a JSON file.
"""

import os
import sys
import argparse

from web_api import *

DATA_DIR = "../resources/data"
CONFIG_FILE = "../config/stocks.json"

def getAPIParameters(api_key):
    """
    Get the API parameters for all stocks in stocks.json.

    Parameters:
        api_key (str): The API key for the financial data API.

    Returns:
        apiParams (dict): Dictionary with API parameters for all stocks in 
                          stocks.json.
    """
    jsonFile = CONFIG_FILE

    with open(jsonFile, "r") as f:
        data = json.load(f)
    
    apiParams = data

    return apiParams

def triggerSearchAPI(api_key, isin):
    """
    Trigger Search API for ISIN and format output as feedback for the user.
    """
    print("Output of Search API for ISIN {}:\n".format(isin))
    searchData = searchAPI_getData(api_key, isin)
    print("{: <20} {: <20} {: <20}".format("Country" ,"Code", "Exchange"))
    for entry in searchData:
        print("{: <20} {: <20} {: <20}".format(entry["Country"], entry["Code"], entry["Exchange"]))
    print("\n")

def getAPIParametersForStock(api_key, isin):
    """
    Get the API parameters for a specific stock in stocks.json.

    Parameters:
        api_key (str): The API key for the financial data API.
        isin (str): The ISIN of the stock that should be pulled from the web API.

    Returns:
        apiParams (dict): Dictionary with API parameters for the stock specified 
                          by the ISIN.
    """
    jsonFile = CONFIG_FILE

    with open(jsonFile, "r") as f:
        data = json.load(f)

    if not isin in data:
        # There is no entry for isin in stocks.json yet.
        print("No data for company with ISIN {}.\n".format(isin))
        triggerSearchAPI(api_key, isin)
        sys.exit("Add entry for {} in {} before continuing...".format(isin, jsonFile))

    apiParams = {}
    apiParams[isin] = data[isin] # only get API parameters for specific ISIN

    return apiParams

def pullStockData(api_key, isin, symbol, exchangeID):
    """
    Pull financial data from the web API for a specific stock.

    Parameters:
        api_key (str): The API key for the financial data API.
        isin (str): The ISIN of the stock that should be pulled from the web API.
        symbol (str): Symbol used by the web API to characterize a certain stock.
        exchangeID (str): Name used to identify the stock exchange for a certain 
                          stock.
    """
    dataDir = DATA_DIR
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
    """
    Pull financial data for each stock contained in apiParams.
    
    Parameters:
        api_key (str): The API key for the financial data API.
        isin (str): The ISIN of the stock that should be pulled from the web API.
    """
    if isin == None:
        apiParams = getAPIParameters(api_key)
    else:
        apiParams = getAPIParametersForStock(api_key, isin)

    for isin in apiParams:
        symbol = apiParams[isin]['Symbol']
        exchangeID = apiParams[isin]['ExchangeID']
        pullStockData(api_key, isin, symbol, exchangeID)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # -k APIKEY -i ISIN
    parser.add_argument("-k", "--apikey", required=True, help="API key")
    parser.add_argument("-i", "--isin", required=False, help="ISIN")

    args = parser.parse_args()

    print("Stage 1: started...")
    stage01(args.apikey, args.isin)
    print("Stage 1: done...\n")
