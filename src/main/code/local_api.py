"""
Retrieves basic financial data based on the company's corresponding JSON file.
"""

import os
import json

stock_data = None
isin = ""


def formatNumber(num, dec):
    """
    Format number into an appropriate format.

    Parameters:
        num (float): Number to be formatted.
        dec (int): Number of decimal points.

    Returns:
        output (str): Formatted string. In case illegal input was parsed, 0.0
                      is returned.
    """
    if dec <= 0:  # illegal input
        return "0.0"
    return ("{:." + str(dec) + "f}").format(num)


def getDataItem(query):
    """
    Get data item from JSON file.

    Parameters:
        query: Query to select specific data item from JSON file.

    Returns:
        data (str): Data item that was requested.
    """
    jsonFileName = os.getenv('JSON_FILE')
    query = query.split("/")

    global stock_data
    global isin

    # TODO: if new ISIN, read again, for now simply check if None
    if isin != os.getenv('ISIN'):
        isin = os.getenv('ISIN')
        with open(jsonFileName, "r") as f:
            stock_data = json.load(f)

    data = stock_data

    for x in query:
        if data is None:
            break
        if x not in data:
            data = None
            break
        data = data[x]

    if data is None:
        data = "null"

    return data


def pad_data(data, type_info, length, template):
    """
    Brings data into the right form (padding) for Latex template since Latex
    template is static.
    """
    if isinstance(type_info, dict):
        if data is None or data == "null":
            data = {}
        for i in range(len(data), length):
            data[str(i)] = template

    return data

# helper functions


def getYearOfDate(date):
    """
    Get year of a specific date string.

    Parameters:
        date (str): Date string in the form "<year>-<month>-<day>".

    Returns:
        year (str): The year is specified as the first part of the date string.
    """
    date = date.split("-")
    return date[0]


def getMonthOfDate(date):
    """
    Get month of a specific date string.

    Parameters:
        date (str): Date string in the form "<year>-<month>-<day>".

    Returns:
        month (str): The month is specified as the second part of the date
                     string.
    """
    date = date.split("-")
    return date[1]


def getDayOfDate(date):
    """
    Get day of a specific date string.

    Parameters:
        date (str): Date string in the form "<year>-<month>-<day>".

    Returns:
        day (str): The day is specified as the third part of the date string.
    """
    date = date.split("-")
    return date[2]


def getFinancialsDate(year):
    """
    Get date format for a specific year required to access fundamental data in
    the JSON file.

    Parameters:
        year (str): Year for which a corresponding date format should be
                    parsed.

    Returns:
        output (str): Formatted date string required to access fundamental
                      data.
    """
    query = "Financials/Balance_Sheet/yearly"
    date = list(getDataItem(query))[0]  # get the latest entry
    return "{}-{}-{}".format(year, getMonthOfDate(date), getDayOfDate(date))

###############################################################################
#                                    General                                  #
###############################################################################


query_General = "General/"


def getBaseYear():
    """
    The base year is the year of the last release of the financial statements.

    Returns:
        baseYear (int): Base year of the last release.
    """
    query = "Financials/Balance_Sheet/yearly"
    date = list(getDataItem(query))[0]  # get the latest entry
    return int(getYearOfDate(date))


def getYear(offset):
    """
    Get year based on base year and offset.

    Parameters:
        offset (int): Number of years to be added to base year.

    Returns:
        year (int): base year + offset
    """
    baseYear = getBaseYear()
    return baseYear + offset


def getCompanyCode():
    """
    Get company ID/code of a stock.

    Returns:
        companyCode (str): Company code to be used to identify a specific stock
                           by the web API.
    """
    query = query_General + "Code"
    companyCode = getDataItem(query)
    return companyCode


def getCompanyName():
    """Get company name of a stock."""
    query = query_General + "Name"
    companyName = getDataItem(query)
    return companyName


