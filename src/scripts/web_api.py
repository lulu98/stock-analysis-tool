#!/usr/bin/env python3

"""
Local instantiations to call the different Web APIs from EOD historical data.
"""

import os
import sys
import requests
import json

################################################################################
##############################  Fundamentals API  ##############################
################################################################################

def fundamentalsAPI_downloadData(api_key, symbol, exchangeID, filePath):
    url = 'https://eodhistoricaldata.com/api/fundamentals/{}.{}?api_token={}'.format(symbol, exchangeID, api_key)
    r = requests.get(url)
    data = r.json()
    with open(filePath, "w") as f:
        json.dump(data, f, indent=2) # indent in order to format json file

def fundamentalsAPI_getData(api_key, symbol, exchangeID, filters):
    url = 'https://eodhistoricaldata.com/api/fundamentals/{}.{}?api_token={}&filter={}'.format(symbol, exchangeID, api_key, filters)
    r = requests.get(url)
    data = r.text.replace('"', '') # remove quotes
    return data

################################################################################
##################################  Search API  ################################
################################################################################

def searchAPI_getData(api_key, isin):
    url = 'https://eodhistoricaldata.com/api/search/{}?api_token={}'.format(isin, api_key)
    r = requests.get(url)
    data = r.json()
    return data

# TODO: add also instantiations for live/delayed API and End-Of-Day API (not
#       needed at the moment)
