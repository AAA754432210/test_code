# -*- coding: utf-8 -*-
"""
@Project : test_code
@File    : referrece_analysis.py
@Author  : 王白熊
@Data    ： 2020/11/11 16:51
"""
import json
import os
from glob import glob
import pandas as pd
import matplotlib.pyplot as plt
import logging
import time
import sys

# from common.Log import Logger

plt.rcParams['font.sans-serif'] = ['SimHei']  # 正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


def create_file(filename):
    path = filename[0:filename.rfind('/')]
    if not os.path.isdir(path):
        os.makedirs(path)
    if not os.path.isfile(filename):
        fd = open(filename, mode='w', encoding='utf-8')
        fd.close()
    else:
        pass


class Logger(object):
    def __init__(self, logger_name):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        path = os.path.dirname(os.path.abspath(__file__))
        rq = time.strftime('%Y%m%d', time.localtime(time.time()))
        log_file = path + rq + '.log'
        create_file(log_file)

        # 定制输出格式
        formatter = logging.Formatter('%(levelname)s - %(message)s')

        handler = logging.FileHandler(log_file, encoding='utf-8', mode='a+')  # 输出到log文件
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(formatter)

        ch = logging.StreamHandler(sys.stdout)  # 输出到控制台
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)

        self.logger.addHandler(handler)
        self.logger.addHandler(ch)

    def getlog(self):
        return self.logger


logger = Logger('reference').getlog()


def read_reference_single(json_file):
    with open(json_file) as fp:
        data_str = fp.read()
        data_list = json.loads(data_str)
    return data_list


