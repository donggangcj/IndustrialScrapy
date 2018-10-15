# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import quote, urljoin, urlparse
from math import ceil

from IndustrialScrapy.items import IndustrialItem
from ..util import format_return_date


class ZhejiangSpider(scrapy.Spider):
    name = 'zhejiang'
    area = "zhejiang"
    origin = "zhejiang"

    url = 'http://www.zjjxw.gov.cn/jrobot/search.do?webid=1585&pg=12&p={p}&tpl=&category=&q={key}&pq=12&oq=&eq=&doctype=&pos=&od=0&date=&date='
    base_url = '{}://{}'.format(urlparse(url).scheme, urlparse(url).netloc)
    keys = ['工业互联网', '工业App']

    def start_requests(self):
        for key in self.keys:
            yield scrapy.Request(
                dont_filter=True,
                url=self.url.format(p=1, key=quote(key)),
                callback=lambda response, key=key: self.get_page(response, key)
            )

    def get_page(self, response, key):
        page_num = int(response.css('#jsearch-info-box::attr(data-total)').extract_first())
        for i in range(1, ceil(page_num / 12) + 1):
            yield scrapy.Request(
                dont_filter=True,
                url=self.url.format(p=i, key=quote(key)),
                callback=self.parse
            )

    def parse(self, response):
        keyword = response.css('#q::attr(value)').extract_first()
        for item in response.css('div.jsearch-result-box'):
            industrial_item = IndustrialItem()
            industrial_item['title'] = ''.join([item.css('div.jsearch-result-title a::text').extract_first(),
                                                *item.css('div.jsearch-result-title  em::text').extract()])
            industrial_item['url'] = urljoin(self.base_url,
                                             item.css('divjsearch-result-title a::attr(href)').extract_first())
            industrial_item['time'] = format_return_date(
                item.css('span.jsearch-result-date::text').extract_first().split()[0])
            industrial_item['area'] = self.area
            industrial_item['nature'] = None
            industrial_item['origin'] = self.origin
            industrial_item['keyword'] = keyword
            yield industrial_item
