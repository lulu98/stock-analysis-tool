import sys
import os
import json
import pytest
from unittest import mock
sys.path.append('../../main/code/')  # noqa: E402
from render import render_data


@pytest.fixture(scope="session", autouse=True)
def setup():
    UNITTEST_DIR = os.path.abspath(os.getcwd())
    RESOURCE_DIR = os.path.join(UNITTEST_DIR, "resources")
    os.environ['JSON_FILE'] = os.path.join(RESOURCE_DIR, "data.json")
    os.environ['FUND_DATA'] = os.path.join(RESOURCE_DIR, "fund_data.json")
    os.environ['FUND_DATA_REF'] = os.path.join(RESOURCE_DIR, "fund_data_ref.json")  # noqa: E501
    os.environ['CALC_DATA'] = os.path.join(RESOURCE_DIR, "calc_data.json")
    os.environ['CALC_DATA_REF'] = os.path.join(RESOURCE_DIR, "calc_data_ref.json")  # noqa: E501


def test_render_data():
    fund_data = os.getenv('FUND_DATA')
    fund_data_ref = os.getenv('FUND_DATA_REF')
    with open(fund_data_ref, "r") as f:
        ref_data = f.read()
    assert render_data(fund_data) == ref_data

    calc_data = os.getenv('CALC_DATA')
    calc_data_ref = os.getenv('CALC_DATA_REF')
    with open(calc_data_ref, "r") as f:
        ref_data = f.read()
    assert render_data(calc_data) == ref_data
