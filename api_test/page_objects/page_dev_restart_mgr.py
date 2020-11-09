from api_test.base_page.homepage import HomePage
from common.Log import Logger
from selenium.webdriver.support.select import Select

logger = Logger("DevRstMgrPage").getlog()


class DevRstMgrPage(HomePage):

    # DRC设备重启 选择DRC_ID
    def drc_choose_drc_id(self, drc_id):
        sel = self.find_element('xpath=>//*[@id="drcChoiceListId"]')
        self.sleep(1)
        Select(sel).select_by_value('%s' % str(drc_id))

    # DRSU设备重启 选择DRC_ID
    def drsu_choose_drc_id(self, drc_id):
        sel = self.find_element('xpath=>//*[@id="drsu_drcChoiceListId"]')
        self.sleep(1)
        Select(sel).select_by_value('%s' % str(drc_id))
        self.sleep(1)

    # DRSU设备重启 选择DRSU_ID
    def drsu_choose_drsu_id(self, drsu_id):
        sel = self.find_element('xpath=>//*[@id="drsuChoiceListId"]')
        self.sleep(1)
        Select(sel).select_by_value('%s' % str(drsu_id))
        self.sleep(3)

    # DRC设备重启 点击软件重启
    def drc_software_restart_click(self):
        drc_software_restart_link = 'xpath=>//*[@id="btn_drcsoftware_restart"]'
        self.sleep(1)
        self.click(drc_software_restart_link)
        self.sleep(1)

    # DRC设备重启 点击设备重启
    def drc_device_restart_click(self):
        drc_device_restart_link = 'xpath=>//*[@id="btn_drcrestart"]'
        self.click(drc_device_restart_link)
        self.sleep(1)

    # DRSU设备重启 点击软件重启
    def drsu_software_restart_click(self):
        drc_software_restart_link = 'xpath=>//*[@id="btn_drsusoftware_restart"]'
        self.click(drc_software_restart_link)
        self.sleep(1)

    # DRSU设备重启 点击设备重启
    def drsu_device_restart_click(self):
        drc_device_restart_link = 'xpath=>//*[@id="btn_drsurestart"]'
        self.click(drc_device_restart_link)
        self.sleep(1)

    # DRC软件重启
    def drc_software_restart(self):
        self.drc_software_restart_click()
        self.sleep(1)
        assert (self.info())
        if self.info_text() == 'RET_SUCCESS':
            logger.info('drc 软件重启成功')
            self.esc_click()
            return True
        else:
            logger.error('drc 软件重启失败')
            self.get_windows_img()
            self.esc_click()
            return False

    # DRC设备重启
    def drc_device_restart(self):
        self.drc_device_restart_click()
        self.sleep(1)
        assert (self.info())
        if self.info_text() == 'RET_SUCCESS':
            logger.info('drc 设备重启成功')
            self.esc_click()
            return True
        else:
            logger.error('drc 设备重启失败')
            self.get_windows_img()
            self.esc_click()
            return False

    # DRSU软件重启
    def drsu_software_restart(self):
        self.drsu_software_restart_click()
        self.sleep(1)
        assert(self.info())
        if self.info_text() == 'RET_SUCCESS':
            logger.info('drsu 软件重启成功')
            self.esc_click()
            return True
        else:
            logger.error('drsu 软件重启失败')
            self.get_windows_img()
            self.esc_click()
            return False

    # DRSU设备重启
    def drsu_device_restart(self):
        self.drsu_device_restart_click()
        self.sleep(1)
        assert(self.info())
        if self.info_text() == 'RET_SUCCESS':
            logger.info('drsu 设备重启成功')
            self.esc_click()
            return True
        else:
            logger.error('drsu 设备重启失败')
            self.get_windows_img()
            self.esc_click()
            return False
    # # 点击确定
    # def sure_click(self):
    #     sure_link = 'xpath=>//*[@id="idlg_btn_158341self.sixty8self.sixty12_0"]'
    #     self.click(sure_link)
