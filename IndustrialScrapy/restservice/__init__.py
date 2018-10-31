#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : __init__.py
@Author: donggangcj
@Date  : 2018/10/12
@Desc  : 
'''

from flask import Flask
from flask_cors import CORS
from config import config
from flask_admin import Admin
from flask_pymongo import PyMongo

from .common.util import JSONEncoder

cors = CORS()
admin = Admin()
mongo = PyMongo()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    cors.init_app(app)
    admin.init_app(app)
    mongo.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api import openapi as api_blueprint
    app.register_blueprint(api_blueprint)

    app.json_encoder = JSONEncoder

    return app