def getAddress():
    """Get address of headquarter of company."""
    query = query_General + "Address"
    address = getDataItem(query)
    return address


def getDescription():
    """Get description of company profile."""
    query = query_General + "Description"
    description = getDataItem(query)
    return description


def getISIN():
    """Get stock ISIN of company."""
    query = query_General + "ISIN"
    data = getDataItem(query)
    return data


def getIPODate():
    """Get IPO date of company."""
    query = query_General + "IPODate"
    data = getDataItem(query)
    return data


def getSector():
    """Get sector in which company operates."""
    query = query_General + "Sector"
    data = getDataItem(query)
    return data


def getIndustry():
    """Get industry in which company operates."""
    query = query_General + "Industry"
    data = getDataItem(query)
    return data


def getNumEmployees():
    """Get number of employees working for company."""
    query = query_General + "FullTimeEmployees"
    data = getDataItem(query)
    return data


def getFiscalYearEnd():
    """Get date when fiscal year ends."""
    query = query_General + "FiscalYearEnd"
    data = getDataItem(query)
    return data


def getCurrency():
    """Get currency under which the financial data is represented."""
    query = query_General + "CurrencyCode"
    data = getDataItem(query)
    return data


def getOfficers():
    """Get list of officers in charge of the company."""
    query = query_General + "Officers"
    officers = getDataItem(query)
    officers = json.dumps(officers, indent=4)
    return officers

###############################################################################
#                                    Holders                                  #
###############################################################################


query_Holders = "Holders/"


def getInstitutions():
    """Get list of institutional investors."""
    query = query_Holders + "Institutions"
    institutions = getDataItem(query)
    template = {
        "name": "-",
        "date": "-",
        "totalShares": 0.0,
        "totalAssets": 0.0,
        "currentShares": 0,
        "change": 0,
        "change_p": 0.0
    }
    institutions = pad_data(institutions, {}, 10, template)
    institutions = json.dumps(institutions, indent=4)
    return institutions


def getFunds():
    """Get list of funds invested in the stock."""
    query = query_Holders + "Funds"
    funds = getDataItem(query)
    template = {
        "name": "-",
        "date": "-",
        "totalShares": 0.0,
        "totalAssets": 0.0,
        "currentShares": 0,
        "change": 0,
        "change_p": 0.0
    }
    funds = pad_data(funds, {}, 10, template)
    funds = json.dumps(funds, indent=4)
    return funds

###############################################################################
#                               InsiderTransactions                           #
###############################################################################


def getInsiderTransactions():
    """Get list of insider transactions."""
    query = "InsiderTransactions"
    insiderTransactions = getDataItem(query)
    template = {
        "date": "-",
        "ownerCik": None,
        "ownerName": "-",
        "transactionDate": "-",
        "transactionCode": "-",
        "transactionAmount": 0,
        "transactionPrice": 0.0,
        "transactionAcquiredDisposed": "-",
        "postTransactionAmount": None,
        "secLink": "-"
    }
    insiderTransactions = pad_data(insiderTransactions, {}, 10, template)
    insiderTransactions = json.dumps(insiderTransactions, indent=4)
    return insiderTransactions

###############################################################################
#                                 Analyst Ratings                             #
###############################################################################


query_AnalystRatings = "AnalystRatings/"


def getAnalystRating():
    """Get rating of analysts."""
    query = query_AnalystRatings + "Rating"
    data = getDataItem(query)
    return data


def getAnalystTargetPrice():
    """Get target price of analysts."""
    query = query_AnalystRatings + "TargetPrice"
    data = getDataItem(query)
    if data != "null":
        data = formatNumber(float(data), 2)
    return data


def getAnalystStrongBuy():
    """Get number of "strong buy" signals from analysts."""
    query = query_AnalystRatings + "StrongBuy"
    data = getDataItem(query)
    return data


