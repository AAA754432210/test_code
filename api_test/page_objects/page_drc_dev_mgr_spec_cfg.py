from api_test.base_page.homepage import HomePage
from common.Log import Logger
from selenium.webdriver.support.select import Select

logger = Logger("DrcDevMgrSpecCfgPage").getlog()


# 该页面点击取消或者弹窗告警确认之后会回到DrcDevMgrPage
class DrcDevMgrSpecCfgPage(HomePage):

    # 填写acu存活检测次数 范围3-10
    def input_acu_active_detec_times(self, times):
        times_link = 'xpath=>//*[@id="ulAcuActiveDetecTimes"]'
        self.type(times_link, str(times))

    # 选择是否长期有效 0:本次 1：长期
    def choose_long_term_valid(self, value):
        sel = self.find_element('xpath=>//*[@id="isLongTermValid"]')
        self.wait(0.5)
        Select(sel).select_by_value(str(value))

    # 填写drc状态上报周期
    def input_drc_stat_report_unit(self, value):
        unit_link = 'xpath=>//*[@id="ulPeriodofStatusRpt"]'
        self.type(unit_link, str(value))

    # 选择障碍物上报开关 默认为OFF value参数填写'OFF','ON'
    def choose_drc_stat_report_switch(self, value):
        sel = self.find_element('xpath=>//*[@id="ul2dInvalidObsta"]')
        self.wait(0.5)
        Select(sel).select_by_visible_text(str(value))

    # 点击取消
    def cancel_click(self):
        cancel_click_link = 'xpath=>//*[@id="btn_cancel"]'
        self.click(cancel_click_link)

    # 点击提交配置
    def submit_drc_cfg_click(self):
        submit_drc_cfg_click_link = 'xpath=>//*[@id="btn_saveDrc"]'
        self.click(submit_drc_cfg_click_link)

    # 点击关闭
    def close_window_click(self):
        close_window_click_link = 'xpath=>//*[@id="idlg_btn_1583303447505_0"]'
        self.click(close_window_click_link)

    # 点击关闭 入库成功
    def close_window_click2(self):
        close_window_click_link = 'xpath=>//*[@id="idlg_btn_1583303507757_0"]'
        self.click(close_window_click_link)

    # 输入DRC设备配置 参数result为预期结果 默认为空
    def input_drc_cfg(self, dict_drc_cfg, result=''):
        self.input_acu_active_detec_times(dict_drc_cfg['ACU存活检测次数'])
        self.input_drc_stat_report_unit(dict_drc_cfg['DRC状态上报周期'])
        if dict_drc_cfg['是否长期有效'] == '长期生效':
            self.choose_long_term_valid('1')
        if dict_drc_cfg['障碍物上报开关'] == 'ON':
            self.choose_drc_stat_report_switch('ON')
        self.sleep(0.5)
        self.get_windows_img()
        self.submit_drc_cfg_click()
        assert self.info()
        self.sleep(1)
        self.get_windows_img()
        if self.info_text() == result:
            logger.info('配置drc成功')
            self.enter_click()
            self.esc_click()
            self.enter_click()
            return True
        elif self.info_text() == result:
            logger.info('配置drc失败但符合预期结果')
            self.esc_click()
            return True
        else:
            logger.error('配置drc失败')
            self.get_windows_img()
            return False

    def drc_qry_abnormal(self):
        self.sleep(1)
        assert (self.info())
        if self.info_text() == '该DRC不在线,不可查询参数':
            logger.info('drc 不在线，不可查询参数')
            self.esc_click()
            return True
        else:
            logger.error('提示不符合预期')
            self.get_windows_img()
            self.esc_click()
            return False

    def drc_cfg_abnormal(self):
        self.sleep(1)
        assert (self.info())
        if self.info_text() == '该DRC不在线,不可配置参数':
            logger.info('drc 不在线，不可配置参数')
            self.esc_click()
            return True
        else:
            logger.error('提示不符合预期')
            self.get_windows_img()
            self.esc_click()
            return False
