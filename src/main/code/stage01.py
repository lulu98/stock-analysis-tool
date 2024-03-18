#!/usr/bin/env python3

"""Pipeline - Stage 1

Description:

Pulls financial data from the Web API (i.e. EOD historical data) and stores it
in a JSON file.

Usage:
    stage01.py [-h] -k <api_key> [-i <isin>] [--clean]

Options:
    -h, --help                      Show help menu.
    -k <api_key>, --key <api_key>   API key for web API.
    -i <isin>, --isin <isin>        ISIN of stock.
    --clean                         Clean up directories.
"""
from docopt import docopt

import os
import sys
import logging
import config
import shutil

from web_api import *

args = docopt(__doc__)

def init_stage01(isin):
    # generate default config
    run_conf = config.generate_default_config(isin)

    # set log level
    logging.basicConfig(level=run_conf["LOG_LEVEL"])

    if isin:
        if args['--clean']:
            # clean up directories
            if os.path.exists(run_conf["RESOURCE_DATA_DIR"]):
                logging.info("Deleting {}".format(run_conf["RESOURCE_DATA_DIR"]))
                shutil.rmtree(run_conf["RESOURCE_DATA_DIR"])
            sys.exit(0)
        else:
            # sanity checks
            if os.path.exists(run_conf["RESOURCE_DATA_FILE"]):
                logging.info("{} detected - nothing to be done.".format(run_conf["RESOURCE_DATA_FILE"]))
                sys.exit(0)

            # create default directories
            if not os.path.exists(run_conf["RESOURCE_DATA_DIR"]):
                os.makedirs(run_conf["RESOURCE_DATA_DIR"])


def getAPIParameters(api_key):
    """
    Get the API parameters for all stocks in stocks.json.

    Parameters:
        api_key (str): The API key for the financial data API.

    Returns:
        apiParams (dict): Dictionary with API parameters for all stocks in
                          stocks.json.
    """
    jsonFile = config.get_run_config_item("STOCKS_FILE")

    with open(jsonFile, "r") as f:
        data = json.load(f)

    apiParams = data

    return apiParams


def triggerSearchAPI(api_key, isin):
    """
    Trigger Search API for ISIN and format output as feedback for the user.
    """
    logging.info("Output of Search API for ISIN {}:\n".format(isin))
    searchData = searchAPI_getData(api_key, isin)
    logging.info("{: <20} {: <20} {: <20}".format(
        "Country",
        "Code",
        "Exchange"))
    for entry in searchData:
        logging.info("{: <20} {: <20} {: <20}".format(
            entry["Country"],
            entry["Code"],
            entry["Exchange"]))
    logging.info("\n")


def getAPIParametersForStock(api_key, isin):
    """
    Get the API parameters for a specific stock in stocks.json.

    Parameters:
        api_key (str): The API key for the financial data API.
        isin (str): The ISIN of the stock that should be pulled from the web
                    API.

    Returns:
        apiParams (dict): Dictionary with API parameters for the stock
                          specified by the ISIN.
    """
    jsonFile = config.get_run_config_item("STOCKS_FILE")

    with open(jsonFile, "r") as f:
        data = json.load(f)

    if isin not in data:
        # There is no entry for isin in stocks.json yet.
        logging.info("No data for company with ISIN {}.\n".format(isin))
        triggerSearchAPI(api_key, isin)
        sys.exit("Add entry for {} in {} before continuing...".format(
            isin,
            jsonFile))

    apiParams = {}
    apiParams[isin] = data[isin]  # only get API parameters for specific ISIN

    return apiParams


def pullStockData(api_key, isin, symbol, exchangeID):
    """
    Pull financial data from the web API for a specific stock.

    Parameters:
        api_key (str): The API key for the financial data API.
        isin (str): The ISIN of the stock that should be pulled from the web
                    API.
        symbol (str): Symbol used by the web API to characterize a certain
                      stock.
        exchangeID (str): Name used to identify the stock exchange for a
                          certain stock.
    """
    init_stage01(isin)
    stockFile = config.get_run_config_item("RESOURCE_DATA_FILE")

    if os.path.exists(stockFile):
        logging.info("File {} does already exist.".format(stockFile))
        return

    logging.info("Pull financial data for company {}".format(isin))
    fundamentalsAPI_downloadData(api_key, symbol, exchangeID, stockFile)


def exec_stage01(api_key, isin):
    """
    Pull financial data for each stock contained in apiParams.

    Parameters:
        api_key (str): The API key for the financial data API.
        isin (str): The ISIN of the stock that should be pulled from the web
                    API.
    """
    if isin is None:
        apiParams = getAPIParameters(api_key)
    else:
        apiParams = getAPIParametersForStock(api_key, isin)

    for isin in apiParams:
        symbol = apiParams[isin]['Symbol']
        exchangeID = apiParams[isin]['ExchangeID']
        pullStockData(api_key, isin, symbol, exchangeID)


if __name__ == '__main__':

    key = args['--key']
    isin = args['--isin']

    init_stage01(isin)
    logging.info("Stage 1: started...")
    exec_stage01(key, isin)
    logging.info("Stage 1: done...")
