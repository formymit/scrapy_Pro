#!usr/bin/env python3.6  
#-*- coding:utf-8 -*-  
""" 
@author:iBoy 
@file: generate_keywords.py 
@time: 2017/06/08 
"""

with open('keywords.txt') as f:
    keyword = f.readline()
    while keyword:
        keyword1 = keyword[:-1] + '洗涤'
        keyword2 = keyword[:-1] + '怎么洗'
        print(keyword1)
        print(keyword2)

        # with open('final_keywords.txt', 'a') as f2:
        #     f2.write(keyword1 + '\n')
        #     f2.write(keyword2 + '\n')

        keyword = f.readline()
