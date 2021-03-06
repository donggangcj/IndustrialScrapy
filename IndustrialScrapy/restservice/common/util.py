# /usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : util.py
@Author: donggangcj
@Date  : 2018/10/12
@Desc  : 
'''

import datetime
import json

from bson.objectid import ObjectId
from flask import jsonify

# AREA_MAP = {
#     "shanghai": "上海",
#     "zhejiang": "浙江",
#     "jiangsu": "江苏",
#     "anhui": "安徽",
#     "chanyelianmeng": "工业互联网产业联盟",
#     "gongxinbu": "工信部",
#     "souhu": "搜狐网",
#     "xinhua": "新华网",
#     "shandong": "山东",
#     "beijing": "北京",
#     "guangdong": "广东",
#     "zaoqizhineng": "造奇智能",
#     "huodongjia": "活动家",
#     "huodongxing": "活动行",
#     "netofthings": "物联网世界",
#     "aii-alliance": "工业互联网产业联盟",
#     "ccidnet": "赛迪",
#     "cifexpo": "上海智能工厂",
# }

AREA_MAP = [
    {'text': '物联网世界', 'key': 'netofthings', 'value': 'netofthings'},
    {'text': '工业互联网产业联盟', 'key': 'aii-alliance', 'value': 'aii-alliance'},
    {'text': '赛迪', 'key': 'ccidnet', 'value': 'ccidnet'},
    {'text': '上海智能工厂', 'key': 'cifexpo', 'value': 'cifexpo'},
]


# 转化地址
def format_return_data(item):
    if not isinstance(item, dict):
        return ValueError('The arg must be the dict type')
    # item['area'] = AREA_MAP[item['area']]
    res = list(filter(lambda i: i.get('key') == item['area'], AREA_MAP))
    # if res is None or len(res) == 0:
    #     return None
    item['area'] = res[0].get('text')
    item['id'] = item.pop('_id')
    if item['time'] is not None:
        item['time'] = datetime.datetime.timestamp(item.pop('time'))
    return item


def format_query_data(item):
    if not isinstance(item, dict):
        return ValueError('The arg must be the dict type')
    if item.get('time'):
        for i, value in enumerate(item.get('time')):
            item.get('time')[i] = datetime.datetime.utcfromtimestamp(value)
        time = item.pop('time')
        item['time'] = {
            '$gte': time[0],
            '$lt': time[1]
        }
    if item.get('area'):
        item['area'] = {
            '$in': item.get('area')
        }
    if item.get('key'):
        item['keyword'] = {
            '$in': item.pop('key')
        }
    return item


KEYWORD = ['工业互联网', '工业物联网', '工业4.0', '智慧工厂', 'PAAS平台']

MSG_MAP = {
    200: 'success',
    401: '未提供认证信息',
    402: '认证信息过期，请重新登录',
    403: '错误的认证信息',
    404: '请求内容不存在',
    405: '不允许的操作',
    410: '用户名已存在',
    421: '用户名或密码错误',
    422: '请求缺少必要参数',
    500: '请求错误，请联系管理员',
    501: 'JSON格式错误',
    10000: '目录名已存在',
    10001: '文件传输错误'
}


class JSONEncoder(json.JSONEncoder):
    """ extend json-encode class"""

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self.o)


# 统一格式返回
def to_json(code, data=None):
    return jsonify({
        "code": code,
        "msg": MSG_MAP[code],
        "data": data
    })
