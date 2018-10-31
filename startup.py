#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : startup.py
@Author: donggangcj
@Date  : 2018/10/30
@Desc  : 
'''

import os

from IndustrialScrapy.restservice import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'develop')
