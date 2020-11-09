from api_test.base_page.homepage import HomePage
from common.Log import Logger
from selenium.webdriver.support.select import Select

import time

logger = Logger("DrsuStatMgrPage").getlog()


class DrsuStatMgrPage(HomePage):

    # DRSU 身份标识填写
    def input_drsu_id(self, drsu_id):
        input_drsu_id_link = 'xpath=>//*[@id="Term"]'
        self.type(input_drsu_id_link, str(drsu_id))

    # 在线状态选择 'null'全部；'0'上线；'1'下线，默认为全部
    def choose_status(self, value):
        sel = self.find_element('xpath=>//*[@id="LocatfffionDesc"]')
        self.wait(2)
        Select(sel).select_by_value('%s' % str(value))

    # 点击查询
    def qry_click(self):
        link = 'xpath=>//*[@id="btn_query"]'
        self.click(link)

    # 点击刷新
    def refresh_click(self):
        refresh_link = 'xpath=>/html/body/div/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[1]/div[2]/button'
        self.click(refresh_link)

    # 点击全屏
    def full_screen_click(self):
        full_screen_link = 'xpath=>/html/body/div/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div/button'
        self.click(full_screen_link)

    # 点击全选
    def all_election_click(self):
        slect_all_click = 'xpath=//*[@id="tb_list"]/thead/tr/th[1]/div[1]/label/input'
        self.click(slect_all_click)

    #             '//*[@id="tb_list"]/tbody/tr/td[10]/a/button'
    #             '//*[@id="tb_list"]/tbody/tr[5]/td[10]/a/button'
    # 点击详情
    def info_click(self, index='0'):
        if str(index) == '0':
            index_str = ''
        else:
            index_str = '[' + str(index) + ']'
        drc_status_link = 'xpath=>//*[@id="tb_list"]/tbody/tr' + index_str + '/td[10]/a/button'
        drc_status = self.find_element(drc_status_link).text
        logger.info("drsu状态上报信息为:%s" % drc_status)
        if drc_status == '上线':
            return True
        else:
            return False

    # 是否存在drsu详情弹窗
    def is_prompt_visible_drsu_status(self):
        selector = '//*[@id="drsuRunningVersionInfoModalLabel"]'
        ret = self.is_visible(selector)
        logger.info("是否弹出DRSU状态详情弹窗%s" % ret)
        return ret

    # 获取状态上报的条数
    def get_the_report_num(self):
        link = 'xpath=>/html/body/div/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[3]/div[1]/span[1]'
        txt = self.find_element(link).text
        a = [int(i) for i in txt if str.isdigit(i)]
        count = 0
        if a[0] == 1 and a[1] == 1 and a[2] == 0:
            for i in range(3, len(a)):
                count += (10 ** (len(a) - 1 - i)) * a[i]
        else:
            count = a[-1]
        return count

    # 选择指定唯一标识设备
    def device_select_click(self, drsu_id):
        try:
            for i in range(1, 12):
                choose_box_link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[2]'
                if self.find_element(choose_box_link_temp).text == str(drsu_id):
                    choose_box_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[1]/label/input'
                    self.click(choose_box_link)
                    logger.info("点击指定标识设备成功 drsu_id:%s" % str(drsu_id))
                    return i
        except:
            logger.info("点击指定标识设备失败 drsu_id:%s" % str(drsu_id))
            return 0

    # 获取指定drc状态上报是上线还是下线 只有唯一一个的时候index填0
    def get_drsu_report_status(self, index='0'):
        if str(index) == '0':
            index_str = ''
        else:
            index_str = '[' + str(index) + ']'
        drc_status_link = 'xpath=>//*[@id="tb_list"]/tbody/tr' + index_str + '/td[3]'
        drc_status = self.find_element(drc_status_link).text
        logger.info("drsu状态上报信息为:%s" % drc_status)
        if drc_status == '上线':
            return True
        else:
            return False

    # 点击返回DRSU管理
    def back_to_drsu_mgr_page(self):
        back_to_acu_mgr_link = 'xpath=>//*[@id="btn_return"]'
        self.click(back_to_acu_mgr_link)

    # 获取指定drsu的全部信息 上线状态 点击详情 里面查询到的信息
    def get_spec_drsu_info(self):
        list_drsu_info_key = ['DRSU唯一标识', 'DRSU在线状态', '子设备数量', '激光雷达电源开关状态',
                              '摄像头电源开关状态', '风扇电源开关状态', '开箱告警功能',
                              '开箱告警延迟开启时间', '风扇开启温度阈值', '风扇关闭温度阈值',
                              '当前机箱内温度值', '当前机箱外温度值']
        list_j = []
        try:
            for i in range(1, 13):
                link = 'xpath=>/html/body/div[1]/div/div[5]/div/div/div[2]/div/div[' + str(i) + ']/div[2]/span'
                para = self.find_element(link).text
                list_j.append(para)
        except Exception as e:
            logger.error('获取drsu状态周期上报数据失败', format(e))
            return None
        dict_drsu_info = dict(zip(list_drsu_info_key, list_j))
        logger.info('获取drsu状态周期上报数据成功%s' % dict_drsu_info)
        return dict_drsu_info

    # 获取指定drsu的全部信息 上线状态 点击详情 里面查询到的信息
    def get_spec_drsu_info_outline(self, index='0'):
        list_drsu_info_key = ['DRSU唯一标识', '子设备数量', '状态', '风扇开启温度阈值', '风扇关闭温度阈值',
                              '开箱告警延迟开启时间', '机箱内温度值', '机箱外温度值']
        list_j = []
        str_index = '[' + str(index) + ']' if index != '0' else ''
        try:
            for i in range(2, 10):
                link = 'xpath=>//*[@id="tb_list"]/tbody/tr' + str_index + '/td[' + str(i) + ']'
                para = self.find_element(link).text
                list_j.append(para)
        except Exception as e:
            logger.error('获取drsu状态周期上报数据失败', format(e))
            return None
        dict_drsu_info = dict(zip(list_drsu_info_key, list_j))
        logger.info('获取drsu状态周期上报数据成功%s' % dict_drsu_info)
        return dict_drsu_info

    # 获取所有状态的drsu、暂时只支持一页以内的 drsu数量不超过10
    def get_all_status_drsu(self):
        # '//*[@id="tb_list"]/tbody/tr[2]/td[2]'
        count = self.get_the_report_num()
        online = []
        outline = []
        if not count:
            logger.info('没有找到任何drsu')
            return None
        if count == 1:
            drsu_link = 'xpath=>//*[@id="tb_list"]/tbody/tr/td[2]'
            drsu = self.find_element(drsu_link).text
            online.append(drsu)
            status_link = 'xpath=>//*[@id="tb_list"]/tbody/tr/td[4]'
            status = self.find_element(status_link).text
            logger.info('获取全部%s drsu成功:%s' % (status, online))
            return online
        try:
            # '//*[@id="tb_list"]/tbody/tr[1]/td[2]'
            for i in range(1, count + 1):
                drsu_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[2]'
                status_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[4]'
                status = self.find_element(status_link).text
                drsu = self.find_element(drsu_link).text
                if status == '上线':
                    online.append(drsu)
                else:
                    outline.append(drsu)
            logger.info('获取全部drc状态成功，激活drc：%s，未激活drc：%s' % (online, outline))
            return online, outline
        except Exception as e:
            logger.error('获取drc状态失败，原因:%s', format(e))
            return None, None

    # 获取上线\下线状态的drsu、暂时只支持一页以内的drsu数量不超过10
    def get_online_drsu(self, online=True):
        # '//*[@id="tb_list"]/tbody/tr[2]/td[2]'
        if online:
            self.choose_status('1')
        else:
            self.choose_status('0')
        self.qry_click()
        self.sleep(0.5)
        count = self.get_the_report_num()
        if not count:
            logger.info('没有找到任何drsu')
            return None
        online = []
        if count == 1:
            drsu_link = 'xpath=>//*[@id="tb_list"]/tbody/tr/td[2]'
            drsu = self.find_element(drsu_link).text
            online.append(drsu)
            status_link = 'xpath=>//*[@id="tb_list"]/tbody/tr/td[4]'
            status = self.find_element(status_link).text
            logger.info('获取全部%s drsu成功:%s' % (status, online))
            return online
        try:
            for i in range(1, count + 1):
                drsu_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[2]'
                drsu = self.find_element(drsu_link).text
                online.append(drsu)
            status_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[1]/td[4]'
            status = self.find_element(status_link).text
            logger.info('获取全部%s drsu成功:%s' % (status, online))
            return online
        except Exception as e:
            logger.error('获取drsu状态失败，原因:%s', format(e))
            return None

    # 查询指定drsu信息
    def qry_spec_drsu_info(self, drsu_id):
        # 首先输入drsu，点击查询
        self.input_drsu_id(drsu_id)
        self.qry_click()
        self.sleep(0.5)
        # 获取记录条数，如果能查询到就是一条，如果查询不到就是0条
        num = self.get_the_report_num()
        if not num:
            self.get_windows_img()
            logger.error('没有找到指定的drsu')
            return None
        assert num == 1
        # 判断drsu状态 如果是上线状态
        if self.get_drsu_report_status():
            self.info_click()
            if not self.is_prompt_visible_drsu_status():
                self.info()
                self.get_windows_img()
                logger.error('出现错误，没有弹出drsu状态弹窗')
                return None
            dict_drsu_info = self.get_spec_drsu_info()
        else:
            dict_drsu_info = self.get_spec_drsu_info_outline()
        return dict_drsu_info

    # 查询指定drsu状态
    def get_spec_drsu_status(self, drsu_id):
        # 首先输入drsu，点击查询
        self.input_drsu_id(drsu_id)
        self.qry_click()
        time.sleep(3)
        # 获取记录条数，如果能查询到就是一条，如果查询不到就是0条
        num = self.get_the_report_num()
        if num == 1:
            # 判断drsu状态 如果是上线状态
            return self.get_drsu_report_status(0)
        if not num:
            self.get_windows_img()
            logger.error('没有找到指定的drsu')
            return False
        if num > 1:
            self.get_windows_img()
            logger.error('没有找到指定的drsu')
            return False
