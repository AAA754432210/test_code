from api_test.base_page.homepage import HomePage
from common.Log import Logger
from selenium.webdriver.support.select import Select

logger = Logger("AssetMgrPage").getlog()

class AssetMgrPage(HomePage):

    dict_type = {'DRSU': '1', 'ACU': '2', 'DRC': '3', 'DRCRM': '4', 'PC': '5', '服务器': '6', '交换机': '7', '显示屏': '8'}
    dict_status = {'在用': '1', '在库': '2', '维修中': '3', '报废': '4', '待修': '5', '备用': '6'}

    # 输入资产编号
    def input_asset_num(self, num):
        link = 'xpath=>//*[@id="InventoryCode"]'
        self.type(link, str(num))

    # 选择资产类型 默认全部 1：DRSU 2：ACU 3：DRC 4：DRCRM 5：PC 6：服务器 7：交换机 8：显示屏
    def choose_asset_type(self, asset_type):
        value = self.dict_type[asset_type]
        sel = self.find_element('xpath=>//*[@id="InventoryType"]')
        Select(sel).select_by_value(value)
        self.sleep(0.5)

    # 输入资产状态 缺省：全部 1：在用 2：在库 3:维修中 4：报废 5：待修 6：备用
    def choose_asset_status(self, status):
        value = self.dict_status[status]
        sel = self.find_element('xpath=>//*[@id="InventoryStatus"]')
        self.wait(1)
        Select(sel).select_by_value(value)

    # 点击查询
    def qry_click(self):
        qry_link = 'xpath=>//*[@id="btn_query"]'
        self.click(qry_link)

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
        slect_all_click = 'xpath=>//*[@id="tb_list"]/thead/tr/th[1]/div[1]/label/input'
        self.click(slect_all_click)

    def confirm_click(self):
        confirm_link_text = 'link_text=>确定'
        self.click(confirm_link_text)

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

    # 选择资产
    def device_select_click(self, asset_name):
        for i in range(1, 12):
            choose_box_link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[3]'
            try:
                if self.find_element(choose_box_link_temp).text == str(asset_name):
                    choose_box_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[1]/label/input'
                    self.click(choose_box_link)
                    logger.info("点击指定资产成功 资产名称:%s" % str(asset_name))
                    return i
            except:
                logger.error("点击指定资产失败 资产名称:%s" % str(asset_name))
                return 0

    # 选择指定编号资产
    def device_select_click_by_id(self, asset_num, num):
        for i in range(1, num+1):
            if num == 1:
                txt = ''
            else:
                txt = '[' + str(i) + ']'
            choose_box_link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr' + txt + '/td[2]'
            record_asset_num = self.find_element(choose_box_link_temp).text
            if record_asset_num == str(asset_num):
                choose_box_link = 'xpath=>//*[@id="tb_list"]/tbody/tr' + txt + '/td[1]/label/input'
                self.click(choose_box_link)
                logger.info("点击指定资产成功 资产编号:%s" % str(asset_num))
                return i
        self.get_windows_img()
        logger.error("点击指定资产失败 资产编号:%s" % str(asset_num))
        return 0

    def get_spec_asset_info(self, index):
        asset_dict = {}
        if index == 0:
            txt = ''
        else:
            txt = '[' + str(index) + ']'
        num_link = 'xpath=>//*[@id="tb_list"]/tbody/tr' + txt + '/td[2]'
        name_link = 'xpath=>//*[@id="tb_list"]/tbody/tr' + txt + '/td[3]'
        type_link = 'xpath=>//*[@id="tb_list"]/tbody/tr' + txt + '/td[4]'
        description_link = 'xpath=>//*[@id="tb_list"]/tbody/tr' + txt + '/td[5]'
        status_link = 'xpath=>//*[@id="tb_list"]/tbody/tr' + txt + '/td[6]'
        asset_dict['资产编号'] = self.find_element(num_link).text
        asset_dict['资产名称'] = self.find_element(name_link).text
        asset_dict['资产类型'] = self.find_element(type_link).text
        asset_dict['资产概况'] = self.find_element(description_link).text
        asset_dict['资产状态'] = self.find_element(status_link).text
        return asset_dict

    def get_spec_asset_info_detail(self):
        asset_dict = {}
        num_link = 'xpath=>//*[@id="xq_InventoryCode"]'
        name_link = 'xpath=>//*[@id="xq_InventoryName"]'
        type_link = 'xpath=>//*[@id="xq_InventoryType"]'
        description_link = 'xpath=>//*[@id="xq_InventoryDescription"]'
        status_link = 'xpath=>//*[@id="xq_InventoryStatus"]'
        remarks_link = 'xpath=>//*[@id="xq_InventoryRemark"]'

        asset_dict['资产编号'] = self.get_value(num_link)
        asset_dict['资产名称'] = self.get_value(name_link)
        asset_dict['资产类型'] = self.get_value(type_link)
        asset_dict['资产概况'] = self.get_value(description_link)
        asset_dict['资产状态'] = self.get_value(status_link)
        asset_dict['备注'] = self.get_value(remarks_link)
        return asset_dict

    # 点击新建资产
    def add_click(self):
        add_link = 'xpath=>//*[@id="btn_addnew"]'
        self.click(add_link)

    # 是否弹出新增资产弹窗
    def is_prompt_visible_add(self):
        selector = '//*[@id="updateZiChanMotaiModalLabel1"]'
        ret = self.is_visible(selector)
        logger.info("是否弹出新增资产弹窗%s" % ret)
        return ret

    # 输入资产编号
    def input_asset_num_add(self, num):
        asset_num_link = 'xpath=>//*[@id="new_InventoryCode"]'
        self.type(asset_num_link, num)

    # 输入资产名称
    def input_asset_name_add(self, name):
        asset_name_link = 'xpath=>//*[@id="new_InventoryName"]'
        self.type(asset_name_link, name)

    # 选择资产类型
    def select_asset_type_add(self, asset_type):
        value = self.dict_type[asset_type]
        sel = self.find_element('xpath=>//*[@id="new_InventoryType"]')
        Select(sel).select_by_value(value)
        self.sleep(0.5)

    # 输入资产概况
    def input_asset_description_add(self, info):
        asset_description_link = 'xpath=>//*[@id="new_InventoryDescription"]'
        self.type(asset_description_link, info)

    # 选择资产状态
    def select_asset_status_add(self, asset_status):
        value = self.dict_status[asset_status]
        sel = self.find_element('xpath=>//*[@id="new_InventoryStatus"]')
        Select(sel).select_by_value(value)
        self.sleep(0.5)

    # 输入备注
    def input_asset_remarks_add(self, remarks):
        asset_remarks_link = 'xpath=>//*[@id="new_InventoryRemark"]'
        self.type(asset_remarks_link, remarks)

    # 点击确认
    def save_assert_cfg_click(self):
        link = 'xpath=>//*[@id="new_baocun"]'
        self.click(link)

    # 点击关闭
    def close_window_click(self):
        link = 'xpath=>//*[@id="updateZiChanMotai1"]/div/div/div[3]/button[1]'
        self.click(link)

    # 点击导入资产信息
    def import_click(self):
        import_link = 'xpath=>//*[@id="btn_import"]'
        self.click(import_link)
        self.sleep(1)

    # 点击导出资产信息
    def export_click(self):
        export_link = 'xpath=>//*[@id="btn_export"]'
        self.click(export_link)
        self.sleep(1)

    # 点击删除资产
    def del_click(self):
        qry_link = 'xpath=>//*[@id="btn_baofei"]'
        self.click(qry_link)

    # 点击资产详情 当只剩下一项的时候，index不需要填写
    # '//*[@id="tb_list"]/tbody/tr[1]/td[7]/a[1]/button'
    def info_click(self, index=0):
        if str(index) == '0':
            index_str = ''
        else:
            index_str = '[' + str(index) + ']'
        link = 'xpath=>//*[@id="tb_list"]/tbody/tr' + index_str + '/td[7]/a[1]/button'
        try:
            self.click(link)
            logger.info('点击指定资产详情成功')
            return True
        except Exception as e:
            self.get_windows_img()
            logger.error('点击指定资产详情失败:%s', format(e))
            return False

    # 当只剩下一项的时候，index不需要填写
    # '//*[@id="tb_list"]/tbody/tr[1]/td[7]/a[2]/button'
    def mod_click(self, index=0):
        if str(index) == '0':
            index_str = ''
        else:
            index_str = '[' + str(index) + ']'
        link = 'xpath=>//*[@id="tb_list"]/tbody/tr' + index_str + '/td[7]/a[2]/button'
        try:
            self.click(link)
            logger.info('点击指定资产编辑成功')
            return True
        except Exception as e:
            self.get_windows_img()
            logger.error('点击指定资产编辑失败:%s', format(e))
            return False

    # 是否弹出资产修改弹窗
    def is_prompt_visible_mod(self):
        selector = '//*[@id="updateZiChanMotaiModalLabel"]'
        ret = self.is_visible(selector)
        logger.info("是否弹出资产修改弹窗%s" % ret)
        return ret

    # 输入资产编号
    def input_asset_num_mod(self, num):
        asset_num_link = 'xpath=>//*[@id="up_InventoryCode"]'
        self.type(asset_num_link, num)

    # 输入资产名称
    def input_asset_name_mod(self, name):
        asset_name_link = 'xpath=>//*[@id="up_InventoryName"]'
        self.type(asset_name_link, name)

    # 选择资产类型
    def select_asset_type_mod(self, asset_type):
        print(asset_type)
        value = self.dict_type[asset_type]
        sel = self.find_element('xpath=>//*[@id="up_InventoryType"]')
        Select(sel).select_by_value(value)
        self.sleep(0.5)

    # 输入资产概况
    def input_asset_description_mod(self, info):
        asset_description_link = 'xpath=>//*[@id="up_InventoryDescription"]'
        self.type(asset_description_link, info)

    # 选择资产状态
    def select_asset_status_mod(self, asset_status):
        value = self.dict_status[asset_status]
        sel = self.find_element('xpath=>//*[@id="up_InventoryStatus"]')
        Select(sel).select_by_value(value)
        self.sleep(0.5)

    # 输入备注
    def input_asset_remarks_mod(self, remarks):
        asset_remarks_link = 'xpath=>//*[@id="up_InventoryRemark"]'
        self.type(asset_remarks_link, remarks)

    # 点击修改
    def save_mod_assert_cfg_click(self):
        link = 'xpath=>//*[@id="up_baocun"]'
        self.click(link)

    # 点击关闭
    def close_window_click_mod(self):
        link = 'xpath=>//*[@id="updateZiChanMotai"]/div/div/div[3]/button[1]'
        self.click(link)

    # flag = True 新增 flag=False 修改
    def set_asset_commom(self, dict_asset):
        self.input_asset_num_add(dict_asset['资产编号'])
        self.input_asset_name_add(dict_asset['资产名称'])
        self.select_asset_type_add(dict_asset['资产类型'])
        self.input_asset_description_add(dict_asset['资产概况'])
        self.select_asset_status_add(dict_asset['资产状态'])
        self.input_asset_remarks_add(dict_asset['备注'])
        self.save_assert_cfg_click()
        self.sleep(0.2)
        assert (self.info())
        info = self.info_text()
        if info == dict_asset['预期结果']:
            self.esc_click()
            self.esc_click()
            logger.info('配置结果与预期结果一致：%s' % dict_asset['预期结果'])
            return True
        else:
            self.get_windows_img()
            logger.error('配置结果与预期结果不一致，预期结果：%s，配置结果：%s' % (dict_asset['预期结果'], info))
            return False

    # 新增资产 '资产新增成功' 保存按钮：//*[@id="new_baocun"] 编号：//*[@id="new_InventoryCode"] title：//*[@id="updateZiChanMotaiModalLabel1"]
    def add_asset(self, dict_asset):
        self.add_click()
        assert(self.is_prompt_visible_add())
        self.input_asset_num_add(dict_asset['资产编号'])
        self.input_asset_name_add(dict_asset['资产名称'])
        self.select_asset_type_add(dict_asset['资产类型'])
        self.input_asset_description_add(dict_asset['资产概况'])
        self.select_asset_status_add(dict_asset['资产状态'])
        self.input_asset_remarks_add(dict_asset['备注'])
        self.save_assert_cfg_click()
        self.sleep(0.2)
        assert (self.info())
        info = self.info_text()
        if info == dict_asset['预期结果']:
            self.esc_click()
            self.esc_click()
            logger.info('配置结果与预期结果一致：%s' % dict_asset['预期结果'])
            return True
        else:
            self.get_windows_img()
            logger.error('配置结果与预期结果不一致，预期结果：%s，配置结果：%s' % (dict_asset['预期结果'], info))
            return False

    # '资产修改成功' 修改按钮：//*[@id="up_baocun"] 编号：//*[@id="up_InventoryCode"] title：//*[@id="updateZiChanMotaiModalLabel"]
    def mod_asset(self, dict_asset):
        index = self.qry_asset(dict_asset['资产编号'])
        if index == 0:
            return False
        self.mod_click()
        self.sleep(10)
        assert (self.is_prompt_visible_mod())
        # self.input_asset_num_mod(dict_asset['资产编号'])
        self.input_asset_name_mod(dict_asset['资产名称'])
        self.select_asset_type_mod(dict_asset['资产类型'])
        self.input_asset_description_mod(dict_asset['资产概况'])
        self.select_asset_status_mod(dict_asset['资产状态'])
        self.input_asset_remarks_mod(dict_asset['备注'])
        self.save_mod_assert_cfg_click()
        self.sleep(0.2)
        assert (self.info())
        info = self.info_text()
        if info == dict_asset['预期结果']:
            self.esc_click()
            self.esc_click()
            logger.info('配置结果与预期结果一致：%s' % dict_asset['预期结果'])
            return True
        else:
            self.get_windows_img()
            logger.error('配置结果与预期结果不一致，预期结果：%s，配置结果：%s' % (dict_asset['预期结果'], info))
            return False

    def assert_spec_asset(self, dict_asset):
        num = self.get_the_report_num()
        if num == 0:
            logger.info('没有找到任何资产记录')
            return False
        index = self.device_select_click_by_id(dict_asset['资产编号'], num)
        if index == 0:
            logger.info('没有找到指定资产编号的资产记录')
            return False
        record_dict_asset = self.get_spec_asset_info(index)
        for k in record_dict_asset:
            if record_dict_asset[k] != dict_asset[k]:
                logger.error('查询指定编号资产数据与配置数据不一致，配置数据：%s,查询数据：%s' % (dict_asset, record_dict_asset))
                return False
        logger.info('查询到配置数据完全一致的资产数据：%s', dict_asset)
        return True

    def assert_spec_asset_detail(self, dict_asset):
        num = self.get_the_report_num()
        if num == 0:
            logger.info('没有找到任何资产记录')
            return False
        index = self.device_select_click_by_id(dict_asset['资产编号'], num)
        if index == 0:
            logger.info('没有找到指定资产编号的资产记录')
            return False
        if num == 1:
            self.info_click()
        else:
            self.info_click(index)
        record_dict_asset = self.get_spec_asset_info_detail()
        for k in record_dict_asset:
            if record_dict_asset[k] != dict_asset[k]:
                logger.error('查询指定编号资产数据与配置数据不一致，配置数据：%s,查询数据：%s' % (dict_asset, record_dict_asset))
                return False
        logger.info('查询到配置数据完全一致的资产数据：%s', dict_asset)
        return True

    def qry_asset(self, asset_num):
        self.input_asset_num(asset_num)
        self.qry_click()
        self.sleep(0.2)
        num = self.get_the_report_num()
        if num == 0:
            logger.error('没有找到指定资产编号：%s资产' % asset_num)
            self.get_windows_img()
            return 0
        elif num != 1:
            logger.error('查询到多个结果，请输入精确资产编号')
            self.get_windows_img()
            return 0
        else:
            index = self.device_select_click_by_id(asset_num, num)
            return index

    def del_asset(self, dict_asset):
        if self.qry_asset(dict_asset['资产编号']) == 0:
            return False
        self.sleep(10)
        self.del_click()
        if self.info_text() == '确定删除选定资产信息':
            self.sleep(2)
            self.confirm_click()
            # self.enter_click()
            # self.esc_click()
            self.sleep(2)
            assert (self.info())
            if self.info_text() == '删除成功':
                self.sleep(2)
                self.enter_click()
                logger.info('资产删除成功')
                return True
        else:
            self.get_windows_img()
            logger.error('资产删除失败%s' % (self.info_text()))
            self.esc_click()
            return False

    def del_batch_asset(self):
        self.del_click()
        if self.info_text() == '确定删除选定资产信息':
            self.sleep(2)
            self.confirm_click()
            # self.enter_click()
            # self.esc_click()
            self.sleep(2)
            assert (self.info())
            if self.info_text() == '删除成功':
                self.sleep(2)
                self.enter_click()
                logger.info('资产删除成功')
                return True
        else:
            self.get_windows_img()
            logger.error('资产删除失败%s' % (self.info_text()))
            self.esc_click()
            return False

    def del_all_asset(self):
        self.all_election_click()
        self.sleep(2)
        self.del_click()
        self.sleep(2)
        if self.info_text() == '确定删除选定资产信息':
            self.sleep(10)
            self.confirm_click()
            # self.enter_click()
            # self.esc_click()
            self.sleep(10)
            assert (self.info())
            if self.info_text() == '删除成功':
                self.sleep(2)
                self.enter_click()
                logger.info('资产删除成功')
                return True
        else:
            self.get_windows_img()
            logger.error('资产删除失败%s' % (self.info_text()))
            self.esc_click()
            return False

    def chooselist(self, listid):
        if listid == 0:
            list_link = 'xpath=>//*[@id="tb_list"]/tbody/tr/td[1]/label/input'
        else:
            list_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(listid) + ']/td[1]/label/input'
        self.click(list_link)

    def qry_result_check_no(self, dict_asset):
        num = self.get_the_report_num()
        if num == 0:
            logger.info('没有找到任何资产记录')
            return False
        for i in range(1, num+1):
            if num == 1:
                txt = ''
            else:
                txt = '[' + str(i) + ']'
            link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr' + txt + '/td[2]'
            record_asset_num = self.find_element(link_temp).text
            if record_asset_num.find(dict_asset['资产编号']) < 0:
                self.get_windows_img()
                return False
        return True

    def qry_result_check_type(self, dict_asset):
        num = self.get_the_report_num()
        if num == 0:
            logger.info('没有找到任何资产记录')
            return False
        for i in range(1, num+1):
            if num == 1:
                txt = ''
            else:
                txt = '[' + str(i) + ']'
            link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr' + txt + '/td[4]'
            record_asset_type = self.find_element(link_temp).text
            if record_asset_type.find(dict_asset['资产类型']) < 0:
                self.get_windows_img()
                return False
        return True

    def qry_result_check_status(self, dict_asset):
        num = self.get_the_report_num()
        if num == 0:
            logger.info('没有找到任何资产记录')
            return False
        for i in range(1, num+1):
            if num == 1:
                txt = ''
            else:
                txt = '[' + str(i) + ']'
            link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr' + txt + '/td[6]'
            record_asset_status = self.find_element(link_temp).text
            if record_asset_status.find(dict_asset['资产状态']) < 0:
                self.get_windows_img()
                return False
        return True

    def qry_result_check_all(self, dict_asset):
        num = self.get_the_report_num()
        if num == 0:
            logger.info('没有找到任何资产记录')
            return False
        for i in range(1, num+1):
            if num == 1:
                txt = ''
            else:
                txt = '[' + str(i) + ']'
            link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr' + txt + '/td[2]'
            record_asset_num = self.find_element(link_temp).text
            link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr' + txt + '/td[4]'
            record_asset_type = self.find_element(link_temp).text
            link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr' + txt + '/td[6]'
            record_asset_status = self.find_element(link_temp).text
            if record_asset_num.find(dict_asset['资产编号']) < 0 or record_asset_type.find(dict_asset['资产类型']) < 0 or record_asset_status.find(dict_asset['资产状态']) < 0:
                self.get_windows_img()
                return False
        return True
