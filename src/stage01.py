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
    """
    Sets environment variables required for stage 1 of the stock analysis 
    pipeline.
    """
    rootDir = os.path.abspath(os.getcwd())
    dataDir = os.path.join(rootDir, "data")

    os.environ['ROOT_DIR'] = rootDir
    os.environ['DATA_DIR'] = dataDir

def getConfig(api_key, isin):
    """
    Get the configuration arguments required for stage 1 of the stock analysis
    pipeline. The configuration arguments are required by the web API as arguments
    to identify a specific stock. These arguments are the Symbol and ExchangeID. 
    Since they are arbitrary, I use the ISIN locally in this project and have a 
    mapping from ISIN to these configuration arguments in stocks.json. If the 
    ISIN is not specified, i.e. is None, we will pull all stocks that are 
    included in stocks.json.

    Parameters:
        api_key (str): The API key for the financial data API.
        isin (str): The ISIN of the stock that should be pulled from the web API.

    Returns:
        config (dict): Dictionary with configuration arguments for either the 
                       stock specified by the ISIN or all stocks if ISIN is None.
    """
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
    """
    Pull financial data from the web API for a specific stock.

    Parameters:
        api_key (str): The API key for the financial data API.
        isin (str): The ISIN of the stock that should be pulled from the web API.
        symbol (str): Symbol used by the web API to characterize a certain stock.
        exchangeID (str): Name used to identify the stock exchange for a certain 
                          stock.
    """
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
    """
    Pull financial data for each stock contained in config.
    
    Parameters:
        api_key (str): The API key for the financial data API.
        isin (str): The ISIN of the stock that should be pulled from the web API.
    """
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
