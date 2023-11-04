import os
import shutil

import pytest


if __name__ == '__main__':
    pytest.main(['-vs', '--alluredir=./report/temp', './testcases',  '--clean-alluredir', '--junitxml=./report/result.xml'])
    shutil.copy('./environment.xml', './report/temp')
    os.system(f'allure serve ./report/temp')

