# -*- coding: utf-8 -*-
import json
from math import ceil

import scrapy
from IndustrialScrapy.items import IndustrialItem


class GongxinbuSpider(scrapy.Spider):
    name = 'gongxinbu'
    area = 'gongxinbu'
    origin = "gongxinbu"
    url = "http://searchweb.miit.gov.cn/search/search"

    keys = ['工业互联网', '工业App']

    def start_requests(self):
        for key in self.keys:
            yield scrapy.FormRequest(
                dont_filter=True,
                url=self.url,
                formdata={"urls": "http://www.miit.gov.cn/", "sortKey": "showTime", "sortFlag": "-1", "sortType": "1",
                          "indexDB": "css", "pageSize": "10", "pageNow": "1", "fullText": key},
                callback=lambda response, key=key: self.get_page(response, key)
            )

    def get_page(self, response, key):
        res = json.loads(response.body.decode())
        totle = int(res.get('total'))
        page_size = int(res.get('pageSize'))
        for i in range(1, ceil(totle / page_size)):
            yield scrapy.FormRequest(
                url=self.url,
                formdata={"urls": "http://www.miit.gov.cn/", "sortKey": "showTime", "sortFlag": "-1", "sortType": "1",
                          "indexDB": "css", "pageSize": "10", "pageNow": str(i), "fullText": key},
                callback=lambda response, key=key: self.parse(response, key)
            )

    def parse(self, response, key):
        res = json.loads(response.body.decode())
        result_array = res.get('array')
        for item in result_array:
            industry_item = IndustrialItem()
            industry_item['url'] = item.get('url')
            industry_item['time'] = item.get('showTime')
            industry_item['title'] = item.get('name')
            industry_item['area'] = self.area
            industry_item['nature'] = None
            industry_item['keyword'] = key
            yield industry_item
