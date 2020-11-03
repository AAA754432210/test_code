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

    # 判断文件是否存在
    def is_exist_file(self, file_path):
        command = 'ls {} | wc -l'.format(file_path)
        if int(self.exec_command_retstr(command)) != 0:
            return True
        else:
            return False

    # 获取文件大小
    def get_file_size(self, file_path):
        command = "ls -l " + file_path + " | awk '{print $5}'"
        return int(self.exec_command_retstr(command))

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

    # 执行带sudo等需要交互的命令
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
        if not self.is_exist_file(file_path):
            return False
        size_ = self.get_file_size(file_path)
        if not size or size == size_:
            logger.info('拷贝成功,大小：%s' % size_)
            return True
        else:
            logger.info('拷贝失败,目标大小：%s,实际大小:%s' % (size, size_))
            return False

    def cp(self, src_file, dest_file, force=True, check_size=False, mode=0):
        if not self.is_exist_file(src_file):
            logger.info('拷贝失败：源文件：%s不存在' % src_file)
            return True
        if not force and self.is_exist_file(dest_file):
            logger.info('文件：%s已存在，无序拷贝' % dest_file)
            return True
        size1 = self.get_file_size(src_file)
        if mode == 0:
            action = 'cp'
        elif mode == 1:
            action = 'mv'
        else:
            logger.info('不支持的文件移动命令')
            return True
        command = '{} {} {}'.format(action, src_file, dest_file)
        self.send_command(command)
        if check_size:
            return self.check_scp(dest_file, size1)
        else:
            return self.is_exist_file(dest_file)
