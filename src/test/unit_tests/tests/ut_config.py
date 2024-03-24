import sys
import os
import pathlib
import json
import pytest
from unittest import mock
sys.path.append('../../main/code/')  # noqa: E402
import config

work_dir = os.getcwd()


@pytest.fixture(scope="session", autouse=True)
def setup():
    UNITTEST_DIR = os.path.abspath(work_dir)
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


def test_generate_default_config(mock_getcwd):
    mock_patch = "os.getcwd"
    with mock.patch(mock_patch) as mck:
        mck.side_effect = mock_getcwd
        run_conf = config.generate_default_config()
        assert run_conf['BUILD_ROOT_DIR'] == os.path.join(os.getcwd(), '../build')
        assert run_conf['JSON_TEMPLATE_DIR'] == os.path.join(os.getcwd(), '../resources/template/data')
        assert run_conf['JSON_TEMPLATE_FILE'] == os.path.join(os.getcwd(), '../resources/template/data/data.json')
        assert run_conf['LATEX_TEMPLATE_DIR'] == os.path.join(os.getcwd(), '../resources/template/latex')

    with mock.patch(mock_patch) as mck:
        mck.side_effect = mock_getcwd
        run_conf = config.generate_default_config(os.environ['ISIN'])
        assert run_conf['BUILD_CONFIG_DIR'] == os.path.join(os.getcwd(), '../build/US0378331005/config')
        assert run_conf['BUILD_CONFIG_FILE'] == os.path.join(os.getcwd(), '../build/US0378331005/config/config.json')
        assert run_conf['BUILD_DATA_DIR'] == os.path.join(os.getcwd(), '../build/US0378331005/data')
        assert run_conf['BUILD_DATA_FILE'] == os.path.join(os.getcwd(), '../build/US0378331005/data/data.json')


def test_get_run_config(mock_getcwd):
    mock_patch = "os.getcwd"
    with mock.patch(mock_patch) as mck:
        mck.side_effect = mock_getcwd
        run_conf = config.get_run_config()
        assert run_conf['BUILD_ROOT_DIR'] == os.path.join(os.getcwd(), '../build')
        assert run_conf['JSON_TEMPLATE_DIR'] == os.path.join(os.getcwd(), '../resources/template/data')
        assert run_conf['JSON_TEMPLATE_FILE'] == os.path.join(os.getcwd(), '../resources/template/data/data.json')
        assert run_conf['LATEX_TEMPLATE_DIR'] == os.path.join(os.getcwd(), '../resources/template/latex')
        assert run_conf['BUILD_CONFIG_DIR'] == os.path.join(os.getcwd(), '../build/US0378331005/config')
        assert run_conf['BUILD_CONFIG_FILE'] == os.path.join(os.getcwd(), '../build/US0378331005/config/config.json')
        assert run_conf['BUILD_DATA_DIR'] == os.path.join(os.getcwd(), '../build/US0378331005/data')
        assert run_conf['BUILD_DATA_FILE'] == os.path.join(os.getcwd(), '../build/US0378331005/data/data.json')


def test_get_run_config_item(mock_getcwd):
    mock_patch = "os.getcwd"
    with mock.patch(mock_patch) as mck:
        mck.side_effect = mock_getcwd
        item = config.get_run_config_item('BUILD_DATA_FILE')
        assert item == os.path.join(os.getcwd(), '../build/US0378331005/data/data.json')
