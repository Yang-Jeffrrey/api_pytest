from conf import setting
import datetime
import os
import logging
import time
from logging.handlers import RotatingFileHandler # 按文件大小滚动备份

log_path = setting.FILE_PATH['LOG']
if not os.path.exists(log_path): os.mkdir(log_path)
logfile_name = log_path + r'\test.{}.log'.format(time.strftime("%Y%m%d"))

class RecordLog:
    """日志模块"""

    def __init__(self):
        self.handle_overdue_log()

    def handle_overdue_log(self):
        """处理过期日志文件"""
        #获取系统的当前时间
        now_time = datetime.datetime.now()
        # 日期偏移30天，最多保留30天的日志文件，超过自动清理
        offset_date = datetime.timedelta(days=-30)
        # 获取前一天的时间戳
        before_date = (now_time + offset_date).timestamp()
        # 找到目录下的文件
        files = os.listdir(log_path)
        for file in files:
            if os.path.splitext(file)[1]:
                filepath = log_path + "\\" + file
                file_create_time = os.path.getctime(filepath) # 获取文件创建时间，返回时间戳
                if file_create_time < before_date:
                    os.remove(filepath)
                else:
                    continue

    def output_logging(self):
        logger = logging.getLogger(__name__)
        # 防止重复打印日志
        if not logger.handlers:
            logger.setLevel(setting.LOG_LEVEL)
            log_format = logging.Formatter(
                '%(levelname)s - %(asctime)s - %(filename)s:%(lineno)d -[%(module)s:%(funcName)s] - %(message)s')
            # 日志输出指定文件，滚动备份日志
            fn = RotatingFileHandler(filename=logfile_name, mode='a', maxBytes=5242800,
                                     backupCount=7, encoding='utf-8')  # maxBytes：控制单个日志文件的大小，单位为字节， backupCount：用于控制日志文件的数量
            fn.setLevel(setting.LOG_LEVEL)
            fn.setFormatter(log_format)
            # 将相应的handler添加在logger对象中
            logger.addHandler(fn)

            # 输出到控制台
            sh = logging.StreamHandler()
            sh.setLevel(setting.STREAM_LOG_LEVEL)
            sh.setFormatter(log_format)
            logger.addHandler(sh)
        return logger

apilog = RecordLog()
logs = apilog.output_logging()
