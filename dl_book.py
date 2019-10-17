# coding:utf-8

from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re

def Get_book_url(page_html):
    '''
    通过html获取本页面所有书籍的url
    '''
    book_url = []
    
    soup = BeautifulSoup(page_html,'lxml')

    card_list = soup.find_all('a',title=re.compile(r'\S*'))
    print(card_list)

url = r'https://sobooks.cc/'

# 打开浏览器
dv = webdriver.Chrome()

# 打开网页
dv.get(url) 

# 获取最大页数
max_page = dv.find_element_by_css_selector("ul>li:last-child span").text

max_page = int(max_page[1:-1])

for i in range(max_page):
    # 组装页
    url = url + r'page/' + str(i+1)

    dv.get(url) 
    Get_book_url(dv.page_source)

dv.close()
    