def read_reference(file_dir):
    """
    解析json文件脚本
    :param file_dir: json文件夹路径，解析后结果会生成一个同名+parsed.csv的文件
    :return:
    """
    reference_data = pd.DataFrame()
    files = glob(os.path.join(file_dir, '*.json'))
    row_num = 0
    logger.info('异常类型一: fx,fy大于5000，任意std(%)值小于1\r\n'
                '异常类型二: fx,fy大于7000，fy_std(%)或fx_std(%)值小于1\r\n'
                '异常类型二: fx,fy大于7000，cx_std(%)或cy_std(%)值小于1')
    for i in files:
        data_list = read_reference_single(i)
        num = int(os.path.basename(i).split('.')[0])
        reference_data.loc[row_num, 'num'] = num
        if data_list['fx'] < 5000 and data_list['fy'] < 5000:
            if data_list['segma_fx']['std(%)'] > 1 or \
                    data_list['segma_fy']['std(%)'] > 1 or \
                    data_list['segma_cx']['std(%)'] > 1 or \
                    data_list['segma_cy']['std(%)'] > 1:
                logger.error('序号{}内参数据异常，异常类型: 一， 具体参数：\r\n fx:{},fy:{},cx:{},cy:{},fy_std(%):{},fx_std(%):{},cx_std(%):{},cy_std(%):{},'
                               .format(num, data_list['fx'], data_list['fy'], data_list['cx'], data_list['cx'], data_list['cy'],
                                       data_list['segma_fx']['std(%)'], data_list['segma_fy']['std(%)'], data_list['segma_cx']['std(%)'],
                                       data_list['segma_cy']['std(%)']))
        elif data_list['fx'] > 7000 and data_list['fy'] > 7000:
            if data_list['segma_fx']['std(%)'] > 1 or \
                    data_list['segma_fy']['std(%)'] > 1:
                logger.error(
                    '序号{}内参数据异常，异常类型: 二， 具体参数：\r\n fx:{},fy:{},cx:{},cy:{},fy_std(%):{},fx_std(%):{},cx_std(%):{},cy_std(%):{},'
                    .format(num, data_list['fx'], data_list['fy'], data_list['cx'], data_list['cx'], data_list['cy'],
                            data_list['segma_fx']['std(%)'], data_list['segma_fy']['std(%)'],
                            data_list['segma_cx']['std(%)'],
                            data_list['segma_cy']['std(%)']))
            elif data_list['segma_cx']['std(%)'] > 1 or \
                    data_list['segma_cy']['std(%)'] > 1:
                logger.warning(
                    '序号{}内参数据异常，异常类型: 三， 具体参数：\r\n fx:{},fy:{},cx:{},cy:{},fy_std(%):{},fx_std(%):{},cx_std(%):{},cy_std(%):{},'
                    .format(num, data_list['fx'], data_list['fy'], data_list['cx'], data_list['cx'], data_list['cy'],
                            data_list['segma_fx']['std(%)'], data_list['segma_fy']['std(%)'],
                            data_list['segma_cx']['std(%)'],
                            data_list['segma_cy']['std(%)']))

        reference_data.loc[row_num, 'fx'] = data_list['fx']
        reference_data.loc[row_num, 'fy'] = data_list['fy']
        reference_data.loc[row_num, 'cx'] = data_list['cx']
        reference_data.loc[row_num, 'cy'] = data_list['cy']
        reference_data.loc[row_num, 'k1'] = data_list['k1']
        reference_data.loc[row_num, 'k2'] = data_list['k2']
        reference_data.loc[row_num, 'p1'] = data_list['p1']
        reference_data.loc[row_num, 'p2'] = data_list['p2']
        reference_data.loc[row_num, 'std_fx'] = data_list['segma_fx']['std']
        reference_data.loc[row_num, 'std(%)_fx'] = data_list['segma_fx']['std(%)']
        reference_data.loc[row_num, 'std_fy'] = data_list['segma_fy']['std']
        reference_data.loc[row_num, 'std(%)_fy'] = data_list['segma_fy']['std(%)']
        reference_data.loc[row_num, 'std_cx'] = data_list['segma_cx']['std']
        reference_data.loc[row_num, 'std(%)_cx'] = data_list['segma_cx']['std(%)']
        reference_data.loc[row_num, 'std_cy'] = data_list['segma_cy']['std']
        reference_data.loc[row_num, 'std(%)_cy'] = data_list['segma_cy']['std(%)']
        reference_data.loc[row_num, 'std_k1'] = data_list['segma_k1']['std']
        reference_data.loc[row_num, 'std(%)_k1'] = data_list['segma_k1']['std(%)']
        reference_data.loc[row_num, 'std_k2'] = data_list['segma_k2']['std']
        reference_data.loc[row_num, 'std(%)_k2'] = data_list['segma_k2']['std(%)']
        reference_data.loc[row_num, 'std_p1'] = data_list['segma_p1']['std']
        reference_data.loc[row_num, 'std(%)_p1'] = data_list['segma_p1']['std(%)']
        reference_data.loc[row_num, 'std_p2'] = data_list['segma_p2']['std']
        reference_data.loc[row_num, 'std(%)_p2'] = data_list['segma_p2']['std(%)']
        row_num += 1
    file_parsed = os.path.join(os.path.dirname(file_dir), os.path.basename(file_dir) + 'parsed.csv')
    reference_data.to_csv(file_parsed, encoding='gbk', sep=',', index=False, header=True)


Listcolors = ['red', 'blue', 'green', 'cyan', 'magenta', 'orange', 'darkred', 'black']


