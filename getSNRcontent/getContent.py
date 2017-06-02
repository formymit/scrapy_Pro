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

url = 'http://www.mongolcnr.cn/contantroot/c/2017/03/23/bc9daa7f-81c1-4b23-b0b6-fca62cba505c.html'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:53.0) Gecko/20100101 Firefox/53.0'
}

spider_queue = MongoQueue('mongolia', 'snr_urls')

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

        all_time = selector.xpath('//p[@style="font-size:20px;text-indent:6em;line-height:29px;"]')
        print(len(all_time))
        if len(all_time) > 0:
            time = all_time[0].xpath('string(.)')
            time = ' '.join(time.split())
            print(time)

        # all_titles = selector.xpath('//h1[@class="main_tit"]')
        all_titles = selector.xpath('//p[@style="font-size:25px;font-weight: 100;line-height:28px;text-shadow:0px 0px 1px #203f7f;text-indent: 2em;margin-top:9px;"]')

        for each in all_titles:
            title_tmp = each.xpath('string(.)')
            title = title + title_tmp
        title = ' '.join(title.split())
        print(title)
        #
        sum_content = ''
        all_content = selector.xpath('//div[@id="htmltext"]//p')
        for each in all_content:
            content = each.xpath('string(.)')
            content = ' '.join(content.split())
            content = '<p>' + content + '</p>'

            sum_content = sum_content + content

        review = ''
        result = '{' + '"title": ' + '"' + title + '", ' + '"url": ' + '"' + url + '", ' + '"review": ' + '"' + review + '", ' + '"content": ' + '"' + sum_content + '", ' + '"time": ' + '"' + time + '", ' + '"type": ' + '"news"' + '}'
        print(result)

        if len(time) > 0:  # there exist data  <p></p>
            with open('snr_Data.txt', 'a') as file:
                file.write(result + '\n')

    except Exception as e:
        print(e)

    return title

def process_crawler():
    process = []
    for i in range(20):
        p = multiprocessing.Process(target=infoCrawler)
        p.start()
        process.append(p)
    for p in process:
        p.join()

if __name__ == '__main__':
    process_crawler()
    # url = 'http://www.mongolcnr.cn/contantroot/c/2017/03/23/bc9daa7f-81c1-4b23-b0b6-fca62cba505c.html'
    # getData(url)

