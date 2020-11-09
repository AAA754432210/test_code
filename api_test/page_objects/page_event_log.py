from api_test.base_page.homepage import HomePage
from common.Log import Logger
from selenium.webdriver.support.select import Select

logger = Logger("EventLogPage").getlog()


class EventLogPage(HomePage):

    # 点击刷新
    def refresh_click(self):
        refresh_link = 'xpath=>//*[@id="vueApp"]/div[2]/div/div/div/div/div[1]/div[1]/div[2]/button'
        self.click(refresh_link)

    # 点击搜索
    def search_click(self):
        search_link = 'xpath=>//*[@id="vueApp"]/div[1]/div[2]/div[1]/div/button'
        self.click(search_link)

    # 输入搜索
    def input_search(self, value):
        # //*[@id="vueApp"]/div[2]/div/div/div/div[1]/div[1]/div[3]/input
        link = 'xpath=>//*[@id="vueApp"]/div[2]/div/div/div/div/div[1]/div[1]/div[3]/input'
        self.type(link, str(value))

    # 输入时间范围
    def input_time_frame(self, days):
        # //*[@id="vueApp"]/div[1]/div[2]/div[2]/div/form[1]/div[1]/div/div/input
        link = 'xpath=>//*[@id="vueApp"]/div[1]/div[2]/div[2]/div/form/div[1]/div/div/div/input'
        self.type(link, str(days))

    # 输入开始时间
    def input_start_time(self, start_time):
        # //*[@id="vueApp"]/div[1]/div[2]/div[2]/div/form[1]/div[2]/div/div/input
        link = 'xpath=>//*[@id="vueApp"]/div[1]/div[2]/div[2]/div/form/div[2]/div/div/div/input'
        self.type(link, str(start_time))

    # 输入结束时间
    def input_end_time(self, end_time):
        # //*[@id="vueApp"]/div[1]/div[2]/div[2]/div/form[1]/div[3]/div/div/input
        link = 'xpath=>//*[@id="vueApp"]/div[1]/div[2]/div[2]/div/form/div[3]/div/div/div/input'
        self.type(link, str(end_time))

    # 点击接收
    def recv_click(self):
        # //*[@id="vueApp"]/div[1]/div[2]/div[2]/div/form[2]/div[1]/div/button
        link = 'xpath=>//*[@id="vueApp"]/div[1]/div[2]/div[2]/div/form/div[4]/div/div/button'
        self.click(link)

    # 点击发送
    def send_click(self):
        # //*[@id="vueApp"]/div[1]/div[2]/div[2]/div/form[2]/div[2]/div/button
        link = 'xpath=>//*[@id="vueApp"]/div[1]/div[2]/div[2]/div/form/div[5]/div/div/button'
        self.click(link)

    # 获取记录数目 //*[@id="vueApp"]/div[2]/div/div/div/div[1]/div[3]/div[1]/span[1]
    def get_event_log_num(self):
        link = 'xpath=>//*[@id="vueApp"]/div[2]/div/div/div/div/div[1]/div[3]/div[1]/span[1]'
        txt = self.find_element(link).text
        a = [int(i) for i in txt if str.isdigit(i)]
        count = 0
        if a[0] == 1 and a[1] == 2 and a[2] == 0:
            for i in range(3, len(a)):
                count += (10 ** (len(a) - 1 - i)) * a[i]
        else:
            count = a[-1]
        logger.info('共找到%s条记录' % count)
        return count

    # 当页数大于等于7页时 最后一页的位置就不变了
    # 点击最后一页 '//*[@id="vueApp"]/div[2]/div/div/div/div/div[1]/div[3]/div[2]/ul/li[8]/a'
    def last_page_click(self, num):
        if num % 20 == 0:
            page_num = num // 20
        else:
            page_num = num // 20 + 1
        if page_num >= 7:
            index = 8
        else:
            index = page_num + 1
        link = 'xpath=>//*[@id="vueApp"]/div[2]/div/div/div/div/div[1]/div[3]/div[2]/ul/li[' + str(index) + ']/a'
        self.click(link)
        logger.info('点击最后一页记录')
        return

    # 点击第一页
    def first_page_click(self):
        link = 'xpath=>//*[@id="vueApp"]/div[2]/div/div/div/div/div[1]/div[3]/div[2]/ul/li[2]/a'
        self.click(link)
        logger.info('点击第一页记录')
        return

    # 获取最后一项数据
    def get_last_obj_value(self, num):
        self.last_page_click(num)
        obj_num = num % 20
        if obj_num == 0:
            obj_num = 20
        arr_log = self.get_event_log_info(obj_num)
        logger.info('获取最后一项记录数据')
        return arr_log[-1]

    #
    # dict_log = {'Day': '', 'Time': '', 'TransId': '',
    #             'Sender': '', 'Receiver': '', 'Type': '',
    #             'info': ''}
    # arr_link = [{'Day': 'xpath=>//*[@id="bspTable"]/tbody/tr[' + str(i) + ']/td[2]/div/div[1]',
    #              'Time': 'xpath=>//*[@id="bspTable"]/tbody/tr[' + str(i) + ']/td[2]/div/div[2]',
    #              'TransId': 'xpath=>//*[@id="bspTable"]/tbody/tr[' + str(i) + ']/td[3]/div/div[1]/span[1]',
    #              'Sender': 'xpath=>//*[@id="bspTable"]/tbody/tr[' + str(i) + ']/td[3]/div/div[1]/span[3]',
    #              'Receiver': 'xpath=>//*[@id="bspTable"]/tbody/tr[' + str(i) + ']/td[3]/div/div[1]/span[4]',
    #              'Type': 'xpath=>//*[@id="bspTable"]/tbody/tr[' + str(i) + ']/td[3]/div/div[1]/span[6]',
    #              'info': 'xpath=>//*[@id="bspTable"]/tbody/tr[' + str(i) + ']/td[3]/div/div[2]'} for i in range(1, 22)]
    # 获取event_log信息
    def get_event_log_info(self, num):
        arr_log = []
        dict_log = {'Day': '', 'Time': '', 'TransId': '',
                    'Sender': '', 'Receiver': '', 'Type': '',
                    'info': ''}
        for i in range(num):
            dict_link = {'Day': 'xpath=>//*[@id="bspTable"]/tbody/tr[' + str(i + 1) + ']/td[2]/div/div[1]',
                         'Time': 'xpath=>//*[@id="bspTable"]/tbody/tr[' + str(i + 1) + ']/td[2]/div/div[2]',
                         'TransId': 'xpath=>//*[@id="bspTable"]/tbody/tr[' + str(i + 1) + ']/td[3]/div/div[1]/span[1]',
                         'Sender': 'xpath=>//*[@id="bspTable"]/tbody/tr[' + str(i + 1) + ']/td[3]/div/div[1]/span[2]',
                         'Receiver': 'xpath=>//*[@id="bspTable"]/tbody/tr[' + str(i + 1) + ']/td[3]/div/div[1]/span[3]',
                         'Type': 'xpath=>//*[@id="bspTable"]/tbody/tr[' + str(i + 1) + ']/td[3]/div/div[1]/span[4]',
                         'info': 'xpath=>//*[@id="bspTable"]/tbody/tr[' + str(i + 1) + ']/td[3]/div/div[2]'}
            for key in dict_log:
                dict_log[key] = self.find_element(dict_link[key]).text
            arr_log.append(dict_log)
        return arr_log

    # 输入事件其他查询条件
    def input_other_qry_criteria(self, string):
        link = 'xpath=>//*[@id="inputSuccess5"]'
        self.type(link, str(string))
