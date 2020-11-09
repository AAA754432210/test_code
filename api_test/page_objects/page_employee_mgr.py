from api_test.base_page.homepage import HomePage
from common.Log import Logger
from selenium.webdriver.support.select import Select

logger = Logger("EmployeeMgrPage").getlog()


class EmployeeMgrPage(HomePage):

    # 输入姓名
    def input_employee_name(self, employee_name):
        link = 'xpath=>//*[@id="Term_EmployeeName"]'
        self.type(link, str(employee_name))

    # 输入部门
    def input_department(self, department):
        link = 'xpath=>//*[@id="Term_EmployeeDepartment"]'
        self.type(link, str(department))

    # 输入职位
    def input_position(self, position):
        link = 'xpath=>//*[@id="Term_EmployeePosition"]'
        self.type(link, str(position))

    # 点击查询
    def qry_click(self):
        qry_link = 'xpath=>//*[@id="btn_query"]'
        self.click(qry_link)

    # 点击全选
    def all_selection_click(self):
        slect_all_click = 'xpath=>//*[@id="tb_list"]/thead/tr/th[1]/div[1]/label/input'
        self.click(slect_all_click)

    # 获取状态上报的条数
    # 人员/html/body/div/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[3]/div[1]/span[1]
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

    # 选择指定唯一标识设备（只剩下一项）
    # //*[@id="tb_list"]/tbody/tr[1]/td[2]
    def employee_select_click_single(self):
        link = 'xpath=>//*[@id="tb_list"]/tbody/tr/td[1]/label/input'
        self.click(link)

    # 选择指定运维人员
    def employee_select_click(self, username, num):
        for i in range(1, num+1):
            choose_box_link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[3]'
            if self.find_element(choose_box_link_temp).text == str(username):
                choose_box_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[1]/label/input'
                self.click(choose_box_link)
                logger.info("点击指定运维人员成功 username:%s" % str(username))
                return i
            self.get_windows_img()
            logger.error("点击指定运维人员失败 username:%s" % str(username))
            return 0

    # 选择指定运维人员
    def employee_select_click_by_id(self, user_id, num):
        for i in range(1, num+1):
            choose_box_link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[2]'
            if self.find_element(choose_box_link_temp).text == str(user_id):
                choose_box_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[1]/label/input'
                self.click(choose_box_link)
                logger.info("点击指定运维人员成功 工号:%s" % str(user_id))
                return i
        self.get_windows_img()
        logger.error("点击指定运维人员失败 工号:%s" % str(user_id))
        return 0

    def add_click(self):
        add_link = 'xpath=>//*[@id="btn_addnew"]'
        self.click(add_link)

    # 是否弹出人员新增弹窗
    def is_prompt_visible_add(self):
        selector = '//*[@id="saveemployeeModalLabe"]'
        ret = self.is_visible(selector)
        logger.info("是否弹出人员新增弹窗%s" % ret)
        return ret

    # 输入姓名
    def input_employee_name_add(self, employee_name):
        link = 'xpath=>//*[@id="EmployeeName"]'
        self.type(link, employee_name)

    # 输入工号
    def input_employee_num_add(self, employee_num):
        link = 'xpath=>//*[@id="EmployeeNumber"]'
        self.type(link, employee_num)

    # 输入部门
    def input_employee_depart_add(self, employee_depart):
        link = 'xpath=>//*[@id="EmployeeDepartment"]'
        self.type(link, employee_depart)

    # 输入职位
    def input_employee_position_add(self, employee_position):
        link = 'xpath=>//*[@id="EmployeePosition"]'
        self.type(link, employee_position)

    # 输入职级
    def input_employee_rank_add(self, employee_rank):
        link = 'xpath=>//*[@id="EmployeeRank"]'
        self.type(link, employee_rank)

    # 输入手机
    def input_employee_mobile_add(self, mobile):
        link = 'xpath=>//*[@id="EmployeeMobile"]'
        self.type(link, mobile)

    # 输入邮箱
    def input_employee_email_add(self, email):
        link = 'xpath=>//*[@id="EmployeeEmail"]'
        self.type(link, email)

    # 输入固定电话
    def input_employee_tel_add(self, tel):
        link = 'xpath=>//*[@id="EmployeeTel"]'
        self.type(link, tel)

    # 输入备注
    def input_employee_remark_add(self, remark):
        link = 'xpath=>//*[@id="EmployeeRemark"]'
        self.type(link, remark)

    # 点击新增 ‘运维人员新增成功
    def save_employee_cfg_click(self):
        link = 'xpath=>//*[@id="save_Employee"]'
        self.click(link)

    # 点击关闭
    def close_window_click(self):
        link = 'xpath=>//*[@id="saveemployee"]/div/div/div[3]/button[1]'
        self.click(link)

    def del_click(self):
        del_link = 'xpath=>//*[@id="btn_signout"]'
        self.click(del_link)

    # 点击导入
    def import_click(self):
        import_link = 'xpath=>//*[@id="btn_import"]'
        self.click(import_link)
        self.sleep(1)

    #     file_path = os.path.dirname(os.path.abspath('.')) + '\\tools\\drsu1.xlsx'
    #     # file_path = "D:\\pythoncode\\code\\\tools\\drsu1.xlsx"
    def upload_file(self, file_path):
        self.import_click()
        self.sleep(0.5)
        self.upload(file_path)
        self.sleep(0.5)
        self.info()
        if self.info_text() == '上传成功':
            self.enter_click()
            logger.info('人员信息导入成功')
            return True
        else:
            self.get_windows_img()
            logger.erroir('人员信息导入失败')
            return False

    def chooselist(self, listid):
        if listid == 0:
            list_link = 'xpath=>//*[@id="tb_list"]/tbody/tr/td[1]/label/input'
        else:
            list_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(listid) + ']/td[1]/label/input'
        self.click(list_link)

    # 点击导出
    def export_click(self):
        import_link = 'xpath=>//*[@id="btn_export"]'
        self.click(import_link)
        self.sleep(1)

    # 当只剩下一项的时候，index不需要填写
    def info_click(self, index='0'):
        if str(index) == '0':
            index_str = ''
        else:
            index_str = '[' + str(index) + ']'
        link = 'xpath=>//*[@id="tb_list"]/tbody/tr' + index_str + '/td[8]/a[1]/button'
        try:
            self.click(link)
            logger.info('点击指定运维人员详情成功')
            return True
        except Exception as e:
            self.get_windows_img()
            logger.error('点击指定运维人员详情失败:%s', format(e))
            return False

    def get_value(self, index, **kwargs):
        dict_employee = {'工号': '', '姓名': '', '部门': '',
                          '职位': '', '职级': '', '手机': '',
                          '邮箱': ''}
        if index == 0:
            txt = ''
        else:
            txt = '[' + str(index) + ']'
        i = 2
        for key in dict_employee:
            link = 'xpath=>//*[@id="tb_list"]/tbody/tr' + txt + '/td[' + str(i) + ']'
            # '//*[@id="tb_list"]/tbody/tr/td[2]'
            dict_employee[key] = self.find_element(link).text
            i = i + 1
        return dict_employee

    # 当只剩下一项的时候，index不需要填写
    def edit_click(self, index='0'):
        if str(index) == '0':
            index_str = ''
        else:
            index_str = '[' + str(index) + ']'
        link = 'xpath=>//*[@id="tb_list"]/tbody/tr' + index_str + '/td[9]/a[2]/button'
        # '//*[@id="tb_list"]/tbody/tr/td[9]/a[2]/button'
        try:
            self.click(link)
            logger.info('点击指定运维人员编辑成功')
            return True
        except Exception as e:
            self.get_windows_img()
            logger.error('点击指定运维人员编辑失败:%s', format(e))
            return False

    # 是否弹出人员新增弹窗
    def is_prompt_visible_mod(self):
        selector = '//*[@id="updateRenyuanGuanliModalLabel"]'
        ret = self.is_visible(selector)
        logger.info("是否弹出修改人员信息弹窗%s" % ret)
        return ret

    # 输入姓名
    def input_employee_name_mod(self, employee_name):
        link = 'xpath=>//*[@id="EmployeeName_up"]'
        self.type(link, employee_name)

    # 输入工号
    def input_employee_num_mod(self, employee_num):
        link = 'xpath=>//*[@id="EmployeeNumber_up"]'
        self.type(link, employee_num)

    # 输入部门
    def input_employee_depart_mod(self, employee_depart):
        link = 'xpath=>//*[@id="EmployeeDepartment_up"]'
        self.type(link, employee_depart)

    # 输入职位
    def input_employee_position_mod(self, employee_position):
        link = 'xpath=>//*[@id="EmployeePosition_up"]'
        self.type(link, employee_position)

    # 输入职级
    def input_employee_rank_mod(self, employee_rank):
        link = 'xpath=>//*[@id="EmployeeRank_up"]'
        self.type(link, employee_rank)

    # 输入手机
    def input_employee_mobile_mod(self, mobile):
        link = 'xpath=>//*[@id="EmployeeMobile_up"]'
        self.type(link, mobile)

    # 输入邮箱
    def input_employee_email_mod(self, email):
        link = 'xpath=>//*[@id="EmployeeEmail_up"]'
        self.type(link, email)

    # 输入固定电话
    def input_employee_tel_mod(self, tel):
        link = 'xpath=>//*[@id="EmployeeTel_up"]'
        self.type(link, tel)

    # 输入备注
    def input_employee_remark_mod(self, remark):
        link = 'xpath=>//*[@id="EmployeeRemark_up"]'
        self.type(link, remark)

    # 点击修改 ‘运维人员新增成功
    def save_employee_mod_click(self):
        link = 'xpath=>//*[@id="update_Employee"]'
        self.click(link)

    # 点击关闭
    def close_mod_window_click(self):
        link = 'xpath=>//*[@id="updateRenyuanGuanli"]/div/div/div[3]/button[1]'
        self.click(link)

    def qry_employee(self, dict_qry):
        self.input_employee_name(dict_qry['姓名'])
        self.input_department(dict_qry['部门'])
        self.input_position(dict_qry['职位'])
        self.sleep(0.5)
        self.qry_click()
        self.sleep(0.5)
        num = self.get_the_report_num()
        if num == 0:
            self.get_windows_img()
            logger.error('没有找到指定运维人员', dict_qry)
            return False
        if num != 1:
            self.get_windows_img()
            logger.error('有多个符合条件的运维人员存在', dict_qry)
            return False
        link = 'xpath=>//*[@id="tb_list"]/tbody/tr/td[1]/label/input'
        self.click(link)
        logger.info('点击指定运维人员成功')
        return True

    def add_employee(self, dict_employee):
        self.add_click()
        if not self.is_prompt_visible_add():
            self.get_windows_img()
            logger.error('没有弹出新增运维人员弹窗，提示信息：%s' % self.info_text())
            return False
        self.input_employee_name_add(dict_employee['姓名'])
        self.input_employee_num_add(dict_employee['工号'])
        self.input_employee_depart_add(dict_employee['部门'])
        self.input_employee_position_add(dict_employee['职位'])
        self.input_employee_rank_add(dict_employee['职级'])
        self.input_employee_mobile_add(dict_employee['手机'])
        self.input_employee_email_add(dict_employee['邮箱'])
        self.input_employee_tel_add(dict_employee['固定电话'])
        self.input_employee_remark_add(dict_employee['备注'])
        self.sleep(0.2)
        self.save_employee_cfg_click()
        assert(self.info())
        info = self.info_text()
        if info == dict_employee['预期结果']:
            logger.info('新增运维人员结果符合预期：%s' % dict_employee['预期结果'])
            self.esc_click()
            return True
        else:
            self.get_windows_img()
            logger.error('新增运维人员结果不符合预期，预期结果：%s,实际结果:%s' %(dict_employee['预期结果'], info))
            self.esc_click()
            return False

    def del_employee(self, dict_del):
        if not self.qry_employee(dict_del):
            return False
        self.del_click()
        assert self.info_text() == '确定删除选定员工信息'
        self.sleep(0.5)
        self.confirm_click()
        if self.info_text() == '删除成功':
            logger.info('删除指定人员成功')
            self.enter_click()
            return True
        else:
            self.get_windows_img()
            logger.error('删除指定人员失败')
            self.enter_click()
            return False

    def assert_employee_info(self, dict_qry):
        num = self.qry_employee(dict_qry)
        if num == 0:
            self.get_windows_img()
            logger.error('没有找到指定运维人员', dict_qry)
            return False
        if num != 1:
            self.get_windows_img()
            logger.error('有多个符合条件的运维人员存在', dict_qry)
            return False
        dict_value = self.get_value(0)
        for key in dict_value:
            if dict_value[key] != dict_qry[key]:
                self.get_windows_img()
                logger.info('不存在完全符合条件的运维人员')
                return False
        logger.info('有且只有一个符合条件的运维人员存在')
        return True

    def mod_employee(self, dict_qry, dict_mod):
        if not self.qry_employee(dict_qry):
            return False
        self.edit_click()
        if not self.is_prompt_visible_mod():
            self.get_windows_img()
            logger.error('没有弹出修改人员信息弹窗，提示信息：%s' % self.info_text())
            return False
        self.input_employee_name_mod(dict_mod['姓名'])
        self.input_employee_num_mod(dict_mod['工号'])
        self.input_employee_depart_mod(dict_mod['部门'])
        self.input_employee_position_mod(dict_mod['职位'])
        self.input_employee_rank_mod(dict_mod['职级'])
        self.input_employee_mobile_mod(dict_mod['手机'])
        self.input_employee_email_mod(dict_mod['邮箱'])
        self.input_employee_tel_mod(dict_mod['固定电话'])
        self.input_employee_remark_mod(dict_mod['备注'])
        self.sleep(0.2)
        self.save_employee_mod_click()
        self.sleep(0.2)
        assert (self.info())
        info = self.info_text()
        if info == dict_mod['预期结果']:
            logger.info('修改人员信息结果符合预期：%s' % dict_mod['预期结果'])
            self.esc_click()
            return True
        else:
            self.get_windows_img()
            logger.error('修改人员信息结果不符合预期，预期结果：%s,实际结果:%s' % (dict_mod['预期结果'], info))
            self.esc_click()
            return False

    def confirm_click(self):
        confirm_link_text = 'link_text=>确定'
        self.click(confirm_link_text)

    def del_batch_asset(self):
        self.del_click()
        if self.info_text() == '确定删除选定员工信息':
            self.sleep(2)
            self.confirm_click()
            # self.enter_click()
            # self.esc_click()
            self.sleep(2)
            assert (self.info())
            if self.info_text() == '删除成功':
                self.sleep(2)
                self.enter_click()
                logger.info('员工删除成功')
                return True
        else:
            self.get_windows_img()
            logger.error('员工删除失败%s' % (self.info_text()))
            self.esc_click()
            return False

    def qry_result_check_name(self, dict_employee):
        num = self.get_the_report_num()
        if num == 0:
            logger.info('没有找到任何人员记录')
            return False
        for i in range(1, num+1):
            if num == 1:
                txt = ''
            else:
                txt = '[' + str(i) + ']'
            link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr' + txt + '/td[3]'
            record_employee_name = self.find_element(link_temp).text
            if record_employee_name.find(dict_employee['姓名']) < 0:
                self.get_windows_img()
                return False
        return True

    def qry_result_check_department(self, dict_employee):
        num = self.get_the_report_num()
        if num == 0:
            logger.info('没有找到任何人员记录')
            return False
        for i in range(1, num+1):
            if num == 1:
                txt = ''
            else:
                txt = '[' + str(i) + ']'
            link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr' + txt + '/td[4]'
            record_department = self.find_element(link_temp).text
            if record_department.find(dict_employee['部门']) < 0:
                self.get_windows_img()
                return False
        return True

    def qry_result_check_position(self, dict_employee):
        num = self.get_the_report_num()
        if num == 0:
            logger.info('没有找到任何人员记录')
            return False
        for i in range(1, num+1):
            if num == 1:
                txt = ''
            else:
                txt = '[' + str(i) + ']'
            link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr' + txt + '/td[5]'
            record_position = self.find_element(link_temp).text
            if record_position.find(dict_employee['职位']) < 0:
                self.get_windows_img()
                return False
        return True

    def qry_result_check_all(self, dict_employee):
        num = self.get_the_report_num()
        if num == 0:
            logger.info('没有找到任何人员记录')
            return False
        for i in range(1, num+1):
            if num == 1:
                txt = ''
            else:
                txt = '[' + str(i) + ']'
            link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr' + txt + '/td[3]'
            record_employee_name = self.find_element(link_temp).text
            link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr' + txt + '/td[4]'
            record_department = self.find_element(link_temp).text
            link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr' + txt + '/td[5]'
            record_position = self.find_element(link_temp).text
            if ((dict_employee['姓名'] != '') and (record_employee_name.find(dict_employee['姓名']) < 0)) or \
                    ((dict_employee['部门'] != '') and (record_department.find(dict_employee['部门']) < 0)) or \
                    ((dict_employee['职位'] != '') and (record_position.find(dict_employee['职位']) < 0)):
                self.get_windows_img()
                return False
        return True
