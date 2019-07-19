# -*- coding: utf-8 -*-
from urllib.parse import quote

import scrapy


class GongkongSpider(scrapy.Spider):
    # name = 'gongkong'
    # allowed_domains = ['gongkong']
    # start_urls = ['http://gongkong.com/']
    #
    # keys = ['工业互联网', '工业物联网', '工业4.0', '智慧工厂', '智能制造2025']
    #
    # def start_requests(self):
    #     for key in self.keys:
    #         yield scrapy.Request(
    #             url="http://so.gongkong.com/cse/search?q={q}&click=1&s=2183495492050139163&nsid=1".format(quote(key)),
    #             callback=lambda response,key: self.__getattribute__()
    #         )
    #
    #
    # def get
    #
    #
    # def parse(self, response):
    #     pass
    pass
