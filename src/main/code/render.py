from jinja2 import Environment, FileSystemLoader
import local_api
import calculations
import os


def get_years_dict():
    years = {
        "0": local_api.getYear(0),
        "-1": local_api.getYear(-1),
        "-2": local_api.getYear(-2),
        "-3": local_api.getYear(-3),
        "-4": local_api.getYear(-4),
        "-5": local_api.getYear(-5),
        "-6": local_api.getYear(-6),
        "-7": local_api.getYear(-7),
        "-8": local_api.getYear(-8),
        "-9": local_api.getYear(-9),
        "-10": local_api.getYear(-10),
        "-11": local_api.getYear(-11)
    }
    return years


func_dict = {
    "get_years_dict": get_years_dict,
    "__formatNumber": local_api.formatNumber,
    "__getDataItem": local_api.getDataItem,
    "__getYearOfDate": local_api.getYearOfDate,
    "__getMonthOfDate": local_api.getMonthOfDate,
    "__getDayOfDate": local_api.getDayOfDate,
    "__getFinancialsDate": local_api.getFinancialsDate,
    "__getBaseYear": local_api.getBaseYear,
    "__getYear": local_api.getYear,
    "__getCompanyCode": local_api.getCompanyCode,
    "__getCompanyName": local_api.getCompanyName,
    "__getAddress": local_api.getAddress,
    "__getDescription": local_api.getDescription,
    "__getISIN": local_api.getISIN,
    "__getIPODate": local_api.getIPODate,
    "__getSector": local_api.getSector,
    "__getIndustry": local_api.getIndustry,
    "__getNumEmployees": local_api.getNumEmployees,
    "__getFiscalYearEnd": local_api.getFiscalYearEnd,
    "__getCurrency": local_api.getCurrency,
    "__getOfficers": local_api.getOfficers,
    "__getInstitutions": local_api.getInstitutions,
    "__getFunds": local_api.getFunds,
    "__getInsiderTransactions": local_api.getInsiderTransactions,
    "__getAnalystRating": local_api.getAnalystRating,
    "__getAnalystTargetPrice": local_api.getAnalystTargetPrice,
    "__getAnalystStrongBuy": local_api.getAnalystStrongBuy,
    "__getAnalystBuy": local_api.getAnalystBuy,
    "__getAnalystHold": local_api.getAnalystHold,
    "__getAnalystSell": local_api.getAnalystSell,
    "__getAnalystStrongSell": local_api.getAnalystStrongSell,
    "__getMarketCapitalization": local_api.getMarketCapitalization,
    "__getDividendShare": local_api.getDividendShare,
    "__getDividendYield": local_api.getDividendYield,
    "__getSharesOutstanding": local_api.getSharesOutstanding,
    "__getSharesFloat": local_api.getSharesFloat,
    "__getSharesPercentInsiders": local_api.getSharesPercentInsiders,
    "__getSharesPercentInstitutions": local_api.getSharesPercentInstitutions,
    "__getSharesPercentPublic": local_api.getSharesPercentPublic,
    "__get50DayMA": local_api.get50DayMA,
    "__getInventory": local_api.getInventory,
    "__getAccountsReceivables": local_api.getAccountsReceivables,
    "__getAccountsPayable": local_api.getAccountsPayable,
    "__getCurrentLiabilities": local_api.getCurrentLiabilities,
    "__getNonCurrentLiabilities": local_api.getNonCurrentLiabilities,
    "__getTotalLiabilities": local_api.getTotalLiabilities,
    "__getLiabilitiesAndEquity": local_api.getLiabilitiesAndEquity,
    "__getTotalEquity": local_api.getTotalEquity,
    "__getCurrentAssets": local_api.getCurrentAssets,
    "__getNonCurrentAssets": local_api.getNonCurrentAssets,
    "__getTotalAssets": local_api.getTotalAssets,
    "__getShortTermDebt": local_api.getShortTermDebt,
    "__getLongTermDebt": local_api.getLongTermDebt,
    "__getTotalDebt": local_api.getTotalDebt,
    "__getInvestedCapital": local_api.getInvestedCapital,
    "__getCommonSharesOutstanding": local_api.getCommonSharesOutstanding,
    "__getEarningsPerShare": local_api.getEarningsPerShare,
    "__getBookValuePerShare": local_api.getBookValuePerShare,
    "__getNetIncome": local_api.getNetIncome,
    "__getRevenue": local_api.getRevenue,
    "__getEBITDA": local_api.getEBITDA,
    "__getGrossProfit": local_api.getGrossProfit,
    "__getOperatingIncome": local_api.getOperatingIncome,
    "__getInterestExpense": local_api.getInterestExpense,
    "__getCostOfRevenue": local_api.getCostOfRevenue,
    "__getOperatingCashFlow": local_api.getOperatingCashFlow,
    "__getInvestingCashFlow": local_api.getInvestingCashFlow,
    "__getCapitalExpenditures": local_api.getCapitalExpenditures,
    "__getFreeCashFlow": local_api.getFreeCashFlow,
    "__getSharesFloatToOutstandingRatio": calculations.getSharesFloatToOutstandingRatio,  # noqa: E501
    "__debtToEquity": calculations.debtToEquity,
    "__debtToFCF": calculations.debtToFCF,
    "__liabilitiesToEquity": calculations.liabilitiesToEquity,
    "__currentRatio": calculations.currentRatio,
    "__acidTestRatio": calculations.acidTestRatio,
    "__returnOnEquity": calculations.returnOnEquity,
    "__returnOnAssets": calculations.returnOnAssets,
    "__returnOnInvestedCapital": calculations.returnOnInvestedCapital,
    "__grossProfitMarginRatio": calculations.grossProfitMarginRatio,
    "__operatingMarginRatio": calculations.operatingMarginRatio,
    "__netIncomeMarginRatio": calculations.netIncomeMarginRatio,
    "__interestCoverageRatio": calculations.interestCoverageRatio,
    "__inventoryTurnoverRatio": calculations.inventoryTurnoverRatio,
    "__accountsReceivablesRatio": calculations.accountsReceivablesRatio,
    "__accountsPayableRatio": calculations.accountsPayableRatio,
    "__fcfToRevenueRatio": calculations.fcfToRevenueRatio,
    "__ICFOCFRatio": calculations.ICFOCFRatio,
    "__priceToEarningsRatio": calculations.priceToEarningsRatio,
    "__priceToBookRatio": calculations.priceToBookRatio,
    "__ebitdaMargin": calculations.ebitdaMargin,
    "__equityGrowthRate": calculations.equityGrowthRate,
    "__epsGrowthRate": calculations.epsGrowthRate,
    "__revenueGrowthRate": calculations.revenueGrowthRate,
    "__fcfGrowthRate": calculations.fcfGrowthRate,
    "__getLongTermGrowthRate": calculations.getLongTermGrowthRate,
    "__fcfHistoricalGrowthRate": calculations.fcfHistoricalGrowthRate,
    "__fcfFutureEstimate": calculations.fcfFutureEstimate,
    "__discountFactorEstimate": calculations.discountFactorEstimate,
    "__discountedCashFlow": calculations.discountedCashFlow,
    "__discountedPerpetuityCashFlow": calculations.discountedPerpetuityCashFlow,  # noqa: E501
    "__sumDiscountedCashFlow": calculations.sumDiscountedCashFlow,
    "__getIntrinsicValue": calculations.getIntrinsicValue,
    "__getIntrinsicValuePerShare": calculations.getIntrinsicValuePerShare,
    "__getMarginOfSafety": calculations.getMarginOfSafety,
}


def render_data(template_path):
    template_dir = os.path.dirname(template_path)
    template_file = os.path.basename(template_path)
    env = Environment(loader=FileSystemLoader(template_dir))
    jinja_template = env.get_template(template_file)
    jinja_template.globals.update(func_dict)
    template_string = jinja_template.render()

    return template_string


def dump_data(data, template_path):
    with open(template_path, "w") as f:
        f.write(data)
