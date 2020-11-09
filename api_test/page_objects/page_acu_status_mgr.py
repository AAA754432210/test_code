from api_test.base_page.homepage import HomePage
from common.Log import Logger
from selenium.webdriver.support.select import Select

logger = Logger("AcuStatMgrPage").getlog()


class AcuStatMgrPage(HomePage):

    # ACU身份标识填写
    def choose_acu_by_id(self, deviceid):
        choose_acu_link = 'xpath=>//*[@id="Term"]'
        self.type(choose_acu_link, str(deviceid))

    # 在线状态选择 'null'全部；'0'上线；'1'下线，默认为全部
    def choose_status(self, value):
        sel = self.find_element('xpath=>//*[@id="LocatfffionDesc"]')
        self.wait(2)
        Select(sel).select_by_value('%s' % str(value))

    # 点击刷新
    def refresh_click(self):
        refresh_link = 'xpath=>/html/body/div[1]/div[1]/div[3]/div[2]/div/div[2]/div/div/div[2]/div[1]/div[2]/button'
        self.click(refresh_link)

    # 点击全屏
    def full_screen_click(self):
        full_screen_link = 'xpath=>/html/body/div[1]/div[1]/div[3]/div[2]/div/div[2]/div/div/div[2]/div[1]/div[' \
                           '2]/div/button '
        self.click(full_screen_link)

    # 点击全选
    def all_election_click(self):
        slect_all_click = 'xpath=//*[@id="tb_list"]/thead/tr/th[1]/div[1]/label/input'
        self.click(slect_all_click)

    # # 选择指定唯一标识设备
    # def device_select_click(self, devid):
    #     for i in range(1, 10):
    #         choose_box_link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[2]'
    #         if self.find_element(choose_box_link_temp).text == devid:
    #             choose_box_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[1]/label/input'
    #             self.click(choose_box_link)
    #             logger.info("点击指定标识设备成功 acudevid:%u" % devid)
    #             return i
    #
    #     logger.info("点击指定标识设备失败 acudevid:%u" % devid)
    #     i = 0
    #     return i

    # 选择指定唯一标识设备 当前版本并不支持
    def device_select_click(self, dev_id):
        for i in range(1, 10):
            choose_box_link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[2]'
            try:
                record_version_id = self.find_element(choose_box_link_temp).text
                if record_version_id == str(dev_id):
                    choose_box_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[1]/label/input'
                    self.click(choose_box_link)
                    logger.info("点击指定标识设备成功 dev_id:%s" % str(dev_id))
                    return i
            except ValueError:
                logger.info("点击指定标识设备失败 dev_id:%s" % str(dev_id))
                i = 0
                return i

    # 点击返回ACU管理
    def back_to_acu_mgr_page_click(self):
        back_to_acu_mgr_page_link = 'xpath=>//*[@id="btn_return"]'
        self.click(back_to_acu_mgr_page_link)
