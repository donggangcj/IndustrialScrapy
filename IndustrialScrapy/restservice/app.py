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
from .util import JSONEncoder

app = Flask(__name__)
app.config['MONGO_URI'] = MONGO_URI + '/' + MONGO_DATABASE
mongo = PyMongo(app)
app.json_encoder = JSONEncoder


@app.route('/latest', methods=['POST', 'GET'])
def get_latest():
    begin_time = datetime.datetime.now() - datetime.timedelta(weeks=1)  # 七天之前
    dummy_id = ObjectId.from_datetime(begin_time)
    try:
        cursor = mongo.db.industrial.find({'_id': {'$gte', dummy_id}})
        count = cursor.count()
        data = cursor
    except Exception as e:
        cursor.close()
        return jsonify({'ok', True,'data':})


@app.route('/news', methods=['GET', 'POST'])
def get_news():
    pass
