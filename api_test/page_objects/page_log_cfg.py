from api_test.base_page.homepage import HomePage
from common.Log import Logger
from selenium.webdriver.support.select import Select

logger = Logger("LogCfgPage").getlog()


class LogCfgPage(HomePage):

    def ftp_fresh(self):
        link = 'xpath=>//*[@id="vueApp"]/div[2]/div/div/div/div/div/div[1]/div[1]/div[2]/button'
        self.click(link)

    # 点击ftp 新建
    def ftp_add_click(self):
        link = 'xpath=>//*[@id="btn_LogFtp_new"]'
        self.click(link)

    # 点击ftp 删除
    # <div class="el-message-box__container"><div class="el-message-box__status el-icon-warning">
    # </div><div class="el-message-box__message"><p>此操作将删除该条目, 是否继续?</p></div></div>
    # /html/body/div[7]/div/div[2]/div[1]
    def ftp_del_click(self):
        link = 'xpath=>//*[@id="btn_LogFtp_Del"]'
        self.click(link)

    def confirm_click(self):
        confirm_link_text = 'link_text=>确定'
        self.click(confirm_link_text)

    def ensure_del_click(self):
        link = 'xpath=>/html/body/div[3]/div/div[3]/button[2]'
        self.click(link)

    # 获取ftp信息的条数
    def get_ftp_info_num(self):
        link = 'xpath=>//*[@id="vueApp"]/div[2]/div/div/div/div/div/div[1]/div[3]/div[1]/span[1]'
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

    # 是否存在新建/修改ftp配置信息弹窗弹窗
    def is_exist_prompt_ftp(self):
        # '//*[@id="FtpModal"]/div/div/div[1]/h4'
        # '//*[@id="FtpModal"]/div/div/div[1]/h4'
        promat_head_link = 'xpath=>//*[@id="FtpModal"]/div/div/div[1]/h4'
        try:
            self.find_element(promat_head_link)
            logger.info("弹出新建ftp配置信息弹窗")
            return True
        except Exception as e:
            logger.info("未弹新建ftp配置信息弹窗")
            return False

    # 输入ftp域名
    def input_ftp_domain_name(self, domain_name):
        set_ftp_domain_link = 'xpath=>//*[@id="FtpModal"]/div/div/div[2]/div/div/form/div[1]/div/div/input'
        self.type(set_ftp_domain_link, str(domain_name))

    # 输入ftp端口
    def input_ftp_port(self, ftp_port):
        set_ftp_port_link = 'xpath=>//*[@id="FtpModal"]/div/div/div[2]/div/div/form/div[2]/div/div/input'
        self.type(set_ftp_port_link, str(ftp_port))

    # 点击确定
    def save_ftp_cfg(self):
        link = 'xpath=>//*[@id="FtpModal"]/div/div/div[3]/button[1]'
        self.click(link)

    # 点击关闭
    def exit_ftp_cfg(self):
        link = 'xpath=>//*[@id="FtpModal"]/div/div/div[3]/button[2]'
        self.click(link)

    def choose_ftp_list(self, listid):
        if listid == 0:
            list_link = 'xpath=>//*[@id="tb_ftp"]/tbody/tr/td[1]/label/input'
        else:
            list_link = 'xpath=>//*[@id="tb_ftp"]/tbody/tr[' + str(listid) + ']/td[1]/label/input'
        self.click(list_link)

    def del_batch_ftp_cfg(self):
        self.ftp_del_click()
        if self.is_exist_prompt_del():
            self.sleep(2)
            # self.confirm_click()
            self.enter_click()
            # self.esc_click()
            self.sleep(2)
            if self.get_alert_info() == '删除FTP配置成功！':
                self.sleep(2)
                self.enter_click()
                logger.info('ftp配置删除成功')
                return True
        else:
            self.get_windows_img()
            logger.error('ftp配置删除失败%s' % (self.get_alert_info()))
            self.esc_click()
            return False

    # 选择指定ftp的id
    def ftp_id_select_click(self, ftp_id, num):
        for i in range(1, num+1):
            if num == 1:
                txt = ''
            else:
                txt = '[' + str(i) + ']'
            choose_box_link_temp = 'xpath=>//*[@id="tb_ftp"]/tbody/tr' + txt + '/td[2]'
            record_version_id = self.find_element(choose_box_link_temp).text
            if record_version_id == str(ftp_id):
                choose_box_link = 'xpath=>//*[@id="tb_ftp"]/tbody/tr' + txt + '/td[1]/label/input'
                self.click(choose_box_link)
                logger.info("点击ftp_id成功 ftp_id:%s" % str(ftp_id))
                return i
        logger.error("点击ftp_id失败 ftp_id:%s" % str(ftp_id))
        return 0

    def ftp_select_click(self, domain, port, num):
        for i in range(1, num+1):
            if num == 1:
                txt = ''
            else:
                txt = '[' + str(i) + ']'
            domain_link_temp = 'xpath=>//*[@id="tb_ftp"]/tbody/tr' + txt + '/td[3]'
            port_link_temp = 'xpath=>//*[@id="tb_ftp"]/tbody/tr' + txt + '/td[4]'
            record_domain = self.find_element(domain_link_temp).text
            record_port = self.find_element(port_link_temp).text
            if record_domain == domain and record_port == str(port):
                choose_box_link = 'xpath=>//*[@id="tb_ftp"]/tbody/tr' + txt + '/td[1]/label/input'
                self.click(choose_box_link)
                logger.info("点击指定ftp配置成功 ftp域名:%s，端口:%s" % (domain, port))
                return i
        logger.error("点击指定ftp配置失败 ftp域名:%s，端口:%s" % (domain, port))
        return 0

    # 点击ftp 修改
    def ftp_mod_click(self, index):
        # '//*[@id="tb_ftp"]/tbody/tr[1]/td[7]/div/button'
        if index == 0:
            link = 'xpath=>//*[@id="tb_ftp"]/tbody/tr/td[7]/div/button'
        else:
            link = 'xpath=>//*[@id="tb_ftp"]/tbody/tr[' + str(index) + ']/td[7]/div/button'
        self.click(link)

    # 日志配置上传配置部分
    # 列表刷新
    def upload_fresh(self):
        link = 'xpath=>//*[@id="vueApp"]/div[4]/div/div/div/div/div/div[1]/div[1]/div[2]/button'
        self.click(link)

    # 点击上传配置 新建
    def log_add_click(self):
        link = 'xpath=>//*[@id="btn_LogConfig_new"]'
        self.click(link)

    # 点击上传配置 删除
    def log_del_click(self):
        link = 'xpath=>//*[@id="btn_LogConfig_del"]'
        self.click(link)

    def is_exist_prompt_del(self):
        # /html/body/div[2]/div/div[2]/div[1]/div[2]
        link = 'class_name=>el-message-box__message'
        info = self.find_element(link).text
        if info == '此操作将删除该条目, 是否继续?':
            return True
        elif info == '请选中需要删除的条目。':
            logger.error('未选中需要删除的条目')
            return False
        else:
            return False

    # 是否存在新建/修改日志配置信息弹窗弹窗
    def is_exist_prompt_log(self):
        promat_head_link = 'xpath=>//*[@id="UploadCfgModal"]/div/div/div[1]/h4'
        try:
            self.find_element(promat_head_link)
            logger.info("弹出新建日志配置信息弹窗")
            return True
        except ValueError:
            logger.info("未弹新建日志配置信息弹窗")
            return False

    # 选择drc_id
    def choose_drc_id(self, drc_id):
        link = 'xpath=>//*[@id="UploadCfgModal"]/div/div/div[2]/div/div/div/form/div[1]/div/div/div/div/input'
        self.input_select_type_(link, drc_id)

    # 选择ftp_id
    def choose_ftp_id(self, ftp_id):
        link = 'xpath=>//*[@id="UploadCfgModal"]/div/div/div[2]/div/div/div/form/div[3]/div/div/div/div/input'
        self.input_select_type_(link, ftp_id)

    # 1:acu 2:drsu 3:drsu和acu 4:drc 5:crm
    def choose_dev_type(self, dev_type):
        link = 'xpath=>//*[@id="UploadCfgModal"]/div/div/div[2]/div/div/div/form/div[2]/div/div/div/div/input'
        self.input_select_type_(link, dev_type)

    # input类型下拉框选择  参数link为下拉框的值，value为要选择的选项值
    def input_select_type_(self, link, value):
        # 采用css定位
        link2 = 'body > div:last-child > div.el-scrollbar > div.el-select-dropdown__wrap.el-scrollbar__wrap > ul'
        # link = 'xpath=>//*[@id="UploadCfgModal"]/div/div/div[2]/div/div/div/form/div[2]/div/div/div/div[1]/input'
        self.input_select(link, link2, value)

    # 输入ftp账号
    def input_ftp_username(self, username):
        # link = 'xpath=>//*[@id="UploadCfgModal"]/div/div/div[2]/div/form[1]/div[3]/div/div/input'
        link = 'xpath=>//*[@id="UploadCfgModal"]/div/div/div[2]/div/div/div/form/div[5]/div/div/div/input'
        self.type(link, str(username))

    # 输入ftp密码
    def input_ftp_password(self, password):
        link = 'xpath=>//*[@id="UploadCfgModal"]/div/div/div[2]/div/div/div/form/div[7]/div/div/div[1]/input'
        self.type(link, str(password))

    def input_upload_day(self, day):
        link = 'xpath=>//*[@id="UploadCfgModal"]/div/div/div[2]/div/div/div/form/div[4]/div/div/div/input'
        self.type(link, str(day))

    def input_upload_time(self, time):
        link = 'xpath=>//*[@id="UploadCfgModal"]/div/div/div[2]/div/div/div/form/div[6]/div/div/div/input'
        self.type_force(link, str(time))

    def input_upload_interval(self, interval):
        link = 'xpath=>//*[@id="UploadCfgModal"]/div/div/div[2]/div/div/div/form/div[9]/div/div/div/input'
        self.type(link, str(interval))

    def input_upload_offset(self, offset):
        link = 'xpath=>//*[@id="UploadCfgModal"]/div/div/div[2]/div/div/div/form/div[10]/div/div/div/input'
        self.type(link, str(offset))

    def input_upload_path(self, path):
        link = 'xpath=>//*[@id="UploadCfgModal"]/div/div/div[2]/div/div/div/form/div[14]/div/div/div/input'
        self.type(link, str(path))

    # 点击确认
    def save_log_cfg(self):
        link = 'xpath=>//*[@id="btn_LogConfigSubmit"]'
        self.click(link)

    # 点击关闭
    def close_window_click_1(self):
        link = 'xpath=>//*[@id="UploadCfgModal"]/div/div/div[3]/button[2]'
        self.click(link)

    # 获取drc_id
    def get_upload_detail(self):
        dict_upload_detail = {}
        drcid_link = 'xpath=>//*[@id="UploadCfgModal"]/div/div/div[2]/div/div/div/form/div[1]/div/div/div/div[1]/input'
        devtype_link = 'xpath=>//*[@id="UploadCfgModal"]/div/div/div[2]/div/div/div/form/div[2]/div/div/div/div[1]/input'
        ftpid_link = 'xpath=>//*[@id="UploadCfgModal"]/div/div/div[2]/div/div/div/form/div[3]/div/div/div/div[1]/input'
        username_link = 'xpath=>//*[@id="UploadCfgModal"]/div/div/div[2]/div/div/div/form/div[5]/div/div/div/input'
        day_link = 'xpath=>//*[@id="UploadCfgModal"]/div/div/div[2]/div/div/div/form/div[4]/div/div/div/input'
        time_link = 'xpath=>//*[@id="UploadCfgModal"]/div/div/div[2]/div/div/div/form/div[6]/div/div/div/input'
        interval_link = 'xpath=>//*[@id="UploadCfgModal"]/div/div/div[2]/div/div/div/form/div[9]/div/div/div/input'
        offset_link = 'xpath=>//*[@id="UploadCfgModal"]/div/div/div[2]/div/div/div/form/div[10]/div/div/div/input'
        path_link = 'xpath=>//*[@id="UploadCfgModal"]/div/div/div[2]/div/div/div/form/div[14]/div/div/div/input'

        dict_upload_detail['drcid'] = self.get_value(drcid_link)
        dict_upload_detail['devtype'] = self.get_value(devtype_link)
        dict_upload_detail['ftpid'] = self.get_value(ftpid_link)
        dict_upload_detail['username'] = self.get_value(username_link)
        dict_upload_detail['day'] = self.get_value(day_link)
        dict_upload_detail['time'] = self.get_value(time_link)
        dict_upload_detail['interval'] = self.get_value(interval_link)
        dict_upload_detail['offset'] = self.get_value(offset_link)
        dict_upload_detail['path'] = self.get_value(path_link)

        return dict_upload_detail

    # 选择指定upload的id
    def upload_id_select_click(self, ftp_id, num):
        for i in range(1, num + 1):
            if num == 1:
                txt = ''
            else:
                txt = '[' + str(i) + ']'
            choose_box_link_temp = 'xpath=>//*[@id="tb_ftp"]/tbody/tr' + txt + '/td[2]'
            record_version_id = self.find_element(choose_box_link_temp).text
            if record_version_id == str(ftp_id):
                choose_box_link = 'xpath=>//*[@id="tb_ftp"]/tbody/tr' + txt + '/td[1]/label/input'
                self.click(choose_box_link)
                logger.info("点击ftp_id成功 ftp_id:%s" % str(ftp_id))
                return i
        logger.error("点击ftp_id失败 ftp_id:%s" % str(ftp_id))
        return 0

    # 获取ftp上传信息的条数
    def get_upload_info_num(self):
        link = 'xpath=>//*[@id="vueApp"]/div[4]/div/div/div/div/div/div[1]/div[3]/div[1]/span[1]'
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

    def upload_select_click(self, drcid, devtype, num):
        for i in range(1, num+1):
            if num == 1:
                txt = ''
            else:
                txt = '[' + str(i) + ']'
            drcid_link_temp = 'xpath=>//*[@id="tb_config"]/tbody/tr' + txt + '/td[2]'
            devtype_link_temp = 'xpath=>//*[@id="tb_config"]/tbody/tr' + txt + '/td[3]'
            record_drcid = self.find_element(drcid_link_temp).text
            record_devtype = self.find_element(devtype_link_temp).text
            if record_drcid == drcid and record_devtype == devtype:
                choose_box_link = 'xpath=>//*[@id="tb_config"]/tbody/tr' + txt + '/td[1]/label/input'
                self.click(choose_box_link)
                logger.info("点击指定上传配置成功 drcid:%s，devtype:%s" % (drcid, devtype))
                return i
        logger.error("点击指定上传配置失败 drcid:%s，devtype:%s" % (drcid, devtype))
        return 0

    # 选择指定drc_id
    def drc_id_select_click(self, drc_id, num):
        for i in range(1, num+1):
            if num == 1:
                txt = ''
            else:
                txt = '[' + str(i) + ']'
            choose_box_link_temp = 'xpath=>//*[@id="tb_config"]/tbody/tr' + txt + '/td[2]'
            record_version_id = self.find_element(choose_box_link_temp).text
            if record_version_id == str(drc_id):
                choose_box_link = 'xpath=>//*[@id="tb_config"]/tbody/tr' + txt + '/td[1]/label/input'
                self.click(choose_box_link)
                logger.info("点击drc_id成功 drc_id:%s" % str(drc_id))
                return i
        logger.error("点击drc_id失败 drc_id:%s" % str(drc_id))
        return 0

    # 点击日志配置 修改
    def config_mod_click(self, index):
        # '//*[@id="tb_config"]/tbody/tr[1]/td[10]/div/button[1]'
        link = 'xpath=>//*[@id="tb_config"]/tbody/tr[' + str(index) + ']/td[10]/div/button[1]'
        self.click(link)

    def config_info_click(self, index):
        # '//*[@id="tb_config"]/tbody/tr[1]/td[10]/div/button[2]'
        if 0 == index:
            link = 'xpath=>//*[@id="tb_config"]/tbody/tr/td[10]/div/button[2]'
        else:
            link = 'xpath=>//*[@id="tb_config"]/tbody/tr[' + str(index) + ']/td[10]/div/button[2]'
        self.click(link)

    def config_switch_click(self, index):
        if 0 == index:
            link = 'xpath=>//*[@id="tb_config"]/tbody/tr/td[10]/div/button[2]'
        else:
            link = 'xpath=>//*[@id="tb_config"]/tbody/tr[' + str(index) + ']/td[10]/div/button[3]'
        self.click(link)

    def get_alert_info(self):
        return self.wait_get_by_class_name('el-message__content')

    # 开关<span class="el-switch__core" style="width: 40px;"></span>
    # <span class="el-switch__core" style="width: 40px;"></span>
    # 选择DRC_ID
    # <div><div role="switch" class="el-switch"><input type="checkbox" name="" true-value="1" false-value="0" class="el-switch__input"><!----><span class="el-switch__core" style="width: 40px;"></span><!----></div></div>
    # <div><div role="switch" aria-checked="true" class="el-switch is-checked"><input type="checkbox" name="" true-value="1" false-value="0" class="el-switch__input"><!----><span class="el-switch__core" style="width: 40px;"></span><!----></div></div>
    # 尝试用is_selected判断
    # <p class="el-message__content">FTP配置失败！存在相同FTP配置请仔细检查</p>
    # 友好型提示 /html/body/div[2]/p
    # /html/body/div[2]/p
    # 错误出现的时候才会有这个元素 //*[@id="FtpModal"]/div/div/div[2]/div/div/form/div[1]/div/div[2]
    # 配置ftp信息错误：/html/body/div[2]/p
    # 错误出现的时候才会有这个元素 //*[@id="FtpModal"]/div/div/div[2]/div/div/form/div[2]/div/div[2]
    # 新增ftp配置
    def add_ftp_cfg(self, dict_ftp):
        self.ftp_add_click()
        assert(self.is_exist_prompt_ftp())
        self.input_ftp_domain_name(dict_ftp['FTP域名'])
        self.sleep(0.2)
        self.input_ftp_port(dict_ftp['端口'])
        self.save_ftp_cfg()
        if dict_ftp['域名预期结果'] and self.wait_get('//*[@id="FtpModal"]/div/div/div[2]/div/div/form/div[1]/div/div[2]') != dict_ftp['域名预期结果']:
            logger.error('新增ftp域名配置结果不符合预期，预期结果：%s,实际结果：%s' %
                         (dict_ftp['域名预期结果'], self.wait_get('//*[@id="FtpModal"]/div/div/div[2]/div/div/form/div[1]/div/div[2]')))
            self.get_windows_img()
            return False
        if dict_ftp['端口预期结果'] and self.wait_get('//*[@id="FtpModal"]/div/div/div[2]/div/div/form/div[2]/div/div[2]') != dict_ftp['端口预期结果']:
            logger.error('新增ftp端口配置结果不符合预期，预期结果：%s,实际结果：%s' %
                         (dict_ftp['端口预期结果'], self.wait_get('//*[@id="FtpModal"]/div/div/div[2]/div/div/form/div[2]/div/div[2]')))
            self.get_windows_img()
            return False
        # body > div.el-message.el-message--success
        # if dict_ftp['预期结果'] and self.wait_get('/html/body/div[2]/p') != dict_ftp['预期结果']:
        if dict_ftp['预期结果'] and self.wait_get_by_class_name('el-message__content') != dict_ftp['预期结果']:
            logger.error('新增ftp配置结果不符合预期，预期结果：%s,实际结果：%s' %
                         (dict_ftp['预期结果'], self.wait_get_by_class_name('el-message__content')))
            self.get_windows_img()
            return False
        logger.info('新增ftp配置结果符合预期:%s,%s,%s' % (dict_ftp['域名预期结果'], dict_ftp['端口预期结果'], dict_ftp['预期结果']))
        return True

    def qry_ftp_cfg(self, dict_ftp, index=1):
        # id_link = 'xpath=>//*[@id="tb_ftp"]/tbody/tr[' + str(index) + ']/td[2]'
        if index == 0:
            domain_link = 'xpath=>//*[@id="tb_ftp"]/tbody/tr/td[3]'
            port_link = 'xpath=>//*[@id="tb_ftp"]/tbody/tr/td[4]'
        else:
            domain_link = 'xpath=>//*[@id="tb_ftp"]/tbody/tr[' + str(index) + ']/td[3]'
            port_link = 'xpath=>//*[@id="tb_ftp"]/tbody/tr[' + str(index) + ']/td[4]'
        # id = self.find_element(id_link).text
        domain = self.find_element(domain_link).text
        port = self.find_element(port_link).text
        if domain != dict_ftp['FTP域名'] or port != dict_ftp['端口']:
            logger.error('查询结果与配置结果不一致，查询ftp域名：%s 查询端口：%s,配置ftp域名：%s,配置端口：%s' %
                         (domain, port, dict_ftp['FTP域名'], dict_ftp['端口']))
            self.get_windows_img()
            return False
        else:
            logger.info('查询结果与配置结果一致:ftp域名：%s，端口:%s' % (domain, port))
            return True

    def del_ftp_cfg(self, dict_ftp):
        num = self.get_ftp_info_num()
        if dict_ftp['ID']:
            index = self.ftp_id_select_click(dict_ftp['ID'], num)
        else:
            index = self.ftp_select_click(dict_ftp['FTP域名'], dict_ftp['端口'], num)
        if index == 0:
            self.get_windows_img()
            logger.error('未找到指定ftp配置', dict_ftp)
            return False
        self.ftp_del_click()
        self.sleep(2)
        if not self.is_exist_prompt_del():
            self.get_windows_img()
            logger.error('删除ftp配置出错')
            return False
        # self.ensure_del_click()
        self.sleep(0.5)
        self.enter_click()
        # /html/body/div[3]/p
        info = self.wait_get_by_class_name('el-message__content')
        if info != dict_ftp['预期结果']:
            logger.error('删除ftp配置结果不符合预期，预期结果：%s,实际结果：%s' %
                         (dict_ftp['预期结果'], info))
            self.get_windows_img()
            return False
        logger.info('新增ftp配置结果符合预期:%s' % (dict_ftp['预期结果']))
        return True

    def find_ftp_cfg(self, dict_ftp):
        num = self.get_ftp_info_num()
        for i in range(1, num+1):
            if num == 1:
                txt = ''
            else:
                txt = '[' + str(i) + ']'
            domain_link_temp = 'xpath=>//*[@id="tb_ftp"]/tbody/tr' + txt + '/td[3]'
            port_link_temp = 'xpath=>//*[@id="tb_ftp"]/tbody/tr' + txt + '/td[4]'
            record_domain = self.find_element(domain_link_temp).text
            record_port = self.find_element(port_link_temp).text
            if record_domain == dict_ftp['FTP域名'] and record_port == dict_ftp['端口']:
                return True
        logger.error("查找指定ftp配置失败 ftp域名:%s，端口:%s" % (dict_ftp['FTP域名'], dict_ftp['端口']))
        return False

    def mod_ftp_cfg(self, dict_ftp, dict_ftp_new):
        num = self.get_ftp_info_num()
        index = 0
        for i in range(1, num + 1):
            if self.qry_ftp_cfg(dict_ftp, i):
                index = i
                break
        self.ftp_mod_click(index)
        assert (self.is_exist_prompt_ftp())
        self.input_ftp_domain_name(dict_ftp_new['FTP域名'])
        self.sleep(0.2)
        self.input_ftp_port(dict_ftp_new['端口'])
        self.save_ftp_cfg()
        if dict_ftp['域名预期结果'] and self.wait_get('//*[@id="FtpModal"]/div/div/div[2]/div/div/form/div[1]/div/div[2]') != \
                dict_ftp['域名预期结果']:
            logger.error('新增ftp域名配置结果不符合预期，预期结果：%s,实际结果：%s' %
                         (dict_ftp['域名预期结果'],
                          self.wait_get('//*[@id="FtpModal"]/div/div/div[2]/div/div/form/div[1]/div/div[2]')))
            self.get_windows_img()
            return False
        if dict_ftp['端口预期结果'] and self.wait_get('//*[@id="FtpModal"]/div/div/div[2]/div/div/form/div[2]/div/div[2]') != \
                dict_ftp['端口预期结果']:
            logger.error('新增ftp端口配置结果不符合预期，预期结果：%s,实际结果：%s' %
                         (dict_ftp['端口预期结果'],
                          self.wait_get('//*[@id="FtpModal"]/div/div/div[2]/div/div/form/div[2]/div/div[2]')))
            self.get_windows_img()
            return False
        # body > div.el-message.el-message--success
        # if dict_ftp['预期结果'] and self.wait_get('/html/body/div[2]/p') != dict_ftp['预期结果']:
        if dict_ftp['预期结果'] and self.wait_get_by_class_name('el-message__content') != dict_ftp['预期结果']:
            logger.error('新增ftp配置结果不符合预期，预期结果：%s,实际结果：%s' %
                         (dict_ftp['预期结果'], self.wait_get_by_class_name('el-message__content')))
            self.get_windows_img()
            return False
        logger.info('新增ftp配置结果符合预期:%s,%s,%s' % (dict_ftp['域名预期结果'], dict_ftp['端口预期结果'], dict_ftp['预期结果']))
        return True

    # 判断开关属性:true or None
    def judge_switch_attribute(self, index):
        if index == 0:
            link = 'xpath=>//*[@id="tb_config"]/tbody/tr/td[6]/div/div'
        else:
            link = 'xpath=>//*[@id="tb_config"]/tbody/tr[' + str(index) + ']/td[6]/div/div'
        return self.get_value(link, 'aria-checked')

    def add_upload_cfg(self, dict_upload):
        self.log_add_click()
        assert (self.is_exist_prompt_log())
        self.choose_drc_id(dict_upload['drcid'])
        self.choose_ftp_id(dict_upload['ftpid'])
        self.choose_dev_type(dict_upload['devtype'])
        self.input_ftp_username(dict_upload['username'])
        self.input_ftp_password(dict_upload['password'])
        self.input_upload_day(dict_upload['day'])
        self.enter_click()
        self.input_upload_time(dict_upload['time'])
        self.enter_click()
        self.input_upload_interval(dict_upload['interval'])
        self.input_upload_offset(dict_upload['offset'])
        self.input_upload_path(dict_upload['path'])
        self.sleep(2)
        self.save_log_cfg()
        # 这里
        # 后面
        # 要加
        # 各输入框的
        # 预期结果
        if dict_upload['预期结果'] and self.wait_get_by_class_name('el-message__content') != dict_upload['预期结果']:
            logger.error('新增上传配置结果不符合预期，预期结果：%s,实际结果：%s' %
                         (dict_upload['预期结果'], self.wait_get_by_class_name('el-message__content')))
            self.get_windows_img()
            return False
        logger.info('新增上传配置结果符合预期：%s' % dict_upload['预期结果'])
        return True

    def del_upload_cfg(self, dict_log):
        num = self.get_upload_info_num()
        index = self.upload_select_click(dict_log['drcid'], dict_log['devtype'], num)
        if index == 0:
            self.get_windows_img()
            logger.error('未找到指定上传配置', dict_log)
            return False
        self.log_del_click()
        self.sleep(2)
        if not self.is_exist_prompt_del():
            self.get_windows_img()
            logger.error('删除上传配置出错')
            return False
        # self.ensure_del_click()
        self.sleep(0.5)
        self.enter_click()
        # /html/body/div[3]/p
        info = self.wait_get_by_class_name('el-message__content')
        if info != dict_log['预期结果']:
            logger.error('删除上传配置结果不符合预期，预期结果：%s,实际结果：%s' %
                         (dict_log['预期结果'], info))
            self.get_windows_img()
            return False
        logger.info('新增ftp配置结果符合预期:%s' % (dict_log['预期结果']))
        return True

    def choose_upload_list(self, listid):
        if listid == 0:
            list_link = 'xpath=>//*[@id="tb_config"]/tbody/tr/td[1]/label/input'
        else:
            list_link = 'xpath=>//*[@id="tb_config"]/tbody/tr[' + str(listid) + ']/td[1]/label/input'
        self.click(list_link)

    def del_batch_upload_cfg(self):
        self.log_del_click()
        if self.is_exist_prompt_log():
            self.sleep(2)
            # self.confirm_click()
            self.enter_click()
            # self.esc_click()
            self.sleep(2)
            if self.get_alert_info() == '删除日志配置成功！':
                self.sleep(2)
                self.enter_click()
                logger.info('上传配置删除成功')
                return True
        else:
            self.get_windows_img()
            logger.error('上传配置删除失败%s' % (self.get_alert_info()))
            self.esc_click()
            return False

    def qry_upload_cfg(self, dict_upload, index=1):
        if index == 0:
            drcid_link = 'xpath=>//*[@id="tb_config"]/tbody/tr/td[2]'
            devtype_link = 'xpath=>//*[@id="tb_config"]/tbody/tr/td[3]'
        else:
            drcid_link = 'xpath=>//*[@id="tb_config"]/tbody/tr[' + str(index) + ']/td[2]'
            devtype_link = 'xpath=>//*[@id="tb_config"]/tbody/tr[' + str(index) + ']/td[3]'
        # id = self.find_element(id_link).text
        drcid = self.find_element(drcid_link).text
        devtype = self.find_element(devtype_link).text
        if drcid != dict_upload['drcid'] or devtype != dict_upload['devtype']:
            logger.error('查询结果与配置结果不一致，查询drcid：%s 查询devtype：%s,配置drcid：%s,配置devtype：%s' %
                         (drcid, devtype, dict_upload['drcid'], dict_upload['devtype']))
            self.get_windows_img()
            return False
        else:
            logger.info('查询结果与配置结果一致:drcid：%s，devtype:%s' % (drcid, devtype))
            return True

    def mod_upload_cfg(self, dict_upload, dict_upload_new):
        num = self.get_upload_info_num()
        for i in range(1, num + 1):
            if self.qry_upload_cfg(dict_upload, i):
                break
        self.config_mod_click(i)
        assert (self.is_exist_prompt_log())
        # self.choose_drc_id(dict_upload_new['drcid'])
        self.choose_ftp_id(dict_upload_new['ftpid'])
        # self.choose_dev_type(dict_upload_new['devtype'])
        self.input_ftp_username(dict_upload_new['username'])
        self.input_ftp_password(dict_upload_new['password'])
        self.input_upload_day(dict_upload_new['day'])
        self.enter_click()
        self.input_upload_time(dict_upload_new['time'])
        self.enter_click()
        self.input_upload_interval(dict_upload_new['interval'])
        self.input_upload_offset(dict_upload_new['offset'])
        self.input_upload_path(dict_upload_new['path'])
        self.sleep(2)
        self.save_log_cfg()
        # 这里
        # 后面
        # 要加
        # 各输入框的
        # 预期结果
        if dict_upload['预期结果'] and self.wait_get_by_class_name('el-message__content') != dict_upload['预期结果']:
            logger.error('修改上传配置结果不符合预期，预期结果：%s,实际结果：%s' %
                         (dict_upload['预期结果'], self.wait_get_by_class_name('el-message__content')))
            self.get_windows_img()
            return False
        logger.info('修改上传配置结果符合预期：%s' % dict_upload['预期结果'])
        return True

    def find_upload_cfg(self, dict_upload):
        num = self.get_upload_info_num()
        for i in range(1, num+1):
            if num == 1:
                txt = ''
            else:
                txt = '[' + str(i) + ']'
            drcid_link = 'xpath=>//*[@id="tb_config"]/tbody/tr' + txt + '/td[2]'
            devtype_link = 'xpath=>//*[@id="tb_config"]/tbody/tr' + txt + '/td[3]'
            day_link = 'xpath=>//*[@id="tb_config"]/tbody/tr' + txt + '/td[4]'
            interval_link = 'xpath=>//*[@id="tb_config"]/tbody/tr' + txt + '/td[5]'
            drcid = self.find_element(drcid_link).text
            devtype = self.find_element(devtype_link).text
            day = self.find_element(day_link).text
            interval = self.find_element(interval_link).text
            if drcid == dict_upload['drcid'] and devtype == dict_upload['devtype']\
                    and day == dict_upload['day'] and interval == dict_upload['interval']:
                return True
        logger.error("查找指定ftp配置失败 drcid:%s，devtype:%s，day:%s，interval:%s" % (dict_upload['drcid'], dict_upload['devtype'], dict_upload['day'], dict_upload['interval']))
        return False

    def find_upload_cfg_detail(self, dict_upload):
        num = self.get_upload_info_num()
        for i in range(1, num+1):
            if num == 1:
                txt = ''
            else:
                txt = '[' + str(i) + ']'
            drcid_link = 'xpath=>//*[@id="tb_config"]/tbody/tr' + txt + '/td[2]'
            devtype_link = 'xpath=>//*[@id="tb_config"]/tbody/tr' + txt + '/td[3]'
            drcid = self.find_element(drcid_link).text
            devtype = self.find_element(devtype_link).text
            if drcid == dict_upload['drcid'] and devtype == dict_upload['devtype']:
                self.config_info_click(i)
                record_upload_config = self.get_upload_detail()
                for k in record_upload_config:
                    if record_upload_config[k] != dict_upload[k]:
                        return False
                return True
        logger.error("查找指定ftp配置失败 ftp域名:%s，端口:%s，day:%s，interval:%s" % (dict_upload['drcid'], dict_upload['devtype'], dict_upload['day'], dict_upload['interval']))
        return False

