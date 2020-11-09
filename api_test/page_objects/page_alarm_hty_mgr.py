from api_test.base_page.homepage import HomePage
from common.Log import Logger
from selenium.webdriver.support.select import Select

logger = Logger("AlarmHtyMgrPage").getlog()


class AlarmHtyMgrPage(HomePage):

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

    # 填写发生时间范围 格式：'2020-04-07 00:00:00 - 2020-05-13 00:00:00'
    def alarm_add_time(self, time_frame):
        alarm_time_link = 'xpath=>//*[@id="Talarmtime"]'
        self.type(alarm_time_link, time_frame)

    # 填写消除时间范围 格式：'2020-04-07 00:00:00 - 2020-05-13 00:00:00'
    def alarm_del_time(self, time_frame):
        alarm_time_link = 'xpath=>//*[@id="sAlarmDelTime"]'
        self.type(alarm_time_link, time_frame)

    # 点击查询
    def alarm_qry_click(self):
        alarm_qry_link = 'xpath=>//*[@id="btn_query"]'
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
        slect_all_click = 'xpath=//*[@id="tb_list"]/thead/tr/th[1]/div[1]/label/input'
        self.click(slect_all_click)

    # 点击手动清除历史 跳转页面到page_alarm_mgr_result
    def user_handle_history_click(self):
        link = 'xpath=>//*[@id="btn_queryUserHandlehistoy"]'
        self.click(link)

    # 选择指定告警
    def alarm_select_click(self, alarm_no):
        for i in range(1, 12):
            choose_box_link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[2]'
            try:
                record_alarm_no = self.find_element(choose_box_link_temp).text
                if record_alarm_no == str(alarm_no):
                    choose_box_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[1]/label/input'
                    self.click(choose_box_link)
                    logger.info("点击指定告警编号成功 alarm_no:%s" % str(alarm_no))
                    return i
            except ValueError:
                logger.info("点击指定告警编号失败 alarm_no:%s" % str(alarm_no))
                i = 0
                return i

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

    # 点击最后一页 原理是不断去获取下一项内容，如果返回错误，说明没有找到元素，返回一个index值 index页获取不到 index-1页就是>页
    # index - 2 就是能够获取的最后一页 '/html/body/div[1]/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[3]/div[2]/ul/li[2]/a'
    def last_page_find(self):
        logger.info('以下错误log不需要关注！！！！！')
        for i in range(2, 12):
            print('第%u页' % (i - 1))
            link = 'xpath=>/html/body/div[1]/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[3]/div[2]/ul/li[' + str(i) + ']/a'
            try:
                self.find_element(link)
            except ValueError:
                return i
        return 0

    def last_page_click(self, index):
        link = 'xpath=>/html/body/div[1]/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[3]/div[2]/ul/li[' + str(index) + ']/a'
        self.click(link)

    # '/html/body/div/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[3]/div[2]/ul/li[1]/a' <页
    # '/html/body/div/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[3]/div[2]/ul/li[2]/a' 只有一页情况下第一页
    # '/html/body/div/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[3]/div[2]/ul/li[2]/a' 第一页
    # '/html/body/div/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[3]/div[2]/ul/li[9]/a' >页
    # '/html/body/div/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[3]/div[2]/ul/li[8]/a' 最后一页
    # '/html/body/div/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[3]/div[2]/ul/li[7]/a' ..省略页
    # 如果有第9项 那么第八项就是最后一项

    # 获取最后一项的数据 暂时不需要获取数据
    # def last_opt_click(self):
    #     status = ''
    #     for i in range(1, 11):
    #         print('第%u项' % i)
    #         #'//*[@id="tb_list"]/tbody/tr[9]/td[1]/label/input'
    #         link = 'xpath=>//*[@id="tb_Updatedlist"]/tbody/tr[' + str(i) + ']/td[9]'
    #         try:
    #             status = self.find_element(link).text
    #         except ValueError:
    #             return status