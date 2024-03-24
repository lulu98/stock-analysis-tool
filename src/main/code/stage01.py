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

import config
import helper
import logging
import os
import shutil
import sys

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
    apiParams = helper.get_api_params(api_key, isin)

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
