from api_test.base_page.homepage import HomePage
from common.Log import Logger

logger = Logger("DrcDevMgrAddPage").getlog()


# 该页面为修改drc设备和新增drc设备共用
class DrcDevMgrAddPage(HomePage):

    # 填写DRC系统唯一标识
    def input_drc_id(self, drc_id):
        input_drc_id_link = 'xpath=>//*[@id="ulGlobalDrcId"]'
        self.type(input_drc_id_link, str(drc_id))

    # 填写设备名称
    def input_drc_name(self, drc_name):
        input_drc_name_link = 'xpath=>//*[@id="sName"]'
        self.type(input_drc_name_link, str(drc_name))

    # 填写服务器型号
    def input_server_model(self, server_model):
        input_server_model_link = 'xpath=>//*[@id="stServerMod"]'
        self.type(input_server_model_link, str(server_model))

    # 填写操作系统版本
    def input_os_version(self, os_version):
        input_os_version_link = 'xpath=>//*[@id="strOsVersion"]'
        self.type(input_os_version_link, str(os_version))

    # 填写处理器颗数
    def input_processor_num(self, processor_num):
        processor_num_link = 'xpath=>//*[@id="stProcessorNum"]'
        self.type(processor_num_link, str(processor_num))

    # 填写处理器型号
    def input_processor_type(self, processor_type):
        processor_type_link = 'xpath=>//*[@id="stProcessorType"]'
        self.type(processor_type_link, str(processor_type))

    # 填写单核处理器核心数
    def input_single_processor_core_num(self, core_num):
        core_num_link = 'xpath=>//*[@id="stSingleProcessorCoreNum"]'
        self.type(core_num_link, str(core_num))

    # 填写处理器基本频率
    def input_processor_basic_freq(self, basic_freq):
        basic_freq_link = 'xpath=>//*[@id="stProcessorBasicFreq"]'
        self.type(basic_freq_link, str(basic_freq))

    # 填写内存容量
    def input_mem_cap(self, mem_cap):
        mem_cap_link = 'xpath=>//*[@id="stMemCap"]'
        self.type(mem_cap_link, str(mem_cap))

    # 填写网卡规格
    def input_nm_card_spec(self, nm_card_spec):
        nm_card_spec_link = 'xpath=>//*[@id="stNWCardSpec"]'
        self.type(nm_card_spec_link, str(nm_card_spec))

    # 填写硬盘容量
    def input_hd_cap(self, hd_cap):
        hd_cap_link = 'xpath=>//*[@id="stHDCap"]'
        self.type(hd_cap_link, str(hd_cap))

    # 填写PCIE扩展槽个数
    def input_pcie_exp_slot_num(self, exp_slot_num):
        exp_slot_num_link = 'xpath=>//*[@id="stPcieExpSlotNum"]'
        self.type(exp_slot_num_link, str(exp_slot_num))

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
        submit_save_click_link = 'xpath=>//*[@id="btn_saveDrc"]'
        self.click(submit_save_click_link)

    # # 点击关闭
    # def close_window_click(self):
    #     close_window_link = 'xpath=>//*[@id="idlg_btn_1583306384095_0"]'
    #     self.click(close_window_link)

    # dict_drc = {'DRC系统唯一标识': '', '设备名称': '', '服务器型号': '','操作系统版本': '', '处理器颗数': '', '处理器型号': '',
    # '单颗处理器核心数': '', '处理器基本频率': '', '内容容量': '', '网卡规格': '', '硬盘容量': '', 'PCIE扩张槽个数': '', }
    def add_drc_dev(self, dict_drc):
        try:
            if dict_drc['DRC系统唯一标识'] != '':
                self.input_drc_id(dict_drc['DRC系统唯一标识'])
            self.input_drc_name(dict_drc['设备名称'])
            self.input_server_model(dict_drc['服务器型号'])
            self.input_os_version(dict_drc['操作系统版本'])
            self.input_processor_num(dict_drc['处理器颗数'])
            self.input_processor_type(dict_drc['处理器型号'])
            self.input_single_processor_core_num(dict_drc['单颗处理器核心数'])
            self.input_processor_basic_freq(dict_drc['处理器基本频率'])
            self.input_mem_cap(dict_drc['内容容量'])
            self.input_nm_card_spec(dict_drc['网卡规格'])
            self.input_hd_cap(dict_drc['硬盘容量'])
            self.input_pcie_exp_slot_num(dict_drc['PCIE扩张槽个数'])
            self.submit_save_click()
            assert self.info()
            if self.info_text() == '新增DRC设备固定参数成功':
                logger.info('新增drc设备成功')
                self.enter_click()
                return True
            else:
                logger.error('新增drc设备失败:%s' % (self.info_text()))
                self.get_windows_img()
                self.esc_click()
                return False
        except Exception as e:
            logger.error('新增drc设备失败:%s' % format(e))
            self.get_windows_img()
            self.esc_click()
            return False
