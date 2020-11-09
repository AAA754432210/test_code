from api_test.base_page.homepage import HomePage
from common.Log import Logger
from selenium.webdriver.support.select import Select

logger = Logger("DrsuVerMgrUpdatePage").getlog()


class DrsuVerMgrUpdatePage(HomePage):

    # 填入DRSU唯一标识
    def input_drsu_id(self, drsu_id):
        input_drsu_id_link = 'xpath=>//*[@id="Term"]'
        self.type(input_drsu_id_link, str(drsu_id))

    # 点击查询
    def qry_click(self):
        qry_link = 'xpath=>//*[@id="btn_query"]'
        self.click(qry_link)

    # 选择指定唯一标识设备
    def dev_select_click(self, drsu_id):
        for i in range(1, 10):
            choose_box_link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[2]'
            try:
                record_drc_id = self.find_element(choose_box_link_temp).text
                if record_drc_id == str(drsu_id):
                    choose_box_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[1]/label/input'
                    self.click(choose_box_link)
                    logger.info("点击drsu系统唯一标识成功 drsu_id:%s" % str(drsu_id))
                    return i
            except ValueError:
                logger.info("点击drsu系统唯一标识失败 drsu_id:%s" % str(drsu_id))
                i = 0
                return i

    # 已经对指定drsu_id进行查询过之后 再点击指定drc 目前查询没有用有多个drsu的时候先用上面的
    def device_select_click_single(self, drsu_id='0'):
        choose_box_link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr/td[2]'
        try:
            if self.find_element(choose_box_link_temp).text == str(drsu_id) or drsu_id == '0':
                choose_box_link = 'xpath=>//*[@id="tb_list"]/tbody/tr/td[1]/label/input'
                self.click(choose_box_link)
                logger.info("点击指定标识drsu设备成功 drsu_id:%s" % str(drsu_id))
                return True
            else:
                logger.error("点击指定标识drsu设备失败 drsu_id:%s" % str(drsu_id))
                return False
        except:
            logger.error("指定标识drsu设备不存在 drsu_id:%s" % str(drsu_id))
            return False
    # # 选择DRC_ID
    # def choose_drc_id(self, drc_id):
    #     sel = self.find_element('xpath=>//*[@id="drcChoiceListId"]')
    #     self.wait(2)
    #     # 后续通过读取配置文件得到drc_id
    #     Select(sel).select_by_value('%s' % str(drc_id))

    def get_drsu_version_info(self, index=''):
        str_index = ''
        if index:
            str_index = '[' + str(index) + ']'
        version_link = 'xpath=>//*[@id="tb_list"]/tbody/tr/td[2]'

    # 点击返回DRSU版本管理
    def return_click(self):
        return_link = 'xpath=>//*[@id="btn_return"]'
        self.click(return_link)

    # 点击升级结果查看
    def show_updated_click(self):
        show_updated_link = 'xpath=>//*[@id="btn_showUpdated"]'
        self.click(show_updated_link)

    def is_prompt_visible_result(self):
        selector = '//*[@id="drsuRemoteUpdatedLabel"]'
        ret = self.is_visible(selector)
        logger.info("是否弹出DRSU软件版本升级结果查看弹窗%s" % ret)
        return ret

    # 序号：//*[@id="tb_Updatedlist"]/tbody/tr[1]/td[2] //*[@id="tb_Updatedlist"]/tbody/tr[1]/td[3]
    # 序号二 //*[@id="tb_Updatedlist"]/tbody/tr[2]/td[2]
    def get_result_parm(self):
        result_dict = {'序号': '', 'DRSU系统唯一标识': '', '当前使用软件版本号': '', '软件升级时间': '', '当前使用地图版本号': '',
                       '升级类型': '', '升级版本号': '', '升级地图版本号': '', 'ulTransld': '', '升级结果代码': '', '升级结果描述': ''}
        return False

    # 点击远程升级
    def remote_update_click(self):
        remote_update_link = 'xpath=>//*[@id="btn_remoteupdate"]'
        self.click(remote_update_link)

    # 点击升级全部
    def all_update_click(self):
        all_update_link = 'xpath=>//*[@id="btn_Allupdate"]'
        self.click(all_update_link)
        self.sleep(0.5)

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

    # 是否存在输入弹窗
    # def is_exist_prompt(self):
    #     prompt_head_link = 'xpath=>//*[@id="drsuAddNewVersionInfoModalLabel"]'
    #     try:
    #         self.find_element(prompt_head_link)
    #         logger.info("弹出新增版本入库设置弹窗")
    #         return True
    #     except Exception as e:
    #         logger.info("未弹出新增版本入库设置弹窗%s" % format(e))
    #         return False
    def is_prompt_visible_update(self):
        selector = '//*[@id="drsuRemoteUpdateModalLabel"]'
        ret = self.is_visible(selector)
        logger.info("是否弹出DRSU软件版本远程升级弹窗%s" % ret)
        return ret

    # 输入版本记录编号
    def input_version_record_no(self, version_no):
        input_version_record_no_link = 'xpath=>//*[@id="first-name"]'
        self.type(input_version_record_no_link, version_no)

    # 输入版本名称
    def input_version_name(self, version_name):
        input_version_name_link = 'xpath=>//*[@id="last-name"]'
        self.type(input_version_name_link, version_name)

    # 点击查询
    def qry_click1(self):
        qry_link = 'xpath=>//*[@id="demo-form2"]/div/div[3]/button'
        self.click(qry_link)

    # 选择是否强制升级 现在默认都是不强制升级
    def check_is_force(self):
        check_is_force_link = 'xpath=>//*[@id="check_isForce"]'
        self.click(check_is_force_link)

    # 选择指定唯一标识设备 升级版本
    def version_select_click(self, version_id):
        for i in range(1, 10):
            choose_box_link_temp = 'xpath=>//*[@id="tb_versionServerslist"]/tbody/tr[' + str(i) + ']/td[2]'
            try:
                record_version_id = self.find_element(choose_box_link_temp).text
                if record_version_id == str(version_id):
                    choose_box_link = 'xpath=>//*[@id="tb_versionServerslist"]/tbody/tr[' + str(i) + ']/td[1]/label/input'
                    self.click(choose_box_link)
                    logger.info("点击版本记录编号成功 version_id:%s" % str(version_id))
                    return i
            except ValueError:
                logger.info("点击版本记录编号失败 version_id:%s" % str(version_id))
                i = 0
                return i

    # 选择版本记录名称 升级版本
    def version_select_click_1(self, version_name):
        for i in range(1, 12):
            choose_box_link_temp = 'xpath=>//*[@id="tb_versionServerslist"]/tbody/tr[' + str(i) + ']/td[3]'
            try:
                record_version_id = self.find_element(choose_box_link_temp).text
                if record_version_id == str(version_name):
                    choose_box_link = 'xpath=>//*[@id="tb_versionServerslist"]/tbody/tr[' + str(
                        i) + ']/td[1]/label/input'
                    self.click(choose_box_link)
                    logger.info("点击版本名称成功 version_name:%s" % str(version_name))
                    return i
            except ValueError:
                logger.info("点击版本名称失败 version_name:%s" % str(version_name))
                return 0

    # 选择版本记录名称 只剩下一个
    def version_select_click_2(self, version_name):
        choose_box_link_temp = 'xpath=>//*[@id="tb_versionServerslist"]/tbody/tr/td[3]'
        try:
            record_version_id = self.find_element(choose_box_link_temp).text
            if record_version_id == str(version_name):
                choose_box_link = 'xpath=>//*[@id="tb_versionServerslist"]/tbody/tr/td[1]/label/input'
                self.click(choose_box_link)
                logger.info("点击版本名称成功 version_name:%s" % str(version_name))
                return True
        except ValueError:
            logger.info("点击版本名称失败 version_name:%s" % str(version_name))
            return False

    # 获取状态上报的条数
    def get_the_report_num(self):
        link = 'xpath=>/html/body/div/div/div[3]/div[2]/div/div[2]/div/div/div[2]/div[3]/div[1]/span[1]'
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

    def choose_show_info_evey_page(self):
        # link_txt = '/html/body/div/div/div[3]/div[2]/div/div[2]/div/div/div[2]/div[3]/div[1]/span[2]/span/button/span[1]'
        # print('每页显示%s项信息' % self.find_element(link_txt).text)
        link = 'xpath=>/html/body/div/div/div[3]/div[2]/div/div[2]/div/div/div[2]/div[3]/div[1]/span[2]/span/button'
        link1 = 'xpath=>/html/body/div/div/div[3]/div[2]/div/div[2]/div/div/div[2]/div[3]/div[1]/span[2]/span/ul/li[4]'
        self.click(link)
        self.sleep(0.2)
        self.click(link1)
        self.sleep(0.2)
        logger.info('每页显示%s项信息' % self.find_element(link_txt).text)

    # 点击关闭
    def close_window_click(self):
        close_window_link = 'xpath=>//*[@id="drsuRemoteUpdateModal"]/div/div/div[3]/button[1]'
        self.click(close_window_link)

    # 点击提交并升级指定版本
    def version_update_click(self):
        version_upload_link = 'xpath=>//*[@id="drsuUpdate"]'
        self.click(version_upload_link)

    # 点击确定 好像没啥用
    def sure_click(self):
        sure_link = 'xpath=>//*[@id="idlg_btn_1583490473287_0"]'
        self.click(sure_link)

    # 选择drsu
    def choose_drsu_(self, drsu_id):
        self.input_drsu_id(drsu_id)
        self.qry_click()
        return self.device_select_click_single()

    # 选择drsu 上面函数无法使用
    def choose_drsu(self, drsu_id):
        count = self.get_the_report_num()
        if count == 0:
            self.get_windows_img()
            logger.error('该drc下不存在在线drsu设备')
            return False
        elif count == 1:
            return self.device_select_click_single(drsu_id=drsu_id)
        else:
            return self.dev_select_click(drsu_id)

    # 单个升级和全部升级公用函数 查询目前没有用 flag是否只有一个版本
    def drsu_update_common(self, version_dict, flag=False):
        # self.input_version_record_no(version_dict['版本记录编号'])
        # self.input_version_record_no(version_dict['版本名称'])
        if version_dict['是否强制升级'] == '是':
            self.check_is_force()
        # self.version_select_click(version_dict['版本记录编号'])
        if flag:
            if not self.version_select_click_2(version_dict['版本名称']):
                return False
        else:
            if self.version_select_click_1(version_dict['版本名称']) == 0:
                return False
        self.version_update_click()
        self.sleep(1)
        self.info()
        if self.info_text() == '发送升级请求成功':
            logger.info('drsu升级请求发送成功')
            self.enter_click()
            return True
        else:
            logger.error('drsu升级请求发送失败')
            self.get_windows_img()
            self.esc_click()
            return False

    def single_drsu_update(self, drsu_id, version_dict):
        if not self.choose_drsu(drsu_id):
            return False
        self.remote_update_click()
        assert self.is_prompt_visible_update()
        return self.drsu_update_common(version_dict)

    def all_drsu_update(self, version_dict):
        self.all_update_click()
        assert self.is_prompt_visible_update()
        return self.drsu_update_common(version_dict)

    def drsu_update(self, version_dict, drsu_id):
        if not drsu_id:
            return self.all_drsu_update(version_dict)
        else:
            return self.single_drsu_update(drsu_id, version_dict)

    # 查询drsu升级结果 没有办法直接获取结果 利用读取的方法进行获取
    def qry_spec_drsu_update_result(self, drsu_id):
        count = self.get_the_report_num()
        if count == 0:
            logger.error('该drc下不存在在线drsu设备')
            return None
        elif count == 1:
            drsu_id_link = 'xpath=>//*[@id="tb_list"]/tbody/tr/td[2]'
            try:
                record_drsu_id = self.find_element(drsu_id_link).text
                if record_drsu_id == str(drsu_id):
                    version_link = 'xpath=>//*[@id="tb_list"]/tbody/tr/td[3]'
                    version = self.find_element(version_link).text
                    logger.info("drsu:%s的当前版本号为:%s" % (str(drsu_id), str(version)))
                    return version
            except ValueError:
                logger.error("查询指定drsu：%s版本号失败" % str(drsu_id))
                return None
        else:
            for i in range(1, count + 1):
                drsu_id_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[2]'
                try:
                    record_drsu_id = self.find_element(drsu_id_link).text
                    if record_drsu_id == str(drsu_id):
                        version_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[3]'
                        version = self.find_element(version_link).text
                        logger.info("drsu:%s的当前版本号为:%s" % (str(drsu_id), str(version)))
                        return version
                except ValueError:
                    logger.error("查询指定drsu：%s版本号失败" % str(drsu_id))
                    return None

    # 查询drsu升级结果 没有办法直接获取结果 利用读取的方法进行获取
    def qry_all_drsu_update_result(self, version_name):
        count = self.get_the_report_num()
        if count == 0:
            logger.error('该drc下不存在在线drsu设备')
            return False
        elif count == 1:
            drsu_id_link = 'xpath=>//*[@id="tb_list"]/tbody/tr/td[2]'
            record_drsu_id = self.find_element(drsu_id_link).text
            version_link = 'xpath=>//*[@id="tb_list"]/tbody/tr/td[3]'
            version = self.find_element(version_link).text
            if version == version_name:
                logger.info("只有一个在线drsu:%s，当前版本号与预期结果一致为:%s" % (str(record_drsu_id), str(version)))
                self.get_windows_img()
                return True
            else:
                logger.error("只有一个在线drsu:%s，当前版本号与预期结果不一致，实际版本:%s， 预期版本：%s" % (record_drsu_id, version, version_name))
                return False
        else:
            if count > 10:
                self.choose_show_info_evey_page()
            for i in range(1, count + 1):
                drsu_id_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[2]'
                record_drsu_id = self.find_element(drsu_id_link).text
                version_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[3]'
                version = self.find_element(version_link).text
                if version != version_name:
                    logger.error("drsu:%s，当前版本号与预期结果不一致，实际版本:%s， 预期版本：%s" % (record_drsu_id, version, version_name))
                    self.get_windows_img()
                    return False
            logger.info('所有drsu的版本均与预期版本一致：%s' % version_name)
            return True

    def qry_drsu_update_result(self, version_name, drsu_id):
        if drsu_id:
            qry_version_name = self.qry_spec_drsu_update_result(drsu_id)
            if version_name.strip('.gz') == qry_version_name:
                logger.info('指定drsu：%s版本号与预期结果一致：%s' % (drsu_id, version_name))
                return True
            else:
                logger.error('指定drsu：%s版本号：%s与预期结果：%s不一致' % (drsu_id, qry_version_name, version_name))
                return False
        else:
            return self.qry_all_drsu_update_result(version_name)

