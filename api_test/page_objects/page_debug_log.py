from automation_framework_demo.api_test.base_page.homepage import HomePage
from automation_framework_demo.common.Log import Logger
from selenium.webdriver.support.select import Select

logger = Logger("DebugLogPage").getlog()


class DebugLogPage(HomePage):

    # 点击刷新
    def refresh_click(self):
        refresh_link = 'xpath=>//*[@id="vueApp"]/div[4]/div/div/div/div/div/div[1]/div[1]/div[2]/button'
        self.click(refresh_link)

    # 点击全屏
    def full_screen_click(self):
        full_screen_link = '//*[@id="vueApp"]/div[4]/div/div/div/div/div/div[1]/div[1]/div[2]/div/button'
        self.click(full_screen_link)

    # 日志时间范围开始时间
    def input_start_time(self, start_time):
        link = 'xpath=>//*[@id="vueApp"]/div[3]/div/form/div[1]/div/div[2]/div/input'
        self.type_force(link, str(start_time))

    # 日志时间范围结束时间
    def input_end_time(self, end_time):
        link = 'xpath=>//*[@id="vueApp"]/div[3]/div/form/div[2]/div/div/div/input'
        self.type_force(link, str(end_time))

    # input类型下拉框选择  参数link为下拉框的值，value为要选择的选项值
    def input_select_type_(self, link, value):
        # 采用css定位
        link2 = 'body > div.el-select-dropdown.el-popper > div.el-scrollbar > div.el-select-dropdown__wrap.el-scrollbar__wrap > ul'
        self.input_select(link, link2, value)

    # 选择日志类型 参数value填写‘全部’，‘定位日志’，‘外部事件’
    def choose_log_type(self, log_type):
        link = 'xpath=>//*[@id="vueApp"]/div[3]/div/form/div[3]/div/div[2]/div/div/input'
        self.input_select_type_(link, log_type)

    # 输入日志文件名
    def input_log_name(self, log_name):
        link = 'xpath=>//*[@id="vueApp"]/div[3]/div/form/div[4]/div/div[2]/div/input'
        self.type(link, str(log_name))

    # 点击查询
    def qry_click(self):
        link = 'xpath=>//*[@id="vueApp"]/div[3]/div/form/div[5]/div/div/button'
        self.click(link)

    # 获取记录数目
    def get_debug_log_num(self):
        link = 'xpath=>//*[@id="vueApp"]/div[4]/div/div/div/div/div/div[1]/div[3]/div[1]/span[1]'
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

    # 当页数大于等于7页时 最后一页的位置就不变了
    # 点击最后一页 //*[@id="vueApp"]/div[4]/div/div/div/div/div/div[1]/div[3]/div[2]/ul/li[8]/a
    def last_page_click(self, num):
        page_num = num//20 + 1 if num//20 else num//20
        index = 8 if page_num >=7 else page_num + 1
        link = 'xpath=>//*[@id="vueApp"]/div[4]/div/div/div/div/div/div[1]/div[3]/div[2]/ul/li[' + str(index) + ']/a'
        self.click(link)
        logger.info('点击最后一页记录')

    # 获取最后一项数据
    def get_last_opj_value(self, num):
        self.last_page_click(num)
        obj_num = num % 20 if num % 20 else 20
        index = 0 if obj_num == 1 else obj_num
        dict_log = self.get_spec_debug_log_info(index)
        logger.info('获取最后一项记录数据成功：%s' % dict_log)
        return dict_log

    # 获取当前页面第n条信息 2-8
    # '//*[@id="tb_RunLog"]/tbody/tr[1]/td[2]'
    # '//*[@id="tb_RunLog"]/tbody/tr[1]/td[9]/div/button' 下载按钮
    # '//*[@id="tb_RunLog"]/tbody/tr[2]/td[2]'
    def get_spec_debug_log_info(self, index):
        list_key = ['ID', '设备id', '开始时间',
                    '结束时间', '日志文件名', '日志类型',
                    '日志保存目录']
        list_j = []
        txt = '' if index == 0 else '[' + str(index) + ']'
        for i in range(2, 9):
            link = 'xpath=>//*[@id="tb_RunLog"]/tbody/tr' + txt + '/td[' + str(i) + ']'
            para = self.find_element(link).text
            list_j.append(para)
        dict_loge_info = dict(zip(list_key, list_j))
        return dict_loge_info

    def download_spec_debug_log_info(self, index):
        if(0 == index):
            link = 'xpath=>//*[@id="tb_RunLog"]/tbody/tr/td[9]/div/button'
        else:
            link = 'xpath=>//*[@id="tb_RunLog"]/tbody/tr[' + str(index) + ']/td[9]/div/button'
        self.click(link)


# print(EventLogPage.dict_link[0])
