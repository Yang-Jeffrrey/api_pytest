import json

import allure
import pytest
import requests
import logs

from common.recordlog import logs
from common.operyaml import ReadYamlData
from requests import utils


class SendRequests:

    def __init__(self):
        self.read = ReadYamlData()

    def send_requests(self, **kwargs):
        cookie = {}
        session = requests.session()
        result = session.request(**kwargs)
        try:
            set_cookie = requests.utils.dict_from_cookiejar(result.cookies)
            if set_cookie:
                cookie['Cookie'] = set_cookie
                self.read.write_yaml_data(cookie)
                logs.info("cookies: %s" % cookie)
            logs.info("接口返回信息：%s" % result.text if result.text else result)
        except requests.exceptions.ConnectionError:
            logs.error("ConnectionError--连接异常")
            pytest.fail("接口请求异常，可能是request的连接数过多或请求速度过快导致程序报错！")
        except requests.exceptions.HTTPError:
            logs.error("HTTPError--http异常")
        except requests.exceptions.RequestException as e:
            logs.error(e)
            pytest.fail("请求异常，请检查系统或数据是否正常!")

        return result

    def run_main(self, name, url, case_name, header, method, cookies=None, file=None, **kwargs):
        try:
            # 收集报告日志信息
            logs.info('接口名称:{}'.format(name))
            logs.info('接口请求地址:{}'.format(url))
            logs.info('测试用例名称:{}'.format(case_name))
            logs.info('请求头:{}'.format(header))
            logs.info('cookie:{}'.format(cookies))
            req_params = json.dumps(kwargs, ensure_ascii=False)
            if 'data' in kwargs.keys():
                allure.attach(req_params, '请求参数', allure.attachment_type.TEXT)
                logs.info("请求参数{}".format(kwargs))
            elif 'json' in kwargs.keys():
                allure.attach(req_params, '请求参数', allure.attachment_type.TEXT)
                logs.info("请求参数{}".format(kwargs))
            elif 'params' in kwargs.keys():
                allure.attach(req_params, '请求参数', allure.attachment_type.TEXT)
                logs.info("请求参数{}".format(kwargs))
            response = self.send_requests(method=method, url=url, headers=header, cookies=cookies, files=file, **kwargs)
            print(response.status_code)
            return response

        except Exception as e:
            logs.error(e)
