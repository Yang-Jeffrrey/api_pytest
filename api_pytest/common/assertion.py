import operator

import allure
import jsonpath

from common.recordlog import logs


class Assertions (object):
    """接口断言"""

    def contains_assert(self, expected, response, status_code):
        """
        字符串断言
        :param expected: yaml文件里面的validation字段中的预期结果
        :param response: 接口实际返回值
        :param status_code: 接口返回状态码
        :return:
        """
        # flag标识，断言标识，0标识成功，否则为失败
        flag = 0
        for assert_key, assert_value in expected.items():
            if assert_key == 'status_code':
                if assert_value != status_code:
                    flag += 1
                    allure.attach(f"预期结果：{assert_value}\n实际结果:{status_code}", '响应代码断言结果：失败',
                                    attachment_type=allure.attachment_type.TEXT)
                    logs.error("contains断言失败：接口返回码[%s]不等于[%s]" % (status_code, assert_value))
            else:
                resp_list = jsonpath.jsonpath(response, f'$..{assert_key}')
                if isinstance(resp_list[0], str):
                    resp_list = ''.join(resp_list)
                if resp_list:
                    if assert_value in resp_list:
                        logs.info("字符串包含断言成功：预期结果[%s],实际结果[%s]" % (assert_value, resp_list))
                    else:
                        flag += 1
                        allure.attach(f"预期结果：{assert_value}\n实际结果:{resp_list}", '响应代码断言结果：失败',
                                      attachment_type=allure.attachment_type.TEXT)
                        logs.error("contains断言失败：预期结果为[%s]，实际结果为[%s]" % (assert_value, resp_list))
        return flag

    def equal_assert(self, expected, response, status_code=None):
        """
        相等断言模式
        :param expected: 预期结果，yaml文件validation值
        :param response: 接口实际响应结果
        :param status_code: 状态码
        :return: 
        """
        flag = 0
        res_lst = []
        if isinstance(response, dict) and isinstance(expected, dict):
            for res in response:
                if list(expected.keys())[0] != res:
                    res_lst.append(res)
            for rl in res_lst:
                del response[rl]
            eq_assert = operator.eq(response, expected)
            if eq_assert:
                logs.info(f"相等断言成功：接口实际结果：{response},等于预期结果:" + str({expected}))
            else:
                flag += 1
                logs.error(f"相等断言失败：接口实际结果：{response},不等于预期结果:" + str({expected}))
        else:
            raise TypeError('相等断言--类型错误，预期结果和接口实际响应结果必须为字典类型')
        return flag
    def no_equal_assert(self, expected, response, status_code=None):
        """
        不相等断言模式
        :param expected: 预期结果，yaml文件validation值
        :param response: 接口实际响应结果
        :param status_code: 状态码
        :return: 
        """
        flag = 0
        res_lst = []
        if isinstance(response, dict) and isinstance(expected, dict):
            for res in response:
                if list(expected.keys())[0] != res:
                    res_lst.append(res)
            for rl in res_lst:
                del response[rl]
            eq_assert = operator.eq(response,expected)
            if eq_assert:
                logs.info(f"不相等断言成功：接口实际结果：{response},不等于预期结果:" + str({expected}))
            else:
                flag += 1
                logs.error(f"不相等断言失败：接口实际结果：{response},等于预期结果:" + str({expected}))
        else:
            raise TypeError('不相等断言--类型错误，预期结果和接口实际响应结果必须为字典类型')
        return flag

    def db_assert(self):
        """数据库断言"""
        pass

    def assert_result(self, expected, response, status_code):
        """
        断言最终封装方法
        :param expected: 预期结果，也就是yaml文件里面的validation字段的值
        :param response: 接口的实际返回结果
        :param status_code: 接口的实际返回状态码
        :return:
        """
        # 0 表示表示断言成功，非0表示接口测试失败
        all_flag = 0
        try:
            logs.info(f"yaml文件的预期结果:{expected}")
            for yq in expected:
                for key, value in yq.items():
                    if key == 'contains':
                        flag = self.contains_assert(value, response, status_code)
                        all_flag = all_flag + flag
                    elif key == 'eq':
                        flag = self.equal_assert(value, response)
                        all_flag = all_flag + flag
                    elif key == 'ne':
                        flag = self.no_equal_assert(value, response)
                        all_flag = all_flag + flag
                    else:
                        logs.error("不支持{key}这种断言方式!")
            # assert all_flag == 0
            # logs.info("测试成功")
        except Exception as e:
            logs.error("请检查断言字段是否包含在接口的返回值中")
            logs.error(f"异常信息:{e}")
            raise e
        if all_flag == 0:
            logs.info("测试成功")
            assert True
        else:
            logs.error("测试失败")
            assert False


