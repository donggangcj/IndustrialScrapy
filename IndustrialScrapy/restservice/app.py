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
from math import ceil

from flask import Flask, request, jsonify, g
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS
from flask_admin import Admin

from IndustrialScrapy.restservice.util import JSONEncoder, to_json, format_return_data, format_query_data

app = Flask(__name__)
MONGO_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
MONGO_DATABASE = os.getenv('MONGODB_DATABASE', 'industry')
app.config['MONGO_URI'] = MONGO_URI + '/' + MONGO_DATABASE
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
mongo = PyMongo(app)
CORS(app)

admin = Admin(app, name='micorblog', template_mode='bootstrap3')

app.json_encoder = JSONEncoder


@app.route('/industrial/latest', methods=['POST', 'GET'])
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
        app.logger(e)
        return to_json(500)
    return to_json(200, data={"items": list(map(format_return_data, cursor)), 'page': ceil(counts / 10)})


@app.route('/industrial/news', methods=['GET', 'POST'])
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


# def get_db():
#     if 'db' not in g:
#         g.db = mongo.db
#     return g.db
#
#
# @app.teardown_appcontext
# def teardown_db():
#     db = g.pop('db', None)
#     if db is not None:
#         db.close()

def make_public_task(task):



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
