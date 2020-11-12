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
from common.Log import Logger
from project.data_analysis.analysis_acu import TrackAcu
from project.data_analysis.constant import const

logger = Logger('analysis_scene').getlog()

# 分析单个场景信息
def analysis_scene(data_path, is_save=True, is_show=True):
    drsu_path = os.path.join(data_path, 'obs_data_trackid')
    acu_file = glob.glob(data_path + r'\*parsed.csv')
    if not acu_file:
        acu_file = glob.glob(data_path + r'\*.csv')
        if not glob.glob(data_path + r'\*.csv'):
            logger.error('data_path 目录下没有待处理acu数据')
            raise FileNotFoundError
    acu_data = TrackAcu(acu_file[0])
    if acu_data.track_type == const.TRACK_STATIC:
        pass
    elif acu_data.track_type == const.TRACK_STRAIGHT:
        # 遍历分析所有drsu的track_id，找到符合条件的目标障碍物
        track_info = analysis_drsu_track(drsu_path, acu_data)



def analysis_whole(data_path):
    """
    :param data_path: 到group一层
    :return:
    """
    cat_paths = [files for files in glob.glob(data_path + "/*") if os.path.isdir(files)]
    # 以文件中的数字进行排名
    cat_paths.sort(key=lambda x: int(os.path.basename(x)[-2:]))
    df = pd.DataFrame(columns=('track_id', 'obj_type', 'track_type', 'volume', 'tho_num', 'center_x',
                               'center_y', 'velocity_x', 'velocity_y', 'bk_obj_type', 'frame_loss', 'file_name'))

    index = 0
    for i in cat_paths:
        # i是一个文件夹，文件夹下面有log.txt acu.csv 文件夹obs_data_trackid
        track_info = analysis_scene(i, is_show=False)
        if track_info.empty:
            logger.critical('文件夹{}所属场景无法解析'.format(i))
            continue
        df = df.append(track_info, ignore_index=True)
        index += 1
