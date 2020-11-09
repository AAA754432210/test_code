from api_test.base_page.homepage import HomePage
from common.Log import Logger
from selenium.webdriver.support.select import Select

logger = Logger("DrsuPowerMgrPage").getlog()
drsu_parm_tup = ('子设备数量', '状态', '风扇开启温度阀值', '风扇关闭温度阀值', '开箱告警延迟开启时间',
                 '机箱内温度值', '机箱外温度值', '操作')
drsu_parm_dict = {'DRSU唯一标识': '2', '子设备数量': '3', '状态': '4', '风扇开启温度阈值': '5', '风扇关闭温度阈值': '6', '开箱告警延迟开启时间': '7',
                  '机箱内温度值': '8', '机箱外温度值': '9', '操作': '10'}


class DrsuPowerMgrPage(HomePage):

    # 选择DRC_ID
    def choose_drc_id(self, drc_id):
        sel = self.find_element('xpath=>//*[@id="drcChoiceListId"]')
        self.wait(2)
        # 后续通过读取配置文件得到drc_id
        Select(sel).select_by_value('%s' % str(drc_id))

    # 直接输入‘在线’或者‘不在线’
    def choose_status(self, value):
        sel = self.find_element('xpath=>//*[@id="onlineornot"]')
        self.wait(2)
        Select(sel).select_by_visible_text('%s' % str(value))

    # 点击配置所有DRSU电源开关
    def all_drsu_power_cfg_click(self):
        all_drsu_power_cfg_link = 'xpath=>//*[@id="btn_allDrsuInDRCx"]'
        self.click(all_drsu_power_cfg_link)

    # 判断按钮是否可以点击
    def all_drsu_power_cfg_click_isvisble(self):
        all_drsu_power_cfg_link = '//*[@id="btn_allDrsuInDRCx"]'
        return self.is_visible(all_drsu_power_cfg_link)

    # 是否存在DRSU电源开关弹窗
    def is_prompt_visible_power(self):
        selector = '//*[@id="configdianyuankaiguanModalLabel"]'
        ret = self.is_visible(selector)
        logger.info("是否弹出DRSU电源开关弹窗%s" % ret)
        return ret

    # 选择电源开关配置模式 0自动1手动 配置所有DRSU电源开关
    def choose_power_cfg_mode(self, value):
        sel = self.find_element('xpath=>//*[@id="ulPeriodOfSatusRpt1"]')
        self.wait(1)
        Select(sel).select_by_value('%s' % str(value))

    # 填写自动开启DRSU时间 时间格式 12:00
    def input_auto_drsu_start_time(self, start_time):
        drsu_start_time_link = 'xpath=>//*[@id="aucStartTime"]'
        self.type(drsu_start_time_link, str(start_time))

    # 填写自动关闭DRSU时间 时间格式 12:00
    def input_auto_drsu_stop_time(self, stop_time):
        drsu_stop_time_link = 'xpath=>//*[@id="aucEndTime"]'
        self.type(drsu_stop_time_link, str(stop_time))

    # 选择电源开关 2：ON 4：OFF
    def choose_power_type(self, value):
        sel = self.find_element('xpath=>//*[@id="ePowerType"]')
        self.wait(1)
        if value.lower() == 'on':
            Select(sel).select_by_value('2')
        else:
            Select(sel).select_by_value('4')

    # 点击关闭 修改
    def close_window_click(self):
        close_window_link = 'link_text=>关闭'
        self.click(close_window_link)

    def close_window_click_(self):
        close_window_link = 'xpath=>//*[@id="configdianyuankaiguan"]/div/div/div[2]/div/button[1]'
        self.click(close_window_link)

    # 点击执行配置所有DRSU电源开关
    def submit_all_drsu_power_cfg_click(self):
        submit_all_drsu_power_cfg_link = 'xpath=>//*[@id="btn_dianyuankaiguan"]'
        self.click(submit_all_drsu_power_cfg_link)

    # 点击配置所有DRSU风扇参数
    def all_drsu_fan_cfg_click(self):
        all_drsu_fan_cfg_link = 'xpath=>//*[@id="btn_configqueryAll"]'
        self.click(all_drsu_fan_cfg_link)

    # 是否存在配置所有DRSU风扇参数弹窗
    # def is_exist_prompt2(self):
    #     selector = '//*[@id="configfengshanModalLabel"]'
    #     ret = self.is_visible(selector)
    #     logger.info("是否弹出配置所有DRSU风扇参数弹窗：%s" % ret)
    #     return ret
    def is_prompt_visible_fans(self):
        selector = '//*[@id="configfengshanModalLabel"]'
        ret = self.is_visible(selector)
        logger.info("是否弹出配置所有DRSU风扇参数弹窗%s" % ret)
        return ret

    # 填写风扇开启温度阀值
    def input_fan_start_temp(self, temp):
        input_fan_start_temp_link = 'xpath=>//*[@id="ulFansStartTemp"]'
        self.type(input_fan_start_temp_link, str(temp))

    # 填写风扇关闭温度阀值
    def input_fan_stop_temp(self, temp):
        input_fan_stop_temp_link = 'xpath=>//*[@id="ulFansStopTemp"]'
        self.type(input_fan_stop_temp_link, str(temp))

    # 点击执行所有DRSU风扇开关
    def submit_all_drsu_fans_cfg(self):
        submit_all_drsu_fans_cfg_link = 'xpath=>//*[@id="btn_dianyuankaiguan1"]'
        self.click(submit_all_drsu_fans_cfg_link)

    # # 点击查询所有DRSU电源参数 这个按钮没见过了啊
    # def qry_all_drsu_fans_cfg_click(self):
    #     qry_all_drsu_fans_cfg_link = 'xpath=>//*[@id="btn_config"]'
    #     self.click(qry_all_drsu_fans_cfg_link)
    #     self.sleep(1)

    # 点击查询所有DRSU自动启停时间
    def qry_all_drsu_auto_time_click(self):
        qry_all_drsu_auto_time_link = 'xpath=>//*[@id="btn_getAllDrsuInDRCx"]'
        self.click(qry_all_drsu_auto_time_link)
        self.sleep(1)

    # 是否弹出查询所有DRSU自动启停时间弹出
    def is_prompt_visible_auto(self):
        selector = '//*[@id="chakandianyuankaiguanModalLabel11"]'
        ret = self.is_visible(selector)
        logger.info("是否弹出查询所有DRSU自动启停时间弹窗%s" % ret)
        return ret

    # 获取自动开始DRSU时间
    def get_auto_drsu_start_time(self):
        # auto_drsu_start_time_link = 'xpath=>//*[@id="ausStartTime"]'
        auto_drsu_start_time_link = 'xpath=>//*[@id="chakandianyuankaiguan-form11"]/div[1]/div[2]'
        try:
            start_time = self.find_element(auto_drsu_start_time_link).text
            # start_time1 = self.find_element(auto_drsu_start_time_link).get_attribute('textContent')
            # start_time2 = self.find_element(auto_drsu_start_time_link).get_attribute('innerText')
            # start_time3 = self.find_element(auto_drsu_start_time_link).get_attribute('innerHTML')
            # start_time4 = self.find_element(auto_drsu_start_time_link).getText()
            # print('start_time1', start_time1)
            # print('start_time2', start_time2)
            # print('start_time3', start_time3)
            # print('start_time4', start_time4)
            logger.info('获取自动开始DRSU时间成功：%s' % start_time)
        except:
            logger.error('获取自动开始DRSU时间失败')
            start_time = ''
        return start_time

    # 获取自动开始DRSU时间
    def get_auto_drsu_stop_time(self):
        auto_drsu_stop_time_link = 'xpath=>//*[@id="ausEndTime"]'
        try:
            stop_time = self.find_element(auto_drsu_stop_time_link).text
            logger.info('获取自动关闭DRSU时间成功：%s' % stop_time)
        except:
            logger.error('获取自动关闭DRSU时间失败')
            stop_time = ''
        return stop_time

    # 点击刷新
    def refresh_click(self):
        refresh_link = 'xpath=>/html/body/div[1]/div/div[3]/div[2]/div/div[2]/div/div/div[2]/div[1]/div[2]/button'
        self.click(refresh_link)

    # 点击全屏
    def full_screen_click(self):
        full_screen_link = 'xpath=>/html/body/div[1]/div/div[3]/div[2]/div/div[2]/div/div/div[2]/div[1]/div[' \
                           '2]/div/button '
        self.click(full_screen_link)

    # 点击全选
    def all_election_click(self):
        select_all_click = 'xpath=//*[@id="tb_list"]/thead/tr/th[1]/div[1]/label/input'
        self.click(select_all_click)

    # 获取DRSU设备记录条数(数量)
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
        logger.info('共找到%s条记录' % count)
        return count

    # 选择指定唯一标识设备 填写正确且只有一页的情况是不会报错的
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

    # 选择指定唯一标识设备 drsu页面无法指定drsuid
    def device_select_click(self, drsu_id, num):
        n = 1
        i = 0
        # for i in range(1, num + 1):
        while True:
            try:
                choose_box_link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(n) + ']/td[2]'
                record_dev_id = self.find_element(choose_box_link_temp).text
                if record_dev_id == str(drsu_id):
                    choose_box_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(n) + ']/td[1]/label/input'
                    self.click(choose_box_link)
                    logger.info("点击指定标识设备成功 drsu_id:%s" % str(drsu_id))
                    return n
                n += 1
            except:
                i += 1
                if n == num + 1 or i == 10:
                    break
        self.get_windows_img()
        logger.error("点击指定标识设备失败 drsu_id:%s" % str(drsu_id))
        return 0

    # 获取drsu状态 参数index为device_select_click返回的值 目前暂时只需要获取状态
    def get_drsu_status(self, index):
        drsu_status_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(index) + ']/td[4]'
        drsu_status = self.find_element(drsu_status_link).text
        logger.info("指定标识设备状态为：%s" % drsu_status)
        if drsu_status == '在线':
            return True
        else:
            return False

    # 点击开箱告警延迟配置
    def open_box_alarm_delay_cfg(self):
        open_box_alarm_delay_cfg_link = 'xpath=>//*[@id="btn_config"]'
        self.click(open_box_alarm_delay_cfg_link)

    # 是否存在开箱告警延迟开始时间弹窗
    # def is_exist_prompt3(self):
    #     selector = '//*[@id="configKaixianggaojingModalLabel"]'
    #     ret = self.is_visible(selector)
    #     logger.info("是否弹出开箱告警延迟开始时间弹窗：%s" % ret)
    #     return ret
    def is_prompt_visible_delay(self):
        selector = '//*[@id="configKaixianggaojingModalLabel"]'
        ret = self.is_visible(selector)
        logger.info("是否弹出开箱告警延迟开始时间弹窗%s" % ret)
        return ret

    # 填写开箱告警延迟开启时间
    def input_open_box_alrm_delay(self, time):
        input_open_box_alrm_delay_link = 'xpath=>//*[@id="ulMinuteLater"]'
        self.type(input_open_box_alrm_delay_link, str(time))

    # 点击关闭 建议使用esc键代替
    def close_window_click1(self):
        close_window_link = 'xpath=>//*[@id="configKaixianggaojing"]/div/div/div[2]/div/button[1]'
        self.click(close_window_link)

    # 点击执行开箱告警延迟配置
    def submit_open_box_alarm_delay(self):
        submit_open_box_alarm_link = 'xpath=>//*[@id="btn_kaixianggaojing"]'
        self.click(submit_open_box_alarm_link)

    # 获取drsu状态 参数index为device_select_click返回值 从1开始 index1 为你想要获取的数据的index值 返回值为字符串
    # index1 取值 0-8 0：DRSU唯一标识 1：子设备数量 2：状态 3：风扇开启温度阈值 4：风扇关闭温度阈值 5：
    # 6：机箱内温度值 7：机箱外温度值 8：操作
    def get_drsu_parm(self, index, parm):
        index1 = drsu_parm_dict[parm]
        drsu_parm_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(index) + ']/td[' + str(index1) + ']'
        try:
            drsu_parm = self.find_element(drsu_parm_link).text
            logger.info("指定drsu%s为:%s" % (parm, drsu_parm))
            return drsu_parm
        except:
            raise ValueError

    # 点击详情 主要获取主页面上获取不到的数据
    def info_click(self, index):
        info_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(index) + ']/td[10]/a[1]/button'
        self.click(info_link)

    # 点击详情关闭
    def info_close_click(self):
        info_close_link = 'xpath=>//*[@id="drsuRunningVersionInfoModal"]/div/div/div[3]/button'
        self.click(info_close_link)

    # 是否出现drsu电源管理详情弹窗
    def is_prompt_visible_info_spec(self):
        selector = '//*[@id="drsuRunningVersionInfoModalLabel"]'
        ret = self.is_visible(selector)
        logger.info("是否弹出drsu电源管理详情弹窗%s" % ret)
        return ret

    # 获取详情中的数据
    # ‘//*[@id="Ulglobaldrsuid"]’ '/html/body/div[1]/div/div[4]/div/div/div[2]/div/div[1]/div[2]/span'
    # 1、标识2、在线状态 3、子设备数量 4、雷达激光电源开关状态 5、摄像头电源开光状态 6、风扇电源开关状态 7、开箱告警功能
    # 8、开箱告警延迟开启时间 9、风扇开启温度阈值 10、风扇关闭温度阈值 11、机箱内温度值 12、机箱外温度值
    def get_drsu_running_info(self, index):
        info_link = 'xpath=>/html/body/div[1]/div/div[4]/div/div/div[2]/div/div[' + str(index) + ']/div[2]/span'
        return self.find_element(info_link).text

    # 点击开关
    def switch_click(self, index):
        # '/html/body/div/div/div[3]/div[2]/div/div[2]/div/div/div[2]/div[2]/div[2]/table/tbody/tr[5]/td[10]/a[2]/button'
        # '/html/body/div/div/div[3]/div[2]/div/div[2]/div/div/div[2]/div[2]/div[2]/table/tbody/tr[4]/td[10]/a[2]/button'
        # switch_link = 'xpath=>//*[@id="kaiguan"]'
        switch_link = 'xpath=>/html/body/div/div/div[3]/div[2]/div/div[2]/div/div/div[2]/div[2]/div[2]/table/tbody/tr[' + str(
            index) + ']/td[10]/a[2]/button'
        self.click(switch_link)

    # 是否出现drsu电源开关弹窗
    def is_prompt_visible_power_spec(self):
        selector = '//*[@id="configAllDrsuOfDrcidModalLabel"]'
        ret = self.is_visible(selector)
        logger.info("是否弹出drsu电源开关弹窗%s" % ret)
        return ret

    # 选择电源开关配置模式 0指定子设备1全部子设备
    def choose_drsu_power_type(self, value):
        sel = self.find_element('xpath=>//*[@id="ulPeriodOfSatusRpt"]')
        self.wait(1)
        Select(sel).select_by_value('%s' % str(value))
        self.wait(1)

    # DRSU电源开关 2：on 4：off
    @staticmethod
    def drsu_power_on(sel):
        Select(sel).select_by_value('2')

    @staticmethod
    def drsu_power_off(sel):
        Select(sel).select_by_value('4')

    def drsu_power_type(self, value):
        sel = self.find_element('xpath=>//*[@id="emRebootCtrl"]')
        self.wait(1)
        if str.lower(value) == 'on':
            Select(sel).select_by_value('2')
        else:
            Select(sel).select_by_value('4')

    # 激光雷达电源开关 1：on 3：off
    @staticmethod
    def lidar_power_on(sel):
        Select(sel).select_by_value('1')

    @staticmethod
    def lidar_power_off(sel):
        Select(sel).select_by_value('3')

    def lidar_power_type(self, value):
        sel = self.find_element('xpath=>//*[@id="devicelidat"]')
        self.wait(1)
        if str.lower(value) == 'on':
            self.lidar_power_on(sel)
        else:
            self.lidar_power_off(sel)

    # 摄像头电源开关 1：on 3：off
    @staticmethod
    def camera_power_on(sel):
        Select(sel).select_by_value('1')

    @staticmethod
    def camera_power_off(sel):
        Select(sel).select_by_value('3')

    def camera_power_type(self, value):
        sel = self.find_element('xpath=>//*[@id="deviceCamera"]')
        self.wait(1)
        if str.lower(value) == 'on':
            self.camera_power_on(sel)
        else:
            self.camera_power_off(sel)

    # 开箱告警电源开关 1：on 3：off
    @staticmethod
    def open_box_alarm_power_on(sel):
        Select(sel).select_by_value('1')

    @staticmethod
    def open_box_alarm_power_off(sel):
        Select(sel).select_by_value('3')

    def open_box_alarm_power_type(self, value):
        sel = self.find_element('xpath=>//*[@id="deviceRadlatorFan"]')
        self.wait(1)
        if str.lower(value) == 'on':
            self.open_box_alarm_power_on(sel)
        else:
            self.open_box_alarm_power_off(sel)

    # 是否存在开箱告警延迟开始时间弹窗
    def is_prompt_visible_delay_2(self):
        selector = '//*[@id="configKaixianggaojing2ModalLabel"]'
        ret = self.is_visible(selector)
        logger.info("是否弹出开箱告警延迟开始时间弹窗%s" % ret)
        return ret

    # 填写开箱告警延迟开启时间
    def input_open_box_alrm_delay_2(self, time):
        input_open_box_alrm_delay_link = 'xpath=>//*[@id="ulMinuteLater2"]'
        self.type(input_open_box_alrm_delay_link, str(time))

    # 点击执行开箱告警延迟配置
    def submit_open_box_alarm_delay_2(self):
        submit_open_box_alarm_link = 'xpath=>//*[@id="btn_kaixianggaojing2"]'
        self.click(submit_open_box_alarm_link)

    # 点击取消
    def cancel_click(self):
        link = 'link_text=>取消'
        self.click(link)

    # 点击确定 点击确定之后不一定配置成功
    def confirm_click(self):
        link = 'link_text=>确定'
        self.click(link)

    def confirm_click_(self):
        link = 'xpath=>//*[@id="btn_excuteAcuConfig"]'
        self.click(link)

    # 是否存在drsu子设备配置结果弹窗 modal
    def is_prompt_visible_sub_dev_result(self):
        selector = '//*[@id="peizhisuoyoudrcLabel"]'
        ret = self.is_visible(selector)
        logger.info("是否弹出DRSU子设备配置结果弹窗：%s" % ret)
        return ret

    # 获取DRSU子设备配置结果记录条数
    def get_cfg_result_num(self):
        link = 'xpath=>//*[@id="peizhisuoyoudrc"]/div/div/div[2]/div[1]/div[3]/div[1]/span[1]'
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

    # 下面函数为复合动作函数 点击配置所有DRSU电源开关，填入参数、点击执行配置
    # 配置所有DRSU电源开关
    def cfg_all_drsu_power(self, dict_power, expect_exec_rst):
        logger.info('excute dict_power:%s' % dict_power)
        # print(self.all_drsu_power_cfg_click_isvisble())  # 点击“配置所有DRSU传感器电源开关”之前先判断该按钮是否可被点击
        self.all_drsu_power_cfg_click()
        if not self.is_prompt_visible_power():
            if self.info_text() == '该DRC不在线,不可配置参数':
                logger.info('未弹出DRSU电源开关弹窗，但符合预期')
                self.esc_click()
                return True
            else:
                self.info()
                self.get_windows_img()
                return False
        if dict_power['电源开关配置模式'] == '自动':
            self.choose_power_cfg_mode('0')
            self.input_auto_drsu_start_time(dict_power['自动开启DRSU时间'])
            self.sleep(2)
            self.input_auto_drsu_stop_time(dict_power['自动关闭DRSU时间'])
            self.sleep(2)
        else:
            self.choose_power_cfg_mode('1')
            self.choose_power_type(dict_power['电源开关'])

        # 点击执行配置
        self.submit_all_drsu_power_cfg_click()
        self.sleep(1)
        assert self.info()
        if self.info_text() == '配置成功':
            logger.info('配置所有drsu电源开关成功')
            self.esc_click()
            self.sleep(1)
            return True
        elif self.info_text() == expect_exec_rst:
            logger.info('配置所有drsu电源开关失败，但符合预期')
            self.esc_click()
            return True
        elif self.info_text() == '开启时间不能晚于或等于关闭时间':
            logger.info('配置自动开启和关闭DRSU时间失败，但符合预期')
            self.esc_click()
            return True
        else:
            logger.error('配置所有DRSU电源开关失败')
            self.get_windows_img()
            self.esc_click()
            self.sleep(1)
            return False

    # 查询所有drsu电源参数，看是否与配置的一致(查询所有DRSU自动启停时间)
    def qry_all_drsu_auto_power_time(self, dict_power):
        self.qry_all_drsu_auto_time_click()
        self.sleep(1)
        if not self.is_prompt_visible_auto():
            self.info()
            self.get_windows_img()
            return False
        assert dict_power['电源开关配置模式'] == '自动'
        start_time = self.get_auto_drsu_start_time()
        stop_time = self.get_auto_drsu_stop_time()
        if dict_power['自动开启DRSU时间'] != start_time or dict_power['自动关闭DRSU时间'] != stop_time:
            logger.error('查询时间与配置时间不一致，查询时间：%s-%s,配置时间：%s-%s'
                         % (start_time, stop_time, dict_power['自动开启DRSU时间'], dict_power['自动关闭DRSU时间']))
            self.esc_click()
            return False
        else:
            logger.info('查询时间与配置时间一致')
            self.esc_click()
            return True

    # 配置所有DRSU风扇参数
    def cfg_all_drsu_fans(self, dict_fans):
        self.all_drsu_fan_cfg_click()
        if not self.is_prompt_visible_fans():
            self.info()
            self.get_windows_img()
            return False
        self.input_fan_start_temp(dict_fans['风扇开启温度阈值'])
        self.input_fan_stop_temp(dict_fans['风扇关闭温度阈值'])
        self.submit_all_drsu_fans_cfg()
        assert self.info()
        if self.info_text() == '配置成功':
            logger.info('配置所有drsu风扇参数成功')
            self.enter_click()
            self.sleep(1)
            return True
        else:
            logger.error('配置所有drsu风扇参数失败')
            self.esc_click()
            self.sleep(1)
            return False

    # 查询所有drsu风扇参数，看是否与配置的一致
    def qry_all_drsu_fans(self, dict_fans):
        for i in range(1, 12):
            # 先获取状态
            try:
                drsu_status = self.get_drsu_parm(i, '状态')
                if drsu_status == '在线':
                    # drsu_fan_start_temp = self.get_drsu_parm(i, '风扇开启温度阈值')
                    # drsu_fan_stop_temp = self.get_drsu_parm(i, '风扇关闭温度阈值')
                    # self.assertEqual(arr[0], self.get_drsu_parm(i, 3), '获取drsu风扇开启温度和配置不一致')
                    # self.assertEqual(arr[0], self.get_drsu_parm(i, 4), '获取drsu风扇关闭温度和配置不一致')
                    print(self.get_drsu_parm(i, '风扇开启温度阈值'))
                    print(self.get_drsu_parm(i, '风扇关闭温度阈值'))
                    # if drsu_fan_start_temp != dict_fans['风扇开启温度阈值'] or drsu_fan_stop_temp != arr['风扇开启温度阈值']:
                    #     return False
            except ValueError:
                logger.info('验证风扇配置成功')
                return True

    # 开箱告警延迟配置
    def cfg_alarm_delay(self, dict_deley):
        self.open_box_alarm_delay_cfg()
        if not self.is_prompt_visible_delay():
            self.info()
            self.get_windows_img()
            return False
        self.input_open_box_alrm_delay(dict_deley['开箱告警延迟开启时间'])
        self.submit_open_box_alarm_delay()
        self.sleep(1)
        assert self.info()
        if self.info_text() == '配置成功':
            logger.info('配置开箱告警延迟配置成功')
            ret = True
        else:
            logger.error('配置开箱告警延迟配置失败')
            ret = False
        self.esc_click()
        self.sleep(1)
        return ret

    # 查询开箱告警延迟配置结果 先点击详情
    def qry_alarm_delay(self, index, dict_deley):
        self.info_click(index)
        self.sleep(1)
        if not self.is_prompt_visible_info_spec():
            logger.error('没有弹出指定drsu详情弹出')
            return False
        delay_time_link = 'xpath=>//*[@id="Ulopenboxalarmextendtime"]'
        delay_time = self.find_element(delay_time_link).text
        if delay_time == dict_deley['开箱告警延迟开启时间']:
            logger.info('配置开箱告警延迟开启时间参数与查询开箱告警延迟开启时间参数一致')
            return True
        else:
            logger.error('配置参数与查询参数不一致，配置时间：%s，查询时间：%s' %(delay_time, dict_deley['开箱告警延迟开启时间']))
            return False

    # 配置单个DRSU电源开关，点击指定设备之后的开关按钮，弹出的配置弹出
    def cfg_spec_drsu_power(self, index, dict_power, expect_exec_rst):
        logger.info('excute dict_power:%s' % dict_power)
        self.sleep(1)
        self.switch_click(index)  # 点击开关
        self.sleep(1)
        if not self.is_prompt_visible_power_spec():
            self.info()
            self.get_windows_img()
            return False
        if dict_power['DRSU电源类型'] == '全部传感器':
            self.choose_drsu_power_type('1')  # 0 子设备,1 全部传感器
            self.drsu_power_type(dict_power['DRSU电源开关'])
            self.sleep(2)
            self.confirm_click_()
            self.sleep(2)
            assert(self.info())
            if self.info_text() == '配置成功':
                logger.info('配置drsu全部子设备类型开关成功')
                self.esc_click()
                return True
            elif self.info_text() == expect_exec_rst == '配置失败':
                logger.info('配置drsu全部子设备类型开关失败，但符合预期结果')
                self.esc_click()
                return True
            else:
                logger.info('配置drsu全部子设备类型开关失败')
                self.esc_click()
                return False
        elif dict_power['DRSU电源类型'] == '子设备':
            self.choose_drsu_power_type('0')  # 0 子设备,1 全部传感器
            self.lidar_power_type(dict_power['激光雷达电源开关'])
            self.camera_power_type(dict_power['摄像头电源开关'])
            # self.open_box_alarm_power_type(dict_power['开箱告警电源开关'])
            # 只有在开关从on状态到off状态才会弹出弹窗
            # if dict_power['开箱告警电源开关'] == 'OFF' and self.is_prompt_visible_delay_2():
            #     self.input_open_box_alrm_delay_2(dict_power['开箱告警延迟开启时间'])
            #     self.submit_open_box_alarm_delay_2()
            #     if self.info_text() != '配置成功':
            #         self.get_windows_img()
            #         self.esc_click()  # 点击两下退出弹窗
            #         self.esc_click()
            #         logger.error('开箱告警电源开关配置失败')
            #         return False
            #     else:
            #         logger.info('开箱告警电源开关配置成功')
            #         self.enter_click()
            #         self.enter_click()
            self.get_windows_img()
            self.confirm_click_()  # 点击确定 点击之后如果弹出info就是失败 弹出弹窗就读取数据
            self.sleep(5)
            result_dict = self.get_spec_drsu_power_result()
            if expect_exec_rst != result_dict:
                self.get_windows_img()
                logger.error('cfg_spec_drsu_power fail, expect_exec_rst:%s, result_dict:%s' % (expect_exec_rst, result_dict))
                return False
            self.esc_click()
            logger.info('cfg_spec_drsu_power succ, expect_exec_rst:%s, result_dict:%s' % (expect_exec_rst, result_dict))
            return True

    # 获取DRSU子设备配置结果
    def get_spec_drsu_power_result(self):
        result_dict = {}
        if not self.is_prompt_visible_sub_dev_result():
            assert (self.info())
            result_dict['弹窗提示符合预期'] = self.info_text()
            return result_dict
        num = self.get_cfg_result_num()
        for i in range(1, num + 1):
            sub_dev_id_link = 'xpath=>//*[@id="tb_list1"]/tbody/tr[' + str(i) + ']/td[4]'
            result_link = 'xpath=>//*[@id="tb_list1"]/tbody/tr[' + str(i) + ']/td[6]'
            sub_dev_id = self.find_element(sub_dev_id_link).text
            result = self.find_element(result_link).text
            result_dict[sub_dev_id] = result
        # print('result_dict:', result_dict)
        return result_dict

    # 查询子设备配置结果 先点击详情
    # dict_power = {'DRSU电源类型': '子设备', '激光雷达电源开关': 'ON', '摄像头电源开关': 'OFF', '风扇电源开关': 'OFF',
    #               '开箱告警电源开关': 'OFF', '开箱告警延迟开启时间': '440'}
    def qry_sub_dev_info(self, drsu_id, index, dict_power):
        self.sleep(1)   # 解决网页没渲染出来，点不中详情按钮的问题
        self.info_click(index)  # 点击详情
        self.sleep(1)
        if not self.is_prompt_visible_info_spec():
            self.get_windows_img()
            logger.error('没有弹出指定drsu详情页面')
            return False
        # 目前风扇还没有完全实现
        current_drsu_id = self.get_drsu_running_info('1')
        lidar_status = self.get_drsu_running_info('4')
        camera_status = self.get_drsu_running_info('5')
        fan_status = self.get_drsu_running_info('6')
        alarm_status = self.get_drsu_running_info('7')
        if current_drsu_id != drsu_id:
            logger.info('设备详情中的DRSU ID与当前ID不一致，详情ID：%s、当前ID：%s' %(current_drsu_id, drsu_id))
            return False
        self.get_windows_img()
        self.info_close_click()
        if '开关' == dict_power['配置方法']:
            if '全部传感器' == dict_power['DRSU电源类型']:
                # 配置全部子设备的时候不包括开箱告警
                if lidar_status == camera_status == dict_power['DRSU电源开关']:
                    logger.info('设备详情与配置一致')
                    return True
                else:
                    logger.error('设备详情与配置不一致，lidar：%s、camera：%s、fans:%s' %(lidar_status, camera_status, alarm_status))
                    return False
            elif '子设备' == dict_power['DRSU电源类型']:
                if lidar_status == dict_power['激光雷达电源开关'] and camera_status == dict_power['摄像头电源开关'] \
                        and fan_status == dict_power['风扇电源开关'] and alarm_status == dict_power['开箱告警电源开关']:
                    logger.info('设备详情与配置一致')
                    return True
                else:
                    logger.error('设备详情与配置不一致，lidar:%s、camera:%s、fan_status:%s、alarm:%s' % (lidar_status, camera_status, fan_status, alarm_status))
                    return False
        elif '配置所有DRSU传感器电源开关' == dict_power['配置方法']:
            if '手动' == dict_power['电源开关配置模式']:
                if lidar_status == camera_status == dict_power['电源开关']:
                    logger.info('设备详情与配置一致')
                    return True
                else:
                    logger.error('设备详情与配置不一致，lidar：%s、camera：%s、fans:%s' % (lidar_status, camera_status, alarm_status))
                    return False

    def get_all_dev_status(self):
        lidar_status = self.get_drsu_running_info('4')
        camera_status = self.get_drsu_running_info('5')
        fans_status = self.get_drsu_running_info('6')
        alarm_status = self.get_drsu_running_info('7')
        if lidar_status == camera_status == alarm_status == fans_status:
            return lidar_status
        else:
            return None

    # all_sub_dev_info = {'DRSU唯一标识': '', 'DRSU在线状态': '', '子设备数量': '', '激光雷达电源开关状态': '',
    #                     '摄像头电源开关状态': '', '风扇电源开关状态': '', '开箱告警功能': '', '开箱告警延迟开启时间': '',
    #                     '风扇开启温度阈值': '', '风扇关闭温度阈值': '', '当前机箱内温度值': '', '当前机箱外温度值': ''}
    def qry_all_sub_dev_info(self, index, all_sub_dev_info):
        self.info_click(index)
        self.sleep(1)
        if not self.is_prompt_visible_info_spec():
            logger.error('没有弹出指定drsu详情弹出')
            return False
        all_sub_dev_info['DRSU唯一标识'] = self.get_drsu_running_info('1')
        all_sub_dev_info['DRSU在线状态'] = self.get_drsu_running_info('2')
        all_sub_dev_info['子设备数量'] = self.get_drsu_running_info('3')
        all_sub_dev_info['激光雷达电源开关状态'] = self.get_drsu_running_info('4')
        all_sub_dev_info['摄像头电源开关状态'] = self.get_drsu_running_info('5')
        all_sub_dev_info['风扇电源开关状态'] = self.get_drsu_running_info('6')
        all_sub_dev_info['开箱告警功能'] = self.get_drsu_running_info('7')
        all_sub_dev_info['开箱告警延迟开启时间'] = self.get_drsu_running_info('8')
        all_sub_dev_info['风扇开启温度阈值'] = self.get_drsu_running_info('9')
        all_sub_dev_info['风扇关闭温度阈值'] = self.get_drsu_running_info('10')
        all_sub_dev_info['当前机箱内温度值'] = self.get_drsu_running_info('11')
        all_sub_dev_info['当前机箱外温度值'] = self.get_drsu_running_info('12')
        self.get_windows_img()
        self.info_close_click()

    # 获取状态上报的条数，查找底部“显示第 1 到第 3 条记录，总共 3 条记录 每页显示  条记录”这句话
    def get_online_drsu_num(self):
        link = 'xpath=>/html/body/div[1]/div/div[3]/div[2]/div/div[2]/div/div/div[2]/div[3]/div[1]/span[1]'
        txt = self.find_element(link).text # txt='显示第 1 到第 3 条记录，总共 3 条记录 每页显示  条记录'
        a = [int(i) for i in txt if str.isdigit(i)] # 提取txt中的数字
        count = 0
        if a[0] == 1 and a[1] == 1 and a[2] == 0:
            for i in range(3, len(a)):
                count += (10 ** (len(a) - 1 - i)) * a[i]
        else:
            count = a[-1]  # 将最后一个数字赋值给count
        return count

    # 获取drc下所有在线的drsu
    def get_all_online_drsu_via_power(self):
        count = self.get_online_drsu_num()
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
