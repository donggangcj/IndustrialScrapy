# /usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : util.py
@Author: donggangcj
@Date  : 2018/10/12
@Desc  : 
'''

import json
import datetime
from bson.objectid import  ObjectId


class JSONEncoder(json.JSONEncoder):
    """ extend json-encode class"""

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self.o)
