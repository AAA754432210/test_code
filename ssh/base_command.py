# -*- coding: utf-8 -*-
import time
from common.Log import Logger
from ssh.operator_shell import OperatorShell

logger = Logger("BaseCommand").getlog()


class BaseCommand(OperatorShell):
    def __init__(self, host, port, username, password):
        super().__init__(host, port, username, password)

    # 删除文件 使用小心！
    def del_file(self, file_path):
        command = 'rm -rf ' + file_path
        self.exec_command_no_readout(command)

    # 查找指定文件指定字符串
    def query_str(self, file_name, query_str):
        query_command = 'cat ' + file_name + ' | grep ' + query_str
        ret_str = self.exec_command_retstr(query_command)
        logger.debug('输入命令：%s,\r\n 返回值:%s' % (query_command, ret_str))
        return ret_str

    # 修改指定文件指定字符串
    def replace_str(self, file_name, old_str, new_str, is_replace_all=True, is_replace_id=False):
        # 如果查询不到待修改字符串直接返回
        if old_str == new_str:
            logger.debug('文件%s无需修改' % file_name)
            return True
        if not self.query_str(file_name, old_str):
            if self.query_str(file_name, new_str):
                logger.debug('文件:%s无需修改' % file_name)
                return True
            logger.debug('文件%s待修改字符串%s未找到' % (file_name, old_str))
            return False
        if is_replace_all:
            sub_command = ("s#%s#%s#g" % (old_str, new_str))
        else:
            # 只匹配第一个
            if is_replace_id:
                sub_command = ("0,/%s/s/%s/%s/" % (old_str, old_str, new_str))
            else:
                sub_command = ("0,#%s#s#%s#%s#" % (old_str, old_str, new_str))
        set_command = ('sed -i ' + ' " ' + sub_command + ' " ' + file_name)
        self.exec_command_no_readout(set_command)
        if self.query_str(file_name, old_str) or not self.query_str(file_name, new_str):
            return False
        logger.info('文件%s中的字符串%s被替换为%s' % (file_name, old_str, new_str))
        return True

    # 执行scp命令
    def remote_shell_sudo(self, command, remote_password=None):
        self.send_command('pwd')
        remote_password = remote_password if remote_password else self._password
        str1 = self.send_command_middle(command)
        time.sleep(0.5)
        if "password for" in str1:
            str1 = self.send_command_middle(self._password)
            logger.info('输入本地密码')
        time.sleep(0.5)
        if 'Are you sure you want to continue connecting (yes/no)' in str1:
            str1 = self.send_command_middle('yes')
            logger.info('输入yes')
        time.sleep(0.5)
        if 'password' in str1 and '@' in str1:
            logger.info('输入远端密码')
            str1 = self.send_command(remote_password)
        if 'Permission denied, please try again' in str1:
            str1 = self.send_command_middle(self._password)
        logger.debug('命令：%s 执行结束' % command)

    # 检查是否拷贝成功 607610540
    def check_scp(self, file_path, size=None):
        # command = "ls -l /dr/dr.tar.gz | awk '{print $5}'"
        command = "ls -l " + file_path + " | awk '{print $5}'"
        str1 = self.exec_command_retstr(command)
        if not size or size == int(str1):
            logger.info('拷贝成功,大小：%s' % str1)
            return True
        else:
            logger.info('拷贝失败,目标大小：%s,实际大小:%s' % (size, str1))
            return False
