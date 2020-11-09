from api_test.base_page.homepage import HomePage
from common.Log import Logger
from selenium.webdriver.support.select import Select
from framework.browser_engine import BrowserEngine

logger = Logger("DrcStatMgrPage").getlog()


class DrcStatMgrPage(HomePage):

    # DRC系统唯一标识
    def input_drc_id(self, drc_id):
        input_drc_id_link = 'xpath=>//*[@id="Term"]'
        self.type(input_drc_id_link, str(drc_id))

    def qry_click(self):
        link = 'xpath=>//*[@id="btn_query"]'
        self.click(link)
        self.sleep(1)

    # 点击刷新
    def refresh_click(self):
        refresh_link = 'xpath=>/html/body/div/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[1]/div[2]/button'
        self.click(refresh_link)

    # 点击全屏
    def full_screen_click(self):
        full_screen_link = 'xpath=>/html/body/div/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div/button'
        self.click(full_screen_link)

    # 点击全选
    def all_election_click(self):
        slect_all_click = 'xpath=//*[@id="tb_list"]/thead/tr/th[1]/div[1]/label/input'
        self.click(slect_all_click)

    # 选择指定唯一标识设备 没啥用
    def device_select_click(self, drc_id):
        try:
            for i in range(1, 10):
                choose_box_link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[2]'
                if self.find_element(choose_box_link_temp).text == str(drc_id):
                    choose_box_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[1]/label/input'
                    self.click(choose_box_link)
                    logger.info("点击指定标识设备成功 drc_id:%u" % str(drc_id))
                    return i
        except:
            logger.info("点击指定标识设备失败 drc_id:%u" % str(drc_id))
            return 0

    # 获取状态上报的条数
    def get_the_report_num(self):
        link = 'xpath=>/html/body/div/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[3]/div[1]/span[1]'
        txt = self.find_element(link).text
        a = [int(i) for i in txt if str.isdigit(i)]
        count = 0
        if a[0] == 1 and a[1] == 1 and a[2] == 0:
            for i in range(3, len(a)):
                count += (10 ** (len(a) - 1 - i)) * a[i]
        else:
            count = a[-1]
        return count

    # 获取指定drc状态上报是上线还是下线 只有唯一一个的时候index填0
    def get_drc_report_status(self, index='0'):
        if str(index) == '0':
            index_str = ''
        else:
            index_str = '[' + str(index) + ']'
        drc_status_link = 'xpath=>//*[@id="tb_list"]/tbody/tr' + index_str + '/td[3]'
        drc_status = self.find_element(drc_status_link).text
        logger.info("drc状态上报信息为:%s" % drc_status)
        if drc_status == '上线':
            return True
        else:
            self.get_windows_img()
            return False

    # 点击返回DRC管理
    def back_to_drc_mgr_page(self):
        back_to_drc_mgr_page_link = 'xpath=>//*[@id="btn_return"]'
        self.click(back_to_drc_mgr_page_link)

    # 暂时只支持一页以内的 drc的数量不为一 drc数量不超过10
    def get_online_drc(self):
        # '//*[@id="tb_list"]/tbody/tr[2]/td[2]'
        # '/html/body/div/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[3]/div[1]/span[1]'
        count = self.get_the_report_num()
        online = []
        outline = []
        for i in range(1, count + 1):
            drc_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[2]'
            status_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[3]'
            print(i, status_link)
            # '//*[@id="tb_list"]/tbody/tr[1]/td[3]'
            # '//*[@id="tb_list"]/tbody/tr[1]/td[3]'
            status = self.find_element(status_link).text
            drc = self.find_element(drc_link).text
            if status == '上线':
                online.append(drc)
            else:
                outline.append(drc)
        logger.info('获取全部drc状态成功，激活drc：%s，未激活drc：%s' % (online, outline))
        return online, outline

    # 获取指定drc的全部信息 先通过查询确定唯一drc
    def get_spec_drc_info_(self):
        list_drc_info_key = ['drc系统唯一标识', '工作时间', '工作温度', 'DRSU在线数量',
                              'ACU在线数量', '各核CPULOAD', '内存', '空闲内存',
                              '使用内存', '缓存', '分区总量', '分区空闲', '分区使用',
                              '分区可用内存', '创建时间', '状态']
        list_j = []
        try:
            for i in range(2, 18):
                # '//*[@id="tb_list"]/tbody/tr[1]/td[2]'
                link = 'xpath=>//*[@id="tb_list"]/tbody/tr/td[' + str(i) + ']'
                para = self.find_element(link).text
                list_j.append(para)
            dict_drc_info = dict(zip(list_drc_info_key, list_j))
            logger.info('获取drc状态周期上报数据成功%s' % dict_drc_info)
            return dict_drc_info
        except Exception as e:
            logger.error('获取drc状态周期上报数据失败', format(e))
            return None

    def get_spec_drc_info(self, drc_id):
        self.input_drc_id(drc_id)
        self.qry_click()
        if self.get_the_report_num() != 1:
            logger.error('获取指定drc失败，请输入正确地drc_id')
            self.get_windows_img()
            return None
        return self.get_spec_drc_info_()

    def get_spec_drc_status(self, drc_id):
        self.input_drc_id(drc_id)
        self.qry_click()
        if self.get_the_report_num() != 1:
            logger.error('获取指定drc失败，请输入正确地drc_id')
            self.get_windows_img()
            return False
        return self.get_drc_report_status()