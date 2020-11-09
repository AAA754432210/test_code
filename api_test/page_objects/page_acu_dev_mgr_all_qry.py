from api_test.base_page.homepage import HomePage
from common.Log import Logger

logger = Logger("AcuDevMgrAllQryPage").getlog()


# acu设备配置可以同时制定多个设备
# 该页面点击取消或者弹窗告警确认之后会回到AcuDevMgrPage
# 该页面点击设备配置之后会跳到AcuDevMgrSpecCfgPage
class AcuDevMgrAllQryPage(HomePage):

    # def is_exist_alert(self):
    #     try:
    #         alert = self.find_element('xpath=>/html/body/div[2]/div/div[2]/div/h3')
    #         logger.info("弹出提示：\' %s \'" % alert.text)
    #         return True
    #     except Exception as e:77777777777777
    #         logger.info("未弹出配置所有的ACU弹窗%s" % format(e))
    #         return False

    # # 点击刷新
    # def refresh_click(self):
    #     refresh_link = 'xpath=>/html/body/div[1]/div/div[3]/div/div/div/div[2]/div/div/div[2]/div[1]/div[2]/button'
    #     self.click(refresh_link)

    # 点击全屏
    def full_screen_click(self):
        full_screen_link = 'xpath=>/html/body/div[1]/div/div[3]/div[2]/div/div/div/div/div[2]/div[1]/div[2]/div/button'
        self.click(full_screen_link)

    # 点击返回
    def return_click(self):
        return_link = 'xpath=>//*[@id="btn_config"]'
        self.click(return_link)

    # 点击运行版本
    def run_version_click(self):
        run_version_link = 'xpath=>//*[@id="btn_versionquery"]'
        self.click(run_version_link)

    # # 点击全选
    # def all_election_click(self):
    #     slect_all_click = 'xpath=>//*[@id="tb_list"]/thead/tr/th[1]/div[1]/label/input'
    #     self.click(slect_all_click)

    # 选择指定唯一标识设备
    # def device_select_click(self, devid):
    #     for i in range(1, 10):
    #         choose_box_link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[2]'
    #         if self.find_element(choose_box_link_temp).text == devid:
    #             choose_box_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[1]/label/input'
    #             self.click(choose_box_link)
    #             logger.info("点击指定标识设备成功 devid:%u" % devid)
    #             return i
    #     logger.info("点击指定标识设备失败 devid:%u" % devid)
    #     i = 0
    #     return i
