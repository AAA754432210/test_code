# -*- coding: utf-8 -*-
"""
@Project : test_code
@File    : yuyv2jpeg.py
@Author  : 王白熊
@Data    ： 2020/10/21 11:35
"""
import time
from numpy import *
from PIL import Image
from common.Log import Logger
import os
import pyinstaller

logger = Logger('YUYVtoRGB').getlog()
screenLevels = 255.0


def yuyv_to_rgb(filename, rows, cols, seek_num=0):
    """
    :param filename: 文件名
    :param rows: 图像行数
    :param cols: 图像列数
    :param seek_num: 文件偏移量
    :return:
    """
    fp = open(filename, 'rb')
    time_stamp = []
    for i in range(16):
        time_stamp.append(ord(fp.read(1)))
    logger.debug('文件：%s的时间戳为:%s' % (filename, time_stamp))
    fp.seek(seek_num, 0)
    rgb_bytes = bytearray(rows * cols * 3)
    red_index = 0
    green_index = 1
    blue_index = 2
    for m in range(rows):
        for n in range(int(cols / 2)):
            Yt1 = ord(fp.read(1))
            Ut = ord(fp.read(1))
            Yt2 = ord(fp.read(1))
            Vt = ord(fp.read(1))
            for i in [Yt1, Yt2]:
                R = int(1.164 * (i - 16) + 1.787 * (Vt - 128))
                G = int(1.164 * (i - 16) - 0.531 * (Vt - 128) - 0.213 * (Ut - 128))
                B = int(1.164 * (i - 16) + 2.112 * (Ut - 128))
                R = 255 if (R > 255) else (0 if (R < 0) else R)
                G = 255 if (G > 255) else (0 if (G < 0) else G)
                B = 255 if (B > 255) else (0 if (B < 0) else B)
                rgb_bytes[red_index] = R
                rgb_bytes[green_index] = G
                rgb_bytes[blue_index] = B
                red_index += 3
                green_index += 3
                blue_index += 3
    fp.close()
    return rgb_bytes


def check_dir(dir):
    if not os.path.exists(str(dir)):
        os.makedirs(str(dir))
    return str(dir)


def _yuyv_to_jpeg():
    from argparse import ArgumentParser
    start_time = time.time()
    arg_parser = ArgumentParser()
    arg_parser.add_argument('file_dir', help='the path of yuv.')
    arg_parser.add_argument('width', default=1920, type=int, help='the width of picture.')
    arg_parser.add_argument('height', default=1080, type=int, help='the width of picture.')
    args = arg_parser.parse_args()
    file_dir, width, height = args.file_dir, args.width, args.height
    dest_dir = file_dir + '/dest/'
    check_dir(dest_dir)
    sizeall = os.path.getsize(file_dir)
    for dir, folder, file in os.walk(file_dir):
        # 遍历单个文件
        for i in file:
            size1 = os.path.getsize(file_dir + '/' + i)
            rgb_bytes = yuyv_to_rgb(file_dir + '/' + i, height, width, 16)
            img = Image.frombytes("RGB", (width, height), bytes(rgb_bytes))
            file_path = dest_dir + '/' + i + '.jpg'
            img.save(file_path, "JPEG", quality=95)
            size2 = os.path.getsize(file_path)
            logger.info('保存图片：%s' % i + '.jpg')
            logger.info('size1:%u,size2:%u,%0.2f' % (size1, size2, size1/size2))
    end_time = time.time()
    logger.info('\n>> cost : ' + str(end_time - start_time) + ' s')
    sizeall2 = os.path.getsize(dest_dir)
    logger.info('size1:%u,size2:%u,%0.2f' % (sizeall, sizeall2, sizeall/sizeall2))

if __name__ == '__main__':
    _yuyv_to_jpeg()