def draw(draw_file, is_show=True):
    """
    cx,cy等前八个数据画图
    :param draw_file: read_reference解析后生成的csv文件路径
    :param is_show: 是否显示图片
    :return:
    """
    pf = pd.read_csv(draw_file)
    # 8个数据一张图
    fig = plt.figure(figsize=(54, 54))
    for i in range(1, pf.shape[1] // 2 + 1):
        ax = fig.add_subplot(3, 3, i)
        ax.set(title=pf.columns[i], )
        ax.scatter(pf.iloc[:, 0], pf.iloc[:, i], c=Listcolors[i % 7])
        ver = pf.iloc[:, i].mean()
        print(ver)
        ax.plot(pf.iloc[:, 0], [ver for _ in range(pf.shape[0])], c=Listcolors[i % 7 + 1], linewidth=0.5,
                linestyle='--')
        ax.set_xticks(pf.iloc[:, 0].to_list())
    file_save = os.path.join(os.path.dirname(draw_file), os.path.basename(draw_file).split('.')[0] + '1')
    plt.savefig(file_save)
    if is_show:
        plt.show()
        plt.pause(0.1)
    plt.close()


def draw1(draw_file, is_show=True):
    """
    八个std数据画图
    :param draw_file: read_reference解析后生成的csv文件路径
    :param is_show: 是否显示图片
    :return:
    """
    pf = pd.read_csv(draw_file)
    # 8个数据一张图
    fig = plt.figure(figsize=(54, 54))
    for i in range(1, pf.shape[1] // 2 + 1):
        ax = fig.add_subplot(3, 3, i)
        ax.set(title=pf.columns[i + 8], )
        ax.scatter(pf.iloc[:, 0], pf.iloc[:, 8 + i], c=Listcolors[i % 7])
        ver = pf.iloc[:, 8 + i].mean()
        ax.plot(pf.iloc[:, 0], [ver for _ in range(pf.shape[0])], c=Listcolors[i % 7 + 1], linewidth=0.5,
                linestyle='--')
        ax.set_xticks(pf.iloc[:, 0].to_list())
    file_save = os.path.join(os.path.dirname(draw_file), os.path.basename(draw_file).split('.')[0] + '2')
    plt.savefig(file_save)
    if is_show:
        plt.show()
        plt.pause(0.1)
    plt.close()


def draw2(draw_file, is_show=True):
    """
    以两个数据成对画图如cx,cy,四个图
    :param draw_file: read_reference解析后生成的csv文件路径
    :param is_show: 是否显示图片
    :return:
    """
    pf = pd.read_csv(draw_file)
    # 8个数据一张图
    fig = plt.figure(figsize=(48, 48))
    for i in range(0, pf.shape[1] // 4):
        ax = fig.add_subplot(2, 2, i + 1)
        ax.set(title=pf.columns[i * 2 + 1] + pf.columns[i * 2 + 2], xlabel=pf.columns[i * 2 + 1],
               ylabel=pf.columns[i * 2 + 2], )
        ax.scatter(pf.iloc[:, i * 2 + 1], pf.iloc[:, i * 2 + 2], c=Listcolors[i % 7])
        for j in range(pf.shape[0]):
            plt.annotate(int(pf.iloc[j, 0]), xy=(pf.iloc[j, i * 2 + 1], pf.iloc[j, i * 2 + 2]))
        # ax.set_xticks(pf.iloc[:, 0].to_list())
    file_save = os.path.join(os.path.dirname(draw_file), os.path.basename(draw_file).split('.')[0] + '3')
    plt.savefig(file_save)
    if is_show:
        plt.show()
        plt.pause(0.1)
    plt.close()


def draw3(draw_file, is_show=True):
    """
    以两个数据成对画图如std_cx,std_cy,四个图
    :param draw_file: read_reference解析后生成的csv文件路径
    :param is_show: 是否显示图片
    :return:
    """
    pf = pd.read_csv(draw_file)
    # 8个数据一张图
    fig = plt.figure(figsize=(48, 48))
    for i in range(0, pf.shape[1] // 4):
        ax = fig.add_subplot(2, 2, i + 1)
        ax.set(title=pf.columns[i * 2 + 9] + pf.columns[i * 2 + 10], xlabel=pf.columns[i * 2 + 9],
               ylabel=pf.columns[i * 2 + 10])
        ax.scatter(pf.iloc[:, i * 2 + 9], pf.iloc[:, i * 2 + 10], c=Listcolors[i % 7])
        for j in range(pf.shape[0]):
            plt.annotate(int(pf.iloc[j, 0]), xy=(pf.iloc[j, i * 2 + 9], pf.iloc[j, i * 2 + 10]))
        # ax.set_xticks(pf.iloc[:, 0].to_list())
    file_save = os.path.join(os.path.dirname(draw_file), os.path.basename(draw_file).split('.')[0] + '4')
    plt.savefig(file_save)
    if is_show:
        plt.show()
        plt.pause(0.1)
    plt.close()


if __name__ == '__main__':
    # json_file = r'D:\data\标定参数\8mm\336.json'
    # data_list = read_reference_single(json_file)
    file_dir = r'D:\data\标定参数\8mm'
    read_reference(file_dir)
    # draw_file = r'D:\data\标定参数\8mmparsed.csv'
    # draw(draw_file)
    # draw1(draw_file)
    # draw2(draw_file)
    # draw3(draw_file)
