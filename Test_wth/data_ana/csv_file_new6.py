# coding:utf-8
import csv
import pandas as pd
import re
import json
import os
import matplotlib.pyplot as plt
import argparse
import sys
from common.Log import Logger
import time

logger = Logger('csv_').getlog()

ACU_FILE_PATH_ERROR = 0
DRSU_FILE_PATH_ERROR = 1
FLAG = 2

strmatchcell = "HandleAcuVehicleState:vehicle state: "

fresult = open(r'D:\pycharm_ws\clip_csv_data\test\40.csv', 'w')

drsu_data = pd.DataFrame()
drsu_data_new = pd.DataFrame(
    columns=['ulFrame', 'ulSubFrame', 'dbTimestamp', 'stCenter.dbx', 'stCenter.dby', 'stCenter.dbz',
             'stvelocity.dbx', 'stvelocity.dby', 'stvelocity.dbz', 'dblength', 'dbwidth', 'dbheight',
             'ulLocalDrsuID', 'stObj_type', 'aulLane',
             'acu_db_time_stamp', 'acu_st_coordicate_dbx', 'acu_st_coordicate_dby',
             'acu_st_coordicate_dbz', 'acu_st_line_speed_x', 'acu_st_line_speed_y',
             'acu_st_line_speed_z'])

##绘制drsu,acu 速度曲线。
plt.rcParams['font.sans-serif'] = ['SimHei']  # 正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


# select_data = pd.DataFrame()
# json_data =[]
class Args(object):
    def __init__(self, flag):
        self.flag = flag
        self.drsu_path = 'D:\\pycharm_ws\\clip_csv_data\\test\\21_drsu_30.csv'
        self.acu_path = 'D:\\pycharm_ws\\clip_csv_data\\test\\30_come_3.csv'
        self.image_path = 'D:\\pycharm_ws\\clip_csv_data\\test\\picture\\'
        self.detal_time = 25.82
        self.drsu_location_x = 234804.2
        self.drsu_location_y = 3344694.69
        self.acu_location_x = 234804.2
        self.acu_location_y = 3344694.69


def read_acu_ori_data(csv_file_path, acu_select_data, detal_time):
    if not os.path.exists(csv_file_path):
        logger.error("file_path文件路径不存在。")
        return ACU_FILE_PATH_ERROR

    with open(csv_file_path, 'r') as f:  # 命令行带参数
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
                logger.info("tmp_dict: " + str(f.tell()))
                continue
            except:
                logger.info('')
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
                acu_select_data.loc[row_num, 'acu_db_time_stamp'] = float(tmp_dict['db_time_stamp'] - detal_time)
                acu_select_data.loc[row_num, 'acu_st_coordicate_dbx'] = float(tmp_dict['st_coordicate']['dbx'])
                acu_select_data.loc[row_num, 'acu_st_coordicate_dby'] = float(tmp_dict['st_coordicate']['dby'])
                acu_select_data.loc[row_num, 'acu_st_coordicate_dbz'] = float(tmp_dict['st_coordicate']['dbz'])
                acu_select_data.loc[row_num, 'acu_st_line_speed_x'] = float(tmp_dict['st_line_speed']['x'])
                acu_select_data.loc[row_num, 'acu_st_line_speed_y'] = float(tmp_dict['st_line_speed']['y'])
                acu_select_data.loc[row_num, 'acu_st_line_speed_z'] = float(tmp_dict['st_line_speed']['z'])

            else:
                return FLAG


def match_and_select_data(drsu_data_, acu_data_):
    for index, row_drsu in drsu_data_.iterrows():
        for i, row_acu in acu_data_.iterrows():
            if abs(row_drsu['dbTimestamp'] - float(row_acu['acu_db_time_stamp'])) < 0.1:
                # list_idx.append(i)
                row_drsu = pd.concat([row_drsu, row_acu], axis=0)
                # drsu_data_new.append(row_drsu, ignore_index=True)
                drsu_data_new.loc[index] = row_drsu  # dataframe插入行时必须要有对应的columns（不能为空的df）

                fresult.write(
                    str(row_acu['acu_st_coordicate_dbx']) + ', ' + str(i) + str(row_drsu['stCenter.dbx']) + '\n')
                break

    # 新增列
    drsu_data_new['drsu_location_x'] = args.drsu_location_x  # drsu_location_x
    drsu_data_new['drsu_location_y'] = args.drsu_location_y  # drsu_location_y
    drsu_data_new['detal_center_dbx'] = drsu_data_new['acu_st_coordicate_dbx'] - drsu_data_new['stCenter.dbx']
    drsu_data_new['detal_center_dby'] = drsu_data_new['acu_st_coordicate_dby'] - drsu_data_new['stCenter.dby']
    drsu_data_new['drsu_to_drsuloc_dbx'] = abs(drsu_data_new['drsu_location_x'] - drsu_data_new['stCenter.dbx'])
    drsu_data_new['drsu_to_drsuloc_dby'] = drsu_data_new['drsu_location_y'] - drsu_data_new['stCenter.dby']
    drsu_data_new['acu_to_drsuloc_dbx'] = abs(drsu_data_new['drsu_location_x'] - drsu_data_new['acu_st_coordicate_dbx'])
    drsu_data_new['acu_to_drsuloc_dby'] = drsu_data_new['drsu_location_y'] - drsu_data_new['acu_st_coordicate_dby']

    drsu_data_new['vel_percentage'] = abs(drsu_data_new['acu_st_line_speed_x'] - drsu_data_new['stvelocity.dbx'])
    drsu_data_new['vel_percentage'] = drsu_data_new['vel_percentage'] / drsu_data_new['acu_st_line_speed_x'] * 100


