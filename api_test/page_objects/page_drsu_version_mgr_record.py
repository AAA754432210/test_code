from api_test.base_page.homepage import HomePage
from common.Log import Logger

logger = Logger("DrsuVerMgrRecordPage").getlog()


class DrsuVerMgrRecordPage(HomePage):

    # 填入DRC唯一标识
    def input_drc_id(self, drc_id):
        input_drc_id_link = 'xpath=>//*[@id="Term"]'
        self.type(input_drc_id_link, str(drc_id))

    # 点击查询
    def qry_click(self):
        qry_link = 'xpath=>//*[@id="btn_query"]'
        self.click(qry_link)

    # # 选择DRC_ID
    # def choose_drc_id(self, drc_id):
    #     sel = self.find_element('xpath=>//*[@id="drcChoiceListId"]')
    #     self.wait(2)
    #     # 后续通过读取配置文件得到drc_id
    #     Select(sel).select_by_value('%s' % str(drc_id))

    # 点击返回DRSU版本管理
    def return_click(self):
        return_link = 'xpath=>//*[@id="btn_return"]'
        self.click(return_link)

    # 点击升级结果查看
    def show_updated_click(self):
        show_updated_link = 'xpath=>//*[@id="btn_showUpdated"]'
        self.click(show_updated_link)

    # 是否弹出DRSU软件版本远程升级弹窗
    def is_prompt_visible(self):
        selector = '//*[@id="drcRemoteUpdatedLabel"]'
        ret = self.is_visible(selector)
        logger.info("是否弹出DRSU软件版本远程升级弹窗%s" % ret)
        return ret

    # 点击最后一页 原理是不断去获取下一项内容，如果返回错误，说明没有找到元素，返回一个index值 index页获取不到 index-1页就是>页
    # index - 2 就是能够获取的最后一页  但是当页数比较多时
    def last_page_find(self):
        logger.info('以下错误log不需要关注！！！！！')
        for i in range(2, 100):
            print('第%u页' % (i - 1))
            # link = 'xpath=>//*[@id="drcRemoteUpdated"]/div/div/div[2]/div/div/div[2]/div/div/div[1]/div[3]/div[' \
            #        '2]/ul/li[' + str(i) + ']/a'
            link = 'xpath=>//*[@id="drsuRemoteUpdated"]/div/div/div[2]/div/div/div/div/div/div[1]/div[3]/div[2]/ul/li[' + str(i) + ']/a'
            try:
                self.find_element(link)
            except ValueError:
                return i
        return

    def last_page_click(self, index):
        # link = 'xpath=>//*[@id="drcRemoteUpdated"]/div/div/div[2]/div/div/div[2]/div/div/div[1]/div[3]/div[' \
        #        '2]/ul/li[' + str(index) + ']/a'
        link = 'xpath=>//*[@id="drsuRemoteUpdated"]/div/div/div[2]/div/div/div/div/div/div[1]/div[3]/div[2]/ul/li[' + str(
            index) + ']/a'
        self.click(link)

    # '/html/body/div/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[3]/div[2]/ul/li[1]/a' <页
    # '/html/body/div/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[3]/div[2]/ul/li[2]/a' 只有一页情况下第一页
    # '/html/body/div/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[3]/div[2]/ul/li[2]/a' 第一页
    # '/html/body/div/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[3]/div[2]/ul/li[9]/a' >页
    # '/html/body/div/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[3]/div[2]/ul/li[8]/a' 最后一页
    # '/html/body/div/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[3]/div[2]/ul/li[7]/a' ..省略页
    # 如果有第9项 那么第八项就是最后一项
    # 获取最后一项的数据
    def last_opt_click(self):
        status = ''
        for i in range(1, 12):
            print('第%u项' % i)
            link = 'xpath=>//*[@id="tb_Updatedlist"]/tbody/tr[' + str(i) + ']/td[9]'
            try:
                status = self.find_element(link).text
            except ValueError:
                return status

    # 点击刷新
    def refresh_click(self):
        refresh_link = 'xpath=>/html/body/div/div/div[3]/div[2]/div/div[2]/div/div/div[2]/div[1]/div[2]/button'
        self.click(refresh_link)

    # 点击全屏
    def full_screen_click(self):
        full_screen_link = 'xpath=>/html/body/div/div/div[3]/div[2]/div/div[2]/div/div/div[2]/div[1]/div[2]/div/button'
        self.click(full_screen_link)

    # 点击全选
    def all_election_click(self):
        select_all_click = 'xpath=//*[@id="tb_list"]/thead/tr/th[1]/div[1]/label/input'
        self.click(select_all_click)

    # 选择指定唯一标识设备
    def dev_select_click(self, drc_id):
        for i in range(1, 12):
            choose_box_link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[2]'
            if self.find_element(choose_box_link_temp).text == str(drc_id):
                choose_box_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[1]/label/input'
                self.click(choose_box_link)
                logger.info("点击drc系统唯一标识成功 drc_id:%s" % str(drc_id))
                return i
        logger.info("点击drc系统唯一标识失败 drc_id:%s" % str(drc_id))
        return 0

    # 选择指定唯一标识设备 升级版本
    def version_select_click1(self, version_id):
        for i in range(1, 12):
            choose_box_link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[2]'
            try:
                record_version_id = self.find_element(choose_box_link_temp).text
                if record_version_id == str(version_id):
                    choose_box_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[1]/label/input'
                    self.click(choose_box_link)
                    logger.info("点击版本记录编号成功 version_id:%s" % str(version_id))
                    return i
            except ValueError:
                logger.info("点击版本记录编号失败 version_id:%s" % str(version_id))
                i = 0
                return i

    # 点击drc设备升级
    def drc_dev_update_click(self):
        drc_dev_update_link = 'xpath=>//*[@id="tb_list"]/tbody/tr/td[9]/a/button'
        self.click(drc_dev_update_link)

    # 点击关闭
    def close_window_click(self):
        close_window_link = 'xpath=>//*[@id="drcRemoteUpdated"]/div/div/div[3]/button'
        self.click(close_window_link)
