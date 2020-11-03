# -*- coding: utf-8 -*-
"""
@Project : code
@File    : yuyv2video.py
@Author  : 王白熊
@Data    ： 2020/10/23 11:21
"""
import os
import sys
import time
import cv2
import glob
from common.Log import Logger
from numpy import *
from PIL import Image
from tqdm import tqdm


def create_file(filename):
    path = filename[0:filename.rfind('/')]
    if not os.path.isdir(path):
        os.makedirs(path)
    if not os.path.isfile(filename):
        fd = open(filename, mode='w', encoding='utf-8')
        fd.close()
    else:
        pass


logger = Logger('yuv_video_switch').getlog()
screenLevels = 255.0


def yuyv_to_rgb(filename, rows, cols, seek_num=0):
    """
    :param filename: 文件名
    :param rows: 图像行数
    :param cols: 图像列数
    :param seek_num: 文件偏移量
    :return:
    """
    logger.debug('读取文件:%s' % filename)
    fp = open(filename, 'rb')
    time_stamp = []
    for i in range(16):
        time_stamp.append(ord(fp.read(1)))
    logger.debug('文件时间戳为:%s' % time_stamp)
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
        logger.info('创建目录：%s' % dir)
        os.makedirs(str(dir))
    return str(dir)


def yuyv_to_jpeg(file_dir, width, height):
    start_time = time.time()
    dest_dir = os.path.join(os.path.dirname(file_dir), 'dest_jpeg')
    check_dir(dest_dir)
    size_all = 0  # 文件压缩前总大小
    size_all2 = 0  # 文件压缩后总大小
    files = glob.glob(os.path.join(file_dir, '*'))
    pbar = tqdm(total=len(files), desc='yuyv转jpeg', ncols=80)
    for i in files:
        size1 = os.path.getsize(i)
        if size1 != 4147216:
            logger.warning('文件%s大小有误' % i)
            continue
        rgb_bytes = yuyv_to_rgb(i, height, width, 16)
        img = Image.frombytes("RGB", (width, height), bytes(rgb_bytes))
        jpg_name = os.path.basename(i)
        file_path = os.path.join(dest_dir, jpg_name + '.jpg')
        img.save(file_path, "JPEG", quality=95)
        size2 = os.path.getsize(file_path)
        size_all += size1
        size_all2 += size2
        pbar.update(1)
        # logger.debug('保存图片：%s.jpg，压缩后大小：%s,压缩比：%0.2f' % (i, size2, size1 / size2))
    pbar.close()
    end_time = time.time()
    logger.info('\n>> 图片转换累计用时 : ' + str(end_time - start_time) + ' s')
    logger.info('文件压缩前总大小:%u,:压缩后总大小：%u,压缩比：%0.2f' % (size_all, size_all2, size_all / size_all2))


def jpeg2video(imgs_dir):
    start_time = time.time()
    fps = 10
    # 指定视频编码格式为H264
    save_dir = os.path.join(os.path.dirname(imgs_dir), 'dest_video')
    check_dir(save_dir)
    save_name = os.path.join(save_dir, 'dest_h264.mp4')
    fourcc = cv2.VideoWriter_fourcc(*"H264")
    video_writer = cv2.VideoWriter(save_name, fourcc, fps, (1920, 1080))
    # 获取文件夹下所有以.jpg结尾的文件名
    imgs = glob.glob(os.path.join(imgs_dir, '*.jpg'))
    # 对文件利用文件中的数字进行排序
    # imgs.sort(key=lambda x: int(x.split('/')[-1].split('_')[-1].strip('.jpg')))
    imgs.sort(key=lambda x: int(x.split('/')[-1].split('_')[-1].strip('.jpg')))
    pbar = tqdm(total=len(imgs), desc='jpeg转视频', ncols=80)
    for i in imgs:
        frame = cv2.imread(i)
        video_writer.write(frame)
        pbar.update(1)
    video_writer.release()
    end_time = time.time()
    logger.info('\n>> 图片转视频用时 : ' + str(end_time - start_time) + ' s')
    logger.info('转换后视频大小：%s' % os.path.getsize(save_name))
    pbar.close()


def video2jpeg(video_dir):
    start_time = time.time()
    video_name = os.path.join(video_dir, 'out.avi')
    cap = cv2.VideoCapture(video_name)  # 加载视频文件
    cap_num = cap.get(7)  # 获取视频总帧数
    cap_width = math.ceil(cap.get(3))  # 获取视频帧宽度（横）
    cap_height = math.ceil(cap.get(4))  # 获取视频帧高度（竖）
    cap_fps = math.ceil(cap.get(5))  # 获取视频帧率
    logger.info('视频数据：帧数：%s，分辨率：%s*%s, 帧率：%s' % (cap_num, cap_width, cap_height, cap_fps))
    cap_cnt = 0
    pbar = tqdm(total=cap_num, desc='视频转jpeg', ncols=80)
    flag, frame = cap.read()  # 读取图片
    pbar.update(1)
    while flag:
        dest_path = os.path.join(os.path.dirname(video_dir), 'dest_jpeg_')
        check_dir(dest_path)
        img_name = os.path.join(dest_path, str(cap_cnt) + '.jpg')  # 图片保存目录
        cv2.imwrite(img_name, frame)
        cap_cnt = cap_cnt + 1
        flag, frame = cap.read()
        pbar.update(1)

    cap.release()
    pbar.close()
    end_time = time.time()
    logger.info('\n>> 视频转图片用时:%s s ' % str(end_time - start_time))


def _jpg_video_switch():
    from argparse import ArgumentParser
    arg_parser = ArgumentParser()
    arg_parser.add_argument('file_dir', help='the path of yuv.')
    arg_parser.add_argument('--mode', required=False, default=0, type=int,
                            help='the mode of switch, 0:yuv2video; 1:video2jpg; 2:yuv2jpeg; 3:jpeg2video,')
    arg_parser.add_argument('--width', required=False, default=1920, type=int, help='the width of picture.')
    arg_parser.add_argument('--height', required=False, default=1080, type=int, help='the width of picture.')
    args = arg_parser.parse_args()
    file_dir, mode, width, height = args.file_dir, args.mode, args.width, args.height
    logger.info('参数：文件目录：%s, 模式：%s, 像素：%s * %s' % (file_dir, mode, width, height))
    # yuv转jpg
    if mode == 0:
        yuyv_to_jpeg(file_dir, width, height)
        imgs_dir = os.path.join(os.path.dirname(file_dir), 'dest_jpeg')
        jpeg2video(imgs_dir)
    elif mode == 1:
        video2jpeg(file_dir)
    elif mode == 2:
        yuyv_to_jpeg(file_dir, width, height)
    elif mode == 3:
        jpeg2video(file_dir)


if __name__ == '__main__':
    _jpg_video_switch()
