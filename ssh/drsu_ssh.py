# -*- coding: utf-8 -*-
import time
from threading import Thread
import os.path
from ssh.base_command import BaseCommand
from config.drsu_config import Drsu_Config
from config.drc_config import Drc_Config
from config.commom_config import Common_Config
from project.xiaoshan.file_name import FilePath
from common.Log import Logger
from common.baidu_upload import upload_dir

logger = Logger('DrsuSSH').getlog()
loopback = '127.0.0.1'


class DrsuSSHConnection(BaseCommand):
    def __init__(self, drsu_id, is_sim, drc_id, host=None, port=None, username=None, password=None, ):
        """
        :param drsu_id: 设备drsu_id
        :param is_sim: 是否需要注册到虚拟drc
        :param drc_id: 注册真实drc情况下的drc_id，
        :param host:
        :param port:
        :param username:
        :param password:
        """
        self._drsu_id = drsu_id
        self._is_sim = is_sim
        self._drc_id = drc_id
        self.drsu = Drsu_Config(drsu_id)
        self.common = Common_Config()
        self.drc = None
        host = host if host else self.drsu.host
        port = port if port else int(self.drsu.port)
        username = username if username else self.common.username
        password = password if password else self.common.password
        super().__init__(host, port, username, password)
        # 是否有share文件夹
        self._is_exist_share = False
        # 指的是drsu文件夹名称中的drsu_id 例如 /dr/drsu_16388 中的16388，原因是设备中这里的命名并不一定和drsuid一致
        self._drsu_file_name = self.drsu.drsu_file_name if self.drsu.drsu_file_name else drsu_id
        self.local_path = None
        self.remote_path = None
        logger.info('建立ssh连接，主机：%s，端口：%s, 账号：%s， 密码：%s, drsuid:%s '
                    % (self._host, self._port, self._username, self._password, self._drsu_id))
        self._connect()  # 建立连接

    @property
    def is_sim(self):
        return self._is_sim

    @is_sim.setter
    def is_sim(self, value):
        self._is_sim = value

    # 是否打开下载开关
    def replace_str_download_common(self, flag=True):
        if flag:
            old_str, new_str = 'enable_dump_msg=false', 'enable_dump_msg=true'
        else:
            new_str, old_str = 'enable_dump_msg=false', 'enable_dump_msg=true'
        self.replace_str(self.drsu.ai_livox_file, old_str, new_str)
        self.replace_str(self.drsu.ai_file, old_str, new_str)

    def replace_str_download(self, flag=True):
        # 先判断是否有挂载盘
        comand = 'ls /home/share'
        ret_bool = self.exec_command_retstr(comand)
        if not ret_bool:
            self._is_exist_share = False
            logger.debug('drsu:%s不存在挂载盘' % self._drsu_id)
        # 只要是脚本打开的 或者是没有挂载盘的 都需要修改为。./data
        ret_set = (not ret_bool) or flag
        self.replace_str_download_dir(ret_set=ret_set)
        self.replace_str_download_common(flag=flag)

    # 根据是否有挂载目录修改保存路径 ret_bool 是否设置为./drsu_data
    def replace_str_download_dir(self, ret_set=True):
        old_str1, old_str2 = 'dump_msg_dir=./drsu_data', 'dump_msg_dir=../drsu_data',
        old_str3 = 'dump_msg_dir=/home/share/drsu' + self._drsu_file_name[-2:] + '_data'
        new_str1 = old_str1 if ret_set else old_str3
        self.replace_str(self.drsu.ai_livox_file, old_str1, new_str1)
        self.replace_str(self.drsu.ai_livox_file, old_str2, new_str1)
        self.replace_str(self.drsu.ai_livox_file, old_str3, new_str1)
        self.replace_str(self.drsu.ai_file, old_str1, new_str1)
        self.replace_str(self.drsu.ai_file, old_str2, new_str1)
        self.replace_str(self.drsu.ai_file, old_str3, new_str1)

    #  设置可视化参数 0 代表关闭 1代表打开 默认需要关闭
    def replace_str_visualization(self, flag=False):
        if flag:
            old_str, new_str = 'is_bev_visualization:0', 'is_bev_visualization:1'
            old_str1, new_str1 = 'is_visualization:0', 'is_visualization:1'
        else:
            new_str, old_str = 'is_bev_visualization:0', 'is_bev_visualization:1'
            new_str1, old_str1 = 'is_visualization:0', 'is_visualization:1'
        return self.replace_str(self.drsu.camera_file, old_str, new_str, is_replace_all=True) and \
               self.replace_str(self.drsu.camera_file, old_str1, new_str1, is_replace_all=True)

    # 过滤读取log文件
    def remote_sleep_log_read_grep_key(self, key):
        # if not os.path.exists(self.drsu.log_file):
        #     logger.debug('log文件:%s不存在' % self.drsu.log_file)
        #     return False
        return self.exec_command_retstr('cat /dr/drsu_' + self._drsu_id + '/DR_APP/log.txt' + ' | grep -a ' + key)

    # 远程杀drsu进程
    def remote_kill(self):
        str_ps = "ps -aux | grep \"./DR_APP/monitor_dr.sh /dr/drsu_" + self._drsu_file_name + "\" | grep -v grep | head -1 | awk -F ' ' '{logger.debugf $2}'"
        process_id_str = self.exec_command_retstr(str_ps)
        str_kill = "kill -9 " + process_id_str
        logger.debug(str_kill)
        self.exec_command_retstr(str_kill)
        str_ps = "ps -aux | grep /dr/drsu_" + self._drsu_file_name + "/DR_APP/dr_drsu | grep -v grep | head -1 | awk -F ' ' '{logger.debugf $2}'"
        process_id_str = self.exec_command_retstr(str_ps)
        str_kill = "kill -9 " + process_id_str
        logger.debug(str_kill)
        self.exec_command_retstr(str_kill)
        logger.info('kill drsu进程')

    # 远程杀drsu进程,全杀
    def remote_kill_(self):
        str_ps = "ps -aux | grep drsu | grep -v grep | awk '{logger.debug $1}' | xargs kill -9 "
        self.exec_command_retstr(str_ps)
        logger.info('kill drsu相关进程')

    # 获取bin目录下最新版本
    def get_version_by_drsu_id(self):
        version_path = '/dr/drsu_' + self._drsu_file_name + '/bin'
        command = 'ls -t ' + version_path + '| grep -v debug | grep -v Debug | grep Release | head -1'
        logger.debug(command)
        return self.exec_command_retstr(command)

    # 获取drsu进程数量
    def remote_ps_drsu_process_num(self):
        str_ps_num = "ps -aux | grep drsu_" + self._drsu_file_name + "| grep -v grep | wc -l"
        return int(self.exec_command_retstr(str_ps_num))

    # 远程启动drsu
    def remote_start_drsu_(self):
        str_start = "cd /dr/drsu_" + self._drsu_file_name + "; nohup /dr/script/start_dr.sh /dr/drsu_" + self._drsu_file_name + ' > log_startup.txt'
        logger.info('远程启动drsu')
        self.exec_command_retstr(str_start)

    # 获取模拟drc进程个数
    def remote_ps_drc_sim_process_num(self):
        str_ps_num = 'ps aux | grep DrPsdrsu | grep -v grep | wc -l'
        return int(self.exec_command_retstr(str_ps_num))

    # 远程启动模拟drc
    def remote_start_drc_sim(self):
        if self.remote_ps_drc_sim_process_num() == 0:
            logger.info('启动模拟drc')
            str_start = 'cd /dr/tool/drc_sim/; /dr/tool/drc_sim/startup.sh'
            self.exec_command_retstr(str_start)
            time.sleep(1)
        else:
            logger.info('模拟drc已启动')

    # 远程启动drsu
    def remote_start_drsu(self):
        if self._drc_id != '0':
            self.remote_replace_drc_ip()
        if self._is_sim:
            thread_02 = Thread(target=self.remote_start_drc_sim)
            # 启动线程02
            thread_02.start()
        time.sleep(5)
        self.remote_start_drsu_()

    # 查询drcip
    def query_str_drc_ip(self):
        command1 = 'cat /dr/drsu_' + self._drsu_file_name + '/config/bootup/drsu_common_config.json | grep "IPv4ForDrc"'
        command2 = 'cat /dr/drsu_' + self._drsu_file_name + '/config/bootup/drsu_common_config.json | grep "IPv4ForDev"'
        command3 = 'cat /dr/drsu_' + self._drsu_file_name + '/config/bootup/drsu_common_config.json | grep "DrcIPv4"'
        str1 = self.exec_command_retstr(command1).split(':')[1].strip().strip(',').strip('"')
        str2 = self.exec_command_retstr(command2).split(':')[1].strip().strip(',').strip('"')
        str3 = self.exec_command_retstr(command3).split(':')[1].strip().strip(',').strip('"')
        return str1, str2, str3

    # 根据当前环境 替换drcip
    def remote_replace_drc_ip(self):
        if not self.drc:
            self.drc = Drc_Config(self._drc_id)
        # 注册到虚拟drc的情况下地址填写本地环回口地址，否则填写本地地址以及drc地址
        new_str1 = loopback if self._is_sim else self._host
        new_str2 = loopback if self._is_sim else self._host
        new_str3 = loopback if self._is_sim else self.drc.host
        file_dir = '/dr/drsu_' + self._drsu_file_name + '/config/bootup/drsu_common_config.json'
        cur_str1, cur_str2, cur_str3 = self.query_str_drc_ip()
        if cur_str1 != new_str1 or cur_str2 != new_str2 or cur_str3 != new_str3:
            self.replace_str(file_dir, cur_str1, new_str1, is_replace_all=False, is_replace_id=True)
            self.replace_str(file_dir, cur_str2, new_str2, is_replace_all=False, is_replace_id=True)
            self.replace_str(file_dir, cur_str3, new_str3, is_replace_all=False, is_replace_id=True)
            qry_str1, qry_str2, qry_str3 = self.query_str_drc_ip()
            logger.info('原地址IPv4ForDrc:%s;IPv4ForDev:%s;DrcIPv4:%s\r\n,'
                        '改后地址IPv4ForDrc:%s;IPv4ForDev:%s;DrcIPv4:%s'
                        % (cur_str1, cur_str2, cur_str3, qry_str1, qry_str2, qry_str3))
        else:
            logger.info('ip地址无需修改')

    # 判断drsu是否成功启动并收集数据 是否到READY状态，是否有传感器数据，是否有障碍物信息
    def is_drsu_ready(self):
        if not self.remote_sleep_log_read_grep_key('CTRL_STATE_READY'):
            logger.info('drsu:%s未进入到READY状态' % self._drsu_id)
            return False
        if not self.remote_sleep_log_read_grep_key('ai_data_notify_cameradp_msg'):
            logger.info('drsu:%s未上报AI_DATA' % self._drsu_id)
            return False
        if not self.remote_sleep_log_read_grep_key('obstacle'):
            logger.info('drsu:%s未上报障碍物' % self._drsu_id)
            return False
        logger.info('drsu:%s启动成功' % self._drsu_id)
        return True

    # 获取md5校验值
    def get_md5sum_value(self):
        command = 'md5sum /dr/drsu_' + self._drsu_file_name + '/bin//DR_APP/startup.sh'
        return self.exec_command_retstr(command)

    # 更换版本，绕开密码验证
    def chmod_version(self):
        base_path = '/dr/drsu_' + self._drsu_file_name + '/bin/'
        start_path = './DR_APP/startup.sh'
        version_name = self.get_version_by_drsu_id()
        logger.debug('版本名称：%s' % version_name)
        debug_version_name = 'dr_drsu_Debug-build_wth.gz'
        command0 = 'cd ' + base_path
        command1 = 'tar xvf ' + version_name
        self.exec_command_retstr(command0 + '; ' + command1)
        md5_1 = self.get_md5sum_value().split()[0]  # 获取修改前的md5sum值
        command2 = 'sed -i "77iecho broadxt333 | sudo -S ls" ' + start_path
        self.exec_command_retstr(command0 + '; ' + command2)
        # 修改之后先计算出md5值 然后去替换旧的md5值
        md5_2 = self.get_md5sum_value().split()[0]
        info_path = base_path + '/DR_APP/info.log'

        self.replace_str(info_path, md5_1, md5_2)
        command6 = 'tar -cvf ' + debug_version_name + ' ./DR_APP/'
        command7 = 'md5sum ' + base_path + debug_version_name + ' > ' + base_path + 'update.bootup.img'
        self.exec_command_retstr(command0 + '; ' + command6 + '; ' + command7)
        return True

    # 修改版本，主要功能是绕开输入命令着一步，启动drsu必须要用这个功能
    def remote_mod_version(self, force=False):
        file_name = '/dr/drsu_' + self._drsu_file_name + '/DR_APP/startup.sh'
        if self.query_str(file_name, 'broadxt333') and not force:
            logger.debug('无需修改版本')
            return True
        else:
            return self.chmod_version()

    # 删除文件 使用小心！
    def remote_del_file(self, file_path):
        command = 'rm -rf ' + file_path
        logger.warning('删除文件：%s' % file_path)
        self.exec_command_no_readout(command)

    # 非公用函数，萧山采集数据专用
    def download_data(self):
        file_path = FilePath(self._drsu_id)
        file_name = file_path.get_tar_file_name()
        base_path1 = '/dr/drsu_' + self._drsu_file_name + '/DR_APP/'
        base_path2 = '/home/share/drsu' + self._drsu_id[-2:] + '_data'
        base_path = base_path2 if self._is_exist_share else base_path1
        today = time.strftime("%Y%m%d", time.localtime())
        data_name = './drsu_data/' + today
        # data_name = './log.txt'
        command0 = 'cd ' + base_path
        command1 = 'tar -czvf ' + './' + file_name + ' ' + data_name
        self.exec_command_retstr(command0 + '; ' + command1 + ';')
        # input_file_path = '/dr/drsu_810020015/log.txt'
        local_file = 'D:\\xiaoshandata\\' + file_name
        if not os.path.exists('D:\\xiaoshandata\\'):
            os.makedirs('D:\\xiaoshandata\\')
        self.local_path = local_file
        # self.remote_path = '/xiaoshandata/' + self._drsu_id + '/' + today
        self.remote_path = '/xiaoshandata/' + today
        self.download(base_path + file_name, local_file)
        time.sleep(20)
        self.remote_del_file(base_path + file_name)
        self.remote_del_file(base_path + data_name)

    # sff定制版本
    def download_lastest_jpg(self, file_path='/home/nvidia/data/'):
        command0 = 'ls -t ' + file_path + ' | grep -v sff  | head -1'
        data_path = self.exec_command_retstr(command0).rstrip()
        rq = time.strftime("%Y%m%d%H%M", time.localtime())
        self._mkdir(file_path + 'sff' + rq)
        command1 = 'cd ' + file_path + data_path
        command2 = 'ls -t ' + file_path + data_path + ' | grep ".jpg" | head -50 | xargs -i cp {} ' + file_path + 'sff' + rq
        ret_bool = self.exec_command_retstr(command1 + '; ' + command2)

    def remote_replace_drc_id(self, drc_id):
        command = 'cat /dr/drsu_' + self._drsu_file_name + '/config/bootup/drsu_common_config.json | grep "DrcSysId" | awk "{print $2}"'
        cur_drc_id = self.exec_command_retstr(command).split(':')[1].strip().strip(',')
        file_dir = '/dr/drsu_' + self._drsu_file_name + '/config/bootup/drsu_common_config.json'
        if cur_drc_id != drc_id:
            ret_bool = self.replace_str(file_dir, cur_drc_id, drc_id, is_replace_all=False, is_replace_id=True)
            if ret_bool:
                logger.info('drc_id修改成功')
            else:
                logger.info('drc_id修改失败')
            return ret_bool
        else:
            logger.debug('drc_id无需修改')
            return True

    # 将drsu_common_config文件中的drsuid改为
    def remote_replace_drsu_id(self):
        command = 'cat /dr/drsu_' + self._drsu_file_name + '/config/bootup/drsu_common_config.json | grep "DrsuSysId" | awk "{print $2}"'
        cur_drsu_id = self.exec_command_retstr(command).split(':')[1].strip().strip(',')
        file_dir = '/dr/drsu_' + self._drsu_file_name + '/config/bootup/drsu_common_config.json'
        if cur_drsu_id != self._drsu_id:
            ret = self.replace_str(file_dir, cur_drsu_id, self._drsu_id, is_replace_all=False, is_replace_id=True)
            if ret:
                logger.info('drsu_id地址修改成功')
            else:
                logger.info('drsu_id地址修改失败')
            return ret
        else:
            logger.info('drsu_id地址无需修改')
            return True

    # 从其他主机上下载文件
    # 'sudo scp -r broadxt@172.16.20.17:/home/broadxt/Downloads/dr.tar.gz /dr'
    def scp_download(self, remote_path, local_path, remote_passwd, size=None):
        logger.info('从远端:%s拷贝文件到本地:%s' % (remote_path, local_path))
        command = 'sudo scp -r ' + remote_path + ' ' + local_path
        self.remote_shell_sudo(command, remote_password=remote_passwd)
        return self.check_scp('/dr/dr.tar.gz', size)

    # 解压文件
    def tar_dr(self):
        command = 'cd /dr'
        command1 = 'sudo tar xvf dr.tar.gz'
        self.send_command(command)
        self.remote_shell_sudo(command1)
        logger.info('解压文件')

    # 修改文件所有用戶為當前用戶
    def chmod_dr(self):
        command = 'sudo chown -R broadxt:broadxt *'
        self.remote_shell_sudo(command)

    # 修改rc.local文件
    def chmod_rc(self):
        command1 = 'cat /etc/rc.local'
        str1 = self.send_command(command1)
        if 'start_user.sh' in str1:
            logger.info('rc 无需修改')
            return True
        command = "echo '/dr/script/start_user.sh &' >> /etc/rc.local"
        self.send_command(command)
        str1 = self.send_command(command1)
        if 'start_user.sh' in str1:
            logger.info('rc 修改成功')
            return True
        else:
            return False

    # 获取factory.bootup.img中的版本信息，用于测试版本升级
    def get_update_version(self):

        command = 'cat /dr/drsu_' + self._drsu_file_name + '/bin/update.bootup.img'
        version = self.exec_command_retstr(command).split()[1].split('/')[-1]
        logger.info('update.bootup.img中的版本为：%s' % version)
        return version

    # 修改配置文件drsu_common_config
    def mod_drsu_cfg(self, config_file):
        dest_file = '/dr/drsu_{}/config/bootup/drsu_common_config.json'.format(self._drsu_id)
        src_file = '/dr/drsu_{}/config/bootup/{}'.format(self._drsu_id, config_file)
        if self.cp(src_file, dest_file, force=True):
            logger.info('drsu:%s 替换drsu_common_config.json' % self._drsu_id)
        else:
            logger.info('drsu:%s 替换drsu_common_config.json 失败' % self._drsu_id)

    # 备份配置文件drsu_common_config
    def bk_drsu_cfg(self, config_file, force):
        src_file = '/dr/drsu_{}/config/bootup/drsu_common_config.json'.format(self._drsu_id)
        dest_file = '/dr/drsu_{}/config/bootup/{}'.format(self._drsu_id, config_file)
        if self.cp(src_file, dest_file, force=force):
            logger.info('drsu:%s 备份drsu_common_config.json' % self._drsu_id)
        else:
            logger.info('drsu:%s 备份drsu_common_config.json 失败' % self._drsu_id)

    # 修改配置文件 drsu_common_para.
    def mod_drsu_para(self, para_file):
        dest_file = '/dr/drsu_{}/config/bootup/drsu_common_para.json'.format(self._drsu_id)
        src_file = '/dr/drsu_{}/config/bootup/{}'.format(self._drsu_id, para_file)
        if self.cp(src_file, dest_file, force=True):
            logger.info('drsu:%s drsu_common_para.json' % self._drsu_id)
        else:
            logger.info('drsu:%s drsu_common_para.json 失败' % self._drsu_id)

    # 备份配置文件 drsu_common_para.
    def bk_drsu_para(self, para_file, force):
        src_file = '/dr/drsu_{}/config/bootup/drsu_common_para.json'.format(self._drsu_id)
        dest_file = '/dr/drsu_{}/config/bootup/{}'.format(self._drsu_id, para_file)
        if self.cp(src_file, dest_file, force=force):
            logger.info('drsu:%s 备份drsu_common_para.json' % self._drsu_id)
        else:
            logger.info('drsu:%s 备份drsu_common_para.json 失败' % self._drsu_id)

    def bk_cfg(self, para_file=None, config_file=None, force=False):
        para_file = para_file if para_file else self.drsu.para_file
        config_file = config_file if config_file else self.drsu.config_file
        self.bk_drsu_para(para_file, force)
        self.bk_drsu_cfg(config_file, force)

    # 修改配置文件, 參數radar為是否安裝了毫米級雷達
    def chmod_cfg(self, radar=False):
        # 如果是虚拟机环境，直接用drsu_common_config_127.json文件数据就行
        if self._is_sim:
            self.mod_drsu_para(self.drsu.sim_para_file)
            self.mod_drsu_cfg(self.drsu.sim_config_file)
        # 如果需要注册到真实drc环境，且区分是否有雷达
        elif radar:
            self.mod_drsu_para(self.drsu.radar_para_file)
            self.mod_drsu_cfg(self.drsu.radar_config_file)
        # 如果需要注册到真实drc环境，则使用drsu_common_config_test.json，并且修改部分配置
        else:
            self.mod_drsu_para(self.drsu.para_file)
            self.mod_drsu_cfg(self.drsu.config_file)

    def set_update_version(self, version):
        if self.get_update_version() == version or version is None:
            return
        version_file = '/dr/drsu_{}/bin/{}'.format(self._drsu_id, version)
        if self.is_exist_file(version_file):
            command = 'md5sum /dr/drsu_{}/bin/{} > update.bootup.img'.format(self._drsu_id, version)
            self.send_command(command)
            logger.info('drsu:%s update.bootup.img中的版本更换为：%s' % (self._drsu_id, version))
        else:
            logger.warning('指定版本：%s不存在' % version)
