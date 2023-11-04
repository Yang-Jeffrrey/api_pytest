import os.path
import sys
import logging

# 设置日志级别
LOG_LEVEL = logging.DEBUG

# 设置控制台日志级别
STREAM_LOG_LEVEL = logging.DEBUG

DIR_PATH = os.path.dirname(os.path.dirname(__file__))
sys.path.append(DIR_PATH)

# 文件路径设置:
FILE_PATH = {
    'YAML': os.path.join(DIR_PATH, 'testcases'),
    'CONFIG': os.path.join(DIR_PATH, 'conf/config.ini'),
    'EXTRACT': os.path.join(DIR_PATH, 'extract.yaml'),
    'LOG': os.path.join(DIR_PATH, 'logs'),
    'EXCEL': os.path.join(DIR_PATH, 'data/api.xlsx')
}
