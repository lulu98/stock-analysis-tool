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
import filecmp

from scripts.local_api import *
from scripts.calculations import *

def setEnvironmentVariables(isin):
    rootDir = os.path.abspath(os.getcwd())
    templateDir = os.path.join(rootDir, "template")
    dataDir = os.path.join(rootDir, "data", isin)
    companyDir = os.path.join(rootDir, "stocks", isin)
    companyDataDir = os.path.join(companyDir, "data")
    jsonSrc = os.path.join(dataDir, "data.json")
    jsonDst = os.path.join(companyDataDir, "data.json")

    if not os.path.exists(dataDir):
        sys.exit("Data for company {} not available. Execute stage 1 first.".format(isin))

    # setup the company folder once initially
    if not os.path.exists(companyDir):
        print("Initial setup started...")
        os.makedirs(companyDir)
        shutil.copytree(templateDir, companyDir, dirs_exist_ok=True)
        shutil.copyfile(jsonSrc, jsonDst)
        print("Initial setup done.")

    # if the data changed, pull the changes into the data folder
    if not filecmp.cmp(jsonSrc, jsonDst):
        print("Changes in data detected.")
        print("Rebuild data directory started...")
        shutil.copytree(os.path.join(templateDir, "data"), companyDataDir, dirs_exist_ok=True)
        shutil.copyfile(jsonSrc, jsonDst)
        print("Rebuild data directory done.")

    os.environ['ROOT_DIR'] = rootDir
    os.environ['DATA_DIR'] = companyDataDir
    os.environ['JSON_FILE'] = jsonDst

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
    output = str(output).replace("&", "\&") # sed pattern & should be replaced
    output = output.replace("/", "\/")      # sed pattern / should be replaced
    output = output.replace("\n", "\\n")    # sed pattern newline should be replaced
    output = output.replace("'", "'\"'\"'") # sed pattern ' should be replaced
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

def stage02():
    dataDir = os.getenv('DATA_DIR')
    files = [os.path.join(dataDir, "fund_data.json"),
             os.path.join(dataDir, "calc_data.json")]

    for fileName in files:
        print("File {}:".format(fileName))
        print("Processing started...")

        # second replace all occurrences of placeholder __getYear
        findAndReplacePattern("__getYear([^()]*)", fileName)

        # start evaluating functions
        findAndReplacePattern("__.*(.*)", fileName)

        print("Processing done.\n")

    cmd = "json2latex {} fundData {}".format(os.path.join(dataDir, "fund_data.json"), os.path.join(dataDir, "fund_data.tex"))
    output = subprocess.check_output(cmd, shell=True).decode('utf-8')

    cmd = "json2latex {} calcData {}".format(os.path.join(dataDir, "calc_data.json"), os.path.join(dataDir, "calc_data.tex"))
    output = subprocess.check_output(cmd, shell=True).decode('utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # -i ISIN
    parser.add_argument("-i", "--isin", required=True, help="ISIN")

    args = parser.parse_args()

    setEnvironmentVariables(args.isin)

    print("Stage 2: started...")
    stage02()
    print("Stage 2: done...\n")
