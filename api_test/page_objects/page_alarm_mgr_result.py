from api_test.base_page.homepage import HomePage
from common.Log import Logger
from selenium.webdriver.support.select import Select

logger = Logger("AlarmHtyMgrPage").getlog()


class AlarmHtyMgrPage(HomePage):

    # 告警码输入
    def input_alarm_no(self, alarm_no):
        input_alarm_no_link = 'xpath=>//*[@id="ulAlarmNo"]'
        self.type(input_alarm_no_link, str(alarm_no))

    # 输入告警处理措施描述
    def input_alarm_description(self, txt):
        input_dev_id_link = 'xpath=>//*[@id="alarmDescriptionTxt"]'
        self.type(input_dev_id_link, str(txt))

    # 点击查询
    def alarm_qry_click(self):
        alarm_qry_link = 'xpath=>//*[@id="btn_query"]'
        self.click(alarm_qry_link)

    def return_click(self):
        link = 'xpath=>//*[@id="btn_return"]'
        self.click(link)

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

    # 点击手动清除历史 跳转页面
    def user_handle_history_click(self):
        link = 'xpath=>//*[@id="btn_queryUserHandlehistoy"]'
        self.click(link)

    # 获取记录条数
    def get_alarm_handle_num(self):
        link = 'xpath=>/html/body/div[1]/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[3]/div[1]/span[1]'
        txt = self.find_element(link).text
        a = [int(i) for i in txt if str.isdigit(i)]
        count = 0
        if a[0] == 1 and a[1] == 1 and a[2] == 0:
            for i in range(3, len(a)):
                count += (10 ** (len(a) - 1 - i)) * a[i]
        else:
            count = a[-1]
        logger.info('共找到%s条记录' % count)
        return count

    # 选择指定告警 alarm_id为全局唯一告警号，alarm_no为告警码 可以根据告警号或者告警码进行获取
    # 如使用告警码这直接获取该告警码最近一次的结果
    def alarm_select_click(self, alarm_num, func, alarm_id=0, alarm_no=0):
        if alarm_id == alarm_no == 0:
            logger.error('至少指定告警号和告警码其中一种')
            return False
        index = 2 if alarm_id != 0 else 3
        for i in range(1, alarm_num+1):
            choose_box_link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[' + str(index) +']'
            record_alarm_no = self.find_element(choose_box_link_temp).text
            if record_alarm_no == str(alarm_no):
                # choose_box_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[1]/label/input'
                # self.click(choose_box_link)
                logger.info("选择指定告警编号成功 alarm_no:%s" % str(alarm_no))
                return func(i)
        logger.info("选择指定告警编号失败 alarm_no:%s" % str(alarm_no))
        return False

    # 选择指定告警,点击告警详情,查询之后
    def alarm_select_click_single(self, alarm_no='0'):
        link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr/td[3]'  # 告警码
        try:
            if self.find_element(link_temp).text == str(alarm_no) or alarm_no == '0':
                choose_box_link = 'xpath=>//*[@id="tb_list"]/tbody/tr/td[7]/a/button'
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
            link = 'xpath=>/html/body/div[1]/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[3]/div[2]/ul/li[' + str(
                i) + ']/a'
            try:
                self.find_element(link)
            except ValueError:
                return i
        return

    def last_page_click(self, index):
        link = 'xpath=>/html/body/div[1]/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[3]/div[2]/ul/li[' + str(
            index) + ']/a'
        self.click(link)

    # 选择指定的告警 推荐使用
    def alarm_spec_select(self, dict_qry):
        self.input_alarm_description(dict_qry['告警码'])
        self.input_alarm_description(dict_qry['告警处理措施描述'])
        self.alarm_qry_click()
        num = self.get_alarm_handle_num()
        index = self.alarm_select_click(num, alarm_id=dict_qry['告警号'], alarm_no=dict_qry['告警码'])
        if not index:
            logger.error('无法找到指定告警码')
            self.get_windows_img()
            return 0
        return index

        # 目前告警详情按钮无法点击，后续代码待补全
