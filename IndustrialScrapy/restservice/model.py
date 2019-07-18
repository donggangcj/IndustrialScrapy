#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : model.py
@Author: donggangcj
@Date  : 2018/10/30
@Desc  : 
'''

import datetime

import mongoengine
from mongoengine import StringField, DateTimeField, EmbeddedDocumentField, EmailField, IntField
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer
from flask import current_app

mongoengine.connect('mongoengine_test', host='localhost', port=27017)


class Contact(mongoengine.EmbeddedDocument):
    email = EmailField()
    iphone = StringField()


class User(mongoengine.Document):
    username = StringField(required=True, unique=True)
    age = DateTimeField(required=True)
    password_hash = StringField(required=True)
    # FIXME The EmeddedDocument can be replaced with DictDocument
    contact = EmbeddedDocumentField(Contact)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration=3600):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'username': self.username}).dncode('UTF-8')

    def confirm(self, token):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token).encode('UTF-8')
        except:
            return None
        return self.objects(username=data.get('username'))


class Developer(mongoengine.Document):
    name = StringField(required=True)
    iphone = StringField(required=True)
    permission = IntField(required=True, default=4)
    last_login = DateTimeField(required=True, default=datetime.datetime.now)
