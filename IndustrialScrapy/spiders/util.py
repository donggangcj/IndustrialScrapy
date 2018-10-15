#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : util.py
@Author: donggangcj
@Date  : 2018/10/15
@Desc  : 
'''
import datetime


def format_return_date(datetime_string):
    datetime_string = datetime_string.split()[0]
    # fixme: -1 == True?
    if datetime_string.find('-') > 0:
        result = datetime.datetime.strptime(datetime_string, '%Y-%m-%d')
    else:
        result = datetime.datetime.strptime(datetime_string, '%Y年%m月%d日')
    return result
