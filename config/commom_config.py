# -*- coding: utf-8 -*-
'''
@Project : test_code
@File    : commom_config.py
@Author  : 王白熊
@Data    ： 2020/10/12 20:03
'''


from config.base_config import Config


class Common_Config(Config):
    def __init__(self, config_file='common_config.ini'):
        super().__init__(config_file)
        self._username = None
        self._password = None

    @property
    def username(self):
        if not self._username:
            self._username = self.get_value('user', 'username')
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def password(self):
        if not self._password:
            self._password = self.get_value('user', 'password')
        return self._password

    @password.setter
    def password(self, value):
        self._password = value


if __name__ == '__main__':
    A = Common_Config()
    print(A.username)
    print(A.password)