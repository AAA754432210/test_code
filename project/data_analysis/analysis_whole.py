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
import numpy as np
import matplotlib.pyplot as plt
from project.data_analysis.analysis_acu import TrackAcu
from project.data_analysis.analysis_drsu import DrsuScene
from project.data_analysis.constant import const

logger = Logger('analysis_scene').getlog()
plt.rcParams['font.sans-serif'] = ['SimHei']  # 正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
List_style = ['-', '--', '-.', ':']
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
        self.draw_data = [pd.DataFrame()] * 3
        self.rq = time.strftime('%Y%m%d', time.localtime(time.time()))
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
        self.save_data()

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
        save_name = os.path.join(self.file_path, self.rq + str(self.index) + 'parsed.csv')
        index = 0
        for i in self.data[self.index]:
            # i.bk保存了每个场景下,筛选出来的目标障碍物
            if i.acu_track.track_type == 0:
                if i.bk_df.shape[0] > 1:
                    draw_info = i.merge_track_static()
                else:
                    draw_info = i.bk_df.iloc[0]
                self.draw_data[self.index] = self.draw_data[self.index].append(draw_info, ignore_index=True)
            elif i.acu_track.track_type == 1:
                draw_info = i.draw_data
                self.draw_data[self.index] = self.draw_data[self.index].append(draw_info, ignore_index=True)
            index += 1
        self.draw_data[self.index].to_csv(save_name, encoding='gbk')

    def draw_static(self):
        pass

    def draw_straight_sub_plt(self, index):
        index_file = 1

        for i in range(3):
            file_name = os.path.join(self.file_path, self.rq + str(i) + 'parsed.csv')
            df = pd.read_csv(file_name)
            df.reset_index(drop=True)
            if index == 0:
                df = df.loc[(df['acu_vx'] > 0)].sort_values(by='acu_vx', ascending=True).reset_index(drop=True)
            else:
                df = df.loc[(df['acu_vx'] < 0)].sort_values(by='acu_vx', ascending=True).reset_index(drop=True)
            vx = abs(df.acu_vx*3.6)
            dict_x = [vx, vx, vx, vx, vx, vx]
            dict_y = [[df.acu_center_x - df.drsu_center_x],
                      [df.acu_center_y - df.drsu_center_y],
                      [(df.acu_vx - df.drsu_vx)*3.6],
                      [(df.acu_vy - df.drsu_vy)*3.6],
                      [df['obj_type_rate']],
                      [df['volume']]]
            dict_x_ticks = [np.arange(0, 50, 10), np.arange(0, 50, 10), np.arange(0, 50, 10),
                            np.arange(0, 50, 10), np.arange(0, 50, 10), np.arange(0, 50, 10)]
            dict_y_ticks = [None, None, None, None, np.arange(90, 120, 10), np.arange(0, 10)]
            label_ = '第{}组'.format(index_file)
            for j in range(len(dict_y)):
                for k in range(len(dict_y[j])):
                    self.ax[j].plot(dict_x[j], dict_y[j][k], Listcolors[(i + j + k) % 8],
                                    linestyle=List_style[k % 4], label=label_)
                    if dict_x_ticks[j] is not None:
                        self.ax[j].set_xticks(dict_x_ticks[j])
                    if dict_y_ticks[j] is not None:
                        self.ax[j].set_yticks(dict_y_ticks[j])
                    self.ax[j].legend(loc='best', borderaxespad=0)
            index_file += 1

    def draw_straight(self, is_show=False):
        list_title = [['不同速度下acu和drsu横向位置偏差图'],
                      ['不同速度下acu和drsu纵向位置偏差图'],
                      ['不同速度下acu和drsu横向速度偏差图'],
                      ['不同速度下acu和drsu纵向速度偏差图'],
                      ['不同速度下drsu障碍物类型识别正确率'],
                      ['不同速度下不同距离drsu识别面积图（宽*高）']]

        list_y_label = ['横向坐标偏差均值', '纵向坐标偏差均值', '横向速度偏差均值',
                        '纵向速度偏差均值', '障碍物类型识别正确率(%)', '障碍物识别面积(平米)']
        list_x_label = ['速度(km/h)', '速度(km/h)', '速度(km/h)', '速度(km/h)', '速度(km/h)', '速度(km/h)', ]
        for i in range(2):
            self.fig = plt.figure(figsize=(20, 10))
            for j in range(len(list_title)):
                ax = self.fig.add_subplot(3, 2, j + 1)
                ax.set(title=list_title[j], xlabel=list_x_label[j], ylabel=list_y_label[j])
                self.ax[j] = ax
            self.draw_straight_sub_plt(i)
            plt.savefig(os.path.join(self.file_path, self.rq + str(i) + 'straight.png'))
            if is_show:
                plt.show()
                plt.pause(0.1)
            plt.close()
            self.fig = None
            self.ax = [None] * 9

    def draw(self):
        if self.draw_data[0].iloc[0].track_type == 0:
            self.draw_static()
        elif self.draw_data[0].iloc[0].track_type == 1:
            self.draw_straight()
        else:
            pass


if __name__ == '__main__':
    # A = AnalysisData(r'D:\data\drsu_staright')
    A = AnalysisData(r'D:\data\data_straight')
    A.analysis_all()
    A.draw_straight()
