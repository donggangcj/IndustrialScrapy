# -*- coding: utf-8 -*-
import math
import re
from datetime import datetime

import scrapy

from IndustrialScrapy.items import IndustrialItem


class AiiAllianceSpider(scrapy.Spider):
    name = 'aii-alliance'

    keys = ['工业互联网', '工业物联网', '工业4.0', '智慧工厂', '智能制造2025']
    url = 'http://www.aii-alliance.org/index.php?m=content&c=search&a=search'

    def start_requests(self):
        for key in self.keys:
            myFormData = {'search': key}
            yield scrapy.FormRequest(url=self.url,
                                     formdata=myFormData,
                                     callback=lambda response, key=key: self.get_page(response, key))

    def get_page(self, response, key):
        total_account = int(
            re.search(re.compile('\d+'), response.xpath('//a[@class="a1"]/text()').extract()[0]).group())
        for page in range(math.ceil(total_account / 20)):
            yield scrapy.Request(dont_filter=True,
                                 url=self.url + '&page={}'.format(page + 1),
                                 callback=lambda inter_response, key=key: self.parse(inter_response, key)
                                 )

    def parse(self, response, key):
        for _ in response.css('ul.download_list li'):
            item_datetime = datetime.strptime(_.css('div.download_list_time::text').extract_first().strip(), '%Y.%m.%d')
            if abs((datetime.utcnow() - item_datetime).days) > 180:
                return
            item = IndustrialItem()
            item['title'] = _.css('h2::text').extract_first()
            item['url'] = _.css('a::attr(href)').extract_first()
            item['time'] = item_datetime
            item['keyword'] = key
            item['origin'] = self.name
            item['area'] = self.name
            yield item
