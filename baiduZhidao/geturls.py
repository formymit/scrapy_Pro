#!usr/bin/env python3.6  
#-*- coding:utf-8 -*-  
""" 
@author:iBoy 
@file: geturls.py 
@time: 2017/06/08 
"""
import requests
from lxml import etree
import re
import time
import random
import urllib.request
from mongodb_queue import MongoQueue
import multiprocessing
import sys

#
# keyword = '羽绒服洗涤'
# KEYWORD = urllib.request.quote(keyword)



#https://zhidao.baidu.com/search?word=%D3%F0%C8%DE%B7%FE%CF%B4%B5%D3&ie=gbk&site=-1&sites=0&date=0&pn=0
#https://zhidao.baidu.com/search?word=羽绒服洗涤&ie=gbk&site=-1&sites=0&date=0&pn=0
#需要编码 关键词  写一个通用文件 和配置文件

# url= 'https://zhidao.baidu.com/search?word=%D3%F0%C8%DE%B7%FE%CF%B4%B5%D3&ie=gbk&site=-1&sites=0&date=0&pn=0' # 0， 10 ， 20...
# url = 'https://zhidao.baidu.com/search?word=' + KEYWORD + '&ie=gbk&site=-1&sites=0&date=0&pn=0'


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:53.0) Gecko/20100101 Firefox/53.0'
}

spider_queue = MongoQueue('baiduzhidao', 'keywords')

def infoCawler():
    while True:
        try:
            keyword = spider_queue.pop()
            keyword1 = keyword[:-1] # delete \n
            print(keyword1)
        except KeyError:
            print('队列中没有数据啦~')
        else:
            getAllurls(keyword1)
            spider_queue.complete(keyword)


def geturls(url, keyword):
    try:
        total_page = 1
        response = requests.get(url, headers=headers)
        # print(response.encoding)
        response.encoding = 'GB18030'

        selector = etree.HTML(response.text)

        all_titles = selector.xpath('//a[@class="ti"]')  #the same label a
        all_hrefs = selector.xpath('//a[@class="ti"]/@href')  #the same label a
        total_page_str = selector.xpath('//a[@class="pager-last"]/@href')[0]  #有无可能解析不到数据？？


        for i in range(len(all_titles)):
            title = all_titles[i].xpath('string(.)')
            href = all_hrefs[i]
            print(title + ', ' + href)
            with open(keyword+'.txt', 'a') as f:  # keyword optimization
                f.write(title + '\t' + href + '\n')

        #print(total_page_str)
        start = total_page_str.find('&pn=')
        total_page = int(total_page_str[start+4:])
        #print(total_page)

    except Exception as e:
        print('0--' + keyword + str(e))
    return total_page

def geturls1(url, keyword):
    try:
        # total_page = 1
        response = requests.get(url, headers=headers)
        print(response.encoding)
        response.encoding = 'GB18030'

        selector = etree.HTML(response.text)

        all_titles = selector.xpath('//a[@class="ti"]')  #the same label a
        all_hrefs = selector.xpath('//a[@class="ti"]/@href')  #the same label a
        # total_page_str = selector.xpath('//a[@class="pager-last"]/@href')[0]  #有无可能解析不到数据？？


        for i in range(len(all_titles)):
            title = all_titles[i].xpath('string(.)')
            href = all_hrefs[i]
            print(title + ', ' + href)
            with open(keyword+'.txt', 'a') as f:  # keyword optimization
                f.write(title + '\t' + href + '\n')

        #print(total_page_str)
        # start = total_page_str.find('&pn=')
        # total_page = int(total_page_str[start+4:])
        #print(total_page)

    except Exception as e:
        print('0--' + keyword + str(e))
    # return total_page

def getAllurls(keyword):
    try:
        # KEYWORD = keyword

        KEYWORD = urllib.request.quote(keyword.encode('gbk'))  #非常关键的编码问题！！
        url = 'https://zhidao.baidu.com/search?word=' + KEYWORD + '&ie=gbk&site=-1&sites=0&date=0&pn=0'
        print('抓取'+ keyword+'第一页： ' + url)
        total_page = geturls(url, keyword)
        for i in range(1, int(total_page/10) + 2):
            print('正在抓取'+ '"' + keyword+ '"'+ '的%s页'%i)
            url =  'https://zhidao.baidu.com/search?word=' + KEYWORD + '&ie=gbk&site=-1&sites=0&date=0&pn='+str(i*10)
            geturls1(url, keyword)
            time.sleep(1.0+ random.random())
    except Exception as e:
        print('1--', e)

def process_crawler():
    process = []
    for i in range(50):
        p = multiprocessing.Process(target=infoCawler)
        p.start()
        process.append(p)
    for p in process:
        p.join()


if __name__ == '__main__':

    process_crawler()

   #KEYWORD 写入数据库 用多进程
    # getAllurls(KEYWORD)
    # getAllurls('西装怎么洗')

