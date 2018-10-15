#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : app.py.py
@Author: donggangcj
@Date  : 2018/10/11
@Desc  : 
'''

import sys
sys.path.append('../../')

import datetime
import os

from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

from IndustrialScrapy.restservice.util import JSONEncoder, to_json, format_return_data

app = Flask(__name__)
MONGO_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
MONGO_DATABASE = os.getenv('MONGODB_DATABASE', 'industry')
app.config['MONGO_URI'] = MONGO_URI + '/' + MONGO_DATABASE
mongo = PyMongo(app)
app.json_encoder = JSONEncoder


@app.route('/latest', methods=['POST', 'GET'])
def get_latest():
    if request.method == 'GET':
        page_number = 0
    else:
        page_number = int(request.json.get('page', 0))
    begin_time = datetime.datetime.now() - datetime.timedelta(weeks=1)  # 一周以内
    dummy_id = ObjectId.from_datetime(begin_time)
    try:
        # FIXME the skip prference is versy pool
        cursor = mongo.db.industrial.find({'_id': {'$gte': dummy_id}}).skip(page_number * 10).limit(10)
    except Exception as e:
        app.logger(e)
        return to_json(500)
    return to_json(200, data=list(map(format_return_data, cursor)))


@app.route('/news', methods=['GET', 'POST'])
def get_news():
    if request.is_json:
        query_filter = request.json
        if query_filter.get('date'):
            for i, value in enumerate(query_filter.get('date')):
                query_filter.get('date')[i] = datetime.datetime.utcfromtimestamp(value)
            time = query_filter.pop('date')
            query_filter['time'] = {
                '$gte': time[0],
                '$lt': time[1]
            }
        # 删除一个item，并且返回value
        page_number = query_filter.pop('page', 0)
        # 拆分查询参数
        cursor = mongo.db.industrial.find(query_filter).sort('_id', -1).skip(page_number * 10).limit(10)
        return to_json(200, data={'items': list(map(format_return_data, cursor)), 'page': page_number})
    else:
        return to_json(501)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
