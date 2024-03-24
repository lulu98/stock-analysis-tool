import sys
import os
import json
import pytest
from unittest import mock
sys.path.append('../../main/code/')
from local_api import *  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def setup():
    UNITTEST_DIR = os.path.abspath(os.getcwd())
    RESOURCE_DIR = os.path.join(UNITTEST_DIR, "resources")
    os.environ['JSON_FILE'] = os.path.join(RESOURCE_DIR, "data.json")
    os.environ['ISIN'] = "US0378331005"

# formatNumber tests


def test_formatNumber_PositiveNumber():
    assert formatNumber(3.12, 4) == "3.1200"
    assert formatNumber(3.12345, 4) == "3.1235"


def test_formatNumber_NegativeNumber():
    assert formatNumber(-3.12, 4) == "-3.1200"
    assert formatNumber(-3.12345, 4) == "-3.1235"


def test_formatNumber_Zero():
    assert formatNumber(0, 4) == "0.0000"


def test_formatNumber_IllegalInput():
    assert formatNumber(3.12, 0) == "0.0"
    assert formatNumber(3.12, -1) == "0.0"

# getXOfDate tests


def test_getYearOfDate():
    assert getYearOfDate("2020-12-10") == "2020"


def test_getMonthOfDate():
    assert getMonthOfDate("2020-12-10") == "12"


def test_getDayOfDate():
    assert getDayOfDate("2020-12-10") == "10"

# functional tests

# Generals


def test_getFinancialsDate():
    assert getFinancialsDate(2020) == "2020-09-30"
    assert getFinancialsDate(2021) == "2021-09-30"


def test_getBaseYear():
    assert getBaseYear() == 2021


def test_getYear():
    assert getYear(-5) == 2016
    assert getYear(0) == 2021
    assert getYear(5) == 2026


def test_getCompanyCode():
    assert getCompanyCode() == "AAPL"


def test_getCompanyName():
    assert getCompanyName() == "Apple Inc"


def test_getAddress():
    address = "One Apple Park Way, Cupertino, CA, United States, 95014"
    assert getAddress() == address


def test_getDescription():
    partOfDescription = "Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide."
    assert partOfDescription in getDescription()


def test_getISIN():
    assert getISIN() == "US0378331005"


def test_getIPODate():
    assert getIPODate() == "1980-12-12"


def test_getSector():
    assert getSector() == "Technology"


def test_getIndustry():
    assert getIndustry() == "Consumer Electronics"


def test_getNumEmployees():
    assert getNumEmployees() == 100000


def test_getFiscalYearEnd():
    assert getFiscalYearEnd() == "September"


def test_getCurrency():
    assert getCurrency() == "USD"


def test_getOfficers():
    officers = json.loads(getOfficers())
    assert len(officers) == 10
    assert officers["0"]["Name"] == "Mr. Timothy D. Cook"
    assert officers["0"]["Title"] == "CEO & Director"
    assert officers["0"]["YearBorn"] == "1961"

# Holders


def test_getInstitutions():
    institutions = json.loads(getInstitutions())
    assert len(institutions) == 20
    assert institutions["0"]["name"] == "Vanguard Group Inc"
    assert institutions["0"]["date"] == "2021-12-31"
    assert institutions["0"]["totalShares"] == 7.7286
    assert institutions["0"]["totalAssets"] == 5.0848
    assert institutions["0"]["currentShares"] == 1261261357
    assert institutions["0"]["change"] == -5071310
    assert institutions["0"]["change_p"] == -0.4005


def test_getFunds():
    funds = json.loads(getFunds())
    assert len(funds) == 20
    assert funds["0"]["name"] == "Vanguard Total Stock Mkt Idx Inv"
    assert funds["0"]["date"] == "2022-02-28"
    assert funds["0"]["totalShares"] == 2.7479
    assert funds["0"]["totalAssets"] == 5.8201
    assert funds["0"]["currentShares"] == 448434441
    assert funds["0"]["change"] == 1622373
    assert funds["0"]["change_p"] == 0.3631

# Insider Transactions


