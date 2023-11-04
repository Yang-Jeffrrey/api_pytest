import os.path

from common.recordlog import logs
from conf import setting
import xml
import xlrd
import xlwt


class HandlerExcel:

    def __init__(self, file_path=None):
        if file_path is not None:
            self.file_path = file_path
        else:
            self.file_path = setting.FILE_PATH['EXCEL']
        self.__global_table = self.xls_obj()
    def xls_obj(self):
        """获取Excel文件的对象，后续都通过这个对象去操作Excel的数据"""
        if os.path.splitext(self.file_path)[-1] != '.xlsx':
            obj = xlrd.open_workbook(self.file_path, formatting_info=True)
            xls_obj = obj.sheet()[1]
            return xls_obj
        else:
            logs.info("Excel文件必须是.xls格式!")

    def get_cols(self):
        """获取Excel的总列数"""
        return self.__global_table.ncols

    def get_rows(self):
        """获取Excel的总行数"""
        return self.__global_table.nrows

    def get_cell_values(self, row, col):
        """
        获取Excel单元的数据
        :param row: Excel行数，索引从0开始，第一行索引0，
        :param col: Excel列数，索引从0开始，第一行索引0，
        :return:
        """
        return self.__global_table.cell_value(row, col)

    def get_each_line(self, row):
        """
        获取Excel一整行的数据
        :param row: 行数
        :return: 返回一整行数据
        """
        rows_data = self.__global_table.row_values(row)
        return rows_data

    def get_each_colum(self, col):
        """
        获取Excel一整列的数据
        :param col: 列数，索引从0开始
        :return: 返回List格式数据
        """
        cols_data = self.__global_table.col_values(col)
        return cols_data

    def write_xls_value(self, row, col, value):
        """
        往Excel文件先写入数据
        :param row: 行数，索引从0开始
        :param col: 列数，索引从0开始
        :param value: 写入数据
        :return:
        """
        try:
            init_table = xlrd.open_workbook(self.file_path, formatting_info=True)
            copy_table = copy(init_table)
            sheet = copy_table.get_sheet(1)
            sheet.write(row, col, value)
            copy_table.save(self.file_path)
        except PermissionError:
            logs.error("请关闭Excel文件再操作!")
            exit()
