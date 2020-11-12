# -*- coding: utf-8 -*-
"""
@Project : test_code
@File    : analysis_drsu.py
@Author  : 王白熊
@Data    ： 2020/11/10 16:36
"""
import os
import pandas as pd
from pandas import DataFrame
import numpy as np
from glob import glob
from common.Log import Logger
import matplotlib.pyplot as plt
from project.data_analysis.constant import const
from project.data_analysis.analysis_drsu_single import TrackDrsu
from project.data_analysis.analysis_acu import TrackAcu

plt.rcParams['font.sans-serif'] = ['SimHei']  # 正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

Listcolors = ['red', 'blue', 'green', 'cyan', 'magenta', 'orange', 'darkred', 'black']

logger = Logger('DrsuScence').getlog()


# drsu 场景，由多个track_id组成
class DrsuScence(object):
    def __init__(self, file_path, acu_file, ort=True):
        """
        :param file_path: drsu路径，到obs_data_trackid这一层
        :param ort:摄像机朝向是否为x方向
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError('drsu数据文件夹:%s不存在' % file_path)
        if not os.path.exists(acu_file):
            raise FileNotFoundError('acu数据文件:%s不存在' % acu_file)
        self.drsu_path = file_path
        self.acu_track = TrackAcu(acu_file, ort=ort)
        self._ort = ort
        self.df = DataFrame()
        self.bk_df = DataFrame()
        # self.match_type = const.MATCH_TYPE_NOT
        # 分别记录不同类别的匹配程度 0为完全匹配。下标index分别为0：障碍物类型
        self.match_list = [0] * 10
        self.obj_jump = 1
        self.fig = None
        self.ax = [None] * 9

    # 获取场景下所有trackid的特征DataFrame
    def get_drsu_data(self):
        files = glob(os.path.join(self.drsu_path, '*.csv'))
        if not files:
            logger.error('文件夹：%s中不存在csv文件' % self.drsu_path)
            exit(0)
        for i in files:
            # 文件记录小于10条的认为无效数据直接丢弃
            if os.path.getsize(i) < const.CSV_SIZE_MIN:
                continue
            track = TrackDrsu(i)
            # 遍历获取track_id的特征信息,并全部放入一个DataFrame中
            track_info = track.track_info
            track_info['file_name'] = [i]
            self.df = self.df.append(track_info, ignore_index=True)
            self.bk_df = self.df

    # 记录两个DataFrame 一个为原始DataFrame，一个作为处理后的DataFrame，
    # flag标识是否基于原始DataFrame进行操作
    # 获取指定状态的轨迹
    def get_track_by_track_type(self, track_type):
        bk_df_ = self.bk_df.loc[self.bk_df.track_type == track_type]
        if not bk_df_.empty:
            logger.info('按轨迹类型trackid成功')
            self.bk_df = bk_df_
        else:
            logger.info('按轨迹类型trackid失败')

    # 获取坐标处于一定范围内的轨迹
    def get_track_by_center(self, center, distance):
        bk_df_ = self.bk_df.loc[(self.bk_df.center_x > center[0] - distance[0]) &
                                (self.bk_df.center_x < center[0] + distance[0]) &
                                (self.bk_df.center_y > center[1] - distance[0]) &
                                (self.bk_df.center_y < center[1] + distance[0])]
        if not bk_df_.empty:
            logger.info('按坐标筛选trackid成功')
            self.bk_df = bk_df_
        else:
            logger.info('按坐标筛选trackid失败')

    # 获取坐标处于一定范围内的轨迹
    def get_track_by_speed(self, speed, speed_diff):
        bk_df_ = self.bk_df.loc[(self.bk_df.speed_x > speed[0] - speed_diff[0]) &
                                (self.bk_df.speed_x < speed[0] + speed_diff[0]) &
                                (self.bk_df.speed_y > speed[1] - speed_diff[0]) &
                                (self.bk_df.speed_y < speed[1] + speed_diff[0])]
        if not bk_df_.empty:
            logger.info('按速度筛选trackid成功')
            self.bk_df = bk_df_
        else:
            logger.info('按速度筛选trackid失败')

    # 获取指定障碍物类型的轨迹
    def get_track_by_obj_type(self, obj_type, bk_obj_type):
        bk_df_ = self.bk_df.loc[self.bk_df.obj_type == obj_type]
        if not bk_df_.empty:
            logger.info('障碍物类型匹配成功')
            self.bk_df = bk_df_
            self.match_list[0] = const.MATCH_TYPE_MAIN
        bk_df_ = self.bk_df.loc[self.bk_df.obj_type == bk_obj_type]
        if not bk_df_.empty:
            logger.info('障碍物类型（相似类型）匹配成功')
            self.bk_df = bk_df_
            self.match_list[0] = const.MATCH_TYPE_BACK_UP
        logger.info('障碍物类型（相似类型）匹配失败')

    # 用体积对track进行筛选
    def get_track_by_obj_volume(self, volume=const.VOLUME_CAR):
        bk_df_ = self.bk_df.loc[self.bk_df.volume > volume]
        if not bk_df_.empty:
            logger.info('按体积筛选成功')
            self.bk_df = bk_df_
        else:
            logger.info('按体积筛选失败')

    # 按帧数筛选
    def find_main_track_id_by_frame_num(self):
        frame_num = self.bk_df['frame_num'].max() // 2
        bk_df_ = self.bk_df.loc[self.bk_df.frame_num > frame_num]
        if not bk_df_.empty:
            logger.info('按帧数筛选成功')
            self.bk_df = bk_df_
        else:
            logger.info('按帧数筛选失败')

    # 按拟合直线斜率和拟合优度进行选择
    def find_main_track_id_by_popt(self):
        popt, r_square = self.acu_track.check_stright_fit()
        bk_df_ = self.bk_df.loc[self.bk_df.frame_num > r_square - const.R_SQUARE_THRESHOLD]
        if not bk_df_.empty:
            logger.info('按拟合优度筛选成功')
            self.bk_df = bk_df_
        else:
            logger.info('按拟合优度筛选失败')

    # 对dataframe进行排序 attr为一个列表，可以有多个排序依据
    def sort_track_by_attr(self, attr):
        self.bk_df = self.bk_df.sort_values(axis=0, ascending=False, by=attr)

    # 静态情况下判断两条轨迹是否为相同障碍物，主要是看坐标是否基本一致
    def check_main_track_id_static(self):
        if self.bk_df.shape[0] > 2:
            logger.warning('存在大于两个满足条件的track_id存在,增加判断')
        if int(abs(self.bk_df.loc[0, :].center_x - self.bk_df.loc[1, :].center_x)) > 2 or \
                int(abs(self.bk_df.loc[0, :].center_y - self.bk_df.loc[1, :].center_y)) > 2:
            logger.warning('同在两个满足条件的track_id，且坐标相差巨大，判定不是相同障碍物，请增加判断')

    def check_main_track_id_straight(self):
        pass

    def find_main_track_id_static(self):
        self.get_track_by_track_type(const.TRACK_STATIC)
        # 搜索范围和 drsu横杆与acu相距距离成正比
        distance = [
            (self.acu_track.center - const.CENTER_DRSU_3[0]) * const.SEARCH_DISTANCE_RATE + const.BASE_SEARCH_DISTANCE,
            (self.acu_track.center - const.CENTER_DRSU_3[0]) * const.SEARCH_DISTANCE_RATE + const.BASE_SEARCH_DISTANCE]
        self.get_track_by_center(self.acu_track.center, distance)
        self.get_track_by_obj_type(const.OBJ_TYPE_BUS, const.OBJ_TYPE_CAR)
        # 只有在类型识别正确的情况下保留认为是跳变，保留多个track
        if self.match_list[0] == const.MATCH_TYPE_MAIN:
            self.obj_jump = self.bk_df.shape[0]
            return
        # 在类型没有完全匹配的情况下 按照体积进行筛选
        self.get_track_by_obj_volume()
        self.find_main_track_id_by_frame_num()

    def find_main_track_id_straight(self):
        # 直行轨迹先筛选出轨迹类型为直行的track_id
        self.get_track_by_track_type(const.TRACK_STRAIGHT)
        self.get_track_by_speed(self.acu_track.speed,
                                [i * const.SEARCH_SPEED_RATE + const.BASE_SEARCH_SPEED for i in self.acu_track.speed])
        self.find_main_track_id_by_popt()
        self.get_track_by_obj_type(const.OBJ_TYPE_BUS, const.OBJ_TYPE_CAR)
        # 只有在类型识别正确的情况下保留认为是跳变，保留多个track
        if self.match_list[0] == const.MATCH_TYPE_MAIN:
            self.obj_jump = self.bk_df.shape[0]
            return
        # 在类型没有完全匹配的情况下 按照体积进行筛选
        self.get_track_by_obj_volume()
        self.find_main_track_id_by_frame_num()

    # 更加acu上报的轨迹数据去寻找drsu识别出来的目标轨迹
    def find_main_track_id(self):
        if self.df.empty:
            self.get_drsu_data()
        if self.acu_track.track_type == const.TRACK_STATIC:
            # 先寻找轨迹类型为静止
            self.find_main_track_id_static()
        elif self.acu_track.track_type == const.TRACK_STRAIGHT:
            self.find_main_track_id_straight()

    # 检查目标轨迹
    def check_main_track_id(self):
        # 经过筛选之后只剩下一个track 不用处理
        if self.bk_df.shape[0] == 1:
            return
        if self.match_list[0] != const.MATCH_TYPE_MAIN:
            self.bk_df = self.bk_df.iloc[0, :]
            return
        if self.acu_track.track_type == const.TRACK_STATIC:
            self.check_main_track_id_static()
        elif self.acu_track.track_type == const.TRACK_STRAIGHT:
            self.check_main_track_id_straight()

    def draw_static_sub(self, is_show=False):
        for i in range(self.bk_df.shape[0]):
            df = round(pd.read_csv(self.bk_df.iloc[i].file_name), 1)
            df['Timestamp'] = (df['dbTimestamp'] - df.iloc[0, :].dbTimestamp) * 10
            time_stamp = df['Timestamp'][df.shape[0]]
            track_id = self.bk_df.iloc[i].track_id
            count_dict = [2, 1, 2, 1]
            dict_x = [df.Timestamp, df.Timestamp, df.Timestamp, np.arange(time_stamp)]
            dict_y = [[abs(df['stCenter.dbx'] - self.acu_track.center[0]),
                       abs(df['stCenter.dby'] - self.acu_track.center[1])],
                      [df.stObj_type],
                      [df.dbwidth * df.dbheight, [const.VOLUME_BUS for _ in range(drsu_data.shape[0])]],
                      [[1 if i in df.Timestamp else 0 for i in range(time_stamp)]]]
            dict_x_ticks = [None, None, None, np.arange(0, time_stamp + 100, 100)]
            dict_y_ticks = [None, np.arange(3, 11), None, [1, 2]]
            dict_label = [['纵向位置偏差track_id:{}'.format(track_id), '横向位置偏差track_id:{}'.format(track_id)],
                          ['障碍物类型'],
                          ['障碍物面积(与摄像头方向正视面)', '小巴车实际面积'],
                          ]
            for i in range(4):
                self.ax[i].plot(dict_x[i], dict_y[i][0], Listcolors[i], label=dict_label[i][0])
                self.ax[i].set_xticks(dict_x_ticks[i])
                self.ax[i].set_yticks(dict_y_ticks[i])
                if count_dict[i] > 1:
                    self.ax[i].plot(dict_x[i], dict_y[i][1], Listcolors[i], label=dict_label[i][1])
                self.ax[i].legend(loc='best', borderaxespad=0)

    def draw_static(self, is_show=False):
        image_path = os.path.dirname(self.drsu_path)
        title = ''.join(self.drsu_path.split('\\')[-2:-1])
        image_name = os.path.join(image_path, title + 'parsed.png')
        print(image_name)
        dict_title = ['纵/横向偏差图', '识别类型变化图', '障碍物面积变化图', '有效帧占比图']
        dict_y_label = ['acu实际与识别坐标偏差(m)', '障碍物识别类型', '障碍物识别面积(平米)', '障碍物识别有效帧']
        self.fig = plt.figure(figsize=(18, 10))
        for i in range(4):
            ax = self.fig.add_subplot(2, 2, i + 1)
            ax.set(title=dict_title[i], ylabel=dict_y_label[i], )
            self.ax[i] = ax
        self.draw_static_sub()
        plt.savefig(image_name)
        if is_show:
            plt.show()
            plt.pause(0.1)
        plt.close()
        self.fig = None
        self.ax = [None] * 9

if __name__ == '__main__':
    drsu_file = r'D:\data\drsu03场景\group1\group1_position01\obs_data_trackid'
    acu_file = r'D:\data\drsu03场景\group1\group1_position01\static_parsed.csv'
    a = DrsuScence(drsu_file, acu_file)
    a.find_main_track_id()
    a.check_main_track_id()
    a.draw_static()