def getAnalystBuy():
    """Get number of "buy" signals from analysts."""
    query = query_AnalystRatings + "Buy"
    data = getDataItem(query)
    return data


def getAnalystHold():
    """Get number of "hold" signals from analysts."""
    query = query_AnalystRatings + "Hold"
    data = getDataItem(query)
    return data


def getAnalystSell():
    """Get number of "sell" signals from analysts."""
    query = query_AnalystRatings + "Sell"
    data = getDataItem(query)
    return data


def getAnalystStrongSell():
    """Get number of "strong sell" signals from analysts."""
    query = query_AnalystRatings + "StrongSell"
    data = getDataItem(query)
    return data

###############################################################################
#                                  Highlights                                 #
###############################################################################


query_Highlights = "Highlights/"


def getMarketCapitalization():
    """Get market capitalization of company."""
    query = query_Highlights + "MarketCapitalization"
    data = getDataItem(query)
    if data != "null":
        data = formatNumber(float(data), 2)
    return data


def getDividendShare():
    """Get dividend share of company."""
    query = query_Highlights + "DividendShare"
    data = getDataItem(query)
    if data != "null":
        data = formatNumber(float(data), 4)
    return data


def getDividendYield():
    """Get dividend yield of company."""
    query = query_Highlights + "DividendYield"
    data = getDataItem(query)
    if data != "null":
        data = formatNumber(float(data), 4)
    return data

###############################################################################
#                                 SharesStats                                 #
###############################################################################


query_SharesStats = "SharesStats/"


def getSharesOutstanding():
    """Get number of shares outstanding."""
    query = query_SharesStats + "SharesOutstanding"
    data = getDataItem(query)
    return data


def getSharesFloat():
    """Get number of shares floating."""
    query = query_SharesStats + "SharesFloat"
    data = getDataItem(query)
    return data


def getSharesPercentInsiders():
    """Get percentage of shares owned by insiders."""
    query = query_SharesStats + "PercentInsiders"
    data = getDataItem(query)
    if data != "null":
        data = formatNumber(float(data), 4)
    return data


def getSharesPercentInstitutions():
    """Get percentage of shares owned by institutions."""
    query = query_SharesStats + "PercentInstitutions"
    data = getDataItem(query)
    if data != "null":
        data = formatNumber(float(data), 4)
    return data


def getSharesPercentPublic():
    """Get percentage of shares owned by the public."""
    percentInsiders = getSharesPercentInsiders()
    percentInsiders = (0.0
                       if percentInsiders == "null"
                       else float(percentInsiders))

    percentInstitutions = getSharesPercentInstitutions()
    percentInstitutions = (0.0
                           if percentInstitutions == "null"
                           else float(percentInstitutions))

    percentPublic = 100.00 - (percentInsiders + percentInstitutions)
    return formatNumber(float(percentPublic), 4)

###############################################################################
#                                  Technicals                                 #
###############################################################################


query_Technicals = "Technicals/"


def get50DayMA():
    """Get 50 Day Moving Average of stock."""
    query = query_Technicals + "50DayMA"
    data = getDataItem(query)
    if data != "null":
        data = formatNumber(float(data), 2)
    return data

###############################################################################
#                                 Balance Sheet                               #
###############################################################################


query_BalanceSheet = "Financials/Balance_Sheet/yearly/"


def getInventory(year):
    """Get Inventory of stock."""
    query = query_BalanceSheet + "{}/inventory".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "null":
        data = formatNumber(float(data), 2)
    return data


def getAccountsReceivables(year):
    """Get Accounts Receivables."""
    query = query_BalanceSheet + "{}/netReceivables".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "null":
        data = formatNumber(float(data), 2)
    return data


def getAccountsPayable(year):
    """Get Accounts Payable."""
    query = query_BalanceSheet + "{}/accountsPayable".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "null":
        data = formatNumber(float(data), 2)
    return data


