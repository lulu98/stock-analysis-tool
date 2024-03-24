import os
import logging
import json

_config = {}


def generate_default_config(isin=None):
    _config["ROOT_DIR"] = os.path.join(os.path.abspath(os.getcwd()), "..")
    _config["LOG_LEVEL"] = logging.INFO
    _config["RESOURCE_DIR"] = os.path.join(_config["ROOT_DIR"], "resources")
    _config["STOCKS_FILE"] = os.path.join(_config["RESOURCE_DIR"], "data", "stocks.json")
    _config["TEMPLATE_DIR"] = os.path.join(_config["RESOURCE_DIR"], "template")
    _config["JSON_TEMPLATE_DIR"] = os.path.join(_config["TEMPLATE_DIR"], "data")
    _config["JSON_TEMPLATE_FILE"] = os.path.join(_config["JSON_TEMPLATE_DIR"], "data.json")
    _config["LATEX_TEMPLATE_DIR"] = os.path.join(_config["TEMPLATE_DIR"], "latex")
    _config["BUILD_ROOT_DIR"] = os.path.join(_config["ROOT_DIR"], "build")

    if isin is not None:
        _config["ISIN"] = isin
        _config["BUILD_DIR"] = os.path.join(_config["BUILD_ROOT_DIR"], isin)
        _config["BUILD_DATA_DIR"] = os.path.join(_config["BUILD_DIR"], "data")
        _config["BUILD_DATA_FILE"] = os.path.join(_config["BUILD_DATA_DIR"], "data.json")
        _config["BUILD_CONFIG_DIR"] = os.path.join(_config["BUILD_DIR"], "config")
        _config["BUILD_CONFIG_FILE"] = os.path.join(_config["BUILD_CONFIG_DIR"], "config.json")

        _config["RESOURCE_DATA_DIR"] = os.path.join(_config["RESOURCE_DIR"], "data", isin)
        _config["RESOURCE_DATA_FILE"] = os.path.join(_config["RESOURCE_DATA_DIR"], "data.json")

    return _config


def get_run_config():
    return _config


def get_run_config_item(key):
    if len(_config) == 0:
        return None
    return _config[key]
