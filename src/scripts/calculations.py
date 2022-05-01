#!/usr/bin/env python3

"""
Includes functions that construct meaningful financial information based on the
local API.
"""

from scripts.local_api import *

################################################################################
##############################  Financial Ratios  ##############################
################################################################################

def getSharesFloatToOutstandingRatio():
    """Shares-Floating-To-Outstanding Ratio = Floating / Outstanding"""
    sharesFloat = getSharesFloat()
    sharesFloat = 0.0 if sharesFloat == "-" else float(sharesFloat)

    sharesOutstanding = getSharesOutstanding()
    sharesOutstanding = 0.0 if sharesOutstanding == "-" else float(sharesOutstanding)

    if sharesOutstanding == 0.0: return "-"

    return formatNumber(sharesFloat / sharesOutstanding, 4)

def debtToEquity(year):
    """Debt-to-Equity Ratio (D/E) = Debt / Equity"""
    totalDebt = getTotalDebt(year)
    totalDebt = 0.0 if totalDebt == "-" else float(totalDebt)

    totalEquity = getTotalEquity(year)
    totalEquity = 0.0 if totalEquity == "-" else float(totalEquity)

    if totalEquity == 0.0: return "-"

    return formatNumber(totalDebt / totalEquity, 4)

def debtToFCF(year):
    """Debt-to-FCF Ratio (D/FCF) = Debt / FCF"""
    totalDebt = getTotalDebt(year)
    totalDebt = 0.0 if totalDebt == "-" else float(totalDebt)

    freeCashFlow = getFreeCashFlow(year)
    freeCashFlow = 0.0 if freeCashFlow == "-" else float(freeCashFlow)

    if freeCashFlow == 0.0: return "-"

    return formatNumber(totalDebt / freeCashFlow, 4)

def liabilitiesToEquity(year):
    """Liabilities-to-Equity Ratio (L/E) = Liabilities / Equity"""
    totalLiabilities = getTotalLiabilities(year)
    totalLiabilities = 0.0 if totalLiabilities == "-" else float(totalLiabilities)

    totalEquity = getTotalEquity(year)
    totalEquity = 0.0 if totalEquity == "-" else float(totalEquity)

    if totalEquity == 0.0: return "-"

    return formatNumber(totalLiabilities / totalEquity, 4)

def currentRatio(year):
    """Current Ratio (CR) = Current Assets / Current Liabilities"""
    totalCurrentAssets = getCurrentAssets(year)
    totalCurrentAssets = 0.0 if totalCurrentAssets == "-" else float(totalCurrentAssets)

    totalCurrentLiabilities = getCurrentLiabilities(year)
    totalCurrentLiabilities = 0.0 if totalCurrentLiabilities == "-" else float(totalCurrentLiabilities)

    if totalCurrentLiabilities == 0.0: return "-"

    return formatNumber(totalCurrentAssets / totalCurrentLiabilities, 4)

def acidTestRatio(year):
    """Acid Test Ratio (ATR) = (Current Assets - Inventory) / Current Liabilities"""
    totalCurrentAssets = getCurrentAssets(year)
    totalCurrentAssets = 0.0 if totalCurrentAssets == "-" else float(totalCurrentAssets)

    inventory = getInventory(year)
    inventory = 0.0 if inventory == "-" else float(inventory)

    totalCurrentLiabilities = getCurrentLiabilities(year)
    totalCurrentLiabilities = 0.0 if totalCurrentLiabilities == "-" else float(totalCurrentLiabilities)

    if totalCurrentLiabilities == 0.0: return "-"

    return formatNumber((totalCurrentAssets - inventory) / totalCurrentLiabilities, 4)

def returnOnEquity(year):
    """Return-on-Equity (ROE) = Net Income / Equity"""
    netIncome = getNetIncome(year)
    netIncome = 0.0 if netIncome == "-" else float(netIncome)

    totalEquity = getTotalEquity(year)
    totalEquity = 0.0 if totalEquity == "-" else float(totalEquity)

    if totalEquity == 0.0: return "-"

    return formatNumber(netIncome / totalEquity, 4)

def returnOnAssets(year):
    """Return-on-Assets (ROA) = Net Income / Total Assets"""
    netIncome = getNetIncome(year)
    netIncome = 0.0 if netIncome == "-" else float(netIncome)

    totalAssets = getTotalAssets(year)
    totalAssets = 0.0 if totalAssets == "-" else float(totalAssets)

    if totalAssets == 0.0: return "-"

    return formatNumber(netIncome / totalAssets, 4)

