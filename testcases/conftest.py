import allure
import pytest
from common.recordlog import logs
from common.operyaml import get_testcase_yaml
from base.apiutil import RequestBase


@pytest.fixture(autouse=True)
def start_test_end():
    logs.info('----------------------接口测试开始--------------------')
    yield
    logs.info('----------------------接口测试结束--------------------')


@pytest.fixture(scope='session', autouse=True)
def system_login():
    login_list = get_testcase_yaml('./testcases/LoginAPI/login.yaml')
    RequestBase().specification_yaml(login_list[0][0], login_list[0][1])

# @pytest.fixture(scope='session', autouse=True)
# def db_init():
#     """
#     后置处理器，比如测试之后的数据清理
#     数据库可以预先与之一批本次测试数据，在测试之后将这批数据清理，就不会对系统造成影响，也不会产生脏数据
#     :return:
#     """
#     conn = ConnectMysql()
#     yield
#     sql = "delete from sys_user where login_name = 'kjldj';"
#     conn.delete(sql)
#     allure.attach('将测试数据清空')
