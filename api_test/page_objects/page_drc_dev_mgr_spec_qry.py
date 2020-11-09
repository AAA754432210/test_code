from api_test.base_page.homepage import HomePage
from common.Log import Logger

logger = Logger("DrcDevMgrSpecQryPage").getlog()


# acu设备配置可以同时制定多个设备
# 该页面点击取消或者弹窗告警确认之后会回到AcuDevMgrPage
# 该页面点击设备配置之后会跳到AcuDevMgrSpecCfgPage
class DrcDevMgrSpecQryPage(HomePage):

    # 点击刷新
    # def refresh_click(self):
    #     refresh_link = 'xpath=>/html/body/div[1]/div/div[3]/div[2]/div/div/div/div/div[2]/div[1]/div[2]/button'
    #     # refresh_link = 'name="refresh"'
    #     self.click(refresh_link)

    # 点击全屏
    def full_screen_click(self):
        full_screen_link = 'xpath=>/html/body/div/div/div[3]/div[2]/div/div/div[2]/div/div/div[2]/div[1]/div[' \
                           '2]/div/button '
        self.click(full_screen_link)

    # 点击返回DRC管理
    def return_click(self):
        return_link = 'xpath=>//*[@id="btn_return"]'
        self.click(return_link)
        self.sleep(1)

    # 点击设备配置 点击之后会跳到DrcDevMgrSpecCfgPage页面
    def dev_cfg_click(self):
        dev_cfg_link = 'xpath=>//*[@id="btn_config"]'
        self.click(dev_cfg_link)

    # 点击全选
    def all_election_click(self):
        slect_all_click = 'xpath=>//*[@id="tb_list"]/thead/tr/th[1]/div[1]/label/input'
        self.click(slect_all_click)

    # 获取指定数据
    def get_drc_spec_para(self, keys):
        dict_drc_info = {'DRC状态上报周期': '2', '融合算法配置': '3', 'ACU存活检测次数': '4', 'CRM接口信息完整性功能配置': '5',
                         'DRSU接口信息完整性功能配置': '6', 'ACU接口信息完整性功能配置': '7', 'CRM接口加密功能配置': '8',
                         'DRSU接口加密功能配置': '9', 'ACU接口加密功能配置': '10'}
        link = 'xpath=>//*[@id="tb_list"]/tbody/tr/td[' + dict_drc_info[keys] + ']'
        para = self.find_element(link).text
        logger.info('获取drc数据%s:%s' % (keys, para))
        return para

    # 获取全部数据
    def get_drc_all_para(self):
        list_drc_info_key = ['DRC状态上报周期', '融合算法配置', 'ACU存活检测次数', 'CRM接口信息完整性功能配置',
                             'DRSU接口信息完整性功能配置', 'ACU接口信息完整性功能配置', 'CRM接口加密功能配置',
                             'DRSU接口加密功能配置', 'ACU接口加密功能配置']
        list_j = []
        try:
            for i in range(2, 11):
                link = 'xpath=>//*[@id="tb_list"]/tbody/tr/td[' + str(i) + ']'
                para = self.find_element(link).text
                list_j.append(para)
        except Exception as e:
            logger.info('获取drc数据失败', format(e))
            return {}
        dict_drc_info = dict(zip(list_drc_info_key, list_j))
        logger.info('获取drc数据成功%s' % dict_drc_info)
        self.get_windows_img()
        return dict_drc_info

    def assert_drc_cfg(self, dict_drc_cfg):
        dict_drc_info = self.get_drc_all_para()
        if not dict_drc_info:
            logger.error('获取drc数据失败')
            return False
        if not(dict_drc_cfg['ACU存活检测次数'] == dict_drc_info['ACU存活检测次数']) and dict_drc_cfg['ACU存活检测次数'] != '':
            logger.error('ACU存活检测次数不一致，查询数据：%s，配置数据：%s' % (dict_drc_cfg['ACU存活检测次数'], dict_drc_info['ACU存活检测次数']))
            return False
        if not(dict_drc_cfg['DRC状态上报周期'] == dict_drc_info['DRC状态上报周期']) and dict_drc_cfg['DRC状态上报周期'] != '':
            logger.error('DRC状态上报周期不一致，查询数据：%s，配置数据：%s' % (dict_drc_cfg['DRC状态上报周期'], dict_drc_info['DRC状态上报周期']))
            return False
        logger.info('查询数据与配置数据一致')
        return True

    def assert_drc_acu_and_period_cfg(self, status_report_period, acu_detect_times):
        dict_drc_info = self.get_drc_all_para()
        if not dict_drc_info:
            logger.error('获取drc数据失败')
            return False
        if not(acu_detect_times == dict_drc_info['ACU存活检测次数']) and acu_detect_times != '':
            logger.error('ACU存活检测次数不一致，查询数据：%s，配置数据：%s' % (acu_detect_times, dict_drc_info['ACU存活检测次数']))
            return False
        if not(status_report_period == dict_drc_info['DRC状态上报周期']) and status_report_period != '':
            logger.error('DRC状态上报周期不一致，查询数据：%s，配置数据：%s' % (status_report_period, dict_drc_info['DRC状态上报周期']))
            return False
        logger.info('查询数据与配置数据一致')
        return True

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
