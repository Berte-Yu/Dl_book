# coding:utf-8

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
from bs4 import BeautifulSoup
import re
import requests
import json
import pyautogui
import random
import logging
import os

USER_AGENTS = [
        "Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1"
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50",
        "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
        "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
        "Mozilla/4.0 (compatible; MSIE 5.0; Windows NT)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12 "
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
        ]

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

def save_book_url():
    url = r'https://sobooks.cc/'
    passkey = '20190808'

    headers = {"User-Agent": random.choice(USER_AGENTS)}

    response = requests.get(url,headers=headers)
    
    if response.status_code != 200:
        print("get请求失败")
        return -1

    max_page = Get_max_page(response.text)

    for i in range(max_page):
        # 组装页
        page_url = url + r'page/' + str(i+1)
        print('开始获取第%d页书籍信息' % (i+1))
        
        response = requests.get(page_url,headers=headers) 
        if response.status_code != 200:
            return

        #获取当前页的所有书的url
        books_url = Get_book_url(response.text)

        print("此页一共有%d本书" % len(books_url))
        
        with open('book_url.txt','a') as fp:
            for book in books_url:
                fp.write(book)
                fp.write('\n')

        time.sleep(random.randint(1,4))

def url_del_repeat():
    book_url = []
    with open('book_url.txt','r') as fp:
        while True:
            line = fp.readline()
            if len(line) < 3:
                break
            book_url.append(line)
        book_url = list(set(book_url))

    with open('url_del_rep_repeat.txt','w') as fp:
        for url in book_url:
            fp.write(url)

def save_book_dl_url():
    logger = logging.getLogger(__name__)
    logger.setLevel(level = logging.INFO)
    log_handler = logging.FileHandler('log.txt',encoding='utf-8')
    log_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)

    chrome_options = webdriver.ChromeOptions()
    profile_dir=r"C:\Users\ALICE\AppData\Local\Google\Chrome\User Data"
    chrome_options.add_argument("user-data-dir="+os.path.abspath(profile_dir))
    
    # 打开Chrome
    driver = webdriver.Chrome(chrome_options=chrome_options)

    driver.implicitly_wait(20)
    cnt = 0
    with open('url_del_rep_repeat.txt','r') as fp_rep_book:
        while True:
            cnt = cnt+1
            logger.info("开始第%d次"%cnt)
            rep_book_url = fp_rep_book.readline()
            
            if len(rep_book_url) < 3:
                logger.error("全部完成")
                driver.quit()
                return 0

            logger.error("start: %s"%rep_book_url)
            try:
                headers = {"User-Agent": random.choice(USER_AGENTS)}
                data = {'e_secret_key': '20190808'}
                response = requests.post(rep_book_url[:-1],data=data, headers=headers)
            except:
                logger.error("post_断言请求失败")
                continue

            if response.status_code != 200:
                logger.error("post_状态码非200")
                continue

            soup = BeautifulSoup(response.text,'lxml')

            # 寻找百度网盘链接
            try:
                card_items = soup.find('table',class_='dltable')

                tr = list(card_items.tbody.children)[-1]
                all_tag = list(tr.td.children)

                # 下载框内的标签的数量
                all_tag_num = len(all_tag) 
                if all_tag_num > 2:
                    all_tag = all_tag[2:all_tag_num]
                else:
                    logger.error("下载表格内没有有效链接")
                    continue

                for tag in all_tag:
                    netdisk_url = tag['href']
                    index = re.search('url=',netdisk_url).span()
                    netdisk_url = netdisk_url[index[1]:]
                    
                    if re.search('pan.baidu',netdisk_url) == None:
                        continue
                    else:
                        break

                if re.search('pan.baidu',netdisk_url) == None:
                    logger.error("当前书籍页面没有网盘链接")
                    continue
            except:
                logger.error("寻找网盘链接出错")
                continue

            # 寻找网盘提取码
            try:
                secret = soup.find('div',class_='e-secret')
                str_secret = secret.b.text[-4:]
            except:
                logger.error("获取验证码出错")
                continue

            time.sleep(random.choice(range(5,8)))
            # 打开百度网盘链接
            try:
                driver.get(netdisk_url)
            except:
                logger.error("打开网盘链接失败")
                continue

            time.sleep(random.choice(range(5,8)))
            time.sleep(random.choice(range(1,3)))
            try:
                # 填入提取码
                driver.find_element_by_id('shlvGK').send_keys(str_secret)
                
                time.sleep(random.choice(range(1,3)))
                
                # 点击提取文件
                select = driver.find_element_by_class_name('g-button-right')
                driver.execute_script("arguments[0].click();", select)
            except:
                logger.error("操作提取页失败")
                continue
            
            time.sleep(random.choice(range(8,10)))
            time.sleep(random.choice(range(1,3)))

            status = 0

            # 点击文件全选
            try:
                # time.sleep(random.choice(range(1,3)))
                select = driver.find_element_by_class_name('zbyDdwb')
                driver.execute_script("arguments[0].click();", select)
            except:
                try:
                    # time.sleep(random.choice(range(1,3)))
                    # 点击保存到网盘
                    select = driver.find_element_by_class_name('g-button-right')
                    driver.execute_script("arguments[0].click();", select)
                    # 操作完成
                    status = 1
                except:
                    # 出错
                    logger.error('网盘页面操作失败')
                    continue

            if status == 1:
                try:
                    # 点击确定
                    time.sleep(random.choice(range(1,3)))
                    select = driver.find_element_by_css_selector('#fileTreeDialog>div.dialog-footer.g-clearfix>a[title=确定]')
                    driver.execute_script("arguments[0].click();", select)
                except:
                    logger.error('网盘页面操作失败')
                    continue
            else:

                try:
                    # 没有全选 直接点击转存
                    time.sleep(random.choice(range(1,3)))

                    # 点击保存到网盘
                    select = driver.find_element_by_class_name('g-button-right')
                    driver.execute_script("arguments[0].click();", select)
                
                    time.sleep(random.choice(range(1,3)))

                    # 点击确定
                    select = driver.find_element_by_css_selector('#fileTreeDialog>div.dialog-footer.g-clearfix>a[title=确定]')
                    driver.execute_script("arguments[0].click();", select)

                except:
                    logger.error('网盘页面操作失败')
                    continue
def main():
    
    while True:
        print("请输入数字，不同的数字对应不同的方法：")
        print("1.爬取所有的书籍并更新书籍网页链接")
        print("2.爬取网页中的诚通网盘链接")
        print("3.退出程序")
        cmd = input("请输入数字：")
        
        if len(cmd) != 1:
            print('命令输入错误，请重新输入')
            continue
        if cmd not in ['1','2','3']:
            print('命令输入错误，请重新输入')
            continue

        if cmd == '1':
            save_book_url()
            url_del_repeat()
        elif cmd == '2':
            save_book_dl_url()

if __name__ == '__main__':
    main()
