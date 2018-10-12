#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : app.py.py
@Author: donggangcj
@Date  : 2018/10/11
@Desc  : 
'''

import datetime
import json

from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

from IndustrialScrapy.settings import MONGO_DATABASE, MONGO_URI
from IndustrialScrapy.restservice.util import JSONEncoder, to_json

app = Flask(__name__)
app.config['MONGO_URI'] = MONGO_URI + '/' + MONGO_DATABASE
mongo = PyMongo(app)
app.json_encoder = JSONEncoder


@app.route('/latest', methods=['POST', 'GET'])
def get_latest():
    begin_time = datetime.datetime.now() - datetime.timedelta(weeks=1)  # 七天之前
    dummy_id = ObjectId.from_datetime(begin_time)
    try:
        cursor = mongo.db.industrial.find({'_id': {'$gte': dummy_id}})
    except Exception as e:
        app.logger(e)
        return to_json(500)
    return to_json(200, data=list(cursor))


@app.route('/news', methods=['GET', 'POST'])
def get_news():
    if request.is_json:
        query_filter = request.json
        cursor = mongo.db.industrial.find(query_filter)
        return to_json(200, data=list(cursor))
    else:
        return to_json(501)


if __name__ == '__main__':
    app.run(debug=True)
