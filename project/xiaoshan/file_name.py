# -*- coding: utf-8 -*-
'''
@Project : test_code
@File    : file_name.py
@Author  : 王白熊
@Data    ： 2020/10/13 14:12
'''

from common.weather import get_cur_weather
from common.Log import Logger
import time

logger = Logger('FilePath').getlog()


class FilePath(object):
    def __init__(self, drsu_id):
        self._drsu_id = drsu_id

    def get_dev(self):
        if str(self._drsu_id) in ['9', '19', '26']:
            dev = '_1camera_1inno'
        else:
            dev = '_1camera'
        return dev

    def get_tar_file_name(self):
        weather = get_cur_weather()
        dev = self.get_dev()
        cur_time = time.strftime("%Y%m%d%H%M", time.localtime())
        file_name = 'drsu' + str(self._drsu_id) + '_' + cur_time + '_' + weather + dev + '.tar.gz'
        logger.info('压缩文件名：%s' % file_name)
        return file_name
        # drsu1_202008181406_rain_1camera_inno.tar.gz

    def get_input_dir(self):
        file_name = self.get_tar_file_name()
        input_file_path = '/dr/drsu_' + str(self._drsu_id) + '/DR_APP/' + file_name
        logger.info('压缩文件全路径：%s' % input_file_path)
        return input_file_path

    def get_data_dir(self):
        today = time.strftime("%Y%m%d", time.localtime())
        data_name = '/dr/drsu_' + str(self._drsu_id) + '/DR_APP/drsu_data/' + today
        return data_name


if __name__ == '__main__':
    A = FilePath('16388')
    A.get_input_dir()
