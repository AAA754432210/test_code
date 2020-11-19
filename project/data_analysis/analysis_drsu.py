# -*- coding: utf-8 -*-
"""
@Project : test_code
@File    : analysis_drsu.py
@Author  : 王白熊
@Data    ： 2020/11/10 16:36
"""
import os
import time
import math
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
List_style = ['-', '--', '-.', ':']
logger = Logger('DrsuScene').getlog()


# drsu 场景，由多个track_id组成
class DrsuScene(object):
    def __init__(self, file_path, ort=True, use_time=False):
        """
        :param file_path: drsu路径，到obs_data_trackid这一层
        :param ort:摄像机朝向是否为x方向
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError('drsu数据文件夹:%s不存在' % file_path)
        self.data_path = file_path
        self.acu_track = TrackAcu(os.path.join(file_path, 'acu_data'), ort=ort)
        self._ort = ort
        self.df = DataFrame()
        self.bk_df = DataFrame()
        # self.match_type = const.MATCH_TYPE_NOT
        # 分别记录不同类别的匹配程度 0为完全匹配。下标index分别为0：障碍物类型
        self.match_list = [0] * 10
        self.obj_jump = 1
        self.fig = None
        self.ax = [None] * 9
        self.draw_flag = False
        self.use_time = use_time
        logger.info('对文件夹{}进行分析'.format(file_path))

    # 获取场景下所有trackid的特征DataFrame
    def get_drsu_data(self):
        drsu_path = os.path.join(self.data_path, 'obs_data_trackid')
        files = glob(os.path.join(drsu_path, '*.csv'))
        if not files:
            logger.error('文件夹：%s中不存在csv文件' % drsu_path)
            exit(0)
        for i in files:
            # 文件记录小于10条的认为无效数据直接丢弃
            if os.path.getsize(i) < const.CSV_SIZE_MIN:
                continue
            track = TrackDrsu(i)
            # 遍历获取track_id的特征信息,并全部放入一个DataFrame中
            track_info = track.track_info
            # track_info['file_name'] = i
            self.df = self.df.append(track_info, ignore_index=True)
            self.bk_df = self.df

    # 记录两个DataFrame 一个为原始DataFrame，一个作为处理后的DataFrame，
    # flag标识是否基于原始DataFrame进行操作
    # 获取指定状态的轨迹
    def get_track_by_track_type(self, track_type):
        bk_df_ = self.bk_df.loc[self.bk_df.track_type == track_type]
        if not bk_df_.empty:
            logger.info('按轨迹类型1筛选trackid成功')
            self.bk_df = bk_df_
        else:
            logger.info('按轨迹类型1筛选trackid失败')

    # 获取坐标处于一定范围内的轨迹
    def get_track_by_center(self):
        distance = [
            (self.acu_track.center[0] - const.CENTER_DRSU_3[
                0]) * const.SEARCH_DISTANCE_RATE + const.BASE_SEARCH_DISTANCE,
            (self.acu_track.center[1] - const.CENTER_DRSU_3[
                1]) * const.SEARCH_DISTANCE_RATE + const.BASE_SEARCH_DISTANCE]
        bk_df_ = self.bk_df.loc[(self.bk_df.center_x > self.acu_track.center[0] - distance[0]) &
                                (self.bk_df.center_x < self.acu_track.center[0] + distance[0]) &
                                (self.bk_df.center_y > self.acu_track.center[1] - distance[0]) &
                                (self.bk_df.center_y < self.acu_track.center[1] + distance[0])]
        if not bk_df_.empty:
            logger.info('按坐标筛选trackid成功')
            self.bk_df = bk_df_
        else:
            logger.info('按坐标筛选trackid失败')

    # 获取坐标处于一定范围内的轨迹
    def get_track_by_speed(self):
        speed_diff = [abs(i * const.SEARCH_SPEED_RATE) + const.BASE_SEARCH_SPEED for i in self.acu_track.speed]
        bk_df_ = self.bk_df.loc[(self.bk_df.speed_x > self.acu_track.speed[0] - speed_diff[0]) &
                                (self.bk_df.speed_x < self.acu_track.speed[0] + speed_diff[0]) &
                                (self.bk_df.speed_y > self.acu_track.speed[1] - speed_diff[1]) &
                                (self.bk_df.speed_y < self.acu_track.speed[1] + speed_diff[1])]
        if not bk_df_.empty:
            logger.info('按速度%s正负%s筛选trackid成功' % (self.acu_track.speed, speed_diff))
            self.bk_df = bk_df_
        else:
            logger.info('按速度%s正负%s筛选trackid失败' % (self.acu_track.speed, speed_diff))

    # 获取坐标处于一定范围内的轨迹
    def get_track_by_timestamp(self):
        time_stamp = self.acu_track.get_time_stamp()
        bk_df_ = self.bk_df.loc[(self.bk_df.start_time > time_stamp[0]) &
                                (self.bk_df.end_time < time_stamp[1])]
        if not bk_df_.empty:
            logger.info('按时间戳:%s筛选trackid成功' % time_stamp)
            self.bk_df = bk_df_
        else:
            logger.info('按时间戳:%s筛选trackid失败' % time_stamp)

    # 获取指定障碍物类型的轨迹
    def get_track_by_obj_type(self, obj_type, bk_obj_type):
        bk_df_ = self.bk_df.loc[self.bk_df.obj_type == obj_type]
        if not bk_df_.empty:
            logger.info('障碍物类型匹配成功')
            self.bk_df = bk_df_
            self.match_list[0] = const.MATCH_TYPE_MAIN
            return
        bk_df_ = self.bk_df.loc[self.bk_df.obj_type == bk_obj_type]
        if not bk_df_.empty:
            logger.info('障碍物类型（相似类型）匹配成功')
            self.bk_df = bk_df_
            self.match_list[0] = const.MATCH_TYPE_BACK_UP
            return
        logger.info('障碍物类型匹配失败')

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
            logger.info('按帧数:%s筛选成功' % frame_num)
            self.bk_df = bk_df_
        else:
            logger.info('按帧数:%s筛选失败' % frame_num)

    # 按拟合直线斜率和拟合优度进行选择
    def find_main_track_id_by_popt(self):
        popt, r_square = self.acu_track.check_stright_fit()
        bk_df_ = self.bk_df.loc[self.bk_df.r_square > r_square - const.R_SQUARE_THRESHOLD]
        if not bk_df_.empty:
            logger.info('按拟合优度:%s范围%s筛选成功' % (r_square, const.R_SQUARE_THRESHOLD))
            self.bk_df = bk_df_
        else:
            logger.info('按拟合优度:%s范围%s筛选失败' % (r_square, const.R_SQUARE_THRESHOLD))

    # 对dataframe进行排序 attr为一个列表，可以有多个排序依据
    def sort_track_by_attr(self, attr):
        self.bk_df = self.bk_df.sort_values(axis=0, ascending=False, by=attr)

    # 静态情况下判断两条轨迹是否为相同障碍物，主要是看坐标是否基本一致
    def check_main_track_id_static(self):
        if self.bk_df.shape[0] > 2:
            logger.warning('存在大于两个满足条件的track_id存在,增加判断')
        if int(abs(self.bk_df.iloc[0, :].center_x - self.bk_df.iloc[1, :].center_x)) > 2 or \
                int(abs(self.bk_df.iloc[0, :].center_y - self.bk_df.iloc[1, :].center_y)) > 2:
            logger.warning('同在两个满足条件的track_id，且坐标相差巨大，判定不是相同障碍物，请增加判断')

    def check_main_track_id_straight(self):
        pass

    # 暂时只支持两个track合并,合并两个track的特征用于整体分析图
    def merge_track_static(self):
        if self.acu_track.track_type != 0:
            return
        if self.bk_df.shape[0] < 2:
            logger.info('track数量小于2，无需融合')
            return self.bk_df.iloc[0]
        if self.bk_df.shape[0] > 2:
            logger.warning('不支持两个以上的track合并')
            return self.bk_df.iloc[0]
        pf1 = TrackDrsu(self.bk_df.iloc[0].file_name)
        pf2 = TrackDrsu(self.bk_df.iloc[1].file_name)
        pf_new = pf1 + pf2
        return pf_new.calc_track_info()

    def find_main_track_id_static(self):
        self.get_track_by_track_type(const.TRACK_STATIC)
        # 搜索范围和 drsu横杆与acu相距距离成正比
        self.get_track_by_center()
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
        self.get_track_by_speed()
        self.find_main_track_id_by_popt()
        if self.use_time:
            self.get_track_by_timestamp()
        self.get_track_by_obj_type(const.OBJ_TYPE_BUS, const.OBJ_TYPE_CAR)
        # 只有在类型识别正确的情况下保留认为是跳变，保留多个track
        if self.match_list[0] == const.MATCH_TYPE_MAIN:
            self.obj_jump = self.bk_df.shape[0]
        # 在类型没有完全匹配的情况下 按照体积进行筛选
        self.get_track_by_obj_volume()
        self.find_main_track_id_by_frame_num()

    # 更加acu上报的轨迹数据去寻找drsu识别出来的目标轨迹
    def find_main_track_id(self):
        if self.df.empty:
            self.get_drsu_data()
        if self.acu_track.track_type == const.TRACK_STATIC:
            logger.info('场景类型为静止')
            # 先寻找轨迹类型为静止
            self.find_main_track_id_static()
        elif self.acu_track.track_type == const.TRACK_STRAIGHT:
            logger.info('场景类型为运动，速度：%s' % self.acu_track.speed)
            self.find_main_track_id_straight()

    # 检查目标轨迹
    def check_main_track_id(self):
        # 经过筛选之后只剩下一个track 不用处理
        if self.bk_df.shape[0] == 1:
            return
        if self.match_list[0] != const.MATCH_TYPE_MAIN:
            self.bk_df = self.bk_df.head(1)
            return
        if self.acu_track.track_type == const.TRACK_STATIC:
            self.check_main_track_id_static()
        elif self.acu_track.track_type == const.TRACK_STRAIGHT:
            self.check_main_track_id_straight()

    def draw_static_sub(self):
        start_time = self.bk_df.start_time.min()
        for i in range(self.bk_df.shape[0]):
            df = round(pd.read_csv(self.bk_df.iloc[i].file_name), 1)
            df['Timestamp'] = (df['dbTimestamp'] * 10 - start_time)
            time_stamp = int(df['Timestamp'][df.shape[0] - 1])
            track_id = self.bk_df.iloc[i].track_id
            count_dict = [2, 1, 2, 1]
            dict_x = [df.Timestamp, df.Timestamp, df.Timestamp, np.arange(time_stamp)]
            dict_y = [[abs(df['stCenter.dbx'] - self.acu_track.center[0]),
                       abs(df['stCenter.dby'] - self.acu_track.center[1])],
                      [df.stObj_type],
                      [df.dbwidth * df.dbheight, [const.VOLUME_BUS for _ in range(df.shape[0])]],
                      [[1 if i in df.Timestamp else 0 for i in range(time_stamp)]]]
            dict_x_ticks = [None, None, None, np.arange(0, time_stamp + 100, 100)]
            dict_y_ticks = [None, np.arange(3, 11), None, [0, 1]]
            dict_label = [['纵向位置偏差track_id:{}'.format(track_id), '横向位置偏差track_id:{}'.format(track_id)],
                          ['障碍物类型'],
                          ['障碍物面积(与摄像头方向正视面)', '小巴车实际面积'],
                          ['障碍物数据帧分布']]
            for j in range(4):
                self.ax[j].plot(dict_x[j], dict_y[j][0], Listcolors[(i + j) % 8], label=dict_label[j][0])
                if dict_x_ticks[j] is not None:
                    self.ax[j].set_xticks(dict_x_ticks[j])
                if dict_y_ticks[j] is not None:
                    self.ax[j].set_yticks(dict_y_ticks[j])
                if count_dict[j] > 1:
                    self.ax[j].plot(dict_x[j], dict_y[j][1], Listcolors[(i + j + 3) % 8], linestyle='--',
                                    label=dict_label[j][1])
                self.ax[j].legend(loc='best', borderaxespad=0)

    def draw_straight_sub(self):
        start_time = self.bk_df.start_time.min()
        for i in range(self.bk_df.shape[0]):
            df = round(pd.read_csv(self.bk_df.iloc[i].file_name), 1)
            self.get_draw_data_straight(df)
            if not self.draw_flag:
                return
            df['Timestamp'] = (df['dbTimestamp'] * 10 - start_time)
            time_stamp = int(df['Timestamp'][df.shape[0] - 1])
            # track_id = self.bk_df.iloc[i].track_id
            # dict_y = [[df['x_incr'], df['y_incr']],
            #           [df['vx_incr'], df['vy_incr']],
            #           [df.stObj_type],
            #           [df.dbwidth * df.dbheight, [const.VOLUME_BUS for _ in range(df.shape[0])]]]
            length = df.shape[0]
            dict_y = [[df['x_acu'], df['stCenter.dbx']],
                      [df['y_acu'], df['stCenter.dby']],
                      [df['vx_acu'], df['stvelocity.dbx']],
                      [df['vy_acu'], df['stvelocity.dby']],
                      [df.stObj_type],
                      [df.dbwidth * df.dbheight, [const.VOLUME_BUS for _ in range(df.shape[0])]]
                      ]
            dict_x_ticks = [None, None, None, None, None, np.arange(0, time_stamp + 100, 100)]
            dict_y_ticks = [None, None, None, None, np.arange(3, 11), np.arange(0, 10)]
            dict_label = [['实际纵向坐标', '识别纵向坐标', '+%5偏差', '-%5偏差'],
                          ['实际横向坐标', '识别横向坐标', '+%5偏差', '-%5偏差'],
                          ['实际纵向速度', '识别纵向速度', '+%5偏差', '-%5偏差'],
                          ['实际横向速度', '识别横向速度', '+%5偏差', '-%5偏差'],
                          ['障碍物类型'],
                          ['障碍物面积(与摄像头方向正视面)', '小巴车实际面积']]
            for j in range(len(dict_y)):
                for k in range(len(dict_y[j])):
                    self.ax[j].plot(df.Timestamp, dict_y[j][k], Listcolors[(i + j + k) % 8],
                                    linestyle=List_style[k % 4], label=dict_label[j][k])
                    if dict_x_ticks[j] is not None:
                        self.ax[j].set_xticks(dict_x_ticks[j])
                    if dict_y_ticks[j] is not None:
                        self.ax[j].set_yticks(dict_y_ticks[j])
                    self.ax[j].legend(loc='best', borderaxespad=0)

    def draw_static(self, is_show=False):
        title = ''.join(self.data_path.split('\\')[-1])
        image_name = os.path.join(self.data_path, title + 'static.png')
        list_title = ['纵/横向偏差图', '识别类型变化图', '障碍物面积变化图', '有效帧占比图']
        list_y_label = ['acu实际与识别坐标偏差(m)', '障碍物识别类型', '障碍物识别面积(平米)', '障碍物识别有效帧']
        self.fig = plt.figure(figsize=(18, 10))
        for i in range(len(list_title)):
            ax = self.fig.add_subplot(2, 2, i + 1)
            ax.set(title=list_title[i], ylabel=list_y_label[i], )
            self.ax[i] = ax
        self.draw_static_sub()
        plt.savefig(image_name)
        if is_show:
            plt.show()
            plt.pause(0.1)
        plt.close()
        self.fig = None
        self.ax = [None] * 9

    def draw_straight(self, is_show=False):
        title = ''.join(self.data_path.split('\\')[-1])
        rq = time.strftime('%Y%m%d%H', time.localtime(time.time()))
        image_name = os.path.join(self.data_path, title + rq + 'straight.png')
        list_title = ['纵向坐标偏差图', '横向坐标偏差图', '纵向速度偏差图', '横向速度偏差图', '识别类型变化图', '障碍物面积变化图']
        list_y_label = ['纵向坐标', '横向坐标', '纵向速度', '横向速度', '识别类型', '识别面积']
        self.fig = plt.figure(figsize=(18, 10))
        for i in range(len(list_title)):
            ax = self.fig.add_subplot(3, 2, i + 1)
            ax.set(title=list_title[i], ylabel=list_y_label[i])
            self.ax[i] = ax
        self.draw_straight_sub()
        plt.savefig(image_name)
        title1 = ''.join(self.data_path.split('\\')[-2:])
        plt.savefig('D:\\data\\scene_picture1\\' + title1 + 'straight.png')
        if is_show:
            plt.show()
            plt.pause(0.1)
        plt.close()
        self.fig = None
        self.ax = [None] * 9

    def draw(self):
        if self.acu_track.track_type == const.TRACK_STATIC:
            self.draw_static()
        elif self.acu_track.track_type == const.TRACK_STRAIGHT:
            self.draw_straight()
        else:
            pass

    # 获取画图数据，主要就是对比时间戳,不考虑trackid跳变
    def get_draw_data_straight(self, df):
        index_drsu = 0
        index_acu = 0
        drsu_time_stamp = round(df['dbTimestamp'] * 10, 1)
        df_acu = self.acu_track.acu_data
        acu_time_stamp = df_acu['time_stamp_drc']
        while True:
            time_drsu = drsu_time_stamp[index_drsu]
            time_acu = acu_time_stamp[index_acu]
            if time_drsu - time_acu > 1:
                index_acu += 1
            elif time_acu - time_drsu > 1:
                index_drsu += 1
            else:
                df.loc[index_drsu, 'x_acu'] = df_acu.loc[index_acu, 'coordinate_x']
                df.loc[index_drsu, 'y_acu'] = df_acu.loc[index_acu, 'coordinate_y']
                df.loc[index_drsu, 'vx_acu'] = df_acu.loc[index_acu, 'speed_x']
                df.loc[index_drsu, 'vy_acu'] = df_acu.loc[index_acu, 'speed_y']
                index_acu += 1
                index_drsu += 1
                self.draw_flag = True
            if index_drsu == df.shape[0] or index_acu == df_acu.shape[0]:
                break
        df['stCenter.dbx'], df['stCenter.dby'] = coordinate_system_transformation(df['stCenter.dbx'],
                                                                                  df['stCenter.dby'])
        df['stvelocity.dbx'], df['stvelocity.dby'] = coordinate_system_transformation(df['stvelocity.dbx'],
                                                                                  df['stvelocity.dby'], v_flag=True)
        df['x_acu'], df['y_acu'] = coordinate_system_transformation(df['x_acu'], df['y_acu'])
        df['vx_acu'], df['vy_acu'] = coordinate_system_transformation(df['vx_acu'], df['vy_acu'], v_flag=True)


# 穿入两个Series
def coordinate_system_transformation(dfx, dfy, v_flag=False):
    if not v_flag:
        dfx = dfx - dfx.min()
        dfy = dfy - dfy[dfx.nsmallest(1).index.values[0]]
    return dfx * math.cos(const.LOAD_VALUE) + dfy * math.sin(const.LOAD_VALUE), dfy * math.cos(
        const.LOAD_VALUE) - dfx * math.sin(const.LOAD_VALUE)


if __name__ == '__main__':
    # drsu_file = r'D:\data\drsu03场景\group1\group1_position02'
    # drsu_file = r'D:\data\drsu_staright\group1\speed20_uniform_04'
    # drsu_file = r'D:\data\drsu_data\01\22'
    drsu_file = r'D:\data\data_straight\2\20kmh_由远到近_04'
    a = DrsuScene(drsu_file)
    a.find_main_track_id()
    a.check_main_track_id()
    # b = a.merge_track_static()
    a.draw()