def returnOnInvestedCapital(year):
    """Return-on-Invested-Capital (ROIC) = Net Income / Invested Capital"""
    netIncome = getNetIncome(year)
    netIncome = 0.0 if netIncome == "-" else float(netIncome)

    investedCapital = getInvestedCapital(year)
    investedCapital = 0.0 if investedCapital == "-" else float(investedCapital)

    if investedCapital == 0.0: return "-"

    return formatNumber(netIncome / investedCapital, 4)

def grossProfitMarginRatio(year):
    """Gross-Profit-Margin-Ratio (GPMR) = Gross Profit / Revenue"""
    grossProfit = getGrossProfit(year)
    grossProfit = 0.0 if grossProfit == "-" else float(grossProfit)

    revenue = getRevenue(year)
    revenue = 0.0 if revenue == "-" else float(revenue)

    if revenue == 0.0: return "-"

    return formatNumber(grossProfit / revenue, 4)

def operatingMarginRatio(year):
    """Operating-Margin-Ratio (OMR) = Operating Income / Revenue"""
    operatingIncome = getOperatingIncome(year)
    operatingIncome = 0.0 if operatingIncome == "-" else float(operatingIncome)

    revenue = getRevenue(year)
    revenue = 0.0 if revenue == "-" else float(revenue)

    if revenue == 0.0: return "-"

    return formatNumber(operatingIncome / revenue, 4)

def netIncomeMarginRatio(year):
    """Net-Income-Margin-Ratio (NIMR) = Net Income / Revenue"""
    netIncome = getNetIncome(year)
    netIncome = 0.0 if netIncome == "-" else float(netIncome)

    revenue = getRevenue(year)
    revenue = 0.0 if revenue == "-" else float(revenue)

    if revenue == 0.0: return "-"

    return formatNumber(netIncome / revenue, 4)

def interestCoverageRatio(year):
    """Interest-Coverage-Ratio (ICR) = Operating Income / Interest Expense"""
    operatingIncome = getOperatingIncome(year)
    operatingIncome = 0.0 if operatingIncome == "-" else float(operatingIncome)

    interestExpense = getInterestExpense(year)
    interestExpense = 0.0 if interestExpense == "-" else float(interestExpense)

    if interestExpense == 0.0: return "-"

    return formatNumber(operatingIncome / interestExpense, 4)

def inventoryTurnoverRatio(year):
    """Inventory-Turnover-Ratio (ITR) = Cost of Revenue / Inventory"""
    costOfRevenue = getCostOfRevenue(year)
    costOfRevenue = 0.0 if costOfRevenue == "-" else float(costOfRevenue)

    inventory = getInventory(year)
    inventory = 0.0 if inventory == "-" else float(inventory)

    if inventory == 0.0: return "-"

    return formatNumber(costOfRevenue / inventory, 4)

def accountsReceivablesRatio(year):
    """Accounts-Receivables-Ratio (ARR) = Turnover / Accounts Receivables"""
    turnover = getRevenue(year)
    turnover = 0.0 if turnover == "-" else float(turnover)

    accountsReceivables = getAccountsReceivables(year)
    accountsReceivables = 0.0 if accountsReceivables == "-" else float(accountsReceivables)

    if accountsReceivables == 0.0: return "-"

    return formatNumber(turnover / accountsReceivables, 4)

def accountsPayableRatio(year):
    """Accounts-Payable-Ratio (APR) = Cost of Revenue / Accounts Payable"""
    costOfRevenue = getCostOfRevenue(year)
    costOfRevenue = 0.0 if costOfRevenue == "-" else float(costOfRevenue)

    accountsPayable = getAccountsPayable(year)
    accountsPayable = 0.0 if accountsPayable == "-" else float(accountsPayable)

    if accountsPayable == 0.0: return "-"

    return formatNumber(costOfRevenue / accountsPayable, 4)

def fcfToRevenueRatio(year):
    """FCF-to-Revenue-Ratio (FCFR) = Free Cash Flow / Revenue"""
    freeCashFlow = getFreeCashFlow(year)
    freeCashFlow = 0.0 if freeCashFlow == "-" else float(freeCashFlow)

    revenue = getRevenue(year)
    revenue = 0.0 if revenue == "-" else float(revenue)

    if revenue == 0.0: return "-"

    return formatNumber(freeCashFlow / revenue, 4)

def ICFOCFRatio(year):
    """ICF-to-OCF-Ratio (ICFOCF) = Investing Cash Flow  / Operating Cash Flow"""
    icf = getInvestingCashFlow(year)
    icf = 0.0 if icf == "-" else float(icf)

    ocf = getOperatingCashFlow(year)
    ocf = 0.0 if ocf == "-" else float(ocf)

    if ocf == 0.0: return "-"

    return formatNumber(icf / ocf, 4)