def test_getInsiderTransactions():
    insiderTransactions = json.loads(getInsiderTransactions())
    assert len(insiderTransactions) == 20
    assert insiderTransactions["0"]["date"] == "2022-04-04"
    assert insiderTransactions["0"]["ownerName"] == "Jeffrey E. Williams"
    assert insiderTransactions["0"]["transactionAmount"] == 105901
    assert insiderTransactions["0"]["transactionPrice"] == 177.75

# Analyst Ratings


def test_getAnalystRating():
    assert getAnalystRating() == 4.3333


def test_getAnalystTargetPrice():
    assert getAnalystTargetPrice() == "169.88"


def test_getAnalystStrongBuy():
    assert getAnalystStrongBuy() == 28


def test_getAnalystBuy():
    assert getAnalystBuy() == 7


def test_getAnalystHold():
    assert getAnalystHold() == 8


def test_getAnalystSell():
    assert getAnalystSell() == 1


def test_getAnalystStrongSell():
    assert getAnalystStrongSell() == 1

# Highlights


@pytest.fixture(name="mock_getDataItem", scope="session")
def fixture_mock_getDataItem():
    """Mock getDataItem to simulate invalid query."""
    def _mock_func(param):
        return "null"
    return _mock_func


def test_getMarketCapitalization_Valid():
    assert getMarketCapitalization() == "2736110698496.00"


def test_getMarketCapitalization_Invalid(mock_getDataItem):
    mock_patch = "local_api.getDataItem"
    with mock.patch(mock_patch) as mck:
        mck.side_effect = mock_getDataItem
        assert getMarketCapitalization() == "null"


def test_getDividendShare_Valid():
    assert getDividendShare() == "0.8650"


def test_getDividendShare_Invalid(mock_getDataItem):
    mock_patch = "local_api.getDataItem"
    with mock.patch(mock_patch) as mck:
        mck.side_effect = mock_getDataItem
        assert getDividendShare() == "null"


def test_getDividendYield_Valid():
    assert getDividendYield() == "0.0053"


def test_getDividendYield_Invalid(mock_getDataItem):
    mock_patch = "local_api.getDataItem"
    with mock.patch(mock_patch) as mck:
        mck.side_effect = mock_getDataItem
        assert getDividendYield() == "null"


# Shares stats tests


def test_getSharesOutstanding():
    assert getSharesOutstanding() == 16319399936


def test_getSharesFloat():
    assert getSharesFloat() == 16302631976


def test_getSharesPercentInsiders_Valid():
    assert getSharesPercentInsiders() == "0.0710"


def test_getSharesPercentInsiders_Invalid(mock_getDataItem):
    mock_patch = "local_api.getDataItem"
    with mock.patch(mock_patch) as mck:
        mck.side_effect = mock_getDataItem
        assert getSharesPercentInsiders() == "null"


def test_getSharesPercentInstitutions_Valid():
    assert getSharesPercentInstitutions() == "59.3690"


def test_getSharesPercentInstitutions_Invalid(mock_getDataItem):
    mock_patch = "local_api.getDataItem"
    with mock.patch(mock_patch) as mck:
        mck.side_effect = mock_getDataItem
        assert getSharesPercentInstitutions() == "null"


def test_getSharesPercentPublic_Valid():
    assert getSharesPercentPublic() == "40.5600"


def test_getSharesPercentInstitutions_Invalid(mock_getDataItem):
    mock_patch = "local_api.getDataItem"
    with mock.patch(mock_patch) as mck:
        mck.side_effect = mock_getDataItem
        assert getSharesPercentPublic() == "100.0000"

# technicals tests


def test_get50DayMA_Valid():
    assert get50DayMA() == "168.08"


def test_get50DayMA_Invalid(mock_getDataItem):
    mock_patch = "local_api.getDataItem"
    with mock.patch(mock_patch) as mck:
        mck.side_effect = mock_getDataItem
        assert get50DayMA() == "null"

# balance sheet


def test_getInventory():
    assert getInventory(2020) == "4061000000.00"
    assert getInventory(2021) == "6580000000.00"


def test_getAccountsReceivables():
    assert getAccountsReceivables(2020) == "37445000000.00"
    assert getAccountsReceivables(2021) == "51506000000.00"


def test_getAccountsPayable():
    assert getAccountsPayable(2020) == "42296000000.00"
    assert getAccountsPayable(2021) == "54763000000.00"


