# -*- coding: utf-8 -*-
"""
@Project : test_code
@File    : compile_.py
@Author  : 王白熊
@Data    ： 2020/10/21 15:35
"""

import compileall
import py_compile
#
# 打包单个.py为pyc
py_compile.compile(r'D:/test_code/project/yuv2jpeg/yuyv2jpeg.py', r'D:/test_code/pyc/yuv2jpeg.pyc')
# 批量生产pyc文件
# compileall.compile_dir(r'H:/game')