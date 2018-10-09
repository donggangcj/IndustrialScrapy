# -*- coding: utf-8 -*-

from datetime import datetime
import json

import scrapy
import requests

from IndustrialScrapy.items import IndustrialItem


class SohuSpider(scrapy.Spider):
    name = 'sohu'

    area = 'souhu'
    keys = ["isesol", "富士康beacon", "用友工业互联网", "根云", "航天云网", '工业互联网', '工业App']

    url = "http://search.sohu.com/outer/search/news"
    form_data = {"keyword": {}, "size": "10", "from": {}, "city": "上海市", "SUV": "1802211642505755",
                 "terminalType": "pc", "source": "direct", "queryType": "edit"}

    def start_requests(self):
        for key in self.keys:
            for x in range(0, 180, 10):
                yield scrapy.FormRequest(
                    url=self.url,
                    formdata={"keyword": key, "size": "10", "from": str(x), "city": "上海市", "SUV": "1802211642505755",
                              "terminalType": "pc", "source": "direct", "queryType": "edit"},
                    callback=lambda response, key=key: self.parse(response, key)
                )

    def parse(self, response, key):
        try:
            res = json.loads(response.body.decode())
            for new in res.get('data').get('news'):
                industria_item = IndustrialItem()
                industria_item["title"] = new["title"]
                industria_item["url"] = new["url"]
                industria_item["area"] = self.area
                industria_item["origin"] = new["authorName"]
                industria_item["nature"] = None
                industria_item['time'] = datetime.fromtimestamp(new.get('postTime') / 1000)
                industria_item['keyword'] = key
                yield industria_item
        except Exception as e:
            self.logger('sohu:Fail parsing the response data {}'.format(e))