def priceToEarningsRatio():
    """Price-to-Earnings-Ratio (P/E) = Market Price Per Share  / Earnings Per Share"""
    marketPrice = get50DayMA()
    marketPrice = 0.0 if marketPrice == "-" else float(marketPrice)

    earningsPerShare = getEarningsPerShare(getYear(0))
    earningsPerShare = 0.0 if earningsPerShare == "-" else float(earningsPerShare)

    if earningsPerShare == 0.0: return "-"

    return formatNumber(marketPrice / earningsPerShare, 4)

def priceToBookRatio():
    """Price-to-Book-Ratio (P/B) = Market Price Per Share  / Book Value Per Share"""
    marketPrice = get50DayMA()
    marketPrice = 0.0 if marketPrice == "-" else float(marketPrice)

    bookValuePerShare = getBookValuePerShare(getYear(0))
    bookValuePerShare = 0.0 if bookValuePerShare == "-" else float(bookValuePerShare)

    if bookValuePerShare == 0.0: return "-"

    return formatNumber(marketPrice / bookValuePerShare, 4)

def ebitdaMargin(year):
    """EBITDA-Margin-Ratio = EBITDA  / Total Revenue"""
    ebitda = getEBITDA(year)
    ebitda = 0.0 if ebitda == "-" else float(ebitda)

    revenue = getRevenue(year)
    revenue = 0.0 if revenue == "-" else float(revenue)

    if revenue == 0.0: return "-"

    return formatNumber(ebitda / revenue, 4)

################################################################################
################################  Growth Rates  ################################
################################################################################

def equityGrowthRate(yearStart, yearEnd):
    """
    Get equity growth rate for a certain time period (yearStart to yearEnd).

    Parameters:
        yearStart (int): Corresponding time period starts at this year.
        yearEnd (int): Corresponding time period ends at this year.

    Returns:
        growthRate (str): Formatted equity growth rate based on time period
                          yearStart to yearEnd.
    """
    equityStart = getTotalEquity(yearStart)
    equityStart = 0.0 if equityStart == "-" else float(equityStart)

    equityEnd = getTotalEquity(yearEnd)
    equityEnd = 0.0 if equityEnd == "-" else float(equityEnd)

    if equityStart * equityEnd <= 0: # both numbers must be the same sign and not 0
        return "-"

    growthRate = (equityEnd / equityStart) ** (1.0 / abs(yearEnd - yearStart)) - 1

    return formatNumber(growthRate, 4)

def epsGrowthRate(yearStart, yearEnd):
    """
    Get EPS growth rate for a certain time period (yearStart to yearEnd).

    Parameters:
        yearStart (int): Corresponding time period starts at this year.
        yearEnd (int): Corresponding time period ends at this year.

    Returns:
        growthRate (str): Formatted EPS growth rate based on time period
                          yearStart to yearEnd.
    """
    epsStart = getEarningsPerShare(yearStart)
    epsStart = 0.0 if epsStart == "-" else float(epsStart)

    epsEnd = getEarningsPerShare(yearEnd)
    epsEnd = 0.0 if epsEnd == "-" else float(epsEnd)

    if epsStart * epsEnd <= 0: # both numbers must be the same sign and not 0
        return "-"

    growthRate = (epsEnd / epsStart) ** (1.0 / abs(yearEnd - yearStart)) - 1

    return formatNumber(growthRate, 4)

def revenueGrowthRate(yearStart, yearEnd):
    """
    Get Revenue growth rate for a certain time period (yearStart to yearEnd).

    Parameters:
        yearStart (int): Corresponding time period starts at this year.
        yearEnd (int): Corresponding time period ends at this year.

    Returns:
        growthRate (str): Formatted Revenue growth rate based on time period
                          yearStart to yearEnd.
    """
    revenueStart = getRevenue(yearStart)
    revenueStart = 0.0 if revenueStart == "-" else float(revenueStart)

    revenueEnd = getRevenue(yearEnd)
    revenueEnd = 0.0 if revenueEnd == "-" else float(revenueEnd)

    if revenueStart * revenueEnd <= 0: # both numbers must be the same sign and not 0
        return "-"
    
    growthRate = (revenueEnd / revenueStart) ** (1.0 / abs(yearEnd - yearStart)) - 1

    return formatNumber(growthRate, 4)

def fcfGrowthRate(yearStart, yearEnd):
    """
    Get FCF growth rate for a certain time period (yearStart to yearEnd).

    Parameters:
        yearStart (int): Corresponding time period starts at this year.
        yearEnd (int): Corresponding time period ends at this year.

    Returns:
        growthRate (str): Formatted FCF growth rate based on time period
                          yearStart to yearEnd.
    """
    fcfStart = getFreeCashFlow(yearStart)
    fcfStart = 0.0 if fcfStart == "-" else float(fcfStart)

    fcfEnd = getFreeCashFlow(yearEnd)
    fcfEnd = 0.0 if fcfEnd == "-" else float(fcfEnd)

    # two numbers are the same sign if the multiplication is positive
    if fcfStart * fcfEnd <= 0: # both numbers must be the same sign and not 0
        return "-"
    
    growthRate = (fcfEnd / fcfStart) ** (1.0 / abs(yearEnd - yearStart)) - 1

    return formatNumber(growthRate, 4)

