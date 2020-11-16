# -*- coding: utf-8 -*-
"""
@Project : test_code
@File    : analysis_drsu_single.py
@Author  : 王白熊
@Data    ： 2020/11/10 16:45
单个drsutrack——id分析
"""
import pandas as pd
import numpy as np
from pandas import Series
from scipy import optimize
from common.Log import Logger
from project.data_analysis.constant import const
import math
import random
import glob
import os
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

logger = Logger('TrackDrsu').getlog()


def target_func(x, A, B):
    return A * x + B


class TrackDrsu(object):
    def __init__(self, file_drsu, ort=True):
        self.df = round(pd.read_csv(file_drsu), 1)
        self.track_id = file_drsu.split('\\')[-1].split('.')[0]
        self.ort = ort
        self.frame_num = self.df.shape[0]
        # 障碍物类型可能出现跳变,所以取众数
        self.obj_type = self.df['stObj_type'].mode()[0]
        self.obj_dict = pd.value_counts(self.df.stObj_type).to_dict()
        logger.debug('trackid:%s,obj_type:%s' % (self.track_id,self.obj_dict))
        self.dict_track_info = pd.Series()
        self._file_name = file_drsu
        # 判断轨迹类型，采用方差法判断轨迹是否是静止, 返回值0：代表是静止状态，1代表是直线运动状态

    def is_track_type_static_by_center(self):
        var_x = self.df['stCenter.dbx'].var()
        var_y = self.df['stCenter.dbx'].var()
        logger.debug('坐标方差，x:%s，y:%s' % (var_x, var_y))
        if var_x < const.VARIANCE_CENTER and var_y < const.VARIANCE_CENTER:
            return True
        else:
            return False

    # 判断轨迹类型，采用方差法判断轨迹是否是静止, 返回值0：代表是静止状态，1代表是直线运动状态
    def is_track_type_static_by_velocity(self):
        var_x = self.df['stvelocity.dbx'].var()
        var_y = self.df['stvelocity.dbx'].var()
        logger.debug('速度方差，x:%s，y:%s' % (var_x, var_y))
        if var_x < const.VARIANCE_VELOCITY and var_y < const.VARIANCE_VELOCITY and self.df['stvelocity.dbx'].mode()[
            0] == 0:
            return True
        else:
            return False

    # 运动方式 0：静止，1：直行运动 2：垂直于摄像头方向直行运动，3：先静止再运动 4：先运动再静止（其中静止时间至少占一半以上）5：其他运动
    # 目前应该是只考虑静止和直行运动
    @staticmethod
    def check_track_type_by_incre(x, y):
        threshold_x, threshold_y = const.CENTER_THRESHOLD_X, const.CENTER_THRESHOLD_Y
        # 如果摄像头方向偏差3米以内，垂直方向偏差1米以内，则认定物体为静止状态,判断摄像头的朝向是x方向还是y方向
        if x[0] < threshold_x and y[0] < threshold_y and x[1] < threshold_x and y[1] < threshold_y and \
                x[2] < threshold_x and y[2] < threshold_y:
            return const.TRACK_STATIC
        # 前面半段符合静止条件
        elif x[1] < threshold_x and y[1] < threshold_y:
            return const.TRACK_STRAIGHT_FRONT
        # 后面半段符合静止条件
        elif x[2] < threshold_x and y[2] < threshold_y:
            return const.TRACK_STRAIGHT_BACK
        # 如果物体在x，y方向上移动距离大于30米，且起始，中间，结束三点基本处于一条直线上，这认定为直行运动
        # 判断处于一条直线的方法为,起点和中点的连线 和中点和终点的连线夹角小于20度
        # 摄像头方向位移方向位移距离超过10
        if x[0] > 20:
            if abs((90 if y[1] == 0 else math.atan(x[1] / y[1]) * const.ANGEL_VER_VALUE) -
                                        (90 if y[2] == 0 else math.atan(x[2] / y[2]) * const.ANGEL_VER_VALUE)) < \
                    const.ANGEL_THRESHOLD:
                # 夹角小于20度判定为车辆沿着摄像头方向直行
                return const.TRACK_STRAIGHT
            else:
                # 夹角大于20度判定为非直行
                return const.TRACK_UNDEFINED
        if y[0] > 10:
            if abs((90 if y[1] == 0 else math.atan(x[1] / y[1]) * const.ANGEL_VER_VALUE) -
                                        (90 if y[2] == 0 else math.atan(x[2] / y[2]) * const.ANGEL_VER_VALUE)) < \
                    const.ANGEL_THRESHOLD:
                # 夹角小于20度判定为车辆沿着摄像头垂直方向直行
                return const.TRACK_STRAIGHT_VERTICAL
            else:
                # 夹角大于20度判定为非直行
                return const.TRACK_UNDEFINED

    # 初步判断轨迹类型，采用三点法判断 0：静止，1：直行运动 2：垂直于摄像头方向直行运动，3：先静止再运动 4：先运动再静止（其中静止时间至少占一半以上）5：其他运动
    # 输入参数 df为DataFrame类型数据，ort为摄像头朝向，True代表x（东西）方向朝向，False代表y（南北）方向朝向
    def get_track_type_by_center(self):
        mid_index = self.frame_num // 2
        stCenter_x = self.df['stCenter.dbx']
        stCenter_y = self.df['stCenter.dby']
        last = self.frame_num - 1
        incre_x = [abs(stCenter_x[last] - stCenter_x[0]), abs(stCenter_x[mid_index] - stCenter_x[0]),
                   abs(stCenter_x[last] - stCenter_x[mid_index])]
        incre_y = [abs(stCenter_y[last] - stCenter_y[0]), abs(stCenter_y[mid_index] - stCenter_y[0]),
                   abs(stCenter_y[last] - stCenter_y[mid_index])]
        # 经过转换之后 x 代表摄像头方向，y代表垂直于摄像头方向
        x, y = (incre_x, incre_y) if self.ort else (incre_y, incre_x)
        track_type = self.check_track_type_by_incre(x, y)
        return track_type

    # 先考虑静止状态,坐标，速度判断任一成立则判定为静止
    def get_track_type(self):
        flag_center = self.is_track_type_static_by_center()
        flag_velocity = self.is_track_type_static_by_velocity()
        if flag_center and flag_velocity:
            return const.TRACK_STATIC
        # 行人因速度慢，速度经常被识别为0，所以行人判断坐标移动就算移动了
        elif not flag_center and flag_velocity and self.obj_type == const.OBJ_TYPE_PER:
            logger.debug('trackid:%s 类型为行人，坐标判断不符合静止条件，速度判断符合静止条件，判断为非静止' % self.track_id)
            return const.TRACK_UNDEFINED
        # 非行人
        elif not flag_center and flag_velocity:
            logger.debug('trackid:%s 坐标判断不符合静止条件，速度判断符合静止条件' % self.track_id)
            return const.TRACK_STATIC
        elif flag_center and not flag_velocity:
            logger.debug('trackid:%s 坐标判断符合静止条件，速度判断不符合静止条件' % self.track_id)
            return const.TRACK_STATIC
        else:
            # 待修改
            return self.get_track_type_by_center()

    # 计算拟合优度
    def check_fit_we(self, popt):
        series_x = self.df['stCenter.dbx']
        series_y = self.df['stCenter.dby']
        y_prd = Series(list(map(lambda x: popt[0] * x + popt[1], series_x)))
        egression = sum((y_prd - series_x.mean()) ** 2)  # r回归平方和
        residual = sum((series_y - y_prd) ** 2)  # 残差平方和
        total = sum((series_y - series_y.mean()) ** 2)  # 总体平方和
        if total == 0:
            r_square = 1
        else:
            r_square = 1 - residual / total  # 相关性系数R^2
        logger.debug('对track_id:%s 轨迹进行拟合，拟合参数:%s,拟合优度：%s' % (self.track_id, popt, r_square))
        return r_square

    # 利用curve_fit 函数获取拟合参数 以及判断拟合优度,返回值为参数及标准方差
    def check_stright_fit(self):
        if self.dict_track_info['track_type'] == const.TRACK_STATIC:
            return [0, 0], 0
        popt, pcov = optimize.curve_fit(target_func, self.df['stCenter.dbx'], self.df['stCenter.dby'])
        perr = np.sqrt(np.diag(pcov))
        r_square = self.check_fit_we(popt)
        return popt, r_square

    # 静止物体删除异常值
    def drop_outliers_static(self):
        x = self.df['stCenter.dbx'].mode()[0]
        df = self.df.loc[(abs(self.df['stCenter.dbx'] - x) < const.CENTER_THRESHOLD_Y)]
        df = df.reset_index()
        frame_num = df.shape[0]  # 帧数
        frame_no = [int(df.ulFrame[0]), int(df.ulFrame[frame_num - 1])]
        tho_num = frame_no[1] - frame_no[0]
        obj_dict = pd.value_counts(df.stObj_type).to_dict()
        return [df['stCenter.dbx'].mean(), df['stCenter.dby'].mean(), tho_num, frame_num, obj_dict]

    # 单个track_id画轨迹图
    def draw_track_straight(self, ax):
        ax.plot(self.df['stCenter.dbx'], self.df['stCenter.dby'], random.choice(const.LIST_COLOR),
                linewidth=0.4, label='track_id:{}'.format(self.track_id))

    # 基础的参数用这个获取，其他的调用函数获取
    def calc_track_info(self):
        track_info = self.dict_track_info
        track_info['track_id'] = self.track_id
        track_info['obj_type'] = self.obj_type
        track_info['track_type'] = self.get_track_type()
        track_info['volume'] = self.df['dbwidth'].mean() * self.df['dbheight'].mean()
        start_time = int(round(self.df.dbTimestamp[0] * 10))
        end_time = int(round(self.df.dbTimestamp[self.df.shape[0] - 1] * 10))
        track_info['time_stamp'] = end_time - start_time
        track_info['start_time'] = start_time
        track_info['end_time'] = end_time
        # 坐标参数一般是用在静态场景下，所以取总数会比较
        track_info['center_x'] = self.df['stCenter.dbx'].mode()[0]
        track_info['center_y'] = self.df['stCenter.dby'].mode()[0]
        track_info['speed_x'] = self.df['stvelocity.dbx'].mean()
        track_info['speed_y'] = self.df['stvelocity.dby'].mean()
        track_info['frame_num'] = self.df.shape[0]
        track_info['file_name'] = self._file_name
        popt, r_square = self.check_stright_fit()
        # y = ax+b
        track_info['a'] = popt[0]
        track_info['b'] = popt[1]
        track_info['r_square'] = r_square
        # logger.debug('单个处理结果：%s'% track_info)
        return track_info

    @property
    def track_info(self):
        if not self.dict_track_info.empty:
            return self.dict_track_info
        else:
            return self.calc_track_info()
        # # 小于10帧的数据直接丢弃
        # if self.frame_num <= 10:
        #     return None


