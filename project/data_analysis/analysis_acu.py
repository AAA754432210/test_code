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
            self.track_type = 0
            index = int(os.path.dirname(file_path)[-2:])
            self.center = const.CENTER_ACU[index - 1]
            # raise FileNotFoundError('acu数据文件:%s不存在' % file_path)
        else:
            self.acu_file = file_path
            self._ort = ort
            self.acu_data = self.get_acu_data()
            if self.acu_data.empty:
                raise FileNotFoundError('acu文件:{}数据不正确'.format(file_path))
            self.track_type = self.get_track_type()
            self.center = [self.acu_data.coordinate_x.mean(), self.acu_data.coordinate_y.mean()]

    def get_acu_data(self):
        data_list = glob.glob(os.path.join(self.acu_file, '*'))
        parsed_list = glob.glob(os.path.join(self.acu_file, '*parsed.csv'))
        if not data_list:
            raise FileNotFoundError('acu数据文件:%s不存在' % file_path)
        # if parsed_list:
        #     acu_data = pd.read_csv(parsed_list[0])
        #     acu_data = acu_data.loc[(acu_data.coordinate_x > const.CENTER_DRSU_3[0]) & (
        #                 acu_data.coordinate_x < (const.CENTER_DRSU_3[0] + 250))]
        #     return acu_data
        # else:
        #     return self.read_acu_ori_data(data_list[0])
        return self.read_acu_ori_data(data_list[0])
    # 获取轨迹类型，acu的判断较为简单，只有直行和静止两种，后续场景增加判断

    def get_track_type(self):
        if abs(self.acu_data.speed_x.mean()) < 1 and abs(self.acu_data.speed_x.mean()) < 1:
            return const.TRACK_STATIC
        else:
            return const.TRACK_STRAIGHT

    # 获取acu和drc之间的延迟时间，由于drc时间和drsu时间已经ntp同步，所以认为这个时间就是drsu和acu的延迟时间
    # 没啥必要获取这个延迟时间 直接拿drc的时间戳进行计算更加简单
    def get_delay_time(self):
        if self.track_type == 0:
            return 0
        return round((self.acu_data.time_stamp_drc - self.acu_data.time_stamp).mean(), 1)

    # 获取acu和drc之间的延迟时间，由于drc时间和drsu时间已经ntp同步，所以认为这个时间就是drsu和acu的延迟时间
    def get_time_stamp(self):
        if self.track_type == 0:
            return [0, 0, 0]
        start_time = self.acu_data.iloc[0].time_stamp_drc
        end_time = self.acu_data.iloc[self.acu_data.shape[0]-1].time_stamp_drc
        time_stamp = end_time - start_time
        logger.info('时间戳数据：%s' % [start_time, end_time, time_stamp])
        return [start_time, end_time, time_stamp]

    @staticmethod
    def read_acu_ori_data(file_name):
        acu_data = pd.DataFrame(
            columns=['time_stamp_drc', 'time_stamp', 'coordinate_x', 'coordinate_y',
                     'coordinate_z', 'speed_x', 'speed_y',
                     'speed_z'])

        with open(file_name, 'r') as f:  # 命令行带参数
            row_num = 0
            for line in f.readlines():
                time_stamp_drc = line[0:17]
                time_stamp_drc_sub = line[17:24]
                timeArray = time.strptime(time_stamp_drc, "%Y%m%d %H:%M:%S")
                drc_timestamp = float(str(int(time.mktime(timeArray)))+time_stamp_drc_sub)
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
                    acu_data.loc[row_num, 'time_stamp_drc'] = drc_timestamp*10  # 直接使用这个时间戳进行处理
                    acu_data.loc[row_num, 'time_stamp'] = float(tmp_dict['db_time_stamp'])
                    acu_data.loc[row_num, 'coordinate_x'] = float(tmp_dict['st_coordicate']['dbx'])
                    acu_data.loc[row_num, 'coordinate_y'] = float(tmp_dict['st_coordicate']['dby'])
                    acu_data.loc[row_num, 'coordinate_z'] = float(tmp_dict['st_coordicate']['dbz'])
                    acu_data.loc[row_num, 'speed_x'] = float(tmp_dict['st_line_speed']['x'])
                    acu_data.loc[row_num, 'speed_y'] = float(tmp_dict['st_line_speed']['y'])
                    acu_data.loc[row_num, 'speed_z'] = float(tmp_dict['st_line_speed']['z'])
                row_num += 1

        acu_file_parsed = os.path.join(os.path.dirname(file_name),
                                       os.path.basename(file_name).split('.')[0] + 'parsed.csv')
        logger.info('acu数据初步处理并保存到文件：%s' % acu_file_parsed)
        acu_data = acu_data.loc[
            (acu_data.coordinate_x > const.CENTER_DRSU_3[0]) & (acu_data.coordinate_x < const.CENTER_DRSU_3[0] + 250)]
        acu_data.to_csv(acu_file_parsed, sep=',', index=False, header=True)
        return acu_data.reset_index()

    # 计算拟合优度
    def check_fit_we(self, popt):
        series_x = self.acu_data.coordinate_x
        series_y = self.acu_data.coordinate_y
        y_prd = pd.Series(list(map(lambda x: popt[0] * x + popt[1], series_x)))
        egression = sum((y_prd - series_x.mean()) ** 2)  # r回归平方和
        residual = sum((series_y - y_prd) ** 2)  # 残差平方和
        total = sum((series_y - series_y.mean()) ** 2)  # 总体平方和
        r_square = 1 - residual / total  # 相关性系数R^2
        logger.info('对acu轨迹进行拟合，拟合参数:%s,拟合优度：%s' % (popt, r_square))
        return r_square

    # 利用curve_fit 函数获取拟合参数 以及判断拟合优度,返回值为参数及标准方差
    def check_stright_fit(self):
        popt, pcov = optimize.curve_fit(target_func, self.acu_data.coordinate_x, self.acu_data.coordinate_y)
        perr = np.sqrt(np.diag(pcov))
        r_square = self.check_fit_we(popt)
        return popt, r_square

    @property
    def speed(self):
        return [self.acu_data.speed_x.mean(), self.acu_data.speed_y.mean()]


if __name__ == '__main__':
    files = r'D:\data\drsu_staright\group3\speed30_uniform_06\acu_data'
    acu_ana = TrackAcu(files)
    # acu_data = acu_ana.read_acu_ori_data()
    # logger.info('acu_data:{}'.format(acu_data))
