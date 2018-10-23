# -*- coding: utf-8 -*-
import scrapy


class AliyunSpider(scrapy.Spider):
    name = 'aliyun'
    allowed_domains = ['aliyun']
    start_urls = ['http://aliyun/']

    def parse(self, response):
        pass