################################################################################
#########################  Intrinsic Value Calculation  ########################
################################################################################

def getLongTermGrowthRate():
    """Get Long Term growth rate."""
    return 0.03

def fcfHistoricalGrowthRate():
    """Get Historical FCF growth rate."""
    numYears = 10 # simply build average over the last 10 years
    growthLimit = 0.20 # limit growth rate on a per year basis to 20 percent
                       # every company will slow down eventually
    divider = numYears
    avg = 0.0
    for i in range(-numYears, 0):
        growthRate = fcfGrowthRate(getYear(i), getYear(0))
        if growthRate == "-":
            divider = divider - 1 # growthRate does not exist and should be ignored
        else:
            growthRate = float(growthRate)
            if growthRate > growthLimit: # limit growth rate to growthLimit
                growthRate = growthLimit
            avg += growthRate

    avg /= divider
    return formatNumber(avg, 4)

def fcfFutureEstimate(n, growthRate=None):
    """FCF Future Estimate = BYFCF * (1 + GR)^n"""
    BYFCF = float(getFreeCashFlow(getYear(0)))
    if growthRate == None:
        GR = float(fcfHistoricalGrowthRate())
    else:
        GR = growthRate
    fcfEstimate = BYFCF * ((1.0 + GR) ** n)
    return formatNumber(fcfEstimate, 2)

def discountFactorEstimate(n, discountRate):
    """Discount Factor Estimate = (1 + DR)^n"""
    discountFactor = (1.0 + discountRate) ** n
    return formatNumber(discountFactor, 4)

def discountedCashFlow(n, discountRate, growthRate=None):
    """Discounted Cash Flow for year n = FCF(n) / DF(n)"""
    fcf = float(fcfFutureEstimate(n, growthRate))
    discountFactor = float(discountFactorEstimate(n, discountRate))
    DCF = fcf / discountFactor
    return formatNumber(float(DCF), 2)

def discountedPerpetuityCashFlow(discountRate, growthRate=None):
    """Discounted Perpetuity Cash Flow (DPCF) = (BYFCF * (1 + GR)^11 * (1 + LGR)) / (1 / (1 + DR)^11)"""
    BYFCF = float(getFreeCashFlow(getYear(0)))
    DR = float(discountRate)
    LGR = float(getLongTermGrowthRate())
    if growthRate == None:
        GR = float(fcfHistoricalGrowthRate())
    else:
        GR = growthRate
    DPCF = 0.0 if DR == LGR else ((BYFCF * ((1.0 + GR) ** 11) * (1.0 + LGR)) / (DR - LGR)) * (1.0 / ((1.0 + DR) ** 11))
    return formatNumber(float(DPCF), 2)

def sumDiscountedCashFlow(discountRate, growthRate=None):
    """Sum Discounted Cash Flow (DFCF) over all the years."""
    cashFlow = 0.0
    for i in range(1, 11):
        cashFlow += float(discountedCashFlow(i, discountRate, growthRate))
    return formatNumber(cashFlow, 2)

def getIntrinsicValue(discountRate, growthRate=None):
    """Intrinsic Value = sum of DFCF + DPCF"""
    sumDFCF = float(sumDiscountedCashFlow(discountRate, growthRate))
    DPCF = float(discountedPerpetuityCashFlow(discountRate, growthRate))
    intrinsicValue = sumDFCF + DPCF
    return formatNumber(float(intrinsicValue), 2)

def getIntrinsicValuePerShare(discountRate, growthRate=None):
    """Intrinsic Value Per Share = Intrinsic Value / Shares"""
    intrinsicValue = float(getIntrinsicValue(discountRate, growthRate))
    shares = float(getCommonSharesOutstanding(getYear(0)))
    intrinsicValuePerShare = 0.0 if shares == 0 else intrinsicValue / shares
    return formatNumber(float(intrinsicValuePerShare), 2)

def getMarginOfSafety(discountRate, growthRate=None):
    """Margin Of Safety (MOS) = 0.5 * Intrinsic Value Per Share"""
    intrinsicValuePerShare = float(getIntrinsicValuePerShare(discountRate, growthRate))
    marginOfSafety = intrinsicValuePerShare * 0.5
    return formatNumber(float(marginOfSafety), 2)
