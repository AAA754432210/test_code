import cv2
import math
import os
import time

def check_dir(dir):
    if not os.path.exists(str(dir)):
        os.makedirs(str(dir))
    return str(dir)


start_time = time.time()
cap = cv2.VideoCapture('dest.mp4')  # 加载视频文件
cap_num = cap.get(7)  # 获取视频总帧数
cap_width = math.ceil(cap.get(3))  # 获取视频帧宽度（横）
cap_height = math.ceil(cap.get(4))  # 获取视频帧高度（竖）
cap_fps = math.ceil(cap.get(5))  # 获取视频帧率
# print(cap_num, cap_width, cap_height, cap_fps)
cap_count = 0
while cap_num:
    cap_count = cap_count + 1
    cap_num = math.floor(cap_num / 10)

fix = '%0' + str(cap_count) + 'd'  # 得到图片保存的前缀，比如001.png，0001.png
cap_cnt = 1

flag, frame = cap.read()  # 读取图片
while flag:
    dest_path = '/home/broadxt/picture_1/dest_imgs/'
    check_dir(dest_path)
    path = dest_path + str(fix % cap_cnt) + '.jpg'  # 图片保存目录
    # print(path)
    cv2.imwrite(path, frame)
    cap_cnt = cap_cnt + 1
    flag, frame = cap.read()

cap.release()
end_time = time.time()
print('\n>> cost : ' + str(end_time - start_time) + ' s')

# 10s