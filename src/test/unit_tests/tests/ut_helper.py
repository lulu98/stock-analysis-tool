import sys
import os
import json
import pathlib
import pytest
from unittest import mock
sys.path.append('../../main/code/')  # noqa: E402
import config
import helper

work_dir = os.getcwd()


@pytest.fixture(scope="session", autouse=True)
def setup():
    UNITTEST_DIR = os.path.abspath(os.getcwd())
    RESOURCE_DIR = os.path.join(UNITTEST_DIR, "resources")
    os.environ['ISIN'] = "US0378331005"
    os.environ['RESOURCE_DIR'] = RESOURCE_DIR


@pytest.fixture(name="mock_getcwd", scope="session")
def fixture_mock_getcwd():
    """Mock os.getcwd to simulate invalid query."""
    def _mock_func():
        path = os.path.abspath(work_dir)
        path = pathlib.Path(path)
        path = path.parent
        path = path.parent
        path = os.path.join(path, "main", "code")
        return path
    return _mock_func


def test_get_api_params(mock_getcwd):
    mock_patch = "os.getcwd"
    apple_isin = os.getenv('ISIN')
    with mock.patch(mock_patch) as mck:
        mck.side_effect = mock_getcwd
        run_conf = config.generate_default_config(apple_isin)
    api_params = helper.get_api_params()
    assert api_params[apple_isin]['ExchangeID'] == 'US'
    assert api_params[apple_isin]['Name'] == 'Apple Inc'
    assert api_params[apple_isin]['Symbol'] == 'AAPL'
    api_params = helper.get_api_params(isin=apple_isin)
    assert api_params[apple_isin]['ExchangeID'] == 'US'
    assert api_params[apple_isin]['Name'] == 'Apple Inc'
    assert api_params[apple_isin]['Symbol'] == 'AAPL'
