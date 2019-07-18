#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : config.py
@Author: donggangcj
@Date  : 2018/10/30
@Desc  : 
'''
import os


class Config:
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/industry')
    FLASK_ADMIN_SWATCH = os.getenv('FLASK_ADMIN_SWATCH', 'cerulean')
    SECRET_KEY = os.getenv('SECRET_KEY', 'guss me ')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    pass


config = {
    'develop': DevelopmentConfig,
    'production': ProductionConfig,
    'test': TestingConfig
}
