from selenium.webdriver.support.select import Select
from api_test.base_page.homepage import HomePage
from common.Log import Logger

logger = Logger("AcuDevMgrPage").getlog()


class AcuDevMgrPage(HomePage):

    # 选择DRC_ID
    def choose_drc_id(self, drc_id):
        sel = self.find_element('xpath=>//*[@id="drcChoiceListId"]')
        # 后续通过读取配置文件得到drc_id
        try:
            Select(sel).select_by_value(str(drc_id))
            logger.info('Choose drc id \' %s \'successful' % drc_id)
        except Exception as e:
            logger.error('Choose drc id failed because %s' % format(e))

    # 在线状态选择 默认全部；'0'未激活；'1'激活
    def choose_status(self, value):
        sel = self.find_element('xpath=>//*[@id="zhuangtai"]')
        Select(sel).select_by_value(str(value))

    # 点击配置所有acu参数
    def all_acu_parm_cfg_click(self):
        all_acu_parm_cfg_link = 'xpath=>//*[@id="btn_allAcuInDRCx"]'
        self.click(all_acu_parm_cfg_link)

    # # 是否存在输入弹窗
    # def is_exist_prompt(self):
    #     try:
    #         self.find_element('xpath=>//*[@id="configAllAcrOfDrcidModalLabel"]')
    #         logger.info("弹出配置所有的ACU弹窗")
    #         return True
    #     except Exception as e:
    #         logger.info("未弹出配置所有的ACU弹窗%s" % format(e))
    #         return False

    # 是否存在输入弹窗
    def is_prompt_visible_cfg_all_acu(self):
        selector = '//*[@id="configAllAcrOfDrcidModalLabel"]'
        ret = self.is_visible(selector)
        logger.info("是否弹出配置所有的ACU弹窗%s" % ret)
        return ret

    # 选择状态上报周期 100 200 500 1000
    def choose_status_report_unit(self, value):
        sel = self.find_element('xpath=>//*[@id="ulPeriodOfSatusRpt"]')
        Select(sel).select_by_value(str(value))

    # 选择告警上报周期 10 30 self.sixty
    def choose_alarm_report_unit(self, value):
        sel = self.find_element('xpath=>//*[@id="ulPeriodOfAlarmRpt"]')
        Select(sel).select_by_value(str(value))

    # 选择车辆信息上报周期 100 200 500 1000
    def choose_car_info_report_unit(self, value):
        sel = self.find_element('xpath=>//*[@id="ulPeriodofInfo"]')
        Select(sel).select_by_value(str(value))

    # 选择是否长期有效 默认为是 'true': 是 'false'：否
    def choose_long_term_valid(self, value):
        sel = self.find_element('xpath=>//*[@id="longTermValid"]')
        Select(sel).select_by_value(str(value))

    # 点击关闭
    def close_window_click(self):
        close_window_link = 'xpath=>//*[@id="configAllAcrOfDrcidModal"]/div/div/div[3]/button[1]'
        self.click(close_window_link)

    # 点击提交配置
    def submit_cfg_click(self):
        submit_cfg_link = 'xpath=>//*[@id="btn_excuteAcuConfig"]'
        self.click(submit_cfg_link)

    # 点击关闭
    def close_window_click2(self):
        close_window_link = 'xpath=>//*[@id="idlg_btn_1582943689222_0"]'
        self.click(close_window_link)

    # 点击查询所有acu参数
    def all_acu_parm_qry_click(self):
        all_acu_parm_qry_link = 'xpath=>//*[@id="btn_configqueryAll"]'
        self.click(all_acu_parm_qry_link)

    # 点击获取已激活的ACU
    def get_online_acu_click(self):
        get_online_acu_link = 'xpath=>//*[@id="btn_getOnlineAcu"]'
        self.click(get_online_acu_link)

    # 点击刷新
    def refresh_click(self):
        refresh_link = 'xpath=>/html/body/div[1]/div[1]/div[3]/div[2]/div/div[2]/div/div/div[2]/div[1]/div[2]/button'
        # refresh_link = 'link_text=>刷新'
        self.click(refresh_link)

    # 点击全屏
    def full_screen_click(self):
        full_screen_link = 'xpath=>/html/body/div[1]/div[1]/div[3]/div[2]/div/div[2]/div/div/div[2]/div[1]/div[' \
                           '2]/div/button '
        self.click(full_screen_link)

    # 点击全选
    def all_election_click(self):
        select_all_click = 'xpath=>//*[@id="tb_list"]/thead/tr/th[1]/div[1]/label/input'
        self.click(select_all_click)

    # 选择指定唯一标识设备 在设备少的情况下推荐使用该方式选择drc_id
    # def device_select_click(self, dev_id):
    #     for i in range(1, 10):
    #         # '//*[@id="tb_list"]/tbody/tr/td[1]/label/input'
    #         choose_box_link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[2]'
    #         if self.find_element(choose_box_link_temp).text == str(dev_id):
    #             choose_box_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[1]/label/input'
    #             self.click(choose_box_link)
    #             logger.info("点击指定标识设备成功 dev_id:%s" % str(dev_id))
    #             return i
    #         else:
    #             pass
    #     logger.info("点击指定标识设备失败 dev_id:%s" % str(dev_id))
    #     i = 0
    #     return i
    # 选择指定唯一标识设备 升级版本
    def device_select_click(self, dev_id):
        for i in range(1, 12):
            choose_box_link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[2]'
            try:
                record_dev_id = self.find_element(choose_box_link_temp).text
                if record_dev_id == str(dev_id):
                    choose_box_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[1]/label/input'
                    self.click(choose_box_link)
                    logger.info("点击指定标识设备成功 dev_id:%s" % str(dev_id))
                    return i
            except ValueError:
                logger.info("点击指定标识设备失败 dev_id:%s" % str(dev_id))
                i = 0
                return i

    # 获取acu状态
    def get_acu_status(self, index):
        acu_status_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(index) + ']/td[5]'
        acu_status = self.find_element(acu_status_link).text
        logger.info("指定acu状态为:%s" % acu_status)
        if acu_status == '激活':
            return True
        else:
            return False

    # index1 行程日志 '//*[@id="tb_list"]/tbody/tr[1]/td[13]/a[2]/button'
    # index2 车辆信息 '//*[@id="tb_list"]/tbody/tr[2]/td[13]/a[1]/button'
    def car_info_click(self, index):
        car_info_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(index) + ']/td[13]/a[1]/button'
        self.click(car_info_link)

    def driving_log_click(self, index):
        driving_log_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(index) + ']/td[13]/a[2]/button'
        self.click(driving_log_link)

    # # 是否存在告警弹窗，未选定drcid 推荐使用basepage里面的info
    # def is_exist_alert(self):
    #     try:
    #         alert = self.find_element('xpath=>/html/body/div[2]/div/div[2]/div/h3')
    #         logger.info("弹出提示：%s" % alert.text)
    #         return True
    #     except Exception as e:
    #         logger.error("未弹出提示%s" % format(e))
    #         return False
    #
    # # 是否存在告警弹窗acu未激活 推荐使用basepage里面的info
    # def is_exist_alert1(self):
    #     try:
    #         alert = self.find_element('//*[@id="bActiveTagModelLabel"]')
    #         logger.error("弹出提示：%s" % alert.text)
    #         return True
    #     except Exception as e:
    #         logger.info("未弹出提示%s" % format(e))
    #         return False

    # 点击指定配置 点击之后跳转到AcuDevMgrSpecCfgPage页面
    def spec_dev_cfg_click(self):
        spec_dev_cfg_link = 'xpath=>//*[@id="btn_config"]'
        self.click(spec_dev_cfg_link)

    # 点击指定查询 点击之后跳转到AcuDevMgrSpecQryPage页面
    def spec_dev_qry_click(self):
        spec_dev_cfg_link = 'xpath=>//*[@id="btn_configquery"]'
        self.click(spec_dev_cfg_link)

    # 点击导入
    def import_click(self):
        import_link = 'xpath=>//*[@id="btn_import"]'
        self.click(import_link)

    # 点击新增 点击之后跳转到AcuDevMgrAddPage页面
    def add_click(self):
        add_link = 'xpath=>//*[@id="btn_add"]'
        self.click(add_link)

    # 点击修改 点击之后跳转到AcuDevMgrAddPage页面
    def mod_click(self):
        mod_link = 'xpath=>//*[@id="btn_edit"]'
        self.click(mod_link)

    # 点击删除
    def del_click(self):
        del_link = 'xpath=>//*[@id="btn_delete"]'
        self.click(del_link)

    # 点击运行版本
    def version_qry_click(self):
        version_qry_link = 'xpath=>//*[@id="btn_versionquery"]'
        self.click(version_qry_link)

    # 获取drc设备软件运行版本信息
    def get_version_info(self):
        try:
            version_info = self.find_element('xpath=>//*[@id="versionInfo"]').text
            return version_info
        except ValueError:
            logger.error('获取版本信息失败')
            return None

    # dict_acu = {'状态上报周期': '1000', '告警上报周期': '10', '车辆信息上报周期': '1000','是否长期有效': '是'}
    def cfg_all_acu(self, dict_acu):
        self.all_acu_parm_cfg_click()
        if not self.is_prompt_visible_cfg_all_acu():
            logger.info('配置所有acu失败，没有出现弹窗')
            self.info() # 没有出现弹窗必定出现提示
            self.get_windows_img() # 截图
            self.esc_click() # 消除弹窗
            return False
        try:
            self.choose_status_report_unit(dict_acu['状态上报周期'])
            self.choose_alarm_report_unit(dict_acu['告警上报周期'])
            self.choose_car_info_report_unit(dict_acu['车辆信息上报周期'])
            if dict_acu['是否长期有效'] == '是':
                self.choose_long_term_valid('true')
            self.submit_cfg_click()
            self.info()
        except Exception as e:
            logger.error('配置所有acu失败%s' % format(e))
            self.get_windows_img()
            return False
        if self.info_text() == '配置成功':
            logger.info('配置所有acu成功')
            ret = True
        else:
            logger.error('配置所有acu失败')
            self.get_windows_img()
            ret = False
        self.enter_click()
        self.esc_click()
        self.enter_click()
        self.sleep(1)
        return ret

    def del_acu_dev(self):
        self.del_click()
        self.info()
        if self.info_text() == '确定删除选定设备':
            self.enter_click() # 点击enter再点击esc 弹出删除成功
            self.esc_click()
            self.sleep(1)
            self.info()
            if self.info_text() == '删除成功':
                self.esc_click()
                logger.info('acu删除成功')
                return True
        logger.error('acu删除失败%s' % (self.info_text()))
        self.get_windows_img()
        self.esc_click()
        return False