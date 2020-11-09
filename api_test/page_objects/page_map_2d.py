from api_test.base_page.homepage import HomePage
from common.Log import Logger
from selenium.webdriver.support.select import Select
import time

logger = Logger("Map2DPage").getlog()


class Map2DPage(HomePage):
    # 点击地图信息
    def map_info_click(self):
        map_info_link = 'xpath=>//*[@id="chk_MapInformation"]'
        self.click(map_info_link)

    # 点击卫星地图
    def stlt_map_info_click(self):
        map_info_link = 'xpath=>//*[@id="chk_MapType"]'
        self.click(map_info_link)

    # 放大地图
    def enlarge_map_click(self):
        enlarge_map_link = 'xpath=>//*[@id="map"]/div/div[3]/div[2]/button[1]'
        self.click(enlarge_map_link)

    # 缩小地图
    def narrow_map_click(self):
        narrow_map_link = 'xpath=>//*[@id="map"]/div/div[3]/div[2]/button[2]'
        self.click(narrow_map_link)

    # 双击地图
    def map_doubleclick(self):
        double_click_map_link = 'xpath=>//*[@id="map"]/div/div/div'
        self.doubleclick(double_click_map_link)

    # 拖拽地图
    def map_drag0(self):
        drag_map_link = 'xpath=>//*[@id="map"]/div/div/div'
        self.drag0(drag_map_link)

    # 拖拽地图
    def map_drag1(self):
        drag_map_link = 'xpath=>//*[@id="map"]/div/div/div'
        self.drag1(drag_map_link)

    # 点击菜单
    def map_menu_click(self):
        map_menu_link = 'xpath=>/html/body/div[3]'
        self.click(map_menu_link)

    # 白天
    def map_3d_day_click(self):
        map_3d_day_link = 'xpath=>//*[@id="id_timemode_0"]'
        self.click(map_3d_day_link)

    # 夜晚
    def map_3d_night_click(self):
        map_3d_night_link = 'xpath=>//*[@id="id_timemode_1"]'
        self.click(map_3d_night_link)

    # 傍晚
    def map_3d_nightfall_click(self):
        map_3d_nightfall_link = 'xpath=>//*[@id="id_timemode_2"]'
        self.click(map_3d_nightfall_link)

    # 晴天
    def map_3d_sunny_click(self):
        map_3d_sunny_link = 'xpath=>//*[@id="id_weathermode_0"]'
        self.click(map_3d_sunny_link)

    # 小雨
    def map_3d_lightrain_click(self):
        map_3d_lightrain_link = 'xpath=>//*[@id="id_weathermode_1"]'
        self.click(map_3d_lightrain_link)

    # 大雨
    def map_3d_heavyrain_click(self):
        map_3d_heavyrain_link = 'xpath=>//*[@id="id_weathermode_2"]'
        self.click(map_3d_heavyrain_link)

    # 小雪
    def map_3d_lightsnow_click(self):
        map_3d_lightsnow_link = 'xpath=>//*[@id="id_weathermode_3"]'
        self.click(map_3d_lightsnow_link)

    # 大雪
    def map_3d_heavysnow_click(self):
        map_3d_heavysnow_link = 'xpath=>//*[@id="id_weathermode_4"]'
        self.click(map_3d_heavysnow_link)

    def map_3d_videoplay(self):
        self.move_and_click()

    def map_3d_videorecord(self, num):
        i = num
        '''每隔5秒保存一张截图'''
        while i > 0:
            self.get_windows_img()
            time.sleep(5)
            i = i - 1

    # 选择acu ‘//*[@id="list-acu"]/li[1]/span’
    # '//*[@id="list-acu"]/li[2]/span'
    # '//*[@id="acuId_123"]' '/html/body/div[1]/div/div/div[1]/table[1]/tbody/tr[1]/td[1]/div/ul/li[1]/img'
    # '/html/body/div[1]/div/div/div[1]/table[1]/tbody/tr[1]/td[1]/div/ul/li[2]/img'
    def spec_acu_select_on(self, acu_name):
        try:
            for i in range (1, 100):
                acu_link = 'xpath=>//*[@id="list-acu"]/li[' + str(i) + ']/span'
                if self.find_element(acu_link).text == str(acu_name):
                    acu_on_off = 'xpath=>/html/body/div[1]/div/div/div[1]/table[1]/tbody/tr[1]/td[1]/div/ul/li[' + str(i) + ']/img'
                    if not self.enable(acu_on_off):
                        logger.info('acu%s2D开关无法被勾选' % str(acu_name))
                    self.click(acu_on_off)
                    logger.info('打开acu%s2D开关成功' %str(acu_name))
                    return i
        except ValueError:
            logger.error('打开acu%s2D开关失败' % str(acu_name))
            return 0

    # '//*[@id="list_drsu"]/li[1]/span'
    # '//*[@id="drsuId_123"]' '/html/body/div[1]/div/div/div[1]/table[2]/tbody/tr[1]/td[1]/div/ul/li[1]/img'
    # '/html/body/div[1]/div/div/div[1]/table[2]/tbody/tr[1]/td[1]/div/ul/li[2]/img'
    # '/html/body/div[1]/div/div/div[1]/table[2]/tbody/tr[1]/td[1]/div/ul/li[1]/span'
    def spec_drsu_select_on(self, drsu_name):
        try:
            for i in range (1, 100):
                drsu_link = 'xpath=>/html/body/div[1]/div/div/div[1]/table[2]/tbody/tr[1]/td[1]/div/ul/li[' + str(i) + ']/span'
                if self.find_element(drsu_link).text == str(drsu_name):
                    drsu_on_off = 'xpath=>/html/body/div[1]/div/div/div[1]/table[2]/tbody/tr[1]/td[1]/div/ul/li[' + str(i) + ']/img'
                    if not self.enable(drsu_on_off):
                        logger.info('drsu%s2D开关无法被勾选' % str(drsu_name))
                    self.click(drsu_on_off)
                    logger.info('打开drsu%s2D开关成功' %drsu_name)
                    return i
        except ValueError:
            logger.error('打开drsu%s2D开关失败' % drsu_name)
            return 0

    def show_chart_click(self):
        show_chart_link = 'xpath=>//*[@id="chk_show_legend"]'
        self.click(show_chart_link)

    def show_dashboard_click(self):
        show_dashboard_link = 'xpath=>//*[@id="chk_show_pannel"]'
        self.click(show_dashboard_link)

    def map_2d_click(self):
        map_2d_link = 'xpath=>//*[@id="chk_2d_map"]'
        self.click(map_2d_link)

    def map_3d_click(self):
        map_3d_link = 'xpath=>//*[@id="chk_3d_map"]'
        self.click(map_3d_link)

    def dev_mgr_click(self):
        dev_mgr_link = 'xpath=>//*[@id="chk_3d_control"]'
        self.click(dev_mgr_link)

    def power_click(self):
        power_link = 'xpath=>//*[@id="id_power"]'
        self.click(power_link)

    # 点击设备管理之后出现的div弹窗 xpath=>//*[@id="switch_pannel_inner"]
    def is_prompt_visible(self):
        selector = '//*[@id="switch_pannel_inner"]'
        ret = self.is_visible(selector)
        logger.info("是否弹出2D地图设备管理设置弹窗%s" % ret)
        return ret

    # 选择DRC_ID
    def choose_drc_id(self, drc_id):
        sel = self.find_element('xpath=>//*[@id="drpbox_drc"]')
        self.wait(1)
        Select(sel).select_by_value('%s' % str(drc_id))

    def refresh_click(self):
        sel = self.find_element('xpath=>//*[@id="switch_pannel_inner"]/table[1]/tbody/tr/td[3]/input')
        self.click(sel)

    def close_window_click(self):
        sel = self.find_element('xpath=>//*[@id="switch_pannel_inner"]/div/input')
        self.click(sel)

    def all_acu_2d_start(self):
        sel = 'xpath=>//*[@id="switch_pannel_inner"]/table[2]/tbody/tr[2]/td[3]/input[1]'
        self.click(sel)

    def all_acu_2d_stop(self):
        sel = 'xpath=>//*[@id="switch_pannel_inner"]/table[2]/tbody/tr[2]/td[3]/input[2]'
        self.click(sel)

    def all_acu_3d_start(self):
        sel = 'xpath=>//*[@id="btn_AcuAll3dOn"]'
        self.click(sel)

    def all_acu_3d_stop(self):
        sel = 'xpath=>//*[@id="btn_AcuAll3dOff"]'
        self.click(sel)

    def all_drsu_2d_start(self):
        sel = 'xpath=>//*[@id="btn_DrsuAll2dOn"]'
        self.click(sel)

    def all_drsu_2d_stop(self):
        sel = 'xpath=>//*[@id="btn_DrsuAll2dOff"]'
        self.click(sel)

    def all_drsu_3d_start(self):
        sel = 'xpath=>//*[@id="btn_DrsuAll3dOn"]'
        self.click(sel)

    def all_drsu_3d_stop(self):
        sel = 'xpath=>//*[@id="btn_DrsuAll3dOff"]'
        self.click(sel)

    # '//*[@id="tr_acuid_800010004"]/td[1]'
    # '//*[@id="tr_acuid_800010005"]/td[1]'
    # '/html/body/div[8]/table[2]/tbody/tr[4]/td[1]/table/tbody/tr[1]/td[1]'
    # '/html/body/div[8]/table[2]/tbody/tr[4]/td[1]/table/tbody/tr[2]/td[1]'
    # '//*[@id="chk_acuid_2d_800010004"]'
    # index 标识你要点击的按钮 2d：index = 2 3D index = 3
    def acu_id_select_click(self, acu_id, index):
        for i in range(1, 12):
            choose_box_link_temp = 'xpath=>/html/body/div[8]/table[2]/tbody/tr[4]/td[1]/table/tbody/tr[' + str(i) + ']/td[1]'
            try:
                record_acu_id = self.find_element(choose_box_link_temp).text
                print('record_acu_id:%s,acu_id:%s' % (str(record_acu_id), str(acu_id)))
                print(str(record_acu_id) == str(acu_id))
                if str(record_acu_id) == str(acu_id):
                    choose_box_link = 'xpath=>/html/body/div[8]/table[2]/tbody/tr[4]/td[1]/table/tbody/tr[' + str(i) + ']/td[' + str(index) + ']/input'
                    if not self.enable(choose_box_link):
                        logger.info('acu_id：%s无法被勾选' % str(acu_id))
                        return 0
                    self.click(choose_box_link)
                    logger.info("点击acu_id成功 acu_id:%s" % str(acu_id))
                    return i
            except ValueError:
                logger.info("点击acu_id失败 acu_id:%s" % str(acu_id))
                i = 0
                return i

    def drsu_id_select_click(self, drsu_id, index):
        for i in range(1, 12):
            choose_box_link_temp = 'xpath=>/html/body/div[8]/table[2]/tbody/tr[4]/td[2]/table/tbody/tr[' + str(i) + ']/td[1]'
            try:
                record_drsu_id = self.find_element(choose_box_link_temp).text
                if record_drsu_id == str(drsu_id):
                    choose_box_link = 'xpath=>/html/body/div[8]/table[2]/tbody/tr[4]/td[2]/table/tbody/tr[' + str(i) + ']/td[' + str(index) + ']/input'
                    if not self.enable(choose_box_link):
                        logger.info('drsu_id：%s无法被勾选' % str(drsu_id))
                        return 0
                    self.click(choose_box_link)
                    logger.info("点击drsu_id成功 drsu_id:%s" % str(drsu_id))
                    return i
            except ValueError:
                logger.info("点击drsu_id失败 drsu_id:%s" % str(drsu_id))
                i = 0
                return i

    def spec_acu_2d_start(self):
        sel = 'xpath=>//*[@id="tb_acu"]/thead/tr[2]/th[2]/input[1]'
        self.click(sel)

    def spec_acu_2d_stop(self):
        sel = 'xpath=>//*[@id="tb_acu"]/thead/tr[2]/th[2]/input[2]'
        self.click(sel)

    def spec_acu_3d_start(self):
        sel = 'xpath=>//*[@id="tb_acu"]/thead/tr[2]/th[3]/input[1]'
        self.click(sel)

    def spec_acu_3d_stop(self):
        sel = 'xpath=>//*[@id="tb_acu"]/thead/tr[2]/th[3]/input[2]'
        self.click(sel)

    def spec_drsu_2d_start(self):
        sel = 'xpath=>//*[@id="tb_drsu"]/thead/tr[2]/th[2]/input[1]'
        self.click(sel)

    def spec_drsu_2d_stop(self):
        sel = 'xpath=>//*[@id="tb_drsu"]/thead/tr[2]/th[2]/input[2]'
        self.click(sel)

    def spec_drsu_3d_start(self):
        sel = 'xpath=>//*[@id="tb_drsu"]/thead/tr[2]/th[3]/input[1]'
        self.click(sel)

    def spec_drsu_3d_stop(self):
        sel = 'xpath=>//*[@id="tb_drsu"]/thead/tr[2]/th[3]/input[2]'
        self.click(sel)