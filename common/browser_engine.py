# -*- coding: utf-8 -*-
'''
@Project : test_code
@File    : browser_engine.py
@Author  : 王白熊
@Data    ： 2020/10/13 16:31
'''

import os.path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config.web_config import Web_Config
from .Log import Logger

logger = Logger("BrowserEngine").getlog()


class BrowserEngine(object):
    dir = os.path.dirname(os.path.abspath('.'))
    chrome_driver_path = dir + '/tools/chromedriver.exe'
    ie_driver_path = dir + '/tools/IEDriverServer.exe'

    def __init__(self, driver):
        self.driver = driver

    # read the browser type from config.ini file, return the driver flag判断是否启动chrome静默模式
    def open_browser(self, driver):
        config = Web_Config()
        # file_path = os.path.dirname(os.getcwd()) + '/config/config.ini'
        file_path = os.path.dirname(os.path.abspath('.')) + '/config/config.ini'
        # config.read(file_path,encoding='UTF-8'), 如果代码有中文注释，用这个，不然报解码错误

        browser = config.get("browserType", "browserName")
        headless = config.get("browserType", "headless")  # 是否启动静默浏览器 目前只支持chrome
        logger.info("You had select %s browser, headless:%s." % (browser, headless))
        url = config.get("testServer", "URL")
        logger.info("The test server url is: %s" % url)

        if browser == "Firefox":
            driver = webdriver.Firefox()
            logger.info("Starting firefox browser.")
        elif browser == "Chrome":
            chrome_options = None
            if headless == 'True':
                # option = webdriver.ChromeOptions()
                # option.add_argument('headless')  # 静默模式 运行速度加快
                chrome_options = Options()
                chrome_options.add_argument('--headless')
            driver = webdriver.Chrome(self.chrome_driver_path, options=chrome_options)
            logger.info("Starting Chrome browser.")
        elif browser == "IE":
            driver = webdriver.Ie(self.ie_driver_path)
            logger.info("Starting IE browser.")

        driver.get(url)
        logger.info("Open url: %s" % url)
        driver.maximize_window()
        logger.info("Maximize the current window.")
        driver.implicitly_wait(10)
        logger.info("Set implicitly wait 10 seconds.")
        return driver

    def quit_browser(self):
        logger.info("Now, Close and quit the browser.")
        self.driver.quit()
