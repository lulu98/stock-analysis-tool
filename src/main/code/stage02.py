#!/usr/bin/env python3

"""Pipeline - Stage 2

Description:

Finds patterns in the JSON data templates and replaces the pattern with a
corresponding value from the local API.

Usage:
    stage02.py [-h] [-i <isin>] [--latex] [--clean] [--clean-all]

Options:
    -h, --help                  Show help menu.
    -i <isin>, --isin <isin>    ISIN of stock.
    --latex                     Generate Latex structure for PDF.
    --clean                     Clean up directories.
    --clean-all                 Clean up all directories.
"""
from docopt import docopt

import argparse
import filecmp
import json
import logging
import os
import shutil
import subprocess
import sys

import config
import helper
import render

args = docopt(__doc__)


def init_stage02(isin):
    # generate default config
    run_conf = config.generate_default_config(isin)

    # set log level
    logging.basicConfig(level=run_conf["LOG_LEVEL"])

    if args['--clean-all']:
        # clean up all directories
        for root, dirs, files in os.walk(run_conf["BUILD_ROOT_DIR"]):
            for d in dirs:
                logging.info("Deleting {}".format(os.path.join(root, d)))
                shutil.rmtree(os.path.join(root, d))
        sys.exit(0)

    if isin:
        # set env vars - TODO: remove this at some point
        os.environ['JSON_FILE'] = run_conf["BUILD_DATA_FILE"]
        os.environ['ISIN'] = run_conf["ISIN"]

        if args['--clean']:
            # clean up directories
            if os.path.exists(run_conf["BUILD_DIR"]):
                logging.info("Deleting {}".format(run_conf["BUILD_DIR"]))
                shutil.rmtree(run_conf["BUILD_DIR"])
            sys.exit(0)
        else:
            # sanity checks
            if not os.path.exists(run_conf["RESOURCE_DATA_FILE"]):
                logging.critical("{} not detected. Execute stage01 for ISIN {} first!".format(run_conf["RESOURCE_DATA_FILE"], isin))
                sys.exit(-1)

            # create default directories
            logging.info("Initial directory setup started...")

            if not os.path.exists(run_conf["BUILD_DIR"]):
                os.makedirs(run_conf["BUILD_DIR"])
            if not os.path.exists(run_conf["BUILD_DATA_DIR"]):
                os.makedirs(run_conf["BUILD_DATA_DIR"])
            if not os.path.exists(run_conf["BUILD_CONFIG_DIR"]):
                os.makedirs(run_conf["BUILD_CONFIG_DIR"])

            # fill directory with content
            if not os.path.exists(run_conf["BUILD_CONFIG_FILE"]):
                with open(run_conf["BUILD_CONFIG_FILE"], "w") as f:
                    f.write(json.dumps(run_conf, indent=4))
            shutil.copytree(
                run_conf["JSON_TEMPLATE_DIR"],
                run_conf["BUILD_DATA_DIR"],
                dirs_exist_ok=True)
            shutil.copyfile(
                run_conf["RESOURCE_DATA_FILE"],
                run_conf["BUILD_DATA_FILE"])
            if args['--latex']:
                shutil.copytree(
                    run_conf["LATEX_TEMPLATE_DIR"],
                    run_conf["BUILD_DIR"],
                    dirs_exist_ok=True)

            logging.info("Initial directory setup done.")


def generate_data(isin):
    """
    Use Jinja to render financial data by replacing placeholders in the JSON
    files (fund_data.json, calc_data.json). After replacing all occurrences of
    patterns in the JSON files, this stage transforms the JSON files into Latex
    compatible files via json2latex. As a result, we can access the financial
    data that is stored in the JSON files from the Latex files.
    """
    run_conf = config.get_run_config()
    data_dir = run_conf["BUILD_DATA_DIR"]
    files = [os.path.join(data_dir, "fund_data.json"),
             os.path.join(data_dir, "calc_data.json")]

    for fileName in files:
        logging.info("File {}:".format(fileName))
        logging.info("Processing started...")

        data = render.render_data(fileName)
        render.dump_data(data, fileName)

        logging.info("Processing done.\n")

    if args['--latex']:
        cmd = "json2latex {} fundData {}".format(
            os.path.join(data_dir, "fund_data.json"),
            os.path.join(data_dir, "fund_data.tex"))
        output = subprocess.check_output(cmd, shell=True).decode('utf-8')

        cmd = "json2latex {} calcData {}".format(
            os.path.join(data_dir, "calc_data.json"),
            os.path.join(data_dir, "calc_data.tex"))
        output = subprocess.check_output(cmd, shell=True).decode('utf-8')


def exec_stage02(isin):
    api_params = helper.get_api_params(isin=isin)

    for isin in api_params:
        init_stage02(isin)
        generate_data(isin)


if __name__ == '__main__':

    isin = args['--isin']

    init_stage02(isin)
    logging.info("Stage 2: started...")
    exec_stage02(isin)
    logging.info("Stage 2: done...\n")
