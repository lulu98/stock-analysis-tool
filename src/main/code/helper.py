import config
import logging
from web_api import *


def triggerSearchAPI(api_key, isin):
    """
    Trigger Search API for ISIN and format output as feedback for the user.
    """
    logging.info("Output of Search API for ISIN {}:\n".format(isin))
    searchData = searchAPI_getData(api_key, isin)
    logging.info("{: <20} {: <20} {: <20}".format(
        "Country",
        "Code",
        "Exchange"))
    for entry in searchData:
        logging.info("{: <20} {: <20} {: <20}".format(
            entry["Country"],
            entry["Code"],
            entry["Exchange"]))
    logging.info("\n")


def get_api_params(api_key=None, isin=None):
    run_conf = config.get_run_config()
    stocks_file = run_conf["STOCKS_FILE"]

    with open(stocks_file, "r") as f:
        data = json.load(f)

    if isin is None:
        api_params = data
    else:
        if isin not in data:
            logging.critical("No data for company with ISIN {}. Put required info in {}.".format(isin, stocks_file))
            if api_key:
                triggerSearchAPI(api_key, isin)
                logging.critical("Add entry for {} in {} before continuing...".format(
                    isin,
                    stocks_file))
            sys.exit(1)

        api_params = {}
        api_params[isin] = data[isin]

    return api_params
