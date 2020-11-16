# -*- coding: utf-8 -*-
"""
@Project : test_code
@File    : analysis_whole.py
@Author  : 王白熊
@Data    ： 2020/11/10 15:30
"""
import glob
import os
import pandas as pd
import time
from common.Log import Logger
import matplotlib.pyplot as plt
from project.data_analysis.analysis_acu import TrackAcu
from project.data_analysis.analysis_drsu import DrsuScene
from project.data_analysis.constant import const

logger = Logger('analysis_scene').getlog()
plt.rcParams['font.sans-serif'] = ['SimHei']  # 正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

Listcolors = ['red', 'blue', 'green', 'cyan', 'magenta', 'orange', 'darkred', 'black']


class AnalysisData():
    def __init__(self, file_path, ort=True):
        if not os.path.exists(file_path):
            raise FileNotFoundError('数据文件夹:%s不存在' % file_path)
        self.file_path = file_path
        self.data = []
        self.index = 0
        self.fig = None
        self.ax = [None] * 9
        self.sub_fig = []
        self.sub_ax = []
        self.draw_data = [pd.DataFrame()] * 3
        # self.track_type = 0

    # 分析一组数据
    def analysis_data_group(self, data_path):
        """
        :param data_path: 到group一层
        :return:
        """
        cat_paths = [files for files in glob.glob(data_path + "/*") if os.path.isdir(files)]
        # 以文件中的数字进行排名
        cat_paths.sort(key=lambda x: int(os.path.basename(x)[-2:]))
        for i in cat_paths:
            # i是一个文件夹，文件夹下面有log.txt acu.csv 文件夹obs_data_trackid
            drsu_scence = DrsuScene(i)
            drsu_scence.find_main_track_id()
            drsu_scence.check_main_track_id()
            drsu_scence.draw()
            self.data[self.index].append(drsu_scence)
        # 一组存一个数据
        # self.save_data()

    def analysis_all(self):
        cat_paths = [files for files in glob.glob(self.file_path + "/*") if os.path.isdir(files)]
        for index in range(len(cat_paths)):
            self.index = index
            self.data.append([])
            self.analysis_data_group(cat_paths[index])

    def save_data(self):
        """
        将静态相关图片和动态相关图片所需要的数据都保存为csv文件，一组数据保存一份csv文件
        :return:
        """
        rq = time.strftime('%Y%m%d', time.localtime(time.time()))
        save_name = os.path.join(self.file_path, rq + str(self.index) + 'parsed.csv')
        index = 0
        for i in self.data[self.index]:
            # i.bk保存了每个场景下,筛选出来的目标障碍物
            if i.bk_df.shape[0] > 1:
                track_info = i.merge_track_static()
            else:
                track_info = i.bk_df.iloc[0]
            self.draw_data[self.index] = self.draw_data[self.index].append(track_info, ignore_index=True)
            index += 1
        self.draw_data[self.index].to_csv(save_name)

    def draw_static(self):
        pass

    def draw_straight(self):
        pass

    def draw(self):
        if self.draw_data[0].iloc[0].track_type == 0:
            draw_static()
        elif self.draw_data[0].iloc[0].track_type == 1:
            draw_straight()
        else:
            pass


if __name__ == '__main__':
    A = AnalysisData(r'D:\data\drsu_staright')
    A.analysis_all()
