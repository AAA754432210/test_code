# -*- coding: utf-8 -*-
'''
@Project : test_code
@File    : airport_expressway.py
@Author  : 王白熊
@Data    ： 2020/10/13 16:08
'''

# -*- coding: utf-8 -*-
import time
from ssh.drsu_ssh import DrsuSSHConnection
from common.Log import Logger

logger = Logger('deploy_drsu_highway').getlog()


def deploy_drsu_highway(host, is_sim, remote_path, local_path, drsu_id='16388', ):
    drsuconn = DrsuSSHConnection(drsu_id, host=host, is_sim=is_sim, drc_id='8200')
    # 從遠端服務器拷貝dr壓縮文件到當前設備
    drsuconn.scp_download(remote_path, local_path, 'broadxt333', size=476955837)
    # 解壓dr壓縮文件
    drsuconn.tar_dr()
    # 修改文件夹名 例如将/drsu/drsu_16388 修改为/drsu/drsu_${drsu_id}

    # 修改文件所有用戶為當前用戶
    drsuconn.chmod_dr()
    # 修改配置文件,參數radar
    drsuconn.chmod_cfg('820020021')
    # 修改rc.local添加設備啟動時自啟動drsu
    drsuconn.chmod_rc()

    drsuconn.is_sim = False
    drsuconn.chmod_cfg_not_sim()
    drsuconn.remote_replace_drsu_id()
    if drsuconn.remote_ps_drsu_process_num() != 0:
        # 如果有残余进程，先杀进程 然后再重新启动
        drsuconn.remote_kill()
        time.sleep(5)
    drsuconn.remote_start_drsu()
    time.sleep(30)
    if not drsuconn.is_drsu_ready():
        logger.error('真实drc环境下drsu启动不成功')
        return False

    if drsuconn.remote_ps_drsu_process_num() != 0:
        # 如果有残余进程，先杀进程 然后再重新启动
        drsuconn.remote_kill()
        time.sleep(5)
    drsuconn.remote_start_drsu()
    time.sleep(30)
    if not drsuconn.is_drsu_ready():
        logger.error('虚拟drc环境下drsu启动不成功')
        return False

    drsuconn.close()


if __name__ == '__main__':
    deploy_drsu_highway('172.18.10.220', is_sim=True,
                        remote_path='broadxt@172.16.20.17:/home/broadxt/Downloads/dr.tar.gz',
                        local_path='/dr')
