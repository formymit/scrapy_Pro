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

url = 'http://www.holvoo.net/article/articleView.do?id=6ca501e9-1b6f-4ffe-9b51-8077b9d312c8'

headers = {
    # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:53.0) Gecko/20100101 Firefox/53.0'
    'User-Agent': 'IE=EmulateIE9'
}

spider_queue = MongoQueue('mongolia', 'holvoo_urls')

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
            spider_queue.complete(url)

def getData(url):
    try:
        title = ''

        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'

        # print(response.text)

        selector = etree.HTML(response.text)

        all_time = selector.xpath('//h6')
        print(len(all_time))
        if len(all_time) > 0:
            time = all_time[0].xpath('string(.)')
            time = ' '.join(time.split())
            time = time[:16]
            # print(time)

        # all_titles = selector.xpath('//h1[@class="main_tit"]')
        all_titles = selector.xpath('//h3')

        for each in all_titles:
            title_tmp = each.xpath('string(.)')
            title = title + title_tmp
        title = ' '.join(title.split())
        # print(title)

        #
        sum_content = ''
        all_content = selector.xpath('//div[@class="txt"]')

        for each in all_content:
            content = each.xpath('string(.)')
            content = ' '.join(content.split())
            sum_content = sum_content + content

        # print(sum_content)

        sum_review = ''
        all_review = selector.xpath('//div[@class="lybox"]//br/following-sibling::text()')

        for each in all_review:
            review = each
            review = ' '.join(review.split())
            sum_review = sum_review + review

        # print(sum_review)

        #
        result = '{' + '"title": ' + '"' + title + '", ' + '"url": ' + '"' + url + '", ' + '"review": ' + '"' + sum_review + '", ' + '"content": ' + '"' + sum_content + '", ' + '"time": ' + '"' + time + '", ' + '"type": ' + '"blog"' + '}'
        print(result)

        if len(time) > 0:  # there exist data  <p></p>
            with open('holvoo_data02.txt', 'a') as file:
                file.write(result + '\n')

    except Exception as e:
        print(e)

    return title

def process_crawler():
    process = []
    for i in range(50):
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

    # url = 'http://www.holvoo.net/article/articleView.do?id=56dbb6b5-13c4-4bd9-a48c-8c0df195845a'
    # url = 'http://www.holvoo.net:80/article/articleView.do?id=e2e63063-d8a9-400c-8435-d7bbb2549205'
    # url = 'http://www.holvoo.net:80/article/articleView.do?id=de6580e3-fbe9-4644-96f9-f3259348f31b'
    # url = 'http://www.holvoo.net/article/articleView.do?id=6ca501e9-1b6f-4ffe-9b51-8077b9d312c8'
    # url = 'http://www.holvoo.net/article/articleView.do?id=2ab1fce0-8902-4ff2-8e09-9a5807dc4af0'
    #
    #
    # getData(url)



