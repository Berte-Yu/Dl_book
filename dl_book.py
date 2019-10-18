# coding:utf-8

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
from bs4 import BeautifulSoup
import re
import requests

def Get_max_page(html):
    soup = BeautifulSoup(html,'lxml')
    page_html = soup.find('div', class_='pagination')
    page_html_str = list(page_html.ul.children)[-1]
    return int(page_html_str.span.text[1:-1])
    
    

def Get_book_url(page_html):
    '''
    通过html获取本页面所有书籍的url
    '''
    book_url = []
    
    soup = BeautifulSoup(page_html,'lxml')
    card_items = soup.find_all('div', class_='card-item')

    for card in card_items:
        book_url.append(card.h3.a['href'])

    book_url = list(set(book_url))
    return book_url

def Get_Extraction_code(url):
    soup = BeautifulSoup(url,'lxml')
    passkey = soup.find('div', class_='e-secret')
    print(passkey)
    print(passkey.b.text)
    return passkey.b.text[-4:]

def baidu_down(url, key):
    chrome = webdriver.Chrome()
    chrome.implicitly_wait(20)
    chrome.get(url)

    # 获取提取密码
    chrome.find_element_by_xpath(r"/html/body/section/div[2]/div/article/div[2]/form/input[1]").send_keys(key)
    tijiao = chrome.find_element_by_xpath(r"/html/body/section/div[2]/div/article/div[2]/form/input[2]")
    chrome.execute_script("arguments[0].click();",tijiao)
    ext_code = Get_Extraction_code(chrome.page_source)

    time.sleep(5)

    # 打开百度云进行登录并转存
    tijiao = chrome.find_element_by_xpath(r"/html/body/section/div[2]/div/article/table/tbody/tr[3]/td/a[1]")
    chrome.execute_script("arguments[0].click();",tijiao)

    time.sleep(3)
    
    # 输入提取码
    chrome.find_element_by_xpath(r'//*[@id="mkco9Kb"]').send_keys(ext_code)
    tijiao = chrome.find_element_by_xpath(r'//*[@id="grmvE3Vo"]/a/span/span')
    chrome.execute_script("arguments[0].click();",tijiao)

    # 点击全选
    tijiao = chrome.find_element_by_xpath(r'//*[@id="shareqr"]/div[2]/div[2]/div/ul[1]/li[1]/div/span[1]')
    chrome.execute_script("arguments[0].click();",tijiao)

    #点击保存至网盘
    tijiao = chrome.find_element_by_xpath(r'//*[@id="bd-main"]/div/div[1]/div/div[2]/div/div/div[2]/a[1]/span/span')
    chrome.execute_script("arguments[0].click();",tijiao)

    pass


url = r'https://sobooks.cc/'
passkey = '20190808'

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}

response = requests.get(url,headers=headers)

if response.status_code != 200:
    print("get请求失败")
    quit()

max_page = Get_max_page(response.text)

print("最大页数是：%d" % max_page)

time.sleep(3)

for i in range(max_page):
    # 组装页
    url = url + r'page/' + str(i+1)
    print('开始获取第%d页书籍信息' % (i+1))
    
    response = requests.get(url,headers=headers) 
    if response.status_code != 200:
        quit()

    #获取当前页的所有书的url
    books_url = Get_book_url(response.text)

    print("此页一共有%d本书" % len(books_url))
    
    time.sleep(3)

    k=0
    for b_url in books_url:
        print("当前转存第%d本书" %(k+1))
        k=k+1
        baidu_down(b_url, passkey)
        time.sleep(3)

dv.close()
    