def getCurrentLiabilities(year):
    """Get Current Liabilities."""
    query = query_BalanceSheet + "{}/totalCurrentLiabilities".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "null":
        data = formatNumber(float(data), 2)
    return data


def getNonCurrentLiabilities(year):
    """Get Noncurrent Liabilities."""
    query = query_BalanceSheet + "{}/nonCurrentLiabilitiesTotal".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "null":
        data = formatNumber(float(data), 2)
    return data


def getTotalLiabilities(year):
    """
    Get Total Liabilities.

    Total Liabilities = Current Liabilities + Noncurrent Liabilities
    """
    currentLiabilities = getCurrentLiabilities(year)
    currentLiabilities = (0.0
                          if currentLiabilities == "null"
                          else float(currentLiabilities))

    nonCurrentLiabilities = getNonCurrentLiabilities(year)
    nonCurrentLiabilities = (0.0
                             if nonCurrentLiabilities == "null"
                             else float(nonCurrentLiabilities))

    totalLiabilities = float(currentLiabilities) + float(nonCurrentLiabilities)
    return formatNumber(float(totalLiabilities), 2)


def getLiabilitiesAndEquity(year):
    """Get Liabilities and Equity."""
    query = query_BalanceSheet + "{}/liabilitiesAndStockholdersEquity".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "null":
        data = formatNumber(float(data), 2)
    return data


def getTotalEquity(year):
    """Get Total Equity."""
    liabilitiesAndEquity = getLiabilitiesAndEquity(year)
    liabilitiesAndEquity = (0.0
                            if liabilitiesAndEquity == "null"
                            else float(liabilitiesAndEquity))

    totalLiabilities = float(getTotalLiabilities(year))
    totalLiabilities = (0.0
                        if totalLiabilities == "null"
                        else float(totalLiabilities))

    totalEquity = liabilitiesAndEquity - totalLiabilities
    return formatNumber(float(totalEquity), 2)


def getCurrentAssets(year):
    """Get Current Assets."""
    query = query_BalanceSheet + "{}/totalCurrentAssets".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "null":
        data = formatNumber(float(data), 2)
    return data


def getNonCurrentAssets(year):
    """Get Noncurrent Assets."""
    query = query_BalanceSheet + "{}/nonCurrentAssetsTotal".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "null":
        data = formatNumber(float(data), 2)
    return data


def getTotalAssets(year):
    """Get Total Assets: Current Assets + Noncurrent Assets"""
    currentAssets = getCurrentAssets(year)
    currentAssets = (0.0
                     if currentAssets == "null"
                     else float(currentAssets))

    nonCurrentAssets = getNonCurrentAssets(year)
    nonCurrentAssets = (0.0
                        if nonCurrentAssets == "null"
                        else float(nonCurrentAssets))

    totalAssets = currentAssets + nonCurrentAssets
    return formatNumber(float(totalAssets), 2)


def getShortTermDebt(year):
    """Get Short-Term Debt."""
    query = query_BalanceSheet + "{}/shortTermDebt".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "null":
        data = formatNumber(float(data), 2)
    return data


def getLongTermDebt(year):
    """Get Long-Term Debt."""
    query = query_BalanceSheet + "{}/longTermDebt".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "null":
        data = formatNumber(float(data), 2)
    return data


def getTotalDebt(year):
    """Get Total Debt: Short-Term Debt + Long-Term Debt"""
    shortTermDebt = getShortTermDebt(year)
    shortTermDebt = 0.0 if shortTermDebt == "null" else float(shortTermDebt)

    longTermDebt = getLongTermDebt(year)
    longTermDebt = 0.0 if longTermDebt == "null" else float(longTermDebt)

    totalDebt = shortTermDebt + longTermDebt
    return formatNumber(float(totalDebt), 2)


