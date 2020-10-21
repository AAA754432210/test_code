# -*- coding: utf-8 -*-
'''
@Project : test_code
@File    : drsu_config.py
@Author  : 王白熊
@Data    ： 2020/10/12 19:32
'''

from config.base_config import Config
from common.Log import Logger

logger = Logger('Drsu_Config').getlog()


class Drsu_Config(Config):
    def __init__(self, drsu_id, config_file='drsu_config.ini'):
        super().__init__(config_file)
        self._drsu_id = drsu_id
        self._host = None
        self._port = None
        self._version = None
        self._data_period = None
        self._alarm_period = None
        self._log_file = None
        self._ai_file = None
        self._ai_livox_file = None
        self._camera_file = None

    @property
    def host(self):
        if not self._host:
            self._host = self.get_value(self._drsu_id, 'host')
        return self._host

    @host.setter
    def host(self, value):
        self._host = value

    @property
    def port(self):
        if not self._port:
            self._port = self.get_value(self._drsu_id, 'port')
        return self._port

    @port.setter
    def port(self, value):
        self._port = value

    @property
    def version(self):
        if not self._version:
            self._version = self.get_value(self._drsu_id, 'version')
        return self._version

    @version.setter
    def version(self, value):
        self._version = value

    @property
    def data_period(self):
        if not self._data_period:
            self._data_period = self.get_value(self._drsu_id, 'data_period')
        return self._data_period

    @data_period.setter
    def data_period(self, value):
        self._data_period = value

    @property
    def alarm_period(self):
        if not self._alarm_period:
            self._alarm_period = self.get_value(self._drsu_id, 'alarm_period')
        return self._alarm_period

    @alarm_period.setter
    def alarm_period(self, value):
        self._alarm_period = value

    @property
    def log_file(self):
        if not self._log_file:
            self._log_file = self.get_value(self._drsu_id, 'log_file')
        return self._log_file

    @log_file.setter
    def log_file(self, value):
        self._log_file = value

    @property
    def ai_file(self):
        if not self._ai_file:
            self._ai_file = self.get_value(self._drsu_id, 'ai_file')
        return self._ai_file

    @ai_file.setter
    def ai_file(self, value):
        self._ai_file = value

    @property
    def ai_livox_file(self):
        if not self._ai_livox_file:
            self._ai_livox_file = self.get_value(self._drsu_id, 'ai_livox_file')
        return self._ai_livox_file

    @ai_livox_file.setter
    def ai_livox_file(self, value):
        self._ai_livox_file = value

    @property
    def camera_file(self):
        if not self._camera_file:
            self._camera_file = self.get_value(self._drsu_id, 'camera_file')
        return self._camera_file

    @camera_file.setter
    def camera_file(self, value):
        self._camera_file = value

    def __getattr__(self, item):
        try:
            return self.get_value(self._drsu_id, item)
        except:
            logger.warning('没有在drsu_config.ini配置文件中找到%s元素' % item)
            return None


if __name__ == '__main__':
    drsu_id = '820020021'
    A = Drsu_Config(drsu_id)
    # A.add_value({drsu_id: {'log_file': '/dr/drsu_' + str(drsu_id) + '/DR_APP/log.txt',
    #                                           'ai_file': '/dr/drsu_' + str(drsu_id) + '/config/perception_ai/conf/perception_ai.conf',
    #                                             'ai_livox_file': '/dr/drsu_' + str(drsu_id) + '/config/perception_ai/conf/perception_ai_livox.conf',
    #                                             'camera_file': '/dr/drsu_' + str(drsu_id) + '/config/perception_ai/conf/dag_single_camera.config'}})
    # A.add_value({drsu_id: {'host': '172.18.10.220', 'port': '22'}})
    print(A.drsu_file_name)
    # print(A.port)
