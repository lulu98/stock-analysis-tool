#!/usr/bin/env python3

"""
Pipeline - Stage 2

Finds patterns in the JSON data templates and replaces the pattern with a
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
    """
    Sets environment variables required by stage 2.
    """
    rootDir = os.path.abspath(os.getcwd())

    templateDir = os.path.join(rootDir, "template")
    dataDir = os.path.join(rootDir, "data", isin)
    buildDir = os.path.join(rootDir, "stocks", isin)

    jsonFile = os.path.join(buildDir, "data", "data.json")

    os.environ['ROOT_DIR'] = rootDir
    os.environ['DATA_DIR'] = dataDir 
    os.environ['TEMPLATE_DIR'] = templateDir 
    os.environ['BUILD_DIR'] = buildDir
    os.environ['JSON_FILE'] = jsonFile

def isStage01Done():
    dataDir = os.getenv('DATA_DIR')
    return os.path.exists(dataDir)

def isBuildDirectoryExists():
    """Returns if build directory exists."""
    buildDir = os.getenv('BUILD_DIR')
    return os.path.exists(buildDir)

def isFilesTheSame(srcFile, dstFile):
    """Returns if srcFile and dstFile are the same."""
    return filecmp.cmp(srcFile, dstFile)

def setupBuildDirectory(srcFile, dstFile):
    """Sets up build directory."""
    templateDir = os.getenv('TEMPLATE_DIR')
    buildDir = os.getenv('BUILD_DIR')

    print("Initial directory setup started...")
    os.makedirs(buildDir)
    shutil.copytree(templateDir, buildDir, dirs_exist_ok=True)
    shutil.copyfile(srcFile, dstFile)
    print("Initial directory setup done.")

def updateDataDirectory(srcFile, dstFile):
    """Updates data directory."""
    templateDir = os.getenv('TEMPLATE_DIR')
    buildDir = os.getenv('BUILD_DIR')

    templateDataDir = os.path.join(templateDir, "data")
    buildDataDir = os.path.join(buildDir, "data")

    print("Changes in data detected.")
    print("Rebuild data directory started...")
    shutil.copytree(templateDataDir, buildDataDir, dirs_exist_ok=True)
    shutil.copyfile(srcFile, dstFile)
    print("Rebuild data directory done.")

def checkAndInitializeBuildDir(srcFile, dstFile):
    """Set up build directory once initially."""
    if not isBuildDirectoryExists():
        setupBuildDirectory(srcFile, dstFile)

def checkAndUpdateDataDir(srcFile, dstFile):
    """If the financial data changed, update the data directory of the build."""
    if not isFilesTheSame(srcFile, dstFile):
        updateDataDirectory(srcFile, dstFile)

def prepareBuildDir(isin):
    """Prepare build directory for stage 2 execution."""
    jsonSrc = os.path.join(os.getenv('DATA_DIR'), "data.json")
    jsonDst = os.getenv('JSON_FILE')

    if not isStage01Done():
        sys.exit("Data for company {} not available. Execute stage 1 first.".format(isin))

    checkAndInitializeBuildDir(jsonSrc, jsonDst)

    checkAndUpdateDataDir(jsonSrc, jsonDst)

def prepareStage(isin):
    """
    Prepares stage 2 of the stock analysis pipeline. 

    Parameters:
        isin (str): ISIN of the stock to be analysed.
    """
    setEnvironmentVariables(isin)
    prepareBuildDir(isin)

def formatStringToSedInput(text):
    """Format string input into sed compliant input string."""
    output = text.replace("\\", "\\\\")
    return output

def formatStringToSedOutput(text):
    """Format string input into sed compliant output string."""
    output = text.replace("&", "\&")
    output = output.replace("/", "\/")
    output = output.replace("\n", "\\n")
    output = output.replace("'", "'\"'\"'")
    return output

def findPattern(regex, fileName):
    '''
    Find pattern in a file.

    Parameters:
        regex (str): Pattern to be found in the file.
        fileName (str): Name of the file.

    Returns:
        output (list): List of occurrences found.
    '''
    cmd = "sed -n -e 's/.*\({}\).*/\\1/p' {}".format(regex, fileName)
    output = subprocess.check_output(cmd, shell=True).decode('utf-8')
    output = output.split("\n")
    output = list(filter(lambda x: x != '', output)) # remove empty strings in array
    return output

def replacePattern(regex, output, fileName):
    '''
    Replace pattern with output in a file.

    Parameters:
        regex (str): Pattern to be used as replacement.
        output (str): Pattern to be replaced.
        fileName (str): Name of the file.
    '''
    cmd = "sed 's/{}/{}/g' {}".format(regex, output, fileName)
    output = subprocess.check_output(cmd, shell=True).decode('utf-8')
    with open(fileName, "w") as f:
        f.write(output)

def findAndReplacePattern(regex, fileName):
    """
    Find and replace pattern in file. The idea is that a pattern with two 
    underscores is found and then evaluated via a Python function. This pattern 
    is then replaced by the real value.

    Parameters:
        regex (str): Pattern to be found and replaced.
        fileName (str): Name of the file.
    """
    output = findPattern(regex, fileName)

    while(len(output) > 0): # while loop to cope with multiple placeholders in one line
        for placeholder in output:
            pattern = formatStringToSedInput(placeholder)
            replacement = str(eval(placeholder.replace('__', ''))) # the first two underscores must be deleted
            replacement = formatStringToSedOutput(replacement)
            replacePattern(pattern, replacement, fileName)
        output = findPattern(regex, fileName)

def executeStage(isin):
    """
    Find and replace patterns with two underscores in the template JSON data 
    files. After replacing all occurrences of patterns in the JSON files, this 
    stage transforms the JSON files into Latex compatible files via json2latex.
    As a result, we can access the data from the JSON files like an array access 
    in the Latex files.
    """
    dataDir = os.path.join(os.getenv('BUILD_DIR'), "data")
    files = [os.path.join(dataDir, "fund_data.json"),
             os.path.join(dataDir, "calc_data.json")]

    for fileName in files:
        print("File {}:".format(fileName))
        print("Processing started...")

        # first replace all occurrences of placeholder __getYear
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

    prepareStage(args.isin)

    print("Stage 2: started...")
    executeStage(args.isin)
    print("Stage 2: done...\n")
