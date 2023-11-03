import allure
import pytest

from base.apiutil import RequestBase
from common.operyaml import get_testcase_yaml
from common.recordlog import logs
from base.generateId import m_id, c_id

@allure.feature(next(m_id) + '智慧物流项目')
class TestProductModule:

    @allure.story(next(c_id) + "获取商品列表")
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize('base_info,testcase', get_testcase_yaml('./testcases/logistic/getMaterial.yaml'))
    def test_get_material(self, base_info, testcase):
        allure.dynamic.title(testcase['case_name'])
        RequestBase().specification_yaml(base_info, testcase)


    @allure.story(next(c_id) + "货主(托运人)下单")
    @pytest.mark.run(order=2)
    @pytest.mark.parametrize('base_info,testcase', get_testcase_yaml('./testcases/logistic/Order.yaml'))
    def test_order_material(self, base_info, testcase):
        allure.dynamic.title(testcase['case_name'])
        RequestBase().specification_yaml(base_info, testcase)

    @allure.story(next(c_id) + "集团接收订单")
    @pytest.mark.run(order=3)
    @pytest.mark.parametrize('base_info,testcase', get_testcase_yaml('./testcases/logistic/GetOrder.yaml'))
    def test_get_order_material(self, base_info, testcase):
        allure.dynamic.title(testcase['case_name'])
        RequestBase().specification_yaml(base_info, testcase)

    @allure.story(next(c_id) + "集团分配物流公司")
    @pytest.mark.run(order=4)
    @pytest.mark.parametrize('base_info,testcase', get_testcase_yaml('./testcases/logistic/AssignOrder.yaml'))
    def test_assign_order_material(self, base_info, testcase):
        allure.dynamic.title(testcase['case_name'])
        RequestBase().specification_yaml(base_info, testcase)
