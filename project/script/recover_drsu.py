# -*- coding: utf-8 -*-
"""
@Project : ssh
@File    : recover_drsu_env.py
@Author  : 王白熊
@Data    ： 2020/10/28 18:57
"""
import threading
import os
import time
from ssh.drsu_ssh import DrsuSSHConnection
from common.Log import Logger

logger = Logger('recover_drsu').getlog()
# 02,12, 14, 21, 24,27
# 25 10
#
drsu_dict = ['810020004', ]
version_demon = 'dr_drsu_3.2.0_Release-build-3169_1015.gz'


def recover_drsu_single(drsu_id):
    drsuconn = DrsuSSHConnection(drsu_id, False, '0')
    # 直接将配置文件替换
    drsuconn.chmod_cfg()
    # dr_drsu_3.2.0_Release-build-3169_1015.gz 演示版本，dr_drsu_3.2.0_Release-build-3233.gz测试版本
    drsuconn.set_update_version(version_demon)
    if drsuconn.remote_ps_drsu_process_num() != 0:
        # 如果有残余进程，先杀进程 然后再重新启动
        drsuconn.remote_kill()
        time.sleep(30)
    drsuconn.remote_start_drsu()
    time.sleep(100)
    if drsuconn.is_drsu_ready():
        logger.info('drsu:%s启动成功' % drsu_id)
        drsuconn.close()
        return True
    else:
        logger.info('drsu:%s启动失败' % drsu_id)
        drsuconn.close()
        return False
    # 修改配置文件


def bk_drsu_sigble(drsu_id):
    drsuconn = DrsuSSHConnection(drsu_id, False, '0')
    # if drsuconn.is_drsu_ready():
    drsuconn.bk_cfg()
    drsuconn.close()


def set_version(drsu_id, version):
    drsuconn = DrsuSSHConnection(drsu_id, False, '0')
    drsuconn.set_update_version(version)
    drsuconn.close()


def mod_cfg(drsu_id):
    drsuconn = DrsuSSHConnection(drsu_id, False, '0')
    drsuconn.chmod_cfg()
    drsuconn.close()


def start_drsu(drsu_id):
    drsuconn = DrsuSSHConnection(drsu_id, False, '0')
    if not drsuconn.is_drsu_ready():
        drsuconn.remote_start_drsu()
        time.sleep(30)
        drsuconn.is_drsu_ready()


def main():
    # from argparse import ArgumentParser
    # arg_parser = ArgumentParser()
    # arg_parser.add_argument('--drsu', help='drsu_id')
    # arg_parser.add_argument('--mode', required=False, default=0, type=int,
    #                         help='the type of operation, 0:recover; 1:backup cfg; 2:mod version; 3:jpeg2video,')
    # arg_parser.add_argument('--version', required=False, default=1920, type=int, help='designated drsu version')
    # args = arg_parser.parse_args()
    # target = bk_drsu_sigble

    for i in drsu_dict:
        t = threading.Thread(target=recover_drsu_single, args=(i,))
        t.start()
        time.sleep(5)


if __name__ == '__main__':
    main()
