# coding:utf-8

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
from bs4 import BeautifulSoup
import re
import requests
import json
import pyautogui

url = r'http://ctfile.sobooks.cc/dir/14804066-35905755-2c310f'

email = r'yubo_5698@163.com'
passkey = r'BaiDu0808'

driver = webdriver.Chrome()
driver.get(url)

time.sleep(3)

# 点击全选文件复选框
select = driver.find_element_by_css_selector(r'#checkbox-bulk-purchases-select')
driver.execute_script("arguments[0].click();", select)

# 点击客户端下载
select = driver.find_element_by_xpath(r'//*[@id="dashboard-actions"]/button[1]')
driver.execute_script("arguments[0].click();", select)

time.sleep(3)


pass