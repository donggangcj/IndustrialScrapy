# -*- coding: utf-8 -*-
from urllib.parse import quote, urlparse, urljoin
import json

import scrapy

from IndustrialScrapy.items import IndustrialItem


class HuodongjiaSpider(scrapy.Spider):
    name = 'huodongjia'
    area = 'huodongjia'
    url = 'https://www.huodongjia.com/search/events/page-{p}/?keyword={key}'
    base_url = '{}://{}'.format(urlparse(url).scheme, urlparse(url).netloc)
    keys = ['工业互联网', '工业物联网', '物联网']
    headers = {"X-Requested-With": "XMLHttpRequest",
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}

    def start_requests(self):
        for key in self.keys:
            yield scrapy.Request(
                dont_filter=True,
                url=self.url.format(p=2, key=quote(key)),
                headers=self.headers,
                callback=lambda response, key=key: self.parse(response, key)
            )

    def parse(self, response, key):
        res = json.loads(response.body).get('events')
        for item in res:
            industry_item = IndustrialItem()
            industry_item['title'] = item.get('event_name')
            industry_item['time'] = item.get('event_rel_time')
            industry_item['area'] = self.area
            industry_item['url'] = urljoin(self.base_url, item.get('event_url'))
            industry_item['nature'] = '活动'
            industry_item['begin_time'] = item.get('event_begin_time')
            industry_item['end_time'] = item.get('event_end_time')
            industry_item['keyword'] = key
            yield industry_item
