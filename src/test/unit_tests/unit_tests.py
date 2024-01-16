import sys
import os
import json
import pytest
from unittest import mock
sys.path.insert(1, '../../main/code/')
from local_api import *  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def setup():
    UNITTEST_DIR = os.path.abspath(os.getcwd())
    RESOURCE_DIR = os.path.join(UNITTEST_DIR, "resources")
    os.environ['JSON_FILE'] = os.path.join(RESOURCE_DIR, "data.json")

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
    partOfDescription = "Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide."  # noqa: E501
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

# TODO: balance sheet
# TODO: cash flow statement
# TODO: income statement
# TODO: calculated data
