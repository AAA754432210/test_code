from api_test.base_page.homepage import HomePage
from common.Log import Logger
from selenium.webdriver.support.select import Select

logger = Logger("UserMgrPage").getlog()


class UserMgrPage(HomePage):

    # 点击新增
    def add_click(self):
        add_link = 'xpath=>//*[@id="btn_add"]'
        self.click(add_link)

    # 检测是否有弹窗
    def is_exist_prompt_add(self):
        prompt_head_link = 'xpath=>//*[@id="addUserModalLabel"]'
        try:
            self.find_element(prompt_head_link)
            logger.info("弹出新增用户弹窗")
            return True
        except Exception as e:
            logger.info("未弹出新增用户弹窗:%s", format(e))
            return False

    # 输入姓名
    def input_user_name(self, user_name):
        link = 'xpath=>//*[@id="adduserName"]'
        self.type(link, str(user_name))

    # 输入登录账户名
    def input_login_name(self, login_name):
        link = 'xpath=>//*[@id="adduseUserName"]'
        self.type(link, str(login_name))

    # 输入登录密码
    def input_login_password(self, login_password):
        link = 'xpath=>//*[@id="adduserPassword"]'
        self.type(link, str(login_password))

    # 配置权限
    def set_user_privileges(self, value):
        if value == 1:
            swith_link = 'xpath=>//*[@id="stopDrsuAllForm"]/div[2]/div[3]/div/div[1]/label/input'
            swith_link = 'link_text=>"浏览查看权限"'
        elif value == 2:
            # swith_link = 'xpath=>//*[@id="stopDrsuAllForm"]/div[2]/div[3]/div/div[2]/label/input'
            swith_link = 'link_text=>"设备参数配置权限"'
        elif value == 3:
            # swith_link = 'xpath=>//*[@id="stopDrsuAllForm"]/div[2]/div[3]/div/div[3]/label/input'
            swith_link = 'link_text=>"地图权限"'
        elif value == 4:
            # swith_link = 'xpath=>//*[@id="stopDrsuAllForm"]/div[2]/div[3]/div/div[4]/label/input'
            swith_link = 'link_text=>"数据修改权限"'
        elif value == 5:
            swith_link = 'xpath=>//*[@id="stopDrsuAllForm"]/div[2]/div[3]/div/div[5]/label/input'
            swith_link = 'link_text=>"用户管理权限"'
        else:
            return False
        self.click(swith_link)
        return True

    # 配置权限 位运算
    def set_user_privileges2(self, value):
        if value & 0b01:
            # swith_link = 'link_text=>"浏览查看权限"'
            swith_link = 'xpath=>//*[@id="stopDrsuAllForm"]/div[2]/div[3]/div/div[1]/label/input'
            self.click(swith_link)
        if value & 0b10:
            # swith_link = 'link_text=>"设备参数配置权限"'
            swith_link = 'xpath=>//*[@id="stopDrsuAllForm"]/div[2]/div[3]/div/div[2]/label/input'
            self.click(swith_link)
        if value & 0b100:
            # swith_link = 'link_text=>"地图权限"'
            swith_link = 'xpath=>//*[@id="stopDrsuAllForm"]/div[2]/div[3]/div/div[3]/label/input'
            self.click(swith_link)
        if value & 0b1000:
            # swith_link = 'link_text=>"数据修改权限"'
            swith_link = 'xpath=>//*[@id="stopDrsuAllForm"]/div[2]/div[3]/div/div[4]/label/input'
            self.click(swith_link)
        if value & 0b10000:
            # swith_link = 'link_text=>"用户管理权限"'
            swith_link = 'xpath=>//*[@id="stopDrsuAllForm"]/div[2]/div[3]/div/div[5]/label/input'
            self.click(swith_link)
        return True

    # 点击关闭
    def close_window_click(self):
        # close_window_link = 'xpath=>//*[@id="addUserModal"]/div/div/div[3]/button[1]'
        close_window_link = 'xpath=>//*[@id="addUserModal"]/div/div/div[3]/button[1]'
        self.click(close_window_link)

    # 点击提交
    def submit_click(self):
        # submit_link = 'xpath=>//*[@id="btn_LogConfigSwitchSubmit"]'
        submit_link = 'xpath=>//*[@id="btn_addUser"]'
        self.click(submit_link)

    # 点击修改
    def mod_click(self):
        mod_link = 'xpath=>//*[@id="btn_edit"]'
        self.click(mod_link)

    # 检测是否有弹窗
    def is_exist_prompt2(self):
        promat_head_link = 'xpath=>//*[@id="modifyUserModalLabel"]'
        try:
            self.find_element(promat_head_link)
            logger.info("弹出修改用户弹窗")
            return True
        except Exception as e:
            logger.info("未弹出修改用户弹窗")
            return False

    # 输入登录密码
    def input_login_password2(self, login_password):
        link = 'xpath=>//*[@id="modifyuserPassword"]'
        self.type(link, login_password)

    # 点击启用/禁用
    def active_click(self):
        active_link = 'xpath=>//*[@id="btn_active"]'
        self.click(active_link)

    # 检测是否有弹窗
    def is_exist_prompt3(self):
        promat_head_link = 'xpath=>//*[@id="avtiveUserModalLabel"]'
        try:
            self.find_element(promat_head_link)
            logger.info("弹出修改用户弹窗")
            return True
        except Exception as e:
            logger.info("未弹出修改用户弹窗")
            return False

    # 选择启用或警用 1启用 0禁用
    def choose_active_or_not(self, value):
        sel = self.find_element('xpath=>//*[@id="activeUser"]')
        self.wait(2)
        Select(sel).select_by_value('%s' % str(value))

    # 点击删除
    def delete_click(self):
        delete_link = 'xpath=>//*[@id="btn_delete"]'
        self.click(delete_link)

    # 检测是否有弹窗告警
    def is_exist_prompt4(self):
        promat_head_link = 'xpath=>/html/body/div[3]/div/div[1]/div'
        try:
            self.find_element(promat_head_link)
            logger.info("弹出修改用户弹窗")
            return True
        except Exception as e:
            logger.info("未弹出修改用户弹窗")
            return False

    # 点击取消
    def cancel_click(self):
        link = 'link_text=>"取消"'
        self.click(link)

    # 点击确认
    def confirm_click(self):
        link = 'link_text=>"确认"'
        self.click(link)

    # 点击刷新
    def refresh_click(self):
        refresh_link = 'xpath=>/html/body/div[1]/div[1]/div[3]/div[2]/div/div[2]/div/div/div[2]/div[1]/div[2]/button'
        self.click(refresh_link)

    # 点击全屏
    def full_screen_click(self):
        full_screen_link = 'xpath=>/html/body/div[1]/div[1]/div[3]/div[2]/div/div[2]/div/div/div[2]/div[1]/div[' \
                           '2]/div/button'
        self.click(full_screen_link)

    # 点击全选
    def all_election_click(self):
        slect_all_click = 'xpath=>//*[@id="tb_list"]/thead/tr/th[1]/div[1]/label/input'
        self.click(slect_all_click)

    # 选择指定唯一标识设备
    def device_select_click(self, username):
        for i in range(1, 12):
            choose_box_link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[2]'
            try:
                if self.find_element(choose_box_link_temp).text == str(username):
                    choose_box_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[1]/label/input'
                    self.click(choose_box_link)
                    logger.info("点击指定用户成功 username:%s" % str(username))
                    return i
            except:
                logger.info("点击指定用户失败 username:%s" % str(username))
                return 0

    # 点击修改
    def mod_click_(self):
        mod_link = 'xpath=>//*[@id="btn_edit"]'
        self.click(mod_link)

    # 点击运行版本
    def version_qry_click(self):
        version_qry_link = 'xpath=>//*[@id="btn_versionquery"]'
        self.click(version_qry_link)

    # 注销用户
    def login_out(self):
        user_link = 'xpath=>/html/body/div/div/div[2]/div/nav/ul/li[1]/a'
        login_out_link = 'xpath=>/html/body/div/div/div[2]/div/nav/ul/li[1]/ul/li[3]/a'
        self.click(user_link)
        self.sleep(0.5)
        self.click(login_out_link)
        self.sleep(0.5)

    def add_user(self, dict_users):
        self.add_click()
        if not self.is_exist_prompt_add():
            logger.error('新增用户失败，没有出现新增用户弹窗')
            self.info()
            self.get_windows_img()
            return False
        self.input_user_name(dict_users['姓名'])
        self.input_login_name(dict_users['登录账户名'])
        self.input_login_password(dict_users['密码'])
        self.set_user_privileges2(dict_users['权限'])
        self.submit_click()
        assert self.info()
        if self.info_text() == dict_users['新增结果']:
            logger.info('新增用户结果符合预期:%s' % dict_users['新增结果'])
            self.esc_click()
            return True
        else:
            logger.error('新增用户结果不符合预期，预期结果：%s,实际结果：%s' % (dict_users['新增结果'], self.info_text()))
            self.get_windows_img()
            self.esc_click()
            return False

    def check_user(self, dict_users):
        self.add_click()
        if not self.is_exist_prompt_add():
            logger.error('新增用户失败，没有出现新增用户弹窗')
            self.info()
            self.get_windows_img()
            return False
        self.input_user_name(dict_users['姓名'])
        self.input_login_name(dict_users['登录账户名'])
        self.input_login_password(dict_users['密码'])
        self.set_user_privileges2(dict_users['权限'])
        self.submit_click()
        assert self.info()
        if self.info_text() == dict_users['新增结果']:
            logger.info('新增用户结果符合预期:%s' % dict_users['新增结果'])
            self.esc_click()
            return True
        else:
            logger.error('新增用户结果不符合预期，预期结果：%s,实际结果：%s' % (dict_users['新增结果'], self.info_text()))
            self.get_windows_img()
            self.esc_click()
            return False