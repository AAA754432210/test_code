# -*- coding: utf-8 -*-
'''
@Project : test_code
@File    : weather.py
@Author  : 王白熊
@Data    ： 2020/10/13 14:13
'''

import requests
import json
from .Log import Logger

logger = Logger('Weather').getlog()

def get_cur_weather():
    url = 'https://www.tianqiapi.com/api/?'
    # https://yiketianqi.com/api?version=v61&appid=45675817&appsecret=tGlJ6F8D
    # APPID：45675817  APPSecret：tGlJ6F8D
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'}
    params = {
        'version': 'v61',
        'appid': '45675817',
        'appsecret': 'tGlJ6F8D',
        'city': '杭州',
    }

    res = requests.get(url, params=params, headers=headers)
    res.encoding = 'utf-8'
    # print(type(res.text))
    # print(res.text)
    # print(json.loads(res.text))
    logger.debug('天气：%s' % json.loads(res.text)['wea'])
    return json.loads(res.text)['wea_img']
