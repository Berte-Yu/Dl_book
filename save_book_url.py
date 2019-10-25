# coding:utf-8

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
from bs4 import BeautifulSoup
import re
import requests
import json


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
        return

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

        time.sleep(3)

def url_del_repeat():
    book_url = []
    with open('book_url.txt','r') as fp:
        while True:
            line = fp.readline()
            if len(line) < 3:
                break
            book_url.append(line)
        book_url = list(set(book_url))

    with open('book_url_1.txt','w') as fp:
        for url in book_url:
            fp.write(url)

if __name__ == '__main__':
    # save_book_url()
    # url_del_repeat()
    pass