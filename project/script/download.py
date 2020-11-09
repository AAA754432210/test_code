# -*- coding: utf-8 -*-
"""
@Project : test_code
@File    : download.py
@Author  : 王白熊
@Data    ： 2020/11/3 20:53
"""
from ssh.drsu_ssh import DrsuSSHConnection
import time


def gather_drsu_data(drsu_id):
    drsuconn = DrsuSSHConnection(str(drsu_id), is_sim=False, drc_id=None)

    if drsuconn.remote_ps_drsu_process_num() != 0:
        # 如果有残余进程，先杀进程 然后再重新启动
        drsuconn.remote_kill()
        time.sleep(10)
    drsuconn.remote_start_drsu()
    time.sleep(100)
    if drsuconn.is_drsu_ready():
        time.sleep(100)
        drsuconn.remote_kill()
        time.sleep(10)
        drsuconn.download_data()
    else:
        drsuconn.remote_kill()