# -*- coding: utf-8 -*-
"""
@Project : test_code
@File    : compile_1.py
@Author  : 王白熊
@Data    ： 2020/10/16 9:52
"""

import py_compile
import compileall

py_compile.compile(r'C:\Users\Admin\Documents\code\EXTODB.py')
compileall.compile_dir(r'C:\Users\Admin\Documents\code')