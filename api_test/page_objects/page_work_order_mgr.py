from api_test.base_page.homepage import HomePage
from common.Log import Logger
from selenium.webdriver.support.select import Select

logger = Logger("WorkOrderMgrPage").getlog()


class WorkOrderMgrPage(HomePage):

    # 输入工单编号
    def input_work_order_num(self, num):
        link = 'xpath=>//*[@id="query_WorkOrderNumber"]'
        self.type(link, str(num))

    # 输入工单名称
    def input_work_order_name(self, name):
        link = 'xpath=>//*[@id="query_WorkOrderName"]'
        self.type(link, str(name))

    # 输入工单负责人
    def input_work_order_owner(self, owner):
        link = 'xpath=>//*[@id="query_WorkOrderPrincipal"]'
        self.type(link, str(owner))

    # 输入工单发起人
    def input_work_order_submitter(self, submitter):
        link = 'xpath=>//*[@id="query_WorkOrderInitiator"]'
        self.type(link, str(submitter))

    # 输入开始时间
    def input_start_time(self, time):
        link = 'xpath=>//*[@id="query_CreatedDatetimeBegin"]'
        self.type(link, str(time))

    # 输入结束时间
    def input_end_time(self, time):
        link = 'xpath=>//*[@id="query_CreatedDatetimeClose"]'
        self.type(link, str(time))

    # 点击查询
    def qry_click(self):
        qry_link = 'xpath=>//*[@id="btn_query"]'
        self.click(qry_link)

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

    # 选择指定唯一标识设备（只剩下一项）
    # //*[@id="tb_list"]/tbody/tr[1]/td[2]
    def device_select_click_single(self):
        link = 'xpath=>//*[@id="tb_list"]/tbody/tr/td[1]/label/input'
        self.click(link)

    # 选择指定工单
    def device_select_click(self, work_order_name):
        for i in range(1, 12):
            choose_box_link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[3]'
            try:
                if self.find_element(choose_box_link_temp).text == str(work_order_name):
                    choose_box_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[1]/label/input'
                    self.click(choose_box_link)
                    logger.info("点击指定工单成功 工单名称:%s" % str(work_order_name))
                    return i
            except:
                logger.info("点击指定工单失败 工单名称:%s" % str(work_order_name))
                return 0

    # 选择指定工单
    def device_select_click_by_id(self, work_order_num):
        for i in range(1, 12):
            choose_box_link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[2]'
            try:
                if self.find_element(choose_box_link_temp).text == str(work_order_num):
                    choose_box_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[1]/label/input'
                    self.click(choose_box_link)
                    logger.info("点击指定工单成功 工单名称:%s" % str(work_order_num))
                    return i
            except:
                logger.info("点击指定工单失败 工单名称:%s" % str(work_order_num))
                return 0

    # 点击新建工单
    def add_click(self):
        qry_link = 'xpath=>//*[@id="btn_addnew"]'
        self.click(qry_link)

    # 是否弹出新建工单弹窗
    def is_prompt_visible_add(self):
        selector = '//*[@id="chuLiMotaiModalLabel1"]'
        ret = self.is_visible(selector)
        logger.info("是否弹出新建工单弹窗%s" % ret)
        return ret

    # 选择姓名，选好之后联系方式也确定了
    def choose_employee_name(self, name):
        sel = self.find_element('xpath=>//*[@id="new_WorkOrderInitiator"]')
        self.wait(0.5)
        # Select(sel).select_by_value('%s' % str(name))
        Select(sel).select_by_visible_text(str(name))

    # 输入单号
    def input_work_order_num_add(self, num):
        link = 'xpath=>//*[@id="new_WorkOrderNumber"]'
        self.type(link, num)

    # 输入工单名称
    def input_work_order_name_add(self, name):
        link = 'xpath=>//*[@id="new_WorkOrderName"]'
        self.type(link, name)

    # 输入概况
    def input_work_order_remark_add(self, remark):
        link = 'xpath=>//*[@id="new_WorkOrderRemark"]'
        self.type(link, remark)

    # 输入工单类型
    def choose_work_order_type_add(self, work_order_type):
        link = 'xpath=>//*[@id="new_WorkOrderType"]'
        sel = self.find_element(link)
        self.wait(0.2)
        Select(sel).select_by_visible_text(str(work_order_type))

    # 输入工单级别
    def choose_work_order_grade_add(self, work_order_grade):
        link = 'xpath=>//*[@id="new_WorkOrderGrade"]'
        sel = self.find_element(link)
        self.wait(0.2)
        Select(sel).select_by_visible_text(str(work_order_grade))

    # 输入概况
    def input_work_order_description_add(self, description):
        link = 'xpath=>//*[@id="new_WorkOrderDescription"]'
        self.type(link, description)

    # '工单号已存在' 工单新增成功
    def save_work_order_cfg_click(self):
        link = 'xpath=>//*[@id="new_baocuo"]'
        self.click(link)
        self.sleep(0.5)

    def close_prompt_click(self):
        link = 'xpath=>//*[@id="chuLiMotai1"]/div/div/div[3]/button[1]'
        self.click(link)

    # 点击工单导出
    def del_click(self):
        qry_link = 'xpath=>//*[@id="btn_shenhe"]'
        self.click(qry_link)

    # 点击导出
    def export_click(self):
        import_link = 'xpath=>//*[@id="btn_export"]'
        self.click(import_link)
        self.sleep(1)

    # 点击工单详情 当只剩下一项的时候，index不需要填写
    # '//*[@id="tb_list"]/tbody/tr[1]/td[11]/a[1]/button'
    def info_click(self, index='0'):
        if str(index) == '0':
            index_str = ''
        else:
            index_str = '[' + str(index) + ']'
        link = 'xpath=>//*[@id="tb_list"]/tbody/tr' + index_str + '/td[11]/a[1]/button'
        try:
            self.click(link)
            logger.info('点击指定工单详情成功')
            return True
        except Exception as e:
            self.get_windows_img()
            logger.error('点击指定工单详情失败:%s', format(e))
            return False

    # 当只剩下一项的时候，index不需要填写
    # '//*[@id="tb_list"]/tbody/tr[1]/td[11]/a[2]/button'
    def deal_click(self, index='0'):
        if str(index) == '0':
            index_str = ''
        else:
            index_str = '[' + str(index) + ']'
        link = 'xpath=>//*[@id="tb_list"]/tbody/tr' + index_str + '/td[11]/a[2]/button'
        try:
            self.click(link)
            logger.info('点击指定工单处理成功')
            return True
        except Exception as e:
            self.get_windows_img()
            logger.error('点击指定工单处理失败:%s', format(e))
            return False

    # 返回1为成功找到唯一指定工单并点击
    def qry_work_order(self, dict_qry):
        self.input_work_order_num(dict_qry['编号'])
        self.input_work_order_name(dict_qry['工单名称'])
        self.input_work_order_owner(dict_qry['工单负责人'])
        self.input_work_order_submitter(dict_qry['工单发起人'])
        self.input_start_time(dict_qry['开始时间'])
        self.input_end_time(dict_qry['结束时间'])
        self.sleep(0.5)
        self.qry_click()
        self.sleep(0.5)
        num = self.get_the_report_num()
        # 直接返回数字，函数调用处进行判断
        # if num == 0:
        #     # self.get_windows_img()
        #     # logger.error('没有找到指定工单', dict_qry)
        #     return num
        if num != 1:
            # self.get_windows_img()
            # logger.error('有多个符合条件的工单存在', dict_qry)
            return num
        link = 'xpath=>//*[@id="tb_list"]/tbody/tr/td[1]/label/input'
        self.click(link)
        logger.info('点击指定工单成功')
        return num

    def add_work_order(self, dict_work_order):
        self.add_click()
        if not self.is_prompt_visible_add():
            self.get_windows_img()
            logger.error('没有弹出新增运维人员弹窗，提示信息：%s' % self.info_text())
            return False
        self.choose_employee_name(dict_work_order['姓名'])
        # 联系方式随姓名带出，不需要自己选择
        self.input_work_order_num_add(dict_work_order['单号'])
        self.input_work_order_name_add(dict_work_order['工单名称'])
        self.input_work_order_remark_add(dict_work_order['概况'])
        self.choose_work_order_type_add(dict_work_order['工单类型'])
        self.choose_work_order_grade_add(dict_work_order['工单级别'])
        self.input_work_order_description_add(dict_work_order['描述'])
        self.sleep(0.2)
        self.save_work_order_cfg_click()
        assert(self.info())
        info = self.info_text()
        if info == dict_work_order['预期结果']:
            logger.info('新增工单结果符合预期：%s' % dict_work_order['预期结果'])
            self.esc_click()
            return True
        else:
            self.get_windows_img()
            logger.error('新增工单结果不符合预期，预期结果：%s,实际结果:%s' %(dict_work_order['预期结果'], info))
            self.esc_click()
            return False

    def del_employee(self, dict_del):
        num = self.qry_work_order(dict_del)
        if 1 != num:
            self.get_windows_img()
            logger.error('无法选择指定工单,num:%s' % num)
            return False
        self.del_click()
        # 前面保证了已经成功选择了工单
        assert self.info_text() == '请选择工单信息进行删除'
        self.sleep(0.5)
        self.enter_click()
        if self.info_text() == '删除成功':
            logger.info('删除指定工单成功')
            self.enter_click()
            return True
        else:
            self.get_windows_img()
            logger.error('删除指定工单失败')
            self.enter_click()
            return False

    # 待写
    def deal_with_work_order(self, dict_qry, dict_mod):
        num = self.qry_work_order(dict_qry)
        if 1 != num:
            self.get_windows_img()
            logger.error('无法选择指定工单,num:%s' % num)
            return False
        self.deal_click()