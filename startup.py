#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : startup.py
@Author: donggangcj
@Date  : 2018/10/30
@Desc  : 
'''

import os

from IndustrialScrapy.restservice import create_app, mongo

app = create_app(os.getenv('FLASK_CONFIG') or 'develop')


@app.shell_context_processor
def make_shell_context():
    return dict()

@app.cli.command()
def test():
    import unittest
    test_user_model = unittest.TestLoader.discover()
