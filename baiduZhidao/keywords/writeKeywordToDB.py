#!usr/bin/env python3.6  
#-*- coding:utf-8 -*-  
""" 
@author:iBoy 
@file: writeKeywordToDB.py 
@time: 2017/06/08 
"""
from mongodb_queue import MongoQueue


spider_queue = MongoQueue('baiduzhidao', 'keywords')

spider_queue.clear()
with open('final_keywords.txt') as f:
    keyword = f.readline()
    while keyword:
        spider_queue.push(keyword)
        keyword = f.readline()

