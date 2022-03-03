#!/usr/bin/env python3

"""
Retrieves basic financial data based on the company's corresponding JSON file.
"""

import os
import json

def formatNumber(num, dec):
    return ("{:." + str(dec) + "f}").format(num)

def formatUnit(num, unit):
    if unit == "i": return num
    if unit == "t": return float(num)/1e3
    if unit == "m": return float(num)/1e6
    if unit == "b": return float(num)/1e9

def getDataItem(query):
    jsonFileName = os.getenv('JSON_FILE')
    query = query.split("/")

    with open(jsonFileName, "r") as f:
        data = json.load(f)

    for x in query:
        if data is None:
            break
        if x not in data:
            data = None
            break
        data = data[x]

    if data is None:
        data = "-"

    return data

# helper functions

def getYearOfDate(date):
    date = date.split("-")
    return date[0]

def getMonthOfDate(date):
    date = date.split("-")
    return date[1]

def getDayOfDate(date):
    date = date.split("-")
    return date[2]

def getFinancialsDate(year):
    query = "Financials/Balance_Sheet/yearly" # we could also use the Income or Cash Flow Statement
    date = list(getDataItem(query))[0] # get the latest entry
    return "{}-{}-{}".format(year, getMonthOfDate(date), getDayOfDate(date))

################################################################################
###################################  General ###################################
################################################################################

query_General = "General/"

def getBaseYear():
    '''
    The base year is the year of the last release of the financial statements.
    '''
    query = "Financials/Balance_Sheet/yearly" # we could also use the Income or Cash Flow Statement
    date = list(getDataItem(query))[0] # get the latest entry
    return int(getYearOfDate(date))

def getYear(offset):
    baseYear = getBaseYear()
    return baseYear + offset

def getCompanyCode():
    query = query_General + "Code"
    companyCode = getDataItem(query)
    return companyCode

def getCompanyName():
    query = query_General + "Name"
    companyName = str(getDataItem(query))
    companyName = companyName.replace("&", "\\\\\&")
    return companyName

def getAddress():
    query = query_General + "Address"
    address = str(getDataItem(query))
    address = address.replace("&", "\\\\\&")
    address = address.replace("'", "")
    return address

def getDescription():
    query = query_General + "Description"
    description = str(getDataItem(query))
    description = description.replace("&", "\\\\\&")
    description = description.replace("/", "\\/")
    description = description.replace("'", "")
    return description

def getISIN():
    query = query_General + "ISIN"
    data = getDataItem(query)
    return data

def getIPODate():
    query = query_General + "IPODate"
    data = getDataItem(query)
    return data

def getSector():
    query = query_General + "Sector"
    data = getDataItem(query)
    return data

def getIndustry():
    query = query_General + "Industry"
    data = getDataItem(query)
    return data

def getNumEmployees():
    query = query_General + "FullTimeEmployees"
    data = getDataItem(query)
    return data

def getFiscalYearEnd():
    query = query_General + "FiscalYearEnd"
    data = getDataItem(query)
    return data

def getCurrency():
    query = query_General + "CurrencyCode"
    data = getDataItem(query)
    return data

def getOfficers():
    subjectLine = ["Title", "Name"]
    officerData = []
   
    query = query_General + "Officers"
    officers = getDataItem(query)

    if officers == "-":
        return [subjectLine, officerData]

    for key in officers:
        entry = [officers[key]["Title"],
                 officers[key]["Name"]]
        officerData.append(entry)
    return [subjectLine, officerData]

################################################################################
###################################  Holders  ##################################
################################################################################

query_Holders = "Holders/"

def getInstitutions():
    subjectLine = ["Name", "Total Shares", "Change", "Total Assets"]
    institutionsData = []
    
    query = query_Holders + "Institutions"
    institutions = getDataItem(query)

    if institutions == "-":
        return [subjectLine, institutionsData]

    for key in institutions:
        entry = [institutions[key]["name"],
                 institutions[key]["totalShares"],
                 institutions[key]["change_p"],
                 institutions[key]["totalAssets"]
                ]
        institutionsData.append(entry)
    return [subjectLine, institutionsData]

