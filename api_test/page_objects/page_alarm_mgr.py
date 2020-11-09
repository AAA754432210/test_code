from api_test.base_page.homepage import HomePage
from common.Log import Logger
from selenium.webdriver.support.select import Select

logger = Logger("AlarmMgrPage").getlog()


class AlarmMgrPage(HomePage):

    # 输入设备标识
    def input_dev_id(self, dev_id):
        input_dev_id_link = 'xpath=>//*[@id="Uldevid"]'
        self.type(input_dev_id_link, str(dev_id))

    # 选择告警级别 null：全部告警；1：一般告警；2：严重告警；3：清除告警
    def choose_alarm_level(self, alarm_level):
        sel = self.find_element('xpath=>//*[@id="alarmLevelSelect"]')
        self.wait(2)
        Select(sel).select_by_value('%s' % str(alarm_level))

    # 告警码输入
    def input_alarm_no(self, alarm_no):
        input_alarm_no_link = 'xpath=>//*[@id="ulAlarmNo"]'
        self.type(input_alarm_no_link, str(alarm_no))

    # 填写发生时间开始 格式：'2020-04-09 00:00:00'
    def alarm_time_begin(self, time_frame):
        alarm_time_link = 'xpath=>//*[@id="sAlarmBeginTime"]'
        self.type(alarm_time_link, time_frame)

    # 填写发生时间开始 格式：'2020-04-09 00:00:00'
    def alarm_time_end(self, time_frame):
        alarm_time_link = 'xpath=>//*[@id="sAlarmCloseTime"]'
        self.type(alarm_time_link, time_frame)

    # 点击告警查询
    def alarm_qry_click(self):
        alarm_qry_link = 'xpath=>//*[@id="btn_alarmquery"]'
        self.click(alarm_qry_link)

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
        select_all_click = 'xpath=//*[@id="tb_list"]/thead/tr/th[1]/div[1]/label/input'
        self.click(select_all_click)

    # 点击告警号
    def checkboxes_alarm_no_click(self):
        link = 'xpath=>/html/body/div/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div/ul/li[1]/label/input'
        self.click(link)

    # 选择指定告警
    def alarm_select_click(self, alarm_no):
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

    # 获取唯一告警号 需要点击全屏 然后点击告警号，显示全局唯一告警号
    def get_alarm_num_union(self):
        link = 'xpath=>//*[@id="tb_list"]/tbody/tr/td[2]'
        return self.find_element(link).text

    # 选择指定告警,点击告警详情,查询之后
    def alarm_select_click_single(self, alarm_no='0'):
        link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr/td[3]'  # 告警码
        try:
            if self.find_element(link_temp).text == str(alarm_no) or alarm_no == '0':
                choose_box_link = 'xpath=>//*[@id="tb_list"]/tbody/tr/td[1]/label/input'
                self.click(choose_box_link)
                logger.info("点击指定告警码告警详情成功失败 alarm_no:%s" % str(alarm_no))
                return True
            else:
                logger.error("点击指定告警码告警详情失败 alarm_no:%s" % str(alarm_no))
                return False
        except:
            logger.error("指定告警码不存在 alarm_no:%s" % str(alarm_no))
            return False

    # 点击返回告警监控
    def return_click(self):
        link = 'xpath=>//*[@id="btn_returnAlarmMonitor"]'
        self.click(link)

    # 点击确认告警 需要先选择告警
    def confirm_alarm_click(self):
        link = 'xpath=>//*[@id="btn_confirmAlarms"]'
        self.click(link)

    # 判断是否出现告警确认弹窗
    def is_prompt_visible_alarm_confirm(self):
        selector = '//*[@id="alarmConfirmModalLabel"]'
        ret = self.is_visible(selector)
        logger.info("是否弹出告警确认弹窗%s" % ret)
        return ret

    # 读取告警去人弹窗中的确认告警个数
    def get_alarm_confirm_num(self):
        link = 'xpath=>//*[@id="cfmnumber"]'
        num = self.find_element(link).text
        return num

    # 获取已确认告警列表
    def get_alarm_confirmed_arr(self):
        link = 'xpath=>//*[@id="alarmNos"]'
        arr = self.get_value(link)
        return arr

    # 获取待确认告警列表
    def get_alarm_to_be_confirmed_arr(self):
        link = 'xpath=>//*[@id="ulAlarmNos"]'
        arr = self.get_value(link)
        return arr

    # 输入确认人，默认为账户名
    def input_alarm_confirmed_staff(self, staff):
        link = 'xpath=>//*[@id="alarmCfmStaff"]'
        self.type(link, staff)

    # 点击确认告警
    def confirm_alarm_submit_click(self):
        link = 'xpath=>//*[@id="btn_cfmAlarnmSubmit"]'
        self.click(link)

    # 点击手动清除告警 需要先选择告警
    def handle_del_alarm_click(self):
        link = 'xpath=>//*[@id="btn_handleAlarms"]'
        self.click(link)

    # 判断是否出现手动清除确认弹窗
    def is_prompt_visible_alarm_handle(self):
        selector = '//*[@id="alarmHandleModalLabel"]'
        ret = self.is_visible(selector)
        logger.info("是否弹出手动清除告警弹窗%s" % ret)
        return ret

    # 读取告警去人弹窗中的确认告警个数
    def get_alarm_handle_num(self):
        link = 'xpath=>//*[@id="number"]'
        num = self.find_element(link).text
        return num

    # 输入密码，账号不需要输入
    def input_password(self, pwd):
        link = 'xpath=>//*[@id="password"]'
        self.type(link, pwd)

    # 获取选定的告警码列表
    def get_alarm_handle_arr(self):
        link = 'xpath=>//*[@id="choicedAlarmInfos"]'
        arr = self.get_value(link)
        return arr

    # 输入处理信息描述
    def input_alarm_handle_desc(self, description):
        link = 'xpath=>//*[@id="alarmHandleDesc"]'
        self.type(link, description)

    # 点击确认告警 ‘密码不正确’'告警处理成功'
    def handle_alarm_submit_click(self):
        link = 'xpath=>//*[@id="btn_handleAlarnmInfoSubmit"]'
        self.click(link)

    # 点击手动清除告警历史 跳转页面到page_alarm_mgr_result
    def handle_del_alarm_hty_click(self):
        link = 'xpath=>//*[@id="btn_alarmHandleResults"]'
        self.click(link)
        self.sleep(0.5)