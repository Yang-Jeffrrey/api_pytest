import configparser
from conf.setting import FILE_PATH

class OperationConfig(object):
    def __init__(self, file_path=None):
        if file_path is None:
            self.__file_path = FILE_PATH['CONFIG']
        else:
            self.__file_path = file_path
        self.conf = configparser.ConfigParser()
        try:
            self.conf.read(self.__file_path, encoding='utf-8')
        except Exception as e:
            print(e)

    def get_section_for_data(self, section, option):
        try:
            values = self.conf.get(section, option)
            return values
        except Exception as e:
            print(e)

    def get_api_host(self):
        return self.get_section_for_data('api_envi', 'host')

    def get_section_mysql(self, option):
        return self.get_section_for_data('MYSQL', option)

    def get_section_redis(self, option):
        return self.get_section_for_data('REDIS', option)

    def get_section_jenkins(self, option):
        return self.get_section_for_data('JENKINS', option)