def getFunds():
    subjectLine = ["Name", "Total Shares", "Change", "Total Assets"]
    fundsData = []
    
    query = query_Holders + "Funds"
    funds = getDataItem(query)

    if funds == "-":
        return [subjectLine, fundsData]

    for key in funds:
        entry = [funds[key]["name"],
                 funds[key]["totalShares"],
                 funds[key]["change_p"],
                 funds[key]["totalAssets"]
                ]
        fundsData.append(entry)
    return [subjectLine, fundsData]


################################################################################
##############################  InsiderTransactions  ###########################
################################################################################

def getInsiderTransactions():
    subjectLine = ["Name", "Date", "Amount", "Price", "(A)cquired or (D)isposed"]
    insiderData = []
    
    query = "InsiderTransactions"
    insiderTransactions = getDataItem(query)

    if insiderTransactions == "-":
        return [subjectLine, insiderData]

    for key in insiderTransactions:
        entry = [insiderTransactions[key]["ownerName"],
                 insiderTransactions[key]["transactionDate"],
                 insiderTransactions[key]["transactionAmount"],
                 insiderTransactions[key]["transactionPrice"],
                 insiderTransactions[key]["transactionAcquiredDisposed"]
                ]
        insiderData.append(entry)
    return [subjectLine, insiderData]

################################################################################
################################  Analyst Ratings ##############################
################################################################################

query_AnalystRatings = "AnalystRatings/"

def getAnalystRating():
    query = query_AnalystRatings + "Rating"
    data = getDataItem(query)
    return data

def getAnalystTargetPrice():
    query = query_AnalystRatings + "TargetPrice"
    data = getDataItem(query)
    if data != "-":
        data = formatNumber(float(data), 2)
    return data

def getAnalystStrongBuy():
    query = query_AnalystRatings + "StrongBuy"
    data = getDataItem(query)
    return data

def getAnalystBuy():
    query = query_AnalystRatings + "Buy"
    data = getDataItem(query)
    return data

def getAnalystHold():
    query = query_AnalystRatings + "Hold"
    data = getDataItem(query)
    return data

def getAnalystSell():
    query = query_AnalystRatings + "Sell"
    data = getDataItem(query)
    return data

def getAnalystStrongSell():
    query = query_AnalystRatings + "StrongSell"
    data = getDataItem(query)
    return data

################################################################################
#################################  Highlights  #################################
################################################################################

query_Highlights = "Highlights/"

def getMarketCapitalization():
    '''
    :param units: {identity, thousands, millions, billions}
    '''
    query = query_Highlights + "MarketCapitalization"
    data = getDataItem(query)
    if data != "-":
        data = formatNumber(float(data), 2)
    return data

def getDividendShare():
    query = query_Highlights + "DividendShare"
    data = getDataItem(query)
    if data != "-":
        data = formatNumber(float(data), 4)
    return data

def getDividendYield():
    query = query_Highlights + "DividendYield"
    data = getDataItem(query)
    if data != "-":
        data = formatNumber(float(data), 4)
    return data

################################################################################
################################  SharesStats  #################################
################################################################################

query_SharesStats = "SharesStats/"

def getSharesOutstanding():
    query = query_SharesStats + "SharesOutstanding"
    data = getDataItem(query)
    return data

def getSharesFloat():
    query = query_SharesStats + "SharesFloat"
    data = getDataItem(query)
    return data

def getSharesPercentInsiders():
    query = query_SharesStats + "PercentInsiders"
    data = getDataItem(query)
    if data != "-":
        data = formatNumber(float(data), 4)
    return data 

def getSharesPercentInstitutions():
    query = query_SharesStats + "PercentInstitutions"
    data = getDataItem(query)
    if data != "-":
        data = formatNumber(float(data), 4)
    return data

