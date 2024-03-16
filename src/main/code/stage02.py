#!/usr/bin/env python3

"""Pipeline - Stage 2

Description:

Finds patterns in the JSON data templates and replaces the pattern with a
corresponding value from the local API.

Usage:
    stage02.py [-h] -i <isin> [--latex]

Options:
    -h, --help                  Show help menu.
    -i <isin>, --isin <isin>    ISIN of stock.
    --latex                     Generate Latex structure for PDF.
"""
from docopt import docopt

import os
import sys
import subprocess
import json
import shutil
import argparse
import filecmp
import logging

import render

args = docopt(__doc__)
logging.basicConfig(level=logging.INFO)


def set_env_vars(isin):
    """
    Sets environment variables required by stage 2.
    """
    root_dir = os.path.join(os.path.abspath(os.getcwd()), "..")

    template_dir = os.path.join(root_dir, "resources", "template")
    json_template_dir = os.path.join(template_dir, "data")
    latex_template_dir = os.path.join(template_dir, "latex")
    data_dir = os.path.join(root_dir, "resources", "data", isin)
    build_dir = os.path.join(root_dir, "build", isin)

    json_file = os.path.join(build_dir, "data", "data.json")

    os.environ['ROOT_DIR'] = root_dir
    os.environ['DATA_DIR'] = data_dir
    os.environ['JSON_TEMPLATE_DIR'] = json_template_dir
    os.environ['LATEX_TEMPLATE_DIR'] = latex_template_dir
    os.environ['BUILD_DIR'] = build_dir
    os.environ['JSON_FILE'] = json_file


def is_stage01_done():
    data_dir = os.getenv('DATA_DIR')
    return os.path.exists(data_dir)


def is_build_dir_exists():
    """Returns if build directory exists."""
    build_dir = os.getenv('BUILD_DIR')
    return os.path.exists(build_dir)


def setup_build_dir(src_file, dst_file):
    """Sets up build directory."""
    build_dir = os.getenv('BUILD_DIR')
    json_template_dir = os.getenv('JSON_TEMPLATE_DIR')
    latex_template_dir = os.getenv('LATEX_TEMPLATE_DIR')

    logging.info("Initial directory setup started...")
    os.makedirs(build_dir)
    shutil.copytree(
            json_template_dir,
            os.path.join(build_dir, "data"),
            dirs_exist_ok=True)
    shutil.copyfile(src_file, dst_file)
    if args['--latex']:
        shutil.copytree(
                latex_template_dir,
                build_dir,
                dirs_exist_ok=True)
    logging.info("Initial directory setup done.")


def check_and_init_build_dir(src_file, dst_file):
    """Set up build directory once initially."""
    if not is_build_dir_exists():
        setup_build_dir(src_file, dst_file)


def prepare_build_dir(isin):
    """Prepare build directory for stage 2 execution."""
    json_src = os.path.join(os.getenv('DATA_DIR'), "data.json")
    json_dst = os.getenv('JSON_FILE')

    if not is_stage01_done():
        logging.critical(
                "Data for company {} not available."
                "Execute stage 1 first.".format(isin))
        sys.exit(1)

    check_and_init_build_dir(json_src, json_dst)


def prepare_stage(isin):
    """
    Prepares stage 2 of the stock analysis pipeline.

    Parameters:
        isin (str): ISIN of the stock to be analysed.
    """
    set_env_vars(isin)
    prepare_build_dir(isin)


def execute_stage(isin):
    """
    Use Jinja to render financial data by replacing placeholders in the JSON
    files (fund_data.json, calc_data.json). After replacing all occurrences of
    patterns in the JSON files, this stage transforms the JSON files into Latex
    compatible files via json2latex. As a result, we can access the financial
    data that is stored in the JSON files from the Latex files.
    """
    data_dir = os.path.join(os.getenv('BUILD_DIR'), "data")
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


if __name__ == '__main__':

    isin = args['--isin']

    logging.info("Stage 2: started...")
    prepare_stage(isin)
    execute_stage(isin)
    logging.info("Stage 2: done...\n")
