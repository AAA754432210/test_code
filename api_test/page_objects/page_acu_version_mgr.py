from api_test.base_page.homepage import HomePage
from common.Log import Logger
from selenium.webdriver.support.select import Select


logger = Logger("AcuVerMgrPage").getlog()


class AcuVerMgrPage(HomePage):

    # 填入版本名称
    def import_version_name(self, version_name):
        import_version_link = 'xpath=>//*[@id="Term"]'
        self.type(import_version_link, version_name)

    # 点击查询
    def qry_click(self):
        qry_link = 'xpath=>//*[@id="btn_query"]'
        self.click(qry_link)

    # 选择DRC_ID
    def choose_drc_id(self, drc_id):
        sel = self.find_element('xpath=>//*[@id="drcChoiceListId"]')
        self.wait(2)
        Select(sel).select_by_value('%s' % str(drc_id))

    # 点击查询版本信息
    def qry_version_click(self):
        qry_version_link = 'xpath=>//*[@id="btn_allAcuInDRCx"]'
        self.click(qry_version_link)

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

    # 选择指定唯一标识设备
    def device_select_click(self, dev_id):
        for i in range(1, 10):
            choose_box_link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[2]'
            if self.find_element(choose_box_link_temp).text == dev_id:
                choose_box_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[1]/label/input'
                self.click(choose_box_link)
                logger.info("点击指定标识设备成功 dev_id:%u" % dev_id)
                return i
        logger.info("点击指定标识设备失败 dev_id:%u" % dev_id)
        i = 0
        return i

    # 点击新增版本入库
    def version_add_click(self):
        version_add_link = 'xpath=>//*[@id="btn_importVersion"]'
        self.click(version_add_link)

    # 是否存在输入弹窗
    # def is_exist_prompt(self):
    #     promat_head_link = 'xpath=>//*[@id="acuAddNewVersionInfoModalLabel"]'
    #     try:
    #         self.find_element(promat_head_link)
    #         logger.info("弹出版本入库设置弹窗")
    #         return True
    #     except Exception as e:
    #         logger.info("未弹出版本入库设置弹窗")
    #         return False
    def is_prompt_visible(self):
        selector = '//*[@id="acuAddNewVersionInfoModalLabel"]'
        ret = self.is_visible(selector)
        logger.info("是否弹出新增版本入库设置弹窗%s" % ret)
        return ret

    # 输入acu版本名称
    def input_version_name(self, version_name):
        input_version_name_link = 'xpath=>//*[@id="versionName"]'
        self.type(input_version_name_link, version_name)

    # 输入版本所在路径
    def input_version_path(self, version_path):
        input_version_path_link = 'xpath=>//*[@id="sSwDir"]'
        self.type(input_version_path_link, version_path)

    # 输入上传者名称
    def input_version_author(self, author):
        input_version_author_link = 'xpath=>//*[@id="uploadUser"]'
        self.type(input_version_author_link, author)

    # 输入上传时间
    def input_version_time(self, time):
        input_version_author_link = 'xpath=>//*[@id="tUploadTime"]'
        self.type(input_version_author_link, time)

    # 点击关闭
    def close_window_click(self):
        close_window_link = 'xpath=>//*[@id="acuAddNewVersionInfoModal"]/div/div/div[3]/button[1]'
        self.click(close_window_link)

    # 点击执行版本入库
    def version_upload_click(self):
        version_upload_link = 'xpath=>//*[@id="btn_uploadeversion"]'
        self.click(version_upload_link)

    # 点击修改版本信息
    def version_mod_click(self):
        version_mod_link = 'xpath=>//*[@id="btn_editVersion"]'
        self.click(version_mod_link)

    # 点击删除版本
    def version_del_click(self):
        version_del_link = 'xpath=>//*[@id="btn_delVersion"]'
        self.click(version_del_link)

    # 点击查看版本ftp信息
    def version_ftp_qry_click(self):
        version_ftp_qry_link = 'xpath=>//*[@id="btn_ftpquery"]'
        self.click(version_ftp_qry_link)

    # 判断是否弹出保存ftp版本信息弹窗
    def is_prompt_visible2(self):
        selector = '//*[@id="saveftp"]'
        ret = self.is_visible(selector)
        logger.info("是否弹出保存ftp版本信息弹窗%s" % ret)
        return ret

    # 输入ftp域名
    def input_ftp_domain_name(self, domain_name):
        set_ftp_domain_link = 'xpath=>//*[@id="ftpAddress"]'
        self.type(set_ftp_domain_link, str(domain_name))

    # 输入ftp端口
    def input_ftp_port(self, ftp_port):
        set_ftp_port_link = 'xpath=>//*[@id="ftpPort"]'
        self.type(set_ftp_port_link, str(ftp_port))

    # 输入ftp用户名
    def input_ftp_user(self, username):
        set_ftp_user_link = 'xpath=>//*[@id="ftpUserName"]'
        self.type(set_ftp_user_link, str(username))

    # 输入ftp密码
    def input_ftp_password(self, password):
        set_ftp_password_link = 'xpath=>//*[@id="ftpPassword"]'
        self.type(set_ftp_password_link, str(password))

    # 点击保存配置信息
    def save_cfg_click(self):
        save_cfg_link = 'xpath=>//*[@id="btn_saveftp"]'
        self.click(save_cfg_link)

    # 点击关闭
    def close_window_click2(self):
        close_window_link = 'xpath=>//*[@id="idlg_btn_1583488554623_0"]'
        self.click(close_window_link)

    # 点击版本升级
    def version_update_click(self):
        version_qry_link = 'xpath=>//*[@id="btn_acuVersionUpdate"]'
        self.click(version_qry_link)


