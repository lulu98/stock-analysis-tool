"""
EOD Historical Data is used as the web API from which the financial data is
pulled. This file comprises of local instantiations to call the web API.
"""

import os
import sys
import requests
import json

###############################################################################
#                               Fundamentals API                              #
###############################################################################


def fundamentalsAPI_downloadData(api_key, symbol, exchangeID, filePath):
    """
    Pull financial data returned from the Fundamentals Data API into a JSON
    file locally.

    Parameters:
        api_key (str): The API key for the web API.
        symbol (str): Symbol used by the web API to characterize a certain
                      stock.
        exchangeID (str): Name used to identify the stock exchange for a
                          certain stock.
        filePath (str): Path to the file that should store the returned data.
    """
    url = 'https://eodhistoricaldata.com/api/fundamentals/{}.{}?api_token={}'.format(symbol, exchangeID, api_key)
    r = requests.get(url)
    data = r.json()
    with open(filePath, "w") as f:
        json.dump(data, f, indent=2)  # indent in order to format json file


def fundamentalsAPI_getData(api_key, symbol, exchangeID, filters):
    """
    Get data from the Fundamentals Data API.

    Parameters:
        api_key (str): The API key for the web API.
        symbol (str): Symbol used by the web API to characterize a certain
                      stock.
        exchangeID (str): Name used to identify the stock exchange for a
                          certain stock.
        filters (str): Filters to be used to select only a subset of the data
                       from the web API.

    Returns:
        data (json): JSON string of what is retruend from the Fundamentals Data
                     API.
    """
    url = 'https://eodhistoricaldata.com/api/fundamentals/{}.{}?api_token={}&filter={}'.format(symbol, exchangeID, api_key, filters)
    r = requests.get(url)
    data = r.text.replace('"', '')  # remove quotes
    return data

###############################################################################
#                                   Search API                                #
###############################################################################


def searchAPI_getData(api_key, isin):
    """
    Get data from the Search API.

    Parameters:
        api_key (str): The API key for the web API.
        isin (str): The ISIN of the stock for which data should be pulled from
                    the web API.

    Returns:
        data (json): JSON string of what is returned from the Search API.
    """
    url = 'https://eodhistoricaldata.com/api/search/{}?api_token={}'.format(isin, api_key)
    r = requests.get(url)
    data = r.json()
    return data

# TODO: add also instantiations for live/delayed API and End-Of-Day API (not
#       needed at the moment)
