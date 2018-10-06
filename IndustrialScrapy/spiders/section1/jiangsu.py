# -*- coding: utf-8 -*-
from urllib.parse import quote
from math import ceil

import scrapy

from IndustrialScrapy.items import IndustrialItem


class JiangsuSpider(scrapy.Spider):
    name = 'jiangsu'
    header = {"User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWe'
                            'bKit/537.36(KHTML, like Gecko) Chrome/6'
                            '3.0.3239.132 Safari/537.36'}
    area = 'jiangsu'
    keys = ['工业App', '工业互联网']

    def start_requests(self):
        for key in self.keys:
            yield scrapy.Request(
                url='http://www.jiangsu.gov.cn/jrobot/search.do?webid=1&analyzeType=1&pg=12&p={p}&tpl=2&category=&q={key}&pos=&od=&date=&date='.format(
                    p=1, key=quote(key)),
                headers=self.header,
                callback=lambda response, key=key: self.get_page(response, key),
                #重复的请求被过滤了，这里第一次获取页面数量，第一页的数据会被过滤
                dont_filter=True
            )

    def get_page(self, response, key):
        _result_num = response.xpath('//div[@id="jsearch-info-box"]/@data-total').extract()[0]
        page = ceil(int(_result_num) / 12)
        for x in range(1, page + 1):
            yield scrapy.Request(
                url='http://www.jiangsu.gov.cn/jrobot/search.do?webid=1&analyzeType=1&pg=12&p={p}&tpl=2&category=&q={key}&pos=&od=&date=&date='.format(
                    p=x, key=quote(key)),
                headers=self.header,
                callback=self.parse
            )

    def parse(self, response):
        key = response.css('#q::attr(value)').extract_first()
        for _ in response.css('div.jsearch-result-box'):
            item = IndustrialItem()
            item['url'] = _.css('div.jsearch-result-url a::text').extract_first()
            item['time'] = _.css('span.jsearch-result-date::text').extract_first()
            item['nature'] = 'None'
            item['title'] = ''.join(_.css('div.jsearch-result-title a::text, em::text').extract())
            item['area'] = self.area
            item['keyword'] = key
            yield item
