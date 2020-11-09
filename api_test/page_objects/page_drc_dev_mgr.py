from api_test.base_page.homepage import HomePage
from common.Log import Logger
from selenium.webdriver.support.select import Select

logger = Logger("DrcDevMgrPage").getlog()


class DrcDevMgrPage(HomePage):

    # 填写DRC_ID
    def input_drc_id(self, drc_id):
        input_drc_id_link = 'xpath=>//*[@id="Term"]'
        self.type(input_drc_id_link, str(drc_id))

    # 在线状态选择 'null'全部；'0'上线；'1'下线，默认为全部
    def choose_status(self, value):
        sel = self.find_element('xpath=>//*[@id="LocatfffionDesc"]')
        self.wait(2)
        Select(sel).select_by_value('%s' % str(value))

    # 点击查询按钮
    def drc_qry_click(self):
        drc_qry_link = 'xpath=>//*[@id="btn_query"]'
        self.click(drc_qry_link)
        self.sleep(1)

    # 点击下载DRC导入模板
    def drc_download_tmp_click(self):
        drc_download_tmp_link = 'xpath=>//*[@id="btn_btn_downDrcTemplate"]'
        self.click(drc_download_tmp_link)

    # 点击可配置参数默认值
    def drc_qry_default_config_click(self):
        link = 'xpath=>//*[@id="btn_queryAllConfig"]'
        self.click(link)

    # 是否弹出默认可配置参数弹窗
    def is_prompt_visible_default_cfg(self):
        selector = '//*[@id="saveemployeeModalLabe"]'
        ret = self.is_visible(selector)
        logger.info("是否弹出人员新增弹窗%s" % ret)
        return ret

    # 获取可配置参数默认值
    def drc_qry_default_config(self):
        # //*[@id="queryAllConfigform"]/div[1]/div[1]
        # //*[@id="queryAllConfigform"]/div[1]/div[2]
        # //*[@id="queryAllConfigform"]/div[2]/div[2]
        drc_value = []
        acu_value = []
        drsu_value = []
        drc_key = ['DRC状态上报周期', '融合算法配置', 'ACU存活检测次数', 'CRM接口消息完整性',
                   'DRSU接口消息完整性', 'ACU接口消息完整性', 'CRM接口消息加密', 'DRSU接口消息加密',
                   'ACU接口消息加密']
        acu_key = ['车辆上报周期', '告警上报周期', '状态上报周期']
        drsu_key = ['数据上报周期', '告警上报周期', '识别算法']
        for i in range(2, 11):
            link = 'xpath=>//*[@id="queryAllConfigform"]/div[1]/div[' + str(i) + ']'
            drc_value.append(self.find_element(link).text)
        for i in range(2, 5):
            link = 'xpath=>//*[@id="queryAllConfigform"]/div[2]/div[' + str(i) + ']'
            acu_value.append(self.find_element(link).text)
        for i in range(2, 5):
            link = 'xpath=>//*[@id="queryAllConfigform"]/div[3]/div[' + str(i) + ']'
            drsu_value.append(self.find_element(link).text)
        dict_drc = dict(zip(drc_key, drc_value))
        dict_acu = dict(zip(acu_key, acu_value))
        dict_drsu = dict(zip(drsu_key, drsu_value))
        return dict_drc, dict_acu, dict_drsu

    # 点击刷新
    def refresh_click(self):
        refresh_link = 'xpath=>/html/body/div/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[1]/div[2]/button'
        self.click(refresh_link)

    # 点击全屏
    def full_screen_click(self):
        full_screen_link = 'xpath=>/html/body/div/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[1]/div[' \
                           '2]/div/button '
        self.click(full_screen_link)

    # 选择指定唯一标识设备
    def device_select_click(self, dev_id):
        for i in range(1, 12):
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

    # 已经对指定drc_id进行查询过之后 再点击指定drc
    def device_select_click_single(self, dev_id='0'):
        choose_box_link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr/td[2]'
        try:
            if self.find_element(choose_box_link_temp).text == str(dev_id) or dev_id == '0':
                choose_box_link = 'xpath=>//*[@id="tb_list"]/tbody/tr/td[1]/label/input'
                self.click(choose_box_link)
                logger.info("点击指定标识drc设备成功 dev_id:%s" % str(dev_id))
                return True
            else:
                self.get_windows_img()
                logger.error("点击指定标识drc设备失败 dev_id:%s" % str(dev_id))
                return False
        except:
            self.get_windows_img()
            logger.error("指定标识drc设备不存在 dev_id:%s" % str(dev_id))
            return False

    # 如果之前已经指定drc_id这里的index就填写0
    def get_drc_status(self, index='0'):
        if str(index) == '0':
            index_str = ''
        else:
            index_str = '[' + str(index) + ']'
            # 未指定drc'//*[@id="tb_list"]/tbody/tr[1]/td[13]'
            # 指定drc '//*[@id="tb_list"]/tbody/tr/td[13]'
        drc_status_link = 'xpath=>//*[@id="tb_list"]/tbody/tr' + index_str + '/td[13]'
        drc_status = self.find_element(drc_status_link).text
        logger.info("指定drc状态为:%s" % drc_status)
        if drc_status == '已激活':
            return True
        else:
            return False

    # 如果之前已经指定drc_id这里的index1就填写0,index1 为指定drc的返回值，index2为想要获取数据的索引值
    # '//*[@id="tb_list"]/tbody/tr/td[2]' '//*[@id="tb_list"]/tbody/tr[1]/td[2]'
    # 2。DRC系统唯一标识 3。设备名称 4.设备型号 5.操作系统版本 6.处理器颗数 7.处理器型号 8.单颗处理器核心数 9.处理器基本频率
    # 10.内存容量 11.网卡规格 12。pcie扩张槽个数 13。设备激活状态
    def get_drc_info(self, index1, index2):
        if index1 == 0:
            index_str = ''
        else:
            index_str = '[' + str(index1) + ']'
            # 未指定drc'//*[@id="tb_list"]/tbody/tr[1]/td[13]'
            # 指定drc '//*[@id="tb_list"]/tbody/tr/td[13]'
        drc_status_link = 'xpath=>//*[@id="tb_list"]/tbody/tr' + index_str + '/td[13]'
        drc_status = self.find_element(drc_status_link).text
        logger.info("指定drc状态为:%s" % drc_status)
        if drc_status == '激活':
            return True
        else:
            return False

    # 点击指定配置
    def spec_dev_cfg_click(self):
        spec_dev_cfg_link = 'xpath=>//*[@id="btn_config"]'
        self.click(spec_dev_cfg_link)

    # 点击指定查询
    def spec_dev_qry_click(self):
        spec_dev_cfg_link = 'xpath=>//*[@id="btn_configquery"]'
        self.click(spec_dev_cfg_link)

    # 点击导入
    def import_click(self):
        import_link = 'xpath=>//*[@id="btn_import"]'
        self.click(import_link)

    # 点击导出
    def export_click(self):
        export_link = 'xpath=>//*[@id="btn_export"]'
        self.click(export_link)

    # 点击新增
    def add_click(self):
        add_link = 'xpath=>//*[@id="btn_add"]'
        self.click(add_link)
        self.sleep(0.2)

    # 点击修改
    def mod_click(self):
        mod_link = 'xpath=>//*[@id="btn_edit"]'
        self.click(mod_link)

    # 点击删除
    def del_click(self):
        del_link = 'xpath=>//*[@id="btn_delete"]'
        self.click(del_link)
        self.sleep(2)

    # 点击确定
    def sure_click(self):
        sure_link = 'xpath=>//*[@id="idlg_btn_1583306909870_0"]'
        self.click(sure_link)

    # 点击取消
    def cancel_click(self):
        del_link = 'xpath=>//*[@id="idlg_btn_1583306909870_1"]'
        self.click(del_link)

    # 点击关闭 先点击确认 再点击关闭之后才能删除成功
    def close_window_click(self):
        close_window_link = 'xpath=>//*[@id="idlg_btn_1583307077224_0"]'
        self.click(close_window_link)

    # 点击运行版本
    def version_qry_click(self):
        version_qry_link = 'xpath=>//*[@id="btn_versionquery"]'
        self.click(version_qry_link)

    # 获取drc设备软件运行版本信息
    def get_version_info(self):
        return self.find_element('xpath=>//*[@id="versionInfo"]').text

    # 点击可配置参数默认值
    def def_cfg_para_click(self):
        def_cfg_para_link = 'xpath=>//*[@id="btn_queryAllConfig"]'
        self.click(def_cfg_para_link)

    # 指定drc 指定步骤为 填写系统唯一标识->点击查询->勾选drc前的复选框 flag 是否要对激活进行判断 flag=True判断
    def drc_spec_click(self, drc_id, flag=True):
        # 第一种选定drc方法
        self.input_drc_id(str(drc_id))
        self.drc_qry_click()
        self.sleep(1)
        if not self.device_select_click_single(str(drc_id)):
            logger.error('drc指定失败')
            return False
        # 第二种选定drc方法
        # page.device_select_click('8200')
        if flag and (not self.get_drc_status('0')):
            logger.error('指定drc未激活')
            return False
        return True

    def del_drc_dev(self):
        self.del_click()
        self.info()
        if self.info_text() == '确定删除选定设备':
            self.enter_click() # 点击enter再点击esc 弹出删除成功
            self.esc_click()
            self.sleep(1)
            self.info()
            if self.info_text() == '删除成功':
                self.esc_click()
                logger.info('drc删除成功')
                return True
        logger.error('drc删除失败%s' % (self.info_text()))
        self.get_windows_img()
        self.esc_click()
        return False