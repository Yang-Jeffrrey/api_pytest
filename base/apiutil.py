import json
import re

import allure
import jsonpath

from common.operyaml import get_testcase_yaml, ReadYamlData
from conf.setting import FILE_PATH
from common.sendrequests import SendRequests
from conf.operationConfig import OperationConfig
from common.debugtalk import DebugTalk
from common.recordlog import logs
from common.assertion import Assertions
from json.decoder import JSONDecodeError
class RequestBase:


    def __init__(self):
        self.run = SendRequests()
        self.conf = OperationConfig()
        self.read = ReadYamlData()
        self.asserts = Assertions()

    def replace_load(self, data):
        """yaml数据替换解析"""
        str_data = data
        if not isinstance(data, str):
            str_data = json.dumps(data, ensure_ascii=False)
        for i in range(str_data.count('${')):
            if '${' in str_data and '}' in str_data:
                start_index = str_data.index('${')
                end_index = str_data.index('}', start_index)
                ref_all_params = str_data[start_index:end_index+1]
                #取出yaml文件的函数名
                func_name = ref_all_params[2:ref_all_params.index("(")]
                #去除函数里面的参数
                func_params = ref_all_params[ref_all_params.index("(")+1:ref_all_params.index(")")]
                # 传入替换的参数获取对应的值，类的反射：getattr,setattr
                extract_data = getattr(DebugTalk(), func_name)(*func_params.split(',') if func_params else "")
                if extract_data and isinstance(extract_data, list):
                    extract_data = ','.join(e for e in extract_data)
                str_data = str_data.replace(ref_all_params, str(extract_data))
        #还原数据
        if data and isinstance(data, dict):
            data = json.loads(str_data)
        else:
            data = str_data
        return data


    def specification_yaml(self, base_info, test_case):
        """
        接口请求处理基本方法
        :param base_info: yaml文件里面的baseInfo
        :param test_case:  yaml文件里面的testCase
        :return:
        """
        try:
            params_type = ['data', 'json', 'params']
            url_host = self.conf.get_api_host()
            api_name = base_info['api_name']
            allure.attach(api_name, f'接口名称{api_name}', allure.attachment_type.TEXT)
            url = url_host + base_info['url']
            allure.attach(api_name, f'接口名称{url}', allure.attachment_type.TEXT)
            method = base_info['method']
            allure.attach(api_name, f'请求方式{method}', allure.attachment_type.TEXT)
            header = self.replace_load(base_info['header'])
            allure.attach(api_name, f'请求头{str(header)}', allure.attachment_type.TEXT)
            cookie = None
            if base_info.get('cookies') is not None:
                cookie = eval(self.replace_load(base_info['cookies']))
                allure.attach(str(cookie), 'cookie', allure.attachment_type.TEXT)
            case_name = test_case.pop('case_name')
            allure.attach(api_name, f'测试用例名称{case_name}', allure.attachment_type.TEXT)
            # 断言结果替换解析
            val = self.replace_load(test_case.get('validation'))
            test_case['validation'] = val
            # 处理当断言结果为字符串形式的列表格式，使用eval函数转换为list类型
            validation = eval(test_case.pop('validation'))
            allure_validation = str([str(list(i.values()))for i in validation])
            allure.attach(allure_validation, "预期结果", allure.attachment_type.TEXT)
            # 处理参数提取
            extract = test_case.pop('extract', None)
            extract_list = test_case.pop('extract_list', None)
            for key, value in test_case.items():
                if key in params_type:
                    test_case[key] = self.replace_load(value)
                else:
                    logs.error("yaml文件的请求参数类型只能设置--params, data,json")
            # 处理文件上传接口
            file, files = test_case.pop('files', None), None
            if file is not None:
                for fk, fv in file.items():
                    allure.attach(json.dumps(file), 'load')
                    files = {fk: open(fv, mode='rb')}
            res = self.run.run_main(name=api_name, url=url, case_name=case_name, header=header,
                                    method=method, cookies=cookie, file=files, **test_case)
            status_code = res.status_code
            allure.attach(res.text, f'接口返回结果{res.text}', allure.attachment_type.TEXT)
            try:
                res_json = json.loads(res.text) # 把Json格式转换成字典类型
                if extract is not None:
                    self.extract_data(extract, res.text)
                if extract_list is not None:
                    self.extract_data_list(extract_list, res.text)
                # 处理断言
                self.asserts.assert_result(validation, res_json, status_code)
            except JSONDecodeError as js:
                logs.error("系统异常或接口未请求！")
                raise js
        except Exception as e:
            logs.error(e)
            raise e
    def extract_data(self, testcases_extract, response):

        """
        提取接口的返回值，支持正则表达式和json提取器
        :param testcases_extract: testcases文件yaml文件中的extract值
        :param response: 接口的实际返回值
        :return:
        """
        # 处理正则表达式提取
        pattern_lst = ['(.*?', '(.+?)', r'(\d)', r'(\d*)']
        try:
            for key, value in testcases_extract.items():
                for pat in pattern_lst:
                    if pat in value:
                        ext_lst = re.search(value, response)
                        if pat in [r'(\d+)', r'(\d*)']:
                            extract_data = {key: int(ext_lst.group(1))}
                            self.read.write_yaml_data ( extract_data )
                        else:
                            extract_data = {key: ext_lst.group(1)}
                            self.read.write_yaml_data ( extract_data )

               # 处理json提取参数
                if '$' in value:
                    ext_json = jsonpath.jsonpath(json.loads(response), value)[0]
                    if ext_json:
                        extract_data = {key: ext_json}
                        self.read.write_yaml_data(extract_data)
                    else:
                        extract_data = {key: '未提取到数据，请检查接口返回值是否为空！'}
                        self.read.write_yaml_data(extract_data)
        except Exception as e:
            logs.error(e)

    def extract_data_list(self, testcases_extract_list, response):

            """
            提取多个参数，支持正则表达式和json提取，提取结果以列表形式返回
            :param testcases_extract_list: testcases文件yaml文件中的extract_list信息
            :param response: 接口的实际返回值,str类型
            :return:
            """
            try:
                for key, value in testcases_extract_list.items():
                    if "(.+?)" in value or "(.*?)" in value:
                        ext_list = re.findall(value, response, re.S)
                        if ext_list:
                            extract_data = {key: ext_list}
                            logs.info('正则提取的参数： %s' % extract_data)
                            self.read.write_yaml_data(extract_data)
                    if "$" in value:
                        #增加提取判断，有些返回结果为空提取不到，给一个默认值
                        ext_json = jsonpath.jsonpath(json.loads(response), value)
                        if ext_json:
                            extract_data = {key: ext_json}
                        else:
                            extract_data = {key: '未提取到数据，请检查接口返回值是否为空！'}
                        logs.info('json提取参数： %s' % extract_data)
                        self.read.write_yaml_data(extract_data)
            except Exception as e:
                logs.error("接口返回值提取异常，请检查yaml文件extract_list表达式是否正确!")

