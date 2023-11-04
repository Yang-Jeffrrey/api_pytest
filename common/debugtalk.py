import random
import re

from common.operyaml import get_testcase_yaml,ReadYamlData
import datetime

class DebugTalk:

    def __init__(self):
        self.read = ReadYamlData()

    def get_extract_order_data(self, data, randoms):
        if randoms not in [0, -1, -2]:
            return data[randoms - 1]

    def get_extract_data(self, node_name, randoms=None):
        """
        获取extract.yaml数据
        :param node_name: extract.yaml文件中的key值
        :param sec_node_name: extract.yaml有多数据时，获取下一个node节点数据
        :param randoms: int类型：0:随机读取；-1：读取全部，返回字符串格式；-2：读取全部，返回列表形式
        :return:
        """
        data = self.read.get_extract_yaml(node_name)
        if randoms is not None and bool(re.compile(r'^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$').match(randoms)):
            randoms = int(randoms)
            data_value = {
                randoms: self.get_extract_order_data(data, randoms),
                0: random.choice(data),
                -1: ','.join(data),
                -2: ','.join(data).split(',')
            }
            data = data_value[randoms]

        return data
    def get_now_date(self):
        cur_time = datetime.datetime.now().strftime("%Y-%m-%d")
        return cur_time

    def replace_header(self, data_type):
        """动态解析头数据"""
        if data_type == 'data':
            return {' Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}

        elif data_type == 'json':
            return {' Content-Type': 'application/json;charset=UTF-8'}

    def get_params(self):
        """动态解析本体数据"""
        pass


