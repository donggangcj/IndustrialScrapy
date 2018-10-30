#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : openapi.py
@Author: donggangcj
@Date  : 2018/10/29
@Desc  : 
'''

from flask import Blueprint

URL_PREFIX = '/api'
open_api = Blueprint('open_api', __name__, url_prefix=URL_PREFIX)


def ping():
    return 'pong'



route = (
    (['ping', '/ping', ping]),
)


def register_route():
    for route_item in route:
        open_api.add_url_rule(route_item[1], view_func=route_item[2], methods=route_item[0])
