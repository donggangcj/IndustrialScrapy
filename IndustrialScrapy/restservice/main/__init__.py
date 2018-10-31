#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : __init__.py.py
@Author: donggangcj
@Date  : 2018/10/30
@Desc  : 
'''

from flask import Blueprint

main = Blueprint('main', __name__)

from . import app
