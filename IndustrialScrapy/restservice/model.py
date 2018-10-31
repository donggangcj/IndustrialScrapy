#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : model.py
@Author: donggangcj
@Date  : 2018/10/30
@Desc  : 
'''
import mongoengine
from mongoengine import StringField, DateTimeField, EmbeddedDocumentField, EmailField
from werkzeug.security import generate_password_hash, check_password_hash

mongoengine.connect('mongoengine_test', host='localhost', port=27017)


class Contact(mongoengine.EmbeddedDocument):
    email = StringField()
    iphone = EmailField()


class User(mongoengine.Document):
    username = StringField(required=True)
    age = DateTimeField(required=True)
    password_hash = StringField(required=True)
    contact = EmbeddedDocumentField(Contact)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
