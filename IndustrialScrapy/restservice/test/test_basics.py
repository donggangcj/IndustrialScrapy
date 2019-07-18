#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : test_basics.py
@Author: donggangcj
@Date  : 2018/10/31
@Desc  : 
'''
import unittest
from flask import current_app
from .. import create_app, mongo


class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
