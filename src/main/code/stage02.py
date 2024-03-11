#!/usr/bin/env python3

"""Pipeline - Stage 2

Description:

Finds patterns in the JSON data templates and replaces the pattern with a
corresponding value from the local API.

Usage:
    stage02.py [-h] -i <isin>

Options:
    -h, --help                  Show help menu.
    -i <isin>, --isin <isin>    ISIN of stock.
"""
from docopt import docopt

import os
import sys
import subprocess
import json
import shutil
import argparse
import filecmp

import render


def setEnvironmentVariables(isin):
    """
    Sets environment variables required by stage 2.
    """
    rootDir = os.path.join(os.path.abspath(os.getcwd()), "..")

    templateDir = os.path.join(rootDir, "resources", "template")
    dataDir = os.path.join(rootDir, "resources", "data", isin)
    buildDir = os.path.join(rootDir, "build", isin)

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
    """If financial data changed, update the data directory of the build."""
    if not isFilesTheSame(srcFile, dstFile):
        updateDataDirectory(srcFile, dstFile)


def prepareBuildDir(isin):
    """Prepare build directory for stage 2 execution."""
    jsonSrc = os.path.join(os.getenv('DATA_DIR'), "data.json")
    jsonDst = os.getenv('JSON_FILE')

    if not isStage01Done():
        sys.exit("Data for company {} not available. "
                 "Execute stage 1 first.".format(isin))

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


def executeStage(isin):
    """
    Use Jinja to render financial data by replacing placeholders in the JSON
    files (fund_data.json, calc_data.json). After replacing all occurrences of
    patterns in the JSON files, this stage transforms the JSON files into Latex
    compatible files via json2latex. As a result, we can access the financial
    data that is stored in the JSON files from the Latex files.
    """
    dataDir = os.path.join(os.getenv('BUILD_DIR'), "data")
    files = [os.path.join(dataDir, "fund_data.json"),
             os.path.join(dataDir, "calc_data.json")]

    for fileName in files:
        print("File {}:".format(fileName))
        print("Processing started...")

        data = render.render_data(fileName)
        render.dump_data(data, fileName)

        print("Processing done.\n")

    cmd = "json2latex {} fundData {}".format(
            os.path.join(dataDir, "fund_data.json"),
            os.path.join(dataDir, "fund_data.tex"))
    output = subprocess.check_output(cmd, shell=True).decode('utf-8')

    cmd = "json2latex {} calcData {}".format(
            os.path.join(dataDir, "calc_data.json"),
            os.path.join(dataDir, "calc_data.tex"))
    output = subprocess.check_output(cmd, shell=True).decode('utf-8')


if __name__ == '__main__':
    args = docopt(__doc__)

    isin = args['--isin']

    prepareStage(isin)

    print("Stage 2: started...")
    executeStage(isin)
    print("Stage 2: done...\n")
