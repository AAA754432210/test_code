from api_test.base_page.homepage import HomePage
from common.Log import Logger


logger = Logger("AcuDevMgrAddPage").getlog()


# 该页面点击取消或者弹窗告警确认之后会回到AcuDevMgrPage
class AcuDevMgrAddPage(HomePage):

    # 填写ACU所属DRC_ID
    def input_drc_id(self, drc_id):
        input_drc_id_link = 'xpath=>//*[@id="drcGlobeId"]'
        self.type(input_drc_id_link, str(drc_id))

    # 填写ACU系统唯一标识
    def input_acu_id(self, acu_id):
        input_acu_id_link = 'xpath=>//*[@id="ulGlobalAcuId"]'
        self.type(input_acu_id_link, str(acu_id))

    # 填写所属发动机号
    def input_engine_no(self, engine_no):
        engine_no_link = 'xpath=>//*[@id="sAcuEngineSerialNum"]'
        self.type(engine_no_link, str(engine_no))

    # 填写所属车牌号
    def input_car_no(self, car_id):
        car_id_link = 'xpath=>//*[@id="sPlateNumber"]'
        self.type(car_id_link, str(car_id))

    # 点击取消
    def cancel_click(self):
        cancel_click_link = 'xpath=>//*[@id="btn_cancel"]'
        self.click(cancel_click_link)

    # 点击重置
    def reset_click(self):
        reset_click_link = 'xpath=>//*[@id="chongzhi"]'
        self.click(reset_click_link)

    # 点击提交保存
    def submit_save_click(self):
        submit_save_click_link = 'xpath=>//*[@id="btn_saveAcu"]'
        self.click(submit_save_click_link)

    # dict_acu = {'ACU所属DRC_ID': '', 'ACU系统唯一标识': '', '所属发动机号': '', '所属车牌号': ''}
    def add_acu_dev(self, dict_acu):
        try:
            self.input_drc_id(dict_acu['ACU所属DRC_ID'])
            if dict_acu['ACU系统唯一标识'] != '':
                self.input_acu_id(dict_acu['ACU系统唯一标识'])
            self.input_engine_no(dict_acu['所属发动机号'])
            self.input_car_no(dict_acu['所属车牌号'])
            self.submit_save_click()
            assert(self.info())
            if self.info_text() == '新增ACU设备固定参数成功':
                logger.info('新增drc设备成功')
                self.enter_click() # 回到drsu设备管理页面 esc会继续停留在当前页面
                return True
            else:
                logger.error('新增acu设备失败:%s' % (self.info_text()))
                self.get_windows_img()
                self.esc_click()
                return False
        except Exception as e:
            logger.error('新增acu设备失败:%s' % format(e))
            self.get_windows_img()
            self.esc_click()
            return False