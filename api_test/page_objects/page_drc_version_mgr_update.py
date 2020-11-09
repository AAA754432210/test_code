from api_test.base_page.homepage import HomePage
from common.Log import Logger

logger = Logger("DrcVerMgrUpdatePage").getlog()


# 改页面和page_drsu_version_mgr_record高度相似
class DrcVerMgrUpdatePage(HomePage):

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

    # 点击返回DRC版本管理
    def return_click(self):
        return_link = 'xpath=>//*[@id="btn_return"]'
        self.click(return_link)

    # 点击升级结果查看
    def show_updated_click(self):
        show_updated_link = 'xpath=>//*[@id="btn_showUpdated"]'
        self.click(show_updated_link)

    # 是否弹出DRSU软件版本远程升级弹窗 为什么是drsu
    def is_prompt_visible_result(self):
        selector = '//*[@id="drcRemoteUpdatedLabel"]'
        ret = self.is_visible(selector)
        logger.info("是否弹出DRSU软件版本远程升级弹窗%s" % ret)
        return ret

    # //*[@id="tb_Updatedlist"]/tbody/tr[1]/td[9]
    # 获取最后一次的升级结果信息
    def get_the_last_update_result(self):
        result_link = 'xpath=>//*[@id="tb_Updatedlist"]/tbody/tr[1]/td[9]'
        version_link = 'xpath=>//*[@id="tb_Updatedlist"]/tbody/tr[1]/td[4]'
        result = self.find_element(result_link).text
        version = self.find_element(version_link).text
        return result, version

    # 点击最后一页 原理是不断去获取下一项内容，如果返回错误，说明没有找到元素，返回一个index值 index页获取不到 index-1页就是>页
    # index - 2 就是能够获取的最后一页  但是当页数比较多时
    def last_page_find(self):
        logger.info('以下错误log不需要关注！！！！！')
        for i in range(2, 100):
            link = 'xpath=>//*[@id="drcRemoteUpdated"]/div/div/div[2]/div/div/div[2]/div/div/div[1]/div[3]/div[' \
                   '2]/ul/li[' + str(i) + ']/a'
            try:
                self.find_element(link)
            except ValueError:
                return i
        return i

    def last_page_click(self, index):
        link = 'xpath=>//*[@id="drcRemoteUpdated"]/div/div/div[2]/div/div/div[2]/div/div/div[1]/div[3]/div[' \
               '2]/ul/li[' + str(index) + ']/a'
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
            link = 'xpath=>//*[@id="tb_Updatedlist"]/tbody/tr[' + str(i) + ']/td[9]'
            try:
                status = self.find_element(link).text
            except ValueError:
                return status

    # 点击关闭 drsu软件版本远程升级弹窗
    def close_window_click(self):
        close_window_link = 'xpath=>//*[@id="drcRemoteUpdated"]/div/div/div[3]/button'
        self.click(close_window_link)

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

    # 选择指定唯一标识设备 升级版本
    def dev_select_click(self, drc_id):
        for i in range(1, 10):
            choose_box_link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[2]'
            try:
                record_drc_id = self.find_element(choose_box_link_temp).text
                if record_drc_id == str(drc_id):
                    choose_box_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[1]/label/input'
                    self.click(choose_box_link)
                    logger.info("点击drc系统唯一标识成功 drc_id:%s" % str(drc_id))
                    return i
            except ValueError:
                logger.info("点击drc系统唯一标识失败 drc_id:%s" % str(drc_id))
                return 0

    # 查询结束 只剩下一个drc的时候的时候用这个
    def dev_select_click_single(self, drc_id='0'):
        choose_box_link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr/td[2]'
        try:
            if self.find_element(choose_box_link_temp).text == str(drc_id) or str(drc_id) == '0':
                choose_box_link = 'xpath=>//*[@id="tb_list"]/tbody/tr/td[1]/label/input'
                self.click(choose_box_link)
                logger.info("点击drc系统唯一标识成功 drc_id:%s" % str(drc_id))
                return True
            else:
                logger.error("点击drc系统唯一标识失败 drc_id:%s" % str(drc_id))
                return False
        except Exception as e:
            logger.error("没有找到指定drc_id,%s" % format(e))
            raise False

    # 点击drc设备升级
    def drc_dev_update_click(self, index=''):
        if index == '':
            str_index = ''
        else:
            str_index = '[' + str(index) + ']'
        drc_dev_update_link = 'xpath=>//*[@id="tb_list"]/tbody/tr' + str_index + '/td[9]/a/button'
        self.click(drc_dev_update_link)

    # 是否弹出drc版本升级弹窗
    def is_prompt_visible_update(self):
        selector = '//*[@id="remoteUpdateDRCModalLabel"]'
        ret = self.is_visible(selector)
        logger.info("是否弹出DRC版本升级弹窗%s" % ret)
        return ret

    # 选择是否强制升级 现在默认都是不强制升级
    def check_is_force(self):
        check_is_force_link = 'xpath=>//*[@id="check_isForce"]'
        self.click(check_is_force_link)

    # 选择指定版本记录编号
    def version_select_click(self, version_id):
        for i in range(1, 12):
            choose_box_link_temp = 'xpath=>//*[@id="tb_remoteUpdatelist"]/tbody/tr[' + str(i) + ']/td[2]'
            try:
                record_version_id = self.find_element(choose_box_link_temp).text
                if record_version_id == str(version_id):
                    choose_box_link = 'xpath=>//*[@id="tb_remoteUpdatelist"]/tbody/tr[' + str(
                        i) + ']/td[1]/label/input'
                    self.click(choose_box_link)
                    logger.info("点击版本记录编号成功 version_id:%s" % str(version_id))
                    return i
            except ValueError:
                logger.info("点击版本记录编号失败 version_id:%s" % str(version_id))
                return 0

    # 选择版本记录名称 升级版本
    def version_select_click1(self, version_name):
        for i in range(1, 12):
            choose_box_link_temp = 'xpath=>//*[@id="tb_remoteUpdatelist"]/tbody/tr[' + str(i) + ']/td[3]'
            try:
                record_version_id = self.find_element(choose_box_link_temp).text
                if record_version_id == str(version_name):
                    choose_box_link = 'xpath=>//*[@id="tb_remoteUpdatelist"]/tbody/tr[' + str(
                        i) + ']/td[1]/label/input'
                    self.click(choose_box_link)
                    logger.info("点击版本名称成功 version_name:%s" % str(version_name))
                    return i
            except ValueError:
                logger.info("点击版本名称失败 version_name:%s" % str(version_name))
                i = 0
                return i

    # 点击关闭 drc版本升级弹窗
    def close_window_click1(self):
        close_window_link = 'xpath=>//*[@id="remoteUpdateDRCModal"]/div/div/div[3]/button[1]'
        self.click(close_window_link)

    # 点击执行DRC版本升级
    def version_update_click(self):
        version_upload_link = 'xpath=>//*[@id="btn_excuteDRCremoteUpdate"]'
        self.click(version_upload_link)

    # 选择drc 查询按键没有用 改函数暂时无法使用
    def choose_drc(self, drc_id):
        self.input_drc_id(drc_id)
        self.qry_click()
        return self.dev_select_click_single()

    # 获取状态上报的条数
    def get_the_report_num(self):
        link = 'xpath=>/html/body/div/div/div[3]/div[2]/div[1]/div[2]/div/div/div[1]/div[3]/div[1]/span[1]'
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

    # dict_update = {'drc_id': '', '版本编号': '', '是否强制': '', '预期结果': '发送升级请求成功'}
    # 高升低 错误状态码:32787 相同版本升级32787

    def drc_update(self, dict_update):
        drc_id = dict_update['drc_id']
        count = self.get_the_report_num()
        if count == 0:
            logger.error('没有找到任何可以升级的drc设备')
            self.get_windows_img()
            return False
        elif count == 1:
            # if not self.dev_select_click_single():
            #     logger.error('找不到指定的drc设备')
            #     self.get_windows_img()
            #     return False
            self.drc_dev_update_click()
        else:
            index_ = self.dev_select_click(drc_id)
            if index_ == 0:
                logger.error('找不到指定的drc设备')
                self.get_windows_img()
                return False
            self.drc_dev_update_click(index=str(index_))
        if not self.is_prompt_visible_update():
            logger.error('没有弹出弹窗')
            self.get_windows_img()
            self.info()
            return False
        if '是' == dict_update['是否强制升级']:
            self.check_is_force()
        if 0 == self.version_select_click(dict_update['版本记录编号']):
            logger.error('版本编号选择失败')
            self.get_windows_img()
            return False
        self.version_update_click()
        assert(self.info())
        if self.info_text() == dict_update['预期结果']:
            logger.info('升级结果与预期结果一致：%s' % dict_update['预期结果'])
            return True
        else:
            logger.error('升级结果与预期结果不一致，升级结果：%s，预期结果：%s' % (self.info_text(), dict_update['预期结果']))
            self.get_windows_img()
            return False

    # 查询drc升级结果
    def qry_drc_update_result(self, result, version):
        self.show_updated_click()
        if not self.is_prompt_visible_result():
            self.info()
            self.get_windows_img()
            return False
        result_, version_ = self.get_the_last_update_result()
        if result == result_ and version == version_:
            logger.info('版本升级结果与预期相符，升级结果：%s，当前版本号：%s' % (result_, version_))
            return True
        else:
            logger.error('版本升级结果与预期不相符，升级结果：%s，当前版本号：%s，预期结果：%s，预期版本号：%s' % (result_, version_, result, version))
            return False

