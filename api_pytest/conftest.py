from common.operyaml import ReadYamlData
import pytest

@pytest.fixture(scope='session', autouse=True)
def clear_data():
    ReadYamlData().clear_yaml_data()