def test_getCurrentLiabilities():
    assert getCurrentLiabilities(2020) == "105392000000.00"
    assert getCurrentLiabilities(2021) == "125481000000.00"


def test_getNonCurrentLiabilities():
    assert getNonCurrentLiabilities(2020) == "153157000000.00"
    assert getNonCurrentLiabilities(2021) == "162431000000.00"


def test_getTotalLiabilities():
    assert getTotalLiabilities(2020) == "258549000000.00"
    assert getTotalLiabilities(2021) == "287912000000.00"


def test_getLiabilitiesAndEquity():
    assert getLiabilitiesAndEquity(2020) == "323888000000.00"
    assert getLiabilitiesAndEquity(2021) == "351002000000.00"


def test_getTotalEquity():
    assert getTotalEquity(2020) == "65339000000.00"
    assert getTotalEquity(2021) == "63090000000.00"


def test_getCurrentAssets():
    assert getCurrentAssets(2020) == "143713000000.00"
    assert getCurrentAssets(2021) == "134836000000.00"


def test_getNonCurrentAssets():
    assert getNonCurrentAssets(2020) == "180175000000.00"
    assert getNonCurrentAssets(2021) == "216166000000.00"


def test_getTotalAssets():
    assert getTotalAssets(2020) == "323888000000.00"
    assert getTotalAssets(2021) == "351002000000.00"


def test_getShortTermDebt():
    assert getShortTermDebt(2020) == "13769000000.00"
    assert getShortTermDebt(2021) == "15613000000.00"


def test_getLongTermDebt():
    assert getLongTermDebt(2020) == "98667000000.00"
    assert getLongTermDebt(2021) == "109106000000.00"


def test_getTotalDebt():
    assert getTotalDebt(2020) == "112436000000.00"
    assert getTotalDebt(2021) == "124719000000.00"


def test_getInvestedCapital():
    assert getInvestedCapital(2020) == "177775000000.00"
    assert getInvestedCapital(2021) == "187809000000.00"


def test_getCommonSharesOutstanding():
    assert getCommonSharesOutstanding(2020) == "17528214000.00"
    assert getCommonSharesOutstanding(2021) == "16864919000.00"


def test_getEarningsPerShare():
    assert getEarningsPerShare(2020) == "3.2753"
    assert getEarningsPerShare(2021) == "5.6140"


def test_getBookValuePerShare():
    assert getBookValuePerShare(2020) == "3.7276"
    assert getBookValuePerShare(2021) == "3.7409"

# income statement


def test_getNetIncome():
    assert getNetIncome(2020) == "57411000000.00"
    assert getNetIncome(2021) == "94680000000.00"


def test_getRevenue():
    assert getRevenue(2020) == "274515000000.00"
    assert getRevenue(2021) == "365817000000.00"


def test_getEBITDA():
    assert getEBITDA(2020) == "81020000000.00"
    assert getEBITDA(2021) == "123136000000.00"


def test_getGrossProfit():
    assert getGrossProfit(2020) == "104956000000.00"
    assert getGrossProfit(2021) == "152836000000.00"


def test_getOperatingIncome():
    assert getOperatingIncome(2020) == "66288000000.00"
    assert getOperatingIncome(2021) == "108949000000.00"


def test_getInterestExpense():
    assert getInterestExpense(2020) == "2873000000.00"
    assert getInterestExpense(2021) == "2645000000.00"


def test_getCostOfRevenue():
    assert getCostOfRevenue(2020) == "169559000000.00"
    assert getCostOfRevenue(2021) == "212981000000.00"

# cash flow statement


def test_getOperatingCashFlow():
    assert getOperatingCashFlow(2020) == "80674000000.00"
    assert getOperatingCashFlow(2021) == "104038000000.00"


def test_getInvestingCashFlow():
    assert getInvestingCashFlow(2020) == "-4289000000.00"
    assert getInvestingCashFlow(2021) == "-14545000000.00"


def test_getCapitalExpenditures():
    assert getCapitalExpenditures(2020) == "7309000000.00"
    assert getCapitalExpenditures(2021) == "11085000000.00"


def test_getFreeCashFlow():
    assert getFreeCashFlow(2020) == "73365000000.00"
    assert getFreeCashFlow(2021) == "92953000000.00"
