import allure
import pytest

from base.apiutil import RequestBase
from common.operyaml import get_testcase_yaml
from common.recordlog import logs
from base.generateId import m_id, c_id

@allure.feature(next(m_id) + '公用接口，供调试使用')
class TestDebugApi:

    def setup_class(self):
        """执行测试之前，需要做的操作"""
        logs.info('环境初始化...')
    # 场景，allure报告的目录结构
    @allure.story(next(c_id) + '新增用户')
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize('base_info,testcase', get_testcase_yaml('./testcases/publicApi/addUser.yaml'))
    def test_add_user(self, base_info, testcase):
        allure.dynamic.title(testcase['case_name'])
        RequestBase().specification_yaml(base_info, testcase)


    @allure.story(next(c_id) + '修改用户')
    @pytest.mark.run(order=2)
    @pytest.mark.parametrize('base_info,testcase', get_testcase_yaml('./testcases/publicApi/updateUser.yaml'))
    def test_update_user(self, base_info, testcase):
        allure.dynamic.title(testcase['case_name'])
        RequestBase().specification_yaml(base_info, testcase)


    @allure.story(next(c_id) + '删除用户')
    @pytest.mark.run(order=3)
    @pytest.mark.parametrize('base_info,testcase', get_testcase_yaml('./testcases/publicApi/deleteUser.yaml'))
    def test_delete_user(self, base_info, testcase):
        allure.dynamic.title(testcase['case_name'])
        RequestBase().specification_yaml(base_info, testcase)


    @allure.story(next(c_id) + '查询用户')
    @pytest.mark.run(order=4)
    @pytest.mark.parametrize('base_info,testcase', get_testcase_yaml('./testcases/publicApi/queryUser.yaml'))
    def test_query_user(self, base_info, testcase):
        allure.dynamic.title(testcase['case_name'])
        RequestBase().specification_yaml(base_info, testcase)


    def teardown_class(self):
        """该测试类的后置操作，如环境清楚，数据恢复"""
        logs.info('正在清理测试数据...')