def getSharesPercentPublic():
    percentInsiders = getSharesPercentInsiders()
    percentInsiders = 0.0 if percentInsiders == "-" else float(percentInsiders)
    
    percentInstitutions = getSharesPercentInstitutions()
    percentInstitutions = 0.0 if percentInstitutions == "-" else float(percentInstitutions)

    percentPublic = 100.00 - (percentInsiders + percentInstitutions)
    return formatNumber(float(percentPublic), 4)

################################################################################
#################################  Technicals  #################################
################################################################################

query_Technicals = "Technicals/"

def get50DayMA():
    query = query_Technicals + "50DayMA"
    data = getDataItem(query)
    if data != "-":
        data = formatNumber(float(data), 2)
    return data

################################################################################
################################  Balance Sheet  ###############################
################################################################################

query_BalanceSheet = "Financials/Balance_Sheet/yearly/"

def getInventory(year):
    query = query_BalanceSheet + "{}/inventory".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "-":
        data = formatNumber(float(data), 2)
    return data

def getAccountsReceivables(year):
    query = query_BalanceSheet + "{}/netReceivables".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "-":
        data = formatNumber(float(data), 2)
    return data

def getAccountsPayable(year):
    query = query_BalanceSheet + "{}/accountsPayable".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "-":
        data = formatNumber(float(data), 2)
    return data

def getCurrentLiabilities(year):
    query = query_BalanceSheet + "{}/totalCurrentLiabilities".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "-":
        data = formatNumber(float(data), 2)
    return data

def getNonCurrentLiabilities(year):
    query = query_BalanceSheet + "{}/nonCurrentLiabilitiesTotal".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "-":
        data = formatNumber(float(data), 2)
    return data

def getTotalLiabilities(year):
    currentLiabilities = getCurrentLiabilities(year)
    currentLiabilities = 0.0 if currentLiabilities == "-" else float(currentLiabilities)

    nonCurrentLiabilities = getNonCurrentLiabilities(year)
    nonCurrentLiabilities = 0.0 if nonCurrentLiabilities == "-" else float(nonCurrentLiabilities)

    totalLiabilities = float(currentLiabilities) + float(nonCurrentLiabilities)
    return formatNumber(float(totalLiabilities), 2)

def getLiabilitiesAndEquity(year):
    query = query_BalanceSheet + "{}/liabilitiesAndStockholdersEquity".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "-":
        data = formatNumber(float(data), 2)
    return data

def getTotalEquity(year):
    liabilitiesAndEquity = getLiabilitiesAndEquity(year)
    liabilitiesAndEquity = 0.0 if liabilitiesAndEquity == "-" else float(liabilitiesAndEquity)

    totalLiabilities = float(getTotalLiabilities(year))
    totalLiabilities = 0.0 if totalLiabilities == "-" else float(totalLiabilities)

    totalEquity = liabilitiesAndEquity - totalLiabilities
    return formatNumber(float(totalEquity), 2)

def getCurrentAssets(year):
    query = query_BalanceSheet + "{}/totalCurrentAssets".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "-":
        data = formatNumber(float(data), 2)
    return data

def getNonCurrentAssets(year):
    query = query_BalanceSheet + "{}/nonCurrentAssetsTotal".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "-":
        data = formatNumber(float(data), 2)
    return data

def getTotalAssets(year):
    currentAssets = getCurrentAssets(year)
    currentAssets = 0.0 if currentAssets == "-" else float(currentAssets)

    nonCurrentAssets = getNonCurrentAssets(year)
    nonCurrentAssets = 0.0 if nonCurrentAssets == "-" else float(nonCurrentAssets)

    totalAssets = currentAssets + nonCurrentAssets
    return formatNumber(float(totalAssets), 2)

def getShortTermDebt(year):
    query = query_BalanceSheet + "{}/shortTermDebt".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "-":
        data = formatNumber(float(data), 2)
    return data

def getLongTermDebt(year):
    query = query_BalanceSheet + "{}/longTermDebt".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "-":
        data = formatNumber(float(data), 2)
    return data

