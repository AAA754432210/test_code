# -*- coding: utf-8 -*-
'''
@Project : test_code
@File    : drc_config.py
@Author  : 王白熊
@Data    ： 2020/10/13 14:02
'''

from config.base_config import Config


class Drc_Config(Config):
    def __init__(self, drc_id, config_file='drc_config.ini'):
        super().__init__(config_file)
        self._drsu_id = drc_id
        self._host = None
        self._port = None
        self._version = None

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