def draw_static_track_and_save_image(drsu_data, image_path):
    plt.xlabel("帧数：单位帧")
    plt.ylabel("acu和drsu位置偏差")
    plt.plot(drsu_data.shape, drsu_data['detal_drsu_acu_location_x'], "g", label="纵向位置偏差")
    plt.plot(drsu_data.shape, drsu_data['detal_drsu_acu_location_y'], "k", label="横向位置偏差")
    plt.legend(bbox_to_anchor=(0, 1), loc=2, borderaxespad=0)
    plt.grid()
    image_path = image_path + time.localtime(time.time()) + '.png'
    plt.savefig(image_path)
    plt.show()


def draw_track_and_save_image(drsu_data, image_path):
    plt.figure(figsize=(70, 70))
    ax4 = plt.subplot(221)
    axd = ax4.twiny()
    ax4.set_xlabel('纵向距离 单位：m')
    # plt.title("帧数")
    plt.xlabel("帧数")
    ax4.set_ylabel('速度 单位：m/s')
    axd.set_xlim(0, drsu_data['acu_to_drsuloc_dbx'][len(drsu_data) - 1])
    ax4.plot(drsu_data['acu_to_drsuloc_dbx'], drsu_data['stvelocity.dbx'], "r", label="drsu_纵向速度")
    ax4.plot(drsu_data['acu_to_drsuloc_dbx'], drsu_data['acu_st_line_speed_x'], "b", label="acu_纵向速度")
    ax4.plot(drsu_data['acu_to_drsuloc_dbx'], drsu_data['stvelocity.dby'], "g", label="drsu_横向速度")
    ax4.plot(drsu_data['acu_to_drsuloc_dbx'], drsu_data['acu_st_line_speed_y'], "k", label="acu_横向速度")
    ax4.legend(bbox_to_anchor=(-0.32, 1), loc=2, borderaxespad=0)
    ax4.grid()

    ax2 = plt.subplot(223)
    ax2.set_xlabel('纵向距离 单位：m')
    ax2.set_ylabel('速度差值百分比 单位：%')
    plt.plot(drsu_data['acu_to_drsuloc_dbx'], drsu_data['vel_percentage'], "r", label="drsu与acu纵向速度差值")
    ax2.legend(bbox_to_anchor=(0, 1), loc=2, borderaxespad=0)
    plt.savefig(image_path)
    plt.show()


if __name__ == '__main__':
    '''
    detal_time = 25.82
    drsu_location_x = 234804.2
    drsu_location_y = 3344694.69
    acu_ori_data_path = 'D:\\pycharm_ws\\clip_csv_data\\test\\40_come_1.csv'
    drsu_file_path = 'D:\\pycharm_ws\\clip_csv_data\\test\\31_drsudata_40km.csv'
    image_path = 'D:\\pycharm_ws\\clip_csv_data\\test\\picture\\40_come_1.jpg'
    '''
    acu_select_data = pd.DataFrame(columns=['acu_db_time_stamp', 'acu_st_coordicate_dbx', 'acu_st_coordicate_dby',
                                            'acu_st_coordicate_dbz', 'acu_st_line_speed_x', 'acu_st_line_speed_y',
                                            'acu_st_line_speed_z'])
    pd.set_option('display.max_columns', None)
    args = Args(1)
    if args.flag == 1:
        if not os.path.exists(args.drsu_path):
            logger.error("drsu file path is not exist！")
            sys.exit(0)
        if not os.path.exists(args.acu_path):
            logger.error("acu file path is not exist！")
            sys.exit(0)
        logger.info("read acu data: ")
        acu_flag = read_acu_ori_data(args.acu_path, acu_select_data, args.detal_time)
        if ACU_FILE_PATH_ERROR == acu_flag or FLAG == acu_flag:
            sys.exit(0)
        logger.info("read drsu data: ")
        drsu_data = pd.read_csv(args.drsu_path)

        if drsu_data.empty:
            logger.error("drsu 数据获取失败！")
            sys.exit(0)
        drsu_data.dropna(axis=1, how='all')
        logger.info("exe match_and_select_data function: ")
        match_and_select_data(drsu_data, acu_select_data)
        logger.info("draw track funcition:")
        draw_track_and_save_image(drsu_data_new, args.image_path)
    else:
        if not os.path.exists(args.drsu_path):
            logger.error("drsu file path is not exist!!！")
            sys.exit(0)
        logger.info("read drsu data: ")
        drsu_data = pd.read_csv(args.drsu_path)

        if drsu_data.empty:
            logger.error("drsu 数据获取失败！")
            sys.exit(0)
        drsu_data.dropna(axis=1, how='all')
        # 新增acu_data
        drsu_data['acu_location_x'] = args.acu_location_x
        drsu_data['acu_location_y'] = args.acu_location_y
        drsu_data['detal_drsu_acu_location_x'] = abs(drsu_data['acu_location_x'] - drsu_data['stCenter.dbx'])
        drsu_data['detal_drsu_acu_location_y'] = abs(drsu_data['acu_location_y'] - drsu_data['stCenter.dby'])
        logger.info(",,,", drsu_data['detal_drsu_acu_location_x'])
        logger.info("hangshu : %s" % len(drsu_data))
        logger.info("draw track funcition:")
        draw_static_track_and_save_image(drsu_data, args.image_path)
        logger.info("acu与摄像头纵向距离：", drsu_data['acu_location_x'] - args.drsu_location_x)
        logger.info("acu与摄像头横向距离：", drsu_data['acu_location_y'] - args.drsu_location_y)
