from api_test.base_page.homepage import HomePage
from common.Log import Logger
from selenium.webdriver.support.select import Select

logger = Logger("AlarmQryPage").getlog()


class AlarmQryPage(HomePage):

    # 告警编号输入
    def input_alarm_no(self, alarm_no):
        input_alarm_no_link = 'xpath=>//*[@id="ulAlarmNo"]'
        self.type(input_alarm_no_link, alarm_no)

    # 选择告警级别null：全部告警；1：一般告警；2：严重告警；3：清除告警
    def choose_alarm_level(self, alarm_level):
        sel = self.find_element('xpath=>//*[@id="alarmLevelSelect"]')
        self.wait(2)
        Select(sel).select_by_value('%s' % str(alarm_level))

    # 选中告警消除开始时间
    def alarm_begin_time(self, begintime):
        alarm_begin_time_link = 'xpath=>//*[@id="sAlarmBeginTime"]'
        self.click(alarm_begin_time_link)

    # 选中告警消除结束时间
    def alarm_end_time(self, endtime):
        alarm_begin_time_link = 'xpath=>//*[@id="sAlarmCloseTime"]'
        self.click(alarm_begin_time_link)

    # 点击刷新
    def refresh_click(self):
        refresh_link = 'xpath=/html/body/div[1]/div[1]/div[3]/div[2]/div/div[2]/div/div/div[2]/div[1]/div[2]/button'
        self.click(refresh_link)

    # 点击全屏
    def full_screen_click(self):
        full_screen_link = 'xpath=/html/body/div[1]/div[1]/div[3]/div[2]/div/div[2]/div/div/div[2]/div[1]/div[' \
                           '2]/div/button '
        self.click(full_screen_link)

    # 点击全选
    def all_election_click(self):
        slect_all_click = 'xpath=//*[@id="tb_list"]/thead/tr/th[1]/div[1]/label/input'
        self.click(slect_all_click)

    # 选择指定唯一标识设备
    def device_select_click(self, alarm_no):
        for i in range(1, 10):
            choose_box_link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[2]'
            if self.find_element(choose_box_link_temp).text == alarm_no:
                choose_box_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[1]/label/input'
                self.click(choose_box_link)
                logger.info("点击指定告警成功 alarm_no:%u" % alarm_no)
                return i
        logger.info("点击指定告警失败 alarm_no:%u" % alarm_no)
        i = 0
        return i

    # 点击处理告警
    def handle_alarm(self):
        handle_alarm_link = 'xpath=>//*[@id="btn_handleAlarms"]'
        self.click(handle_alarm_link)

    # 点击告警处理结果
    def handle_alarm_results(self):
        handle_alarm_results_link = 'xpath=>//*[@id="btn_alarmHandleResults"]'
        self.click(handle_alarm_results_link)

