#!usr/bin/env python3.6  
#-*- coding:utf-8 -*-  
""" 
@author:iBoy 
@file: test.py 
@time: 2017/06/08 
"""
import urllib.request
import requests

data = '羽绒服洗涤'

data = urllib.request.quote(data)
print(data)