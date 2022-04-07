#!/usr/bin/env python3

"""
Pipeline - Stage 2

Finds patterns in the Latex template and replaces the pattern with a
corresponding value from the local API.
"""

import os
import sys
import subprocess
import json
import shutil
import argparse

import preparation

from scripts.local_api import *
from scripts.calculations import *

parser = argparse.ArgumentParser()

# -k APIKEY -i ISIN
parser.add_argument("-k", "--apikey", required=True, help="API key")
parser.add_argument("-i", "--isin", required=True, help="ISIN")

args = parser.parse_args()

def findPattern(regex, fileName):
    '''
    Find pattern regex in file fileName.
    '''
    cmd = "sed -n -e 's/.*\({}\).*/\\1/p' {}".format(regex, fileName)
    output = subprocess.check_output(cmd, shell=True).decode('utf-8')
    output = output.split("\n")
    output = list(filter(lambda x: x != '', output)) # remove empty strings in array
    return output

def replacePattern(regex, output, fileName):
    '''
    Replace pattern regex with output in file fileName.
    '''
    cmd = "sed 's/{}/{}/g' {}".format(regex, output, fileName)
    output = subprocess.check_output(cmd, shell=True).decode('utf-8')
    with open(fileName, "w") as f:
        f.write(output)

def findAndReplacePattern(regex, fileName):
    output = findPattern(regex, fileName)

    while(len(output) > 0): # while loop to cope with multiple placeholders in one line
        for placeholder in output:
            pattern = placeholder.replace("\\", "\\\\") # sed pattern must have double backslash
            replacement = eval(placeholder.replace('__', '')) # the first two underscores must be deleted
            replacePattern(pattern, replacement, fileName)
        output = findPattern(regex, fileName)

def stage02(symbol):
    jsonFile = os.getenv('JSON_FILE')
    if not os.path.exists(jsonFile):
        print("data.json file {} does not exist".format(jsonFile))
        print("Please execute stage01.py first.")
        return

    stockDir = os.getenv('STOCK_DIR')
    if stockDir == None:
        print("Please set environment variable STOCK_DIR.")
        return

    # create company-specific latex template
    #if not os.path.exists(stockDir):
    #    shutil.copytree("./template", stockDir)

    # files in chapters + main.tex
    files = os.listdir(os.path.join(stockDir, "chapters"))
    files = [os.path.join(stockDir, "chapters", x) for x in files]
    files.append(os.path.join(stockDir, "main.tex"))

    for fileName in files:
        print("File {}:".format(fileName))
        print("Processing started...")

        # first replace all occurrences of placeholder __ticker
        #replacePattern("__ticker", "{}".format(symbol), fileName)

        # second replace all occurrences of placeholder __getYear
        findAndReplacePattern("__getYear([^()]*)", fileName)

        # start evaluating functions
        findAndReplacePattern("__.*(.*)", fileName)

        print("Processing done.\n")

preparation.setup(args.apikey, args.isin)

symbol = os.getenv('SYMBOL')
exchangeID = os.getenv('EXCHANGE_ID')

print("Stage 2: started...")
stage02(symbol)
print("Stage 2: done...\n")
