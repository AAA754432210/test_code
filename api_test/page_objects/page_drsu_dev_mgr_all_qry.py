from api_test.base_page.homepage import HomePage
from common.Log import Logger
from selenium.webdriver.support.select import Select

logger = Logger("DrsuDevMgrAllQryPage").getlog()

drsu_sub_dev_para_tup = ('drsu身份识别', '子设备编号', '设备型号', '子设备版本', '数据上报周期',
                         '告警上报周期', '障碍物算法')


# acu设备配置可以同时制定多个设备
# 该页面点击取消或者弹窗告警确认之后会回到AcuDevMgrPage
# 该页面点击设备配置之后会跳到AcuDevMgrSpecCfgPage
class DrsuDevMgrAllQryPage(HomePage):

    # 点击刷新
    # def refresh_click(self):
    #     refresh_link = 'xpath=>/html/body/div[1]/div/div[3]/div[2]/div/div/div/div/div[2]/div[1]/div[2]/button'
    #     # refresh_link = 'name="refresh"'
    #     self.click(refresh_link)

    # 点击全屏
    def full_screen_click(self):
        full_screen_link = 'xpath=>/html/body/div/div/div[3]/div[2]/div/div/div/div/div[2]/div[1]/div[2]/div/button'
        self.click(full_screen_link)

    # 点击返回
    def return_click(self):
        return_link = 'xpath=>//*[@id="btn_config"]'
        self.click(return_link)

    # 是否弹出没有查到相关数据提示
    def assert_qry_data_success(self):
        if self.info():
            if self.info_text == '没有查到相关数据':
                logger.error('查询所有设备参数失败')
                self.get_windows_img()
                self.esc_click()
                return False
            else:
                logger.error('出现告警')
                self.get_windows_img()
                self.esc_click()
                return False
        else:
            return True
    # # 点击设备配置
    # def dev_cfg_click(self):
    #     dev_cfg_link = 'xpath=>//*[@id="btn_config"]'
    #     self.click(dev_cfg_link)

    # # 点击全选
    # def all_election_click(self):
    #     slect_all_click = 'xpath=>//*[@id="tb_list"]/thead/tr/th[1]/div[1]/label/input'
    #     self.click(slect_all_click)

    # 选择指定唯一标识设备
    def device_select_click(self, dev_id, sub_dev_id):
        for i in range(1, 10):
            drsu_id_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[2]'
            drsu_sub_id_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[3]'
            try:
                drsu_id = self.find_element(drsu_id_link).text
                drsu_sub_id = self.find_element(drsu_sub_id_link).text
                if (drsu_id == str(dev_id)) and (drsu_sub_id == str(sub_dev_id)):
                    logger.info("点击指定标识设备成功 DRSU身份识别:%s，子设备编号：%s" % (str(dev_id), str(sub_dev_id)))
                    return i
            except Exception as e:
                logger.error("点击指定标识设备失败 DRSU身份识别:%s，子设备编号：%s" % (str(dev_id), str(sub_dev_id)))
                print(format(e))
                i = 0
                return i

    # 获取“查询所有DRSU参数”表中共多少条记录
    def get_drsu_sub_dev_info_num(self):
        link = 'xpath=>/html/body/div/div/div[3]/div[2]/div/div/div/div/div[2]/div[3]/div[1]/span[1]'
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

    # 获取drsu子设备信息 第一个参数row表示第row行即第row条记录，也可以是 device_select_click 返回值，第二个参数column为需要获取的数据
    def get_drsu_sub_dev_para(self, row, column):
        link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(row) + ']/td[' + str(column) + ']'
        para = self.find_element(link).text
        logger.info('获取数据%s:%s' % (drsu_sub_dev_para_tup[column], para))
        return para

    # 获取每条记录的全部数据，第一个参数row表示第row行，即第row条记录，也可以是 device_select_click 返回值
    def get_spec_drsu_all_para(self, row):
        list_drsu_info_key = ['drsu身份识别', '子设备编号', '设备型号', '子设备版本号', '告警上报周期', '障碍物算法']
        list_j = []
        try:
            for i in range(2, 8):
                # '//*[@id="tb_list"]/tbody/tr[1]/td[2]'
                # '//*[@id="tb_list"]/tbody/tr[1]/td[7]'
                link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(row) + ']/td[' + str(i) + ']'
                para = self.find_element(link).text
                list_j.append(para)
        except Exception as e:
            logger.info('获取drsu数据失败', format(e))
            self.get_windows_img()
            return {}
        dict_drsu_info = dict(zip(list_drsu_info_key, list_j))
        logger.info('获取第%s条drsu数据成功%s' % (row, dict_drsu_info))
        return dict_drsu_info

    # 子设备数量超过10个时，修改成每页显示100条记录
    def choose_show_info_evey_page(self):
        link_txt = 'xpath=>/html/body/div/div/div[3]/div[2]/div/div/div/div/div[2]/div[3]/div[1]/span[2]/span/button/span[1]'
        logger.info('每页显示%s项信息' % self.find_element(link_txt).text)
        link = 'xpath=>/html/body/div/div/div[3]/div[2]/div/div/div/div/div[2]/div[3]/div[1]/span[2]/span/button'
        link1 = 'xpath=>/html/body/div/div/div[3]/div[2]/div/div/div/div/div[2]/div[3]/div[1]/span[2]/span/ul/li[4]/a'
        self.sleep(0.2)
        self.click(link)
        self.sleep(0.2)
        self.click(link1)
        if self.find_element(link_txt).text != str(100):
            logger.info('每页显示%s项信息' % self.find_element(link_txt).text)
            self.get_windows_img()
        self.sleep(1)
        logger.info('每页显示%s项信息' % self.find_element(link_txt).text)

    # 获取“查询所有DRSU参数”表中的所有信息
    def get_all_drsu_para(self):
        num = self.get_drsu_sub_dev_info_num()
        arr_all_drsu_para = []
        if num > 10:
            self.choose_show_info_evey_page()
        for i in range(1, num+1):
            dict_drsu_info = self.get_spec_drsu_all_para(i)
            arr_all_drsu_para.append(dict_drsu_info)
        logger.info(arr_all_drsu_para)
        return arr_all_drsu_para

    # 子设备数量超过10个时，修改成每页显示100条记录
    def choose_show_info_evey_page(self):
        link_txt = 'xpath=>/html/body/div/div/div[3]/div[2]/div/div/div/div/div[2]/div[3]/div[1]/span[2]/span/button/span[1]'
        logger.info('每页显示%s项信息' % self.find_element(link_txt).text)
        link = 'xpath=>/html/body/div/div/div[3]/div[2]/div/div/div/div/div[2]/div[3]/div[1]/span[2]/span/button'
        link1 = 'xpath=>/html/body/div/div/div[3]/div[2]/div/div/div/div/div[2]/div[3]/div[1]/span[2]/span/ul/li[4]/a'
        self.sleep(1)
        self.click(link)
        self.sleep(1)
        self.click(link1)
        self.sleep(1)
        logger.info('每页显示%s项信息' % self.find_element(link_txt).text)

    # # 判断drsu参数是否和配置参数一致
    # def assert_drsu_cfg(self, dict_drsu_cfg):
    #     dict_drsu_info = self.get_drsu_all_para()
    #     if not dict_drsu_info:
    #         logger.error('获取drsu数据失败')
    #         return False
    #     if not(dict_drsu_cfg['数据上报周期'] == dict_drsu_info['数据上报周期']):
    #         logger.error('数据上报周期，查询数据：%s，配置数据：%s' %(dict_drsu_cfg['数据上报周期'], dict_drsu_info['数据上报周期']))
    #         return False
    #     if not(dict_drsu_cfg['告警上报周期'] == dict_drsu_info['告警上报周期']):
    #         logger.error('告警上报周期，查询数据：%s，配置数据：%s' %(dict_drsu_cfg['告警上报周期'], dict_drsu_info['告警上报周期']))
    #         return False
    #     if not(dict_drsu_cfg['障碍物算法'] == dict_drsu_info['障碍物算法']):
    #         logger.error('障碍物算法，查询数据：%s，配置数据：%s' %(dict_drsu_cfg['障碍物算法'], dict_drsu_info['障碍物算法']))
    #         return False
    #     return True

    # 断言第几列的参数都为value 1'勾选', 2'DRSU身份识别', 3'子设备编号', 4'设备型号', 5'子设备版本', 6'告警上报周期', 7'障碍物算法'
    # def assert_parm(self, column, value):
    #     num = self.get_drsu_sub_dev_info_num()
    #     if num > 10:
    #         self.choose_show_info_evey_page()
    #     for i in range(1, num+1):
    #         parm_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[' + str(column) + ']'
    #         logger.info('i = %s' % i)
    #         para = self.find_element(parm_link).text
    #         if para != str(value):
    #             self.get_windows_img()
    #             logger.error('查询参数与配置参数不一致 column：%s，配置参数：%s，查询参数：%s' % (column, value, para))
    #             return False
    #     logger.info('查询参数与配置参数一致')
    #     return True

    # 目前只需要判断告警上报周期
    def assert_drsu_cfg_period_of_alarm_report(self, dict_drsu_cfg):
        # 1'勾选', 2'DRSU身份识别', 3'子设备编号', 4'设备型号', 5'子设备版本', 6'告警上报周期', 7'障碍物算法'
        # 告警上报周期对应column为第6列
        column = 6
        num = self.get_drsu_sub_dev_info_num()
        if num > 10:
            self.choose_show_info_evey_page()
        for i in range(1, num + 1):
            parm_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[' + str(column) + ']'
            para = self.find_element(parm_link).text
            value = dict_drsu_cfg['告警上报周期']
            logger.info('row：%s，column：%s，para：%s，value：%s' % (i, column, para, value))
            if para != str(value):
                self.get_windows_img()
                logger.error('查询参数与配置参数不一致 row：%s，column：%s，配置参数：%s，查询参数：%s' % (i, column, value, para))
                return False
        logger.info('查询参数与配置参数一致')
        return True

    def assert_drsu_query_period_of_alarm_report(self, arr_all_drsu_para):
        # 1'勾选', 2'DRSU身份识别', 3'子设备编号', 4'设备型号', 5'子设备版本', 6'告警上报周期', 7'障碍物算法'
        # 告警上报周期对应column为第6列
        column = 6
        num = self.get_drsu_sub_dev_info_num()
        if num > 10:
            self.choose_show_info_evey_page()
        for i in range(1, num + 1):
            parm_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[' + str(column) + ']'
            para = self.find_element(parm_link).text
            value = arr_all_drsu_para[i-1]['告警上报周期']
            logger.info('row：%s，column：%s，para：%s，value：%s, %s' % (i, column, para, value, arr_all_drsu_para[i-1]['子设备编号']))
            if para != str(value):
                self.get_windows_img()
                logger.error('查询参数与配置参数不一致 row：%s，column：%s，配置参数：%s，查询参数：%s' % (i, column, value, para))
                return False
        logger.info('查询参数与配置参数一致')
        return True
