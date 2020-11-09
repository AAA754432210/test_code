from api_test.base_page.homepage import HomePage
from common.Log import Logger
from selenium.webdriver.support.select import Select

logger = Logger("AcuDevMgrSpecCfgPage").getlog()


# acu设备配置可以同时制定多个设备
# 该页面点击取消或者弹窗告警确认之后会回到AcuDevMgrPage
class AcuDevMgrSpecCfgPage(HomePage):

    # 选择状态上报周期 100 200 500 1000
    def choose_status_report_unit(self, value):
        sel = self.find_element('xpath=>//*[@id="ulPeriodOfSatusRpt"]')
        self.wait(2)
        Select(sel).select_by_value(str(value))

    # 选择告警上报周期 10 30 self.sixty
    def choose_alarm_report_unit(self, value):
        sel = self.find_element('xpath=>//*[@id="ulPeriodOfAlarmRpt"]')
        self.wait(2)
        Select(sel).select_by_value(str(value))

    # 选择车辆信息上报周期 100 200 500 1000
    def choose_car_info_report_unit(self, value):
        sel = self.find_element('xpath=>//*[@id="ulPeriodofInfo"]')
        self.wait(2)
        Select(sel).select_by_value(str(value))

    # 点击取消
    def cancel_click(self):
        cancel_click_link = 'xpath=>//*[@id="btn_cancel"]'
        self.click(cancel_click_link)

    # 点击重置
    def reset_click(self):
        reset_click_link = 'xpath=>//*[@id="acusConfig-form"]/div[6]/div/button[2]'
        self.click(reset_click_link)

    # 点击执行ACU参数配置
    def submit_acu_cfg_click(self):
        submit_acu_cfg_click_link = 'xpath=>//*[@id="btn_saveDrc"]'
        self.click(submit_acu_cfg_click_link)

