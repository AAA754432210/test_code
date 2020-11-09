from api_test.base_page.homepage import HomePage
from common.Log import Logger
from selenium.webdriver.support.select import Select

logger = Logger("DrsuDevMgrSpecCfgPage").getlog()


# drsu设备配置可以同时制定多个设备
# 该页面点击取消或者弹窗告警确认之后会回到DrsuDevMgrPage
class DrsuDevMgrSpecCfgPage(HomePage):

    # 选择告警上报周期 10 30 self.sixty
    def choose_alarm_report_cycle(self, value):
        sel = self.find_element('xpath=>//*[@id="ulPeriodOfAlarmRpt"]')
        Select(sel).select_by_value(str(value))
        self.sleep(2)

    # 选择是否长期有效 目前只有否 false
    def choose_long_term_valid(self, value='false'):
        sel = self.find_element('xpath=>//*[@id="longTermValid"]')
        Select(sel).select_by_value(str(value))
        self.sleep(2)

    # 点击取消
    def cancel_click(self):
        cancel_click_link = 'xpath=>//*[@id="btn_cancel"]'
        self.click(cancel_click_link)
        self.sleep(2)

    # 点击提交配置
    def submit_cfg_click(self):
        submit_cfg_click_link = 'xpath=>//*[@id="btn_savesDrsu"]'
        if self.is_visible('//*[@id="btn_savesDrsu"]'):
            self.click(submit_cfg_click_link)
        else:
            logger.info('未找到提交配置按钮')
        self.sleep(2)

    # 是否弹出drsu配置失败
    def is_prompt_visible(self):
        selector = '//*[@id="configAllAcrOfDrcidModalLabel"]'
        ret = self.is_visible(selector)
        logger.info("是否弹出配置drsu失败弹窗%s" % ret)
        return ret

    # 待扩展
    def get_err_id(self):
        err_id_link = 'xpath=>//*[@id="tb_list"]/tbody/tr/td[3]'
        err_id = self.find_element(err_id_link).text
        logger.info("DRSU配置指定可配置参数部分失败，错误码：%s" % err_id)
        return err_id

    # 点击关闭
    def close_window_click(self):
        close_window_click_link = 'xpath=>//*[@id="guanbi"]'
        self.click(close_window_click_link)

    # 点击关闭 弹出入库成功 再点击关闭
    def close_window_click1(self):
        close_window_click_link = 'xpath=>//*[@id="idlg_btn_1583478789096_0"]'
        self.click(close_window_click_link)
        self.sleep(1)
        close_window_click_link1 = 'xpath=>//*[@id="idlg_btn_1583478882498_0"]'
        self.click(close_window_click_link1)

    # 对指定drsu设备进行配置 函数调用之后正常情况会回到DRSU设备配置页面
    def cfg_spec_drsu(self, dict_drsu):
        try:
            self.choose_alarm_report_cycle(dict_drsu['告警上报周期']) # 填入告警上报周期的值
            # self.choose_long_term_valid(dict_drsu['是否长期有效']) # 这里目前只有否
        except Exception as e:
            logger.error('配置指定drsu失败%s' % format(e))
            self.get_windows_img()
            return False
        self.submit_cfg_click()
        if self.info() and self.info_text() == '配置成功':
            logger.info('配置drsu成功')
            self.enter_click()
            self.esc_click()
            self.enter_click()
            return True
        else:
            logger.error('配置drsu失败')
            self.get_windows_img()
            return False