# -*- coding: utf-8 -*-
'''
@Project : test_code
@File    : baidu_upload.py
@Author  : 王白熊
@Data    ： 2020/10/13 14:22
'''

from bypy import ByPy
import os
import datetime
from common.Log import Logger

logger = Logger('Baidu').getlog()

def create_baidu_dir():
    bp = ByPy()
    for i in range(810020001, 810020026):
        dir_name = '/xiaoshandata/' + str(i)
        bp.mkdir(remotepath=dir_name)


# 获取文件的大小,结果保留两位小数，单位为MB
def get_FileSize(filePath):
    fsize = os.path.getsize(filePath)
    fsize = fsize / float(1024 * 1024)
    return round(fsize, 2)


def upload_dir(local_path, remote_path):
    print('开始上传文件：%s' % (local_path.split('\\')[-1]))
    start = datetime.datetime.now()  # 计时开始
    bp = ByPy()
    if remote_path:
        bp.mkdir(remotepath=remote_path)
    if bp.upload(localpath=local_path, remotepath=remote_path, ondup='newcopy'):
        end = datetime.datetime.now()  # 计时结束
        dir_size = get_FileSize(local_path)
        logger.info(
            "文件发送完成：本地路径：%s,远程文件夹：%s 大小:%sMB,花费时间%s" % (local_path, remote_path, dir_size, str((end - start).seconds)))
        if os.path.exists(local_path):  # 如果文件存在
            # 删除文件，可使用以下两种方法。
            os.remove(local_path)
            logger.info('删除本地文件')
    else:
        logger.info('上传百度云失败')


if __name__ == '__main__':
    create_baidu_dir()
    # upload_dir('D:\\xiaoshandata\\drsu810020002_202009011633_yun_1camera.tar.gz', '/xiaoshandata/810020002/20200901')
