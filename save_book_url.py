# coding:utf-8

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
from bs4 import BeautifulSoup
import re
import requests
import json

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

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}

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
    url_del_repeat()