# -*- coding: utf-8 -*-
"""
@Project : code
@File    : imgs2video.py
@Author  : 王白熊
@Data    ： 2020/10/22 13:34
"""
import glob
import cv2
import os
import time


def imgs2video(imgs_dir, save_name):
    start_time = time.time()
    fps = 10
    # fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    # fourcc = cv2.VideoWriter_fourcc(*"MJPG")  # avi
    # fourcc = cv2.VideoWriter_fourcc('F', 'L', 'V', '1')
    # https://www.fourcc.org/codecs.php
    # cv2.VideoWriter_fourcc('M','J','P','G') = motion-jpeg codec
    # cv2.VideoWriter_fourcc('P','I','M','1') = MPEG-1 codec
    # cv2.VideoWriter_fourcc('M', 'P', '4', '2') = MPEG-4.2 codec
    # cv2.VideoWriter_fourcc('D', 'I', 'V', '3') = MPEG-4.3 codec
    # cv2.VideoWriter_fourcc('D', 'I', 'V', 'X') = MPEG-4 codec
    # cv2.VideoWriter_fourcc('U', '2', '6', '3') = H263 codec
    # cv2.VideoWriter_fourcc('I', '2', '6', '3') = H263I codec
    # cv2.VideoWriter_fourcc('F', 'L', 'V', '1') = FLV1 codec
    #
    fourcc = cv2.VideoWriter_fourcc(*"H264")
    video_writer = cv2.VideoWriter(save_name, fourcc, fps, (1920, 1080))
    imgs = glob.glob(os.path.join(imgs_dir, '*.jpg'))
    imgs.sort(key=lambda x: int(x.split('/')[-1].split('_')[-1].strip('.jpg')))
    for i in imgs:
        frame = cv2.imread(i)
        video_writer.write(frame)
    # print(type(frame), len(frame), len(frame[0]), len(frame[0][0]))

    video_writer.release()
    end_time = time.time()
    print('\n>> cost : ' + str(end_time - start_time) + ' s')


if __name__ == '__main__':
    imgs2video('/home/broadxt/picture_1/dest', '/home/broadxt/picture_1/dest_video/dest_h264.avi')

