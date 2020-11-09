import time
from api_test.base_page.homepage import HomePage
from common.Log import Logger
from selenium.webdriver.support.select import Select

logger = Logger("DrsuDevMgrPage").getlog()


class DrsuDevMgrPage(HomePage):

    # 选择DRC_ID
    def choose_drc_id(self, drc_id):
        sel = self.find_element('xpath=>//*[@id="drcChoiceListId"]')
        # self.wait(1)
        self.sleep(1)
        Select(sel).select_by_value('%s' % str(drc_id))
        # self.wait(1)
        self.sleep(1)

    # 在线状态选择 默认全部；'0'未激活；'1'激活
    def choose_status(self, value):
        sel = self.find_element('xpath=>//*[@id="zhuangtai"]')
        self.sleep(2)
        Select(sel).select_by_value('%s' % str(value))

    # 点击配置所有DRSU参数
    def all_drsu_parm_cfg_click(self):
        all_drsu_parm_cfg_link = 'xpath=>//*[@id="btn_allDrsuInDRCx"]'
        self.click(all_drsu_parm_cfg_link)
        self.sleep(1)

    # 是否存在输入弹窗
    # def is_exist_prompt(self):
    #     try:
    #         self.find_element('xpath=>//*[@id="peizhisuoyoudrcLabel"]')
    #         logger.info("弹出配置所有的DRSU弹窗")
    #         return True
    #     except Exception as e:
    #         logger.info("未弹出配置所有的DRSU弹窗")
    #         return False

    # 是否弹出配置所有的DRSU弹窗
    def is_prompt_visible_cfg_all_drsu(self):
        selector = '//*[@id="peizhisuoyoudrcLabel"]'
        ret = self.is_visible(selector)
        logger.info("是否弹出配置所有的DRSU弹窗%s" % ret)
        return ret

    # 选择数据上报周期 100 200 500 1000
    def choose_data_report_cycle(self, value):
        sel = self.find_element('xpath=>//*[@id="ulPeriodOfDataRpt"]')
        # self.wait(2)
        self.sleep(2)
        Select(sel).select_by_value('%s' % str(value))

    # 选择告警上报时间 10 30 self.sixty
    def choose_alarm_report_cycle(self, value):
        sel = self.find_element('xpath=>//*[@id="ulPeriodOfAlarmRpt"]')
        # self.wait(1)
        self.sleep(1)
        Select(sel).select_by_value('%s' % str(value))

    # 选择识别算法 0基本识别算法 1高级识别算法
    def choose_rec_algorithm(self, value):
        sel = self.find_element('xpath=>//*[@id="ulRecAlgorithm"]')
        # self.wait(1)
        self.sleep(1)
        Select(sel).select_by_value('%s' % str(value))

    # 选择是否长期有效 true false 注意是小写
    def choose_long_term_valid(self, value):
        sel = self.find_element('xpath=>//*[@id="longTermValid"]')
        # self.wait(1)
        self.sleep(1)
        Select(sel).select_by_value('%s' % str(value))

    # 点击关闭 点击弹窗的关闭按钮
    def close_window_click(self):
        # close_window_link = 'link_text=>"关闭"'
        close_window_link = 'xpath=>//*[@id="peizhisuoyoudrc"]/div/div/div[3]/button[1]'
        self.click(close_window_link)

    # 点击提交配置
    def submit_cfg_click(self):
        submit_cfg_link = 'xpath=>//*[@id="btn_tijiaopeizhi"]'
        self.click(submit_cfg_link)

    # 点击关闭 这里有两个电机关闭 后一个是入库成功之后的点击  使用enter键代替
    # def close_window_click1(self):
    #     # close_window_link = 'link_text=>"关闭"'
    #     close_window_link = 'xpath=>//*[@id="idlg_btn_1583312950920_0"]'
    #     self.click(close_window_link)
    #     self.sleep(1)
    #     close_window_link = 'xpath=>//*[@id="idlg_btn_1583313011406_0"]'
    #     self.click(close_window_link)
    #     self.sleep(1)

    # 点击查询所有设备参数
    def qry_all_dev_cfg_click(self):
        qry_all_dev_cfg_link = 'xpath=>//*[@id="btn_configqueryAll"]'
        self.click(qry_all_dev_cfg_link)
        self.sleep(1)

    # 点击获取在线的DRSU
    def get_online_drsu_click(self):
        get_online_acu_link = 'xpath=>//*[@id="btn_getAllDrsuInDRCx"]'
        self.click(get_online_acu_link)
        self.sleep(1)

    # 点击下载DRSU导入模板
    def download_drsu_import_temp_click(self):
        download_drsu_import_temp_link = 'xpath=>//*[@id="btn_downDrsuImportTemplate"]'
        self.click(download_drsu_import_temp_link)

    # 点击刷新
    def refresh_click(self):
        refresh_link = 'xpath=>//html/body/div/div/div[3]/div[2]/div/div[2]/div/div/div[2]/div[1]/div[2]/button'
        self.click(refresh_link)

    # 点击全屏
    def full_screen_click(self):
        full_screen_link = 'xpath=>/html/body/div/div/div[3]/div[2]/div/div[2]/div/div/div[2]/div[1]/div[2]/div/button'
        self.click(full_screen_link)

    # 点击全选
    def all_election_click(self):
        slect_all_click = 'xpath=//*[@id="tb_list"]/thead/tr/th[1]/div[1]/label/input'
        self.click(slect_all_click)

    # 获取DRSU数量
    def get_drsu_num(self):
        link = 'xpath=>/html/body/div/div/div[3]/div[2]/div/div[2]/div/div/div[2]/div[3]/div[1]/span[1]'
        txt = self.find_element(link).text
        a = [int(i) for i in txt if str.isdigit(i)]
        count = 0
        if a[0] == 1 and a[1] == 1 and a[2] == 0:
            for i in range(3, len(a)):
                count += (10 ** (len(a) - 1 - i)) * a[i]
        else:
            count = a[-1]
        logger.info('共找到%s个DRSU' % count)
        return count

    def choose_page_show_num(self, num='100'):
        show_num_link = 'xpath=>/html/body/div/div/div[3]/div[2]/div/div[2]/div/div/div[2]/div[3]/div[1]/span[2]/span/button'
        self.find_element(show_num_link).click()
        # self.wait(1)
        self.sleep(1)
        show_num_link_100 = 'xpath=>/html/body/div/div/div[3]/div[2]/div/div[2]/div/div/div[2]/div[3]/div[1]/span[2]/span/ul/li[4]/a'
        self.find_element(show_num_link_100).click()
        # self.wait(1)
        self.sleep(1)

    # 选择指定唯一标识设备
    # def device_select_click(self, drsu_id):
    #     for i in range(1, 10):
    #         choose_box_link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[2]'
    #         if self.find_element(choose_box_link_temp).text == str(drsu_id):
    #             choose_box_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[1]/label/input'
    #             self.click(choose_box_link)
    #             logger.info("点击指定标识设备成功 drsu_id:%s" % str(drsu_id))
    #             return i
    #     logger.info("点击指定标识设备失败 drsu_id:%s" % str(drsu_id))
    #     i = 0
    #     return i
    def device_select_click(self, drsu_id):
        num = self.get_drsu_num()
        if num > 10:
            self.choose_page_show_num()
        for i in range(1, 101):
            choose_box_link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[2]'
            try:
                record_drsu_id = self.find_element(choose_box_link_temp).text
                if record_drsu_id == str(drsu_id):
                    choose_box_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[1]/label/input'
                    self.click(choose_box_link)
                    logger.info("点击指定标识设备成功 drsu_id:%s" % str(drsu_id))
                    return i
            except ValueError:
                logger.info("点击指定标识设备失败 drsu_id:%s" % str(drsu_id))
                return 0

    # 获取drsu状态 参数index为device_select_click返回的值 目前暂时只需要获取状态
    def get_drsu_status(self, index):
        drsu_status_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(index) + ']/td[11]'
        drsu_status = self.find_element(drsu_status_link).text
        logger.info("指定标识设备状态为：%s" % drsu_status)
        if drsu_status == '激活':
            return True
        else:
            return False

    # 点击指定配置 点击之后跳转到DrsuDevMgrSpecCfgPage页面
    def spec_dev_cfg_click(self):
        spec_dev_cfg_link = 'xpath=>//*[@id="btn_config"]'
        self.click(spec_dev_cfg_link)
        time.sleep(1)

    # 是否弹出"以下DRSU设备不在线不可执行该操作"
    def is_prompt_visible_online(self):
        selector = '//*[@id="bActiveTagModelLabel"]'
        ret = self.is_visible(selector)  # 判断是否有"以下DRSU设备不在线不可执行该操作"弹窗
        logger.info("是否弹出以下DRSU未在线弹窗:%s" % ret)
        if ret == True:
            self.esc_click()
        return ret

    # 点击关闭 因设备未激活而弹出告警框的关闭 推荐使用basepage里面的esc
    def close_window_click2(self):
        # '//*[@id="bActiveTagModelLabel"]' 告警框的头部
        close_window_link = 'xpath=>//*[@id="guanbi1"]'
        self.click(close_window_link)

    # 点击指定查询
    def spec_dev_qry_click(self):
        spec_dev_cfg_link = 'xpath=>//*[@id="btn_configquery"]'
        self.click(spec_dev_cfg_link)
        time.sleep(1)

    # 点击导入
    def import_click(self):
        import_link = 'xpath=>//*[@id="btn_import"]'
        self.click(import_link)
        self.sleep(1)

    # 点击导出
    def export_click(self):
        import_link = 'xpath=>//*[@id="btn_export"]'
        self.click(import_link)
        self.sleep(1)

    # 点击新增
    def add_click(self):
        add_link = 'xpath=>//*[@id="btn_add"]'
        self.click(add_link)
        self.sleep(1)

    # 点击修改
    def mod_click(self):
        mod_link = 'xpath=>//*[@id="btn_edit"]'
        self.click(mod_link)
        self.sleep(1)

    # 点击删除
    def del_click(self):
        del_link = 'xpath=>//*[@id="btn_delete"]'
        self.click(del_link)

    # 询问 确定删除选定设备 0：确定 1 取消
    def sure_click(self, value):
        sure_link = 'xpath=>//*[@id="idlg_btn_158331self.sixty78348_' + str(value) + '\"]'
        self.click(sure_link)

    # 点击关闭 提示删除成功
    def close_window_click3(self):
        cancel_link = 'xpath=>//*[@id="idlg_btn_1583316447465_0"]'
        self.click(cancel_link)

    # # 点击取消 合并到sure_click里面了
    # def cancel_click(self):
    #     cancel_link = 'xpath=>//*[@id="idlg_btn_158331self.sixty78348_1"]'
    #     self.click(cancel_link)

    # 点击运行版本
    def version_qry_click(self):
        version_qry_link = 'xpath=>//*[@id="btn_versionquery"]'
        self.click(version_qry_link)

    # 获取状态上报的条数，查找底部“显示第 1 到第 3 条记录，总共 3 条记录 每页显示  条记录”这句话
    def get_the_report_num(self):
        link = 'xpath=>/html/body/div/div/div[3]/div[2]/div/div[2]/div/div/div[2]/div[3]/div[1]/span[1]'
        txt = self.find_element(link).text # txt='显示第 1 到第 3 条记录，总共 3 条记录 每页显示  条记录'
        a = [int(i) for i in txt if str.isdigit(i)] # 提取txt中的数字
        count = 0
        if a[0] == 1 and a[1] == 1 and a[2] == 0:
            for i in range(3, len(a)):
                count += (10 ** (len(a) - 1 - i)) * a[i]
        else:
            count = a[-1]  # 将最后一个数字赋值给count
        return count

    # 获取drc设备软件运行版本信息
    def get_version_info(self):
        try:
            version_info = self.find_element('xpath=>//*[@id="versionInfo"]').text
            return version_info
        except ValueError:
            logger.error('获取版本信息失败')
            return None

    # 点击查询所有设备参数：判断弹窗
    def qry_all_drsu(self, result=''):
        self.qry_all_dev_cfg_click()
        time.sleep(3)
        if self.info():  #
            if self.info_text() == result:
                logger.error('查询所有drsu参数失败，弹出提示符合预期')
                self.esc_click()
                return True
            logger.error('查询所有drsu参数失败，没有出现弹窗')
            self.get_windows_img()  # 截图
            self.esc_click()  # 消除弹窗
            return False
        return True

    # 点击配置所有设备参数：判断弹窗：填入参数：提交配置：判断结果
    def cfg_all_drsu(self, dict_drsu, result=''):
        self.all_drsu_parm_cfg_click()
        if not self.is_prompt_visible_cfg_all_drsu():
            self.info()  # 没有出现弹窗必定出现其他提示
            if self.info_text() == result:
                logger.error('配置所有drsu参数失败，弹出提示符合预期')
                self.esc_click()
                return True
            logger.error('配置所有drsu参数失败，没有出现弹窗')
            self.get_windows_img()  # 截图
            self.esc_click()  # 消除弹窗
            return False
        # 填入参数，所属drc不需要填写 这个try有点浪费
        try:
            # self.choose_data_report_cycle(dict_drsu['数据上报周期']) 突然间消失了
            self.choose_alarm_report_cycle(dict_drsu['告警上报周期'])
            # self.choose_long_term_valid(dict_drsu['是否长期有效']) # 填写 true or false 注意是小写
            if dict_drsu['是否长期有效'] == '是':
                self.choose_long_term_valid('true')
            else:
                self.choose_long_term_valid('false')
        except Exception as e:
            logger.error('配置所有drsu失败%s' % format(e))
            self.get_windows_img()
            return False
        self.submit_cfg_click()
        time.sleep(2)
        assert self.info()
        if self.info_text() == '配置成功':
            logger.info('配置所有drsu成功')
            self.enter_click()
            self.esc_click()
            self.sleep(1)
            self.enter_click()
            self.sleep(1)
            return True
        elif self.info_text() == result:
            logger.info('配置所有drsu失败，但是符合预期')
            self.esc_click()
            return True
        else:
            logger.error('配置所有drsu失败')
            self.get_windows_img()
            self.esc_click()
            return False

    def del_drsu_dev(self):
        self.del_click()
        self.info()
        if self.info_text() == '确定删除选定设备':
            self.enter_click()  # 点击enter再点击esc 弹出删除成功
            self.esc_click()
            self.sleep(1)
            self.info()
            if self.info_text() == '删除成功':
                self.esc_click()
                logger.info('acu删除成功')
                return True
        logger.error('drsu删除失败%s' % (self.info_text()))
        self.get_windows_img()
        self.esc_click()
        return False

    # 获取drc下所有在线的drsu
    def get_all_online_drsu(self, drc_id):
        self.choose_drc_id(drc_id)
        time.sleep(1)
        self.get_online_drsu_click()
        time.sleep(1)
        count = 0
        # 判断是否弹框，如果弹框，则判断提示语句是否为“没有在线的DRSU”（if分支），如果没有弹框则计算在线的DRSU数量（else分支）
        if self.info():
            if self.info_text() == "没有在线的DRSU":
                count = 0
        else:
            count = self.get_the_report_num()
        online_drsu = []
        if count == 0:
            logger.info('在线drsu数量为0')
        elif count == 1:
            link = 'xpath=>//*[@id="tb_list"]/tbody/tr/td[2]'
            drsu = self.find_element(link).text
            online_drsu.append(drsu)
            logger.info('在线drsu数量为1，drsu_id:%s' % drsu)
        else:
            for i in range(1, count+1):
                link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[2]'
                drsu = self.find_element(link).text
                online_drsu.append(drsu)
            logger.info('在线drsu数量为%u，drsu_id:%s' % (count, online_drsu))
        return online_drsu

    # 点击查询指定设备参数：判断弹窗
    def qry_spec_drsu(self, result=''):
        if self.info():
            if self.info_text() == result:
                logger.error('查询所有drsu失败，弹出提示符合预期')
                self.esc_click()
                return True
            logger.error('查询所有drsu失败，没有出现弹窗')
            self.get_windows_img()  # 截图
            self.esc_click()  # 消除弹窗
            return False
        return True

    # 点击配置指定设备参数，判断弹窗
    def cfg_spec_drsu(self, result=''):
        if self.info():
            if self.info_text() == result:
                logger.error('配置所有drsu失败，弹出提示符合预期')
                self.esc_click()
                return True
            logger.error('配置所有drsu失败，没有出现弹窗')
            self.get_windows_img()  # 截图
            self.esc_click()  # 消除弹窗
            return False
        return True
