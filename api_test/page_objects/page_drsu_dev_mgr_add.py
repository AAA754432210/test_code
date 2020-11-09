from api_test.base_page.homepage import HomePage
from common.Log import Logger

logger = Logger("DrsuDevMgrAddPage").getlog()


# 该页面为修改drc设备和新增drc设备共用
class DrsuDevMgrAddPage(HomePage):

    # 填写所属DRC_ID
    def input_drc_id(self, drc_id):
        input_drc_id_link = 'xpath=>//*[@id="ulDrcId"]'
        self.type(input_drc_id_link, str(drc_id))

    # 填写DRSU系统唯一标识
    def input_drsu_id(self, drsu_id):
        input_drsu_id_link = 'xpath=>//*[@id="ulGlobalDrsuId"]'
        self.type(input_drsu_id_link, str(drsu_id))

    # 填写设备名称
    def input_drsu_name(self, drsu_name):
        input_drsu_name_link = 'xpath=>//*[@id="sName"]'
        self.type(input_drsu_name_link, str(drsu_name))

    # 填写drsu的mac地址
    def input_mac_add(self, mac_add):
        input_mac_add_link = 'xpath=>//*[@id="sDrsuMacAddr"]'
        self.type(input_mac_add_link, str(mac_add))

    # 填写前向探测距离
    def input_forward_dist(self, forward_dist):
        input_forward_dist_link = 'xpath=>//*[@id="ulForwardDist"]'
        self.type(input_forward_dist_link, str(forward_dist))

    # 填写后向探测距离
    def input_back_dist(self, back_dist):
        input_back_dist_link = 'xpath=>//*[@id="ulBackDist"]'
        self.type(input_back_dist_link, str(back_dist))

    # 填写GPS坐标 x坐标
    def input_gps_x(self, gps_x):
        gps_x_link = 'xpath=>//*[@id="gpsCoordinateX"]'
        self.type(gps_x_link, str(gps_x))

    # 填写GPS坐标 y坐标
    def input_gps_y(self, gps_y):
        gps_y_link = 'xpath=>//*[@id="gpsCoordinateY"]'
        self.type(gps_y_link, str(gps_y))

    # 填写GPS坐标 z坐标
    def input_gps_z(self, gps_z):
        gps_z_link = 'xpath=>//*[@id="gpsCoordinateZ"]'
        self.type(gps_z_link, str(gps_z))

    # 填写支持最大雷达数
    def input_max_lidar_num(self, lidar_num):
        max_lidar_num_link = 'xpath=>//*[@id="ulMaxLidarNum"]'
        self.type(max_lidar_num_link, str(lidar_num))

    # 填写支持最大摄像头数
    def input_max_camera_num(self, camera_num):
        max_camera_num_link = 'xpath=>//*[@id="ulMaxCameraNum"]'
        self.type(max_camera_num_link, str(camera_num))

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
        submit_save_click_link = 'xpath=>//*[@id="drsuAddnewDevSubmit"]/div[11]/div/button[3]'
        self.click(submit_save_click_link)

    # 点击关闭 提示 新增drsu设备固定参数成功
    def close_window_click(self):
        close_window_link = 'xpath=>//*[@id="idlg_btn_158331self.sixty02074_0"]'
        self.click(close_window_link)

    # dict_drsu = {'所属（上级）DRC_ID': '', 'drsu系统唯一标识': '', '设备名称': '', 'drsu的MAC地址': '','前向探测距离': '',
    # '后向探测距离': '', 'GPS坐标_X坐标': '', 'GPS坐标_Y坐标': '', 'GPS坐标_Z坐标': '',
    # '支持最大的雷达数': '', '支持最大摄像头数': '' }
    def add_drc_dev(self, dict_drsu):
        try:
            self.input_drc_id(dict_drsu['所属（上级）DRC_ID'])
            if dict_drsu['drsu系统唯一标识'] != '':
                self.input_drsu_id(dict_drsu['drsu系统唯一标识'])
            self.input_drsu_name(dict_drsu['设备名称'])
            self.input_mac_add(dict_drsu['drsu的MAC地址'])
            self.input_forward_dist(dict_drsu['前向探测距离'])
            self.input_back_dist(dict_drsu['后向探测距离'])
            self.input_gps_x(dict_drsu['GPS坐标_X坐标'])
            self.input_gps_y(dict_drsu['GPS坐标_Y坐标'])
            self.input_gps_z(dict_drsu['GPS坐标_Z坐标'])
            self.input_max_lidar_num(dict_drsu['支持最大的雷达数'])
            self.input_max_camera_num(dict_drsu['支持最大摄像头数'])
            self.submit_save_click()
            assert(self.info())
            if self.info_text() == '新增DRSU设备固定参数成功':
                logger.info('新增DRSU设备成功')
                self.enter_click() # 回到drsu设备管理页面 esc会继续停留在当前页面
                return True
            else:
                logger.error('新增DRSU设备失败:%s' % (self.info_text()))
                self.get_windows_img()
                self.esc_click()  # 回到drsu设备管理页面
                return False
        except Exception as e:
            logger.error('新增DRSU设备失败:%s' % format(e))
            self.get_windows_img()
            self.esc_click()
            return False