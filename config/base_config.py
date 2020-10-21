# -*- coding: utf-8 -*-
from configparser import ConfigParser
import os


class Config:
    def __init__(self, config_file):
        """
        初始化
        config_file:待读取的配置文件名称
        """
        self.config = ConfigParser()
        self.conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), config_file)
        if not os.path.exists(self.conf_path):
            raise FileNotFoundError("请确保配置文件:%s存在！" % self.conf_path)
        self.config.read(self.conf_path, encoding='utf-8')

    def get_sections(self):
        """
        获取配置文件的所有section
        :return:
        """
        return self.config.sections()

    def get_options(self, section_name):
        """
        获取指定section的所有option
        :param section_name:
        :return:
        """
        if self.config.has_section(section_name):
            return self.config.options(section_name)
        else:
            raise ValueError(section_name)

    def get_value(self, section, option):
        """
        获取字符串类型的选项值
        :param section:
        :param option:
        :return:
        """
        return self.config.get(section, option)

    def get_int(self, section, option):
        """
        获取整数类型的选项值
        :param section:
        :param option:
        :return:
        """
        return self.config.getint(section, option)

    def get_float(self, section, option):
        """
        获取浮点类型的选项值
        :param section:
        :param option:
        :return:
        """
        return self.config.getfloat(section, option)

    def get_boolean(self, section, option):
        """
        获取布尔类型的选项值
        :param section:
        :param option:
        :return:
        """
        return self.config.getboolean(section, option)

    def get_eval_data(self, section, option):
        """
        获取内置类型的选项值
        :param section:
        :param option:
        :return:
        """
        return eval(self.config.get(section, option))

    @staticmethod
    def write_value(filename, data):
        """
        定义一个写入配置文件的方法
        :param filename: 配置文件名
        :param data: 嵌套字典的字典，键为区域名，嵌套的区域值为选项名和选项值的字典
        :return:
        """
        config = ConfigParser()
        if isinstance(data, dict):
            for key in data:
                config[key] = data[key]
            # 创建一个配置文件并将获取到的配置信息使用配置文件对象的写入方法进行写入
            with open(filename, mode='w', encoding='utf-8') as f:
                config.write(f)

    def add_value(self, dict_data):
        """
        定义一个写入配置文件的方法
        :param filename: 配置文件名
        :param data: 嵌套字典的字典，键为区域名，嵌套的区域值为选项名和选项值的字典
        :return:
        """
        if isinstance(dict_data, dict):
            for key, value in dict_data.items():
                for key1, value1 in value.items():
                    self.config.set(key, key1, value1)
            # 创建一个配置文件并将获取到的配置信息使用配置文件对象的写入方法进行写入
            self._update_cfg_file()

    def add_new_section(self, section_name):
        """
        增加section
        :param section_name:
        :return:
        """
        if not self.config.has_section(section_name):
            self.config.add_section(section_name)
            self._update_cfg_file()

    def add_option(self, section_name, option_key, option_value):
        """
        增加指定section下option
        :param section_name:
        :param option_key:
        :param option_value:
        :return:
        """
        if self.config.has_section(section_name):
            self.config.set(section_name, option_key, option_value)
            self._update_cfg_file()

    def del_section(self, section_name):
        """
        删除指定section
        :param section_name:
        :return:
        """
        if self.config.has_section(section_name):
            self.config.remove_section(section_name)
            self._update_cfg_file()

    def del_option(self, section_name, option_name):
        """
        删除指定section下的option
        :param section_name:
        :param option_name:
        :return:
        """
        if self.config.has_option(section_name, option_name):
            self.config.remove_option(section_name, option_name)
            self._update_cfg_file()

    def _update_cfg_file(self):
        with open(self.conf_path, "w") as f:
            self.config.write(f)

if __name__ == '__main__':
    # cf = Config('drsu_config.ini')
    A = Config('common_config.ini')
    data = {'8200': {'host': '172.16.20.11'}, '8100': {'host': '10.10.10.30'}, '8101': {'host': '10.10.10.11'}}
    A.write_value('drc_config.ini', data)
    # print(cf.read_dir())
    # print(cf.read_email())
