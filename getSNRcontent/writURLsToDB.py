#!usr/bin/env python3.6  
#-*- coding:utf-8 -*-  
""" 
@author:iBoy 
@file: writURLsToDB.py 
@time: 2017/05/27 
"""
from mongodb_queue import MongoQueue

spider_queue = MongoQueue('mongolia', 'snr_urls')

# spider_queue.clear()

with open('mongolcnr.txt') as f:
    url = f.readline()
    while url:
        try:
            spider_queue.push(url)
            url = f.readline()
        except Exception as e:
            print(e)



