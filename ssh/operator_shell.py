# -*- coding: utf-8 -*-

import paramiko
import time
from common.Log import Logger

logger = Logger("OperatorShell").getlog()


class OperatorShell(object):
    def __init__(self, host, port, username, password):
        self._host = host
        self._port = port if port else 22
        self._username = username
        self._password = password
        self._transport = None
        self._sftp = None
        self._channel = None
        self._client = None
        # 等待超时时间
        self.timeout = 3600
        # 连接失败的重试次数
        self.try_times = 3

    def _connect(self):
        while True:
            try:
                self._transport = paramiko.Transport((self._host, self._port))
                # 用户名密码方式
                self._transport.connect(username=self._username, password=self._password)
                # 打开一个通道
                self._channel = self._transport.open_session()
                self._channel.settimeout(self.timeout)
                # 获取一个终端
                self._channel.get_pty()
                # 激活
                self._channel.invoke_shell()
                logger.warning(u'连接%s成功' % self._host)
                return
            except Exception as e:
                if self.try_times != 0:
                    logger.warning(u'连接%s失败，进行重试' % self._host)
                    self.try_times -= 1
                else:
                    logger.warning(u'重试3次失败，结束程序')
                    exit(1)

    def reconnect(self):
        self._connect()

    def send_command(self, cmd):
        result = ''
        # 发送要执行的命令
        self._channel.send(cmd + '\r')
        # 回显很长的命令可能执行较久，通过循环分批次取回回显
        while True:
            time.sleep(0.2)
            ret = self._channel.recv(65535)
            try:
                ret = ret.decode('utf-8')
            except:
                ret = ret.decode('gbk')
            result += ret
            if ret.endswith(r'$ '):
                break
        logger.debug('输入命令：%s,回显结果：%s' % (cmd, result))
        return result

    # 命令执行到一半需要输入信息，输入完成后继续
    def send_command_middle(self, cmd):
        # 发送要执行的命令
        self._channel.send(cmd + '\r')
        # 回显很长的命令可能执行较久，通过循环分批次取回回显
        time.sleep(0.5)
        ret = self._channel.recv(65535)
        try:
            ret = ret.decode('utf-8')
        except:
            ret = ret.decode('gbk')
        logger.debug('输入命令：%s, 回显结果：%s' % (cmd, ret))
        return ret

    # 带pty执行命令 可以不用再次输入命令
    def exec_command_retstr(self, command, get_pty=False):
        if self._client is None:
            self._client = paramiko.SSHClient()
            self._client._transport = self._transport
        stdin, stdout, stderr = self._client.exec_command(command, get_pty=get_pty)
        data = stdout.read()
        logger.debug('输入命令：%s，回显：%s' % (command, data.decode('utf-8')))
        return data.decode('utf-8')

    # 执行命令
    def exec_command_no_readout(self, command):
        if self._client is None:
            self._client = paramiko.SSHClient()
            self._client._transport = self._transport
        self._client.exec_command(command)
        logger.debug('输入命令：%s' % command)

    # 下载
    def download(self, remotepath, localpath):
        if self._sftp is None:
            self._sftp = paramiko.SFTPClient.from_transport(self._transport)
        self._sftp.get(remotepath, localpath)
        logger.debug('从远端：%s下载文件到：%s' % (remotepath, localpath))

    # 上传
    def put(self, localpath, remotepath):
        if self._sftp is None:
            self._sftp = paramiko.SFTPClient.from_transport(self._transport)
        self._sftp.put(localpath, remotepath)
        logger.debug('从本地：%s上传文件到：%s' % (localpath, remotepath))

    def _mkdir(self, dir_path):
        if self._client is None:
            self._client = paramiko.SSHClient()
            self._client._transport = self._transport
        sftp = self._client.open_sftp()
        sftp.mkdir(dir_path)
        logger.debug('新建文件夹：%s', dir_path)

    def close(self):
        logger.warning('连接关闭')
        if self._transport:
            self._transport.close()
            self._transport = None
        if self._client:
            self._client.close()
            self._client = None
        if self._channel:
            self._channel.close()
            self._channel = None


if __name__ == '__main__':
    ssh = OperatorShell('172.18.10.220', 22, 'broadxt', 'broadxt333')
    ssh._connect()
