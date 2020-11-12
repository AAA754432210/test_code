# -*- coding: utf-8 -*-
'''
@Project : test_code
@File    : web_config.py
@Author  : 王白熊
@Data    ： 2020/10/13 16:35
'''

from config.base_config import Config
from common.Log import Logger

logger = Logger('Web_Config').getlog()


class Web_Config(Config):
    def __init__(self, config_file='web_config.ini'):
        super().__init__(config_file)

    @property
    def username(self):
        return self.get_value('user', 'username')

    @property
    def password(self):
        return self.get_value('user', 'password')

    @property
    def browserName(self):
        return self.get_value('browserType', 'browserName')

    @property
    def headless(self):
        return self.get_value('browserType', 'headless')

    @property
    def url(self):
        print('get url')
        return self.get_value('testServer', 'url')

    def __getattr__(self, item):
        try:
            print('get_wth')
            return self.get_value('testServer', item)
        except:
            logger.warning('没有在web_config.ini配置文件中找到%s元素' % item)


if __name__ == '__main__':
    A = Web_Config()
    print(A.url)
    print(A.asd)