def getInvestedCapital(year):
    """Get Invested Capital: Debt + Equity"""
    debt = getTotalDebt(year)
    debt = 0.0 if debt == "null" else float(debt)

    equity = getTotalEquity(year)
    equity = 0.0 if equity == "null" else float(equity)

    investedCapital = debt + equity
    return formatNumber(float(investedCapital), 2)


def getCommonSharesOutstanding(year):
    """Get number of oustanding shares."""
    query = query_BalanceSheet + "{}/commonStockSharesOutstanding".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "null":
        data = formatNumber(float(data), 2)
    return data


def getEarningsPerShare(year):
    """Get Earnings Per Shares (EPS): Earnings / Shares"""
    earnings = getNetIncome(year)
    earnings = 0.0 if earnings == "null" else float(earnings)

    sharesOutstanding = getCommonSharesOutstanding(year)
    sharesOutstanding = (0.0
                         if sharesOutstanding == "null"
                         else float(sharesOutstanding))

    earningsPerShare = (0.0
                        if sharesOutstanding == 0.0
                        else earnings / sharesOutstanding)
    return formatNumber(float(earningsPerShare), 4)


def getBookValuePerShare(year):
    """Get Book Value Per Share (BVPS): Equity / Shares"""
    equity = getTotalEquity(year)
    equity = 0.0 if equity == "null" else float(equity)

    shares = getCommonSharesOutstanding(year)
    shares = 0.0 if shares == "null" else float(shares)

    bookValuePerShare = 0.0 if shares == 0.0 else equity / shares
    return formatNumber(float(bookValuePerShare), 4)

###############################################################################
#                               Income Statement                              #
###############################################################################


query_IncomeStatement = "Financials/Income_Statement/yearly/"


def getNetIncome(year):
    """Get Net Income."""
    query = query_IncomeStatement + "{}/netIncome".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "null":
        data = formatNumber(float(data), 2)
    return data


def getRevenue(year):
    """Get Revenue."""
    query = query_IncomeStatement + "{}/totalRevenue".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "null":
        data = formatNumber(float(data), 2)
    return data


def getEBITDA(year):
    """Get EBITDA."""
    query = query_IncomeStatement + "{}/ebitda".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "null":
        data = formatNumber(float(data), 2)
    return data


def getGrossProfit(year):
    """Get Gross Profit."""
    query = query_IncomeStatement + "{}/grossProfit".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "null":
        data = formatNumber(float(data), 2)
    return data


def getOperatingIncome(year):
    """Get Operating Income."""
    query = query_IncomeStatement + "{}/operatingIncome".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "null":
        data = formatNumber(float(data), 2)
    return data


def getInterestExpense(year):
    """Get Interest Expense."""
    query = query_IncomeStatement + "{}/interestExpense".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "null":
        data = formatNumber(float(data), 2)
    return data


def getCostOfRevenue(year):
    """Get Cost Of Revenue."""
    query = query_IncomeStatement + "{}/costOfRevenue".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "null":
        data = formatNumber(float(data), 2)
    return data

###############################################################################
#                            Cash Flow Statement                              #
###############################################################################


query_CashFlow = "Financials/Cash_Flow/yearly/"


def getOperatingCashFlow(year):
    """Get Operating Cash Flow (OCF)."""
    query = query_CashFlow + "{}/totalCashFromOperatingActivities".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "null":
        data = formatNumber(float(data), 2)
    return data


def getInvestingCashFlow(year):
    """Get Investing Cash Flow (ICF)."""
    query = query_CashFlow + "{}/totalCashflowsFromInvestingActivities".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "null":
        data = formatNumber(float(data), 2)
    return data


def getCapitalExpenditures(year):
    """Get Capital Expenditures."""
    query = query_CashFlow + "{}/capitalExpenditures".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "null":
        data = formatNumber(float(data), 2)
    return data


def getFreeCashFlow(year):
    """Get Free Cash Flow (FCF)."""
    query = query_CashFlow + "{}/freeCashFlow".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "null":
        data = formatNumber(float(data), 2)
    return data
