import sys
import os
import json
import pytest
from unittest import mock
sys.path.append('../../main/code/')
from calculations import *  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def setup():
    UNITTEST_DIR = os.path.abspath(os.getcwd())
    RESOURCE_DIR = os.path.join(UNITTEST_DIR, "resources")
    os.environ['JSON_FILE'] = os.path.join(RESOURCE_DIR, "data.json")


def test_getSharesFloatToOutstandingRatio():
    assert getSharesFloatToOutstandingRatio() == "0.9990"


def test_debtToEquity():
    assert debtToEquity(2020) == "1.7208"
    assert debtToEquity(2021) == "1.9768"


def test_debtToFCF():
    assert debtToFCF(2020) == "1.5326"
    assert debtToFCF(2021) == "1.3417"


def test_liabilitiesToEquity():
    assert liabilitiesToEquity(2020) == "3.9570"
    assert liabilitiesToEquity(2021) == "4.5635"


def test_currentRatio():
    assert currentRatio(2020) == "1.3636"
    assert currentRatio(2021) == "1.0746"


def test_acidTestRatio():
    assert acidTestRatio(2020) == "1.3251"
    assert acidTestRatio(2021) == "1.0221"


def test_returnOnEquity():
    assert returnOnEquity(2020) == "0.8787"
    assert returnOnEquity(2021) == "1.5007"


def test_returnOnAssets():
    assert returnOnAssets(2020) == "0.1773"
    assert returnOnAssets(2021) == "0.2697"


def test_returnOnInvestedCapital():
    assert returnOnInvestedCapital(2020) == "0.3229"
    assert returnOnInvestedCapital(2021) == "0.5041"


def test_grossProfitMarginRatio():
    assert grossProfitMarginRatio(2020) == "0.3823"
    assert grossProfitMarginRatio(2021) == "0.4178"


def test_operatingMarginRatio():
    assert operatingMarginRatio(2020) == "0.2415"
    assert operatingMarginRatio(2021) == "0.2978"


def test_netIncomeMarginRatio():
    assert netIncomeMarginRatio(2020) == "0.2091"
    assert netIncomeMarginRatio(2021) == "0.2588"


def test_interestCoverageRatio():
    assert interestCoverageRatio(2020) == "23.0727"
    assert interestCoverageRatio(2021) == "41.1905"


def test_inventoryTurnoverRatio():
    assert inventoryTurnoverRatio(2020) == "41.7530"
    assert inventoryTurnoverRatio(2021) == "32.3679"


def test_accountsReceivablesRatio():
    assert accountsReceivablesRatio(2020) == "7.3312"
    assert accountsReceivablesRatio(2021) == "7.1024"


def test_accountsPayableRatio():
    assert accountsPayableRatio(2020) == "4.0089"
    assert accountsPayableRatio(2021) == "3.8891"


def test_fcfToRevenueRatio():
    assert fcfToRevenueRatio(2020) == "0.2673"
    assert fcfToRevenueRatio(2021) == "0.2541"


def test_ICFOCFRatio():
    assert ICFOCFRatio(2020) == "-0.0532"
    assert ICFOCFRatio(2021) == "-0.1398"


def test_priceToEarningsRatio():
    assert priceToEarningsRatio() == "29.9394"


def test_priceToBookRatio():
    assert priceToBookRatio() == "44.9304"


def test_ebitdaMargin():
    assert ebitdaMargin(2020) == "0.2951"
    assert ebitdaMargin(2021) == "0.3366"


# Growth Rates Tests


def test_equityGrowthRate():
    assert equityGrowthRate(2020, 2021) == "-0.0344"
    assert equityGrowthRate(2018, 2021) == "-0.1618"
    assert equityGrowthRate(2016, 2021) == "-0.1323"


def test_epsGrowthRate():
    assert epsGrowthRate(2020, 2021) == "0.7140"
    assert epsGrowthRate(2018, 2021) == "0.2355"
    assert epsGrowthRate(2016, 2021) == "0.2201"


def test_revenueGrowthRate():
    assert revenueGrowthRate(2020, 2021) == "0.3326"
    assert revenueGrowthRate(2018, 2021) == "0.1126"
    assert revenueGrowthRate(2016, 2021) == "0.1115"


def test_fcfGrowthRate():
    assert fcfGrowthRate(2020, 2021) == "0.2670"
    assert fcfGrowthRate(2018, 2021) == "0.1318"
    assert fcfGrowthRate(2016, 2021) == "0.1220"


# Intrinsic Value Calculation Tests


def test_getLongTermGrowthRate():
    assert getLongTermGrowthRate() == 0.03


def test_fcfHistoricalGrowthRate():
    assert fcfHistoricalGrowthRate() == "0.1268"


def test_getIntrinsicValuePerShare():
    assert getIntrinsicValuePerShare(0.10, -0.10) == "30.39"
    assert getIntrinsicValuePerShare(0.10, 0.00) == "62.29"
    assert getIntrinsicValuePerShare(0.10, 0.10) == "136.22"
    assert getIntrinsicValuePerShare(0.10) == "168.75"
    assert getIntrinsicValuePerShare(0.15, -0.10) == "21.32"
    assert getIntrinsicValuePerShare(0.15, 0.00) == "37.83"
    assert getIntrinsicValuePerShare(0.15, 0.10) == "72.53"
    assert getIntrinsicValuePerShare(0.15) == "87.16"
    assert getIntrinsicValuePerShare(0.20, -0.10) == "17.01"
    assert getIntrinsicValuePerShare(0.20, 0.00) == "27.60"
    assert getIntrinsicValuePerShare(0.20, 0.10) == "48.05"
    assert getIntrinsicValuePerShare(0.20) == "56.34"


def test_getMarginOfSafety():
    assert getMarginOfSafety(0.10, -0.10) == "15.20"
    assert getMarginOfSafety(0.10, 0.00) == "31.14"
    assert getMarginOfSafety(0.10, 0.10) == "68.11"
    assert getMarginOfSafety(0.10) == "84.38"
    assert getMarginOfSafety(0.15, -0.10) == "10.66"
    assert getMarginOfSafety(0.15, 0.00) == "18.91"
    assert getMarginOfSafety(0.15, 0.10) == "36.27"
    assert getMarginOfSafety(0.15) == "43.58"
    assert getMarginOfSafety(0.20, -0.10) == "8.51"
    assert getMarginOfSafety(0.20, 0.00) == "13.80"
    assert getMarginOfSafety(0.20, 0.10) == "24.02"
    assert getMarginOfSafety(0.20) == "28.17"
