from .base_page import BasePage
from common.Log import Logger


# create a logger instance
logger = Logger("HomePage").getlog()


class HomePage(BasePage):
    """
    登录设备管理系统
    """

    # 配置管理链接
    cfg_mgr_link = 'xpath=>//*[@id="sidebar-menu"]/div[1]/ul/li[1]/a'
    # 告警管理连接
    alarm_mgr_link = 'xpath=>//*[@id="sidebar-menu"]/div[1]/ul/li[2]/a'
    # 状态上报链接
    status_report_link = 'xpath=>//*[@id="sidebar-menu"]/div[1]/ul/li[3]/a'
    # 版本管理链接
    version_mgr_link = 'xpath=>//*[@id="sidebar-menu"]/div[1]/ul/li[4]/a'
    # 日志管理链接
    log_mgr_link = 'xpath=>//*[@id="sidebar-menu"]/div[1]/ul/li[5]/a'
    # 统计报表
    statistical_report_link = 'xpath=>//*[@id="sidebar-menu"]/div[1]/ul/li[6]/a'
    # 用户管理
    user_mgr_link = 'xpath=>//*[@id="sidebar-menu"]/div[1]/ul/li[7]/a'
    # 2Dmap
    map_2d_link = 'xpath=>//*[@id="sidebar-menu"]/div[2]/ul/li[1]/a'
    # 3Dmap
    map_3d_link = 'xpath=>//*[@id="sidebar-menu"]/div[2]/ul/li[2]/a'
    # 工程维护
    engineering_maintenance_link = 'xpath=>//*[@id="sidebar-menu"]/div[3]/ul/li/a'

    # 配置管理部分
    # 点击配置管理
    def cfg_mgr_click(self):
        self.click(self.cfg_mgr_link)
        # self.wait(3)

    # 配置管理->DRC设备配置
    def drc_dev_cfg_mgr_click(self):
        drc_cfg_set_link = 'xpath=>//*[@id="sidebar-menu"]/div[1]/ul/li[1]/ul/li[1]/a'
        if self.is_visible('//*[@id="sidebar-menu"]/div[1]/ul/li[1]/ul/li[1]/a'):
            self.click(drc_cfg_set_link)
        else:
            logger.info('未找到DRC配置管理按钮')
        self.sleep(1)

    # 配置管理->ACU设备配置
    def acu_dev_cfg_mgr_click(self):
        acu_cfg_set_link = 'xpath=>//*[@id="sidebar-menu"]/div[1]/ul/li[1]/ul/li[2]/a'
        if self.is_visible('//*[@id="sidebar-menu"]/div[1]/ul/li[1]/ul/li[2]/a'):
            self.click(acu_cfg_set_link)
        else:
            logger.info('未找到ACU配置管理按钮')
        self.sleep(1)

    # 配置管理->DRSU设备配置
    def drsu_dev_cfg_mgr_click(self):
        drsu_cfg_set_link = 'xpath=>//*[@id="sidebar-menu"]/div[1]/ul/li[1]/ul/li[3]/a'
        if self.is_visible('//*[@id="sidebar-menu"]/div[1]/ul/li[1]/ul/li[3]/a'):
            self.click(drsu_cfg_set_link)
        else:
            logger.info('未找到DRSU配置管理按钮')
        self.sleep(1)

    # 配置管理->DRSU电源管理
    def drsu_power_mgr_click(self):
        drsu_power_mgr_link = 'xpath=>//*[@id="sidebar-menu"]/div[1]/ul/li[1]/ul/li[4]/a'
        if self.is_visible('//*[@id="sidebar-menu"]/div[1]/ul/li[1]/ul/li[4]/a'):
            self.click(drsu_power_mgr_link)
        else:
            logger.info('未找到DRSU电源管理按钮')
        self.sleep(1)

    # 配置管理->重启管理
    def dev_rst_mgr_click(self):
        dev_rst_mgr_link = 'xpath=>//*[@id="sidebar-menu"]/div[1]/ul/li[1]/ul/li[5]/a'
        if self.is_visible('//*[@id="sidebar-menu"]/div[1]/ul/li[1]/ul/li[5]/a'):
            self.click(dev_rst_mgr_link)
        else:
            logger.info('未找到重启管理按钮')
        self.sleep(1)

    # 告警管理部分
    # 点击告警管理
    def alarm_mgr_click(self):
        self.click(self.alarm_mgr_link)
        self.sleep(1)

    # 设备实时告警
    def dev_alarm_mgr_realtime_click(self):
        dev_alarm_realtime = 'xpath=>//*[@id="sidebar-menu"]/div[1]/ul/li[2]/ul/li[1]/a'
        # self.click(self.alarm_mgr_link)
        self.click(dev_alarm_realtime)
        self.sleep(1)

    # 设备历史告警
    def dev_alarm_mgr_hty_click(self):
        dev_alarm_history = 'xpath=>//*[@id="sidebar-menu"]/div[1]/ul/li[2]/ul/li[2]/a'
        # self.click(self.alarm_mgr_link)
        self.click(dev_alarm_history)
        self.sleep(1)

    # 状态上报部分
    # 点击状态上报
    def status_report_click(self):
        self.click(self.status_report_link)
        self.sleep(1)

    # DRC状态上报
    def drc_dev_status_report_click(self):
        drc_dev_status_report = 'xpath=>//*[@id="sidebar-menu"]/div[1]/ul/li[3]/ul/li[1]/a'
        # self.click(self.status_report)
        self.click(drc_dev_status_report)
        self.sleep(1)

    # ACU状态上报
    def acu_dev_status_report_click(self):
        acu_dev_status_report = 'xpath=>//*[@id="sidebar-menu"]/div[1]/ul/li[3]/ul/li[2]/a'
        # self.click(self.status_report)
        self.click(acu_dev_status_report)
        self.sleep(1)

    # DRSU状态上报
    def drsu_dev_status_report_click(self):
        drsu_dev_status_report = 'xpath=>//*[@id="sidebar-menu"]/div[1]/ul/li[3]/ul/li[3]/a'
        # self.click(self.status_report)
        self.click(drsu_dev_status_report)
        self.sleep(1)

    # 版本管理部分
    # 点击版本管理
    def version_mgr_click(self):
        self.click(self.version_mgr_link)
        self.sleep(1)

    # drc版本升级
    def drc_version_mgr_click(self):
        drc_dev_version_mgr = 'xpath=>//*[@id="sidebar-menu"]/div[1]/ul/li[4]/ul/li[1]/a'
        # self.click(self.version_mgr_link)
        self.click(drc_dev_version_mgr)
        self.sleep(1)

    # ACU版本升级
    def acu_version_mgr_click(self):
        acu_dev_version_mgr = 'xpath=>//*[@id="sidebar-menu"]/div[1]/ul/li[4]/ul/li[2]/a'
        # self.click(self.version_mgr_link)
        self.click(acu_dev_version_mgr)
        self.sleep(1)

    # DRSU版本升级
    def drsu_version_mgr_click(self):
        drsu_dev_version_mgr = 'xpath=>//*[@id="sidebar-menu"]/div[1]/ul/li[4]/ul/li[3]/a'
        # self.click(self.version_mgr_link)
        self.click(drsu_dev_version_mgr)
        self.sleep(1)

    # 日志管理部分
    # 点击日志管理
    def log_mgr_click(self):
        self.click(self.log_mgr_link)
        self.sleep(1)

    # 日志配置
    def log_cfg_click(self):
        log_cfg = 'xpath=>//*[@id="sidebar-menu"]/div[1]/ul/li[5]/ul/li[1]/a'
        # self.click(self.log_mgr_link)
        self.click(log_cfg)
        self.sleep(1)

    # 事件日志
    def event_log_click(self):
        event_log = 'xpath=>//*[@id="sidebar-menu"]/div[1]/ul/li[5]/ul/li[2]/a'
        # self.click(self.log_mgr_link)
        self.click(event_log)
        self.sleep(1)

    # 定位日志
    def debug_log_click(self):
        debug_log = 'xpath=>//*[@id="sidebar-menu"]/div[1]/ul/li[5]/ul/li[3]/a'
        # self.click(self.log_mgr_link)
        self.click(debug_log)
        self.sleep(1)

    # 统计报表部分
    # KPI统计
    def kpi_statistics_click(self):
        kpi_statistics = 'xpath=>//*[@id="sidebar-menu"]/div[1]/ul/li[6]/ul/li[1]/a'
        self.click(self.statistical_report_link)
        self.click(kpi_statistics)
        self.sleep(2)

    # 用户管理部分
    # 用户管理
    def user_mgr_click(self):
        user_mgr = 'xpath=>//*[@id="sidebar-menu"]/div[1]/ul/li[7]/ul/li[1]/a'
        self.click(self.user_mgr_link)
        self.click(user_mgr)
        self.sleep(2)

    # 2Dmap
    def map_2d_click(self):
        self.click(self.map_2d_link)

    # 3Dmap
    def map_3d_click(self):
        self.click(self.map_2d_link)

    # 工程维护部分
    # 点击工程维护
    def engineering_maintenance_click(self):
        self.click(self.engineering_maintenance_link)
        self.sleep(1)

    # 点击工单管理
    def work_order_mgr_click(self):
        link = 'xpath=>//*[@id="sidebar-menu"]/div[3]/ul/li/ul/li[1]/a'
        self.click(link)

    # 点击人员管理
    def personnel_mgr_click(self):
        link = 'xpath=>//*[@id="sidebar-menu"]/div[3]/ul/li/ul/li[2]/a'
        self.click(link)

    # 点击资产管理
    def asset_mgr_click(self):
        link = 'xpath=>//*[@id="sidebar-menu"]/div[3]/ul/li/ul/li[3]/a'
        self.click(link)

    # 点击运营统计分析
    def operation_statistical_analysis_click(self):
        link = 'xpath=>//*[@id="sidebar-menu"]/div[3]/ul/li/ul/li[4]/a'
        self.click(link)

    # 点击刷新
    def refresh_click(self):
        refresh_link = 'name=>refresh'
        self.click(refresh_link)

    def switch_to_drc_status(self):
        self.status_report_click()
        self.drc_dev_status_report_click()

    def switch_to_drsu_status(self):
        self.status_report_click()
        self.drsu_dev_status_report_click()

    def switch_to_acu_status(self):
        self.status_report_click()
        self.acu_dev_status_report_click()