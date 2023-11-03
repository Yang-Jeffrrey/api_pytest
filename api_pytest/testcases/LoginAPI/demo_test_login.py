import allure
import pytest
from common.operyaml import get_testcase_yaml
from common.sendrequests import SendRequests
from base.apiutil import RequestBase


class TestLogin:
    @allure.story('用户名密码正确登录')
    @pytest.mark.parametrize('case_info', get_testcase_yaml('./testcases/LoginAPI/login.yaml'))
    def test_login_01(self, case_info):
        RequestBase().specification_yaml(case_info)

    # @allure.story('用户名密码正确错误登录')
    # @pytest.mark.parametrize('case_info', get_testcase_yaml('./testcases/LoginAPI/login.yaml'))
    # def test_login_02(self, case_info):
    #     RequestBase().specification_yaml(case_info)
