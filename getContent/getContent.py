#!usr/bin/env python3.6  
#-*- coding:utf-8 -*-  
""" 
@author:iBoy 
@file: getContent.py 
@time: 2017/06/02 
"""
import requests
from lxml import etree
from mongodb_queue import MongoQueue
import multiprocessing

url = 'http://mongol.people.com.cn/15660778.html'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:53.0) Gecko/20100101 Firefox/53.0'
}

spider_queue = MongoQueue('mongolia', 'xinhua_urls')

def infoCrawler():
    while True:
        try:
            url = spider_queue.pop()
            print(url)
        except KeyError:
            print('队列没有数据啦')
            break
        else:
            result = getData(url[:-1]) #不能有回车啊~~ 昨天也是这个问题
            # if len(result) == 0:  #很聪明的办法 用title代替 sumContent
            #     #区分没有抓到数据以及本身没有数据 有重置 死循环？ 谨慎重置 不然就是死循环 永远抓不完 如果有isotime 则complete
            #     spider_queue.reset(url)
            # else:
            #     spider_queue.complete(url)

def getData(url):
    try:
        title = ''

        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'

        # print(response.text)

        selector = etree.HTML(response.text)

        all_time = selector.xpath('//span[@class="t02 tb_rl"]')
        print(len(all_time))
        if len(all_time) > 0:
            time = all_time[0].xpath('string(.)')
            time = ' '.join(time.split())
            print(time)

        if len(all_time) == 0:
            all_time = selector.xpath('//table[@class="wbc_lt wbc_bg01 tb_rl wbc01"]//td')

            if len(all_time) == 0:
                all_time = selector.xpath('//td[@class="aaa"]')
                time = all_time[0].xpath('string(.)')
                time = ' '.join(time.split())
                print(time)

            else:
                time = all_time[0].xpath('string(.)')
                time = ' '.join(time.split())
                print(time)



        # all_titles = selector.xpath('//h1[@class="main_tit"]')
        all_titles = selector.xpath('//td[@style="writing-mode:tb-rl;"]')
        if len(all_titles) == 0:
            all_titles = selector.xpath('//h1[@class="mwfwb"]')
            if len(all_titles) == 0:
                all_titles = selector.xpath('//div[@id="p_title"]')

        for each in all_titles:
            title_tmp = each.xpath('string(.)')
            title = title + title_tmp
        title = ' '.join(title.split())
        print(title)
        #
        content = ''
        all_content = selector.xpath('//td[@class="zhengwen"]')
        if len(all_content) == 0:
            all_content = selector.xpath('//h3')
            if len(all_content) == 0:
                all_content = selector.xpath('//table[@class="table_content"]')
                if len(all_content) == 0:
                    all_content = selector.xpath('//div[@id="p_content"]')
        for each in all_content:
            content = each.xpath('string(.)')
            content = ' '.join(content.split())
            print(content)
        review = ''
        result = '{' + '"title": ' + '"' + title + '", ' + '"url": ' + '"' + url[:-1] + '", ' + '"review": ' + '"' + review + '", ' + '"content": ' + '"' + content + '", ' + '"time": ' + '"' + time + '", ' + '"type": ' + '"news"' + '}'
        print(result)

        if len(time) > 0:  # there exist data  <p></p>
            with open('xinhua_Data.txt', 'a') as file:
                file.write(result + '\n')

    except Exception as e:
        print(e)

    return title

def process_crawler():
    process = []
    for i in range(3):
        p = multiprocessing.Process(target=infoCrawler)
        p.start()
        process.append(p)
    for p in process:
        p.join()

if __name__ == '__main__':
    process_crawler()
    # url = 'http://mongol.people.com.cn/15664394.html'
    # url = 'http://mongol.people.com.cn/166861/11748785.html'
    # url = 'http://mongol.people.com.cn/306955/15192092.html'
    # url = 'http://mongol.people.com.cn/80999/6577159.html'
    # getData(url)

