# -*- coding: utf-8 -*-
"""
@Project : analydata
@File    : analysis_acu.py
@Author  : 王白熊
@Data    ： 2020/10/30 15:17
"""

import re
import json
import os
import pandas as pd
import numpy as np
from project.data_analysis.constant import const
from scipy import optimize
from common.Log import Logger
import glob
import time
import re

logger = Logger('AnalysisAcu').getlog()

strmatchcell = "HandleAcuVehicleState:vehicle state: "


def target_func(x, A, B):
    return A * x + B


# ACU轨迹
class TrackAcu(object):
    # ort表示道路是否为x方向
    def __init__(self, file_path, ort=True):
        if not os.path.exists(file_path):
            raise FileNotFoundError('acu数据文件:%s不存在' % file_path)
        self.acu_file = file_path
        self._ort = ort
        self.acu_data = self.get_acu_data()
        if self.acu_data.empty:
            raise FileNotFoundError('acu文件:{}数据不正确'.format(file_path))
        self._x = self.acu_data.coordinate_x
        self._y = self.acu_data.coordinate_y
        self._t = self.acu_data.time_stamp
        self._vx = self.acu_data.speed_x
        self._vy = self.acu_data.speed_y
        self.track_type = self.get_track_type()
        self._center = [self._x.mean(), self._y.mean()]

    def get_acu_data(self):
        if not re.search(r'parsed.csv', os.path.basename(self.acu_file)):
            return self.read_acu_ori_data()
        else:
            return pd.read_csv(self.acu_file)

    # 获取轨迹类型，acu的判断较为简单，只有直行和静止两种，后续场景增加判断
    def get_track_type(self):
        if self._vx.mean() < 1 and self._vx.mean() < 1:
            return const.TRACK_STATIC
        else:
            return const.TRACK_STRAIGHT

    def read_acu_ori_data(self, detal_time=const.ACU_DELAY_TIME):
        acu_data = pd.DataFrame(
            columns=['time_stamp', 'coordinate_x', 'coordinate_y',
                     'coordinate_z', 'speed_x', 'speed_y',
                     'speed_z'])

        with open(self.acu_file, 'r') as f:  # 命令行带参数
            row_num = 0
            for line in f.readlines():
                line = line.strip('\n')
                tmp_data = re.search(strmatchcell, line).span()
                if tmp_data is None:
                    logger.warning("没有匹配到字符HandleAcuVehicleState:vehicle state: 。")
                    continue
                # 提取文件中每行json格式的数据，并保存到临时的dict中（tmp_dict）。
                csv_data = line[tmp_data[-1]:]
                try:
                    tmp_dict = json.loads(csv_data)  # 查看json异常处理
                except json.decoder.JSONDecodeError:
                    logger.error("acu文件json解码失败，读取文件位置:{} ".format(str(f.tell())))
                    continue
                except:
                    logger.error('读取文件失败，读取文件位置：{}'.format(f.tell()))
                    continue
                # 判断读取文件数据的行数
                row_num += 1
                # key 判断
                if 'db_time_stamp' in tmp_dict.keys() \
                        and 'st_coordicate' in tmp_dict.keys() \
                        and 'st_line_speed' in tmp_dict.keys() \
                        and 'dbx' in tmp_dict['st_coordicate'].keys() \
                        and 'dby' in tmp_dict['st_coordicate'].keys() \
                        and 'dbz' in tmp_dict['st_coordicate'].keys() \
                        and 'x' in tmp_dict['st_line_speed'].keys() \
                        and 'y' in tmp_dict['st_line_speed'].keys() \
                        and 'z' in tmp_dict['st_line_speed'].keys():
                    acu_data.loc[row_num, 'time_stamp'] = float(tmp_dict['db_time_stamp'] - detal_time)
                    acu_data.loc[row_num, 'coordinate_x'] = float(tmp_dict['st_coordicate']['dbx'])
                    acu_data.loc[row_num, 'coordinate_y'] = float(tmp_dict['st_coordicate']['dby'])
                    acu_data.loc[row_num, 'coordinate_z'] = float(tmp_dict['st_coordicate']['dbz'])
                    acu_data.loc[row_num, 'speed_x'] = float(tmp_dict['st_line_speed']['x'])
                    acu_data.loc[row_num, 'speed_y'] = float(tmp_dict['st_line_speed']['y'])
                    acu_data.loc[row_num, 'speed_z'] = float(tmp_dict['st_line_speed']['z'])

        acu_file_parsed = os.path.join(os.path.dirname(self.acu_file), os.path.basename(self.acu_file).split('.')[0] + 'parsed.csv')
        logger.info('acu数据初步处理并保存到文件：%s' % acu_file_parsed)
        acu_data.to_csv(acu_file_parsed, sep=',', index=False, header=True)
        return acu_data

    # 计算拟合优度
    def check_fit_we(self, popt):
        series_x = self._x
        series_y = self._y
        y_prd = pd.Series(list(map(lambda x: popt[0] * x + popt[1], series_x)))
        egression = sum((y_prd - series_x.mean()) ** 2)  # r回归平方和
        residual = sum((series_y - y_prd) ** 2)  # 残差平方和
        total = sum((series_y - series_y.mean()) ** 2)  # 总体平方和
        r_square = 1 - residual / total  # 相关性系数R^2
        logger.info('对轨迹进行拟合，拟合参数:%s,拟合优度：%s' % (popt, r_square))
        return r_square

    # 利用curve_fit 函数获取拟合参数 以及判断拟合优度,返回值为参数及标准方差
    def check_stright_fit(self):
        popt, pcov = optimize.curve_fit(target_func, self._x, self._y)
        perr = np.sqrt(np.diag(pcov))
        r_square = self.check_fit_we(popt)
        return popt, r_square

    @property
    def speed(self):
        return [self._vx.mean(), self._vy.mean()]

    @property
    def center(self):
        return [self._x.mean(), self._y.mean()]

if __name__ == '__main__':
    files = r'D:\data\drsu_staright\group1\speed10_uniform_01\10kmh_n2f_1parsed.csv'
    acu_ana = TrackAcu(files)
        # acu_data = acu_ana.read_acu_ori_data()
        # logger.info('acu_data:{}'.format(acu_data))
