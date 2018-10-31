#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : app.py.py
@Author: donggangcj
@Date  : 2018/10/11
@Desc  : 
'''

# import sys
# sys.path.append('../../')

import datetime
from math import ceil

from flask import current_app, request
from bson.objectid import ObjectId

from IndustrialScrapy.restservice.common.util import to_json, format_return_data, format_query_data
from .. import mongo
from . import main


@main.route('/industrial/latest', methods=['POST', 'GET'])
def get_latest():
    if request.method == 'GET':
        page_number = 0
    else:
        page_number = int(request.json.get('page', 0))
    begin_time = datetime.datetime.now() - datetime.timedelta(weeks=1)  # 一周以内
    dummy_id = ObjectId.from_datetime(begin_time)
    try:
        counts = mongo.db.industrial.count_documents({'_id': {'$gte': dummy_id}})
        # FIXME the skip prference is versy pool
        cursor = mongo.db.industrial.find({'_id': {'$gte': dummy_id}}).skip(page_number * 10).limit(10)
    except Exception as e:
        current_app.logger(e)
        return to_json(500)
    return to_json(200, data={"items": list(map(format_return_data, cursor)), 'page': ceil(counts / 10)})


@main.route('/industrial/news', methods=['GET', 'POST'])
def get_news():
    print(request.json)
    if request.is_json:
        query_filter = format_query_data(request.json)
        print(query_filter)
        # 删除一个item，并且返回value
        page_number = int(query_filter.pop('page', 0))
        # 拆分查询参数
        cursor = mongo.db.industrial.find(query_filter).sort('_id', -1).skip(page_number * 10).limit(10)
        return to_json(200, data={'items': list(map(format_return_data, cursor)), 'page': page_number})
    else:
        return to_json(501)