def getTotalDebt(year):
    shortTermDebt = getShortTermDebt(year)
    shortTermDebt = 0.0 if shortTermDebt == "-" else float(shortTermDebt)

    longTermDebt = getLongTermDebt(year)
    longTermDebt = 0.0 if longTermDebt == "-" else float(longTermDebt)

    totalDebt = shortTermDebt + longTermDebt
    return formatNumber(float(totalDebt), 2)

def getInvestedCapital(year):
    debt = getTotalDebt(year)
    debt = 0.0 if debt == "-" else float(debt)

    equity = getTotalEquity(year)
    equity = 0.0 if equity == "-" else float(equity)

    investedCapital = debt + equity
    return formatNumber(float(investedCapital), 2)

def getCommonSharesOutstanding(year):
    query = query_BalanceSheet + "{}/commonStockSharesOutstanding".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "-":
        data = formatNumber(float(data), 2)
    return data

def getEarningsPerShare(year):
    earnings = getNetIncome(year)
    earnings = 0.0 if earnings == "-" else float(earnings)

    sharesOutstanding = getCommonSharesOutstanding(year)
    sharesOutstanding = 0.0 if sharesOutstanding == "-" else float(sharesOutstanding)

    earningsPerShare = 0.0 if sharesOutstanding == 0.0 else earnings / sharesOutstanding
    return formatNumber(float(earningsPerShare), 4)

def getBookValuePerShare(year):
    equity = getTotalEquity(year)
    equity = 0.0 if equity == "-" else float(equity)

    shares = getCommonSharesOutstanding(year)
    shares = 0.0 if shares == "-" else float(shares)

    bookValuePerShare = 0.0 if shares == 0.0 else equity / shares
    return formatNumber(float(bookValuePerShare), 4)

################################################################################
##############################  Income Statement  ##############################
################################################################################

query_IncomeStatement = "Financials/Income_Statement/yearly/"

def getNetIncome(year):
    query = query_IncomeStatement + "{}/netIncome".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "-":
        data = formatNumber(float(data), 2)
    return data

def getRevenue(year):
    query = query_IncomeStatement + "{}/totalRevenue".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "-":
        data = formatNumber(float(data), 2)
    return data

def getEBITDA(year):
    query = query_IncomeStatement + "{}/ebitda".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "-":
        data = formatNumber(float(data), 2)
    return data

def getGrossProfit(year):
    query = query_IncomeStatement + "{}/grossProfit".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "-":
        data = formatNumber(float(data), 2)
    return data

def getOperatingIncome(year):
    query = query_IncomeStatement + "{}/operatingIncome".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "-":
        data = formatNumber(float(data), 2)
    return data

def getInterestExpense(year):
    query = query_IncomeStatement + "{}/interestExpense".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "-":
        data = formatNumber(float(data), 2)
    return data

def getCostOfRevenue(year):
    query = query_IncomeStatement + "{}/costOfRevenue".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "-":
        data = formatNumber(float(data), 2)
    return data

################################################################################
###########################  Cash Flow Statement  ##############################
################################################################################

query_CashFlow = "Financials/Cash_Flow/yearly/"

def getOperatingCashFlow(year):
    query = query_CashFlow + "{}/totalCashFromOperatingActivities".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "-":
        data = formatNumber(float(data), 2)
    return data

def getInvestingCashFlow(year):
    query = query_CashFlow + "{}/totalCashflowsFromInvestingActivities".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "-":
        data = formatNumber(float(data), 2)
    return data

def getCapitalExpenditures(year):
    query = query_CashFlow + "{}/capitalExpenditures".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "-":
        data = formatNumber(float(data), 2)
    return data

def getFreeCashFlow(year):
    query = query_CashFlow + "{}/freeCashFlow".format(getFinancialsDate(year))
    data = getDataItem(query)
    if data != "-":
        data = formatNumber(float(data), 2)
    return data