# 用来显示单个场景下，非静止物体不同拟合优度的轨迹图
def wth_test():
    fig = plt.figure(figsize=(36, 36))
    # plt.title('不同点位识别参数分析', color='black', fontsize=18, loc='center')
    ax1 = fig.add_subplot(331)
    ax2 = fig.add_subplot(332)
    ax3 = fig.add_subplot(333)
    ax4 = fig.add_subplot(334)
    ax5 = fig.add_subplot(335)
    ax6 = fig.add_subplot(336)
    ax7 = fig.add_subplot(337)
    ax8 = fig.add_subplot(338)
    ax9 = fig.add_subplot(339)
    ax1.set(title='0.98', )
    ax2.set(title='0.95', )
    ax3.set(title='0.92', )
    ax4.set(title='0.88', )
    ax5.set(title='0.82', )
    ax6.set(title='0.74', )
    ax7.set(title='0.62', )
    ax8.set(title='0.50', )
    ax9.set(title='0.30', )

    file_dir = r'D:\data\drsu_staright\group1\speed10_uniform_01\obs_data_trackid'
    track_files = glob.glob(os.path.join(file_dir, '*.csv'))
    for i in track_files:
        track = TrackDrsu(i)
        if track.get_track_type() != 0:
            popt, r_square = track.check_stright_fit()
            if r_square > 0.98:
                track.draw_track_straight(ax1)
            elif r_square > 0.95:
                track.draw_track_straight(ax2)
            elif r_square > 0.92:
                track.draw_track_straight(ax3)
            elif r_square > 0.88:
                track.draw_track_straight(ax4)
            elif r_square > 0.82:
                track.draw_track_straight(ax5)
            elif r_square > 0.74:
                track.draw_track_straight(ax6)
            elif r_square > 0.62:
                track.draw_track_straight(ax7)
            elif r_square > 0.50:
                track.draw_track_straight(ax8)
            elif r_square > 0.30:
                track.draw_track_straight(ax9)
    plt.savefig(r'D:\data\test_wth.png')
    plt.show()


def wth_test1():
    file_dir = r'D:\data\drsu_staright\group1\speed10_uniform_01\obs_data_trackid\10.csv'
    track = TrackDrsu(file_dir)
    print(track.track_info)


if __name__ == '__main__':
    wth_test1()
